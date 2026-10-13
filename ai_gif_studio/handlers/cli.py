"""Typer-based CLI: `ai-gif-studio render --prompt ... --frames ...`."""
from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from ai_gif_studio.config.presets import get_preset
from ai_gif_studio.models.job import GifJob

app = typer.Typer(help="AI GIF generator studio — CLI renderer.")
console = Console()


@app.command()
def render(
    prompt: str = typer.Option(..., "--prompt", "-p"),
    frames: int = typer.Option(16, "--frames"),
    fps: int = typer.Option(12, "--fps"),
    resolution: int = typer.Option(512, "--res"),
    seed: int = typer.Option(6767, "--seed"),
    preset: str | None = typer.Option(None, "--preset"),
    model: str = typer.Option("sd15-gif-lora", "--model"),
    out: Path = typer.Option(Path("outputs/out.gif"), "--out", "-o"),
) -> None:
    if preset:
        p = get_preset(preset)
        frames, fps, resolution = p.frames, p.fps, p.resolution
    job = GifJob(prompt=prompt, frames=frames, fps=fps, resolution=resolution, seed=seed, model=model)
    console.print(f"[bold]queued[/] job {job.id} — {frames}f @ {fps}fps, {resolution}px")
    console.print(f"→ {out}")


if __name__ == "__main__":
    app()