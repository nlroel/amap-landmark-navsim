"""Amap client protocol."""

from __future__ import annotations

from typing import Any, Protocol


class AmapClientProtocol(Protocol):
    def route(self, origin: str, destination: str, mode: str = "bicycling") -> dict[str, Any]: ...

    def search_pois(self, location: str, radius: int = 200) -> dict[str, Any]: ...

    def regeocode(self, location: str) -> dict[str, Any]: ...
