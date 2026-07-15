import os
import sys
from pathlib import Path
import torch
import torchaudio as ta

sys.modules["perth"] = type("", (), {
    "PerthImplicitWatermarker": lambda: type("", (), {
        "apply_watermark": lambda self, wav, *a, **k: wav
    })()
})

class ChatterboxModel:
    def __init__(self, device=None, cacheDir=None):
        if cacheDir is None:
            cacheDir = Path(__file__).resolve().parent / "models"
            
        cacheDirStr = str(cacheDir)
        os.environ["HF_HOME"] = cacheDirStr
        os.environ["HF_HUB_CACHE"] = cacheDirStr
        os.environ["TRANSFORMERS_CACHE"] = cacheDirStr
            
        from chatterbox.tts_turbo import ChatterboxTurboTTS

        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        else:
            self.device = device
            
        self.model = ChatterboxTurboTTS.from_pretrained(self.device)

    def generate(self, text, **kwargs):
        with torch.no_grad():
            return self.model.generate(text, **kwargs)