# Getting Started

Follow this checklist to install the KiCad Master Library (KML) alongside your KiCad environment.

## Requirements

- **KiCad 9.x stable**. Tested against 9.0 series releases. Earlier majors (8.x and older) are not supported for editing these libraries.
- Git 2.25+ with submodule support.
- Disk space: ~400 MB for the full checkout with submodules.

## Clone the repository with submodules

Choose any working directory. Placing the checkout under `Documents/KiCad/<major>/footprints` makes it easy to find, but any path works.

```sh
git clone --recurse-submodules https://github.com/FEASTorg/KiCad-Master-Lib.git
```

Already cloned? Bring submodules up to date from the repo root:

```sh
git submodule update --init --recursive
```

## Configure KiCad path variables

1. Launch KiCad.
2. Open `Preferences -> Configure Paths`.
3. Add `KICAD_KML_MASTER` pointing to the repository root.
4. Add `KICAD_KML_CUSTOM_MODELS` pointing to `${KICAD_KML_MASTER}/KML-Custom/3dmodels`.
5. Save.

Notes:

- Custom environment variables are the recommended way to reference third-party assets and 3D models so paths remain portable across systems.
- Some built-in variables (for KiCad's official libraries) are versioned per major release; custom variables like the two above are user-defined and stable across updates.

## Register the custom symbol library

1. `Preferences -> Manage Symbol Libraries...`
2. `Global Libraries` tab.
3. Add a row:
   - **Nickname**: `kml-custom`
   - **Library Path**: `${KICAD_KML_MASTER}/KML-Custom/kml-custom.kicad_sym`
   - **Library Format**: `KiCad`
4. Apply.

## Register the custom footprint library

1. `Preferences -> Manage Footprint Libraries...`
2. `Global Libraries` tab.
3. Add a row:
   - **Nickname**: `kml-custom`
   - **Library Path**: `${KICAD_KML_MASTER}/KML-Custom/kml-custom.pretty`
   - **Library Format**: `KiCad`
4. Save.

Keep the nickname `kml-custom` stable. Existing symbols reference footprints by nickname.

## Optional: register vendor libraries

Add only what you need to keep tables manageable. Typical locations:

- Arduino: `arduino-kicad-library/symbols/arduino-library.kicad_sym` and `arduino-kicad-library/footprints/arduino-library.pretty`
- Digi-Key: `digikey-kicad-library/digikey-symbols` and `digikey-kicad-library/digikey-footprints.pretty`
- SparkFun: `SparkFun-KiCad-Libraries/Symbols` and `SparkFun-KiCad-Libraries/Footprints`
- Seeed OPL: subfolders under `OPL_Kicad_Library/` (for example `Seeed Studio XIAO Series Library`)

Refer to each vendor's README for any special steps.

## Verify the installation

1. Open the **Symbol Editor**, select `kml-custom`, and browse symbols.
2. Open the **Footprint Editor**, select `kml-custom`, and browse footprints.
3. Place a `kml-custom` footprint on a scratch PCB and open the **3D Viewer** to confirm `${KICAD_KML_CUSTOM_MODELS}` resolves. If models do not appear, recheck the path variable. Using environment variables for 3D models is supported and recommended.

## Keeping your checkout current

Update the main repo and submodules periodically:

```sh
git pull origin main
git submodule update --init --recursive
```

When you need a newer upstream vendor release, run `git submodule update --remote <path>` for the relevant submodule and commit the change. Pinning submodule SHAs keeps the workspace reproducible. (This is standard Git behavior for submodules.)
