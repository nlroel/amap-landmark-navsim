"""Route-related Pydantic models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from landmark_nav.models.geo import LngLat


class ManeuverType(StrEnum):
    STRAIGHT = "straight"
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    SLIGHT_LEFT = "slight_left"
    SLIGHT_RIGHT = "slight_right"
    KEEP_LEFT = "keep_left"
    KEEP_RIGHT = "keep_right"
    ARRIVE = "arrive"
    UNKNOWN = "unknown"


class RouteStep(BaseModel):
    index: int = Field(ge=0)
    instruction: str
    road: str = ""
    distance_meters: float = Field(ge=0)
    duration_seconds: float = Field(ge=0)
    maneuver: ManeuverType = ManeuverType.UNKNOWN
    polyline: list[LngLat] = Field(min_length=1)


class Route(BaseModel):
    origin: LngLat
    destination: LngLat
    mode: str = "bicycling"
    distance_meters: float = Field(ge=0)
    duration_seconds: float = Field(ge=0)
    steps: list[RouteStep] = Field(min_length=1)
