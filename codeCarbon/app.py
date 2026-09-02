import time
import asyncio
from carbon import PowerTracker, trackPower


def printDashboard(label, tracker):
    barLen = 20
    filled = min(barLen, max(0, round((tracker.systemLoad / 100.0) * barLen)))
    bar = "█" * filled + "░" * (barLen - filled)
    co2 = f"{tracker.co2:.6f} g"
    
    print(f"\n[{label}]")
    print(f"  Duration:      {tracker.duration:.3f}s")
    print(f"  Process CPU:   {tracker.cpuUsage:.1f}%")
    print(f"  System CPU:    {bar} {tracker.systemLoad:.1f}%")
    print(f"  Process RAM:   {tracker.ramGb:.4f} GB")
    print(f"  Energy:        {tracker.energy:.6f} Wh")
    print(f"  CO2:           {co2}\n")


def exportToJson(label, tracker, filename="carbon.json"):
    import json
    data = {
        "label": label,
        "durationS": round(tracker.duration, 4),
        "cpuUsagePercent": round(tracker.cpuUsage, 2),
        "ramGb": round(tracker.ramGb, 4),
        "energyWh": tracker.energy,
        "co2G": tracker.co2
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


@trackPower
async def runTask():
    bigList = [0] * 10_000_000
    total = 0
    for i in range(2_000_000):
        total += i
    await asyncio.sleep(0.5)


def runSyncTask():
    tracker = PowerTracker()
    tracker.start()
    
    total = sum(i * i for i in range(5_000_000))
    time.sleep(0.1)
    
    tracker.stop()
    return tracker


async def main():
    await runTask()
    printDashboard("Async Task (Decorator)", runTask.tracker)
    
    syncTracker = runSyncTask()
    printDashboard("Sync Task (Manual)", syncTracker)
    
    exportToJson("Async Task", runTask.tracker)
    print("\nExported to carbon.json")


if __name__ == "__main__":
    asyncio.run(main())