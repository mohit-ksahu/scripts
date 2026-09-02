import breeze

with breeze.load("models/breeze-tts-2-q8_0.gguf", use_gpu=True) as model:
    audio = model.generate(
        text="(clears throat) I just got the tickets for the outdoor concert next Saturday, and the forecast says it will be completely clear and sunny.",
        instruction="An upbeat, friendly voice sharing exciting news with warmth.",
        cfg_scale=2.0,
        seed=100,
    )
    audio.save("output.wav")