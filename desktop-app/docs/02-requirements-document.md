# CaptionLayer Desktop — Requirements Document

## 1. Purpose

This document defines the functional and non-functional requirements for the CaptionLayer Desktop application.

The desktop app is a standalone local application that processes audio into a structured caption timeline JSON using the following logical stages:

```text
Audio -> Alignment -> Segmentation -> Styling -> Timeline -> Export (JSON)
```

## 2. Product Boundary

The desktop application:

- runs locally on a user machine
- may call external LLM APIs for selected tasks
- performs backend-style Python processing inside the app
- stores projects locally
- exports structured JSON locally

The desktop application does not need:

- public API endpoints
- multi-tenant backend infrastructure
- cloud deployment design
- webhooks
- server-based billing systems

## 3. Functional Requirements

### 3.1 Project management

The app shall allow the user to:

- create a new project and select the root directory/location for the project folder
- open an existing local project
- prominently display the active project name in the application window
- rename a project
- save project state locally
- reopen the last-used or recent projects

### 3.2 Asset intake

The app shall allow the user to:

- import an audio file
- provide optional transcript text
- provide optional style instructions
- view basic file metadata such as duration and format when available

The app shall validate:

- supported audio file types
- file readability
- size or duration constraints if defined by the app settings

### 3.3 Speech path selection

The app shall:

- use forced alignment when both audio and text are available
- use ASR transcription when text is not available
- normalize outputs from either path into a shared word timing structure

### 3.4 Alignment and transcription

The app shall:

- generate a transcript when no source text is supplied
- align transcript words to timestamps
- record confidence or alignment quality values when available
- detect and surface mismatch warnings when supplied text diverges from audio significantly

### 3.5 Segmentation

The app shall:

- segment text into display-friendly caption units
- use deterministic rules such as punctuation, max characters, or duration thresholds
- optionally use an LLM API to refine segmentation decisions

### 3.6 Styling

The app shall:

- allow users to provide style instructions
- attach style metadata to segments and optionally to words
- support basic style presets or rules
- optionally use an LLM API to infer emphasis and style hints

### 3.7 Timeline editing

The app shall allow the user to:

- inspect generated segments
- edit segment text
- edit segment timing
- re-run segmentation
- apply or adjust style metadata

### 3.8 Export

The app shall:

- export the canonical timeline as JSON, SRT, or VTT
- provide a dedicated view to inspect and preview the generated JSON output
- allow initiating exports directly from the JSON view
- preserve structured metadata in the JSON export
- save the export to a user-selected local path, defaulting to the project's export directory

### 3.9 Settings and configuration

The app shall provide settings for:

- LLM API key and provider configuration
- model selection when relevant
- processing preferences
- local storage paths
- logging or debug mode options

## 4. Canonical Export Requirements

The JSON export should contain, at minimum:

- project metadata
- source asset metadata
- transcript text
- word-level timing data
- segment-level timing data
- style metadata
- timeline version or generation metadata

The JSON schema should be consistent regardless of whether the source came from ASR or forced alignment.

## 5. Non-Functional Requirements

### 5.1 Performance

The app should remain responsive while processing by using background workers, threads, or subprocesses.

Long-running tasks shall not freeze the UI.

### 5.2 Reliability

The app should:

- recover gracefully from processing failures
- preserve project data across sessions
- provide error messages for failed stages
- avoid corrupting timeline data on partial failure

### 5.3 Usability

The app should provide:

- clear stage-by-stage progress updates
- basic logs or status reporting
- easy-to-understand project workflow
- a simple review-and-export path

### 5.4 Maintainability

The codebase should be modular so that:

- UI concerns are separated from processing logic
- alignment, segmentation, styling, and export modules can evolve independently
- future export formats can be added without redesigning the core data model

### 5.5 Portability

The app should be designed so it can be packaged for common desktop operating systems, especially Windows as an initial priority.

### 5.6 Security

The app should:

- store API keys securely where practical
- avoid exposing sensitive keys in logs
- handle user files locally unless explicitly sent to configured external APIs

## 6. Technical Requirements

### Recommended technology baseline

- Python as the main implementation language
- PySide6 or PyQt for desktop UI
- local JSON or lightweight database for project persistence
- Python processing modules for ASR, alignment, segmentation, style inference, and export

### External dependency handling

The app may rely on:

- external LLM APIs for refinement tasks
- local or external ASR/alignment engines depending on implementation choice

The architecture should allow fallback behavior if the LLM stage is unavailable.

## 7. Constraints

- the app must remain useful even without a public backend API
- the canonical data model must stay central
- the desktop app should avoid overreaching into full video-editing responsibilities in the initial version

## 8. Out-of-Scope Items for Initial Desktop Version

- real-time live captioning
- collaborative editing
- cloud sync
- team workspaces
- public API server
- enterprise admin features
- billing and subscription management

## 9. Acceptance Criteria

The initial desktop version is acceptable when a user can:

- create a local project
- load audio
- optionally provide transcript text
- run processing end to end
- inspect and edit the resulting timeline
- export a valid canonical timeline JSON
- recover from normal validation or API errors without losing the project
