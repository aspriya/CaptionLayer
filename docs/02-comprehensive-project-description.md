# CaptionLayer — Project Description

CaptionLayer transforms audio into structured caption data.

## 1.Core flow:

Audio → Alignment → Segmentation → Styling → Timeline → Export

Core asset:
Structured caption timeline JSON

Vision:
Become the standard caption layer for video systems and AI tools.


## 2. Problem Statement

Existing subtitle and caption solutions usually fall into one of three weak categories:

1. transcription tools that output plain text with timestamps
2. creator apps with flashy styling but poor API support
3. enterprise subtitle workflows that are rigid and not creator-friendly

Users increasingly need a system that can:

* accept audio and optional script text
* align words accurately
* segment text in a human-friendly way
* attach style meaning to specific segments or words
* let users edit results
* export in multiple formats
* integrate into products through an API

This project addresses that gap.

## 3. Vision

Build a platform that converts spoken content into **structured, styled caption data** that is usable by both humans and machines.

The system should not think of captions as fixed text blocks. It should treat them as timed visual objects with semantic and stylistic properties.

## 4. Core User Value

For UI users:

* faster caption creation
* better-looking captions
* editable timing and text
* useful exports

For API users:

* automated caption generation
* structured word/segment timings
* style-aware output
* easy integration with video or avatar pipelines

## 5. Functional Scope

The system should support the following flow:

### Input

* upload audio
* optionally provide the original text
* optionally provide style instructions
* optionally choose a target language
* later: upload a video for preview application

### Processing

* detect whether source text exists
* if not, run ASR to produce transcript
* if text exists, run forced alignment against audio
* produce word-level timings
* segment content into display-friendly caption units
* annotate segments with style metadata
* generate export files

### Editing

* adjust text
* adjust timing
* choose style preset
* emphasize words
* choose display mode and visual style

### Output

* preview in UI
* export subtitle files
* export structured JSON
* later: render burned-in or overlay caption outputs

## 6. Non-Functional Goals

* job-based asynchronous processing
* scalable API-first backend
* low-friction browser UI
* stable storage and retrieval
* deterministic export generation
* future support for collaborative editing

## 7. Why Option C Is the Right Core

The recommended backend logic is:

```
Text + Audio → forced alignment
↓
LLM → segment captions and attach style hints
↓
Renderer / exporter → files, preview, downstream use
```

This approach is stronger than direct subtitle generation because:

* alignment gives precise timing
* LLM segmentation improves readability
* style metadata enables more expressive exports
* the same structured output can feed many downstream targets

## 8. Canonical Data Model Philosophy

The system should store one main truth object:

* project
* source assets
* transcript
* word timings
* display segments
* style metadata
* export artifacts

Everything else should be derived from this.

This avoids making SRT or VTT the center of the system, which would limit future capability.

## 9. Core Technical Components

### A. Asset intake

Responsible for receiving and validating audio, text, and user instructions.

### B. Speech understanding

Responsible for transcription or alignment.

### C. Caption intelligence

Responsible for semantic splitting, phrase grouping, emphasis detection, and style mapping.

### D. Editing layer

Responsible for user modifications and project persistence.

### E. Export layer

Responsible for transforming caption data into different formats.

### F. API layer

Responsible for enabling third-party access.

## 10. Style System

The style system should not just store colors and fonts. It should also express caption behavior.

Possible style attributes:

* capitalization mode
* emphasis behavior
* pacing behavior
* word highlighting mode
* animation family
* line breaking preference
* safe-zone layout hints
* color / typography tokens

## 11. Export Philosophy

Support two classes of output:

### Machine-friendly

* JSON timeline
* webhook payloads
* edit-state project files

### Human / media-friendly

* SRT
* VTT
* ASS
* preview render
* later: burned video and overlay output

## 12. Suggested Tech Stack

### Frontend

* Next.js
* TypeScript
* Tailwind or equivalent
* waveform + timeline components

### Backend

* FastAPI preferred for processing-oriented backend
* or Node/TypeScript if unified stack is preferred

### Workers

* Python workers for alignment, ASR, LLM orchestration, export generation

### Infra

* Postgres
* object storage
* Redis or queue broker
* containerized workers

## 13. Why Users Would Choose This Product

* better than raw transcription outputs
* more flexible than rigid subtitle tools
* easier to integrate than creator-only apps
* gives both API and UI
* lets users keep captions editable

## 14. MVP Boundary

The MVP should focus on:

* audio upload
* optional text input
* transcription/alignment
* timeline generation
* style presets
* editable segment text
* export to JSON/SRT/VTT/ASS

The MVP should not initially overcommit to:

* full video editing
* complex team collaboration
* live real-time captioning
* advanced alpha overlay video rendering

## 15. Long-Term Positioning

This project can become:

* a standalone SaaS
* an API platform for creator tools
* an infrastructure layer for talking-head generation pipelines
* a white-labeled caption engine for agencies and platforms
