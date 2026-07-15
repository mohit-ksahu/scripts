import sys
from pathlib import Path
import torch
from whisperModel import WhisperModel

def main():
    import platform
    device = "cpu" if platform.system() == "Darwin" and not torch.cuda.is_available() else None
    
    model = WhisperModel(device=device)
    audioPath = Path("output.wav")
    
    if not audioPath.exists():
        sys.exit(1)

    returnTimestamps = "word"      # Set to True, "word" (for word-level timestamps), or False
    generateKwargs = {
        "language": "english",    # specify language (e.g. "english", "french") or None for auto-detection
        "task": "transcribe",     # "transcribe" to transcribe, "translate" to translate to English
    }

    result = model.transcribe(
        audioPath,
        return_timestamps=returnTimestamps,
        generate_kwargs=generateKwargs
    )
    
    import json
    rawOutput = json.dumps(result)
    print(rawOutput)
    
    outputTextPath = Path("transcription.txt")
    outputTextPath.write_text(rawOutput + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
