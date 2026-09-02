# LLM

Interact with GGUF language models on your hardware using an interactive console chat loop built on `llama-cpp-python`.

## Key Features

- **Hardware Accelerated Inference:** Run quantized GGUF models efficiently across CPU and GPU backends.
- **Conversational History:** Maintains context across message turns.
- **Custom System Prompts:** Configure the behavior and personality of the model.
- **Response Streaming:** Output responses token-by-token in real-time.

## Installation

Install the required dependencies:
```bash
pip install -r requirements.txt
```

## API Usage

Import the `LLM` class from `model.py` to run model inferences.

### 1. Initialization

```python
from model import LLM

# Initialize the model with path and parameters
model = LLM(
    model_path="path/to/your/model.gguf",
    n_ctx=4096,
    n_gpu_layers=10,
    flash_attn=True
)
```

### 2. Synchronous Generation

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

response = model.generate(messages, stream=False)
print(response)
```

### 3. Streaming Generation

```python
stream = model.generate(messages, stream=True, temperature=0.7, top_p=0.95)

for chunk in stream:
    delta = chunk["choices"][0]["delta"]
    if "content" in delta:
        print(delta["content"], end="", flush=True)
print()
```