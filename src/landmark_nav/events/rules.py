"""Navigation event mapping rules."""

from __future__ import annotations

from landmark_nav.models.events import EventType
from landmark_nav.models.route import ManeuverType

MANEUVER_EVENT_MAP: dict[ManeuverType, EventType] = {
    ManeuverType.TURN_LEFT: EventType.TURN_LEFT,
    ManeuverType.TURN_RIGHT: EventType.TURN_RIGHT,
    ManeuverType.KEEP_LEFT: EventType.KEEP_LEFT,
    ManeuverType.KEEP_RIGHT: EventType.KEEP_RIGHT,
    ManeuverType.SLIGHT_LEFT: EventType.SLIGHT_LEFT,
    ManeuverType.SLIGHT_RIGHT: EventType.SLIGHT_RIGHT,
    ManeuverType.ARRIVE: EventType.ARRIVE,
    ManeuverType.STRAIGHT: EventType.STRAIGHT,
}


def event_type_for_maneuver(maneuver: ManeuverType) -> EventType | None:
    return MANEUVER_EVENT_MAP.get(maneuver)
