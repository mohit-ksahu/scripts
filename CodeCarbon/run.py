import os
import time
import asyncio
from carbon import PowerTracker, track_power


def print_dashboard(label, tracker):
    bar_len = 20
    filled = min(bar_len, max(0, round((tracker.system_load / 100.0) * bar_len)))
    bar = "█" * filled + "░" * (bar_len - filled)
    co2 = f"{tracker.co2:.6f} g"
    
    print(f"\n[{label}]")
    print(f"  Duration:      {tracker.duration:.3f}s")
    print(f"  Process CPU:   {tracker.cpu_usage:.1f}%")
    print(f"  System CPU:    {bar} {tracker.system_load:.1f}%")
    print(f"  Process RAM:   {tracker.ram_gb:.4f} GB")
    print(f"  Energy:        {tracker.energy:.6f} Wh")
    print(f"  CO2:           {co2}\n")


def export_to_json(label, tracker, filename="carbon.json"):
    import json
    data = {
        "label": label,
        "duration_s": round(tracker.duration, 4),
        "cpu_usage_percent": round(tracker.cpu_usage, 2),
        "ram_gb": round(tracker.ram_gb, 4),
        "energy_wh": tracker.energy,
        "co2_g": tracker.co2
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


@track_power
async def run_task():
    big_list = [0] * 10_000_000
    total = 0
    for i in range(2_000_000):
        total += i
    await asyncio.sleep(0.5)


async def main():
    await run_task()
    print_dashboard("Task", run_task.tracker)
    
    export_to_json("Task", run_task.tracker)
    print("\nExported to carbon.json")


if __name__ == "__main__":
    asyncio.run(main())