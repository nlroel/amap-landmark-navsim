"""Build landmark candidates from Amap POI responses."""

from __future__ import annotations

from typing import Any

from landmark_nav.geo.distance import haversine_meters
from landmark_nav.models.events import NavigationEvent
from landmark_nav.models.geo import LngLat
from landmark_nav.models.poi import LandmarkCandidate, Poi, PoiCategory


def categorize_poi(type_text: str, name: str) -> PoiCategory:
    text = f"{type_text} {name}"
    if "交通" in text or "红绿灯" in text or "路口" in text:
        return PoiCategory.TRAFFIC
    if "银行" in text:
        return PoiCategory.FINANCE
    if "广场" in text or "商场" in text or "购物" in text:
        return PoiCategory.SHOPPING
    if "餐" in text or "咖啡" in text:
        return PoiCategory.FOOD
    if "大厦" in text or "中心" in text:
        return PoiCategory.BUILDING
    return PoiCategory.OTHER


def pois_from_amap(payload: dict[str, Any], event_location: LngLat) -> list[Poi]:
    pois: list[Poi] = []
    for index, raw in enumerate(payload.get("pois", [])):
        name = str(raw.get("name") or f"POI-{index}")
        type_text = str(raw.get("type") or "")
        location = LngLat.from_amap(str(raw.get("location")))
        raw_distance = raw.get("distance")
        distance = (
            float(raw_distance)
            if raw_distance not in (None, "")
            else haversine_meters(event_location, location)
        )
        pois.append(
            Poi(
                id=str(raw.get("id") or f"poi-{index}"),
                name=name,
                location=location,
                type=type_text,
                category=categorize_poi(type_text, name),
                distance_meters=distance,
            )
        )
    return pois


def candidates_for_event(event: NavigationEvent, pois: list[Poi]) -> list[LandmarkCandidate]:
    return [
        LandmarkCandidate(event_id=event.id, poi=poi, score=0, reason="unscored") for poi in pois
    ]
