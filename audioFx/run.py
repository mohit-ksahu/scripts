from audioFx import audioFx

def main():
    audioFx(
        inputPath="./audio.wav",
        outputPath="output.wav",
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
    )
    print("Saved output.wav")


if __name__ == "__main__":
    main()
