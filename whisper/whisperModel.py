import os
import sys
from pathlib import Path
import torch
import torchaudio as ta
import torchaudio.functional as F

class WhisperModel:
    def __init__(self, modelName="openai/whisper-tiny", device=None, cacheDir=None):
        if cacheDir is None:
            cacheDir = Path(__file__).resolve().parent / "models"
            
        cacheDirStr = str(cacheDir)
        os.environ["HF_HOME"] = cacheDirStr
        os.environ["HF_HUB_CACHE"] = cacheDirStr
        os.environ["TRANSFORMERS_CACHE"] = cacheDirStr
        
        from transformers import pipeline

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        else:
            self.device = device
            
        with torch.no_grad():
            self.pipe = pipeline(
                "automatic-speech-recognition",
                model=modelName,
                device=self.device,
                torch_dtype=torch.float32,
                chunk_length_s=30,
            )

    def transcribe(self, audioPath, **kwargs):
        audioPath = Path(audioPath)
        if not audioPath.exists():
            raise FileNotFoundError(f"Audio file '{audioPath}' not found.")
            
        # Load audio using torchaudio
        waveform, sampleRate = ta.load(str(audioPath))
        
        # Resample to 16kHz (Whisper expected sample rate)
        if sampleRate != 16000:
            waveform = F.resample(waveform, sampleRate, 16000)
            
        # Mix down to mono if multi-channel
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
            
        audioData = waveform.squeeze(0).numpy()
        
        # Run Whisper model inference with torch.no_grad()
        with torch.no_grad():
            result = self.pipe(audioData, **kwargs)
            
        return result
