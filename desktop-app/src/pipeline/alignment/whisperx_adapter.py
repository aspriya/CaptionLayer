import os
import torch
import whisperx
from typing import Dict, Any, Optional

class WhisperXAdapter:
    def __init__(self, model_name: str = "base", device: str = "cpu", compute_type: str = "int8"):
        """Initialize WhisperX adapter. 
        Parameters:
        - model_name: e.g. "base", "small", "medium", "large-v2"
        - device: "cuda" or "cpu"
        - compute_type: "int8", "float16", "float32"
        """
        # Auto-detect CUDA if available
        if device == "cuda" and not torch.cuda.is_available():
            print("CUDA not available, falling back to CPU")
            device = "cpu"
            compute_type = "int8" # safe fallback
        elif device == "cpu":
            # float16 is not supported on CPU for WhisperX by default
            compute_type = "int8"
            
        self.device = device
        self.compute_type = compute_type
        self.model_name = model_name
        self.model = None

    def load_model(self):
        """Loads the transcription model into memory."""
        if not self.model:
            print(f"Loading WhisperX {self.model_name} model on {self.device} ({self.compute_type})...")
            self.model = whisperx.load_model(self.model_name, self.device, compute_type=self.compute_type)
            print("Model loaded.")

    def transcribe_and_align(self, audio_path: str, batch_size: int = 16, language: Optional[str] = "en") -> Dict[str, Any]:
        """
        Runs transcription and forced alignment on the audio.
        Returns a dictionary with segments and word-level timings.
        """
        self.load_model()
        
        print(f"Loading audio from {audio_path}...")
        audio = whisperx.load_audio(audio_path)
        
        # 1. Transcribe
        print("Starting transcription...")
        result = self.model.transcribe(audio, batch_size=batch_size, language=language)
        
        language = result.get("language", language)
        print(f"Transcription complete (Language: {language}).")
        
        # 2. Align
        print("Loading alignment model...")
        model_a, metadata = whisperx.load_align_model(language_code=language, device=self.device)
        
        print("Aligning words to audio...")
        aligned_result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)
        print("Alignment complete.")
        
        return aligned_result
