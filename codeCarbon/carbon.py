import os
import time
import functools
import tracemalloc
import asyncio

class PowerTracker:
    def __init__(self, tdp=65.0, intensityGKwh=436.0, pue=1.2):
        self.tdp = tdp
        self.intensity = intensityGKwh / 1000.0
        self.pue = pue

    def start(self):
        self.t0 = time.perf_counter()
        self.cpu0 = time.process_time()
        tracemalloc.start()

    def stop(self):
        self.duration = time.perf_counter() - self.t0
        diff = time.process_time() - self.cpu0
        cores = os.cpu_count() or 1
        
        _, peakMemBytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.ramGb = peakMemBytes / (1024 ** 3)
        
        self.cpuUsage = (diff / self.duration) * 100 if self.duration else 0.0
        self.systemLoad = self.cpuUsage / cores
        
        cpuEnergy = self.tdp * (self.systemLoad / 100) * (self.duration / 3600)
        ramEnergy = (self.ramGb * 0.375) * (self.duration / 3600)
        
        self.energy = (cpuEnergy + ramEnergy) * self.pue
        self.co2 = self.energy * self.intensity
        
        return self.co2

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *_):
        self.stop()
        
    async def __aenter__(self):
        self.start()
        return self

    async def __aexit__(self, *_):
        self.stop()

def trackPower(func=None, /, tdp=65.0, intensityGKwh=436.0, pue=1.2):
    def decorator(f):
        if asyncio.iscoroutinefunction(f):
            @functools.wraps(f)
            async def asyncWrapper(*args, **kwargs):
                t = PowerTracker(tdp=tdp, intensityGKwh=intensityGKwh, pue=pue)
                async with t:
                     result = await f(*args, **kwargs)
                asyncWrapper.tracker = t
                return result
            return asyncWrapper
        else:
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                t = PowerTracker(tdp=tdp, intensityGKwh=intensityGKwh, pue=pue)
                with t:
                    result = f(*args, **kwargs)
                wrapper.tracker = t
                return result
            return wrapper
    return decorator(func) if func is not None else decorator