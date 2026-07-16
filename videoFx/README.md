# VideoFX

Compress video files using standard single-pass CRF (Constant Rate Factor) encoding in FFmpeg.

## Key Features

- **CRF Quality Control:** Uses Constant Rate Factor encoding for efficient and consistent visual quality.
- **Preset Selection:** Fine-tune the speed vs. compression ratio trade-off.
- **Codec Support:** Support for H.264 (`libx264`) and H.265 (`libx265`).

## Installation

Install the required dependencies:
```bash
pip install -r requirements.txt
```

*Note: `imageio-ffmpeg` automatically manages and downloads the appropriate platform-specific FFmpeg binary on first run.*

## Usage

To compress a video, configure the parameters directly in `main.py` and execute it:

```bash
python main.py
```

## API Usage

Import and use the `videoFx` function in your own Python projects:

```python
from videoFx import videoFx

videoFx(
    input_path="my_video.mp4",
    output_path="my_video_compressed.mp4",
    crf=18,
    preset="slow",
    codec="libx264"
)
```

## Presets

The `preset` parameter determines the trade-off between **encoding speed** and **compression efficiency**:

| Preset | Encoding Speed | Compression Efficiency | Recommended Use Case |
| :--- | :--- | :--- | :--- |
| `ultrafast` | Extremely Fast | Extremely Low (very large files) | Real-time capturing / screen recording where CPU speed is critical. |
| `superfast` | Very Fast | Very Low | Quick drafts / testing encoding setups. |
| `veryfast` | Fast | Low | Live streaming with moderate CPU capability. |
| `faster` | Moderately Fast | Moderately Low | Quick rendering. |
| `fast` | Slightly Fast | Balanced-low | Fast video processing where you don't mind slightly larger files. |
| `medium` | Balanced | Balanced | Standard encoding (default baseline for general use). |
| `slow` | Slow | High (smaller files) | Recommended for archiving and final renders if you have time. |
| `slower` | Very Slow | Very High | High-quality distribution encodes. |
| `veryslow` | Extremely Slow | Maximum | Squeezing out the absolute last drops of compression quality. |
