#!/usr/bin/env python3
"""Detect drift between vendored libraries and their upstreams.

Reads vendor.yaml, asks each upstream for the current tip of the tracked ref
(via `git ls-remote`, so nothing is cloned), and reports which libraries have
moved since the commit we vendored.

    python3 scripts/check_drift.py            # human-readable table
    python3 scripts/check_drift.py --json     # machine-readable, for CI

Exit status is 0 whether or not drift is found; drift is a normal condition,
not an error. Use --json and inspect `drifted` in CI.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "vendor.yaml"


def load_manifest() -> list[dict]:
    """Parse vendor.yaml without requiring PyYAML.

    The manifest is a fixed, simple shape (a list of flat string mappings), so a
    targeted parser keeps this script dependency-free and runnable on a bare CI
    image. If the manifest ever grows nested structure, switch to PyYAML.
    """
    if yaml_available():
        import yaml  # noqa: PLC0415

        return yaml.safe_load(MANIFEST.read_text())["libraries"]

    libs: list[dict] = []
    for block in re.split(r"^\s*-\s+(?=name:)", MANIFEST.read_text(), flags=re.M)[1:]:
        entry: dict[str, str] = {}
        for key in ("name", "path", "upstream", "ref", "commit", "license"):
            m = re.search(rf"^\s*{key}:\s*(.+?)\s*$", block, flags=re.M)
            if m:
                entry[key] = m.group(1).strip().strip("\"'")
        if entry.get("name"):
            libs.append(entry)
    return libs


def yaml_available() -> bool:
    try:
        import yaml  # noqa: F401, PLC0415

        return True
    except ImportError:
        return False


def upstream_tip(url: str, ref: str) -> str | None:
    """Current SHA of `ref` at `url`, or None if it can't be resolved."""
    try:
        out = subprocess.run(
            ["git", "ls-remote", url, ref],
            capture_output=True, text=True, timeout=60, check=True,
        ).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return out.split()[0] if out.strip() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="emit JSON for CI")
    args = ap.parse_args()

    results = []
    for lib in load_manifest():
        tip = upstream_tip(lib["upstream"], lib["ref"])
        pinned = lib["commit"]
        results.append({
            "name": lib["name"],
            "upstream": lib["upstream"],
            "ref": lib["ref"],
            "pinned": pinned,
            "tip": tip,
            "drifted": bool(tip) and tip != pinned,
            "unreachable": tip is None,
        })

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    width = max(len(r["name"]) for r in results)
    for r in results:
        if r["unreachable"]:
            status = "?? unreachable"
        elif r["drifted"]:
            status = f"DRIFTED  {r['pinned'][:8]} -> {r['tip'][:8]}"
        else:
            status = f"up to date ({r['pinned'][:8]})"
        print(f"{r['name']:<{width}}  {status}")

    drifted = sum(r["drifted"] for r in results)
    print(f"\n{drifted} of {len(results)} librar{'y' if drifted == 1 else 'ies'} drifted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
