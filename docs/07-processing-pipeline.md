# CaptionLayer — Pipeline

## 1. Goal

Convert uploaded audio, optional text, and optional style instructions into a structured caption timeline and downloadable export files.

## 2. High-Level Pipeline

```
Input Intake
↓
Validation + normalization
↓
Speech path selection
  - ASR path if no text
  - Alignment path if text exists
↓
Word timing normalization
↓
Segmentation
↓
Style inference / preset application
↓
Timeline persistence
↓
Export generation
↓
Optional preview rendering
```

## 3. Detailed Stages

## Stage A — Input intake

Receive:

* audio file
* optional source text
* optional style instructions
* optional selected preset
* language metadata if provided

Actions:

* validate file type
* validate duration and size
* store raw assets
* create project/job records

## Stage B — Audio preprocessing

Normalize audio into an internal standard format when needed.

Possible actions:

* resample
* convert channels
* standardize container/codec
* compute duration

## Stage C — Speech path decision

### Path 1: audio only

* run ASR
* produce transcript
* produce initial timings if available

### Path 2: audio + text

* run forced alignment
* compare alignment success
* flag mismatch if uploaded text and audio diverge too much

## Stage D — Word timing normalization

Normalize outputs from ASR or aligner into a shared schema:

* token index
* word text
* start_ms
* end_ms
* confidence if available

This stage is critical because all downstream logic should consume one standard structure.

## Stage E — Caption segmentation

Use a hybrid approach:

* deterministic rules first
* LLM refinement second

### Rule-based suggestions

* punctuation boundaries
* phrase length caps
* minimum display duration
* maximum characters per line
* balancing readability

### LLM refinement

* improve sentence splitting
* detect emphasis-worthy phrases
* preserve semantic grouping
* avoid awkward breaks

## Stage F — Style tagging

Apply style using:

* selected preset
* user instructions
* simple rules
* optional LLM assistance

Possible outputs:

* segment style class
* emphasized words
* line break behavior
* capitalization hints
* animation hints

## Stage G — Timeline persistence

Persist:

* transcript
* word timings
* segment objects
* style metadata
* timeline version

## Stage H — Export generation

Generate requested formats:

* canonical JSON
* SRT
* VTT
* ASS

Each export should derive from the same active timeline version to ensure consistency.

## Stage I — Optional preview rendering

Generate a lightweight preview render:

* static background or transparent simulation
* styled caption timing
* compressed output for quick review

This is useful but should remain asynchronous.

## 4. Error Handling Strategy

### Hard failures

* unreadable audio
* unsupported format
* system processing failure

### Soft warnings

* text/audio mismatch
* low confidence ASR sections
* style instructions partially unsupported

## 5. Reprocessing Strategy

Support reprocessing without forcing re-upload:

* resegment existing timings
* apply different preset
* re-export without rerunning full speech pipeline

This is important for both cost control and speed.

## 6. Observability

Track per-stage:

* queued time
* processing time
* failure reason
* output quality metrics if available

## 7. Performance Advice

Keep these stages decoupled:

* transcription/alignment
* segmentation/style inference
* export generation
* preview rendering

That separation allows retries and cheaper recomputation.
