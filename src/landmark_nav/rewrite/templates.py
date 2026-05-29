"""Templates for landmark-aware navigation instructions."""

from __future__ import annotations

from landmark_nav.models.events import EventType


def render_template(event_type: EventType, original: str, landmark_name: str | None) -> str:
    if not landmark_name:
        return original
    if event_type == EventType.TURN_RIGHT:
        return f"前方{landmark_name}右转"
    if event_type == EventType.TURN_LEFT:
        return f"前方{landmark_name}左转"
    if event_type == EventType.KEEP_RIGHT:
        return f"沿当前道路直行，经过{landmark_name}后靠右"
    if event_type == EventType.KEEP_LEFT:
        return f"沿当前道路直行，经过{landmark_name}后靠左"
    if event_type == EventType.SLIGHT_RIGHT:
        return f"到前方岔路口，朝{landmark_name}方向走右前方道路"
    if event_type == EventType.SLIGHT_LEFT:
        return f"到前方岔路口，朝{landmark_name}方向走左前方道路"
    if event_type == EventType.ARRIVE:
        return f"到达{landmark_name}附近的目的地"
    return original
