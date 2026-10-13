"""Job + frame data models."""
from __future__ import annotations

import enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


class JobState(str, enum.Enum):
    QUEUED = "queued"
    RENDERING = "rendering"
    POST = "post"
    DONE = "done"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(slots=True)
class GifJob:
    prompt: str
    frames: int
    fps: int
    resolution: int
    seed: int
    model: str
    preset: str | None = None
    init_image: str | None = None
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    state: JobState = JobState.QUEUED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    progress: float = 0.0
    error: str | None = None

    @property
    def duration_ms(self) -> int:
        return int(1000 * self.frames / max(self.fps, 1))