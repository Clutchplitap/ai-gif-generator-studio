# Contributing to ai-gif-generator-studio

Thanks for wanting to push frames. This project is a Windows-first desktop
studio that turns a text prompt (or an image + prompt) into an animated GIF
using a diffusion pipeline with temporal coherence sampling.

## Ground rules

- Python 3.11+ on Windows 10/11 (x64). CUDA 12.1+ recommended; CPU path exists but is slow.
- One feature per PR. Keep diffs scoped.
- Run `ruff check .` and `pytest -q` before opening a PR.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m ai_gif_studio.app
```

## Where things live

- `ai_gif_studio/pipeline/` — the diffusion + temporal-coherence core.
- `ai_gif_studio/features/` — user-facing feature modules (prompt, post, export).
- `ai_gif_studio/services/` — long-lived services (model registry, job queue, cache).
- `ai_gif_studio/handlers/` — CLI + IPC command handlers.
- `ai_gif_studio/ui/` — PySide6 desktop shell.

## Commit style

`area: short imperative summary` — e.g. `pipeline: fix frame drift at 24fps`.

## Reporting bugs

Open an issue with: OS build, GPU + driver, model checkpoint, prompt, seed,
frame count, and the exact command you ran. Attach the `.log` from `logs/`.