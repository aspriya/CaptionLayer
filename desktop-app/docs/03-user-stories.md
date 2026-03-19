# CaptionLayer Desktop — User Stories

## 1. Creator User Stories

### Project setup

- As a creator, I want to create a local project so that I can organize work by audio asset or video episode.
- As a creator, I want to reopen a saved project later so that I can continue editing without repeating processing.

### Input and processing

- As a creator, I want to import an audio file so that I can generate structured captions from it.
- As a creator, I want to optionally paste the original script so that alignment can be more accurate than raw transcription alone.
- As a creator, I want to provide style instructions so that the output timeline better matches the look and feel I want later.
- As a creator, I want to see which processing path was used so that I understand whether the result came from ASR or forced alignment.

### Review and editing

- As a creator, I want to inspect word timings so that I can trust the generated timeline.
- As a creator, I want to edit segment text so that I can improve punctuation, readability, or wording.
- As a creator, I want to adjust segment timing so that the display flow better matches my intended pacing.
- As a creator, I want to re-run segmentation so that I can generate more readable caption groups without re-importing the audio.
- As a creator, I want to adjust style hints or emphasis so that the timeline is ready for downstream rendering.

### Output

- As a creator, I want to export the project as structured JSON so that I can use it in another renderer or workflow.
- As a creator, I want the exported JSON to preserve timings and style metadata so that I do not lose important information.

## 2. Developer / Power User Stories

### Processing control

- As a developer, I want to configure external LLM provider settings so that I can use my own API key and model choice.
- As a developer, I want processing modules to be replaceable so that I can experiment with different ASR or alignment tools.
- As a developer, I want the app to keep a stable canonical JSON schema so that other local tools can consume the output predictably.

### Debugging and inspection

- As a developer, I want to inspect intermediate outputs such as transcript text, word timings, and segments so that I can debug quality issues.
- As a developer, I want basic logs for each processing stage so that I can understand failures and bottlenecks.

## 3. Research / Experimentation User Stories

- As a researcher, I want to compare outputs from audio-only versus audio-plus-text workflows so that I can evaluate quality differences.
- As a researcher, I want to tweak segmentation rules and style instructions so that I can study how caption readability changes.
- As a researcher, I want to keep projects local so that sensitive or experimental data stays on my machine except when I intentionally call external APIs.

## 4. Reliability and Error Handling Stories

- As a user, I want clear validation messages when my audio file is unsupported so that I know how to fix the issue.
- As a user, I want the app to warn me if my provided transcript does not match the spoken audio closely enough so that I do not trust a broken alignment blindly.
- As a user, I want a failed LLM stage to fail gracefully so that I can still keep or export partial non-LLM results when possible.
- As a user, I want the application to save project state safely so that I do not lose work if the app closes unexpectedly.

## 5. Future User Stories

- As a user, I want waveform-based editing so that I can adjust timing more visually.
- As a user, I want additional export formats such as SRT or ASS so that I can use the same project across more tools.
- As a user, I want reusable style presets so that I can apply the same visual logic across many projects.
- As a user, I want optional offline models for some stages so that I can reduce dependence on external APIs.
