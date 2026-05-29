"""Evaluation runner."""

from __future__ import annotations

from landmark_nav.eval.metrics import instruction_coverage


def build_eval_report(total_events: int, rewritten_instructions: int) -> dict[str, float]:
    return {"instruction_coverage": instruction_coverage(total_events, rewritten_instructions)}
