# KiCad Master Library

KiCad Master Library (KML) collects FEAST-specific custom KiCad assets alongside curated upstream vendor libraries. Each third-party library is tracked as a Git submodule so the project can pin known-good revisions while keeping updates straightforward.

## Repository layout

- `KML-Custom/`: FEAST maintained symbol, footprint, and 3D model library.
- `arduino-kicad-library/`: upstream Arduino module symbols and footprints.
- `digikey-kicad-library/`: Digi-Key reference symbols and footprints.
- `SparkFun-KiCad-Libraries/`: SparkFun maintained symbols, footprints, and 3D models.
- `OPL_Kicad_Library/`: Seeed Studio Open Parts Library (OPL) content.

Use the guides below for hands-on setup and contribution workflows.

## Supported KiCad versions

Use KiCad **9.x stable** for editing and day-to-day use. These libraries are authored and tested with KiCad 9.0-series builds. Prior major versions are not supported because of format and feature changes across major releases. Refer to the official KiCad 9.0 release notes for detailed compatibility guidance.

## File format notes

KML uses the KiCad 9.x symbol and footprint formats. Avoid depending on the numeric `version` headers inside the library files; KiCad guarantees compatibility within a major series, but a future major release may require migration. Review the 9.0 library format documentation before upgrading the toolchain.

## Keeping the libraries current

```sh
git pull origin main
git submodule update --init --recursive
```

Run those commands from the repository root whenever you need the latest upstream changes. Update individual submodules with the usual `git submodule update --remote <path>` workflow when you want to track newer vendor releases.

## Next steps

- [Getting Started](getting_started) walks through installing the libraries and configuring KiCad.
- [Adding New Components](adding_components) covers the workflow for contributing new parts to `KML-Custom`.
