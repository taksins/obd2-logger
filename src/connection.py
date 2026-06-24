"""ELM327 connection setup and PID capability querying."""

from typing import Optional

import obd

from src.config import TARGET_PIDS


def connect_to_adapter(port: Optional[str] = None) -> dict[str, object]:
    """Connect to an ELM327 adapter and report which target PIDs it supports.

    Args:
        port: Serial port the ELM327 adapter is attached to (e.g. "COM3" on
            Windows or "/dev/ttyUSB0" on Linux). If None, python-obd scans
            for and connects to the first available adapter.

    Returns:
        A dict with:
            'connection': the obd.OBD connection object.
            'available_pids': list of PID names (str) that are both in
                TARGET_PIDS and supported by the connected vehicle.

    Raises:
        ConnectionError: If the adapter cannot establish a connection.
    """
    connection = obd.OBD(portstr=port)

    if not connection.is_connected():
        raise ConnectionError(f"Could not connect to ELM327 adapter on port {port!r}")

    supported_names = {cmd.name for cmd in connection.supported_commands}
    available_pids = [pid for pid in TARGET_PIDS if pid in supported_names]

    return {
        "connection": connection,
        "available_pids": available_pids,
    }
