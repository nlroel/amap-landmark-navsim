from __future__ import annotations

from landmark_nav.clients.mock import MockAmapClient
from landmark_nav.parsers.route_parser import parse_amap_route
from landmark_nav.sim.gps import simulate_gps


def test_simulate_gps(sample_route_path) -> None:  # type: ignore[no-untyped-def]
    route = parse_amap_route(MockAmapClient(route_sample=sample_route_path).route())
    trace = simulate_gps(route, interval_meters=100)
    assert len(trace.points) > len(route.steps)
    assert trace.points[-1].location == route.destination
