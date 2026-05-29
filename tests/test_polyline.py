from __future__ import annotations

from landmark_nav.parsers.polyline import parse_polyline


def test_parse_polyline() -> None:
    points = parse_polyline("116.1,39.1;116.2,39.2")
    assert points[0].lng == 116.1
    assert points[1].lat == 39.2
