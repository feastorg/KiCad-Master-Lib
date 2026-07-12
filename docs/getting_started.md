# Getting Started

## Requirements

- KiCad 10.x stable
- Git 2.25+
- ~356 MB disk (~73 MB if you exclude 3D models — see below)

## Clone

```sh
git clone https://github.com/feastorg/KiCad-Master-Lib.git
```

## Configure KiCad

### Path variables

`Preferences → Configure Paths`:

| Variable | Value |
| --- | --- |
| `KICAD_MASTER_LIB` | the repository root |
| `KMLIB_LOCAL` | `${KICAD_MASTER_LIB}/kmlib-local` |

Use a forward slash on all platforms. A backslash does not resolve on Linux or macOS, and
KiCad gives no error — 3D models simply do not appear.

### Library tables

The repository commits its library tables:

| File | Registers |
| --- | --- |
| `kmlib.fp-lib-table` | 51 footprint libraries |
| `kmlib.sym-lib-table` | 46 symbol libraries |
| `kmlib.design-block-lib-table` | 10 design-block libraries |

They cover `kmlib-local` and the vendored upstream libraries. Every URI is relative to
`${KICAD_MASTER_LIB}`, so a clean clone resolves everything with no per-machine setup.

Merge them into your KiCad configuration (`~/.config/kicad/10.0/`, or
`~/.var/app/org.kicad.KiCad/config/kicad/10.0/` for the flatpak):

- `fp-lib-table` ← `kmlib.fp-lib-table`
- `sym-lib-table` ← `kmlib.sym-lib-table`
- `design-block-lib-table` ← `kmlib.design-block-lib-table`

Keep your existing entries for the stock KiCad libraries; these only add to them.

Regenerate after adding or removing a library:

```sh
python3 scripts/gen_lib_tables.py
```

## Verify

1. **Symbol Editor** — select a `KMLib_*` library and browse.
2. **Footprint Editor** — likewise.
3. **Schematic Editor** — `Place → Add Design Block`, browse the `KMLib_*` blocks.
4. **3D Viewer** — place a KMLib footprint on a scratch board and confirm the model appears.

## Updating

```sh
git pull origin main
```

## Vendored upstream libraries

Upstream libraries are vendored under `vendor/` and pinned in [`vendor.yaml`](../vendor.yaml).

| Library | Licence |
| --- | --- |
| SparkFun-KiCad-Libraries | CC-BY-4.0 |
| OPL_Kicad_Library (Seeed) | CC-BY-SA-4.0 |
| digikey-kicad-library | CC-BY-SA-4.0, with an exception — see its `LICENSE.md` |
| arduino-kicad-library | CC-BY-SA-4.0 |

They are registered in the committed tables; nothing extra to configure.

A daily [`upstream-drift`](../.github/workflows/upstream-drift.yml) workflow opens a
tracking issue when an upstream moves past its pin. Nothing syncs automatically.

```sh
python3 scripts/check_drift.py                  # report drift
python3 scripts/vendor_sync.py <name> --check   # preview upstream commits
python3 scripts/vendor_sync.py <name>           # three-way merge; local edits preserved
```

Before advancing a pin, check that the parts your boards use have not changed **pad
geometry** — not merely that they still resolve.

## Cloning without 3D models

ERC, DRC and netlist generation never read a 3D model; only renders and STEP export do.
Excluding them gives a ~73 MB checkout with every library present:

```sh
git clone --filter=blob:none --sparse https://github.com/feastorg/KiCad-Master-Lib.git
cd KiCad-Master-Lib
git sparse-checkout set --no-cone '/*' \
    '!*.step' '!*.STEP' '!*.stp' '!*.STP' '!*.wrl' '!*.WRL'
```

Exclude by extension, not directory — some upstreams keep models loose in product folders
rather than under `*.3dshapes/`.
