"""Prompt + negative-prompt model with light sanitization."""
from __future__ import annotations

from dataclasses import dataclass

MAX_PROMPT_CHARS = 1200


@dataclass(slots=True, frozen=True)
class Prompt:
    text: str
    negative: str = "blurry, watermark, text, low quality, jpeg artifacts"
    weight: float = 1.0

    def normalized(self) -> "Prompt":
        text = " ".join(self.text.strip().split())[:MAX_PROMPT_CHARS]
        if not text:
            raise ValueError("prompt text is empty after normalization")
        neg = " ".join(self.negative.strip().split())[:MAX_PROMPT_CHARS]
        return Prompt(text=text, negative=neg, weight=max(0.1, min(self.weight, 2.0)))