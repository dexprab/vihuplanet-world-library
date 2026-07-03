# VihuPlanet Asset Pipeline

Place source assets in raw/. GitHub Actions will normalize them into
production/, generate a manifest.json for every collection, and
synchronize both into `dexprab/vihustudio/vihuplanet/world-library/`.

See [`docs/PIPELINE.md`](docs/PIPELINE.md) for the full artist
workflow and the manifest format.

## Required secret

The sync step needs a repo secret named `VIHUSTUDIO_SYNC_TOKEN` — a
GitHub personal access token with push access to `dexprab/vihustudio`.
Without it, normalization and manifest generation still run and commit
to this repo, but the sync step fails (visibly, in the Actions log)
instead of silently skipping.
