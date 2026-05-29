"""Simple evaluation metrics."""

from __future__ import annotations


def ratio(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return round(numerator / denominator, 4)


def instruction_coverage(total_events: int, rewritten_instructions: int) -> float:
    return ratio(rewritten_instructions, total_events)
