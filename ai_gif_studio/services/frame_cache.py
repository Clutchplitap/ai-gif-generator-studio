"""LRU disk cache for rendered frames keyed by (prompt, seed, step)."""
from __future__ import annotations

import hashlib
from collections import OrderedDict
from pathlib import Path

import numpy as np


class FrameCache:
    def __init__(self, cache_dir: Path, capacity: int = 256) -> None:
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.capacity = capacity
        self._index: OrderedDict[str, Path] = OrderedDict()

    @staticmethod
    def key(prompt: str, seed: int, step: int, resolution: int) -> str:
        raw = f"{prompt}|{seed}|{step}|{resolution}".encode()
        return hashlib.blake2b(raw, digest_size=16).hexdigest()

    def get(self, key: str) -> np.ndarray | None:
        path = self._index.get(key)
        if path is None or not path.exists():
            return None
        self._index.move_to_end(key)
        return np.load(path)

    def put(self, key: str, frame: np.ndarray) -> None:
        path = self.cache_dir / f"{key}.npy"
        np.save(path, frame)
        self._index[key] = path
        self._index.move_to_end(key)
        while len(self._index) > self.capacity:
            _, old = self._index.popitem(last=False)
            old.unlink(missing_ok=True)