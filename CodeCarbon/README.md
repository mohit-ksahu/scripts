# Carbon Tracker

Ultra-compact, zero-dependency CPU carbon footprint tracker. Drop a single file into any project. No pip install, no config.

---

## Setup

```bash
# No dependencies — just copy carbon.py into your project.
# Optional: create a venv for isolation.
python3 -m venv venv && source venv/bin/activate
```

---

## Usage

### 1. Manual

```python
from carbon import PowerTracker

tracker = PowerTracker()
tracker.start()

sum(i * i for i in range(10_000_000))

tracker.stop()
print(tracker.energy)  # Wh
print(tracker.co2)     # g CO₂e, or None if CARBON_INTENSITY_G_KWH not set
```

### 2. Context Manager

```python
from carbon import PowerTracker

with PowerTracker() as tracker:
    sum(i * i for i in range(10_000_000))

print(tracker.energy)
```

### 3. Decorator

```python
from carbon import track_power

@track_power
def my_task():
    sum(i * i for i in range(10_000_000))

my_task()
print(my_task.tracker.energy)
```

---

## Attributes

After `.stop()` or exiting a `with` block:

| Attribute | Type | Description |
|---|---|---|
| `duration` | float | Wall-clock time (s) |
| `load` | float | System CPU utilisation (%) |
| `energy` | float | Estimated energy (Wh) |
| `co2` | float | Carbon emissions (g CO₂e) |
| `tdp` | float | TDP used for estimation (W) |



## Run Demo

```bash
python3 run.py
```