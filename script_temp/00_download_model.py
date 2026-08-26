"""One-time download of DINOv2 ViT-B/14 weights via torch.hub (~330MB)."""
import torch

model = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14')
print('loaded OK:', type(model).__name__)
