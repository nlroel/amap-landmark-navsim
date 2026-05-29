"""Mock end-to-end pipeline."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from landmark_nav.clients.mock import MockAmapClient
from landmark_nav.events.detector import detect_events
from landmark_nav.landmarks.candidates import pois_from_amap
from landmark_nav.landmarks.ranker import rank_landmarks
from landmark_nav.models.events import NavigationEvent
from landmark_nav.models.gps import GpsTrace
from landmark_nav.models.instructions import LandmarkInstruction
from landmark_nav.models.poi import LandmarkCandidate
from landmark_nav.models.route import Route
from landmark_nav.parsers.route_parser import parse_amap_route
from landmark_nav.pipeline.artifacts import write_json
from landmark_nav.rewrite.landmark_rewriter import rewrite_events
from landmark_nav.sim.gps import simulate_gps
from landmark_nav.viz.geojson import events_geojson, landmarks_geojson, route_geojson, trace_geojson
from landmark_nav.viz.html import render_html


class PipelineArtifacts(BaseModel):
    route: Path
    trace: Path
    events: Path
    landmarks: Path
    instructions: Path
    route_geojson: Path | None = None
    trace_geojson: Path | None = None
    events_geojson: Path | None = None
    landmarks_geojson: Path | None = None
    html: Path | None = None


class PipelineResult(BaseModel):
    route: Route
    trace: GpsTrace
    events: list[NavigationEvent]
    landmarks: dict[str, list[LandmarkCandidate]]
    instructions: list[LandmarkInstruction]
    artifacts: PipelineArtifacts


def run_mock_pipeline(
    *,
    sample: Path,
    out_dir: Path,
    interval_meters: float = 50.0,
    trigger_distance_meters: float = 80.0,
    top_k: int = 3,
    visualize: bool = False,
) -> PipelineResult:
    client = MockAmapClient(route_sample=sample)
    route = parse_amap_route(client.route())
    trace = simulate_gps(route, interval_meters=interval_meters)
    events = detect_events(route, trace, trigger_distance_meters=trigger_distance_meters)

    pois_by_event = {
        event.id: pois_from_amap(client.search_pois(event.location.to_amap()), event.location)
        for event in events
    }
    landmarks = rank_landmarks(events, pois_by_event, top_k=top_k)
    instructions = rewrite_events(events, landmarks)

    artifacts = PipelineArtifacts(
        route=write_json(out_dir / "route.json", route),
        trace=write_json(out_dir / "trace.json", trace),
        events=write_json(out_dir / "events.json", events),
        landmarks=write_json(out_dir / "landmarks.json", landmarks),
        instructions=write_json(out_dir / "instructions.json", instructions),
    )
    if visualize:
        artifacts.route_geojson = write_json(out_dir / "route.geojson", route_geojson(route))
        artifacts.trace_geojson = write_json(out_dir / "trace.geojson", trace_geojson(trace))
        artifacts.events_geojson = write_json(out_dir / "events.geojson", events_geojson(events))
        artifacts.landmarks_geojson = write_json(
            out_dir / "landmarks.geojson", landmarks_geojson(landmarks)
        )
        html_path = out_dir / "index.html"
        html_path.parent.mkdir(parents=True, exist_ok=True)
        html_path.write_text(render_html(), encoding="utf-8")
        artifacts.html = html_path
    return PipelineResult(
        route=route,
        trace=trace,
        events=events,
        landmarks=landmarks,
        instructions=instructions,
        artifacts=artifacts,
    )
