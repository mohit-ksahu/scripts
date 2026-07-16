import subprocess
from pathlib import Path
import imageio_ffmpeg

def videoFx(
    input_path,
    output_path,
    crf=18,
    preset="slow",
    codec="libx264",
):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", str(Path(input_path)),
        "-c:v", codec,
        "-crf", str(crf),
        "-preset", preset,
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        str(Path(output_path))
    ]
    
    subprocess.run(cmd, check=True)