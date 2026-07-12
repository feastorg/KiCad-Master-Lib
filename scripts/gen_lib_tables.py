#!/usr/bin/env python3
"""Regenerate the KiCad library tables from what is actually on disk.

Scans kmlib-local/ (first-party) and vendor/ (vendored upstreams) and writes:

    kmlib.fp-lib-table            footprints  (*.pretty)
    kmlib.sym-lib-table           symbols     (*.kicad_sym)
    kmlib.design-block-lib-table  design blocks (*.kicad_blocks)

Paths are emitted relative to ${KICAD_MASTER_LIB} so the tables are portable:
point that variable at this repo and every library resolves, with no dependence
on a developer's global KiCad configuration.

Legacy KiCad 5 symbol libraries (*.lib) are deliberately skipped -- KiCad 10's
sym-lib-table cannot consume them. They remain on disk for manual import.

Nickname is the library's basename. Where two libraries would claim the same
nickname, the parent directory is prefixed to disambiguate, deterministically.

    python3 scripts/gen_lib_tables.py
"""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOTS = ("kmlib-local", "vendor")
VAR = "${KICAD_MASTER_LIB}"

KINDS = (
    # (output file,                  table tag,               suffix,           is_dir)
    ("kmlib.fp-lib-table", "fp_lib_table", ".pretty", True),
    ("kmlib.sym-lib-table", "sym_lib_table", ".kicad_sym", False),
    ("kmlib.design-block-lib-table", "design_block_lib_table", ".kicad_blocks", True),
)


def discover(suffix: str, is_dir: bool) -> list[Path]:
    out: list[Path] = []
    for root in ROOTS:
        base = ROOT / root
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            for name in (dirnames if is_dir else filenames):
                if name.endswith(suffix):
                    out.append(Path(dirpath) / name)
    return sorted(out)


def nicknames(paths: list[Path], suffix: str) -> dict[Path, str]:
    """Basename as nickname, prefixing ancestor dirs until every name is unique.

    Some upstreams ship the same library name under several product variants
    (OPL carries two LoRa-E5.pretty, one per Wio-E5 variant), and their immediate
    parents collide too -- so keep climbing rather than assuming one level fixes it.
    """
    result = {p: p.name[: -len(suffix)] for p in paths}
    for depth in range(1, 6):
        dupes = {n for n, c in Counter(result.values()).items() if c > 1}
        if not dupes:
            break
        for p in paths:
            if result[p] in dupes:
                parts = p.relative_to(ROOT).parts
                ancestors = parts[max(0, len(parts) - 1 - depth) : -1]
                result[p] = "_".join([*ancestors, p.name[: -len(suffix)]])
    # Nicknames are used verbatim in lib_id strings; keep them shell/script safe.
    return {p: n.replace(" ", "_") for p, n in result.items()}


def main() -> None:
    for filename, tag, suffix, is_dir in KINDS:
        paths = discover(suffix, is_dir)
        nicks = nicknames(paths, suffix)
        lines = [f"({tag}", "\t(version 7)"]
        for p in paths:
            rel = p.relative_to(ROOT).as_posix()
            src = "first-party" if rel.startswith("kmlib-local") else "vendored"
            lines.append(
                f'\t(lib (name "{nicks[p]}")(type "KiCad")'
                f'(uri "{VAR}/{rel}")(options "")(descr "{src}"))'
            )
        lines.append(")\n")
        (ROOT / filename).write_text("\n".join(lines))
        print(f"{filename:<30} {len(paths):>3} libraries")


if __name__ == "__main__":
    main()
