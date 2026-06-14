# Chatterbox TTS — High-Quality Voice Cloning

This component provides premium voice cloning and text-to-speech synthesis utilizing Chatterbox Turbo.

## Features

- **Voice Cloning:** Feed any high-quality WAV audio file reference to clone the target speaker's voice instantly.
- **Text Chunking:** Automatic, robust sentence-boundary chunking up to 300 characters to process long-form narratives.
- **Mac CPU Optimization:** Seamlessly forces CPU on Apple Silicon to prevent Metal Performance Shaders (MPS) compilation issues.

## Usage

You can run the script from the project root directory or directly inside the `chatter/` folder.

### From Root:
```bash
python3 chatter/chatter_run.py "Hello from Chatterbox clone!"
```

### From chatter/ Directory:
```bash
cd chatter
python3 chatter_run.py "Hello from Chatterbox clone!"
```

### Full Options:
```bash
python3 chatter/chatter_run.py script.txt -p assets/audio1.wav -o output.wav -t 0.8
```

| Flag | Description | Default |
|------|-------------|---------|
| `text` | Raw text string or path to a `.txt` file | required |
| `-p`, `--prompt` | WAV file for voice cloning | `assets/audio1.wav` |
| `-o`, `--output` | Output WAV path | `output1.wav` |
| `-t`, `--temperature` | Sampling temperature | `0.8` |
| `-rp`, `--repetition_penalty` | Repetition penalty | `1.1` |
| `--top_p` | Top-p sampling | `0.95` |
| `--top_k` | Top-k sampling | `1000` |
| `--no-norm` | Disable loudness normalization | off |
