"""Small geographic calculations used by the simulator."""

from __future__ import annotations

from math import atan2, cos, radians, sin, sqrt

from landmark_nav.models.geo import LngLat

EARTH_RADIUS_METERS = 6_371_000.0


def haversine_meters(a: LngLat, b: LngLat) -> float:
    d_lat = radians(b.lat - a.lat)
    d_lng = radians(b.lng - a.lng)
    lat1 = radians(a.lat)
    lat2 = radians(b.lat)
    h = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lng / 2) ** 2
    return 2 * EARTH_RADIUS_METERS * atan2(sqrt(h), sqrt(1 - h))


def bearing_degrees(a: LngLat, b: LngLat) -> float:
    lat1 = radians(a.lat)
    lat2 = radians(b.lat)
    d_lng = radians(b.lng - a.lng)
    y = sin(d_lng) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(d_lng)
    return (atan2(y, x) * 180 / 3.141592653589793 + 360) % 360


def interpolate(a: LngLat, b: LngLat, fraction: float) -> LngLat:
    bounded = min(max(fraction, 0.0), 1.0)
    return LngLat(lng=a.lng + (b.lng - a.lng) * bounded, lat=a.lat + (b.lat - a.lat) * bounded)


def polyline_length_meters(points: list[LngLat]) -> float:
    return sum(haversine_meters(start, end) for start, end in zip(points, points[1:], strict=False))
