from model import LLM

model = LLM(
    "models/Ministral-3-3B-Instruct-2512-Q5_K_M.gguf",
    chat_format=None,
    n_ctx=4096,
    n_gpu_layers=10,
)

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful AI assistant. "
            "Never use markdown. "
            "Reply in short plain text only."
        ),
    }
]

while True:
    user_input = input("> ").strip()

    if user_input == "/exit":
        break

    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    response = ""
    stream = model.generate(
        messages,
        stream=True,
        temperature=0.7,
        top_p=0.95,
    )

    for chunk in stream:
        delta = chunk["choices"][0]["delta"]
        if "content" in delta:
            text = delta["content"]
            print(text, end="", flush=True)
            response += text

    print()
    messages.append({"role": "assistant", "content": response})
