"""Polling loop that reads OBD-II PIDs and appends timestamped rows to CSV."""

import csv
import time
from pathlib import Path
from typing import Optional

import obd

from src.config import POLL_RATE_HZ


class DataLogger:
    """Polls an OBD-II connection at POLL_RATE_HZ and logs readings to CSV."""

    def __init__(
        self,
        connection: obd.OBD,
        available_pids: list[str],
        output_path: Path,
    ) -> None:
        """Initialize the logger.

        Args:
            connection: Active obd.OBD connection to poll.
            available_pids: PID names to query each cycle (e.g. "RPM", "SPEED").
            output_path: Destination CSV file path.
        """
        self.connection = connection
        self.available_pids = available_pids
        self.output_path = output_path

    def _poll_once(self) -> dict[str, float]:
        """Query every available PID once.

        Returns:
            Dict mapping PID name to its numeric reading, in that PID's
            native unit (e.g. RPM in rev/min, SPEED in km/h, COOLANT_TEMP
            in °C, THROTTLE_POS and ENGINE_LOAD in %, INTAKE_PRESSURE in kPa).
        """
        readings: dict[str, float] = {}
        for pid_name in self.available_pids:
            command = obd.commands[pid_name]
            response = self.connection.query(command)
            value = response.value
            readings[pid_name] = value.magnitude if hasattr(value, "magnitude") else value
        return readings

    def start(self, duration_seconds: Optional[float] = None) -> None:
        """Poll at POLL_RATE_HZ and append a timestamped row to CSV each cycle.

        Args:
            duration_seconds: How long to log, in seconds. If None, logs
                until interrupted with Ctrl+C (KeyboardInterrupt).
        """
        poll_interval_s = 1.0 / POLL_RATE_HZ
        fieldnames = ["timestamp", *self.available_pids]

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            start_time = time.monotonic()
            try:
                while duration_seconds is None or (time.monotonic() - start_time) < duration_seconds:
                    cycle_start = time.monotonic()

                    readings = self._poll_once()
                    writer.writerow({"timestamp": time.time(), **readings})
                    csv_file.flush()

                    remaining = poll_interval_s - (time.monotonic() - cycle_start)
                    if remaining > 0:
                        time.sleep(remaining)
            except KeyboardInterrupt:
                pass
