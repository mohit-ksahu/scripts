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