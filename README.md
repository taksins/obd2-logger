# OBD-II Data Logger

A Python CLI that logs live OBD-II vehicle data from an ELM327 adapter to CSV and visualizes it as time-series plots.

[![CI](https://github.com/taksins/obd2-logger/actions/workflows/ci.yml/badge.svg)](https://github.com/taksins/obd2-logger/actions/workflows/ci.yml)

## Overview

This tool polls a vehicle's OBD-II port for engine and powertrain signals — RPM, speed, coolant temperature, throttle position, engine load, and intake pressure — at a configurable rate and records them to CSV. It's built as a small automotive/EV engineering portfolio project: a focused, well-tested example of real-time sensor acquisition and time-series visualization against real vehicle hardware.

## How It Works

The tool connects to an **ELM327** adapter over a serial port and uses [`python-obd`](https://github.com/brendan-w/python-OBD) to query which **OBD-II PIDs** (Parameter IDs — standardized sensor identifiers) the vehicle actually supports. It intersects that list with the PIDs this tool targets, then runs a polling loop that queries each available PID at a fixed rate, timestamps every reading, and appends rows to a CSV as it goes. A separate visualization step loads that CSV with pandas and renders one time-aligned subplot per signal using **matplotlib**.

## Demo

[Screenshot placeholder — will update with real hardware]

## Usage

### Log a session

```bash
python main.py log --port COM3 --duration 300 --output data/my_session.csv
```

### Visualize a session

```bash
python main.py plot --input data/sample_session.csv
```

## Supported PIDs

| PID name | Description | Unit |
|---|---|---|
| RPM | Engine speed | rev/min |
| SPEED | Vehicle speed | km/h |
| COOLANT_TEMP | Engine coolant temperature | °C |
| THROTTLE_POS | Throttle position | % |
| ENGINE_LOAD | Calculated engine load | % |
| INTAKE_PRESSURE | Intake manifold absolute pressure | kPa |

## Hardware

- ELM327 adapter (USB or Bluetooth)
- Recommended: OBDLink SX (USB) or Veepeak OBDCheck BLE (Bluetooth)
- Compatible with any OBD-II vehicle (US cars 1996+)

## Tech Stack

python-obd · pandas · matplotlib · pytest · GitHub Actions

## Project Structure

```
src/connection.py    — ELM327 connection and PID capability query
src/logger.py        — polling loop and CSV writer
src/visualizer.py    — matplotlib plots from CSV
src/config.py        — PID list, poll rate, constants
```
