# CaptionLayer — Deployment Strategy

## Overview

CaptionLayer uses a cloud-native, cost-optimised deployment architecture built on **Supabase** (managed backend services) and **Google Cloud Platform** (compute and storage), with **Pulumi** (TypeScript) as the Infrastructure as Code tool.

This strategy is designed to:
- Cost **$0 during development**
- Cost **~$25/mo at early production** (10–50 users)
- Scale incrementally as user volume grows
- Keep infrastructure reproducible and version-controlled via Pulumi

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CaptionLayer                               │
│                                                                     │
│   ┌─────────────┐                                                   │
│   │   Vercel    │  Next.js frontend (TypeScript)                    │
│   │  (Frontend) │  Hobby tier — free indefinitely                   │
│   └──────┬──────┘                                                   │
│          │ HTTPS                                                     │
│   ┌──────▼──────────────────────┐                                   │
│   │  GCP Cloud Run              │  FastAPI (Python)                 │
│   │  (API Service)              │  Validates Supabase JWT           │
│   │  Scales to zero when idle   │  Dispatches jobs to queue         │
│   └──────┬──────────────────────┘                                   │
│          │                                                           │
│   ┌──────▼──────────────────────┐                                   │
│   │  GCP Cloud Tasks            │  HTTP-based job queue             │
│   │  (Queue)                    │  1M tasks/mo free tier            │
│   └──────┬──────────────────────┘                                   │
│          │ triggers per job                                          │
│   ┌──────▼──────────────────────┐                                   │
│   │  GCP Cloud Run Jobs         │  Python worker containers         │
│   │  (Processing Workers)       │  Spin up per job, exit when done  │
│   │                             │  Scale to zero — pay per second   │
│   │  ├── Transcription Worker   │  Whisper (open-source ASR)        │
│   │  ├── Alignment Worker       │  WhisperX / forced alignment      │
│   │  ├── Segmentation Worker    │  Rules + Gemini Flash LLM         │
│   │  ├── Export Worker          │  SRT / VTT / ASS / JSON           │
│   │  └── Preview Render Worker  │  ffmpeg lightweight render        │
│   └──────┬──────────────────────┘                                   │
│          │                                                           │
│   ┌──────▼────────────────────────────────────────────────────┐     │
│   │                      Supabase (Pro)                        │     │
│   │                                                            │     │
│   │  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐  │     │
│   │  │ PostgreSQL  │  │    Auth     │  │     Storage      │  │     │
│   │  │  (17 tables)│  │  (JWT/RLS)  │  │ (exports, audio) │  │     │
│   │  └─────────────┘  └─────────────┘  └──────────────────┘  │     │
│   │  ┌─────────────┐                                          │     │
│   │  │  Realtime   │  Job status updates (WebSocket)          │     │
│   │  │             │  Frontend subscribes to ProcessingJob    │     │
│   │  └─────────────┘                                          │     │
│   └────────────────────────────────────────────────────────────┘     │
│                                                                     │
│   ┌──────────────────────┐   ┌──────────────────────┐              │
│   │  GCS Bucket          │   │  Gemini Flash API    │              │
│   │  (Large audio files  │   │  (LLM: segmentation  │              │
│   │   > 50MB)            │   │   + style tagging)   │              │
│   └──────────────────────┘   └──────────────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Services

### Frontend — Vercel

| Property | Value |
|----------|-------|
| Service | Vercel |
| Framework | Next.js (TypeScript) |
| Tier | Hobby (free) |
| CI/CD | Auto-deploy on `git push` to `main` |

Vercel is the optimal host for Next.js: zero-config deployments, automatic preview URLs per pull request, edge CDN, and free indefinitely on the Hobby tier. The frontend has no backend logic — all API calls go to Cloud Run.

---

### API — GCP Cloud Run (FastAPI)

| Property | Value |
|----------|-------|
| Service | GCP Cloud Run |
| Runtime | Python, FastAPI container |
| Scaling | 0 → N instances (scales to zero when idle) |
| Authentication | Validates Supabase-issued JWTs on every request |
| Free tier | 2M requests/mo + 180K vCPU-seconds/mo |

The FastAPI service handles all business logic: project management, asset registration, job submission, timeline retrieval, export management, webhooks, and billing. It writes to Supabase PostgreSQL and dispatches processing jobs to Cloud Tasks.

Workers are **not** triggered directly from Cloud Run — they go through Cloud Tasks to ensure reliable delivery, retries, and decoupling.

---

### Job Queue — GCP Cloud Tasks

| Property | Value |
|----------|-------|
| Service | GCP Cloud Tasks |
| Queue model | HTTP-based (targets Cloud Run Jobs HTTP endpoint) |
| Free tier | 1M tasks/mo |
| Retry policy | Configurable per queue (max attempts, backoff) |

One Cloud Tasks queue per pipeline stage:
- `queue-transcription`
- `queue-alignment`
- `queue-segmentation`
- `queue-export`
- `queue-preview-render`

Each task carries a JSON payload referencing the `ProcessingJob` ID. Workers pull job context from the database on startup.

---

### Processing Workers — GCP Cloud Run Jobs (Python)

| Property | Value |
|----------|-------|
| Service | GCP Cloud Run Jobs |
| Runtime | Python containers (one image per worker type) |
| Scaling | Zero when idle — container starts per job trigger |
| Resources | 1 vCPU / 2GB RAM per job (Whisper Small) |
| Free tier | ~25 hours execution/mo included in Cloud Run free tier |

| Worker | Function | Key dependency |
|--------|----------|---------------|
| Transcription | Audio → word timings (ASR) | Whisper (open-source, bundled in container) |
| Alignment | Audio + text → word timings | WhisperX or Montreal Forced Aligner |
| Segmentation | Word timings → caption segments | Deterministic rules + Gemini Flash |
| Export | Timeline → SRT / VTT / ASS / JSON | Pure Python, no external API |
| Preview Render | Timeline → lightweight MP4 preview | ffmpeg (bundled in container) |

Workers update `ProcessingJob.status` in Supabase PostgreSQL on start, completion, and failure. Supabase Realtime propagates these updates to the frontend immediately.

**ASR note:** Whisper Small is bundled inside the worker container — no per-minute ASR API fees. For the MVP, Whisper Small handles clean short-to-medium audio well. Upgrade to Whisper Medium post-MVP if accuracy needs improving.

---

### Database, Auth, Storage, Realtime — Supabase

| Property | Value |
|----------|-------|
| Service | Supabase Pro |
| Cost | $25/mo |
| Database | Managed PostgreSQL (8GB included) |
| Auth | JWT-based, Row-Level Security (RLS) on all tables |
| Storage | 100GB file storage (audio uploads, generated exports) |
| Realtime | WebSocket subscriptions for job status updates |

Supabase replaces four separate services (PostgreSQL host, auth provider, file storage, realtime layer) at a single flat rate. This is the primary reason it was chosen — it significantly reduces infrastructure complexity at the MVP stage.

**Auth flow:**
1. User signs up / logs in via Supabase Auth
2. Supabase issues a JWT
3. Frontend includes JWT in `Authorization: Bearer` header on all API calls
4. Cloud Run (FastAPI) validates the JWT using Supabase's JWKS endpoint
5. `auth.uid()` is used in PostgreSQL RLS policies to enforce row-level data isolation

**Realtime flow:**
1. Frontend subscribes to `ProcessingJob` table filtered by `project_id`
2. When a worker updates `ProcessingJob.status`, Supabase broadcasts the change
3. UI updates instantly — no polling

**Storage split:**
- **Supabase Storage:** Exports (SRT, VTT, ASS, JSON, preview MP4), audio files under ~50MB
- **GCS Bucket:** Large audio files (> 50MB) — cheaper at scale, Supabase Storage is not optimised for large media

---

### Object Storage — GCP Cloud Storage (GCS)

| Property | Value |
|----------|-------|
| Service | GCP Cloud Storage |
| Use case | Large audio files (> 50MB) |
| Free tier | 5GB regional storage + 1GB egress/mo |
| Cost beyond free | $0.02/GB/mo storage, $0.12/GB egress |

Workers write generated exports to Supabase Storage (accessed via signed URLs). Raw large audio files are stored in GCS and referenced by path in the `Asset` database table. FastAPI generates signed GCS URLs for direct browser uploads — audio never transits through the API server.

---

### LLM — Gemini Flash

| Property | Value |
|----------|-------|
| Service | Google Gemini 1.5 Flash |
| Dev API | Google AI Studio (free — 1,500 req/day) |
| Prod API | Vertex AI (pay-per-token) |
| Input cost | $0.075 / 1M tokens |
| Output cost | $0.30 / 1M tokens |

Used in two pipeline stages:
1. **Segmentation Worker** — refines deterministic caption splits (semantic grouping, awkward break avoidance, emphasis detection)
2. **Export Worker (style tagging)** — interprets free-text style instructions, maps to style preset fields

Caption segmentation operates on short text (< 2,000 tokens per job). At 100 jobs/day, Gemini Flash costs < $1/mo.

**Dev vs prod API key:** Google AI Studio keys are free with rate limits — sufficient for development and early production. Switch to Vertex AI for production when daily volume exceeds 1,500 requests.

---

### IaC — Pulumi (TypeScript)

| Property | Value |
|----------|-------|
| Tool | Pulumi |
| Language | TypeScript |
| Provider | `@pulumi/gcp` |
| State backend | Pulumi Cloud (free for solo dev) |
| Environments | `dev`, `staging`, `prod` (separate stacks) |

```
infra/
  Pulumi.yaml
  Pulumi.dev.yaml
  Pulumi.staging.yaml
  Pulumi.prod.yaml
  index.ts
  components/
    artifact-registry.ts   # Container image repos (one per worker + API)
    cloud-run.ts           # FastAPI Cloud Run service
    cloud-run-jobs.ts      # Worker job definitions
    cloud-tasks.ts         # Task queues (one per pipeline stage)
    gcs.ts                 # Audio + export buckets
    iam.ts                 # Service accounts, Workload Identity
    secrets.ts             # Secret Manager (Supabase keys, Gemini key)
```

Supabase is a managed SaaS — database schema, RLS policies, storage buckets, and auth config are managed via Supabase CLI migrations (not Pulumi). The Pulumi stack manages GCP resources only.

---

## Environments

### Local Development

```
supabase start          # Runs full Postgres + Auth + Storage + Realtime in Docker
fastapi dev             # API on localhost:8000
python -m workers.X    # Individual workers run directly
next dev                # Frontend on localhost:3000
```

No cloud account required. Supabase CLI provides a complete local environment. Workers run directly with Python — no Cloud Run Jobs needed locally.

**Cost: $0**

---

### Staging

| Component | Staging setup |
|-----------|--------------|
| Frontend | Vercel preview deployment (auto per PR) |
| API | Cloud Run service (`staging` tag) |
| Workers | Cloud Run Jobs (`staging` suffix) |
| Database | Supabase free-tier project (`captionlayer-staging`) |
| Storage | Separate GCS bucket (`captionlayer-staging-audio`) |

Supabase free projects are acceptable for staging since inactivity pausing is not a concern (CI/CD keeps it active). Pulumi `staging` stack targets staging-specific resource names.

**Cost: $0 (within free tiers)**

---

### Production

| Component | Production setup |
|-----------|-----------------|
| Frontend | Vercel Hobby (custom domain) |
| API | Cloud Run service (min 0, max 10 instances) |
| Workers | Cloud Run Jobs (triggered by Cloud Tasks) |
| Database | Supabase Pro (`captionlayer-prod`) — $25/mo |
| Storage | GCS bucket (`captionlayer-prod-audio`) |
| Secrets | GCP Secret Manager |

**Cost: ~$25/mo at launch, scaling with usage**

---

## Cost Progression

| Phase | Users | Jobs/day | Monthly Cost | Primary driver |
|-------|-------|----------|--------------|---------------|
| Local dev | 1 | — | **$0** | — |
| Staging | 1–5 | < 20 | **$0** | Within free tiers |
| Early production | 10–50 | < 50 | **~$25** | Supabase Pro |
| Growing | 100–300 | ~200 | **~$45–65** | + GCP worker compute |
| Scaling | 500+ | ~1,000 | **~$80–120** | + Gemini API, GCS egress |

**GCP worker cost calculation:**
- Whisper Small on 1 vCPU / 2GB processes 10-min audio in ~3 min wall time
- Cost per job ≈ $0.005
- 200 jobs/day × $0.005 × 30 days ≈ **$30/mo**

**Largest cost levers:**
1. Worker execution time — directly tied to audio volume processed
2. Supabase plan — fixed $25/mo baseline
3. Gemini API — negligible at typical caption job sizes

---

## CI/CD Flow

```
git push origin main
        │
        ├──► Vercel           (auto-deploy frontend)
        │
        └──► GitHub Actions
                │
                ├── Build Docker images (API + workers)
                ├── Push to Artifact Registry
                └── pulumi up --stack prod
                        │
                        ├── Update Cloud Run service (new image tag)
                        └── Update Cloud Run Job definitions
```

Container images are tagged with the Git commit SHA. Pulumi updates only changed resources. Rollback is a `pulumi stack export` + re-deploy of the previous tag.

---

## Key Decisions & Rationale

| Decision | Chosen | Alternatives considered | Reason |
|----------|--------|------------------------|--------|
| IaC tool | Pulumi (TypeScript) | Terraform | Real programming language, better for conditional logic and loops; TypeScript consistent with frontend |
| Managed backend | Supabase | Firebase, bare Cloud SQL | Replaces 4 services (DB + Auth + Storage + Realtime) at $25/mo; Auth tightly coupled to PostgreSQL RLS |
| Compute model | Cloud Run + Cloud Run Jobs | GKE, App Engine, Lambda | Scale-to-zero, pay-per-execution, no cluster management |
| Queue | Cloud Tasks | Pub/Sub, Redis, SQS | HTTP-based, 1M/mo free, simple retry config, no broker to manage |
| ASR | Whisper (open-source, in-container) | Google Speech-to-Text, Deepgram | No per-minute API fees; bundled in worker image |
| LLM | Gemini Flash | GPT-4o, Claude | Native GCP integration; cheapest capable model; 1,500 req/day free on AI Studio |
| Object storage split | Supabase Storage + GCS | GCS only | Supabase Storage for exports (tightly coupled to DB rows); GCS for large raw audio |
| Frontend host | Vercel | Firebase Hosting, Cloud Run | Best Next.js DX; free; preview deployments per PR |
| No Redis | — | Memorystore, Upstash | Cloud Tasks replaces queue need; Supabase Realtime replaces pub/sub for job status |

---

## Open Decisions (to finalise before scaffolding)

- [ ] GCP region (`us-central1` cheapest, or region closest to target users)
- [ ] Supabase region (should match GCP region geography)
- [ ] Whisper model size for MVP: `small` (fast, cheaper) or `medium` (more accurate)
- [ ] Single GCP project vs. separate `staging` / `prod` projects
- [ ] Custom domain strategy (apex domain on Vercel, API subdomain on Cloud Run)
