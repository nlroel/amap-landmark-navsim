from __future__ import annotations

from landmark_nav.pipeline.mock_pipeline import run_mock_pipeline


def test_mock_pipeline_writes_artifacts(tmp_path, sample_route_path) -> None:  # type: ignore[no-untyped-def]
    result = run_mock_pipeline(sample=sample_route_path, out_dir=tmp_path, visualize=True)
    assert result.artifacts.route.exists()
    assert result.artifacts.html is not None
    assert result.artifacts.html.exists()
    assert result.instructions
