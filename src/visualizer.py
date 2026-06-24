"""Matplotlib visualization of OBD-II CSV session logs."""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from src.config import PID_UNITS


class Visualizer:
    """Loads a logged CSV session and plots its signals over time."""

    def __init__(self, csv_path: Path) -> None:
        """Initialize the visualizer.

        Args:
            csv_path: Path to a CSV produced by DataLogger, with a
                'timestamp' column (Unix epoch seconds) plus one column
                per logged PID.
        """
        self.csv_path = csv_path
        self.data: Optional[pd.DataFrame] = None
        self.figure: Optional[Figure] = None

    def load_data(self) -> "Visualizer":
        """Read the CSV into a DataFrame and parse timestamps.

        Returns:
            self, for method chaining.
        """
        self.data = pd.read_csv(self.csv_path)
        self.data["timestamp"] = pd.to_datetime(self.data["timestamp"], unit="s")
        return self

    def plot_signals(self, signals: Optional[list[str]] = None) -> Figure:
        """Plot one subplot per signal against time, sharing the x-axis.

        Args:
            signals: PID column names to plot. If None, plots every column
                except 'timestamp'.

        Returns:
            The created matplotlib Figure.
        """
        if self.data is None:
            raise RuntimeError("Call load_data() before plot_signals().")

        if signals is None:
            signals = [column for column in self.data.columns if column != "timestamp"]

        figure, axes = plt.subplots(len(signals), 1, sharex=True, squeeze=False)
        axes = axes[:, 0]

        for axis, signal in zip(axes, signals):
            axis.plot(self.data["timestamp"], self.data[signal])
            axis.set_ylabel(f"{signal} ({PID_UNITS.get(signal, '')})".strip())

        axes[-1].set_xlabel("Time")
        figure.suptitle(f"Session: {self.csv_path.name}")
        figure.tight_layout()

        self.figure = figure
        return figure

    def save_plot(self, output_path: Path) -> None:
        """Save the current figure to a PNG file.

        Args:
            output_path: Destination path for the PNG image.
        """
        if self.figure is None:
            raise RuntimeError("Call plot_signals() before save_plot().")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.figure.savefig(output_path)

    def show(self) -> None:
        """Display the current figure interactively."""
        plt.show()
