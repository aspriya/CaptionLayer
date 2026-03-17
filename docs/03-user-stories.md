# CaptionLayer — User Stories

## 1. Creator / Solo User Stories

### Upload and generate

* As a creator, I want to upload an audio file so that I can automatically generate captions.
* As a creator, I want to optionally paste the original script so that the generated timings are more accurate.
* As a creator, I want to describe the caption look in plain language so that I can help the styling engine (LLM) to its task according to my preferences.

### Edit and refine

* As a creator, I want to edit caption text after generation so that I can fix wording and punctuation.
* As a creator, I want to adjust caption segment timing so that the flow matches my preference.
* As a creator, I want to emphasize selected words so that key moments stand out.

### Export and use

* As a creator, I want to export captions as SRT so that I can use them in common editors and platforms.
* As a creator, I want to export captions as ASS so that I can preserve richer styling.
* As a creator, I want a preview render so that I can quickly judge the output before downloading.

## 2. Agency User Stories

### Repeatable styling

* As an agency user, I want reusable style presets so that all client videos follow brand consistency.
* As an agency user, I want to duplicate projects so that I can process similar client jobs quickly.
* As an agency user, I want project history so that I can revisit and adjust past outputs.

### Scale and coordination

* As an agency user, I want predictable processing status so that I can plan delivery timelines.
* As an agency user, I want structured exports so that my editors can continue work in external tools.

## 3. API Customer User Stories

### Integration

* As a developer, I want to submit audio and optional text through an API so that my application can automate caption generation.
* As a developer, I want asynchronous job handling so that large files do not block user requests.
* As a developer, I want webhook notifications so that my system can react when jobs finish.

### Data quality

* As a developer, I want word-level timing data so that I can build my own caption renderer.
* As a developer, I want segment-level style hints so that I can apply custom presentation logic downstream.
* As a developer, I want deterministic export retrieval URLs so that I can fetch output files reliably.

## 4. Internal Operations User Stories

### Observability

* As an operator, I want job statuses and failure reasons so that I can troubleshoot user issues.
* As an operator, I want processing metrics by stage so that I can identify bottlenecks.
* As an operator, I want audit logs for project changes so that support issues are explainable.

### Billing

* As an operator, I want processed-minute tracking so that billing and quota enforcement are accurate.
* As an operator, I want export usage tracking so that premium features can be billed separately.

## 5. Admin User Stories

* As an admin, I want to manage style presets so that new product themes can be offered without code changes.
* As an admin, I want to disable abusive accounts so that system capacity is protected.
* As an admin, I want to inspect failed jobs so that support can resolve issues quickly.

## 6. Edge Case User Stories

* As a user, I want the system to work even when I only have audio and no script.
* As a user, I want the system to warn me when my uploaded text does not match the spoken audio closely enough.
* As a user, I want the system to detect unsupported audio formats before a job is processed.
* As a user, I want to re-run processing with different style instructions without re-uploading the same file.

## 7. Future User Stories

* As a user, I want to upload video and preview captions directly on it.
* As a user, I want multilingual caption translation while preserving style intent.
* As a user, I want collaborative editing with teammates.
* As a developer, I want white-label configuration for styles and API outputs.
