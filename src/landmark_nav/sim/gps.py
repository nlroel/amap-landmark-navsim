"""GPS trace simulator."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from landmark_nav.geo.distance import haversine_meters, interpolate
from landmark_nav.models.gps import GpsPoint, GpsTrace
from landmark_nav.models.route import Route


def simulate_gps(
    route: Route, *, interval_meters: float = 50.0, speed_mps: float = 5.0
) -> GpsTrace:
    points: list[GpsPoint] = []
    now = datetime(2024, 1, 1, tzinfo=UTC)
    elapsed_seconds = 0.0
    distance_along = 0.0

    for step in route.steps:
        for segment_start, segment_end in zip(step.polyline, step.polyline[1:], strict=False):
            segment_length = haversine_meters(segment_start, segment_end)
            sample_count = max(int(segment_length // interval_meters), 1)
            for sample in range(sample_count):
                fraction = sample / sample_count
                location = interpolate(segment_start, segment_end, fraction)
                points.append(
                    GpsPoint(
                        index=len(points),
                        location=location,
                        timestamp=now + timedelta(seconds=elapsed_seconds),
                        speed_mps=speed_mps,
                        step_index=step.index,
                        distance_along_route_meters=distance_along + segment_length * fraction,
                    )
                )
                elapsed_seconds += interval_meters / speed_mps
            distance_along += segment_length
    last_step = route.steps[-1]
    points.append(
        GpsPoint(
            index=len(points),
            location=last_step.polyline[-1],
            timestamp=now + timedelta(seconds=elapsed_seconds),
            speed_mps=speed_mps,
            step_index=last_step.index,
            distance_along_route_meters=distance_along,
        )
    )
    return GpsTrace(points=points)
