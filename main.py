"""CLI entry point for the OBD-II data logger: log a session or plot one."""

import argparse
from datetime import datetime
from pathlib import Path

from src.connection import connect_to_adapter
from src.logger import DataLogger
from src.visualizer import Visualizer

APP_NAME: str = "obd2-logger"
APP_VERSION: str = "0.1.0"


def _default_output_path() -> Path:
    """Build the default session CSV path: data/session_YYYYMMDD_HHMMSS.csv."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path("data") / f"session_{timestamp}.csv"


def _run_log(args: argparse.Namespace) -> None:
    """Connect to the ELM327 adapter and log data to CSV.

    Args:
        args: Parsed CLI arguments with port, duration, and output.
    """
    adapter = connect_to_adapter(port=args.port)
    data_logger = DataLogger(
        connection=adapter["connection"],
        available_pids=adapter["available_pids"],
        output_path=args.output,
    )

    print(f"Logging PIDs: {', '.join(adapter['available_pids'])}")
    print(f"Writing to: {args.output}")
    if args.duration is None:
        print("Press Ctrl+C to stop logging.")

    data_logger.start(duration_seconds=args.duration)
    print("Logging complete.")


def _run_plot(args: argparse.Namespace) -> None:
    """Load a recorded session and plot its signals.

    Args:
        args: Parsed CLI arguments with input, signals, and save.
    """
    visualizer = Visualizer(args.input).load_data()
    visualizer.plot_signals(signals=args.signals)

    if args.save is not None:
        visualizer.save_plot(args.save)
        print(f"Saved plot to: {args.save}")
    else:
        visualizer.show()


def build_parser() -> argparse.ArgumentParser:
    """Construct the CLI argument parser with its 'log' and 'plot' subcommands."""
    parser = argparse.ArgumentParser(prog=APP_NAME, description="OBD-II data logger and visualizer.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"{APP_NAME} {APP_VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    log_parser = subparsers.add_parser("log", help="Connect to an ELM327 adapter and log data.")
    log_parser.add_argument(
        "--port",
        type=str,
        default=None,
        help="Serial port the adapter is on (e.g. COM3). Auto-detected if omitted.",
    )
    log_parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Recording duration in seconds. Runs until Ctrl+C if omitted.",
    )
    log_parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path. Defaults to data/session_YYYYMMDD_HHMMSS.csv.",
    )
    log_parser.set_defaults(handler=_run_log)

    plot_parser = subparsers.add_parser("plot", help="Visualize a recorded session.")
    plot_parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to the CSV file to plot.",
    )
    plot_parser.add_argument(
        "--signals",
        nargs="+",
        default=None,
        help="Signal names to plot. Defaults to all columns except timestamp.",
    )
    plot_parser.add_argument(
        "--save",
        type=Path,
        default=None,
        help="Path to save the plot as a PNG. Shows interactively if omitted.",
    )
    plot_parser.set_defaults(handler=_run_plot)

    return parser


def main() -> None:
    """Parse CLI arguments and dispatch to the selected subcommand."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "log" and args.output is None:
        args.output = _default_output_path()

    args.handler(args)


if __name__ == "__main__":
    main()
