import re
import platform
from pathlib import Path
import torch
import torchaudio as ta
from kokoroModel import KokoroModel

def chunkText(text, maxChars=500):
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

def model(lang_code, device=None):
    if device is None:
        device = "cpu" if platform.system() == "Darwin" and not torch.cuda.is_available() else None
    return KokoroModel(lang_code=lang_code, device=device)

def generate(model, text, outputPath, voice, speed, maxChars=500, **kwargs):
    outputPath = Path(outputPath)
    outputPath.parent.mkdir(parents=True, exist_ok=True)
        
    chunks = chunkText(text, maxChars=maxChars)
    
    waveforms = []
    with torch.no_grad():
        for chunk in chunks:
            waveform = model.generate(text=chunk, voice=voice, speed=speed, **kwargs)
            waveforms.append(waveform)
            
    combinedWaveform = torch.cat(waveforms, dim=-1)
    ta.save(str(outputPath), combinedWaveform, model.sr)
    
    # Free memory
    del waveforms
    del combinedWaveform
    import gc
    gc.collect()
    
    return str(outputPath)
