#!/usr/bin/env python3
"""Select a local card image and call the TCG recognize service."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from tkinter import Tk, filedialog

import requests


def select_image() -> Path | None:
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected = filedialog.askopenfilename(
        title="Select a card image",
        filetypes=[("Images", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*")],
    )
    root.destroy()
    return Path(selected) if selected else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Call the TCG recognize API with a local image")
    parser.add_argument("image", nargs="?", type=Path, help="local image path; opens a file picker when omitted")
    parser.add_argument("--base-url", default="http://127.0.0.1:8003", help="service base URL")
    parser.add_argument("--strategy", choices=("serial", "fusion"), default="serial")
    parser.add_argument("--text", help="optional multiline OCR text")
    parser.add_argument("--confidence", type=float, help="optional confidence from 0 to 1")
    parser.add_argument("--timeout", type=float, default=180.0, help="request timeout in seconds")
    args = parser.parse_args()
    if args.confidence is not None and not 0 <= args.confidence <= 1:
        parser.error("--confidence must be between 0 and 1")

    image_path = args.image or select_image()
    if image_path is None:
        print("No image selected.")
        return 1
    if not image_path.is_file():
        parser.error(f"image does not exist: {image_path}")

    url = f"{args.base_url.rstrip('/')}/v2/recognize/{args.strategy}"
    data = {}
    if args.text is not None:
        data["text"] = args.text
    if args.confidence is not None:
        data["confidence"] = str(args.confidence)

    print(f"POST {url}")
    print(f"Image: {image_path}")
    with image_path.open("rb") as image_file:
        response = requests.post(
            url,
            files={"image": (image_path.name, image_file)},
            data=data,
            timeout=args.timeout,
        )

    print(f"HTTP {response.status_code}")
    try:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except ValueError:
        print(response.text)
    return 0 if response.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
