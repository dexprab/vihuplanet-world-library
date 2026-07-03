# VihuPlanet Asset Pipeline

Place source assets in raw/. GitHub Actions will normalize them into production/.

## World Library publishing workflow

`production/` is the single source of truth for VihuPlanet artwork. It
publishes automatically into the VihuStudio repository, where the Hero
Page consumes it.

```
Artist
  ↓
Generate artwork
  ↓
Resize using GIMP
  ↓
Commit into production/
  ↓
Push to main
  ↓
GitHub Action
  ↓
Synchronize assets
  ↓
Generate manifests
  ↓
Update VihuStudio
  ↓
Hero automatically renders new artwork.
```

No manual registration. No code changes. Adding a PNG to `production/`
and pushing to `main` is the entire publishing step — the Hero Page
discovers it by reading each collection's `manifest.json` rather than
listing directories, since directory listings return 404 on GitHub
Pages and most static hosts.

The sync is handled by `.github/workflows/sync-world-library.yml`. See
[docs/WORLD_LIBRARY_SYNC.md](docs/WORLD_LIBRARY_SYNC.md) for required
secrets, one-time setup, manual triggering, manifest generation, and
failure recovery.
