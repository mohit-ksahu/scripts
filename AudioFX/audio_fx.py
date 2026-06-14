import subprocess
import imageio_ffmpeg

def audio_fx(input_path: str, output_path: str, remove_silence: bool = True, enhance: bool = True):
    filters = []
    
    if remove_silence:
        filters.append(
            "silenceremove="
            "stop_periods=-1:"
            "stop_duration=2.0:"
            "stop_threshold=-55dB:"
            "stop_silence=0.5"
        )
        
    if enhance:
        filters.extend([
            "highpass=f=80",
            "equalizer=f=3000:width_type=o:w=1:g=2",
            "acompressor=threshold=-18dB:ratio=1.5:attack=30:release=250:makeup=1",
            "alimiter=limit=-1dB",
            "loudnorm=I=-14:TP=-1:LRA=7",
        ])
    
    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(), 
        "-y", 
        "-i", input_path,
        "-ar", "48000",
        "-c:a", "aac",
        "-b:a", "384k",
        "-ac", "2",
    ]
    
    if filters:
        cmd.extend(["-af", ",".join(filters)])
        
    cmd.append(output_path)
    subprocess.run(cmd)