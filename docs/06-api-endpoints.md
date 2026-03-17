# CaptionLayer — API

## 1. API Design Principles

* use asynchronous job processing for non-trivial work
* treat projects as the main container object
* expose both machine-friendly JSON and downloadable exports
* support polling and webhooks

Base path example:

`/v1`

## 2. Authentication

### POST /auth/signup

Create a user account.

### POST /auth/login

Authenticate and return token/session.

### POST /auth/logout

Terminate session.

### GET /auth/me

Return current user profile and plan info.

## 3. Projects

### POST /projects

Create a project.

Request:

* title
* source_language optional

Response:

* project object

### GET /projects

List user projects.

### GET /projects/

Get project details, status, and active timeline summary.

### PATCH /projects/

Update project metadata.

### DELETE /projects/

Archive or delete project.

## 4. Assets

### POST /projects//assets/upload-url

Create signed upload target.

### POST /projects//assets

Register uploaded asset metadata.

### GET /projects//assets

List assets.

### GET /projects//assets/

Get asset metadata.

## 5. Transcript and Processing Requests

### POST /projects//process

Start processing for a project.

Request example:

* audio_asset_id
* optional_text
* style_instruction_text optional
* style_preset_id optional
* source_language optional
* requested_exports [json, srt, vtt, ass]

Behavior:

* chooses transcription path or forced-alignment path
* enqueues downstream jobs

Response:

* processing job id
* project status

### GET /projects//jobs

List processing jobs.

### GET /projects//jobs/

Get job status and error details if failed.

## 6. Timelines and Segments

### GET /projects//timelines

List timeline versions.

### GET /projects//timelines/

Get full timeline including segments and optionally words.

### POST /projects//timelines//duplicate

Create a new timeline version from an existing one.

### PATCH /projects//timelines//segments/

Update segment text, timing, or style metadata.

### POST /projects//timelines//resegment

Re-run segmentation using current transcript and instructions.

### POST /projects//timelines//apply-style-preset

Apply a style preset to a timeline or subset of segments.

## 7. Styles

### GET /style-presets

List available style presets.

### POST /style-presets

Create a user style preset.

### GET /style-presets/

Get style preset.

### PATCH /style-presets/

Update style preset.

### DELETE /style-presets/

Delete style preset.

## 8. Exports

### POST /projects//exports

Generate export artifact.

Request:

* timeline_id
* export_type

### GET /projects//exports

List exports.

### GET /projects//exports/

Get export metadata and status.

### GET /projects//exports//download

Download export artifact.

## 9. Preview Rendering

### POST /projects//preview-render

Generate preview render from active timeline.

### GET /projects//preview-render/

Get preview render status.

## 10. Webhooks

### GET /webhooks

List webhook endpoints.

### POST /webhooks

Create webhook endpoint.

### PATCH /webhooks/

Update webhook endpoint.

### DELETE /webhooks/

Delete webhook endpoint.

## 11. Usage and Billing

### GET /usage

Return quota and usage summary.

### GET /usage/ledger

Return metering records.

### GET /plans

List plans.

### POST /billing/checkout

Start subscription checkout.

## 12. Suggested Webhook Events

* project.processing.started
* project.processing.completed
* project.processing.failed
* export.ready
* export.failed
* preview_render.ready
* preview_render.failed
