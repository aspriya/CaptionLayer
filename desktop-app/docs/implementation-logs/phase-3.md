# Phase 3: Segmentation & Refinement Implementation Log

## Overview
Phase 3 focused on implementing the segmentation logic to split the raw continuous transcription from WhisperX into readable, chunked segments. We introduced a deterministic rule-based segmenter and an optional LLM-based refiner using Google Gemini for casing and punctuation. We also updated the UI to support viewing these segments in a table format and managing API keys.

## What We Built
1.  **Rule-Based Segmenter (`src/pipeline/segmentation/segmenter.py`)**:
    *   Implemented deterministic chunking based on character limits, word counts, and trailing punctuation.
    *   Ensures consistent caption lengths without relying entirely on AI.
2.  **Gemini Refiner (`src/pipeline/segmentation/gemini_refiner.py`)**:
    *   Integrated `google-generativeai` to utilize the Gemini 2.5 Flash model.
    *   Added logic to refine casing and punctuation of the segmented text while strictly preserving word timings and preventing hallucinated structural changes.
3.  **Settings Manager (`src/infrastructure/settings/settings_manager.py`)**:
    *   Created a configuration manager to securely store and retrieve user settings, specifically the Gemini API Key, in a local `settings.json` file (typically under `~/.config/captionlayer/`).
4.  **UI Enhancements (`src/ui/windows/main_window.py`)**:
    *   Replaced the basic `QListWidget` timeline with a robust `QTableWidget` to clearly display start times, end times, and segmented text.
    *   Added an "Integrations" section in the Configuration panel to allow users to input and save their Gemini API key.
5.  **Pipeline Integration (`src/workers/transcription_worker.py`)**:
    *   Updated the `TranscriptionWorker` `QThread` to seamlessly chain WhisperX -> Canonical Mapping -> Rule Segmentation -> Conditional Gemini Refinement (if an API key is available).

## Wins
*   **Structured Pydantic Data**: The strict Pydantic `CanonicalTimeline` proved its value here, making it trivial to pass data between the mapping layer, rule segmenter, and the Gemini refiner without losing timing information.
*   **Modular Pipeline**: Chaining the Rule-Based Segmenter *before* the Gemini Refiner resulted in a more robust architecture. The LLM only needs to focus on punctuation/casing rather than calculating chunk splits, which reduces cognitive load on the prompt and improves consistency.
*   **Background Processing**: The `QThread` continues to cleanly encapsulate the heavy AI processing, keeping the UI responsive even during external API calls to Gemini.
*   **Dynamic UI**: The `QTableWidget` makes reviewing captions significantly clearer than a raw list.

## Difficulties & Challenges
*   **UI String Replacement Issues**: Modifying the massive `main_window.py` class via standard string replacement tools was difficult due to indentation sensitivity and the large volume of interconnected UI methods.
    *   *Solution*: We deployed a custom Python injection script (`patch.py`) to surgically insert the new UI components (API key fields and the `QTableWidget`), bypassing the limitations of fuzzy text matching.
*   **Workspace Context Tracking**: When executing `uv` commands in background terminals, we occasionally lost the relative context of the `desktop-app/` root, requiring strict defensive `cd "desktop-app"` prefixes before running scripts.
*   **LLM Strictness**: Enforcing Gemini to *only* modify casing and punctuation without altering the underlying word structures required careful prompt engineering to ensure the mapping back to Pydantic didn't fail.

## Next Steps
Proceeding to **Phase 4: Export & Polish**. We will focus on:
1.  Taking the finalized `CanonicalTimeline` Pydantic model and exporting it to standard subtitle formats (SRT, VTT).
2.  Adding export configuration options to the UI.
3.  General app polish and bug fixing.