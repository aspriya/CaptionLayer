# CaptionLayer — MVP Features

## 1. MVP Objective

Ship a useful first version that solves a real workflow for both UI and API users without overbuilding.

## 2. Included MVP Features

### Authentication and account basics

* sign up / sign in
* basic subscription or quota awareness
* project dashboard

### Input workflow

* audio upload
* optional text input
* optional free-text style instructions
* basic language selection

### Processing

* transcription for audio-only inputs
* forced alignment for audio + text inputs
* word-level timing normalization
* segment generation
* style preset application
* timeline creation

### Editing

* edit segment text
* choose style preset
* re-run segmentation
* basic segment timing adjustment

### Exports

* JSON timeline export
* SRT export
* WebVTT export
* ASS export

### API

* project creation
* asset registration
* processing job submission
* job status retrieval
* export retrieval
* webhook notifications

### Usage and admin

* quota tracking
* processing logs
* failure states visible to users
* basic admin observability

## 3. Explicitly Out of MVP Scope

* collaborative editing
* direct full video editing
* real-time live caption generation
* multilingual translation workflows
* alpha-channel overlay video export
* extensive preset marketplace
* in-depth brand kit management

## 4. MVP UI Screens

* auth screens
* projects list
* create/upload screen
* processing status screen
* caption editor screen
* exports screen
* account/usage screen

## 5. MVP API Capability Summary

The MVP API should support:

* create a project
* upload/register audio
* submit process job
* get project and job status
* retrieve timeline JSON
* download exports
* receive webhook events

## 6. MVP Quality Bar

MVP should meet these standards:

* stable handling of clean short-to-medium audio
* visible value from style presets
* accurate enough word timing for standard creator workflows
* predictable export correctness
* reasonable asynchronous job reliability

## 7. MVP Positioning Statement

A simple way to describe the MVP:

> Upload audio, optionally provide the original text, choose a caption style, review the generated timeline, and export clean subtitle or structured caption outputs through either a browser UI or an API.
