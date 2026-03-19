# Implementation Plan

## Plan: CaptionLayer Desktop App Initialization

### TL;DR
Implementing a local-first desktop application for caption processing using Python (managed via `uv`), PySide6, and WhisperX. The app transforms audio into a canonical structured caption timeline JSON. We will start by drafting the schema, setting up a modern UI shell, and implementing the core pipeline with simple rule-based segmentation followed by Gemini-based refinements.

### Phases & Steps

**Phase 1: Foundation (Data Model & UI Skeleton)**
1. Draft the Canonical Timeline JSON schema (Pydantic models) — *Crucial first step as all pipeline stages depend on this data model.*
2. Set up the Python project structure using `uv` for package management, installing dependencies like `pyside6`, `whisperx`, and `pydantic`.
3. Build the initial PySide6 Main Window layout (sidebar, main content area, project status) focusing on a clean, modern creator aesthetic.

**Phase 2: Core Processing Pipeline**
1. Implement local project creation, persistence, and file intake.
2. Implement the ASR and Alignment module using `WhisperX` as a background worker.
3. Normalize WhisperX's output into the Canonical Timeline schema.

**Phase 2.1: Configuration & Environment Check UI**
1. Add a "Configuration" tab/section to the PySide6 UI.
2. Implement a system check to verify if `FFmpeg` is installed and available in the system PATH.
3. Implement a model check to verify if the Faster-Whisper and PyTorch models have been cached/downloaded (and add descriptive text that they will download automatically on first run).
4. Provide a clear visual indicator (e.g., green check / red cross) for these environment prerequisites.

**Phase 3: Segmentation & Timeline View**
1. Implement a rule-based segmentation module to chunk the WhisperX word timing data.
2. Integrate a Gemini-based refinement layer over the rule-based segmentation to improve readability and apply basic styling.
3. Build the Timeline Viewer/Editor in PySide6 to display segments and word timings, and allow editing.

**Phase 4: Export & Polish**
1. Implement the Export Module to output the canonical JSON file.
2. Add background thread workers for PySide6 to ensure the UI remains responsive during long-running tasks.

**Phase 5: UX Improvements & Advanced Export (Completed)**
1. Update `project_manager.py` and the UI to allow selecting the parent directory when creating a new project.
2. Modify `main_window.py` to prominently display the active project name in the application title bar and/or a visible header in the project workspace area.
3. Update the Export dialog/workflow to allow the user to select the destination folder (defaulting to `{project_dir}/exports/`).
4. Implement a "Code / JSON View" tab in the `main_window.py` to let the user inspect the compiled timeline JSON directly inside the app.
5. Add capabilities to export multiple formats (JSON, SRT, VTT) directly from the new Code/JSON view.

**Relevant files**
- `desktop-app/src/domain/schemas/timeline.py` — The core Pydantic data models for the timeline.
- `desktop-app/src/pipeline/alignment/whisperx_adapter.py` — A wrapper around WhisperX to abstract the ASR/Alignment tasks.
- `desktop-app/src/pipeline/segmentation/segmenter.py` — Includes deterministic segmentation and the Gemini refinement adapter.
- `desktop-app/src/ui/windows/main_window.py` — The primary PySide6 view.

**Verification**
1. Initialize the project with `uv init` and install dependencies.
2. Create a dummy test audio file and execute the core pipeline script offline.
3. Verify that WhisperX generates output, the rule-based+Gemini segmenter runs, and the app dumps a structured JSON timeline in the project folder.

**Decisions**
- **Package Manager**: Use `uv` for Python dependency management.
- **Segmentation Strategy**: Base layer of deterministic rules, enhanced by a Gemini-based model for deeper refinements.
- **UI Framework**: PySide6 for building a modern desktop interface.
- **Processing**: Local execution with WhisperX for ASR and optional text-audio forced alignment.