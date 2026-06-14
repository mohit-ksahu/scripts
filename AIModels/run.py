from models import LlamaModel

model = LlamaModel(
    "models/Phi-4-mini-instruct-Q4_K_M.gguf",
    chat_format=None,
    n_ctx=16384,
    type_k=8,
    type_v=8
)
messages = [{"role": "system", "content": "You are a helpful AI assistant. Do not use Markdown in your responses. Always respond in plain text."}]

while True:
    user_input = input("> ").strip()
    if not user_input:
        continue
        
    messages.append({"role": "user", "content": user_input})
    
    response = ""
    stream = model.generate(messages, stream=True, temperature=0.7, top_p=0.95)
    for chunk in stream:
        delta = chunk['choices'][0]['delta']
        if 'content' in delta:
            text = delta['content']
            print(text, end="", flush=True)
            response += text
    
    print()
    messages.append({"role": "assistant", "content": response})