# Adding New Components

This guide documents the workflow for adding or modifying parts in `kmlib-local`. Use KiCad **10.x stable**.

## Naming rules

- **No spaces** in library, symbol or footprint names. Names appear verbatim in `lib_id`
  strings and on command lines. Use `Thermal_Pad`, not `Thermal Pad`.
- **Prefer the manufacturer part number**, e.g. `AP63205WU-7_Buck_Regulator`.
- **Do not put FEAST parts in a vendor library.** `vendor/` is reserved for upstream
  content, and is overwritten on sync. First-party parts belong in `kmlib-local`.
- **Renaming a symbol also renames its sub-units.** A symbol's sub-units carry the bare
  item name (`ITEM_0_1` inside `LIB:ITEM`); if they disagree, KiCad refuses to open any
  schematic using the symbol. The Symbol Editor handles this; hand-editing does not.

## kmlib-local organization

The `kmlib-local/` folder contains FEAST's custom KiCad libraries. Components are organized into categorized KMLib\_\* libraries to avoid naming conflicts and improve discoverability.

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

`.pretty` directories are prefixed with "KMLib\_" while `.3dshapes` folders have no prefix. They are organized into the following categories:

| Category             | Includes                                                            |
| -------------------- | ------------------------------------------------------------------- |
| **Aesthetic**        | Logos, labels, decorative elements (no 3dmodels)                    |
| **Boards_Modules**   | Discrete boards, modules, shields                                   |
| **Passives_SMD**     | 0402, 0603, 0805, 1206, 1210, 1812 resistors, capacitors, inductors |
| **Passives_THT**     | Resistors, capacitors, inductors                                    |
| **IC_SMD**           | SOIC, TSSOP, QFN, BGA packages                                      |
| **IC_THT**           | DIP, SIP packages                                                   |
| **Connectors**       | Headers, JST, USB, terminals                                        |
| **Switches**         | Tactile, rotary, DIP switches                                       |
| **Relays**           | Signal and power relays                                             |
| **TestPoints**       | Various test point footprints                                       |
| **Mounting**         | Mounting holes, standoffs                                           |
| **Proto**            | Prototyping footprints for hand soldering and testing               |
| **Proto_Decorators** | Prototyping decorator elements such as those for solder tracing     |

### Design Blocks

Design blocks are stored under `kmlib-local/blocks/` and use KiCad's native **Design Block** format for reusable schematic fragments.

At the top level, design blocks are organized into category directories with the suffix `.kicad_blocks`.  
Each category directory is prefixed with `KMLib_` and represents a logical grouping of reusable circuit designs (for example: ADCs, Power, Interfaces, Microcontrollers).

Within each `.kicad_blocks` directory, individual reusable designs are stored as `.kicad_block` subdirectories.  
Each `.kicad_block` directory represents a single design block and contains:

- One `.kicad_sch` schematic file implementing the circuit
- One `.json` metadata file describing the block (name, description, versioning, etc.)

They are categorized as follows:

| Category             | Includes                                      |
| -------------------- | --------------------------------------------- |
| **ADCs**             | Analog-to-digital converter circuits          |
| **Analog**           | General-purpose analog signal conditioning    |
| **Digital**          | Digital logic support circuits                |
| **Interface**        | Communication and external interface circuits |
| **Memory**           | Non-volatile and external memory devices      |
| **Microcontroller**  | MCU reference implementations                 |
| **Networks_Active**  | Active network circuits                       |
| **Networks_Passive** | Passive networks                              |
| **Power**            | Power management and regulation circuits      |
| **Sensor**           | Sensor devices and interfaces                 |

Several of the design blocks derived from: [williamweatherholtz/kicad_subs](https://github.com/williamweatherholtz/kicad_subs/tree/master).

The nRF54L design blocks are from [hlord2000/nordic-lib-kicad](https://github.com/hlord2000/nordic-lib-kicad).

## Working with Design Blocks

Design blocks are reusable schematic fragments managed through KiCad's Design Blocks panel. They allow you to save and reuse circuit designs across projects. See the KiCad documentation for more details: [KiCad Design Blocks](https://docs.kicad.org/9.0/ca/eeschema/eeschema.html#schematic-design-blocks).

### Using design blocks

1. Ensure design block libraries are registered (see [Getting Started](getting_started.md)).
2. In the **Schematic Editor**, open **View → Panels → Design Blocks**.
3. Browse the library tree or use the filter textbox to search by name, description, or keywords.
4. Select a design block to preview it, then double click or right click → **Place Design Block**.
5. Configure placement options:
   - **Place as sheet**: Inserts as a hierarchical sheet (click twice to define corners).
   - **Keep annotations**: Preserves symbol references instead of reannotating.
   - **Place repeated copies**: Continues placing after each insertion (press Esc to cancel).
6. Click in the canvas to place the block.

### Creating design blocks for kmlib-local

**Prerequisites:** The appropriate `KMLib_<Category>.kicad_blocks` library must already exist. If you need a new category library:

1. Right click in the Design Blocks panel → **New Library…**
2. Choose **Global library table** (available to all projects).
3. Set location to `${KMLIB_LOCAL}/blocks/` and name as `KMLib_<Category>.kicad_blocks`.

**To save a new design block:**

1. Create and test your circuit in a schematic (entire sheet or selected objects).
2. Right click the target KMLib library in the Design Blocks panel and choose:
   - **Save Current Sheet as Design Block…** for entire sheet, or
   - **Save Selection as Design Block…** for selected objects.
3. Configure in the **Design Block Properties** dialog:
   - **Name**: Descriptive identifier (e.g., `MCP73831_LiPo_Charger`).
   - **Description**: Brief explanation of circuit function.
   - **Keywords**: Space-separated search terms.
   - **Default Fields**: Optional key/value pairs for hierarchical sheets.
4. Click **OK**. KiCad automatically creates a `.kicad_block` directory with `.kicad_sch` and `.json` files.

**To edit existing blocks:** Right click the design block → **Properties…** to modify metadata.

### Committing to the repository

```sh
git add kmlib-local/blocks/KMLib_<Category>.kicad_blocks/<BlockName>.kicad_block/
git commit -m "Add <BlockName> design block: <brief description>"
```

## Adding Individual Components

The following steps cover adding or modifying individual symbols, footprints, and 3D models to `kmlib-local`.

### 1) Create or update the schematic symbol

1. Open **Symbol Editor** and select the appropriate KMLib\_\* library based on component category.
2. Create a symbol or duplicate a similar one.
3. Populate properties:
   - `Reference`: family designator (`U`, `J`, etc.).
   - `Value`: match the symbol name.
   - `Footprint`: `KMLib_<Category>:<footprint_name>` once the footprint exists.
   - `Datasheet`, `Description`, `Keywords`: copy from the datasheet.
4. Set pin names, electrical types, and units. Follow KiCad's symbol conventions for readability.
5. Run **Tools -> Symbol Checker** and fix issues before saving.

### 2) Create or update the footprint

1. Open **Footprint Editor** and select the appropriate KMLib\_\* library based on component category.
2. Create the footprint in millimetres. Align the local origin sensibly (pin 1 or part centre).
3. Add `F.SilkS`, `B.SilkS`, `F.CrtYd`, and `F.Fab` graphics following KiCad conventions.
4. In **Footprint Properties -> 3D Models**, reference `${KMLIB_LOCAL}/3dmodels/<category>/<model-file>`.
5. Verify pad-to-pad spacing against the datasheet.
6. Run **Tools -> Footprint Checker** and resolve errors.

### 3) Place the 3D model

1. Put the STEP/WRL model in `kmlib-local/3dmodels/<Category>.3dshapes/` matching the footprint category.
2. Reference using `${KMLIB_LOCAL}/3dmodels`, for example: `${KMLIB_LOCAL}/3dmodels/<Category>.3dshapes/<model-file>`.
3. Orient/scale in the **3D Models** tab.
4. Confirm with **3D Viewer**.

### 4) Link symbol and footprint

- Update the symbol `Footprint` field to `KMLib_<Category>:<footprint_name>` matching the footprint library used.
- If the part supports multiple packages, create aliases or variants with clear suffixes.

### 5) Validate

- Place the new symbol in a scratch schematic. Run ERC.
- Update the footprint on a dummy PCB. Run DRC and open 3D Viewer.
- Check `git status` for unintended edits.

### 6) Commit and share

Stage the categorized files:

```sh
git add kmlib-local/symbols/KMLib_<Category>.kicad_sym
git add kmlib-local/footprints/KMLib_<Category>.pretty/<new-footprint>.kicad_mod
git add kmlib-local/3dmodels/<Category>.3dshapes/<model-file>
```

Commit with a clear message referencing the part number.

**If you added or removed a library**, regenerate the committed library tables so a clean
checkout still resolves everything:

```sh
python3 scripts/gen_lib_tables.py
```

**Do not hand-edit anything under `vendor/`** to pick up an upstream change. Use
`scripts/vendor_sync.py`, which performs a three-way merge and moves the pin in
`vendor.yaml`, so the update stays traceable. A local fix to a vendored part is allowed and
will survive a sync — but prefer upstreaming it.
