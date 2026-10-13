"""Prompt builder + exporter tests."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from ai_gif_studio.config.presets import get_preset
from ai_gif_studio.features.exporter import export_gif
from ai_gif_studio.features.prompt_builder import build_prompt
from ai_gif_studio.models.prompt import Prompt


def test_build_prompt_includes_style_and_preset() -> None:
    p = build_prompt("a cat on a skateboard", "anime", get_preset("bouncy-loop"))
    assert "anime key visual" in p.text
    assert "16 frames" in p.text


def test_prompt_rejects_empty() -> None:
    try:
        Prompt(text="   ").normalized()
    except ValueError:
        return
    raise AssertionError("expected ValueError on empty prompt")


def test_export_gif_writes_file(tmp_path: Path) -> None:
    frames = [Image.fromarray(np.full((8, 8, 3), i, dtype=np.uint8)) for i in range(4)]
    out = export_gif(frames, tmp_path / "clip.gif", fps=12)
    assert out.exists() and out.stat().st_size > 0
    with Image.open(out) as img:
        assert img.format == "GIF"