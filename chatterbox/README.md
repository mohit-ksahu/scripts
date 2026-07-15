# Chatterbox TTS

Clone any target speaker's voice instantly from a WAV reference file and generate high-quality text-to-speech audio using Chatterbox Turbo.

## Key Features

- **Voice Cloning:** Clone a speaker's voice using a single WAV reference file.
- **Text Chunking:** Automatically splits long-form text at sentence boundaries for smooth synthesis.
- **Embedding Caching:** Speeds up subsequent chunk generation by 10x by caching the speaker embedding vector.

## Installation

Install the required dependencies:
```bash
pip install -r requirements.txt
```

## API Usage

You can initialize the model and synthesize text with voice cloning using the utilities in `chatter.py`.

### 1. Basic Speech Generation

```python
import chatter

# Load the model (automatically uses CUDA, MPS, or CPU)
model = chatter.model()

# Generate audio from text
chatter.generate(
    model=model,
    text="Hello, this is a test of voice synthesis.",
    outputPath="output.wav"
)
```

### 2. Voice Cloning with a Reference Audio

Pass a prompt WAV audio reference to clone a target speaker's voice:

```python
import chatter

model = chatter.model()

chatter.generate(
    model=model,
    text="This synthesized speech will sound like the speaker in the prompt audio.",
    outputPath="output.wav",
    promptPath="path/to/reference_speaker_voice.wav",
    norm_loudness=True,
    temperature=0.6,
    repetition_penalty=1.1
)
```

## Key Utility Functions

### `chatter.model(device=None)`
Loads and returns the `ChatterboxModel`. Auto-detects device, with Apple Silicon CPU fallback to prevent compilation issues with MPS.

### `chatter.generate(model, text, outputPath, promptPath=None, **genKwargs)`
Generates voice cloning text-to-speech.
* Automatically splits input text into chunks (up to 300 characters) at sentence boundaries.
* Extracts and caches the speaker embedding on the first chunk to ensure consistent voice quality across long-form synthesis.