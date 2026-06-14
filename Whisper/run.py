import sys
from pathlib import Path
import torch
from whisper_model import WhisperModel

def main():
    import platform
    device = "cpu" if platform.system() == "Darwin" and not torch.cuda.is_available() else None
    
    model = WhisperModel(device=device)
    audio_path = Path("output.wav")
    
    if not audio_path.exists():
        sys.exit(1)

    return_timestamps = "word"      # Set to True, "word" (for word-level timestamps), or False
    generate_kwargs = {
        "language": "english",    # specify language (e.g. "english", "french") or None for auto-detection
        "task": "transcribe",     # "transcribe" to transcribe, "translate" to translate to English
    }

    result = model.transcribe(
        audio_path,
        return_timestamps=return_timestamps,
        generate_kwargs=generate_kwargs
    )
    
    import json
    raw_output = json.dumps(result)
    print(raw_output)
    
    output_text_path = Path("transcription.txt")
    output_text_path.write_text(raw_output + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
