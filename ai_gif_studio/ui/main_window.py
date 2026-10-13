"""Main desktop window: prompt panel, preview, render queue."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ai_gif_studio.config.settings import Settings
from ai_gif_studio.services.job_queue import JobQueue
from ai_gif_studio.services.model_registry import ModelRegistry


class MainWindow(QMainWindow):
    def __init__(self, settings: Settings, registry: ModelRegistry, queue: JobQueue) -> None:
        super().__init__()
        self.settings = settings
        self.registry = registry
        self.queue = queue
        self.setWindowTitle("AI GIF Generator Studio")
        self.resize(1080, 720)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QWidget()
        outer = QHBoxLayout(root)

        left = QVBoxLayout()
        left.addWidget(QLabel("Prompt"))
        self.prompt_input = QLineEdit()
        left.addWidget(self.prompt_input)

        left.addWidget(QLabel("Frames"))
        self.frames_spin = QSpinBox()
        self.frames_spin.setRange(4, 64)
        self.frames_spin.setValue(self.settings.render.default_frames)
        left.addWidget(self.frames_spin)

        self.render_btn = QPushButton("Render GIF")
        self.render_btn.clicked.connect(self._on_render)
        left.addWidget(self.render_btn)
        left.addStretch(1)

        right = QVBoxLayout()
        right.addWidget(QLabel("Queue"))
        self.queue_list = QListWidget()
        right.addWidget(self.queue_list)

        outer.addLayout(left, 2)
        outer.addLayout(right, 3)
        self.setCentralWidget(root)

    def _on_render(self) -> None:
        text = self.prompt_input.text().strip()
        if not text:
            return
        self.queue_list.addItem(f"queued: {text[:48]}")