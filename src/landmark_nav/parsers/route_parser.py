"""Parse Amap route responses into internal route models."""

from __future__ import annotations

from typing import Any

from landmark_nav.geo.distance import polyline_length_meters
from landmark_nav.models.geo import LngLat
from landmark_nav.models.route import ManeuverType, Route, RouteStep
from landmark_nav.parsers.polyline import parse_polyline


def normalize_maneuver(
    instruction: str, action: str = "", assistant_action: str = ""
) -> ManeuverType:
    text = f"{instruction} {action} {assistant_action}"
    if "到达" in text:
        return ManeuverType.ARRIVE
    if "右前方" in text:
        return ManeuverType.SLIGHT_RIGHT
    if "左前方" in text:
        return ManeuverType.SLIGHT_LEFT
    if "靠右" in text:
        return ManeuverType.KEEP_RIGHT
    if "靠左" in text:
        return ManeuverType.KEEP_LEFT
    if "右转" in text:
        return ManeuverType.TURN_RIGHT
    if "左转" in text:
        return ManeuverType.TURN_LEFT
    if "直行" in text:
        return ManeuverType.STRAIGHT
    return ManeuverType.UNKNOWN


def _first_path(payload: dict[str, Any]) -> dict[str, Any]:
    route = payload.get("route", {})
    paths = route.get("paths") or []
    if not paths:
        msg = "Amap route payload does not contain route.paths"
        raise ValueError(msg)
    return dict(paths[0])


def parse_amap_route(payload: dict[str, Any], *, mode: str = "bicycling") -> Route:
    route_obj = payload.get("route", {})
    path = _first_path(payload)
    raw_steps = path.get("steps") or []
    if not raw_steps:
        msg = "Amap route path does not contain steps"
        raise ValueError(msg)

    steps: list[RouteStep] = []
    for index, raw in enumerate(raw_steps):
        points = parse_polyline(str(raw.get("polyline", "")))
        distance = float(raw.get("distance") or polyline_length_meters(points))
        steps.append(
            RouteStep(
                index=index,
                instruction=str(raw.get("instruction", "")),
                road=str(raw.get("road", "")),
                distance_meters=distance,
                duration_seconds=float(raw.get("duration") or max(distance / 4, 1)),
                maneuver=normalize_maneuver(
                    str(raw.get("instruction", "")),
                    str(raw.get("action", "")),
                    str(raw.get("assistant_action", "")),
                ),
                polyline=points,
            )
        )

    origin = LngLat.from_amap(str(route_obj.get("origin") or steps[0].polyline[0].to_amap()))
    destination = LngLat.from_amap(
        str(route_obj.get("destination") or steps[-1].polyline[-1].to_amap())
    )
    return Route(
        origin=origin,
        destination=destination,
        mode=mode,
        distance_meters=float(path.get("distance") or sum(step.distance_meters for step in steps)),
        duration_seconds=float(
            path.get("duration") or sum(step.duration_seconds for step in steps)
        ),
        steps=steps,
    )
