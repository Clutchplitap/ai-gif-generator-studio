"""Named render presets shipped with the studio."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Preset:
    name: str
    frames: int
    fps: int
    resolution: int
    guidance: float
    coherence: float


PRESETS: dict[str, Preset] = {
    "bouncy-loop": Preset("bouncy-loop", frames=16, fps=12, resolution=512, guidance=7.5, coherence=0.72),
    "cinematic-slow": Preset("cinematic-slow", frames=24, fps=8, resolution=640, guidance=6.0, coherence=0.88),
    "sticker-pop": Preset("sticker-pop", frames=12, fps=16, resolution=384, guidance=9.0, coherence=0.55),
    "wallpaper-drift": Preset("wallpaper-drift", frames=32, fps=10, resolution=768, guidance=5.5, coherence=0.91),
}


def get_preset(name: str) -> Preset:
    try:
        return PRESETS[name]
    except KeyError as exc:
        raise ValueError(f"unknown preset: {name!r}; known={sorted(PRESETS)}") from exc