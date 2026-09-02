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