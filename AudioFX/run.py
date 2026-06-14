from audio_fx import audio_fx

def main():
    # You can decide exactly what to do by changing these to True or False!
    audio_fx(
        input_path="./audio.wav", 
        output_path="output_final.m4a", 
        remove_silence=True, 
        enhance=True
    )
    print("Saved output_final.m4a")

if __name__ == "__main__":
    main()