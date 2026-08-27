"""
Benchmark with optimized PP-OCRv4 (smaller det size, more threads)
"""
import json, sys, time
from pathlib import Path
import cv2
_HERE = Path(__file__).resolve().parent
_PROJ = _HERE.parent
if str(_PROJ) not in sys.path:
    sys.path.insert(0, str(_PROJ))
from script_temp.ocr_engine import create_engine
from script_temp.ppocr_v4_engine import PPOCRv4Engine, PPOCRv4Detector, PPOCRv4Recognizer, PaddleInferSession

# Test with optimized settings
test_dir = _PROJ / "test-images"
images = sorted(test_dir.glob("*.jpg"))[:5]

# Original v4
v4_orig = PPOCRv4Engine()

# Optimized v4: smaller det size, more threads
class PaddleInferSessionOptimized:
    def __init__(self, model_dir):
        model_dir = Path(model_dir)
        config = paddle.inference.Config(str(model_dir / "inference.pdmodel"), str(model_dir / "inference.pdiparams"))
        config.disable_gpu()
        config.enable_mkldnn()
        config.set_cpu_math_library_num_threads(8)
        # Try enabling IR optimization
        config.switch_ir_optim(True)
        config.disable_glog_info()
        config.switch_use_feed_fetch_ops(False)
        self.predictor = paddle.inference.create_predictor(config)
        self.output_names = list(self.predictor.get_output_names())
    def run(self, feed_dict):
        for n, a in feed_dict.items():
            self.predictor.get_input_handle(n).copy_from_cpu(a)
        self.predictor.run()
        return [self.predictor.get_output_handle(n).copy_to_cpu() for n in self.output_names]

import paddle
from rapidocr_onnxruntime.ch_ppocr_v3_det.utils import DBPostProcess, create_operators, transform
from rapidocr_onnxruntime.ch_ppocr_v3_rec.utils import CTCLabelDecode

class PPOCRv4DetectorOpt:
    def __init__(self, limit_side_len=512):
        self._session = PaddleInferSessionOptimized(str(_PROJ / "script_temp" / "ppocr_v4_models_extracted" / "ch_PP-OCRv4_det_infer"))
        ops = {
            "DetResizeForTest": {"limit_side_len": limit_side_len, "limit_type": "min"},
            "NormalizeImage": {"std": [0.229, 0.224, 0.225], "mean": [0.485, 0.456, 0.406], "scale": "1./255.", "order": "hwc"},
            "ToCHWImage": None,
            "KeepKeys": {"keep_keys": ["image", "shape"]},
        }
        self._preprocess = create_operators(ops)
        self._postprocess = DBPostProcess(thresh=0.3, box_thresh=0.5, max_candidates=1000, unclip_ratio=1.6, use_dilation=True, score_mode="fast")
    def __call__(self, img):
        ori_shape = img.shape[:2]
        data = transform({"image": img}, self._preprocess)
        if data is None: return np.empty((0,4,2), dtype=np.float32), 0.0
        t, sl = data
        t = np.expand_dims(t, 0).astype(np.float32)
        sl = np.expand_dims(sl, 0)
        start = time.perf_counter()
        preds = self._session.run({"x": t})[0]
        elapsed = time.perf_counter() - start
        boxes = self._postprocess(preds, sl)[0]["points"]
        h, w = ori_shape[:2]
        res = []
        for b in boxes:
            xs = b[np.argsort(b[:,0]), :]
            lm = xs[:2]; lm = lm[np.argsort(lm[:,1]), :]
            rm = xs[2:]; rm = rm[np.argsort(rm[:,1]), :]
            b = np.array([lm[0], rm[0], rm[1], lm[1]], dtype="float32")
            b[:,0] = np.clip(b[:,0], 0, w-1); b[:,1] = np.clip(b[:,1], 0, h-1)
            if int(np.linalg.norm(b[0]-b[1])) > 3 and int(np.linalg.norm(b[0]-b[3])) > 3:
                res.append(b)
        return np.array(res, dtype=np.float32) if res else np.empty((0,4,2), dtype=np.float32), elapsed

import numpy as np
import math

class PPOCRv4RecognizerOpt:
    def __init__(self):
        self._session = PaddleInferSessionOptimized(str(_PROJ / "script_temp" / "ppocr_v4_models_extracted" / "ch_PP-OCRv4_rec_infer"))
        self._rec_img_shape = [3, 48, 320]
        self._batch_num = 6
        self._postprocess = CTCLabelDecode(str(_PROJ / "script_temp" / "ppocr_v4_models_extracted" / "ppocr_keys_v1.txt"))
    def __call__(self, img_list):
        if not img_list: return [], 0.0
        wl = [i.shape[1]/max(i.shape[0],1) for i in img_list]
        idx = np.argsort(np.array(wl))
        n = len(img_list); res = [("",0.0)]*n; total = 0.0
        for beg in range(0, n, self._batch_num):
            end = min(n, beg+self._batch_num); bi = idx[beg:end]
            mwr = max(w/max(h,1) for h,w in (img_list[i].shape[:2] for i in bi))
            nb = np.concatenate([self._resize_norm_img(img_list[i], mwr)[np.newaxis,:] for i in bi]).astype(np.float32)
            start = time.perf_counter()
            out = self._session.run({"x": nb})[0]
            total += time.perf_counter() - start
            for rno, one in enumerate(self._postprocess(out)):
                res[beg+rno] = one
        return res, total
    def _resize_norm_img(self, img, mwr):
        c, h, w = self._rec_img_shape
        w = int(h * mwr)
        ih, iw = img.shape[:2]
        rw = w if math.ceil(h*iw/ih) > w else int(math.ceil(h*iw/ih))
        r = cv2.resize(img, (rw, h)).astype("float32")
        r = r.transpose((2,0,1))/255.0; r -= 0.5; r /= 0.5
        p = np.zeros((c, h, w), dtype=np.float32); p[:,:,:rw] = r; return p

def get_rotate_crop_image(img, box):
    box = box.reshape(-1,2)
    cw = int(max(np.linalg.norm(box[0]-box[1]), np.linalg.norm(box[2]-box[3])))
    ch = int(max(np.linalg.norm(box[0]-box[3]), np.linalg.norm(box[1]-box[2])))
    pts = np.float32([[0,0],[cw,0],[cw,ch],[0,ch]])
    M = cv2.getPerspectiveTransform(box, pts)
    return cv2.warpPerspective(img, M, (cw,ch), borderMode=cv2.BORDER_REPLICATE, flags=cv2.INTER_CUBIC)

class PPOCRv4EngineOpt:
    def __init__(self, limit_side_len=512):
        self.detector = PPOCRv4DetectorOpt(limit_side_len=limit_side_len)
        self.recognizer = PPOCRv4RecognizerOpt()
        self._text_score = 0.5
    def read(self, image):
        start = time.perf_counter()
        boxes, _ = self.detector(image)
        if len(boxes) == 0: return [], time.perf_counter() - start
        crops = [get_rotate_crop_image(image, b.astype(np.float32)) for b in boxes]
        rec, _ = self.recognizer(crops)
        elapsed = time.perf_counter() - start
        res = []
        for b, (t, c) in zip(boxes, rec):
            if c >= self._text_score:
                res.append(__import__("script_temp.ocr_engine", fromlist=["OCRResult"]).OCRResult(text=t, confidence=round(float(c),4), bbox=b.tolist()))
        return res, elapsed

v4_opt = PPOCRv4EngineOpt(limit_side_len=512)

print("Benchmarking optimized PP-OCRv4 (limit_side_len=512, threads=8, ir_optim=True)...")
for idx, img_path in enumerate(images):
    raw = cv2.imread(str(img_path))
    if raw is None: continue
    t0 = time.perf_counter()
    res, el = v4_opt.read(raw)
    t = time.perf_counter() - t0
    print(f"  Image {idx+1}: {t:.3f}s, {len(res)} blocks")
    for r in res[:3]:
        print(f"    [{r.confidence:.2f}] {r.text}")
print("Done")