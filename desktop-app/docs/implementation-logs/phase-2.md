# Phase 2 Implementation Log

## Overview
In Phase 2, we brought the core pipeline logic to life. The goal was to establish reliable local project persistence, implement an adapter for WhisperX to handle ASR and forced alignment, map those results to our custom Canonical Timeline schema, and connect everything asynchronously to our PySide6 UI.

### What We Did
1. **Local Persistent Storage:** Implemented `ProjectManager` (`src/infrastructure/storage/project_manager.py`) to scaffold new project folders (`assets`, `intermediate`, `timelines`, `exports`) and handle file copying. 
2. **ASR & Alignment Pipeline:** Created `WhisperXAdapter` (`src/pipeline/alignment/whisperx_adapter.py`) to wrap transcription and word-level alignment gracefully, defaulting to `cpu` and `int8` if CUDA is unavailable.
3. **Canonical Normalization:** Created `whisperx_to_canonical` in `src/domain/schemas/mapper.py` which takes raw WhisperX dictionary outputs and forces them into our strict Pydantic `CanonicalTimeline` structure.
4. **App Integration & Concurrency:** Created `TranscriptionWorker` extending `QThread` (`src/workers/transcription_worker.py`) to handle the heavy AI processing in the background. Hooked this worker to the PySide6 UI to update labels in real-time without freezing the app.

## Errors & Bumps Encountered
1. **Missing Intermediate Directories:** We initially encountered errors trying to create files in paths where the parent directories (`src/infrastructure`, `src/app`) were not yet created.
2. **Missing WhisperX Timings:** Sometimes WhisperX doesn't provide word-level timings for highly overlapped or silent segments. Our mapper needed to be robust enough to handle words lacking `start`/`end` keys without crashing.
3. **Environment Assumptions:** We realized WhisperX intimately relies on standard system dependencies (FFmpeg) and aggressively downloads large model files upon its first execution, which might confuse an end user if they aren't warned.

## Silly Mistakes & Learnings for Next Phase
- **Always Pre-Create Paths:** File writing logic needs absolute assurance that containing directories exist. `Path.mkdir(parents=True, exist_ok=True)` is our best friend.
- **Background Processing is Mandatory:** WhisperX locks the execution context heavily; `QThread` worked perfectly and will be the standard mechanism for our upcoming Gemini/Segmentation pipelines.
- **The Need for a Config/Environment Checker:** Users running this out of the box will scratch their heads if FFmpeg isn't installed. Hence, we're pivoting perfectly to include an Environment Config Check (Phase 2.1) before doing advanced segmentation.