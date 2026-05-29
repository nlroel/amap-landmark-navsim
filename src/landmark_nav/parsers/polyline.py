"""Amap polyline parser."""

from __future__ import annotations

from landmark_nav.models.geo import LngLat


def parse_polyline(value: str) -> list[LngLat]:
    points = [LngLat.from_amap(item) for item in value.split(";") if item.strip()]
    if not points:
        msg = "polyline must contain at least one coordinate"
        raise ValueError(msg)
    return points
