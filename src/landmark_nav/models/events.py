"""Navigation event models."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from landmark_nav.models.geo import LngLat


class EventType(StrEnum):
    TURN_LEFT = "turn_left"
    TURN_RIGHT = "turn_right"
    KEEP_LEFT = "keep_left"
    KEEP_RIGHT = "keep_right"
    SLIGHT_LEFT = "slight_left"
    SLIGHT_RIGHT = "slight_right"
    ARRIVE = "arrive"
    STRAIGHT = "straight"


class NavigationEvent(BaseModel):
    id: str
    event_type: EventType
    step_index: int = Field(ge=0)
    instruction: str
    location: LngLat
    trigger_distance_meters: float = Field(ge=0)
