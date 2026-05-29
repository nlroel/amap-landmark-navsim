"""Landmark scoring helpers."""

from __future__ import annotations

from landmark_nav.models.events import EventType, NavigationEvent
from landmark_nav.models.poi import LandmarkCandidate, PoiCategory

CATEGORY_WEIGHTS: dict[PoiCategory, float] = {
    PoiCategory.TRAFFIC: 35,
    PoiCategory.SHOPPING: 28,
    PoiCategory.FINANCE: 24,
    PoiCategory.BUILDING: 20,
    PoiCategory.FOOD: 15,
    PoiCategory.OTHER: 10,
}


def score_candidate(event: NavigationEvent, candidate: LandmarkCandidate) -> LandmarkCandidate:
    poi = candidate.poi
    distance_score = max(0.0, 40.0 - poi.distance_meters / 5.0)
    category_score = CATEGORY_WEIGHTS[poi.category]
    name_score = min(len(poi.name), 12) * 1.5
    event_bonus = 5.0
    if (
        event.event_type in {EventType.TURN_RIGHT, EventType.TURN_LEFT}
        and poi.category == PoiCategory.TRAFFIC
    ):
        event_bonus = 30.0
    elif (
        event.event_type in {EventType.KEEP_RIGHT, EventType.KEEP_LEFT}
        and poi.category == PoiCategory.FINANCE
    ) or (
        event.event_type in {EventType.SLIGHT_RIGHT, EventType.SLIGHT_LEFT}
        and poi.category == PoiCategory.SHOPPING
    ):
        event_bonus = 35.0
    score = distance_score + category_score + name_score + event_bonus
    return candidate.model_copy(
        update={"score": round(score, 3), "reason": f"distance/category/name/event={score:.1f}"}
    )
