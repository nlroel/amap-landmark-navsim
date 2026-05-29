from __future__ import annotations

from landmark_nav.clients.mock import MockAmapClient
from landmark_nav.events.detector import detect_events
from landmark_nav.landmarks.candidates import pois_from_amap
from landmark_nav.landmarks.ranker import rank_landmarks
from landmark_nav.parsers.route_parser import parse_amap_route
from landmark_nav.rewrite.landmark_rewriter import rewrite_events


def test_rank_and_rewrite(sample_route_path) -> None:  # type: ignore[no-untyped-def]
    client = MockAmapClient(route_sample=sample_route_path)
    route = parse_amap_route(client.route())
    events = detect_events(route)
    pois_by_event = {
        event.id: pois_from_amap(client.search_pois(event.location.to_amap()), event.location)
        for event in events
    }
    ranked = rank_landmarks(events, pois_by_event, top_k=2)
    instructions = rewrite_events(events, ranked)
    assert ranked[events[0].id][0].poi.name == "红绿灯"
    assert any("工商银行" in item.landmark_text for item in instructions)
    assert any("万达广场" in item.landmark_text for item in instructions)
