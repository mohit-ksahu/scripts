# Kokoro-82M TTS

Generate high-quality, lightweight text-to-speech audio using Kokoro-82M.

## Features

- **High-Quality TTS:** 82 million parameter model delivering premium 24kHz audio.
- **Multiple Voices:** Support for multiple built-in voice styles (e.g., `af_heart`, `af_bella`, `am_michael`, etc.).
- **Multi-Language Support:** Easily configure different languages by passing the corresponding `lang_code`.
- **Text Chunking:** Automatically splits long-form text at sentence boundaries for smooth, natural synthesis and to respect the model's 510-token context limit.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
import kokoroTTS

# Load the model (automatically uses CUDA, MPS, or CPU)
model = kokoroTTS.model(lang_code='a')

# Generate audio from text (supports single voice or blended voices)
kokoroTTS.generate(
    model=model,
    text="Hello, this is a test of Kokoro-82M voice synthesis.",
    outputPath="output.wav",
    voice="af_heart,af_bella",  # Blend voices using a comma, or use a single voice like "af_heart"
    speed=1.0
)
```

## API Reference

### `kokoroTTS.model(lang_code, device=None)`

Loads and returns the `KokoroModel`. Auto-detects device (CUDA, MPS, CPU).

### `kokoroTTS.generate(model, text, outputPath, voice, speed, maxChars=500, **kwargs)`

Generates text-to-speech audio:
* Automatically splits input text into semantic chunks at sentence boundaries (up to 300 characters).
* Executes inference on each chunk, concatenates the resulting audio arrays, and saves the output to `outputPath`.

## Supported Languages & Voices

Voices in Kokoro-82M follow the convention `[language_prefix][gender]_[name]`.

### Supported Language Codes

| Code | Language |
|---|---|
| `a` | American English |
| `b` | British English |
| `e` | Spanish |
| `f` | French |
| `h` | Hindi |
| `i` | Italian |
| `j` | Japanese |
| `p` | Brazilian Portuguese |
| `z` | Mandarin Chinese |

> [!NOTE]
> Japanese (`j`) and Mandarin Chinese (`z`) require their respective `misaki` package extras installed (e.g., `pip install misaki[ja]` or `pip install misaki[zh]`).

### Available Voices

#### American English (Prefix: `a`)
- **Female (`af_`):** `af_heart`, `af_alloy`, `af_aoede`, `af_bella`, `af_jessica`, `af_kore`, `af_nicole`, `af_nova`, `af_river`, `af_sarah`, `af_sky`
- **Male (`am_`):** `am_adam`, `am_echo`, `am_eric`, `am_fenrir`, `am_liam`, `am_michael`, `am_onyx`, `am_puck`, `am_santa`

#### British English (Prefix: `b`)
- **Female (`bf_`):** `bf_alice`, `bf_emma`, `bf_isabella`, `bf_lily`
- **Male (`bm_`):** `bm_daniel`, `bm_fable`, `bm_george`, `bm_lewis`

#### Japanese (Prefix: `j`)
- **Female (`jf_`):** `jf_alpha`, `jf_glowing`, `jf_neutral`, `jf_tealtree`
- **Male (`jm_`):** `jm_kondo`

#### Mandarin Chinese (Prefix: `z`)
- **Female (`zf_`):** `zf_xiaobei`, `zf_xiaoni`, `zf_xiaoxiao`, `zf_xiaoyi`
- **Male (`zm_`):** `zm_yunjian`, `zm_yunxi`, `zm_yunye`, `zm_yunze`

#### Spanish (Prefix: `e`)
- **Female (`ef_`):** `ef_dora`
- **Male (`em_`):** `em_alex`, `em_santa`

#### French (Prefix: `f`)
- **Female (`ff_`):** `ff_sixtine`
- **Male (`fm_`):** `fm_julien`

#### Hindi (Prefix: `h`)
- **Female (`hf_`):** `hf_ananya`, `hf_alpha`, `hf_beta`
- **Male (`hm_`):** `hm_omega`

#### Italian (Prefix: `i`)
- **Female (`if_`):** `if_sara`
- **Male (`im_`):** `im_nicola`

#### Brazilian Portuguese (Prefix: `p`)
- **Female (`pf_`):** `pf_dora`
- **Male (`pm_`):** `pm_alex`, `pm_santa`

> [!TIP]
> You can blend two or more voices together by separating their IDs with a comma (e.g., `voice="af_bella,af_heart"`). This will automatically load and average their style vectors.
