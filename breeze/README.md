# Breeze

A zero-dependency text-to-speech runtime for **Breeze-TTS-2 (GGUF)**.

---

## Features

* **Zero Heavy Dependencies**: Operates with only `numpy` and Python standard libraries: no PyTorch, TorchAudio, or compiler toolchains.
* **Precompiled Native Engine**: Bundles standalone native runtimes for macOS, Linux, and Windows statically linked with optimized BLAS and `ggml` CPU kernels.
* **Sub-Second Streaming**: Yields decoded 24 kHz audio chunks synchronously as frames are generated for low-latency voice applications.
* **Natural-Language Voice Design**: Synthesizes unique speaker identities directly from descriptive text prompts without reference audio.
* **Zero-Shot Voice Cloning**: Clones speaker timbre, cadence, and delivery from short reference audio clips.
* **Expressive Vocal Event Tags**: Supports inline emotional markers including `(sigh)`, `(laugh)`, `(cough)`, `(clears throat)`, and `(gasp)`.
* **Pure WAV Export**: Built-in 16-bit mono 24 kHz PCM WAV file encoding without external audio packages.

---

## Installation

### 1. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Model Weights

Download the quantized GGUF weights from [HoppouAI/Breeze-TTS-2.cpp](https://huggingface.co/HoppouAI/Breeze-TTS-2.cpp/tree/main) and place them inside the `models/` directory (e.g. `models/breeze-tts-2-q8_0.gguf`).

---

## Quick Start

### 1. Voice Design

Synthesize speech using natural-language voice descriptions without reference audio:

```python
import breeze

model = breeze.load("models/breeze-tts-2-q8_0.gguf", use_gpu=True)
audio = model.generate(
    text="(sigh) There is nothing quite like holding a warm cup of coffee on a quiet weekend morning while watching the sunlight fill the garden.",
    instruction="A warm, relaxed person speaking with peaceful contentment.",
    cfg_scale=2.5,
    seed=42,
)
audio.save("output.wav")
```

### 2. Context Manager

Automatically release native engine memory when synthesis completes:

```python
import breeze

with breeze.load("models/breeze-tts-2-q8_0.gguf", use_gpu=True) as model:
    audio = model.generate(
        text="(clears throat) I just got the tickets for the outdoor concert next Saturday, and the forecast says it will be completely clear and sunny.",
        instruction="An upbeat, friendly voice sharing exciting news with warmth.",
        cfg_scale=2.0,
        seed=100,
    )
    audio.save("output.wav")
```

### 3. Real-Time Streaming

Yield decoded audio chunks synchronously for sub-second playback latency:

```python
import breeze

model = breeze.load("models/breeze-tts-2-q8_0.gguf", use_gpu=True)
text = "(laugh) The golden retriever puppy learned how to fetch the frisbee on the very first try today, and now he refuses to put it down!"
for chunk in model.stream(
    text=text,
    instruction="A joyful, smiling storyteller speaking with bright energy.",
    cfg_scale=2.5,
    seed=777,
):
    chunk.save(f"chunk_{chunk.index}.wav")
```

### 4. Voice Cloning

Clone speaker timbre from reference audio using a matching transcript:

```python
import breeze

model = breeze.load("models/breeze-tts-2-q8_0.gguf", use_gpu=True)
audio = model.generate(
    text="(sigh) There has never been a better time to build, create, and invest across this entire nation. We are going to build the finest roads, modernize our bridges, and deliver the most incredible future for our families and communities.",
    instruction="A confident, energetic speaker delivering a speech with bold emphasis.",
    ref_audio="reference.wav",
    ref_text="I know that Congress is eager to pass an infrastructure bill and I am eager to work with you on legislation to deliver a new and important infrastructure investment including investments in cutting edge industries of the future.",
    cfg_scale=3.0,
    seed=42,
)
audio.save("cloned.wav")
```

---

## API Reference

### `breeze.load(path, use_gpu=True, lib_path=None)`
Loads the GGUF model binary into memory and initializes native C-ABI runtime structures. Returns an active `Model` instance.

### `Model.generate(...)`
| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `text` | `str` | *Required* | Input text string to synthesize into speech waveform. Supports inline emotional and non-speech vocal event tags: `(sigh)`, `(laugh)`, `(cough)`, `(clears throat)`, `(gasp)`, `[笑]`, `[叹气]`. |
| `instruction` | `str` | `"Speak clearly and naturally."` | Natural-language prompt controlling speaker identity (age, gender, accent, timbre) during voice design, or emotional tone and delivery cadence during voice cloning. |
| `ref_audio` | `str / Path / np.ndarray / Audio` | `None` | Path to a 16-bit PCM `.wav` file or float32 NumPy array providing the speaker reference timbre for zero-shot voice cloning. |
| `ref_text` | `str` | `None` | Verbatim text transcript of `ref_audio`. Required when `ref_audio` is supplied to align speaker acoustic features with phonetic tokens. |
| `cfg_scale` | `float` | `1.0` | Classifier-Free Guidance scale for logit steering. Higher values (`2.0` - `3.5`) strongly enforce the `instruction` style and vocal event tags. `1.0` disables guidance. |
| `seed` | `int` | `None` | Deterministic random number generator seed for reproducible token sampling and acoustic generation. Defaults to a random 31-bit integer when omitted. |
| `max_new_tokens` | `int` | `0` | Hard upper bound on generated autoregressive acoustic codebook frames. Setting `0` automatically uses the model's native context window limit. |
| `split_chars` | `int` | `0` | Character threshold for automatic paragraph and sentence chunking during long-form synthesis. Setting `0` defaults to 600 characters per chunk. |
| `temperature` | `float` | `0.0` | Softmax temperature for autoregressive token probability distribution. `0.0` enables deterministic greedy decoding; values > 0.0 introduce acoustic variation. |
| `top_k` | `int` | `0` | Top-K filtering cutoff restricting sampling to the K most probable tokens per step. Setting `0` disables top-k truncation. |
| `top_p` | `float` | `0.0` | Top-P (nucleus) sampling threshold accumulating probability mass. Setting `0.0` disables nucleus filtering; `0.9` retains the top 90% cumulative probability mass. |
| `repetition_penalty` | `float` | `0.0` | Logit penalty applied to previously generated token IDs to prevent repetitive audio artifacts or looping phonemes. Setting `0.0` disables the penalty. |
| `on_chunk` | `Callable` | `None` | Streaming callback invoked synchronously on every decoded float32 audio chunk (`Chunk` object). Return `False` to abort generation immediately. |

### `Model.stream(...)`
Synchronous generator yielding `Chunk` instances as frames are decoded in real-time. Accepts the same synthesis parameters as `Model.generate()`.

### `breeze.Audio`
* `audio.samples`: 1D contiguous float32 NumPy array containing normalized PCM audio waveform values in `[-1.0, 1.0]`.
* `audio.rate`: Audio sample rate in Hz (`24000` Hz for native MimiCodec output).
* `audio.duration`: Calculated playback length in seconds (`len(samples) / rate`).
* `audio.save(path)`: Encodes and writes the audio buffer to a standard 1-channel, 16-bit PCM `.wav` file at the specified file destination.
* `audio.to_numpy()`: Returns an isolated float32 NumPy array copy of the underlying waveform buffer.
* `audio.to_bytes()`: Converts normalized float32 samples to signed 16-bit integers and returns raw Little-Endian PCM byte stream.
* `audio.to_wav()`: Encodes and returns complete RIFF/WAV file format binary bytes in memory without writing to disk.

### `breeze.load_audio(path, rate=24000)`
Loads and resamples a `.wav` file into a 1D float32 NumPy array normalized to `[-1.0, 1.0]` at the specified sample rate.

---

## License

This project is licensed under the [Apache 2.0 License](LICENSE).