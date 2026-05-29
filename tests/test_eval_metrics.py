from __future__ import annotations

from landmark_nav.eval.metrics import instruction_coverage


def test_instruction_coverage() -> None:
    assert instruction_coverage(4, 3) == 0.75
    assert instruction_coverage(0, 0) == 0.0
