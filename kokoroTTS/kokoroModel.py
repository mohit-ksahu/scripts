import os
import sys
from pathlib import Path
import torch

class KokoroModel:
    def __init__(self, lang_code, device=None, cacheDir=None):
        if cacheDir is None:
            cacheDir = Path(__file__).resolve().parent / "models"
            
        cacheDirStr = str(cacheDir)
        os.environ["HF_HOME"] = cacheDirStr
        os.environ["HF_HUB_CACHE"] = cacheDirStr
        os.environ["TRANSFORMERS_CACHE"] = cacheDirStr
            
        from kokoro import KPipeline

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        else:
            self.device = device
            
        # KPipeline will automatically download model files and cache them under the specified HF_HOME
        self.pipeline = KPipeline(lang_code=lang_code, device=self.device)
        self.sr = 24000

    def generate(self, text, voice, speed, **kwargs):
        import numpy as np
        generator = self.pipeline(text, voice=voice, speed=speed, **kwargs)
        audios = []
        for _, _, audio in generator:
            if audio is not None and len(audio) > 0:
                audios.append(audio)
        
        if not audios:
            return torch.zeros(1, 0)
            
        combined_audio = np.concatenate(audios)
        waveform = torch.from_numpy(combined_audio).unsqueeze(0)  # Shape [1, num_samples]
        return waveform