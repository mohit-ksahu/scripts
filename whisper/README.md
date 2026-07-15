# Whisper

Perform high-accuracy local speech-to-text transcription utilizing OpenAI's Whisper model via Hugging Face `transformers`. The pipeline automatically preprocesses input audio (resampling to 16kHz and mixing multi-channel files down to mono) and outputs word-level timestamps.

## Key Features

- **Automated Resampling & Mono Mixing:** Automatically downmixes multi-channel inputs and resamples incoming audio to 16kHz (matching Whisper's expected format).
- **Flexible Device Selection:** Auto-detects device, supporting CUDA, CPU, and MPS.
- **Local Model Caching:** Saves downloaded Hugging Face models in the local `models/` directory.

## Installation

Install the required dependencies:
```bash
pip install -r requirements.txt
```

## API Usage

Import `WhisperModel` from `whisperModel.py` to perform local audio transcription.

### 1. Initialization

```python
from whisperModel import WhisperModel

# Initialize the model (defaults to openai/whisper-tiny)
model = WhisperModel(model_name="openai/whisper-tiny")
```

### 2. Basic Transcription

```python
# Transcribe audio file
result = model.transcribe("path/to/audio.wav")
print(result["text"])
```

### 3. Advanced Configuration (Timestamps & Language)

```python
# Transcribe with language forcing and word-level timestamps
result = model.transcribe(
    "path/to/audio.wav",
    return_timestamps="word",
    generate_kwargs={
        "language": "english",
        "task": "transcribe"
    }
)

print(result)
```