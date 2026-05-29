"""Offline Amap client backed by JSON fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class MockAmapClient:
    def __init__(
        self, data_dir: Path | str = "data/mock", *, route_sample: Path | str | None = None
    ) -> None:
        self.data_dir = Path(data_dir)
        self.route_sample = Path(route_sample) if route_sample is not None else None

    def _read_json(self, path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as handle:
            return dict(json.load(handle))

    def route(
        self, origin: str = "", destination: str = "", mode: str = "bicycling"
    ) -> dict[str, Any]:
        del origin, destination, mode
        path = self.route_sample or self.data_dir / "route_bicycling_sample.json"
        if not path.exists():
            path = self.data_dir / "routes" / "bicycling_sample.json"
        return self._read_json(path)

    def search_pois(self, location: str, radius: int = 200) -> dict[str, Any]:
        del location, radius
        return self._read_json(self.data_dir / "pois" / "around_sample.json")

    def regeocode(self, location: str) -> dict[str, Any]:
        del location
        return self._read_json(self.data_dir / "regeocode" / "sample.json")
