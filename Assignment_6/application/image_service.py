"""Extract transparent, reproducible image features from local PNG/JPEG files.

This is a handcrafted visual descriptor, not a pretrained AI embedding. It
compares foreground colors and a coarse spatial silhouette. The image file is
actually read and encoded for every image search.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


class ImageService:
    def encode(self, image_path: str | Path) -> np.ndarray:
        path = Path(image_path)
        if not path.is_file():
            raise FileNotFoundError(f"Image not found: {path}")
        with Image.open(path) as source:
            image = source.convert("RGB").resize((96, 96), Image.Resampling.LANCZOS)
        pixels = np.asarray(image, dtype=np.float32) / 255.0
        # Sample artwork uses a white background. Distance from white keeps
        # background pixels from dominating the comparison.
        difference = 1.0 - pixels
        mask = (np.max(difference, axis=2) > 0.10).astype(np.float32)
        if float(mask.sum()) < 30:
            raise ValueError(f"Image has too little visible foreground: {path}")

        # Preserve color and shape in a small spatial grid.
        color_grid = difference.reshape(12, 8, 12, 8, 3).mean(axis=(1, 3)).ravel()
        shape_grid = mask.reshape(12, 8, 12, 8).mean(axis=(1, 3)).ravel()
        foreground_mean = (difference * mask[..., None]).sum(axis=(0, 1)) / mask.sum()
        foreground_fraction = np.array([mask.mean()], dtype=np.float32)
        vector = np.concatenate(
            [color_grid * 2.2, shape_grid * 0.35, foreground_mean * 3.0, foreground_fraction]
        ).astype(np.float32)
        norm = float(np.linalg.norm(vector))
        return vector / norm if norm else vector
