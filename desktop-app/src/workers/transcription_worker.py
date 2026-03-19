from PySide6.QtCore import QThread, Signal
from pathlib import Path
import json

from src.infrastructure.storage.project_manager import ProjectManager
from src.infrastructure.settings.settings_manager import SettingsManager
from src.pipeline.alignment.whisperx_adapter import WhisperXAdapter
from src.domain.schemas.mapper import whisperx_to_canonical
from src.pipeline.segmentation.segmenter import RuleBasedSegmenter
from src.pipeline.segmentation.gemini_refiner import GeminiRefiner

class TranscriptionWorker(QThread):
    progress_signal = Signal(str)
    error_signal = Signal(str)
    finished_signal = Signal(str) # Emits the timeline JSON path

    def __init__(self, project_manager: ProjectManager, settings: SettingsManager, audio_path: Path):
        super().__init__()
        self.project_manager = project_manager
        self.settings = settings
        self.audio_path = audio_path

    def run(self):
        try:
            self.progress_signal.emit(f"Importing {self.audio_path.name}...")
            # Import to project
            imported_audio = self.project_manager.import_audio(str(self.audio_path))
            
            project_dir = self.project_manager.current_project_dir
            project_meta = self.project_manager.load_project(project_dir)

            self.progress_signal.emit("Loading transcription models...")
            # Note: For now using base on CPU to avoid massive memory requirement loops if missing CUDA.
            adapter = WhisperXAdapter(model_name="base", device="cpu", compute_type="int8")
            
            self.progress_signal.emit(f"Transcribing and aligning {imported_audio.name} (this will take time)...")
            result = adapter.transcribe_and_align(str(imported_audio))
            
            self.progress_signal.emit("Mapping generated data to Canonical Timeline...")
            timeline = whisperx_to_canonical(
                project_id=project_meta["project_id"],
                project_name=project_meta["name"],
                audio_filename=imported_audio.name,
                whisperx_result=result
            )

            self.progress_signal.emit("Applying Rule-Based Segmentation...")
            # We apply simple text layout chunking before saving.
            segmenter = RuleBasedSegmenter(max_words=6)
            timeline = segmenter.process(timeline)

            # Check if Gemini refinement is enabled
            gemini_key = self.settings.get("GEMINI_API_KEY")
            if gemini_key:
                self.progress_signal.emit("Refining segmentation with Gemini...")
                refiner = GeminiRefiner(api_key=gemini_key)
                timeline = refiner.process(timeline)
            else:
                self.progress_signal.emit("Skipping LLM refinement (No API Key).")

            # Dump canonical to file
            timeline_json = timeline.model_dump_json(indent=4)
            timeline_path = project_dir / "timelines" / "canonical_timeline.json"
            
            with open(timeline_path, "w", encoding="utf-8") as f:
                f.write(timeline_json)

            self.progress_signal.emit("Transcription complete!")
            self.finished_signal.emit(str(timeline_path))

        except Exception as e:
            self.error_signal.emit(str(e))
