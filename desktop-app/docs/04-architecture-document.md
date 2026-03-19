# CaptionLayer Desktop — Architecture Document

## 1. Goal

Define the architecture for a standalone desktop application that processes audio into a structured caption timeline JSON.

Core pipeline:

Audio -> Alignment -> Segmentation -> Styling -> Timeline -> Export (JSON)

The architecture supports a local-first product with Python-based processing, optional use of external LLM APIs, and a responsive desktop UI.

## 2. Principles

### 2.1 Canonical timeline first

The canonical timeline JSON is the source of truth. All editing and exports should derive from this model rather than from subtitle formats.

### 2.2 Local-first workflow

Projects, inputs, intermediate data, and exports should live locally unless the user explicitly enables external API-based processing.

### 2.3 Separation of concerns

The application should separate:

- UI layer
- application orchestration layer
- processing pipeline modules
- persistence layer
- external service adapters

### 2.4 Replaceable processing stages

ASR, alignment, segmentation, styling, and export components should be modular so they can evolve independently.

## 3. High-Level Components

- Desktop UI
- Application Controller / Orchestrator
- Processing Pipeline Manager
- Asset Intake Module
- ASR Module
- Alignment Module
- Segmentation Module
- Styling Module
- Timeline Builder
- Export Module
- Persistence Layer
- LLM API Adapter
- Optional speech and alignment tool adapters

## 4. Layered Design

### 4.1 Presentation Layer

Responsible for:

- project creation and opening
- file import flows
- status display
- timeline review and editing
- settings management
- export actions

Recommended implementation:

- PySide6 UI with a main window, project views, and processing dialogs

### 4.2 Application Layer

Responsible for:

- coordinating user actions
- initiating processing jobs
- routing outputs between modules
- handling validation and state transitions
- updating the UI with progress and errors

This layer should not contain low-level signal processing or LLM logic directly.

### 4.3 Processing Layer

Responsible for the actual pipeline logic.

Submodules:

#### Asset Intake Module

- validates inputs
- reads file metadata
- copies or references local assets in the project workspace

#### ASR Module

- produces transcript text and approximate timings for audio-only projects

#### Alignment Module

- aligns provided text against speech when source text exists
- produces word-level timings and quality metadata

#### Segmentation Module

- groups words into caption segments
- uses rule-based logic first
- may call LLM APIs for refinement

#### Styling Module

- applies style metadata and emphasis hints
- merges preset logic, user instructions, and optional LLM responses

#### Timeline Builder

- transforms transcript, word timings, segments, and style metadata into the canonical timeline model

#### Export Module

- serializes the canonical timeline into JSON
- writes exported files to local disk

### 4.4 Persistence Layer

Responsible for local storage of:

- project metadata
- source asset references
- transcripts
- word timings
- timeline versions
- settings and API preferences
- logs where needed

Possible storage options:

- project folder with JSON files for simplicity
- SQLite for metadata plus JSON artifacts if needed later

For the first version, project-folder plus JSON is a strong and simple approach.

## 5. Project Storage Model

A project can be stored in a local folder structure like this:

- project-name/
- project.json
- assets/audio/
- intermediate/transcript.json
- intermediate/word_timings.json
- intermediate/segmentation.json
- timelines/timeline.v1.json
- exports/caption_timeline.json
- logs/process.log

This keeps the data transparent and easy to debug.

## 6. Processing Flow

### Stage A — Input intake

- user creates or opens a project
- audio file is imported
- optional script text and style instructions are provided
- app validates the inputs

### Stage B — Speech understanding

- if source text exists, the app uses the alignment module
- otherwise, the app uses the ASR module
- output is normalized into a shared word timing structure

### Stage C — Segmentation

- deterministic segmentation rules run first
- optional LLM refinement improves readability and semantic grouping

### Stage D — Styling

- style preset and free-text instructions are processed
- style metadata is attached to segments and optionally words

### Stage E — Timeline build

- canonical timeline JSON is created and versioned

### Stage F — Review and edit

- user inspects and edits timeline content in the UI
- edits update the local canonical timeline state

### Stage G — Export

- final timeline is exported as JSON

## 7. Concurrency and Responsiveness

Heavy operations must not block the UI.

Recommended approach:

- UI thread for presentation only
- worker threads or subprocesses for heavy tasks
- event or signal-based progress updates back to the UI

Potential candidates for background execution:

- ASR
- forced alignment
- LLM API calls
- large-file parsing
- export generation if needed

## 8. External API Integration

The desktop app may use external LLM APIs for:

- segmentation refinement
- style inference
- emphasis detection

Design guidance:

- isolate LLM calls behind an adapter interface
- keep prompts and parsing logic outside the UI layer
- support provider-specific configuration in settings
- fail gracefully if the API is unavailable or misconfigured

## 9. Canonical Data Model Guidance

The timeline JSON should include:

- project metadata
- source metadata
- transcript text
- word timing list
- segment list
- style metadata
- processing provenance
- version information

Important rule:

All later exports or renderers should read from this canonical structure.

## 10. Error Handling Strategy

### Hard failure examples

- unreadable file
- unsupported format
- alignment engine crash
- invalid export path

### Soft failure examples

- transcript/audio mismatch warning
- low-confidence alignment sections
- LLM style inference unavailable

The architecture should allow the app to preserve intermediate results where possible.

## 11. Suggested Code Structure

- desktop-app/
- docs/
- src/app/
- src/app/controllers/
- src/app/state/
- src/ui/
- src/ui/windows/
- src/ui/dialogs/
- src/ui/widgets/
- src/domain/models/
- src/domain/services/
- src/domain/schemas/
- src/pipeline/intake/
- src/pipeline/asr/
- src/pipeline/alignment/
- src/pipeline/segmentation/
- src/pipeline/styling/
- src/pipeline/timeline/
- src/pipeline/export/
- src/infrastructure/storage/
- src/infrastructure/settings/
- src/infrastructure/logging/
- src/infrastructure/llm/
- src/workers/jobs/
- src/workers/signals/
- tests/
- assets/

## 12. Recommended Technology Choices

- Python for the whole desktop app
- PySide6 for UI
- Pydantic or dataclasses for internal schema modeling
- local JSON-based persistence first, SQLite if needed later
- modular adapters for LLM providers and speech tools

## 13. MVP Architecture Recommendation

For MVP, optimize for clarity over complexity.

Recommended choices:

- one desktop app process
- background workers for heavy tasks
- project-folder persistence
- JSON as canonical storage and export
- simple settings screen for API keys and model preferences
- minimal but clean timeline editor

## 14. Long-Term Evolution

This architecture can later grow into:

- richer waveform editing
- additional exports like SRT, VTT, and ASS
- local model support
- plugin-style processing modules
- render preview support
- optional sync or shared project storage
