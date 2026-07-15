from audioFx import audioFx

def main():
    # You can decide exactly what to do by changing these to True or False!
    audioFx(
        inputPath="./audio.wav", 
        outputPath="output_final.m4a", 
        removeSilence=True, 
        enhance=True
    )
    print("Saved output_final.m4a")

if __name__ == "__main__":
    main()