# KiCad Master Library

KiCad Master Library (KMLib) collects FEAST-specific custom KiCad assets alongside curated
upstream vendor libraries, so every FEAST design resolves its parts from one pinned place.

## Repository layout

```
kmlib-local/     FEAST symbols, footprints, 3D models and design blocks (KMLib_* libraries)
vendor/          upstream libraries, vendored (see vendor.yaml)
scripts/         library-table generation, vendoring, drift detection
```

| File | Registers |
| --- | --- |
| `kmlib.fp-lib-table` | 51 footprint libraries |
| `kmlib.sym-lib-table` | 46 symbol libraries |
| `kmlib.design-block-lib-table` | 10 design-block libraries |

Every URI is written relative to `${KICAD_MASTER_LIB}`, covering both `kmlib-local` and the
vendored upstreams. **A clean clone resolves everything**, on any machine, with no
per-developer KiCad configuration.

That is the point. Library resolution that lives only in someone's global KiCad config
cannot be reproduced from a clean checkout — so a board cannot be rebuilt from source, and
CI cannot verify it.

## Supported KiCad version

**KiCad 10.x stable.** Authored and tested against KiCad 10.0.

Note that the format-version header inside a board or library file is the *only* reliable
signal of what wrote it — and it is easy to over-read. A board saved by KiCad 9 opens fine
in KiCad 10, and a board merely *opened* in KiCad 10 and re-saved is not thereby migrated
in any deeper sense: its library references can still be broken. Check, don't infer.

## Vendored upstream libraries

Upstream libraries are **vendored as plain files**, not git submodules — so they can be
patched locally, cloned without `--recursive`, and used offline.

[`vendor.yaml`](../vendor.yaml) is the manifest: upstream URL, tracked ref, **pinned
commit**, and licence for each.

Clone and update with plain git:

```sh
git clone https://github.com/feastorg/KiCad-Master-Lib.git
git pull origin main
```

### Upstream drift is tracked, never automatic

A daily [`upstream-drift`](../.github/workflows/upstream-drift.yml) workflow asks each
upstream whether it has moved past our pin and opens **one tracking issue per drifted
library**. A human reviews it, runs `scripts/vendor_sync.py`, and moves the pin forward
deliberately.

**Nothing syncs on its own — by design.** For PCB libraries, a footprint silently changing
under a board you have already fabricated is a manufacturing hazard, not a feature. The
library is curated and frozen; the pin is what makes a design reproducible.

## Next steps

- [Getting Started](getting_started) — install the libraries and configure KiCad.
- [Adding New Components](adding_components) — contribute new parts to `kmlib-local`.
