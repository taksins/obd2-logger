# obd2-logger

A Python CLI that connects to a vehicle over an ELM327 adapter, logs OBD-II sensor data to CSV, and visualizes it as time-series plots.

[![CI](https://github.com/taksins/obd2-logger/actions/workflows/ci.yml/badge.svg)](https://github.com/taksins/obd2-logger/actions/workflows/ci.yml)

## Motivation

Modern vehicles expose a wealth of real-time engine and powertrain data over the OBD-II port, but most of that data disappears the moment it's read by a generic scan tool. This project captures it: polling key PIDs (RPM, speed, coolant temperature, throttle position, engine load, intake pressure) at a configurable rate, persisting full sessions to CSV, and plotting them for analysis. It's built as a small, focused automotive/EV engineering portfolio piece — a minimal, well-tested tool rather than a general-purpose scan tool replacement.

## How It Works

1. `src/connection.py` opens a serial connection to an ELM327 adapter via `python-OBD`, queries which PIDs the vehicle actually supports, and intersects that with the PIDs this tool targets (`TARGET_PIDS` in `src/config.py`).
2. `src/logger.py`'s `DataLogger` polls each available PID at `POLL_RATE_HZ`, timestamps every reading, and appends rows to a CSV as it goes.
3. `src/visualizer.py`'s `Visualizer` loads a logged CSV into a pandas DataFrame and renders one time-aligned subplot per signal with matplotlib.
4. `main.py` ties both together behind a `log` / `plot` CLI.

## Usage

Log a session (auto-detects the adapter port, logs until you press Ctrl+C):

```bash
python main.py log
```

Log for a fixed duration to a specific file:

```bash
python main.py log --port COM3 --duration 300 --output data/my_session.csv
```

Plot a recorded session interactively:

```bash
python main.py plot --input data/sample_session.csv
```

Plot specific signals and save to PNG instead of displaying:

```bash
python main.py plot --input data/sample_session.csv --signals RPM SPEED --save plot.png
```

## Sample Output

![Sample plot](docs/sample_plot.png)
<!-- Screenshot placeholder — generate with: python main.py plot --input data/sample_session.csv --save docs/sample_plot.png -->

## Requirements

- Python 3.11
- Dependencies in `requirements.txt`: `obd`, `pandas`, `matplotlib`, `pytest`

Install with:

```bash
pip install -r requirements.txt
```

## Hardware

This tool talks to vehicles through an **ELM327** OBD-II adapter (USB, Bluetooth, or Wi-Fi). Compatible adapters include:

- USB ELM327 cables (e.g. OBDLink SX)
- Bluetooth ELM327 dongles (e.g. OBDLink MX+, Veepeak OBDCheck BLE)
- Wi-Fi ELM327 adapters (e.g. OBDLink MX+ Wi-Fi, generic ELM327 Wi-Fi dongles)

Any adapter exposing a standard ELM327 AT-command serial interface that `python-OBD` can talk to should work. Genuine/well-reviewed adapters (OBDLink brand in particular) tend to be far more reliable than cheap clone ELM327 chips, which are known to drop commands or misreport supported PIDs.

## Tech Stack

- Python 3.11
- [python-OBD](https://github.com/brendan-w/python-OBD) — ELM327 communication
- pandas — data handling
- matplotlib — visualization
- pytest — testing
