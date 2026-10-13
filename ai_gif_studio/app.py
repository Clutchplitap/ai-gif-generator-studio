"""Entry point / bootstrap for the AI GIF generator studio desktop app."""
from __future__ import annotations

import logging
import sys
from pathlib import Path

from ai_gif_studio.config.settings import load_settings
from ai_gif_studio.services.model_registry import ModelRegistry
from ai_gif_studio.services.job_queue import JobQueue
from ai_gif_studio.ui.main_window import MainWindow


def _init_logging(log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s :: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "studio.log", encoding="utf-8"),
            logging.StreamHandler(sys.stderr),
        ],
    )


def main() -> int:
    settings = load_settings()
    _init_logging(settings.paths.log_dir)

    registry = ModelRegistry(settings.paths.models_dir)
    registry.discover()

    queue = JobQueue(max_workers=settings.render.max_workers)

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow(settings=settings, registry=registry, queue=queue)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())