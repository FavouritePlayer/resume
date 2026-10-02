#!/usr/bin/env python3
"""Revolving before/after: keep the last-approved .tex/.pdf of every resume in previous/.

  python3 scripts/snapshot.py diff [files...]   # current vs previous/ (tex diff + page counts)
  python3 scripts/snapshot.py accept            # previous/ <- what's in git HEAD (the approved state)
  python3 scripts/snapshot.py accept --working  # previous/ <- working tree instead (no commit needed)

"Approved" means committed: .githooks/post-commit runs `accept` after every commit, so previous/
always holds the state as of the last commit. It is seeded from HEAD on first use.
previous/ is gitignored (git history is the durable record; this is the quick local before/after).
"""
import argparse, difflib, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREV = ROOT / "previous"


def names():
    stems = ["cv_master"] + sorted(p.stem for p in ROOT.glob("resume_*.tex"))
    return [f"{s}{e}" for s in stems for e in (".tex", ".pdf")]


def from_head(name):
    r = subprocess.run(["git", "show", f"HEAD:{name}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def accept(working):
    PREV.mkdir(exist_ok=True)
    for n in names():
        data = None if working else from_head(n)
        src = ROOT / n
        if data is None and src.exists():  # untracked (e.g. cv_master.pdf) or --working
            data = src.read_bytes()
        if data is not None:
            (PREV / n).write_bytes(data)
    print(f"previous/ updated from {'working tree' if working else 'git HEAD'}")


def pages(path):
    try:
        import fitz
        return len(fitz.open(path)) if path.exists() else None
    except Exception:
        return None


def diff(files):
    if not PREV.exists():
        accept(False)
        print("(seeded previous/ from HEAD)")
    wanted = [n for n in names() if n.endswith(".tex") and (not files or n in files or n[:-4] in files)]
    any_change = False
    for n in wanted:
        old = PREV / n
        a = old.read_text().splitlines(True) if old.exists() else []
        b = (ROOT / n).read_text().splitlines(True)
        d = list(difflib.unified_diff(a, b, f"previous/{n}", n, n=2))
        pdf = n[:-4] + ".pdf"
        po, pn = pages(PREV / pdf), pages(ROOT / pdf)
        if not d and po == pn:
            continue
        any_change = True
        print(f"\n===== {n}   pages: {po} -> {pn}")
        sys.stdout.writelines(d)
    if not any_change:
        print("no changes vs previous/")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["diff", "accept"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--working", action="store_true")
    a = ap.parse_args()
    accept(a.working) if a.cmd == "accept" else diff(a.files)
