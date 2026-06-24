"""Shared constants for the OBD-II data logger."""

#: Display units for known PID columns, keyed by column name.
PID_UNITS: dict[str, str] = {
    "RPM": "rev/min",
    "SPEED": "km/h",
    "COOLANT_TEMP": "°C",
    "THROTTLE_POS": "%",
    "ENGINE_LOAD": "%",
    "INTAKE_PRESSURE": "kPa",
}
