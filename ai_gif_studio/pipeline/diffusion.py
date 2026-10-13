"""Diffusion wrapper around a diffusers text-to-image pipeline with GIF sampling."""
from __future__ import annotations

import logging
from dataclasses import dataclass

import torch

log = logging.getLogger(__name__)


@dataclass(slots=True)
class DiffusionConfig:
    model_id: str
    device: str = "cuda"
    dtype: str = "float16"
    enable_xformers: bool = True


class DiffusionEngine:
    """Loads a diffusers pipeline and exposes per-frame latent sampling.

    Note: v0.30+ of diffusers moved `enable_attention_slicing` behind a
    deprecation shim; we call the new `set_attention_slice` path directly.
    """

    def __init__(self, cfg: DiffusionConfig) -> None:
        self.cfg = cfg
        self._pipe = None

    def load(self) -> None:
        from diffusers import StableDiffusionPipeline  # lazy: heavy import

        dtype = getattr(torch, self.cfg.dtype)
        self._pipe = StableDiffusionPipeline.from_pretrained(
            self.cfg.model_id, torch_dtype=dtype, safety_checker=None
        ).to(self.cfg.device)
        if self.cfg.enable_xformers and self.cfg.device == "cuda":
            try:
                self._pipe.enable_xformers_memory_efficient_attention()
            except Exception as exc:  # noqa: BLE001 — xformers optional
                log.warning("xformers unavailable, falling back: %s", exc)

    @property
    def pipe(self):
        if self._pipe is None:
            raise RuntimeError("DiffusionEngine.load() must be called first")
        return self._pipe

    @torch.inference_mode()
    def sample_frame(self, prompt: str, negative: str, seed: int, steps: int = 24):
        generator = torch.Generator(device=self.cfg.device).manual_seed(seed)
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative,
            num_inference_steps=steps,
            generator=generator,
        )
        return result.images[0]