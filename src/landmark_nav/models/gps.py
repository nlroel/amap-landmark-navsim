"""GPS trace models."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from landmark_nav.models.geo import LngLat


class GpsPoint(BaseModel):
    index: int = Field(ge=0)
    location: LngLat
    timestamp: datetime
    speed_mps: float = Field(ge=0)
    step_index: int = Field(ge=0)
    distance_along_route_meters: float = Field(ge=0)


class GpsTrace(BaseModel):
    points: list[GpsPoint] = Field(min_length=1)
