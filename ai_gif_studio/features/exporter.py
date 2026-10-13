"""GIF / MP4 export with atomic writes."""
from __future__ import annotations

import os
import tempfile
from collections.abc import Sequence
from pathlib import Path

from PIL import Image


def export_gif(frames: Sequence[Image.Image], out_path: Path, fps: int, loop: int = 0) -> Path:
    """Write a GIF atomically: temp file then os.replace."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    duration_ms = int(1000 / max(fps, 1))
    fd, tmp = tempfile.mkstemp(suffix=".gif", dir=out_path.parent)
    os.close(fd)
    tmp_path = Path(tmp)
    try:
        first, *rest = frames
        first.save(
            tmp_path,
            save_all=True,
            append_images=rest,
            duration=duration_ms,
            loop=loop,
            optimize=True,
        )
        os.replace(tmp_path, out_path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
    return out_path