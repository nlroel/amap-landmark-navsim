from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def sample_route_path() -> Path:
    return Path("data/mock/route_bicycling_sample.json")
