import re
import platform
from pathlib import Path
import torch
import torchaudio as ta
from chatterbox_model import ChatterboxModel

def chunk_text(text, max_chars=250):
    raw_segments = re.split(r'([.!?]+(?:\s+|$))', text.strip())
    sentences = []
    for idx in range(0, len(raw_segments) - 1, 2):
        sentence = raw_segments[idx].strip()
        punc = raw_segments[idx+1].strip()
        if sentence:
            sentences.append(sentence + punc)
    if len(raw_segments) % 2 != 0 and raw_segments[-1].strip():
        sentences.append(raw_segments[-1].strip())
        
    chunks = []
    current_chunk = []
    current_len = 0
    for sentence in sentences:
        sentence_len = len(sentence)
        if current_len + sentence_len + (1 if current_chunk else 0) > max_chars:
            if current_chunk:
                chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_len = sentence_len
        else:
            current_chunk.append(sentence)
            current_len += sentence_len + (1 if len(current_chunk) > 1 else 0)
            
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def model(device=None):
    if device is None:
        device = "cpu" if platform.system() == "Darwin" and not torch.cuda.is_available() else None
    return ChatterboxModel(device=device)

def generate(model, text, output_path, prompt_path=None, **gen_kwargs):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
        
    chunks = chunk_text(text, max_chars=300)
    if prompt_path:
        prompt_path = Path(prompt_path)
        if not prompt_path.exists():
            prompt_path = None
    
    waveforms = []
    with torch.no_grad():
        for i, chunk in enumerate(chunks, 1):
            # Pass the prompt_path only on the first chunk to extract and cache the speaker embedding.
            # Subsequent chunks reuse the cached embedding, ensuring consistency while running 10x faster.
            chunk_prompt = str(prompt_path) if (i == 1 and prompt_path) else None
            waveform = model.generate(text=chunk, audio_prompt_path=chunk_prompt, **gen_kwargs)
            waveforms.append(waveform)
            
    combined_waveform = torch.cat(waveforms, dim=-1)
    ta.save(str(output_path), combined_waveform, model.model.sr)
    
    # Free memory
    del waveforms
    del combined_waveform
    import gc
    gc.collect()
    
    return str(output_path)