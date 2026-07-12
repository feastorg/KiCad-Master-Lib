# KiCad Master Library

KiCad Master Library (KMLib) collects FEAST-specific KiCad assets alongside curated upstream
vendor libraries, so every FEAST design resolves its parts from one place.

## Repository layout

```
kmlib-local/     FEAST symbols, footprints, 3D models and design blocks (KMLib_* libraries)
vendor/          upstream libraries, pinned in vendor.yaml
scripts/         library-table generation, vendoring, drift detection
```

## Library tables

| File | Registers |
| --- | --- |
| `kmlib.fp-lib-table` | 51 footprint libraries |
| `kmlib.sym-lib-table` | 46 symbol libraries |
| `kmlib.design-block-lib-table` | 10 design-block libraries |

Every URI is relative to `${KICAD_MASTER_LIB}` and covers both `kmlib-local` and the
vendored upstreams, so a clean clone resolves everything with no per-machine setup.

Regenerate with `python3 scripts/gen_lib_tables.py`.

## Supported KiCad version

KiCad 10.x stable.

## Upstream libraries

Vendored under `vendor/` and pinned in [`vendor.yaml`](../vendor.yaml). A daily
[`upstream-drift`](../.github/workflows/upstream-drift.yml) workflow opens a tracking issue
when an upstream moves past its pin; a human reviews it and advances the pin with
`scripts/vendor_sync.py`.

Nothing syncs automatically. A footprint that changes under an already-fabricated board is
a manufacturing problem, so the pin is deliberate.

## Next steps

- [Getting Started](getting_started) — install and configure.
- [Adding New Components](adding_components) — contribute parts to `kmlib-local`.
