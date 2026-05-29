"""Typer command line interface."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

import typer

from landmark_nav.clients.mock import MockAmapClient
from landmark_nav.eval.run_eval import build_eval_report
from landmark_nav.parsers.route_parser import parse_amap_route
from landmark_nav.pipeline.artifacts import write_json
from landmark_nav.pipeline.mock_pipeline import run_mock_pipeline

app = typer.Typer(help="Amap landmark-aware navigation simulator.")
debug_app = typer.Typer(help="Debug individual pipeline phases.")
app.add_typer(debug_app, name="debug")


@app.command("run-mock")
def run_mock(
    sample: Annotated[
        Path,
        typer.Option(help="Mock Amap route JSON sample."),
    ] = Path("data/mock/route_bicycling_sample.json"),
    out_dir: Annotated[
        Path,
        typer.Option("--out-dir", "--output-dir", help="Directory for generated artifacts."),
    ] = Path("outputs/mock_demo"),
    interval_meters: Annotated[float, typer.Option(help="GPS sampling interval in meters.")] = 50.0,
    trigger_distance: Annotated[
        float, typer.Option(help="Event pre-trigger distance in meters.")
    ] = 80.0,
    top_k: Annotated[int, typer.Option(help="Number of landmark candidates per event.")] = 3,
    visualize: Annotated[
        bool, typer.Option(help="Generate GeoJSON and HTML visualization files.")
    ] = True,
    strict: Annotated[
        bool, typer.Option(help="Return non-zero if no events or instructions are generated.")
    ] = False,
) -> None:
    """Run the complete offline mock pipeline."""
    result = run_mock_pipeline(
        sample=sample,
        out_dir=out_dir,
        interval_meters=interval_meters,
        trigger_distance_meters=trigger_distance,
        top_k=top_k,
        visualize=visualize,
    )
    typer.echo("Generated artifacts:")
    for name, value in result.artifacts.model_dump().items():
        if value is not None:
            typer.echo(f"- {name}: {value}")
    if strict and (not result.events or not result.instructions):
        raise typer.Exit(code=2)


@app.command("eval")
def eval_command(
    mock: Annotated[bool, typer.Option("--mock", help="Use mock fixtures.")] = True,
    fixtures: Annotated[Path, typer.Option(help="Fixture directory.")] = Path("tests/fixtures"),
    output: Annotated[Path, typer.Option(help="Evaluation report path.")] = Path(
        "outputs/eval_report.json"
    ),
) -> None:
    """Run a lightweight evaluation report."""
    del mock, fixtures
    sample = Path("data/mock/route_bicycling_sample.json")
    result = run_mock_pipeline(sample=sample, out_dir=Path("outputs/eval_tmp"), visualize=False)
    report = build_eval_report(len(result.events), len(result.instructions))
    write_json(output, report)
    typer.echo(f"instruction_coverage={report['instruction_coverage']}")
    typer.echo(f"report: {output}")


@debug_app.command("parse-route")
def debug_parse_route(
    sample: Annotated[Path, typer.Option(help="Mock route sample.")] = Path(
        "data/mock/route_bicycling_sample.json"
    ),
) -> None:
    route = parse_amap_route(MockAmapClient(route_sample=sample).route())
    typer.echo(f"steps={len(route.steps)}")
    typer.echo(f"distance={route.distance_meters:.0f} duration={route.duration_seconds:.0f}")


@debug_app.command("route")
def debug_route(
    sample: Annotated[Path, typer.Option(help="Mock route sample.")] = Path(
        "data/mock/route_bicycling_sample.json"
    ),
) -> None:
    payload = MockAmapClient(route_sample=sample).route()
    route = parse_amap_route(payload)
    typer.echo(f"mock route: {len(route.steps)} steps")
    typer.echo(f"from {route.origin.to_amap()} to {route.destination.to_amap()}")


def main() -> None:
    # Avoid leaking AMAP_KEY: the CLI never prints environment values.
    os.environ.get("AMAP_KEY")
    app()
