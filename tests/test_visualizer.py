"""Tests for Visualizer, using the real sample_session.csv as a fixture."""

from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")

from src.visualizer import Visualizer

SAMPLE_CSV = Path(__file__).resolve().parent.parent / "data" / "sample_session.csv"


@pytest.fixture
def visualizer() -> Visualizer:
    return Visualizer(SAMPLE_CSV)


def test_load_data_returns_self_and_parses_timestamps(visualizer: Visualizer) -> None:
    result = visualizer.load_data()

    assert result is visualizer
    assert visualizer.data is not None
    assert "timestamp" in visualizer.data.columns
    assert str(visualizer.data["timestamp"].dtype).startswith("datetime64")


def test_plot_signals_generates_figure_without_error(visualizer: Visualizer) -> None:
    visualizer.load_data()

    figure = visualizer.plot_signals()

    assert figure is not None
    assert visualizer.figure is figure
    non_timestamp_columns = [c for c in visualizer.data.columns if c != "timestamp"]
    assert len(figure.axes) == len(non_timestamp_columns)


def test_plot_signals_with_subset(visualizer: Visualizer) -> None:
    visualizer.load_data()

    figure = visualizer.plot_signals(signals=["RPM", "SPEED"])

    assert len(figure.axes) == 2


def test_save_plot_creates_file(visualizer: Visualizer, tmp_path: Path) -> None:
    visualizer.load_data()
    visualizer.plot_signals()
    output_path = tmp_path / "plot.png"

    visualizer.save_plot(output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0
