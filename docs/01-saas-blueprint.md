# CaptionLayer — SaaS Blueprint

CaptionLayer is an API-first and UI-driven platform that converts audio into structured, styled captions.

## 1. Executive Summary

This SaaS provides **styled, editable, API-accessible caption generation** from audio, optional text, and optional style instructions. The core system turns raw speech into a structured caption timeline with word-level timing, semantic segmentation, and style metadata. Users can then preview, edit, export, or apply those captions to video in their own workflow.

The product should be positioned as **caption intelligence infrastructure**, not merely subtitle generation. The strongest value comes from the combination of:

- precise timing
- high-quality segmentation
- style-aware caption objects
- multi-format export
- API + UI
- editable project workflows

## 2. Product Thesis

Most caption tools stop at transcription and basic subtitle files. This product should instead treat captions as a **designable data layer**.

Core principle:

> The primary product artifact is not the rendered subtitle file. It is the structured caption timeline.

That timeline can power:

- subtitle exports
- styled overlays
- rendered preview videos
- downstream editing tools
- partner integrations
- future brand templates and automation

## 3. Target Customers

### Primary

- AI video tool builders
- talking-head / avatar SaaS products
- creator tools
- agencies producing short-form video
- podcast clipping tools
- internal media automation teams

### Secondary

- solo creators
- educators
- marketing teams
- course platforms
- podcast publishers

## 4. Core Inputs

The system should support:

- audio only
- audio + text
- audio + text + style instructions
- video + audio + optional text (later)
- TTS-originated audio and human-recorded audio

## 5. Core Outputs

### Canonical output

- structured JSON caption timeline

### Derived outputs

- SRT
- WebVTT
- ASS / SSA
- project JSON for later editing
- preview render
- burned-in video render (post-MVP or selective MVP)
- overlay alpha export (later)

## 6. Key Product Modes

### UI mode

A browser-based workflow where users upload inputs, preview results, edit segments, choose style presets, and export.

### API mode

A job-based processing API for developers and partner products. This should support webhook delivery, asynchronous processing, and export retrieval.

## 7. Differentiators

The moat should come from these layers, in this order:

1. reliable alignment quality
2. better segmentation than commodity ASR outputs
3. style metadata and presets
4. editable timeline UX
5. strong export coverage
6. integration-ready API

## 8. Commercial Packaging

### Possible plans

- Free: limited minutes/month, basic exports
- Pro: more minutes, style presets, editable projects
- Growth/API: higher throughput, webhooks, JSON exports
- Enterprise: SLA, white-label styles, custom processing rules

### Metering options

- billed by processed audio minute
- billed by render/export credits
- billed by active projects/storage
- billed by API jobs + overages

## 9. Architecture Summary

### Frontend

- Next.js app
- project dashboard
- upload flows
- caption editor
- export manager

### Backend API

- FastAPI (Python) backend
- auth
- project/job orchestration via workers
- export handling
- billing hooks

### Workers

- transcription / forced alignment
- LLM segmentation and style tagging
- format export generation
- optional preview rendering

### Storage

- object storage for audio and exports
- relational DB for metadata
- cache / queue system for jobs

## 10. Recommended System Shape

```text

Client UI / API Consumer

        ↓

API Layer

        ↓

Project + Job Orchestrator

        ↓

Processing Workers

  - ASR or alignment

  - segmentation

  - style tagging

  - export generation

  - render preview

        ↓

Storage + Retrieval
```

## 11. Strategic Recommendation

Build the product around the **canonical caption timeline JSON** , then derive all other exports from it. That decision will keep the product extensible and prevents the architecture from becoming trapped inside legacy subtitle formats.

## 12. Risks

### Product risks

* becoming a thin wrapper around transcription
* weak editing UX
* low perceived value if only basic formats are delivered

### Technical risks

* inaccurate alignment on noisy audio
* inconsistent LLM segmentation
* rendering cost if previews become too heavy
* queue buildup under API load

## 13. Success Criteria

A good MVP should achieve:

* strong timing on clean audio
* clean segment boundaries
* usable style presets
* fast export turnaround
* stable API job lifecycle
* clear developer adoption path

## 14. Long-Term Expansion

Possible expansion paths:

* brand-specific caption kits
* multilingual caption adaptation
* translation + restyling
* direct social-video integrations
* editor SDK / embeddable caption editor
* talking-head video caption overlays
* creator analytics around caption engagement
