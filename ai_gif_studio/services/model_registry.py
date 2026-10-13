"""Discovers model checkpoints under models_dir and validates manifests."""
from __future__ import annotations

import hashlib
import logging
import tomllib
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)


@dataclass(slots=True, frozen=True)
class Checkpoint:
    name: str
    path: Path
    sha256: str
    family: str


class ModelRegistry:
    def __init__(self, models_dir: Path) -> None:
        self.models_dir = models_dir
        self._checkpoints: dict[str, Checkpoint] = {}

    def discover(self) -> None:
        self._checkpoints.clear()
        manifest = self.models_dir / "manifest.toml"
        if not manifest.exists():
            log.warning("no model manifest at %s", manifest)
            return
        with manifest.open("rb") as fh:
            data = tomllib.load(fh)
        for name, meta in (data.get("checkpoints") or {}).items():
            self._checkpoints[name] = Checkpoint(
                name=name,
                path=self.models_dir / meta["file"],
                sha256=meta.get("sha256", ""),
                family=meta.get("family", "sd15"),
            )

    def get(self, name: str) -> Checkpoint:
        if name not in self._checkpoints:
            raise KeyError(f"unknown checkpoint {name!r}; known={sorted(self._checkpoints)}")
        return self._checkpoints[name]

    def verify(self, name: str) -> bool:
        ckpt = self.get(name)
        if not ckpt.path.exists() or not ckpt.sha256:
            return False
        digest = hashlib.sha256()
        with ckpt.path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                digest.update(chunk)
        return digest.hexdigest() == ckpt.sha256