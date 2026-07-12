#!/usr/bin/env python3
"""Re-vendor an upstream library, preserving local modifications.

    python3 scripts/vendor_sync.py <name>                 # sync to tip of tracked ref
    python3 scripts/vendor_sync.py <name> --to <sha>      # sync to a specific commit
    python3 scripts/vendor_sync.py <name> --check         # report, change nothing

Local edits to a vendored tree are preserved via a real three-way merge: we
replay our current copy onto the upstream commit we last vendored, then merge
the new upstream commit on top. Git does the merge, so renames and context are
handled properly, and genuine conflicts are surfaced as conflicts rather than
being silently overwritten.

On conflict, the working tree is left with conflict markers in
vendor/<name>/ and vendor.yaml is NOT advanced -- resolve, then re-run with
--to <sha> to record the new pin.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "vendor.yaml"


def git(*args: str, cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=check,
    )


def load_entry(name: str) -> dict[str, str]:
    text = MANIFEST.read_text()
    for block in re.split(r"^\s*-\s+(?=name:)", text, flags=re.M)[1:]:
        entry = {
            k: m.group(1).strip().strip("\"'")
            for k in ("name", "path", "upstream", "ref", "commit")
            if (m := re.search(rf"^\s*{k}:\s*(.+?)\s*$", block, flags=re.M))
        }
        if entry.get("name") == name:
            return entry
    sys.exit(f"error: '{name}' not found in vendor.yaml")


def mirror(src: Path, dst: Path) -> None:
    """Make dst an exact copy of src, ignoring git metadata."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".git"))


def update_manifest(name: str, sha: str) -> None:
    text = MANIFEST.read_text()
    today = dt.date.today().isoformat()

    def fix(block: str) -> str:
        block = re.sub(r"^(\s*commit:\s*).+$", rf"\g<1>{sha}", block, flags=re.M)
        return re.sub(r'^(\s*synced:\s*).+$', rf'\g<1>"{today}"', block, flags=re.M)

    parts = re.split(r"(^\s*-\s+name:.*$)", text, flags=re.M)
    out, hit = [], False
    for part in parts:
        if re.match(r"^\s*-\s+name:", part):
            hit = part.split("name:")[1].strip() == name
            out.append(part)
        else:
            out.append(fix(part) if hit else part)
    MANIFEST.write_text("".join(out))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--to", metavar="SHA", help="upstream commit to sync to (default: tip of ref)")
    ap.add_argument("--check", action="store_true", help="report only, change nothing")
    args = ap.parse_args()

    e = load_entry(args.name)
    vendored = ROOT / e["path"]
    base_sha = e["commit"]

    with tempfile.TemporaryDirectory() as tmp:
        up = Path(tmp) / "upstream"
        print(f"cloning {e['upstream']} ...")
        git("clone", "--quiet", e["upstream"], str(up), cwd=ROOT)

        target = args.to or git("rev-parse", f"origin/{e['ref']}", cwd=up).stdout.strip()
        target = git("rev-parse", target, cwd=up).stdout.strip()

        if target == base_sha:
            print(f"{args.name}: already at {target[:8]} -- nothing to do")
            return 0

        log = git("log", "--oneline", f"{base_sha}..{target}", cwd=up, check=False).stdout
        n = len(log.strip().splitlines())
        print(f"{args.name}: {base_sha[:8]} -> {target[:8]}  ({n} upstream commit(s))")
        if args.check:
            print(log)
            return 0

        # Replay our current (possibly locally-modified) copy onto the commit we
        # last vendored, so git can three-way merge the new upstream onto it.
        git("checkout", "--quiet", "-B", "vendored", base_sha, cwd=up)
        for child in up.iterdir():
            if child.name != ".git":
                shutil.rmtree(child) if child.is_dir() else child.unlink()
        for child in vendored.iterdir():
            dest = up / child.name
            shutil.copytree(child, dest) if child.is_dir() else shutil.copy2(child, dest)

        git("add", "-A", cwd=up)
        if git("diff", "--cached", "--quiet", cwd=up, check=False).returncode:
            git("-c", "user.email=vendor@local", "-c", "user.name=vendor",
                "commit", "--quiet", "-m", "local modifications", cwd=up)
            print("  (local modifications detected and preserved)")

        merged = git("-c", "user.email=vendor@local", "-c", "user.name=vendor",
                     "merge", "--no-edit", target, cwd=up, check=False)
        # -z: paths may contain spaces (several upstream libs have them).
        conflicts = [
            p for p in git("diff", "--name-only", "--diff-filter=U", "-z",
                           cwd=up, check=False).stdout.split("\0") if p
        ]

        mirror(up, vendored)

        if merged.returncode or conflicts:
            print("\nCONFLICT -- resolve these, then re-run with --to " + target[:8])
            for c in conflicts:
                print(f"  {e['path']}/{c}")
            print("\nvendor.yaml NOT advanced.")
            return 1

    update_manifest(args.name, target)
    print(f"  synced; vendor.yaml pinned to {target[:8]}")
    print("  review the diff, then commit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
