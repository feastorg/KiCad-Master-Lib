# TODO

- [x] ~~Evaluate scripting options to generate KiCad library tables automatically instead of
  the current manual registration steps.~~ Done: `scripts/gen_lib_tables.py` generates
  `kmlib.{fp,sym,design-block}-lib-table` from what is on disk, and they are committed. A
  clean clone resolves every library with no manual registration.

- [ ] Eventually split `kmlib-local` into its own repo (e.g. `feast-kicad-library`).
  **Note:** do *not* bring it back as a submodule. Submodules were removed in favour of
  vendoring precisely because they cannot be patched locally, need `--recursive`, and
  break checkouts (`submodules: true` fails outright on a stray gitlink). If it is split
  out, vendor it like the others and track it in `vendor.yaml`.

- [ ] Database integration / the relationship to kicad databases

- Add the following to kmlib-local/blocks:
  - Passive Networks
    - [ ] Two-Resistor Voltage Divider

    - [ ] Single-Pole RC Low-Pass Filter

    - [ ] Single-Pole RC High-Pass Filter

    - [ ] LC Pi Filter (C-L-C)

    - [ ] RC Snubber Network

  - Active Networks
    - [ ] Non-Inverting Op-Amp Gain Stage

    - [ ] Inverting Op-Amp Gain Stage

    - [ ] Unity-Gain Voltage Follower

    - [ ] Sallen-Key Low-Pass Filter (2nd Order)

    - [ ] Basic Op-Amp Comparator (No Hysteresis)

- [ ] Future References
  - [JMVI/KiCAD-PCB-Design-Examples](https://github.com/JMVI/KiCAD-PCB-Design-Examples)

  - [mfhepp/open_hardware_template](https://github.com/mfhepp/open_hardware_template)

  - [computergeek1507/KiCad_Designs](https://github.com/computergeek1507/KiCad_Designs)

  - [dbuchwald/kicad-simple](https://github.com/dbuchwald/kicad-simple)
