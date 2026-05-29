"""Instruction models."""

from __future__ import annotations

from pydantic import BaseModel


class Instruction(BaseModel):
    event_id: str
    original: str


class LandmarkInstruction(Instruction):
    landmark_text: str
    landmark_name: str | None = None
