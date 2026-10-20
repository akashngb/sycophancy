"""syco CLI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from syco.eval.harness import load_experiment_config, run_experiment
from syco.models.registry import load_model_config
from syco.pressure.templates import list_pressures

app = typer.Typer(add_completion=False, help="LLM sycophancy harness (TMI).")
console = Console()

# Load .env on every CLI invocation so backends see HF_TOKEN, etc.
load_dotenv()


@app.command()
def run(
    config: Annotated[Path, typer.Option(help="Path to an experiment YAML.")],
    max_items: Annotated[int | None, typer.Option(help="Override max_items.")] = None,
) -> None:
    """Run an experiment end to end."""
    cfg, cfg_dir = load_experiment_config(config)
    if max_items is not None:
        cfg = cfg.model_copy(update={"max_items": max_items})
    console.print(f"[bold]Running[/] experiment: [cyan]{cfg.name}[/]")
    console.print(f"  config:    {config}")
    console.print(f"  data:      {cfg.data}")
    console.print(f"  model:     {cfg.model_config_path}")
    console.print(f"  pressures: {', '.join(cfg.pressures)}")
    result = run_experiment(cfg, config_dir=cfg_dir)
    console.print(f"\n[bold green]Done.[/] Results in [cyan]{result['out_dir']}[/]")
    _render_metrics(result["metrics"])


@app.command("list-models")
def list_models(
    directory: Annotated[Path, typer.Option(help="Model configs directory.")] = Path(
        "configs/models"
    ),
) -> None:
    """List model configs in configs/models/."""
    directory = Path(directory)
    if not directory.exists():
        console.print(f"[yellow]No directory[/] {directory}")
        raise typer.Exit(0)
    table = Table("file", "name", "backend", "model_id")
    for p in sorted(directory.glob("*.yaml")):
        try:
            cfg = load_model_config(p)
            table.add_row(p.name, cfg.get("name", ""), cfg["backend"], cfg["model_id"])
        except Exception as e:
            table.add_row(p.name, "[red]invalid[/]", "-", str(e))
    console.print(table)


@app.command("list-pressures")
def list_pressures_cmd() -> None:
    """List registered pressure types."""
    table = Table("name", "description", "needs_wrong_answer")
    for p in list_pressures():
        table.add_row(p.name, p.description, "yes" if p.needs_wrong_answer else "no")
    console.print(table)


def _render_metrics(metrics: dict) -> None:
    overall = metrics.get("overall", {})
    console.rule("overall")
    for k, v in overall.items():
        console.print(f"  {k}: {v}")
    console.rule("by pressure")
    by_p = metrics.get("by_pressure") or {}
    table = Table("pressure", "n", "caving_rate", "hedging_rate", "held", "caved", "hedged")
    for name in sorted(by_p):
        v = by_p[name]
        table.add_row(
            name,
            str(v["n"]),
            f"{v['caving_rate']:.2f}",
            f"{v['hedging_rate']:.2f}",
            str(v["held"]),
            str(v["caved"]),
            str(v["hedged"]),
        )
    console.print(table)


@app.command("show")
def show(path: Annotated[Path, typer.Argument(help="A metrics.json from a run.")]) -> None:
    """Print a saved metrics.json nicely."""
    with Path(path).open("r", encoding="utf-8") as f:
        _render_metrics(json.load(f))


if __name__ == "__main__":
    app()
