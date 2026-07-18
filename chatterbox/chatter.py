import re
import platform
from pathlib import Path
import torch
import torchaudio as ta
from chatterboxModel import ChatterboxModel

def chunkText(text, maxChars=250):
    rawSegments = re.split(r'([.!?]+(?:\s+|$))', text.strip())
    sentences = []
    for idx in range(0, len(rawSegments) - 1, 2):
        sentence = rawSegments[idx].strip()
        punc = rawSegments[idx+1].strip()
        if sentence:
            sentences.append(sentence + punc)
    if rawSegments[-1].strip():
        sentences.append(rawSegments[-1].strip())

    chunks = []
    currentChunk = []
    currentLen = 0
    for sentence in sentences:
        sentenceLen = len(sentence)
        if currentLen + sentenceLen + (1 if currentChunk else 0) > maxChars:
            if currentChunk:
                chunks.append(" ".join(currentChunk))
            currentChunk = [sentence]
            currentLen = sentenceLen
        else:
            currentChunk.append(sentence)
            currentLen += sentenceLen + (1 if len(currentChunk) > 1 else 0)

    if currentChunk:
        chunks.append(" ".join(currentChunk))
    return chunks

def model(device=None):
    if device is None:
        device = "cpu" if platform.system() == "Darwin" and not torch.cuda.is_available() else None
    return ChatterboxModel(device=device)

def generate(model, text, outputPath, promptPath=None, **genKwargs):
    outputPath = Path(outputPath)
    outputPath.parent.mkdir(parents=True, exist_ok=True)
        
    chunks = chunkText(text, maxChars=300)
    if promptPath:
        promptPath = Path(promptPath)
        if not promptPath.exists():
            promptPath = None
    
    waveforms = []
    with torch.no_grad():
        for i, chunk in enumerate(chunks, 1):
            # Pass the promptPath only on the first chunk to extract and cache the speaker embedding.
            # Subsequent chunks reuse the cached embedding, ensuring consistency while running 10x faster.
            chunkPrompt = str(promptPath) if (i == 1 and promptPath) else None
            waveform = model.generate(text=chunk, audio_prompt_path=chunkPrompt, **genKwargs)
            waveforms.append(waveform)
            
    combinedWaveform = torch.cat(waveforms, dim=-1)
    ta.save(str(outputPath), combinedWaveform, model.model.sr)
    
    # Free memory
    del waveforms
    del combinedWaveform
    import gc
    gc.collect()
    
    return str(outputPath)
