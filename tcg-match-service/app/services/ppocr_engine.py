"""PP-OCRv4 engine — detection + recognition using PaddlePaddle inference.

Extracted from the original project's script_temp/ppocr_v4_engine.py with
minimal changes: only the import path for OCRResult was adjusted.
"""
import math
import sys
import time
from pathlib import Path
from typing import List, Tuple

import cv2
import numpy as np
import paddle
from rapidocr_onnxruntime.ch_ppocr_v3_det.utils import DBPostProcess, create_operators, transform
from rapidocr_onnxruntime.ch_ppocr_v3_rec.utils import CTCLabelDecode


class OCRResult:
    """A single recognized text block."""
    def __init__(self, text: str, confidence: float, bbox: List[List[float]]):
        self.text = text
        self.confidence = confidence
        self.bbox = bbox


class _PaddleInferSession:
    def __init__(self, model_dir: str, ir_optim: bool = False, threads: int = 4):
        model_dir = Path(model_dir)
        config = paddle.inference.Config(
            str(model_dir / "inference.pdmodel"),
            str(model_dir / "inference.pdiparams"),
        )
        config.disable_gpu()
        config.enable_mkldnn()
        config.set_cpu_math_library_num_threads(threads)
        config.switch_ir_optim(ir_optim)
        config.disable_glog_info()
        config.switch_use_feed_fetch_ops(False)
        self.predictor = paddle.inference.create_predictor(config)
        self.input_names = list(self.predictor.get_input_names())
        self.output_names = list(self.predictor.get_output_names())

    def run(self, feed_dict):
        for name, arr in feed_dict.items():
            self.predictor.get_input_handle(name).copy_from_cpu(arr)
        self.predictor.run()
        return [self.predictor.get_output_handle(n).copy_to_cpu() for n in self.output_names]


class _PPOCRv4Detector:
    _DET_LIMIT_SIDE_LEN = 736
    _DET_THRESH = 0.3
    _DET_BOX_THRESH = 0.5
    _DET_UNCLIP_RATIO = 1.6
    _DET_USE_DILATION = True
    _DET_SCORE_MODE = "fast"

    def __init__(self, model_dir: str, ir_optim: bool = False, threads: int = 4):
        self._session = _PaddleInferSession(model_dir, ir_optim=ir_optim, threads=threads)
        pre_process_list = [
            {"DetResizeForTest": {"limit_side_len": self._DET_LIMIT_SIDE_LEN, "limit_type": "min"}},
            {"NormalizeImage": {"std": [0.229, 0.224, 0.225], "mean": [0.485, 0.456, 0.406],
                                "scale": "1./255.", "order": "hwc"}},
            {"ToCHWImage": None},
            {"KeepKeys": {"keep_keys": ["image", "shape"]}},
        ]
        self._preprocess = create_operators(pre_process_list)
        self._postprocess = DBPostProcess(
            thresh=self._DET_THRESH, box_thresh=self._DET_BOX_THRESH,
            max_candidates=1000, unclip_ratio=self._DET_UNCLIP_RATIO,
            use_dilation=self._DET_USE_DILATION, score_mode=self._DET_SCORE_MODE,
        )

    def __call__(self, img):
        ori_shape = img.shape[:2]
        data = transform({"image": img}, self._preprocess)
        if data is None:
            return np.empty((0, 4, 2), dtype=np.float32), 0.0
        img_tensor, shape_list = data
        img_tensor = np.expand_dims(img_tensor, 0).astype(np.float32)
        shape_list = np.expand_dims(shape_list, 0)
        start = time.perf_counter()
        preds = self._session.run({"x": img_tensor})[0]
        elapsed = time.perf_counter() - start
        boxes = self._postprocess(preds, shape_list)[0]["points"]
        return self._filter_boxes(boxes, ori_shape), elapsed

    @staticmethod
    def _order_points_clockwise(pts):
        xs = pts[np.argsort(pts[:, 0]), :]
        lm = xs[:2]
        lm = lm[np.argsort(lm[:, 1]), :]
        rm = xs[2:]
        rm = rm[np.argsort(rm[:, 1]), :]
        return np.array([lm[0], rm[0], rm[1], lm[1]], dtype="float32")

    @staticmethod
    def _clip_det_res(p, h, w):
        p[:, 0] = np.clip(p[:, 0], 0, w - 1)
        p[:, 1] = np.clip(p[:, 1], 0, h - 1)
        return p

    def _filter_boxes(self, boxes, shape):
        h, w = shape[:2]
        res = []
        for b in boxes:
            b = self._order_points_clockwise(b)
            b = self._clip_det_res(b, h, w)
            rw = int(np.linalg.norm(b[0] - b[1]))
            rh = int(np.linalg.norm(b[0] - b[3]))
            if rw <= 3 or rh <= 3:
                continue
            res.append(b)
        return np.array(res, dtype=np.float32) if res else np.empty((0, 4, 2), dtype=np.float32)


class _PPOCRv4Recognizer:
    _REC_IMG_SHAPE = [3, 48, 320]
    _REC_BATCH_NUM = 6

    def __init__(self, model_dir: str, keys_path: str, ir_optim: bool = False, threads: int = 4):
        self._session = _PaddleInferSession(model_dir, ir_optim=ir_optim, threads=threads)
        self._rec_img_shape = list(self._REC_IMG_SHAPE)
        self._batch_num = self._REC_BATCH_NUM
        self._postprocess = CTCLabelDecode(keys_path)

    def __call__(self, img_list):
        if not img_list:
            return [], 0.0
        width_list = [i.shape[1] / max(i.shape[0], 1) for i in img_list]
        indices = np.argsort(np.array(width_list))
        n = len(img_list)
        rec_res = [("", 0.0)] * n
        total = 0.0
        for beg in range(0, n, self._batch_num):
            end = min(n, beg + self._batch_num)
            bi = indices[beg:end]
            max_wh_ratio = max(
                self._rec_img_shape[2] / self._rec_img_shape[1],
                max(width_list[i] for i in bi),
            )
            norm_batch = np.concatenate([
                self._resize_norm_img(img_list[i], max_wh_ratio)[np.newaxis, :] for i in bi
            ]).astype(np.float32)
            start = time.perf_counter()
            out = self._session.run({"x": norm_batch})[0]
            total += time.perf_counter() - start
            for rno, one in enumerate(self._postprocess(out)):
                rec_res[int(bi[rno])] = one
        return rec_res, total

    def _resize_norm_img(self, img, max_wh_ratio):
        c, h, w = self._rec_img_shape
        w = int(h * max_wh_ratio)
        ih, iw = img.shape[:2]
        rw = w if math.ceil(h * iw / ih) > w else int(math.ceil(h * iw / ih))
        resized = cv2.resize(img, (rw, h)).astype("float32")
        resized = resized.transpose((2, 0, 1)) / 255.0
        resized -= 0.5
        resized /= 0.5
        padded = np.zeros((c, h, w), dtype=np.float32)
        padded[:, :, :rw] = resized
        return padded


def _get_rotate_crop_image(img, box):
    box = box.reshape(-1, 2)
    cw = int(max(np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[2] - box[3])))
    ch = int(max(np.linalg.norm(box[0] - box[3]), np.linalg.norm(box[1] - box[2])))
    pts = np.float32([[0, 0], [cw, 0], [cw, ch], [0, ch]])
    M = cv2.getPerspectiveTransform(box, pts)
    return cv2.warpPerspective(img, M, (cw, ch), borderMode=cv2.BORDER_REPLICATE, flags=cv2.INTER_CUBIC)


class PPOCRv4Engine:
    def __init__(self, det_model_dir: str, rec_model_dir: str, keys_path: str,
                 text_score: float = 0.5, threads: int = 4):
        self.detector = _PPOCRv4Detector(model_dir=det_model_dir, threads=threads)
        self.recognizer = _PPOCRv4Recognizer(model_dir=rec_model_dir, keys_path=keys_path, threads=threads)
        self._text_score = text_score

    def read(self, image: np.ndarray) -> Tuple[List[OCRResult], float]:
        """Run PP-OCRv4 on a BGR image.

        Returns (list of OCRResult, elapsed seconds).
        """
        start = time.perf_counter()
        boxes, _ = self.detector(image)
        if len(boxes) == 0:
            return [], time.perf_counter() - start
        crops = [_get_rotate_crop_image(image, b.astype(np.float32)) for b in boxes]
        rec, _ = self.recognizer(crops)
        elapsed = time.perf_counter() - start
        results = []
        for b, (t, c) in zip(boxes, rec):
            if c >= self._text_score:
                results.append(OCRResult(text=t, confidence=round(float(c), 4), bbox=b.tolist()))
        return results, elapsed