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
GitHub Action runs
  ↓
Assets automatically synchronize into
dexprab/vihustudio/vihuplanet/world-library/
  ↓
Hero Page automatically uses the latest production assets.
```

The sync is handled by `.github/workflows/sync-world-library.yml`. See
[docs/WORLD_LIBRARY_SYNC.md](docs/WORLD_LIBRARY_SYNC.md) for required
secrets, one-time setup, manual triggering, and failure recovery.
