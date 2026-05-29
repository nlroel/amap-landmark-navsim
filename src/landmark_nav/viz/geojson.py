"""GeoJSON exporters."""

from __future__ import annotations

from typing import Any

from landmark_nav.models.events import NavigationEvent
from landmark_nav.models.gps import GpsTrace
from landmark_nav.models.poi import LandmarkCandidate
from landmark_nav.models.route import Route


def feature_collection(features: list[dict[str, Any]]) -> dict[str, Any]:
    return {"type": "FeatureCollection", "features": features}


def route_geojson(route: Route) -> dict[str, Any]:
    coords = [point.geojson() for step in route.steps for point in step.polyline]
    return feature_collection(
        [
            {
                "type": "Feature",
                "properties": {"kind": "route"},
                "geometry": {"type": "LineString", "coordinates": coords},
            }
        ]
    )


def trace_geojson(trace: GpsTrace) -> dict[str, Any]:
    return feature_collection(
        [
            {
                "type": "Feature",
                "properties": {"kind": "trace"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [point.location.geojson() for point in trace.points],
                },
            }
        ]
    )


def events_geojson(events: list[NavigationEvent]) -> dict[str, Any]:
    return feature_collection(
        [
            {
                "type": "Feature",
                "properties": {
                    "id": event.id,
                    "type": event.event_type.value,
                    "instruction": event.instruction,
                },
                "geometry": {"type": "Point", "coordinates": event.location.geojson()},
            }
            for event in events
        ]
    )


def landmarks_geojson(candidates_by_event: dict[str, list[LandmarkCandidate]]) -> dict[str, Any]:
    features: list[dict[str, Any]] = []
    for event_id, candidates in candidates_by_event.items():
        for candidate in candidates:
            features.append(
                {
                    "type": "Feature",
                    "properties": {
                        "event_id": event_id,
                        "name": candidate.poi.name,
                        "score": candidate.score,
                    },
                    "geometry": {"type": "Point", "coordinates": candidate.poi.location.geojson()},
                }
            )
    return feature_collection(features)
