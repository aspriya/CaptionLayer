# Phase 2.1 Implementation Log

## Overview
In Phase 2.1, we focused on making the application robust and user-friendly before running compute-heavy workloads. This involved verifying the availability of critical system dependencies (FFmpeg) and large AI models, and communicating them clearly through a new Configuration UI.

### What We Did
1. **Environment Checker Utility:** Implemented `EnvironmentChecker` inside `src/infrastructure/environment.py`. This class uses `shutil.which` to detect checking FFmpeg and uses heuristic directory checks on `~/.cache` to see if `faster-whisper` and PyTorch model weights have been initialized locally.
2. **UI Architecture Upgrade:** Transformed the `main_window.py` shell from a simple flat layout to a `QStackedWidget` layout. This enables clean, stateful navigation between the "Project Workspace" and the newly created "Configuration" panel without instantiating modal dialogs.
3. **Configuration View:** Designed a modern, dark-themed settings panel that executes the `EnvironmentChecker` and reports back to the user with familiar traffic-light status indicators (✅ Green / ❌ Red / ⚠️ Amber), including an automated refresh mechanism.

## Errors & Bumps Encountered
1. **Model Cache Ambiguity:** The `whisperx` / `faster-whisper` ecosystem caches models in standard HuggingFace directories (`~/.cache/huggingface/hub`). Writing a cross-platform check (Windows vs Mac vs Linux) requires relying strictly on Python's `Path.home()` rather than hardcoding directory paths.
2. **PySide6 Layout Management:** Migrating an existing layout into a `QStackedWidget` required correctly re-parenting Qt elements and managing margins so the UI didn't visually jump when changing sidebar contexts.

## Silly Mistakes & Learnings for Next Phase
- **Heuristic Limitations:** Our check for `faster-whisper` is purely directory-based. We learned that the "Amber" state (missing models) is perfectly normal for a first-run since WhisperX acts permissively and downloads them on request. We properly annotated this with a disclaimer in the UI.
- **UI Scalability:** `QStackedWidget` is definitely the correct pattern to carry forward as we introduce Timeline Editors and Export modal variants in upcoming phases.