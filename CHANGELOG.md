# Changelog

Notable changes to KiCad-Master-Lib.

Format: [Keep a Changelog](https://keepachangelog.com/)

This repository had no formal releases through most of its history, so earlier entries are
grouped by dated development era rather than by version.

---

## [Unreleased]

### Added

- `1990973` (Phoenix Contact SPT 2,5/ 2-H-5,0, 2-position push-in terminal block, 5 mm
  pitch, 24 A, horizontal wire entry) in `KMLib_Connectors`, with its footprint. Same
  geometry as `1751066`, one position wider: body 11.4 x 14.4 mm, two 1.2 mm solder pins
  per potential 8.2 mm apart, both numbered with their potential (pads 1, 1, 2, 2). The
  symbol has one pin per potential.
- `PCIE-036-02-X-D-TH` (Samtec PCI Express x1 edge-card socket, 36 positions, 1.00 mm
  pitch, vertical, through-hole) in `KMLib_Connectors`, with its footprint
  `SAMTEC_PCIE-036-02-X-D-TH`. Slice_STPC referenced both but neither was in the library.
  Holes, rows and the two Ø2.35 mm peg holes follow Samtec's recommended PCB layout,
  Rev F; no 3D model yet.
- `1985218` (Phoenix Contact PTSA 1,5/ 4-3,5-Z, 4-position push-in terminal block, 3.5 mm
  pitch, zig-zag pins) in `KMLib_Connectors`, with its footprint. Pin positions follow the
  Phoenix drill plan; no 3D model yet.
- `G3VM-61VY4` (Omron MOS FET relay, 60 V, 700 mA AC peak/DC, 0.3 Ω max, 1 mA trigger) in
  `KMLib_Electromechanical`, with a `KMLib_Relays` footprint on Omron's recommended pads
  (K347-E1). It replaces the CPC1002N, which Littelfuse marks Not For New Designs.
- `TPS26630PWP_eFuse` (TI TPS26630, 60 V, 6 A industrial eFuse: adjustable OVP cutoff and
  UVLO, active current limit, reverse polarity with an external N-FET) in `KMLib_IC_Power`.
  Pins follow TI SLVSE94G Table 5-1; the footprint is KiCad's stock HTSSOP-20 PowerPAD
  matching TI's PWP0020T land pattern (3.4 x 6.5 mm pad, 2.96 x 2.96 mm mask opening).
- `scripts/lint_lib.py` — static checks over `kmlib-local/`: dead 3D-model paths,
  symbol Footprints with no library prefix or naming a footprint that does not exist,
  footprint name differing from file name (errors); `unspecified` pins, non-URL
  datasheets, empty Footprints (warnings).
- `scripts/check_parse.py` — loads every first-party library through `kicad-cli`.
- `scripts/gen_lib_tables.py --check` — exits non-zero when the committed tables are
  stale.
- `.github/workflows/lint.yml` — runs all three on every pull request, the parse step in
  the fleet's pinned KiCad 10 image.
- `PDS1040-13` (40 V 10 A Schottky, PowerDI 5) and `ZLLS350TA` (40 V 380 mA Schottky,
  SOD-523) in `KMLib_Discrete_Semiconductors`, with `POWERDI5_DIO` and `DIODE_SOD-523_DIO`
  footprints (and `-L`/`-M` variants) and 3D models.
- `SI7288DP-T1-GE3` (dual N-channel 40 V MOSFET) in `KMLib_Discrete_Semiconductors`, with
  `POWERPAK_SO-8_DUAL_VIS` footprint (and `-L`/`-M` variants) and 3D model. Replaces the
  Slice_SOLR rescue symbol, which still carried the AO4882 value, datasheet and SOIC-8
  footprint it had been cloned from.
- `LTC4311ISC6-TRMPBF` (I2C accelerator) — symbol, `SOT-6_SC_LIT` footprint and its
  variants, and 3D model.

### Changed

- `SparkFun-KiCad-Libraries` synced `2423e36a` → `5741e46f` (44 upstream commits): symbols
  reformatted for KiCad 10, MicroMod moved out of its own symbol library (the
  `SparkFun-MicroMod` nickname is gone from `kmlib.sym-lib-table`; no board used it),
  new M.2-E MicroMod footprints, `LBEE5KL1YN`, an 0402 coil, and `User.1` milling
  outlines moved to `F.Fab`/`User.2`. Of the symbols and footprints the fleet uses
  (`WS2812B_5050`, `LED`, `ThingPlus_With_Connectors`, `LED_0603_1608Metric`,
  `OSHW_Logo_5mm`), none changed.
- The Atlas Scientific Electrically Isolated EZO Carrier Board Gen 2 is now a mount, not
  a connector. `KMLib_Connectors:Hole_Mounted_Conn_01x05_Female` and its footprint
  `Hole_Mounted_24mmx34mm_PinHeader_1x05_P2.54mm_Vertical` are replaced by the pinless
  symbol `KMLib_Sensors:Atlas_EZO_Carrier_Gen2_Mount` (reference `A`, not in the BOM) and
  the footprint `KMLib_Boards_Modules:Atlas_EZO_Carrier_Gen2_Mount`; the old names are
  gone. The carrier is screwed flat on its standoffs, and its right-angle header connects
  by its own 5-wire Dupont cable, so nothing on the host sits under it. Put the five
  signals on a stock 1x05 2.54 mm male header (`Conn_01x05_Pin`) beside the carrier's
  pin edge. The old footprint also did not match the carrier: its four 4.0 mm holes
  formed a skewed 33.96-33.99 x 24.65-24.81 mm quadrilateral. The new one, measured
  from Atlas's STEP model, has four 3.2 mm NPTH on the carrier's 24.00 x 34.00 mm
  rectangle (3.0 mm holes on the carrier, #4-40 hardware), with the origin at the
  rectangle's centre. Fab and silk draw the 32 x 42 mm board, and fab also draws the
  SMA overhang (-x) and the right-angle pin overhang (+x, VCC end marked). The courtyard
  covers the board and both overhangs, with screw-head circles on `B.CrtYd`. The 3D
  model moved to `Boards_Modules.3dshapes` and lands its holes on the NPTH. Only
  Slice_PHDO (an unpublished branch, J3/J4, no layout yet) used the old parts.

### Fixed

- `1751066` (Phoenix Contact SPT 2,5/ 1-H-5,0) in `KMLib_Connectors`: the body outline was
  4.1 x 14.4 mm and sat 0.7 mm towards the wire entry; the part is 6.4 x 14.4 mm. Body,
  silk and courtyard now follow Phoenix's 3D model: the two solder pins of the potential
  on the body's long axis, 2.3 mm from one side, the wire-entry face 3.67 mm in front of
  pad 1 and the back face 2.53 mm behind pad 2. Holes are 1.2 mm (Phoenix's figure, was
  1.1) on 2.4 mm pads. The 3D model now lands its pins on the pad centres. Pad numbers
  and positions are unchanged.
- `Atlas_OEM` in `KMLib_Boards_Modules`: P6, P7, P8 and P11 sat 0.01-0.1 mm off the
  module's 0 / 12 mm pad columns (P6 at x -0.01, P7/P8 at 12.1, P11 at 11.9). They are on
  the grid now. 10-pin pH/EC/ORP modules sit on P1-P5 and P8-P12. The 12-pin RTD OEM does
  not fit: its pad columns are 11 mm apart, not 12.
- `Atlas_OEM` in `KMLib_Boards_Modules`: the module outline on F.SilkS ran through the
  centre of all 12 castellated pads. The outline is now on F.Fab, and a silk rectangle
  sits outside the pads (0.147 mm or more from every pad). On Slice_AOEM's four modules
  this clears all 48 silk_over_copper warnings and adds no other silkscreen or clearance
  violation.
- `Thermal_Pad` in `KMLib_Mounting` no longer has F.Paste. It is the BREAD slices'
  unsoldered heat-spreading pad opposite the buck regulator, with open GND vias in it; a
  stencil would have printed paste over the whole 12 x 12 mm pad, and paste over open vias
  wicks away in reflow.
- `5025700893` (Molex 502570-0893 microSD) in `KMLib_Connectors` now carries the three
  pattern-prohibition areas from Molex drawing SD-502570-001 rev A, sheet 2, as F.Cu
  keepouts (no tracks, vias or pour). Pads are unchanged; they already match that drawing.
- `SOIC_05WU-7_DIO`: the pin-1 `*` was drawn twice on F.SilkS and twice on F.Fab, as
  identical texts at the same position. One of each remains.
- 21 generated footprints drew the pin-1 `*` twice on F.SilkS and twice on F.Fab, as
  identical texts at the same position. One of each remains. In `KMLib_IC_SMD`: CD4060BM,
  CD4060-L/-M, CP_16_19_ADI, DGN8_1P89X1P57, DIODE_SOD-523_DIO, RS_20_ADI and
  SOT-6_SC_LIT with their `-L`/`-M` variants, and `SOIC_05WU-7_DIO-L`/`-M` (20); in
  `KMLib_Switches`: `SW_Slide-CK-1101M2S3CQE2`.
- `1217861-1_Tab`: both pins were `unspecified`, so every connection to the tab raised a
  `pin_to_pin` ERC warning. Now `passive`.
- 17 footprint `(model ...)` paths that resolved nowhere — KiCad 5 library names
  (`Housings_QFP.3dshapes/…`, `Pin_Headers.3dshapes/…`), `${KIPRJMOD}`-relative paths, and
  `${KICAD9_3DMODEL_DIR}` — now point at the equivalent KiCad 10 stock models via
  `${KICAD10_3DMODEL_DIR}`.
- Six symbol Footprints that could never resolve: `NTGS4111PT1G`, the two Phoenix PTSA
  terminals (no library prefix), the Wago 2606 and both Keystone test points (wrong
  footprint name).
- `KMLib_Aesthetic/BREAD_logo_v1.kicad_mod` declared itself `LOGO`; KiCad keys
  footprints by the name inside the file.
- `ADUM5010ARSZ-RL7_Isolated_DC-DC`: the GNDP and GNDISO pins were `power_out`, so tying
  a side's grounds together raised `pin_to_pin` ERC errors, and VISO was `unspecified`,
  so nothing drove the isolated supply. Grounds are now `power_in` and VISO `power_out`.

### Removed

- **Git LFS.** `.gitattributes` tracked `*.step` and `*.stl` through LFS, but only 14 files
  (22.6 MB) were ever stored that way — `*.stp` and `*.wrl` were not tracked, and neither
  were the vendored 3D models. Any clone without `git-lfs` installed silently received
  132-byte pointer files instead of models, and KiCad reported nothing: the 3D viewer simply
  showed no model.

  The 14 objects have been fetched from LFS storage and committed as ordinary files. At
  22.6 MB, LFS offered no benefit and cost a hard dependency on every clone and CI job.

### Added

- `CHANGELOG.md`.

### Changed

- Documentation updated for KiCad 10, the committed library tables, and vendoring.
  `KMLIB_LOCAL` is documented as `${KICAD_MASTER_LIB}/kmlib-local` with a forward slash;
  the backslash previously given does not resolve on Linux or macOS, and KiCad reports no
  error when it fails — 3D models simply do not appear.

---

## 2026-07-12

### Changed

- Vendored upstream libraries synced ([#4]):
  - `SparkFun-KiCad-Libraries` `42e5152f` → `2423e36a` (123 commits)
  - `OPL_Kicad_Library` `d3392376` → `b0035c51` (6 commits)

  No board's library resolution changed. Of the footprints in use, only `Standoff` and
  `Jumper_2_NC_Trace` changed, and both retain identical pad geometry.

---

## 2026-07-11 — vendoring and library tables ([#1])

### Added

- `kmlib.fp-lib-table`, `kmlib.sym-lib-table`, `kmlib.design-block-lib-table` — committed
  library tables registering all 51 footprint, 46 symbol and 10 design-block libraries via
  `${KICAD_MASTER_LIB}`. A clean clone now resolves every library without per-machine KiCad
  configuration.
- `scripts/gen_lib_tables.py` — regenerates the tables from what is on disk.
- `scripts/vendor_sync.py` — re-vendors an upstream library via a three-way merge, so local
  modifications survive an upstream sync.
- `scripts/check_drift.py` and a daily `upstream-drift` workflow — opens a tracking issue
  when an upstream moves past its pin. Nothing syncs automatically.
- `vendor.yaml` — manifest of upstream URL, tracked ref, pinned commit and licence for each
  vendored library.
- `KMLib_Connectors:BREAD_Slice_Bus_10Pin` — the BREAD slice-bus connector footprint.

### Changed

- Upstream libraries (SparkFun, Seeed OPL, DigiKey, Arduino) are **vendored** under
  `vendor/` instead of tracked as git submodules.
- Names no longer contain spaces (`Thermal Pad` → `Thermal_Pad`, and similar), since names
  appear verbatim in `lib_id` strings and on command lines.

### Fixed

- `LMD18200TNOPB`: 3D model path pointed outside `3dmodels/IC_THT.3dshapes/`.

---

## 2026-04 — organisation

### Changed

- Org rename: `FEASTorg` → `feastorg`.

---

## 2026-01 — reorganisation

### Changed

- Symbols, footprints and 3D models reorganised into categorised `KMLib_*` libraries.
- Prototyping footprints renamed and grouped.

---

## 2025-04 — 3D models

### Added

- 3D models for KMLib parts, stored via Git LFS (since removed — see [Unreleased]).
- Design blocks (`kmlib-local/blocks/`), migrated from the archived
  `KiCad-Hierarchical-Designs` repository.
- GitHub Pages documentation.

---

## 2024-05 — initial

### Added

- Initial library: FEAST symbols and footprints, with upstream vendor libraries as git
  submodules.

[#1]: https://github.com/feastorg/KiCad-Master-Lib/pull/1
[#4]: https://github.com/feastorg/KiCad-Master-Lib/pull/4
