"""Post-processing: palette quantization, dithering, loop trimming."""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from PIL import Image


def to_gif_frames(arrays: Sequence[np.ndarray]) -> list[Image.Image]:
    return [Image.fromarray(a).convert("P", palette=Image.ADAPTIVE, colors=256) for a in arrays]


def trim_loop(frames: list[Image.Image], drop: int = 1) -> list[Image.Image]:
    """Drop the tail frames that typically cause a visible loop pop."""
    if len(frames) <= drop + 1:
        return frames
    return frames[:-drop]