import re

path = r'D:\Code2026\tcg-embedding-service\app\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update import: add preprocess_query_ocr
old_import = 'from preprocess import orientation_candidates, to_model_input, preprocess_query'
new_import = 'from preprocess import orientation_candidates, to_model_input, preprocess_query, preprocess_query_ocr'
content = content.replace(old_import, new_import)

# 2. Remove ocr_preprocessor from global line
old_global = 'global ocr_engine, ocr_preprocessor'
new_global = 'global ocr_engine'
content = content.replace(old_global, new_global)

# 3. Remove OCR preprocessor loading
old_prep = (
    '    log.info("Loading OCR preprocessor...")\n'
    '    ocr_preprocessor = OCRPreprocessor(max_dim=1200)\n'
    '    log.info("OCR preprocessor loaded")'
)
content = content.replace(old_prep, '')

# 4. Change preprocess_query to preprocess_query_ocr in OCR route
# The specific location is after img.load() near the OCR route
old_pp = '        img.load()\n    img = preprocess_query(img)'
new_pp = '        img.load()\n    img = preprocess_query_ocr(img)'
content = content.replace(old_pp, new_pp)

# 5. Replace BGR conversion and remove redundant OCR preprocessor
old_bgr = (
    '    # Convert PIL (RGB) to BGR numpy array for OpenCV\n'
    '    img_np = np.array(img)\n'
    '    if img_np.ndim == 2:\n'
    '        img_bgr = np.stack([img_np] * 3, axis=-1)\n'
    '    elif img_np.shape[2] == 4:\n'
    '        img_bgr = img_np[:, :, :3][:, :, ::-1]\n'
    '    elif img_np.shape[2] == 3:\n'
    '        img_bgr = img_np[:, :, ::-1]\n'
    '    else:\n'
    '        img_bgr = img_np\n'
    '\n'
    '    # Preprocess for better OCR accuracy\n'
    '    img_pp = ocr_preprocessor.preprocess(img_bgr)\n'
    '\n'
    '    # Convert preprocessed image to base64 (BGR -> RGB -> JPEG)\n'
    '    _img_rgb = img_pp[:, :, ::-1]'
)
new_bgr = (
    '    # Convert PIL (RGB) to BGR numpy array for OpenCV\n'
    '    img_np = np.array(img)\n'
    '    if img_np.ndim == 2:\n'
    '        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR)\n'
    '    elif img_np.shape[2] == 4:\n'
    '        img_bgr = img_np[:, :, :3][:, :, ::-1]\n'
    '    elif img_np.shape[2] == 3:\n'
    '        img_bgr = img_np[:, :, ::-1]\n'
    '    else:\n'
    '        img_bgr = img_np\n'
    '\n'
    '    # Convert preprocessed image to base64 (BGR -> RGB -> JPEG)\n'
    '    _img_rgb = img_bgr[:, :, ::-1]'
)
content = content.replace(old_bgr, new_bgr)

# 6. Replace img_pp with img_bgr in OCR engine call
content = content.replace('results, elapsed = ocr_engine.read(img_pp)', 'results, elapsed = ocr_engine.read(img_bgr)')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
