# CaptionLayer — Database

## 1. Design Notes

Use a relational database such as Postgres for metadata and business objects, and object storage for media files and generated artifacts.

The entities below represent the minimum practical model.

## 2. Core Entities

## User

Represents an account holder.

Fields:

* id
* email
* name
* password_hash or external_auth_id
* plan_id
* status
* created_at
* updated_at

## Plan

Represents subscription configuration.

Fields:

* id
* name
* monthly_audio_minutes
* max_projects
* api_access_enabled
* webhook_enabled
* export_limits_json
* created_at
* updated_at

## Organization

Optional for future team support.

Fields:

* id
* name
* owner_user_id
* created_at
* updated_at

## Project

Represents a captioning job container and editable workspace.

Fields:

* id
* user_id
* organization_id nullable
* title
* source_language
* status
* active_timeline_version_id nullable
* created_at
* updated_at

## Asset

Represents uploaded or generated media/text assets tied to a project.

Fields:

* id
* project_id
* asset_type (audio, video, transcript_text, generated_export, preview_media)
* storage_path
* mime_type
* file_size_bytes
* duration_ms nullable
* checksum nullable
* created_at

## ProcessingJob

Represents asynchronous processing activity.

Fields:

* id
* project_id
* job_type (transcribe, align, segment, export, render_preview)
* status
* input_payload_json
* output_payload_json nullable
* error_message nullable
* started_at nullable
* completed_at nullable
* created_at

## Transcript

Represents the source transcript associated with a project.

Fields:

* id
* project_id
* transcript_source (uploaded_text, asr_generated, corrected_text)
* full_text
* language
* confidence_score nullable
* created_at
* updated_at

## WordTiming

Represents word-level alignment/timing.

Fields:

* id
* project_id
* transcript_id
* token_index
* word_text
* start_ms
* end_ms
* confidence_score nullable
* speaker_label nullable
* created_at

## CaptionTimeline

Represents a versioned, editable canonical timeline.

Fields:

* id
* project_id
* version_number
* source_transcript_id
* source_type (aligned, transcribed, edited)
* status
* created_by_user_id nullable
* created_at

## CaptionSegment

Represents a display-level caption block.

Fields:

* id
* timeline_id
* segment_index
* text
* start_ms
* end_ms
* style_preset_id nullable
* style_metadata_json
* created_at
* updated_at

## CaptionSegmentWord

Optional join-like materialization linking words to a segment.

Fields:

* id
* segment_id
* word_timing_id
* order_index
* emphasis_flag
* style_metadata_json nullable

## StylePreset

Represents a reusable named preset.

Fields:

* id
* owner_scope (system, user, organization)
* owner_user_id nullable
* organization_id nullable
* name
* description
* preset_json
* created_at
* updated_at

## ExportArtifact

Represents a downloadable generated output.

Fields:

* id
* project_id
* timeline_id
* export_type (json, srt, vtt, ass, preview_mp4)
* storage_path
* mime_type
* file_size_bytes nullable
* status
* created_at
* updated_at

## WebhookEndpoint

Represents user-configured delivery endpoints for API events.

Fields:

* id
* user_id
* url
* signing_secret
* is_active
* created_at
* updated_at

## WebhookDelivery

Represents attempted webhook sends.

Fields:

* id
* webhook_endpoint_id
* event_type
* payload_json
* response_status nullable
* response_body nullable
* status
* attempted_at

## UsageLedger

Represents metering and billing events.

Fields:

* id
* user_id
* project_id nullable
* usage_type (audio_minutes, export_job, api_job, storage_bytes)
* quantity
* unit
* metadata_json nullable
* created_at

## AuditLog

Represents key user or system actions.

Fields:

* id
* actor_user_id nullable
* project_id nullable
* action_type
* action_payload_json
* created_at

## 3. Recommended Relationships

* User 1..N Project
* Project 1..N Asset
* Project 1..N ProcessingJob
* Project 1..N Transcript
* Project 1..N CaptionTimeline
* CaptionTimeline 1..N CaptionSegment
* CaptionSegment N..N WordTiming via CaptionSegmentWord
* Project 1..N ExportArtifact
* User 1..N WebhookEndpoint
* User 1..N UsageLedger

## 4. Versioning Guidance

Never overwrite the timeline destructively once users begin editing. Instead:

* create new timeline versions
* keep audit logs
* mark one version as active

This will make future collaboration and rollback much easier.
