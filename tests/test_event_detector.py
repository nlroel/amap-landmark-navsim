from __future__ import annotations

from landmark_nav.clients.mock import MockAmapClient
from landmark_nav.events.detector import detect_events
from landmark_nav.models.events import EventType
from landmark_nav.parsers.route_parser import parse_amap_route


def test_detect_events(sample_route_path) -> None:  # type: ignore[no-untyped-def]
    route = parse_amap_route(MockAmapClient(route_sample=sample_route_path).route())
    events = detect_events(route)
    assert [event.event_type for event in events] == [
        EventType.TURN_RIGHT,
        EventType.KEEP_RIGHT,
        EventType.SLIGHT_RIGHT,
        EventType.ARRIVE,
    ]
