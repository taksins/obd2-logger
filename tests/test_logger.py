"""Tests for DataLogger. obd.Connection is mocked — no hardware required."""

import csv
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src import logger as logger_module
from src.logger import DataLogger

AVAILABLE_PIDS = ["RPM", "SPEED", "COOLANT_TEMP"]
FAKE_VALUES = {"RPM": 1200.0, "SPEED": 60.0, "COOLANT_TEMP": 90.0}


class FakeResponse:
    """Stand-in for obd.OBDResponse with a plain numeric .value."""

    def __init__(self, value: float) -> None:
        self.value = value


def make_fake_connection() -> MagicMock:
    """Build a mock obd.OBD connection that echoes FAKE_VALUES by PID name."""
    connection = MagicMock()
    connection.query.side_effect = lambda command: FakeResponse(FAKE_VALUES[command])
    return connection


@pytest.fixture(autouse=True)
def fake_obd_commands(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make obd.commands[pid_name] resolve to the PID name itself (identity)."""
    monkeypatch.setattr(logger_module.obd, "commands", {pid: pid for pid in AVAILABLE_PIDS})


def test_poll_once_returns_readings_for_each_pid() -> None:
    data_logger = DataLogger(
        connection=make_fake_connection(),
        available_pids=AVAILABLE_PIDS,
        output_path=Path("unused.csv"),
    )

    readings = data_logger._poll_once()

    assert readings == FAKE_VALUES


def test_start_creates_csv_with_correct_columns_and_values(tmp_path: Path) -> None:
    output_path = tmp_path / "session.csv"
    data_logger = DataLogger(
        connection=make_fake_connection(),
        available_pids=AVAILABLE_PIDS,
        output_path=output_path,
    )

    data_logger.start(duration_seconds=0.5)

    assert output_path.exists()

    with output_path.open(newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        assert reader.fieldnames == ["timestamp", *AVAILABLE_PIDS]
        rows = list(reader)

    assert len(rows) >= 1
    for row in rows:
        assert row["timestamp"] != ""
        for pid_name, expected_value in FAKE_VALUES.items():
            assert float(row[pid_name]) == expected_value
