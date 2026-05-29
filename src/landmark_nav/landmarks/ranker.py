"""Rank landmark candidates for navigation events."""

from __future__ import annotations

from landmark_nav.landmarks.candidates import candidates_for_event
from landmark_nav.landmarks.scoring import score_candidate
from landmark_nav.models.events import NavigationEvent
from landmark_nav.models.poi import LandmarkCandidate, Poi


def rank_landmarks(
    events: list[NavigationEvent],
    pois_by_event: dict[str, list[Poi]],
    *,
    top_k: int = 3,
) -> dict[str, list[LandmarkCandidate]]:
    ranked: dict[str, list[LandmarkCandidate]] = {}
    for event in events:
        scored = [
            score_candidate(event, item)
            for item in candidates_for_event(event, pois_by_event.get(event.id, []))
        ]
        ranked[event.id] = sorted(scored, key=lambda item: (-item.score, item.poi.distance_meters))[
            :top_k
        ]
    return ranked
