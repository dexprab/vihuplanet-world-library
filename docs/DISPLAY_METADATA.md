# Display Metadata (Phase 1 — Sprint MEP-08)

## Why this exists

Hero MEP investigation into the Story Meadow found the production
artwork itself is fine — the problem is that a square (2048×2048)
painting gets displayed inside a box shaped nothing like a square
(VihuPlanet's meadow strip is `100vw × 7vh`, roughly a 25:1 letterbox
at typical desktop sizes). `object-fit: cover` can only crop, never
tell the difference between "the boring middle of the canvas" and
"the part of the painting that actually reads as a place." The fix
belongs with the art, not with a one-off Hero hack: let a production
asset optionally say which part of itself matters most, and let any
consumer (Hero or otherwise) read that instead of guessing via a
hardcoded 50%/50% crop.

This is Phase 1: the schema and the tooling that produces it. No
renderer consumes it yet — see "Phase 2" at the bottom.

## Schema

A collection directory may contain an optional `display.json` file
alongside its PNGs, keyed by filename **stem** (the filename without
its extension):

```json
{
  "story-meadow-gentle-hills": { "anchor": "bottom", "focusY": 0.65 }
}
```

`tools/generate_manifests.py` merges this into that collection's
`manifest.json` automatically. A PNG with a matching entry in
`display.json` is emitted as an object instead of a plain filename
string:

```json
{
  "id": "story-meadow-gentle-hills",
  "file": "story-meadow-gentle-hills.png",
  "display": { "anchor": "bottom", "focusY": 0.65 }
}
```

Every other PNG in that same manifest — including every PNG in every
*other* collection — is completely unaffected and stays a plain
string, exactly as it always has been.

### Fields

| Field | Type | Range | Meaning |
|---|---|---|---|
| `id` | string | — | The filename stem (`story-meadow-gentle-hills`, not `story-meadow-gentle-hills.png`). Lets a consumer refer to the asset independent of file extension. Always equals `Path(file).stem`. |
| `file` | string | — | The actual filename in this directory, exactly as it appears in the flat/legacy manifest form. |
| `display.anchor` | string | one of `"top"`, `"center"`, `"bottom"` | A coarse, human-readable description of which part of the image matters — a plain-English fallback for a consumer that isn't ready to do anything with `focusY`. Mirrors the vocabulary of a CSS `object-position` keyword because that's the most likely first consumer, but the field itself carries no CSS or Hero-specific meaning. |
| `display.focusY` | number | `0.0`–`1.0` | The normalized vertical position (as a fraction of the full image height, `0` = top edge, `1` = bottom edge) that should stay visible/centered when this image is cropped into a box shorter than it is. Normalized so it means the same thing regardless of the image's actual pixel resolution. When present, prefer this over `anchor` — it's the precise value `anchor` is a coarse description of. |

Both `anchor` and `focusY` are optional independently — a `display`
block may carry either, both, or (in a future collection) neither if
some other display field is added later. Today, every field describes
**vertical** framing only, because that's the specific, evidenced
problem (the meadow's crop box loses height, not width). No horizontal
(`focusX`), scale, or zoom field exists yet — don't add one
speculatively; the World Library has no image whose crop problem is
horizontal today.

### Backward compatibility

- No `display.json` in a directory → that directory's `manifest.json`
  is a flat array of filename strings, byte-identical to what
  `generate_manifests.py` produced before this feature existed.
- A PNG with no matching key in `display.json` → that PNG's manifest
  entry is a plain string, same as if `display.json` didn't exist.
- Existing consumers that only understand plain filename strings (this
  includes VihuStudio's Hero today — see Phase 2 below) will break on
  an object entry unless updated first. That's exactly why VihuPlanet
  hasn't been touched in this phase: shipping `display.json` for a
  collection is what flips its manifest entries to objects, so a
  collection should only get one once its consumer knows how to read
  it.

## Who authors `display.json`

Hand-authored today, directly in `production/<collection>/`, by
whoever curates that collection's framing — not generated from `raw/`
and not touched by `tools/normalize_assets.py`. This keeps Phase 1
scoped to proving the schema and the generator support for it, without
also building an authoring workflow. `tools/generate_manifests.py`
already runs against `production/` (locally) or the synced destination
(in CI, via `sync-world-library.yml`), so as long as `display.json`
sits next to the PNGs it describes, it's picked up automatically the
same way `manifest.json` itself is — no other pipeline step needed.

## What Phase 1 deliberately does not do

- Does not resize, regenerate, or otherwise touch any PNG.
- Does not change `tools/normalize_assets.py` or anything under `raw/`.
- Does not change `.github/workflows/asset-normalizer.yml` or
  `.github/workflows/sync-world-library.yml` — the mirror/transfer
  step is untouched; it already rsyncs whatever sits in `production/`,
  `display.json` included, and already re-runs
  `generate_manifests.py` against the synced destination.
- Does not add any Hero-specific or VihuPlanet-specific logic anywhere
  in this repository.
- Does not add speculative fields "for later." `anchor` and `focusY`
  are the only two fields, because they're the only two the actual
  investigated problem calls for.

## Phase 2 recommendation (not implemented)

The smallest renderer change that would let VihuPlanet actually use
this, once someone decides to do it:

In `shared/worldLibrary.js`, manifest entries are currently assumed to
always be strings (`_parseManifest` does `typeof name !== 'string'` and
skips anything else). The smallest generic change is:

1. Let `_parseManifest` accept either a string or a `{id, file,
   display}` object per entry — extracting `file` for the URL exactly
   as it does today for a plain string, and, when present, carrying
   the `display` block alongside the resolved URL instead of
   discarding it (today `resolve()`/`resolveAt()` only ever return a
   URL string — this would need to return `{url, display}` instead, or
   a second lookup function, so existing callers that only want a URL
   keep working unchanged).
2. In `css/scene.css`, the one existing rule that hardcodes
   `object-position: 50% 50%` (the story-meadow `<img>` rule) would
   read `display.focusY` (falling back to `anchor` → `top`/`center`/
   `bottom`, falling back to today's `50% 50%` if neither is present)
   and set `object-position: 50% {focusY * 100}%` — either inline via
   JS when the image mounts, or via a CSS custom property the way
   other Hero effects already parameterize per-instance values
   (`--vp-motion-duration` etc.).
3. This is generic (any future collection can carry `display.json`
   and any future consumer of `WorldLibrary.resolve()` gets the same
   `{url, display}` shape), Hero-specific only in the one CSS rule
   that chooses to *act* on `focusY`, and requires no change to how
   Story Worlds, the telescope, or any other object resolves its
   artwork.

This is a recommendation, not a plan to execute — Phase 2 work starts
only once this is reviewed.
