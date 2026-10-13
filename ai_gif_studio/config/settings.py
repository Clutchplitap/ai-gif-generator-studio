"""Typed settings loader. Reads config/default.toml + config/local.toml overlay."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


@dataclass(slots=True, frozen=True)
class Paths:
    models_dir: Path
    outputs_dir: Path
    cache_dir: Path
    log_dir: Path


@dataclass(slots=True, frozen=True)
class Render:
    max_workers: int = 2
    default_frames: int = 16
    default_fps: int = 12
    max_resolution: int = 768
    vram_budget_mb: int = 8192


@dataclass(slots=True, frozen=True)
class Settings:
    paths: Paths
    render: Render = field(default_factory=Render)
    default_model: str = "sd15-gif-lora"
    device: str = "cuda"


def _read_toml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def load_settings() -> Settings:
    base = _read_toml(CONFIG_DIR / "default.toml")
    overlay = _read_toml(CONFIG_DIR / "local.toml")
    merged = {**base, **overlay}

    root = Path(merged.get("root", Path.home() / "ai-gif-studio"))
    paths = Paths(
        models_dir=root / "models",
        outputs_dir=root / "outputs",
        cache_dir=root / "cache",
        log_dir=root / "logs",
    )
    render = Render(**(merged.get("render") or {}))
    return Settings(
        paths=paths,
        render=render,
        default_model=merged.get("default_model", "sd15-gif-lora"),
        device=merged.get("device", "cuda"),
    )