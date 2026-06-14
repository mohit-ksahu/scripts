import os
import time
import functools
import tracemalloc
import asyncio

class PowerTracker:
    def __init__(self, tdp=65.0, intensity_g_kwh=436.0, pue=1.2):
        self.tdp = tdp
        self.intensity = intensity_g_kwh / 1000.0
        self.pue = pue

    def start(self):
        self.t0 = time.perf_counter()
        self.cpu0 = time.process_time()
        tracemalloc.start()

    def stop(self):
        self.duration = time.perf_counter() - self.t0
        diff = time.process_time() - self.cpu0
        cores = os.cpu_count() or 1
        
        _, peak_mem_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.ram_gb = peak_mem_bytes / (1024 ** 3)
        
        self.cpu_usage = (diff / self.duration) * 100 if self.duration else 0.0
        self.system_load = self.cpu_usage / cores
        
        cpu_energy = self.tdp * (self.system_load / 100) * (self.duration / 3600)
        ram_energy = (self.ram_gb * 0.375) * (self.duration / 3600)
        
        self.energy = (cpu_energy + ram_energy) * self.pue
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

def track_power(func=None, /, tdp=65.0, intensity_g_kwh=436.0, pue=1.2):
    def decorator(f):
        if asyncio.iscoroutinefunction(f):
            @functools.wraps(f)
            async def async_wrapper(*args, **kwargs):
                t = PowerTracker(tdp=tdp, intensity_g_kwh=intensity_g_kwh, pue=pue)
                async with t:
                    result = await f(*args, **kwargs)
                async_wrapper.tracker = t
                return result
            return async_wrapper
        else:
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                t = PowerTracker(tdp=tdp, intensity_g_kwh=intensity_g_kwh, pue=pue)
                with t:
                    result = f(*args, **kwargs)
                wrapper.tracker = t
                return result
            return wrapper
    return decorator(func) if func is not None else decorator