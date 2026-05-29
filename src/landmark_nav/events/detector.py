"""Detect navigation events from route steps."""

from __future__ import annotations

from landmark_nav.events.rules import event_type_for_maneuver
from landmark_nav.models.events import EventType, NavigationEvent
from landmark_nav.models.gps import GpsTrace
from landmark_nav.models.route import Route


def detect_events(
    route: Route,
    trace: GpsTrace | None = None,
    *,
    trigger_distance_meters: float = 80.0,
) -> list[NavigationEvent]:
    del trace
    events: list[NavigationEvent] = []
    for step in route.steps:
        event_type = event_type_for_maneuver(step.maneuver)
        if event_type is None or event_type == EventType.STRAIGHT:
            continue
        events.append(
            NavigationEvent(
                id=f"event-{len(events) + 1}",
                event_type=event_type,
                step_index=step.index,
                instruction=step.instruction,
                location=step.polyline[-1],
                trigger_distance_meters=trigger_distance_meters,
            )
        )
    if not events or events[-1].event_type != EventType.ARRIVE:
        final = route.steps[-1]
        events.append(
            NavigationEvent(
                id=f"event-{len(events) + 1}",
                event_type=EventType.ARRIVE,
                step_index=final.index,
                instruction="到达目的地",
                location=route.destination,
                trigger_distance_meters=0,
            )
        )
    return events
