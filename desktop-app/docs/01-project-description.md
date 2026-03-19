# CaptionLayer Desktop — Project Description

## 1. Overview

CaptionLayer Desktop is a standalone desktop application that converts audio into structured, styled caption timeline data.

Core pipeline:

```text
Audio -> Alignment -> Segmentation -> Styling -> Timeline -> Export (JSON)
```

The desktop version focuses on a local-first workflow. It does not expose a public API, does not need cloud deployment architecture, and does not need SaaS billing or multi-tenant infrastructure. Instead, it packages the full creator workflow into a single desktop application while still allowing selected stages to use external LLM APIs for higher-quality segmentation and style refinement.

## 2. Product Thesis

The primary artifact is not a rendered subtitle file. It is the **structured caption timeline JSON**.

That timeline should capture:

- source transcript
- word-level timings
- display-friendly caption segments
- segment and word-level style metadata
- project-level processing metadata
- export-ready structured data

This allows the desktop app to become a practical authoring and processing tool rather than just a subtitle exporter.

## 3. Product Goal

Provide users with a local desktop tool that can:

- ingest raw audio
- align transcript text to speech when text is available
- transcribe audio when text is not available
- split content into readable caption segments
- apply style-aware metadata to those segments
- let users review and edit the timeline
- export a canonical JSON file for later use by renderers, editors, or automation tools

## 4. Target Users

### Primary users

- solo creators producing captioned videos
- podcast editors
- talking-head video creators
- internal media teams
- developers who want a local caption processing tool

### Secondary users

- researchers experimenting with caption intelligence
- agencies preparing timeline data for downstream video tools
- educators preparing caption assets for course content

## 5. Desktop Product Scope

### Included

- desktop UI
- local project management
- audio import
- optional script text import
- transcription path
- forced alignment path
- caption segmentation
- style metadata generation
- timeline viewing and editing
- JSON export
- settings for LLM/API keys and processing preferences

### Excluded from this desktop version

- public REST API exposure
- webhooks
- multi-user collaboration
- subscription billing
- cloud deployment architecture
- server-side queue infrastructure

## 6. Core Workflow

### Input stage

The user imports:

- an audio file
- optional script text
- optional style instructions
- optional processing preferences

### Processing stage

The app decides:

- if text exists: run forced alignment
- if text does not exist: run ASR, then normalize transcript and timings

Then it performs:

- word timing normalization
- caption segmentation
- style metadata generation
- timeline creation

### Review stage

The user reviews:

- transcript
- words and timings
- caption segments
- style metadata

The user may edit text, timing, segmentation, and style selections.

### Output stage

The app exports:

- canonical timeline JSON

Future exports such as SRT, VTT, or ASS can be added later, but JSON remains the main output.

## 7. Core Value Proposition

CaptionLayer Desktop should deliver value through five things:

1. reliable local project workflow
2. better caption segmentation than raw ASR output
3. support for text-plus-audio alignment
4. style-aware structured timeline data
5. clean export of canonical JSON for downstream usage

## 8. Product Positioning

CaptionLayer Desktop should be positioned as:

> A local caption intelligence workbench that transforms audio into editable, structured caption timeline JSON.

This keeps the desktop app focused and avoids turning it into a full video editor.

## 9. Success Criteria

A successful first version should allow a user to:

- open the app and create a local project
- import audio and optional text
- process audio into a valid timeline
- inspect and edit segments
- apply style instructions or presets
- export a clean JSON timeline without needing any web deployment

## 10. Future Expansion Possibilities

Possible future enhancements:

- SRT, VTT, ASS exports
- preview caption rendering
- waveform-based editing
- reusable style presets
- packaging for Windows/macOS/Linux
- optional offline models for transcription and segmentation support
