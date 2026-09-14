from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from script_temp.batch_test_recognize_v3 import (
    build_cases,
    call_recognize,
    load_completed_filenames,
    latest_records_by_filename,
    parse_args,
    select_retry_cases,
    summarize_records,
)


class FakeResponse:
    status_code = 200
    ok = True
    text = ""

    def json(self) -> dict:
        return {
            "text": {"state": True, "productId": "123"},
            "priceTrend": [],
            "monitor": {
                "status_match": "matched",
                "strategy": "serial",
                "latency_ms": 123,
            },
        }


class JsonResponse:
    status_code = 200
    ok = True
    text = ""

    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def json(self) -> dict:
        return self.payload


class BatchRecognizeV3Tests(unittest.TestCase):
    def test_cli_defaults_to_local_deployed_recognize_service(self) -> None:
        with patch.object(sys, "argv", ["batch_test_recognize_v3.py"]):
            args = parse_args()

        self.assertEqual(args.base_url, "http://127.0.0.1:8003")

    def test_build_cases_requires_exact_one_to_one_filename_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image_dir = Path(tmp)
            (image_dir / "a.jpg").write_bytes(b"a")
            (image_dir / "b.png").write_bytes(b"b")

            cases = build_cases(
                [("a.jpg", "Pikachu 025/165", 12.3), ("b.png", "Mew ex", 9.1)],
                image_dir,
            )

            self.assertEqual([case.filename for case in cases], ["a.jpg", "b.png"])
            self.assertEqual(cases[0].text, "Pikachu 025/165")

            with self.assertRaisesRegex(ValueError, "duplicate OCR filename"):
                build_cases([("a.jpg", "one", 1), ("a.jpg", "two", 2)], image_dir)

            with self.assertRaisesRegex(ValueError, "mapping mismatch"):
                build_cases([("a.jpg", "one", 1)], image_dir)

    def test_select_retry_cases_uses_only_each_filename_latest_failed_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image_dir = Path(tmp)
            (image_dir / "a.jpg").write_bytes(b"a")
            (image_dir / "b.jpg").write_bytes(b"b")
            cases = build_cases([("a.jpg", "A", 1), ("b.jpg", "B", 1)], image_dir)
            attempts = [
                {"filename": "a.jpg", "error": "connection refused"},
                {"filename": "a.jpg", "error": None, "job_status": "succeeded"},
                {"filename": "b.jpg", "error": "connection reset"},
            ]

            latest = latest_records_by_filename(attempts)
            retry_cases = select_retry_cases(cases, latest)

        self.assertEqual(list(latest), ["a.jpg", "b.jpg"])
        self.assertEqual([case.filename for case in retry_cases], ["b.jpg"])

    def test_call_recognize_posts_image_and_text_to_compatibility_endpoint(self) -> None:
        captured: dict = {}

        def fake_post(url, *, files, data, timeout):
            captured.update(url=url, files=files, data=data, timeout=timeout)
            return FakeResponse()

        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "card.jpg"
            image_path.write_bytes(b"jpeg-bytes")
            record = call_recognize(
                "http://server:8003",
                image_path,
                "Pikachu 025/165",
                timeout=45,
                post=fake_post,
            )

        self.assertEqual(captured["url"], "http://server:8003/v2/recognize")
        self.assertEqual(set(captured["files"]), {"image"})
        self.assertEqual(captured["files"]["image"][0], "card.jpg")
        self.assertEqual(captured["files"]["image"][1], b"jpeg-bytes")
        self.assertEqual(captured["data"], {"text": "Pikachu 025/165"})
        self.assertEqual(captured["timeout"], 45)
        self.assertEqual(record["status_match"], "matched")
        self.assertEqual(record["product_id"], "123")
        self.assertEqual(record["raw_response"]["monitor"]["strategy"], "serial")

    def test_call_recognize_polls_async_job_and_preserves_final_api_response(self) -> None:
        submitted = {"jobId": "job-123", "status": "queued"}
        running = {"jobId": "job-123", "status": "running"}
        succeeded = {
            "jobId": "job-123",
            "status": "succeeded",
            "result": {
                "text": {"state": True, "productId": "987", "cardName": "Mew ex"},
                "priceTrend": [{"soldDate": "2026-09-01", "price": {"raw": 2.5}}],
                "monitor": {"status_match": "matched", "strategy": "serial", "latency_ms": 321},
            },
        }
        poll_responses = iter([running, succeeded])
        requested_urls: list[str] = []

        def fake_post(url, **kwargs):
            requested_urls.append(url)
            return JsonResponse(submitted)

        def fake_get(url, **kwargs):
            requested_urls.append(url)
            return JsonResponse(next(poll_responses))

        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "card.jpg"
            image_path.write_bytes(b"jpeg-bytes")
            try:
                record = call_recognize(
                    "http://server:8003",
                    image_path,
                    "Mew ex 151/165",
                    timeout=45,
                    job_timeout=60,
                    poll_interval=0,
                    post=fake_post,
                    get=fake_get,
                    sleep=lambda _: None,
                )
            except TypeError as exc:
                self.fail(f"async polling arguments are unsupported: {exc}")

        self.assertEqual(
            requested_urls,
            [
                "http://server:8003/v2/recognize",
                "http://server:8003/v2/recognize/jobs/job-123",
                "http://server:8003/v2/recognize/jobs/job-123",
            ],
        )
        self.assertEqual(record["job_id"], "job-123")
        self.assertEqual(record["job_status"], "succeeded")
        self.assertEqual(record["product_id"], "987")
        self.assertEqual(record["submit_response"], submitted)
        self.assertEqual(record["raw_response"], succeeded)
        self.assertEqual(record["raw_response"]["result"]["priceTrend"][0]["price"]["raw"], 2.5)

    def test_load_completed_filenames_ignores_truncated_jsonl_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.jsonl"
            path.write_text(
                json.dumps({"filename": "a.jpg"}) + "\n" + '{"filename":',
                encoding="utf-8",
            )

            self.assertEqual(load_completed_filenames(path), {"a.jpg"})

    def test_call_recognize_keeps_elapsed_time_when_transport_fails(self) -> None:
        def failing_post(*args, **kwargs):
            raise requests.Timeout("timed out")

        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "card.jpg"
            image_path.write_bytes(b"jpeg-bytes")
            with patch("script_temp.batch_test_recognize_v3.time.perf_counter", side_effect=[10.0, 12.5]):
                try:
                    record = call_recognize(
                        "http://server:8003", image_path, "Pikachu", timeout=45, post=failing_post
                    )
                except requests.RequestException as exc:
                    self.fail(f"transport exception escaped: {exc}")

        self.assertFalse(record["http_ok"])
        self.assertEqual(record["elapsed_ms"], 2500.0)
        self.assertEqual(record["error"], "request failed: timed out")

    def test_summarize_records_reports_status_errors_and_latency_percentiles(self) -> None:
        records = [
            {"filename": "a.jpg", "http_ok": True, "status_match": "matched", "elapsed_ms": 100},
            {"filename": "b.jpg", "http_ok": True, "status_match": "candidates", "elapsed_ms": 200},
            {"filename": "c.jpg", "http_ok": False, "error": "timeout", "elapsed_ms": 300},
            {"filename": "d.jpg", "http_ok": True, "status_match": "matched", "elapsed_ms": 400},
        ]

        summary = summarize_records(records, expected_total=4)

        self.assertEqual(summary["processed"], 4)
        self.assertEqual(summary["http_success"], 3)
        self.assertEqual(summary["errors"], 1)
        self.assertEqual(summary["status_match"], {"candidates": 1, "matched": 2})
        self.assertEqual(summary["elapsed_ms"]["p50"], 200.0)
        self.assertEqual(summary["elapsed_ms"]["p95"], 380.0)


if __name__ == "__main__":
    unittest.main()
