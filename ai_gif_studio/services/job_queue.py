"""Thread-pool job queue for render jobs."""
from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from ai_gif_studio.models.job import GifJob, JobState

log = logging.getLogger(__name__)


@dataclass(slots=True)
class JobHandle:
    job: GifJob
    future: object


class JobQueue:
    def __init__(self, max_workers: int = 2) -> None:
        self._pool = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="gif-render")
        self._lock = threading.Lock()
        self._active: dict[str, JobHandle] = {}

    def submit(self, job: GifJob, fn: Callable[[GifJob], None]) -> JobHandle:
        def _wrapped() -> None:
            job.state = JobState.RENDERING
            try:
                fn(job)
                job.state = JobState.DONE
                job.progress = 1.0
            except Exception as exc:  # noqa: BLE001
                job.state = JobState.FAILED
                job.error = str(exc)
                log.exception("job %s failed", job.id)

        with self._lock:
            fut = self._pool.submit(_wrapped)
            handle = JobHandle(job=job, future=fut)
            self._active[job.id] = handle
            return handle

    def cancel(self, job_id: str) -> bool:
        with self._lock:
            handle = self._active.get(job_id)
        if handle is None:
            return False
        handle.job.state = JobState.CANCELLED
        return bool(handle.future.cancel())

    def shutdown(self, wait: bool = True) -> None:
        self._pool.shutdown(wait=wait)