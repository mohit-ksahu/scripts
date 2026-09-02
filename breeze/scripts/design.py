import breeze

model = breeze.load("models/breeze-tts-2-q8_0.gguf", use_gpu=True)
audio = model.generate(
    text="(sigh) There is nothing quite like holding a warm cup of coffee on a quiet weekend morning while watching the sunlight fill the garden.",
    instruction="A warm, relaxed person speaking with peaceful contentment.",
    cfg_scale=2.5,
    seed=42,
)
audio.save("output.wav")