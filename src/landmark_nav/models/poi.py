"""POI and landmark candidate models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from landmark_nav.models.geo import LngLat


class PoiCategory(StrEnum):
    TRAFFIC = "traffic"
    FINANCE = "finance"
    SHOPPING = "shopping"
    FOOD = "food"
    BUILDING = "building"
    OTHER = "other"


class Poi(BaseModel):
    id: str
    name: str = Field(min_length=1)
    location: LngLat
    type: str = ""
    category: PoiCategory = PoiCategory.OTHER
    distance_meters: float = Field(default=0, ge=0)


class LandmarkCandidate(BaseModel):
    event_id: str
    poi: Poi
    score: float
    reason: str
