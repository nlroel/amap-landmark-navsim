from __future__ import annotations

from landmark_nav.clients.mock import MockAmapClient


def test_mock_client_reads_all_payloads(sample_route_path) -> None:  # type: ignore[no-untyped-def]
    client = MockAmapClient(route_sample=sample_route_path)
    assert client.route()["status"] == "1"
    assert client.search_pois("116,39")["pois"]
    assert "regeocode" in client.regeocode("116,39")
