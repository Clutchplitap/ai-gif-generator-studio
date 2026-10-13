"""Compose final prompts from user text + style tags + preset modifiers."""
from __future__ import annotations

from ai_gif_studio.config.presets import Preset
from ai_gif_studio.models.prompt import Prompt

STYLE_TAGS: dict[str, str] = {
    "anime": "anime key visual, cel shading, clean lineart",
    "pixel": "pixel art, 16-bit palette, crisp dithering",
    "clay": "claymation, stop-motion, soft studio light",
    "neon": "neon cyberpunk, volumetric glow, rain-slick streets",
}


def build_prompt(user_text: str, style: str | None, preset: Preset | None) -> Prompt:
    parts = [user_text.strip()]
    if style and style in STYLE_TAGS:
        parts.append(STYLE_TAGS[style])
    if preset is not None:
        parts.append(f"loop-friendly, {preset.frames} frames, {preset.fps}fps")
    return Prompt(text=", ".join(p for p in parts if p)).normalized()