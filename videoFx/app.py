from videoFx import videoFx

def main():
    videoFx(
        input_path="./video.mp4",
        output_path="output.mp4",
        crf=18,
        preset="slow",
        codec="libx264",
    )
    print("Saved output.mp4")

if __name__ == "__main__":
    main()