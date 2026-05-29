from __future__ import annotations

from typer.testing import CliRunner

from landmark_nav.cli import app


def test_cli_run_mock(tmp_path) -> None:  # type: ignore[no-untyped-def]
    result = CliRunner().invoke(
        app,
        [
            "run-mock",
            "--sample",
            "data/mock/route_bicycling_sample.json",
            "--out-dir",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0
    assert (tmp_path / "instructions.json").exists()
