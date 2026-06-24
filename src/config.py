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
