# Getting Started

Follow this checklist to install the KiCad Master Library (KML) alongside your KiCad environment.

## Requirements

- **KiCad 9.x stable**. Tested against 9.0 series releases. Earlier majors (8.x and older) are not supported for editing these libraries.
- Git 2.25+ with submodule support.
- Disk space: ~400 MB for the full checkout with submodules.

## Clone the repository with submodules

Choose any working directory. Placing the checkout under `Documents/KiCad/KiCad-Master-Lib` makes it easy to find, but any path works. Placing it within the versioned KiCad installation folder (i.e. placing under `Documents/KiCad/9.0`) may cause issues during upgrades or modifications of your KiCad installation.

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
3. Add `KICAD_MASTER_LIB` pointing to the repository root.
4. Add `KMLIB_LOCAL` pointing to `${KICAD_MASTER_LIB}/kmlib-local`.
5. Save.

Notes:

- Custom environment variables are the recommended way to reference third-party assets and 3D models so paths remain portable across systems.
- Some built-in variables (for KiCad's official libraries) are versioned per major release; custom variables like the two above are user-defined and stable across updates.

## Register symbol libraries

1. `Preferences -> Manage Symbol Libraries...`
2. `Global Libraries` tab.
3. Add each categorized library with `${KMLIB_LOCAL}/symbols/` as the base path:

| Nickname                        | Library File                              |
| ------------------------------- | ----------------------------------------- |
| `KMLib_Aesthetic`               | `KMLib_Aesthetic.kicad_sym`               |
| `KMLib_Connectors`              | `KMLib_Connectors.kicad_sym`              |
| `KMLib_Discrete_Semiconductors` | `KMLib_Discrete_Semiconductors.kicad_sym` |
| `KMLib_Electromechanical`       | `KMLib_Electromechanical.kicad_sym`       |
| `KMLib_IC_Analog`               | `KMLib_IC_Analog.kicad_sym`               |
| `KMLib_IC_Digital`              | `KMLib_IC_Digital.kicad_sym`              |
| `KMLib_IC_MCU_MPU`              | `KMLib_IC_MCU_MPU.kicad_sym`              |
| `KMLib_IC_Power`                | `KMLib_IC_Power.kicad_sym`                |
| `KMLib_Misc`                    | `KMLib_Misc.kicad_sym`                    |
| `KMLib_Passives`                | `KMLib_Passives.kicad_sym`                |
| `KMLib_Power`                   | `KMLib_Power.kicad_sym`                   |
| `KMLib_Sensors`                 | `KMLib_Sensors.kicad_sym`                 |
| `KMLib_Switches`                | `KMLib_Switches.kicad_sym`                |

## Register footprint libraries

1. `Preferences -> Manage Footprint Libraries...`
2. `Global Libraries` tab.
3. Add each categorized library with `${KMLIB_LOCAL}/footprints/` as the base path:

| Nickname               | Folder                        |
| ---------------------- | ----------------------------- |
| `KMLib_Aesthetic`      | `KMLib_Aesthetic.pretty`      |
| `KMLib_Boards_Modules` | `KMLib_Boards_Modules.pretty` |
| `KMLib_Connectors`     | `KMLib_Connectors.pretty`     |
| `KMLib_IC_SMD`         | `KMLib_IC_SMD.pretty`         |
| `KMLib_IC_THT`         | `KMLib_IC_THT.pretty`         |
| `KMLib_Mounting`       | `KMLib_Mounting.pretty`       |
| `KMLib_Passives_SMD`   | `KMLib_Passives_SMD.pretty`   |
| `KMLib_Passives_THT`   | `KMLib_Passives_THT.pretty`   |
| `KMLib_Relays`         | `KMLib_Relays.pretty`         |
| `KMLib_Switches`       | `KMLib_Switches.pretty`       |
| `KMLib_TestPoints`     | `KMLib_TestPoints.pretty`     |

## Optional: register vendor libraries

Add only what you need to keep tables manageable. Typical locations:

- Arduino: `arduino-kicad-library/symbols/arduino-library.kicad_sym` and `arduino-kicad-library/footprints/arduino-library.pretty`
- Digi-Key: `digikey-kicad-library/digikey-symbols` and `digikey-kicad-library/digikey-footprints.pretty`
- SparkFun: `SparkFun-KiCad-Libraries/Symbols` and `SparkFun-KiCad-Libraries/Footprints`
- Seeed OPL: subfolders under `OPL_Kicad_Library/` (for example `Seeed Studio XIAO Series Library`)

Refer to each vendor's README for any special steps.

## Verify the installation

1. Open the **Symbol Editor**, select any KMLib\_\* library, and browse symbols.
2. Open the **Footprint Editor**, select any KMLib\_\* library, and browse footprints.
3. Place a footprint on a scratch PCB and open the **3D Viewer** to confirm `${KMLIB_LOCAL}/3dmodels` resolves and models appear correctly.

## Keeping your checkout current

Update the main repo and submodules periodically:

```sh
git pull origin main
git submodule update --init --recursive
```

When you need a newer upstream vendor release, run `git submodule update --remote <path>` for the relevant submodule and commit the change. Pinning submodule SHAs keeps the workspace reproducible. (This is standard Git behavior for submodules.)
