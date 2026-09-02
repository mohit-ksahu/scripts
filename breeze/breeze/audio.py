import io
import wave
from pathlib import Path
import numpy as np

class Audio:

    def __init__(self, samples, rate=24000):
        self._samples = np.ascontiguousarray(samples, dtype=np.float32)
        self._rate = int(rate)

    @property
    def samples(self):
        return self._samples

    @property
    def rate(self):
        return self._rate

    @property
    def duration(self):
        return len(self._samples) / float(self._rate)

    def to_numpy(self):
        return self._samples.copy()

    def to_int16(self):
        return (np.clip(self._samples, -1.0, 1.0) * 32767.0).astype(np.int16)

    def to_bytes(self):
        return self.to_int16().tobytes()

    def to_wav(self):
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(self._rate)
            file.writeframes(self.to_bytes())
        return buffer.getvalue()

    def save(self, path):
        destination = Path(path).resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(destination), "wb") as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(self._rate)
            file.writeframes(self.to_bytes())
        return str(destination)

    def __len__(self):
        return len(self._samples)

    def __getitem__(self, item):
        return Audio(self._samples[item], self._rate)

    def __repr__(self):
        return f"<Audio duration={self.duration:.2f}s rate={self._rate}Hz samples={len(self)}>"

class Chunk(Audio):

    def __init__(self, samples, rate=24000, index=0):
        super().__init__(samples, rate)
        self.index = index

    def __repr__(self):
        return f"<Chunk #{self.index} duration={self.duration:.2f}s samples={len(self)}>"

def load_audio(path, rate=24000):
    with wave.open(str(Path(path).resolve()), "rb") as file:
        channels = file.getnchannels()
        width = file.getsampwidth()
        source_rate = file.getframerate()
        raw = file.readframes(file.getnframes())
    if width == 2:
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32767.0
    else:
        samples = np.frombuffer(raw, dtype=np.int32).astype(np.float32) / 2147483647.0
    if channels > 1:
        samples = samples.reshape(-1, channels).mean(axis=1)
    if source_rate != rate:
        duration = len(samples) / source_rate
        sample_count = int(duration * rate)
        source_times = np.linspace(0, duration, len(samples), endpoint=False)
        output_times = np.linspace(0, duration, sample_count, endpoint=False)
        samples = np.interp(output_times, source_times, samples).astype(np.float32)
    return np.ascontiguousarray(samples, dtype=np.float32)