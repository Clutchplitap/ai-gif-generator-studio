"""Temporal coherence: blends consecutive frames to reduce flicker."""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def optical_blend(prev: np.ndarray, cur: np.ndarray, alpha: float) -> np.ndarray:
    """Linear blend in float32; alpha=0 -> prev, alpha=1 -> cur."""
    a = np.clip(alpha, 0.0, 1.0)
    return (prev.astype(np.float32) * (1 - a) + cur.astype(np.float32) * a).astype(np.uint8)


def stabilize(frames: Sequence[np.ndarray], coherence: float) -> list[np.ndarray]:
    """Apply forward coherence pass. Higher coherence -> stronger pull to prev."""
    if not frames:
        return []
    alpha = 1.0 - max(0.0, min(coherence, 0.98))
    out = [frames[0]]
    for cur in frames[1:]:
        out.append(optical_blend(out[-1], cur, alpha))
    return out