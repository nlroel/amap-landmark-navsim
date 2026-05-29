"""Real Amap HTTP client with diskcache-backed response caching."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx
from diskcache import Cache

from landmark_nav.clients.errors import AmapClientError


class AmapClient:
    def __init__(
        self,
        key: str,
        *,
        base_url: str = "https://restapi.amap.com/v3",
        cache_dir: Path | str = ".cache/amap",
        timeout: float = 10.0,
    ) -> None:
        self._key = key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._cache = Cache(str(cache_dir))

    def _get(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        safe_params = {**params, "key": self._key, "output": "json"}
        cache_key = (
            endpoint,
            tuple(sorted((k, str(v)) for k, v in safe_params.items() if k != "key")),
        )
        cached = self._cache.get(cache_key)
        if isinstance(cached, dict):
            return cached
        try:
            response = httpx.get(
                f"{self._base_url}/{endpoint.lstrip('/')}",
                params=safe_params,
                timeout=self._timeout,
            )
            response.raise_for_status()
            payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise AmapClientError("Amap request failed") from exc
        if str(payload.get("status", "1")) == "0":
            raise AmapClientError(str(payload.get("info", "Amap API error")))
        self._cache.set(cache_key, payload)
        return dict(payload)

    def route(self, origin: str, destination: str, mode: str = "bicycling") -> dict[str, Any]:
        if mode == "walking":
            endpoint = "direction/walking"
        elif mode == "driving":
            endpoint = "direction/driving"
        else:
            endpoint = "direction/bicycling"
        return self._get(endpoint, {"origin": origin, "destination": destination})

    def search_pois(self, location: str, radius: int = 200) -> dict[str, Any]:
        return self._get(
            "place/around", {"location": location, "radius": radius, "extensions": "all"}
        )

    def regeocode(self, location: str) -> dict[str, Any]:
        return self._get("geocode/regeo", {"location": location, "extensions": "all"})
