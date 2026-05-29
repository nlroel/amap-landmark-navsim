from __future__ import annotations

from landmark_nav.geo.distance import haversine_meters, interpolate
from landmark_nav.models.geo import LngLat


def test_distance_and_interpolation() -> None:
    a = LngLat(lng=116.0, lat=39.0)
    b = LngLat(lng=116.0, lat=39.001)
    assert haversine_meters(a, b) > 100
    mid = interpolate(a, b, 0.5)
    assert mid.lat == 39.0005
