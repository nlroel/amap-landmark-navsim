"""Rewrite plain navigation instructions with landmark candidates."""

from __future__ import annotations

from landmark_nav.models.events import NavigationEvent
from landmark_nav.models.instructions import LandmarkInstruction
from landmark_nav.models.poi import LandmarkCandidate
from landmark_nav.rewrite.templates import render_template


def rewrite_event(
    event: NavigationEvent, candidates: list[LandmarkCandidate]
) -> LandmarkInstruction:
    best = candidates[0] if candidates else None
    landmark_name = best.poi.name if best else None
    return LandmarkInstruction(
        event_id=event.id,
        original=event.instruction,
        landmark_text=render_template(event.event_type, event.instruction, landmark_name),
        landmark_name=landmark_name,
    )


def rewrite_events(
    events: list[NavigationEvent],
    candidates_by_event: dict[str, list[LandmarkCandidate]],
) -> list[LandmarkInstruction]:
    return [rewrite_event(event, candidates_by_event.get(event.id, [])) for event in events]
