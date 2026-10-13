"""Frame scheduler: decides seeds, steps, and interpolation across the clip."""
from __future__ import annotations

from dataclasses import dataclass

from ai_gif_studio.models.job import GifJob


@dataclass(slots=True)
class FramePlan:
    seeds: list[int]
    steps: int
    interpolate: bool


def plan_frames(job: GifJob, base_steps: int = 24) -> FramePlan:
    """Deterministic seed ladder from a base seed.

    Uses a simple LCG so the same job always produces the same clip.
    """
    seeds: list[int] = []
    s = job.seed & 0xFFFFFFFF
    for _ in range(job.frames):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        seeds.append(s)
    interpolate = job.frames > 16
    return FramePlan(seeds=seeds, steps=base_steps, interpolate=interpolate)