# Adding New Components

This guide documents the workflow for adding or modifying parts in `KML-Custom`. Use KiCad **9.x stable**.

## Before you start

- Collect the component datasheet, recommended footprint, and mechanical model.
- Use a unique, descriptive name. Prefer the manufacturer part number (for example `031-5431-1010`).
- Check for similar parts to avoid duplicates.

## 1) Create or update the schematic symbol

1. Open **Symbol Editor** -> `kml-custom`.
2. Create a symbol or duplicate a similar one.
3. Populate properties:
   - `Reference`: family designator (`U`, `J`, etc.).
   - `Value`: match the symbol name.
   - `Footprint`: `kml-custom:<footprint_name>` once the footprint exists.
   - `Datasheet`, `Description`, `Keywords`: copy from the datasheet.
4. Set pin names, electrical types, and units. Follow KiCad's symbol conventions for readability.
5. Run **Tools -> Symbol Checker** and fix issues before saving.

## 2) Create or update the footprint

1. Open **Footprint Editor** -> `kml-custom`.
2. Create the footprint in millimetres. Align the local origin sensibly (pin 1 or part centre).
3. Add `F.SilkS`, `B.SilkS`, `F.CrtYd`, and `F.Fab` graphics following KiCad conventions.
4. In **Footprint Properties -> 3D Models**, reference `${KICAD_KML_CUSTOM_MODELS}/<model-file>`.
5. Verify pad-to-pad spacing against the datasheet.
6. Run **Tools -> Footprint Checker** and resolve errors.

## 3) Place the 3D model

1. Put the STEP/WRL model in `KML-Custom/3dmodels`.
2. Reference it via the `${KICAD_KML_CUSTOM_MODELS}` variable so paths are portable between systems.
3. Orient/scale in the **3D Models** tab.
4. Confirm with **3D Viewer**.

## 4) Link symbol and footprint

- Update the symbol `Footprint` field to `kml-custom:<footprint_name>`.
- If the part supports multiple packages, create aliases or variants with clear suffixes.

## 5) Validate

- Place the new symbol in a scratch schematic. Run ERC.
- Update the footprint on a dummy PCB. Run DRC and open 3D Viewer.
- Check `git status` for unintended edits.

## 6) Commit and share

Stage the typical set:

```sh
git add KML-Custom/kml-custom.kicad_sym
git add KML-Custom/kml-custom.pretty/<new-footprint>.kicad_mod
git add KML-Custom/3dmodels/<model-file>
```

Commit with a clear message referencing the part number. If you updated a vendor submodule, commit that change separately so upstream updates stay traceable.
