from __future__ import annotations

from typer.testing import CliRunner

from landmark_nav.cli import app


def test_cli_help() -> None:
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Amap landmark-aware" in result.output
