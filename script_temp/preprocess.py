# Shared preprocessing: orientation candidates + model input resize.
from PIL import Image

# (W, H) multiples of 14 to match the DINOv2 ViT-B/14 patch grid.
MODEL_INPUT = (168, 224)


def orientation_candidates(img):
    """Yield plausible upright versions of a card image.

    Portrait images yield themselves; landscape images yield both 90-degree
    rotations so downstream scoring can pick the better one without needing
    an orientation classifier.
    """
    w, h = img.size
    if w > h:
        yield img.rotate(-90, expand=True)
        yield img.rotate(90, expand=True)
    else:
        yield img


def to_model_input(img):
    return img.convert("RGB").resize(MODEL_INPUT, Image.BICUBIC)
