#!/usr/bin/env python3
"""
Exact, sub-point-precise layout measurement for this repo's resume .tex
files -- goes beyond check_resume.py's pixel-based whitespace estimate by
asking pdfTeX itself where every bullet actually landed on the page.

Mechanism: \\pdfsavepos + \\pdflastypos are core pdfTeX primitives (no
package needed -- this is what the `zref-savepos` package wraps internally,
but that package isn't installed here and needs sudo to add, so this uses
the primitives directly). A deferred \\write (not \\immediate\\write) is
required: \\pdflastypos is only updated when the page actually ships out,
and a non-immediate \\write is itself a whatsit that gets processed at
shipout time, right after \\pdfsavepos's own whatsit -- so both resolve
together, in one compile pass, no multi-run trickery needed. Verified
empirically against known \\baselineskip/\\topskip values (see git history
/ HANDOFF notes for this branch) before being pointed at real content.

    python3 scripts/measure_layout.py resume_mle.tex
    python3 scripts/measure_layout.py resume_mle.tex --suggest-cuts --overflow-in 0.4

This never touches the real .tex -- it writes an instrumented copy to a
scratch directory, compiles that, and reports on it.

VALIDATED ACCURACY AND ITS LIMIT (tested against a controlled, real
overflow -- not just self-consistency):
  - Per-item heights are exact to the point, and predicting a whitespace
    change from removing an item that's entirely on the LAST page (no
    page-break between it and the document end) matched a real recompile
    to within rounding (predicted +0.532in of new trailing space, measured
    +0.54in).
  - Predicting across a page-break boundary is NOT reliable by arithmetic
    alone: removing an earlier, page-1 item that should also free ~0.53in
    only produced +0.20in of new page-2 whitespace in practice, because
    freeing room on page 1 pulled part of the next item back up from page
    2 -- a real, non-linear TeX reflow effect (the same `\needspace`-driven
    behavior noted in CLAUDE.md's orphan-check section), not a bug in this
    script. Conclusion: trust this script's per-item costs for ranking and
    for same-page arithmetic; always re-run check_resume.py after actually
    applying a cut that crosses a page boundary to confirm the real
    outcome, rather than trusting the arithmetic across that boundary.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = ROOT / ".build" / "measure_scratch"

BOOTSTRAP = r"""
\newwrite\poslogfile
\immediate\openout\poslogfile=\jobname.poslog
\newcommand{\poscheck}[1]{\pdfsavepos\write\poslogfile{MARK #1 page=\arabic{page}\space y=\the\pdflastypos}}
"""

ITEM_RE = re.compile(r"^(\s*)\\item\b")
SECTION_RE = re.compile(r"^\s*\\section\{([^}]*)\}")
END_HIGHLIGHTS_RE = re.compile(r"^\s*\\end\{highlights\}")


def inject_markers(source: str):
    """Returns (instrumented_source, marks) where marks is an ordered list
    of (mark_id, kind, label) describing what each \\poscheck{} corresponds
    to. A mark for item N is placed just before the *next* \\item or
    \\end{highlights} -- i.e. at the end of that item's own content, which
    may span multiple physical lines."""
    lines = source.splitlines(keepends=True)
    out = []
    marks = []
    pending_item_label = None
    item_counter = 0
    section_counter = 0

    def flush_pending(before_line_kind):
        nonlocal pending_item_label, item_counter
        if pending_item_label is not None:
            item_counter += 1
            mark_id = f"item_{item_counter}"
            out.append(f"\\poscheck{{{mark_id}}}\n")
            marks.append((mark_id, "item", pending_item_label))
            pending_item_label = None

    for line in lines:
        if ITEM_RE.match(line):
            flush_pending("item")
            label = ITEM_RE.sub("", line).strip()
            label = re.sub(r"\\textbf\{([^}]*)\}", r"\1", label)
            label = re.sub(r"[\\{}]", "", label)[:60]
            pending_item_label = label or "(empty)"
            out.append(line)
            continue

        if END_HIGHLIGHTS_RE.match(line):
            flush_pending("end_highlights")
            out.append(line)
            continue

        sec_match = SECTION_RE.match(line)
        if sec_match:
            flush_pending("section")
            section_counter += 1
            mark_id = f"section_{section_counter}_start"
            out.append(line)
            out.append(f"\\poscheck{{{mark_id}}}\n")
            marks.append((mark_id, "section_start", sec_match.group(1)))
            continue

        if line.strip() == r"\end{document}":
            flush_pending("end_document")
            out.append("\\poscheck{doc_end}\n")
            marks.append(("doc_end", "doc_end", ""))
            out.append(line)
            continue

        out.append(line)

    instrumented = "".join(out)
    # bootstrap must land right after \begin{document}
    instrumented = instrumented.replace(
        r"\begin{document}", r"\begin{document}" + BOOTSTRAP, 1
    )
    return instrumented, marks


def compile_instrumented(tex_path: Path):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    scratch_tex = SCRATCH / tex_path.name
    source = tex_path.read_text()
    instrumented, marks = inject_markers(source)
    scratch_tex.write_text(instrumented)

    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", scratch_tex.name]
    result = subprocess.run(cmd, cwd=SCRATCH, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout[-3000:])
        print(result.stderr[-1000:])
        raise RuntimeError(f"latexmk failed on instrumented copy of {tex_path.name}")

    poslog_path = SCRATCH / f"{scratch_tex.stem}.poslog"
    positions = {}
    for line in poslog_path.read_text().splitlines():
        m = re.match(r"MARK (\S+) page=(\d+) y=(-?\d+)", line)
        if m:
            positions[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return marks, positions


def sp_to_pt(sp: int) -> float:
    return sp / 65536.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file")
    parser.add_argument("--suggest-cuts", action="store_true", help="rank items by height and show a greedy cut plan to close a given overflow")
    parser.add_argument("--overflow-in", type=float, default=None, help="known overflow in inches (from check_resume.py) to close via --suggest-cuts")
    args = parser.parse_args()

    tex_path = ROOT / args.tex_file
    if not tex_path.exists():
        print(f"no such file: {tex_path}")
        sys.exit(1)

    marks, positions = compile_instrumented(tex_path)

    print(f"=== {tex_path.name}: per-element layout (pdfTeX-exact) ===")
    print(f"{'label':<45} {'page':>4} {'height (pt)':>12} {'height (in)':>12}")

    prev_page, prev_y = None, None
    results = []
    for mark_id, kind, label in marks:
        if mark_id not in positions:
            print(f"  [WARN] no position recorded for {mark_id} ({kind}: {label!r})")
            continue
        page, y = positions[mark_id]
        height_pt = None
        if prev_page is not None and page == prev_page:
            height_pt = sp_to_pt(prev_y - y)
        display_label = label if kind == "item" else f"[{kind}] {label}"
        height_str = f"{height_pt:.3f}" if height_pt is not None else "(crosses page)"
        height_in_str = f"{height_pt / 72:.4f}" if height_pt is not None else ""
        print(f"{display_label:<45} {page:>4} {height_str:>12} {height_in_str:>12}")
        if kind == "item" and height_pt is not None:
            results.append((label, height_pt))
        prev_page, prev_y = page, y

    if args.suggest_cuts:
        print()
        print("=== suggested cut order (largest first -- a naive size-based")
        print("    default; override with real content-value judgment before")
        print("    actually cutting anything, per CLAUDE.md's cutting-priority")
        print("    rules) ===")
        ranked = sorted(results, key=lambda r: -r[1])
        cumulative = 0.0
        target = args.overflow_in * 72 if args.overflow_in else None
        for label, height_pt in ranked:
            cumulative += height_pt
            marker = ""
            if target is not None and cumulative >= target:
                marker = "  <-- cumulative now covers the given overflow"
            print(f"  {height_pt:7.3f}pt  (running total {cumulative:8.3f}pt / {cumulative/72:.3f}in)  {label}{marker}")
            if target is not None and cumulative >= target:
                break
        print()
        print("NOTE: this cumulative total is only reliable arithmetic within a single")
        print("page. If the real overflow spans a page break, apply the cut and re-run")
        print("check_resume.py to confirm the actual result -- removing earlier content")
        print("can shift the break point itself (validated non-linear effect, see the")
        print("module docstring), not just shrink the last page linearly.")


if __name__ == "__main__":
    main()
