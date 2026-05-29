"""Geographic Pydantic models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LngLat(BaseModel):
    """A longitude/latitude coordinate in Amap order."""

    lng: float = Field(ge=-180.0, le=180.0)
    lat: float = Field(ge=-90.0, le=90.0)

    @classmethod
    def from_amap(cls, value: str) -> LngLat:
        lng_text, lat_text = value.split(",", maxsplit=1)
        return cls(lng=float(lng_text), lat=float(lat_text))

    def to_amap(self) -> str:
        return f"{self.lng:.6f},{self.lat:.6f}"

    def geojson(self) -> list[float]:
        return [self.lng, self.lat]
