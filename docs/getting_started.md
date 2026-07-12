# Getting Started

Install the KiCad Master Library (KMLib) and point KiCad at it.

## Requirements

- **KiCad 10.x stable.** These libraries are authored and tested against KiCad 10.0.
- Git 2.25+.
- Disk space: ~335 MB for a full checkout (~260 MB of that is 3D models — see
  [Cloning without 3D models](#cloning-without-3d-models) if you don't need them).

## Clone

```sh
git clone https://github.com/feastorg/KiCad-Master-Lib.git
```

**No `--recurse-submodules`.** Upstream vendor libraries used to be git submodules; they
are now vendored as plain files under `vendor/`. See
[Vendored upstream libraries](#vendored-upstream-libraries).

## Configure KiCad

### 1. Path variables

`Preferences → Configure Paths`:

| Variable | Value |
| --- | --- |
| `KICAD_MASTER_LIB` | the repository root |
| `KMLIB_LOCAL` | `${KICAD_MASTER_LIB}/kmlib-local` |

> **Use a forward slash.** An earlier version of this page said
> `${KICAD_MASTER_LIB}\kmlib-local`, with a **backslash**. On Linux and macOS that does
> not resolve — and because KiCad reports nothing, the only symptom is that 3D models
> silently fail to appear. 55 KMLib footprints reference `${KMLIB_LOCAL}` for their
> models. Windows accepts a forward slash too, so always use `/`.

### 2. Library tables

The repository **commits its library tables**. Do not register 36 libraries by hand.

| File | Registers |
| --- | --- |
| `kmlib.fp-lib-table` | 51 footprint libraries |
| `kmlib.sym-lib-table` | 46 symbol libraries |
| `kmlib.design-block-lib-table` | 10 design-block libraries |

They cover **both** `kmlib-local` and the vendored upstream libraries, and every URI is
written relative to `${KICAD_MASTER_LIB}` — so a clean clone resolves everything, on any
machine, with no per-developer configuration.

Merge them into your KiCad configuration (`~/.config/kicad/10.0/`, or
`~/.var/app/org.kicad.KiCad/config/kicad/10.0/` for the flatpak):

- `fp-lib-table` ← `kmlib.fp-lib-table`
- `sym-lib-table` ← `kmlib.sym-lib-table`
- `design-block-lib-table` ← `kmlib.design-block-lib-table`

Keep any existing entries for the stock KiCad libraries; the KMLib tables only add to them.

**This matters more than convenience.** Library resolution that lives only in one
developer's KiCad configuration cannot be reproduced from a clean checkout — so a board
cannot be rebuilt, and CI cannot verify it. The committed tables are the source of truth.

After adding or removing a library, regenerate them:

```sh
python3 scripts/gen_lib_tables.py
```

## Verify

1. **Symbol Editor** — select any `KMLib_*` library and browse.
2. **Footprint Editor** — likewise.
3. **Schematic Editor** — `Place → Add Design Block`, and browse the `KMLib_*` blocks.
4. **3D Viewer** — place a KMLib footprint on a scratch board and confirm the model
   appears. If it doesn't, `KMLIB_LOCAL` is wrong (see the forward-slash note above).

## Vendored upstream libraries

Upstream libraries live under `vendor/` as plain files, so they can be patched locally,
cloned without `--recursive`, and used offline.

[`vendor.yaml`](../vendor.yaml) is the manifest: upstream URL, tracked ref, **pinned
commit**, and licence for each. The pin moves forward deliberately, by a human, after
review — never automatically.

| Library | Licence |
| --- | --- |
| SparkFun-KiCad-Libraries | CC-BY-4.0 |
| OPL_Kicad_Library (Seeed) | CC-BY-SA-4.0 |
| digikey-kicad-library | CC-BY-SA-4.0, with an exception — see its `LICENSE.md` |
| arduino-kicad-library | CC-BY-SA-4.0 |

They are already registered in the committed tables — nothing extra to configure.

### Keeping current

```sh
git pull origin main
```

That's it. No `git submodule update`.

Upstream tracking is a separate, deliberate act. A daily
[`upstream-drift`](../.github/workflows/upstream-drift.yml) workflow asks each upstream
whether it has moved past our pin and opens **one tracking issue per drifted library**.
Nothing syncs automatically.

Check drift yourself:

```sh
python3 scripts/check_drift.py
```

Integrate a drifted library:

```sh
python3 scripts/vendor_sync.py <name> --check   # preview the upstream commits
python3 scripts/vendor_sync.py <name>           # three-way merge, then review and commit
```

**Local modifications survive.** `vendor_sync.py` replays your copy onto the commit we
last vendored, then lets git three-way merge the new upstream on top. Conflicts are
reported and the pin is left unadvanced until you resolve them. Prefer upstreaming a fix
over carrying it here.

> **Before syncing, know what depends on it.** A vendor sync can change a footprint under
> a board that has already been fabricated. Check that the parts your boards actually
> *use* have not changed **pad geometry** — not merely that they still resolve.

## Cloning without 3D models

A full checkout is ~335 MB, ~260 MB of which is 3D models. ERC, DRC, netlist generation
and schematic generation never open one — only 3D renders and STEP export do.

Excluding them gives a **~73 MB** checkout with every library still present:

```sh
git clone --filter=blob:none --sparse https://github.com/feastorg/KiCad-Master-Lib.git
cd KiCad-Master-Lib
git sparse-checkout set --no-cone '/*' \
    '!*.step' '!*.STEP' '!*.stp' '!*.STP' '!*.wrl' '!*.WRL'
```

Exclude by **extension, not directory** — some upstreams keep 3D models loose in product
folders rather than under `*.3dshapes/`.

This is what CI uses.
