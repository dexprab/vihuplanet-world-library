# World Library → VihuStudio Sync

`production/` in this repository is the single source of truth for
VihuPlanet artwork. `.github/workflows/sync-world-library.yml` mirrors it
into `dexprab/vihustudio`'s `vihuplanet/world-library/` folder, which the
Hero Page consumes. VihuStudio never edits these assets directly — it is
a read-only consumer of the World Library.

The destination folder always mirrors `production/` exactly: files added
or updated in `production/` are added or updated in
`vihuplanet/world-library/`, and files removed from `production/` are
removed from `vihuplanet/world-library/`. Nothing outside that folder in
VihuStudio is ever touched.

## Required GitHub secret

The workflow authenticates to VihuStudio with a Personal Access Token,
stored as a secret in **this** repository (World Library), following
GitHub's recommended approach for `actions/checkout` against a second
repository.

| Secret | Value |
|---|---|
| `VIHUSTUDIO_SYNC_TOKEN` | A fine-grained PAT scoped only to `dexprab/vihustudio`, with **Contents: Read and write** repository permission. |

Generate it under the token owner's GitHub Settings → Developer settings
→ Fine-grained personal access tokens → Generate new token, restricted
to the `vihustudio` repository. A classic PAT with the `repo` scope also
works if fine-grained tokens aren't available, but prefer the narrower
option.

## One-time repository setup

1. Create `VIHUSTUDIO_SYNC_TOKEN` as described above in **World Library**
   → Settings → Secrets and variables → Actions → New repository secret.
2. Confirm the token's account has push access to `dexprab/vihustudio`.
3. No manual folder creation is needed in VihuStudio — the workflow
   creates `vihuplanet/world-library/` on its first run if it doesn't
   already exist.

## How to manually trigger the workflow

Go to **Actions → World Library Sync → Run workflow** in the World
Library repository, and run it against `main`. This is useful for
re-running a sync without waiting for a new push, or for recovering
after a failed run.

## Failure behaviour

- The job validates that `production/` and
  `vihuplanet/world-library/` are byte-identical immediately after
  mirroring, before committing anything. If that check fails, the job
  fails and **nothing is committed or pushed** to VihuStudio — a failed
  sync never leaves a partial or inconsistent result.
- If `VIHUSTUDIO_SYNC_TOKEN` is missing, expired, or lacks push access,
  the checkout or push step fails and no changes reach VihuStudio.
- Concurrent runs are serialized (`concurrency: world-library-sync`),
  so overlapping pushes queue instead of racing each other.
- Every run ends with a summary (visible in the workflow run's Summary
  tab) listing files added, updated, and removed, or confirming no
  changes were needed.

## How to recover from a failed sync

1. Open the failed run under **Actions → World Library Sync** and read
   the failing step's log to identify the cause (auth failure,
   validation mismatch, push rejected, etc.).
2. Fix the underlying issue — most commonly a stale or missing
   `VIHUSTUDIO_SYNC_TOKEN`, or a manual edit made directly to
   `vihuplanet/world-library/` in VihuStudio that now conflicts with
   the mirror.
3. Re-run the workflow manually (see above). Because the sync always
   mirrors the current state of `production/`, re-running is safe and
   idempotent — it does not matter how many times it runs or how far
   behind VihuStudio has fallen.
