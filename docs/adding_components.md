# Adding New Components

This guide documents the workflow for adding or modifying parts in `KML-Custom`. Use KiCad **9.x stable**.

## Before you start

- Collect the component datasheet, recommended footprint, and mechanical model.
- Use a unique, descriptive name. Prefer the manufacturer part number (for example `031-5431-1010`).
- Check for similar parts to avoid duplicates.

## kmlib-local organization

This is the folder for our local files for kicad master library kml-custom. The "KMLib" prefixed is used for symbols and footprints to avoid name conflicts with other libraries when added to the KiCad library manager.

### Symbols

`.kicad_sym` files are prefixed with "KMLib\_" and organized into the following categories:

| Category                    | Includes                                               |
| --------------------------- | ------------------------------------------------------ |
| **Aesthetic**               | Logos, labels, decorative elements                     |
| **Power**                   | GND, +5V, VREF, net-ties, ferrite beads (logical role) |
| **Passives**                | R, C, L, resistor networks                             |
| **Discrete_Semiconductors** | Diodes, BJTs, MOSFETs, TVS                             |
| **IC_Analog**               | Op-amps, ADCs, DACs, comparators                       |
| **IC_Digital**              | Logic gates, flip-flops, buffers                       |
| **IC_MCU_MPU**              | MCUs, MPUs, SoCs                                       |
| **IC_Power**                | Regulators, PMICs, motor drivers                       |
| **Sensors**                 | Temp, pressure, IMU, light                             |
| **Connectors**              | Headers, JST, USB, terminals                           |
| **Switches**                | Tactile, rotary, DIP                                   |
| **Electromechanical**       | Relays, motors, buzzers                                |
| **Misc**                    | Crystals, jumpers, test points                         |

### Footprints & 3D Models

`.pretty` files are prefixed with "KMLib\_" while `3dmodels` folders have no prefix. They are organized into the following categories:

| Category               | Includes                                                            |
| ---------------------- | ------------------------------------------------------------------- |
| **Aesthetic**          | Logos, labels, decorative elements (no 3dmodels)                    |
| **Passives_SMD**       | 0402, 0603, 0805, 1206, 1210, 1812 resistors, capacitors, inductors |
| **Passives_THT**       | Resistors, capacitors, inductors                                    |
| **IC_SMD**             | SOIC, TSSOP, QFN, BGA packages                                      |
| **IC_THT**             | DIP, SIP packages                                                   |
| **Connectors_JST**     | JST XH, PH, SH series connectors                                    |
| **Connectors_Molex**   | Molex KK, Micro-Fit connectors                                      |
| **Connectors_Generic** | USB, HDMI, Ethernet, terminal blocks                                |
| **Switches**           | Tactile, rotary, DIP switches                                       |
| **Relays**             | Signal and power relays                                             |
| **TestPoints**         | Various test point footprints                                       |
| **Mounting**           | Mounting holes, standoffs                                           |

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
