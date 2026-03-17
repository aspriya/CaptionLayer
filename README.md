# CaptionLayer

**CaptionLayer is the intelligence layer for captions.** 

An API-first and UI-driven platform that converts audio into structured, styled captions. Instead of stopping at basic transcription and raw subtitle files, CaptionLayer treats captions as a **designable data layer**, turning raw speech into a comprehensive timeline with exact word-level timing, semantic segmentation, and style metadata.

## 🌟 The Core Philosophy

> The primary product artifact is not the rendered subtitle file. It is the **structured caption timeline** (JSON).

By centering around a structured data model, CaptionLayer can power:
- Raw structured exports (JSON for timelines and metadata)
- Traditional subtitle formats (SRT, WebVTT, ASS)
- Styled video preview renders & burned-in caption overlays
- Downstream developer integrations & creator tools

## ⚡ Key Features

- **Multi-Modal Input Support:** Process raw audio alone, or provide audio + source text for high-precision forced alignment. Style instructions can also be applied.
- **Intelligent Segmentation:** Combines deterministic text rules with LLM-assisted refinement for human-friendly boundaries, semantic groupings, and natural emphasis.
- **Style-Aware Metadata:** Captions are aware of style elements like emphasis, pacing, capitalization, and animations.
- **API & UI Interfaces:** Designed not just as a creator web app, but as a headless caption engine for AI video tools, podcast clippers, and automated media pipelines.

## 🛠 Architecture & Tech Stack (Proposed)

### Frontend
- Next.js (TypeScript) & Tailwind CSS
- Web-based waveform UI and caption editor

### Backend
- Next.js Route Handlers (API routes)
- Asynchronous job/project orchestration via queues

### Processing Workers (Python)
- ASR for transcription 
- Forced Alignment engines for sync
- LLM for segmentation & semantic styling
- Render/Export generators

### Infrastructure
- Relational Database (PostgreSQL) for metadata
- Object Storage for audio and exports
- Redis / MQ caching and job queueing

## 📖 Documentation

The `docs` directory contains the complete structural blueprint and design decisions for CaptionLayer. This is designed to serve as the single source of truth for the platform:

1. `01-saas-blueprint.md` - Overall system vision, strategy, and go-to-market structure.
2. `02-comprehensive-project-description.md` - Core product flow, problem statement, and technical components.
3. `03-user-stories.md` - Detailed behavior and expectations from the end-user perspective.
4. `04-mvp-and-post-mvp-steps.md` - Roadmap and sequencing of development phases.
5. `05-database-entities.md` - Core data models guiding the system.
6. `06-api-endpoints.md` - The REST API design for the headless infrastructure.
7. `07-processing-pipeline.md` - The step-by-step intelligence pipeline details.
8. `08-mvp-feature-set.md` - The concise boundary for the Minimum Viable Product.

---

*CaptionLayer — Transforming audio into structured, styled, and integrable caption data.*
