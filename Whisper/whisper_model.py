import os
import sys
from pathlib import Path
import torch
import torchaudio as ta
import torchaudio.functional as F

class WhisperModel:
    def __init__(self, model_name="openai/whisper-tiny", device=None, cache_dir=None):
        if cache_dir is None:
            cache_dir = Path(__file__).resolve().parent / "models"
            
        cache_dir_str = str(cache_dir)
        os.environ["HF_HOME"] = cache_dir_str
        os.environ["HF_HUB_CACHE"] = cache_dir_str
        os.environ["TRANSFORMERS_CACHE"] = cache_dir_str
        
        from transformers import pipeline

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        else:
            self.device = device
            
        with torch.no_grad():
            self.pipe = pipeline(
                "automatic-speech-recognition",
                model=model_name,
                device=self.device,
                torch_dtype=torch.float32,
                chunk_length_s=30,
            )

    def transcribe(self, audio_path, **kwargs):
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file '{audio_path}' not found.")
            
        # Load audio using torchaudio
        waveform, sample_rate = ta.load(str(audio_path))
        
        # Resample to 16kHz (Whisper expected sample rate)
        if sample_rate != 16000:
            waveform = F.resample(waveform, sample_rate, 16000)
            
        # Mix down to mono if multi-channel
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
            
        audio_data = waveform.squeeze(0).numpy()
        
        # Run Whisper model inference with torch.no_grad()
        with torch.no_grad():
            result = self.pipe(audio_data, **kwargs)
            
        return result
