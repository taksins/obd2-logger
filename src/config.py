"""Shared constants for the OBD-II data logger."""

#: OBD-II PIDs to poll, by python-obd command name.
TARGET_PIDS: list[str] = [
    "RPM",
    "SPEED",
    "COOLANT_TEMP",
    "THROTTLE_POS",
    "ENGINE_LOAD",
    "INTAKE_PRESSURE",
]

#: Polling rate for the logger loop, in Hz (polls per second).
POLL_RATE_HZ: int = 2

#: Display units for known PID columns, keyed by column name.
PID_UNITS: dict[str, str] = {
    "RPM": "rev/min",
    "SPEED": "km/h",
    "COOLANT_TEMP": "°C",
    "THROTTLE_POS": "%",
    "ENGINE_LOAD": "%",
    "INTAKE_PRESSURE": "kPa",
}
