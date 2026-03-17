# CaptionLayer — MVP Plan

## 1. MVP Goal

Deliver a usable product that lets users:

* upload audio
* optionally provide text
* generate timed captions
* edit text segments
* choose style presets
* export JSON, SRT, VTT, and ASS

## 2. MVP Build Steps

### Step 1 — Product definition

* lock the core use cases
* define the canonical caption JSON schema
* define the initial style preset model
* define export targets

### Step 2 — Asset intake

* implement account auth
* implement project creation
* implement audio upload
* implement optional text and instructions intake
* validate file formats and size

### Step 3 — Speech pipeline

* add transcription path for audio-only jobs
* add alignment path for audio + text jobs
* normalize outputs into a single word-timing format

### Step 4 — Caption intelligence layer

* implement segmentation rules
* add LLM-based segmentation refinement
* add style-tag assignment
* validate for common punctuation and phrase boundaries

### Step 5 — Persistence

* store projects, assets, transcripts, segments, style metadata, and exports
* version the timeline when edits occur

### Step 6 — UI editor

* project list
* upload form
* processing status view
* timeline/segment editor
* style preset selector
* export download view

### Step 7 — Export layer

* JSON export
* SRT export
* VTT export
* ASS export

### Step 8 — API layer

* create asynchronous job endpoints
* add status polling
* add webhook support
* add export retrieval endpoints

### Step 9 — Billing and quotas

* usage tracking
* project limits
* quota enforcement
* upgrade prompts

### Step 10 — Reliability hardening

* retries
* failure states
* logging
* metrics
* support visibility

## 3. Post-MVP Steps

### Phase 1 — Better editing and quality

* word-level timing editing
* waveform editing
* finer style controls
* transcript mismatch warnings
* improved alignment quality metrics

### Phase 2 — Better media experience

* video upload preview
* burned-in preview render
* side-by-side caption preview modes
* template gallery

### Phase 3 — Platform features

* team workspaces
* shared style libraries
* project duplication
* audit logs
* RBAC

### Phase 4 — API platform maturity

* SDKs
* rate-limit tiers
* usage dashboards
* signed webhooks
* batch jobs

### Phase 5 — Premium differentiation

* branded style packs
* AI restyling suggestions
* multilingual translation + timing preservation
* engagement-optimized caption presets
* editor embeddable widget

## 4. Suggested Execution Order

1. canonical data model
2. alignment/transcription pipeline
3. segmentation and style engine
4. export generation
5. basic UI
6. API exposure
7. billing
8. rendering extras

## 5. What Not to Build Too Early

Avoid spending early cycles on:

* full video editor behavior
* real-time live captioning
* overly complex team workflows
* alpha-channel media exports
* large template marketplaces

## 6. MVP Exit Criteria

MVP is ready when:

* processing is stable for clean input audio
* generated timelines are editable
* exports are correct and downloadable
* API jobs are reliable
* style presets are visibly useful
* usage can be metered and limited
