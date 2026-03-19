import os
import shutil
from pathlib import Path

class EnvironmentChecker:
    @staticmethod
    def check_ffmpeg() -> bool:
        """Check if FFmpeg is installed and accessible in the system PATH."""
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def check_models_downloaded() -> bool:
        """
        Heuristic check to see if Faster-Whisper and PyTorch model caches exist.
        On first run, WhisperX downloads these models to the user's .cache directory.
        """
        # Common locations for HuggingFace and PyTorch caches
        hf_cache = Path.home() / ".cache" / "huggingface" / "hub"
        torch_cache = Path.home() / ".cache" / "torch"
        
        # Check standard Windows paths as well if different from Path.home() 
        # (Though Path.home() usually maps correct on Windows as C:\Users\Username)
        
        models_found = False

        if hf_cache.exists():
            # Check if there are any faster-whisper models inside
            for item in hf_cache.iterdir():
                if item.is_dir() and "faster-whisper" in item.name.lower():
                    models_found = True
                    break
                    
        # Just a basic heuristic. If they aren't found here, it'll show a red cross, 
        # but the app might still try to download them on the first run.
        return models_found
