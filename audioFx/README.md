# AudioFX

Apply a professional-grade audio enhancement and cleanup pipeline to audio files automatically using FFmpeg.

## Key Features

- **Silence Removal:** Trims silent parts of the audio dynamically.
- **Highpass Filtering:** Removes low-frequency rumble (below 80 Hz).
- **Vocal Presence EQ:** Boosts clarity around 3 kHz.
- **Dynamic Compression & Limiting:** Prevents clipping and smooths volume spikes.
- **Loudness Normalization:** Standardizes output loudness targeting -14 LUFS.

## Installation

Install the required dependencies:
```bash
pip install -r requirements.txt
```

*Note: `imageio-ffmpeg` automatically manages and downloads the appropriate platform-specific FFmpeg binary on first run.*

## API Usage

Import the `audioFx` utility function from `audioFx.py`:

```python
from audioFx import audioFx

audioFx(
    inputPath="input.wav",
    outputPath="output.m4a",
    removeSilence=True,
    enhance=True
)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `inputPath` | `str` | *Required* | Path to the input audio file. |
| `outputPath` | `str` | *Required* | Path where the processed audio (AAC, 384k, stereo, 48kHz) will be saved. |
| `removeSilence` | `bool` | `True` | Removes silent portions matching `stop_duration=2.0` and `stop_threshold=-55dB`. |
| `enhance` | `bool` | `True` | Applies a highpass filter (80 Hz), equalizer (boosts 3 kHz), standard compressor, limiter, and loudness normalization to `-14 LUFS`. |
