# CaptionLayer — Documentation Pack

CaptionLayer is the **intelligence layer for captions**.

Core principle:

- Canonical truth = structured caption timeline JSON
- Everything else is derived (SRT, VTT, ASS, video)



This folder contains the requested Markdown documents:

1. `01-saas-blueprint.md`
2. `02-comprehensive-project-description.md`
3. `03-user-stories.md`
4. `04-mvp-and-post-mvp-steps.md`
5. `05-database-entities.md`
6. `06-api-endpoints.md`
7. `07-processing-pipeline.md`
8. `08-mvp-feature-set.md`

These documents are internally aligned around one core architecture decision:

* the canonical truth is a **structured caption timeline JSON**
* all exports are derived from that timeline
* the platform supports both **UI users** and **API consumers**
