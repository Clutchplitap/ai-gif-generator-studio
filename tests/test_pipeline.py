"""Pipeline + post-process tests."""
from __future__ import annotations

import numpy as np

from ai_gif_studio.features.post_process import trim_loop
from ai_gif_studio.pipeline.coherence import optical_blend, stabilize
from ai_gif_studio.pipeline.sampler import plan_frames
from ai_gif_studio.models.job import GifJob


def _solid(value: int, shape=(8, 8, 3)) -> np.ndarray:
    return np.full(shape, value, dtype=np.uint8)


def test_optical_blend_endpoints() -> None:
    a, b = _solid(0), _solid(255)
    assert np.array_equal(optical_blend(a, b, 0.0), a)
    assert np.array_equal(optical_blend(a, b, 1.0), b)


def test_stabilize_pulls_toward_prev() -> None:
    frames = [_solid(0), _solid(255), _solid(255)]
    out = stabilize(frames, coherence=0.9)
    assert out[1].mean() < 255


def test_plan_frames_deterministic() -> None:
    job = GifJob(prompt="x", frames=8, fps=12, resolution=256, seed=6767, model="sd15-gif-lora")
    a = plan_frames(job)
    b = plan_frames(job)
    assert a.seeds == b.seeds
    assert len(a.seeds) == 8


def test_trim_loop_keeps_short_clips() -> None:
    from PIL import Image

    frames = [Image.new("P", (4, 4)) for _ in range(2)]
    assert len(trim_loop(frames)) == 2