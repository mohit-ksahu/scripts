import subprocess
import imageio_ffmpeg

def audioFx(
    inputPath,
    outputPath,
    silenceDuration=2.0,
    silenceThreshold="-55dB",
    silenceKeep=0.5,
    highpassFreq=80,
    eqFreq=3000,
    eqBandwidth=1,
    eqGain=2,
    compressThreshold="-18dB",
    compressRatio=1.5,
    compressAttack=30,
    compressRelease=250,
    compressMakeup=1,
    limiterCeiling="-1dB",
    loudnormTarget=-14,
    loudnormPeak=-1,
    loudnormRange=7,
):
    filters = []

    if silenceDuration is not None:
        filters.append(
            "silenceremove="
            "stop_periods=-1:"
            f"stop_duration={silenceDuration}:"
            f"stop_threshold={silenceThreshold}:"
            f"stop_silence={silenceKeep}"
        )

    if highpassFreq is not None:
        filters.append(f"highpass=f={highpassFreq}")

    if eqGain is not None:
        filters.append(f"equalizer=f={eqFreq}:width_type=o:w={eqBandwidth}:g={eqGain}")

    if compressThreshold is not None:
        filters.append(
            f"acompressor=threshold={compressThreshold}:ratio={compressRatio}:"
            f"attack={compressAttack}:release={compressRelease}:makeup={compressMakeup}"
        )

    if limiterCeiling is not None:
        filters.append(f"alimiter=limit={limiterCeiling}")

    if loudnormTarget is not None:
        filters.append(f"loudnorm=I={loudnormTarget}:TP={loudnormPeak}:LRA={loudnormRange}")

    cmd = [
        imageio_ffmpeg.get_ffmpeg_exe(),
        "-y",
        "-i", inputPath,
        "-ar", "48000",
        "-c:a", "aac",
        "-b:a", "384k",
        "-ac", "2",
    ]

    if filters:
        cmd.extend(["-af", ",".join(filters)])

    cmd.append(outputPath)
    subprocess.run(cmd)
