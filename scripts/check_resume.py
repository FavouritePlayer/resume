#!/usr/bin/env python3
"""
Fast, non-visual checks for this repo's resume .tex files -- replaces the
"render to an image and read it" loop for the two checks that dominated
that loop's cost: is this still one page, and did any line overflow its
column (an orphan/widow-causing wrap).

    python3 scripts/check_resume.py                    # check every
                                                         # resume_*.tex
    python3 scripts/check_resume.py resume_mle.tex ...  # check specific
                                                         # files
    python3 scripts/check_resume.py --render            # also save a
                                                         # per-page PNG
                                                         # (only step that
                                                         # still needs a
                                                         # human/vision look)

For each file this compiles with the same latexmk invocation documented in
CLAUDE.md, then reports:
  - page count (via PyMuPDF -- exact, no need to "trust" it or eyeball it)
  - any "Overfull \\hbox" lines from the LaTeX log (near-exact proxy for
    the orphan/wrap check CLAUDE.md's workflow otherwise requires a
    rendered-image read for)
  - trailing whitespace at the bottom of the last page, both as a raw
    percentage and as "extra slack beyond the configured margin" (parsed
    from the file's own \\usepackage[...]{geometry} block) -- the same
    two numbers CLAUDE.md's whitespace policy asks you to reason about,
    computed here instead of by hand each time.

cv_master.tex is never one-page by design -- it's skipped by default (page
count is still reported, just not treated as a failure).

Exit code is non-zero if any *sendable* profile (every resume_*.tex except
cv_master.tex) didn't compile to exactly one page, or if latexmk failed.
Overfull-hbox and whitespace findings are reported but don't fail the run
on their own -- they're signal for you to look at, same as the old
workflow's manual read, just cheaper to get to.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / ".build"


def compile_tex(tex_path: Path) -> tuple[bool, Path, str]:
    cmd = [
        "latexmk",
        "-pdf",
        f"-aux-directory={BUILD_DIR}",
        "-emulate-aux-dir",
        "-interaction=nonstopmode",
        tex_path.name,
    ]
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    pdf_path = ROOT / (tex_path.stem + ".pdf")
    ok = result.returncode == 0 and pdf_path.exists()
    return ok, pdf_path, result.stdout + result.stderr


def check_overfull(tex_stem: str) -> list[str]:
    log_path = BUILD_DIR / f"{tex_stem}.log"
    if not log_path.exists():
        return []
    return [
        line.strip()
        for line in log_path.read_text(errors="ignore").splitlines()
        if "Overfull \\hbox" in line
    ]


def page_count(pdf_path: Path) -> int:
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    try:
        return doc.page_count
    finally:
        doc.close()


def parse_margins_cm(tex_path: Path) -> dict:
    """Pull top/bottom/left/right/footskip out of the file's own geometry
    block, in cm, so whitespace slack is measured against what this
    specific file is actually configured for (margins are tuned per
    profile, not shared -- see CLAUDE.md)."""
    text = tex_path.read_text()
    margins = {}
    for key in ("top", "bottom", "left", "right", "footskip"):
        m = re.search(rf"{key}\s*=\s*([\d.]+)\s*cm", text)
        if m:
            margins[key] = float(m.group(1)) / 2.54  # cm -> in
    return margins


def render_and_measure(pdf_path: Path, margins: dict, save_png: bool):
    import fitz  # PyMuPDF
    import numpy as np
    from PIL import Image
    import io

    doc = fitz.open(pdf_path)
    try:
        last_page = doc[doc.page_count - 1]
        pix = last_page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("png")
    finally:
        doc.close()

    if save_png:
        out_dir = ROOT / ".build" / "previews"
        out_dir.mkdir(parents=True, exist_ok=True)
        for i in range(fitz.open(pdf_path).page_count):
            d = fitz.open(pdf_path)
            p = d[i].get_pixmap(dpi=150)
            p.save(str(out_dir / f"{pdf_path.stem}_p{i + 1}.png"))
            d.close()

    im = Image.open(io.BytesIO(img_bytes)).convert("L")
    arr = np.array(im)
    h = arr.shape[0]
    rows_with_content = np.where(arr.min(axis=1) < 200)[0]
    if len(rows_with_content) == 0:
        return None
    last_row = rows_with_content.max()
    page_height_in = 11.0  # letter
    trailing_in = (h - last_row) / h * page_height_in
    bottom_margin = margins.get("bottom")
    extra_slack = trailing_in - bottom_margin if bottom_margin is not None else None
    return {"trailing_in": trailing_in, "extra_slack_in": extra_slack}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", help="specific resume_*.tex files (default: all)")
    parser.add_argument("--render", action="store_true", help="also save a per-page PNG under .build/previews/")
    parser.add_argument(
        "--include-master", action="store_true", help="also check cv_master.tex's page count (informational only)"
    )
    args = parser.parse_args()

    if args.files:
        tex_files = [ROOT / f for f in args.files]
    else:
        tex_files = sorted(ROOT.glob("resume_*.tex"))
        if args.include_master:
            tex_files = sorted(ROOT.glob("*.tex"))

    BUILD_DIR.mkdir(exist_ok=True)
    any_fail = False
    rows = []

    for tex_path in tex_files:
        if not tex_path.exists():
            print(f"[ERROR] {tex_path.name}: not found")
            any_fail = True
            continue

        sendable = tex_path.stem != "cv_master"
        ok, pdf_path, log_tail = compile_tex(tex_path)
        if not ok:
            print(f"[FAIL] {tex_path.name}: latexmk did not produce a PDF")
            print(log_tail[-2000:])
            any_fail = True
            continue

        pages = page_count(pdf_path)
        overfull = check_overfull(tex_path.stem)
        margins = parse_margins_cm(tex_path)
        measurement = render_and_measure(pdf_path, margins, args.render)

        status = "OK"
        if sendable and pages != 1:
            status = "FAIL"
            any_fail = True

        rows.append((tex_path.name, status, pages, len(overfull), measurement))

        print(f"[{status}] {tex_path.name}: {pages} page(s)" + ("" if sendable else " (master, no page limit)"))
        if overfull:
            print(f"    WARNING: {len(overfull)} overfull \\hbox line(s):")
            for w in overfull:
                print(f"      {w}")
        if measurement and measurement["extra_slack_in"] is not None:
            print(
                f"    last-page trailing: {measurement['trailing_in']:.2f}in "
                f"(extra slack beyond configured margin: {measurement['extra_slack_in']:.2f}in)"
            )

    print()
    print("=== summary ===")
    for name, status, pages, n_overfull, measurement in rows:
        slack = f"{measurement['extra_slack_in']:.2f}in slack" if measurement and measurement["extra_slack_in"] is not None else "?"
        print(f"  [{status}] {name:32s} {pages} page(s)  overfull={n_overfull}  {slack}")

    if args.render:
        print(f"\nper-page PNGs saved under {BUILD_DIR / 'previews'}")

    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
