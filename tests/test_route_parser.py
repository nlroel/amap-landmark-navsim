from __future__ import annotations

from landmark_nav.clients.mock import MockAmapClient
from landmark_nav.models.route import ManeuverType
from landmark_nav.parsers.route_parser import parse_amap_route


def test_parse_mock_route(sample_route_path) -> None:  # type: ignore[no-untyped-def]
    route = parse_amap_route(MockAmapClient(route_sample=sample_route_path).route())
    assert len(route.steps) == 4
    assert route.steps[0].maneuver == ManeuverType.TURN_RIGHT
    assert route.steps[-1].maneuver == ManeuverType.ARRIVE
