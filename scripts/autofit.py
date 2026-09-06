#!/usr/bin/env python3
"""
Find a minimal, VERIFIED set of changes (margin reduction + bullet cuts) to
bring a resume back to one page, when it's over.

    python3 scripts/autofit.py resume_mle.tex
    python3 scripts/autofit.py resume_mle.tex --floor-in 0.5 --apply

Design (see CLAUDE.md's "measure_layout.py" note for why arithmetic
prediction across a page-break isn't trustworthy on its own): this script
never predicts. Every candidate combination of (margin setting, bullets
cut) is verified by an actual latexmk compile + real page count, exactly
like a human would do by hand -- the only thing automated is the search
order, using measure_layout.py's exact per-bullet heights to make that
search efficient instead of exhaustive.

Policy (confirmed 2026-09):
  - Margin and content cuts are considered together, but margin room
    within [floor, current] is treated as strictly free (no content lost)
    and is always fully used before any bullet is cut -- there's no
    downside to using available margin room within the allowed floor, so
    partially using it while still cutting more content than necessary
    would be strictly worse. Only once margin is at its floor (or was
    already at/below it -- as all five profiles are, as of this writing)
    does the search fall back to content-only cuts.
  - A hard floor (default 0.5in, matching CLAUDE.md's ATS margin
    guidance) is enforced -- if the file's current margin is already at or
    below the floor, the margin lever contributes zero headroom and is
    skipped entirely, not forced tighter.
  - Top/bottom margin changes only affect page *capacity*, never
    individual bullets' heights (no reflow within a column), so they are
    verified in a single recompile at the floor value -- unlike content
    cuts, there's no non-linear-boundary risk to search around.
  - Every file's margins are read from and written back to *that file's
    own* geometry block -- nothing here assumes or shares a margin value
    across profiles.
  - Content cuts are ranked largest-first by default (from
    measure_layout.py's exact heights) purely to make the search efficient;
    this is NOT a content-value judgment. Always review the proposed cut
    list against CLAUDE.md's cutting-priority rules before using --apply.

Without --apply this only reports the plan (which bullets, what margin,
verified page count) -- it never touches the real .tex unless you pass it.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRATCH = ROOT / ".build" / "autofit_scratch"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from measure_layout import (  # noqa: E402
    ITEM_RE,
    END_HIGHLIGHTS_RE,
    inject_markers,
    sp_to_pt,
)

MARGIN_RE = re.compile(r"(top|bottom)(\s*=\s*)([\d.]+)(\s*cm)")


def get_item_spans(source: str):
    """Line-range spans for each \\item block, in the same order/labeling
    measure_layout.py uses, so cut indices line up with its height report."""
    lines = source.splitlines(keepends=True)
    spans = []
    current_start = None
    current_label = None
    for i, line in enumerate(lines):
        if ITEM_RE.match(line):
            if current_start is not None:
                spans.append((current_start, i, current_label))
            current_start = i
            label = ITEM_RE.sub("", line).strip()
            label = re.sub(r"\\textbf\{([^}]*)\}", r"\1", label)
            current_label = re.sub(r"[\\{}]", "", label)[:60] or "(empty)"
        elif END_HIGHLIGHTS_RE.match(line) or line.strip() == r"\end{document}":
            if current_start is not None:
                spans.append((current_start, i, current_label))
                current_start = None
    return spans, lines


def get_current_margins_cm(source: str) -> dict:
    return {m.group(1): float(m.group(3)) for m in MARGIN_RE.finditer(source)}


def build_variant(base_lines, spans, cut_indices: set, margin_in) -> str:
    lines = list(base_lines)
    for idx in sorted(cut_indices, reverse=True):
        start, end, _ = spans[idx]
        del lines[start:end]
    source = "".join(lines)
    if margin_in is not None:
        margin_cm = margin_in * 2.54
        source = MARGIN_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}{margin_cm:.4f}{m.group(4)}", source)
    return source


def compile_variant(source: str, tag: str):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    scratch_tex = SCRATCH / f"{tag}.tex"
    scratch_tex.write_text(source)
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", scratch_tex.name]
    result = subprocess.run(cmd, cwd=SCRATCH, capture_output=True, text=True)
    pdf_path = SCRATCH / f"{tag}.pdf"
    if result.returncode != 0 or not pdf_path.exists():
        return None
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    try:
        return doc.page_count
    finally:
        doc.close()


def get_baseline_heights(tex_path: Path):
    """Exact per-item heights from measure_layout.py's own mechanism, keyed
    by the same item_N ordering get_item_spans() produces."""
    source = tex_path.read_text()
    instrumented, marks = inject_markers(source)
    scratch_tex = SCRATCH / f"{tex_path.stem}_measure.tex"
    SCRATCH.mkdir(parents=True, exist_ok=True)
    scratch_tex.write_text(instrumented)
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", scratch_tex.name]
    result = subprocess.run(cmd, cwd=SCRATCH, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("baseline measurement compile failed")
    poslog = SCRATCH / f"{scratch_tex.stem}.poslog"
    positions = {}
    for line in poslog.read_text().splitlines():
        m = re.match(r"MARK (\S+) page=(\d+) y=(-?\d+)", line)
        if m:
            positions[m.group(1)] = (int(m.group(2)), int(m.group(3)))

    heights = {}
    prev_page, prev_y = None, None
    item_i = 0
    for mark_id, kind, label in marks:
        if mark_id not in positions:
            continue
        page, y = positions[mark_id]
        if kind == "item":
            if prev_page is not None and page == prev_page:
                heights[item_i] = sp_to_pt(prev_y - y)
            else:
                heights[item_i] = None  # unknown -- crosses a page boundary
            item_i += 1
        prev_page, prev_y = page, y
    return heights


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file")
    parser.add_argument("--floor-in", type=float, default=0.5, help="hard lower bound for top/bottom margin (default 0.5in, matches CLAUDE.md's ATS floor)")
    parser.add_argument("--apply", action="store_true", help="write the winning plan back to the real file (default: dry run / report only)")
    args = parser.parse_args()

    tex_path = ROOT / args.tex_file
    source = tex_path.read_text()
    spans, base_lines = get_item_spans(source)
    margins = get_current_margins_cm(source)
    current_margin_in = margins.get("top", 0) / 2.54

    print(f"=== {tex_path.name}: current margin {current_margin_in:.3f}in, floor {args.floor_in}in ===")

    baseline_pages = compile_variant(source, "baseline")
    print(f"baseline: {baseline_pages} page(s)")
    if baseline_pages == 1:
        print("already one page -- nothing to do.")
        return

    heights = get_baseline_heights(tex_path)
    ranked = sorted(
        [i for i in range(len(spans)) if heights.get(i) is not None],
        key=lambda i: -heights[i],
    )

    # Step 1: margin, if there's real headroom -- strictly free, so use all
    # of it up front (never partially, and never below the floor).
    margin_headroom = current_margin_in - args.floor_in
    if margin_headroom > 1e-6:
        trial_margin = args.floor_in
        pages = compile_variant(build_variant(base_lines, spans, set(), trial_margin), "margin_only")
        print(f"margin -> {trial_margin}in alone: {pages} page(s)")
        if pages == 1:
            print(f"\nPLAN: shrink margin {current_margin_in:.3f}in -> {trial_margin:.3f}in. No content cuts needed.")
            if args.apply:
                apply_plan(tex_path, source, base_lines, spans, set(), trial_margin)
            return
        active_margin = trial_margin
    else:
        print(f"margin already at or below the floor ({current_margin_in:.3f}in <= {args.floor_in}in) -- no headroom, content-only.")
        active_margin = None

    # Step 2: greedy add content cuts (largest first) until it fits.
    cuts = set()
    for idx in ranked:
        cuts.add(idx)
        pages = compile_variant(build_variant(base_lines, spans, cuts, active_margin), "trial")
        print(f"  + cut '{spans[idx][2]}' ({heights[idx]:.1f}pt) -> {pages} page(s)")
        if pages == 1:
            break
    else:
        print("\nFAIL: even cutting every measurable bullet didn't reach one page.")
        sys.exit(1)

    # Step 3: minimize -- try restoring the smallest cuts first, keep the
    # restoration only if it still fits.
    for idx in sorted(cuts, key=lambda i: heights[i]):
        trial_cuts = cuts - {idx}
        pages = compile_variant(build_variant(base_lines, spans, trial_cuts, active_margin), "trial")
        if pages == 1:
            cuts = trial_cuts
            print(f"  - restored '{spans[idx][2]}' (still one page without it being cut)")

    print("\n=== PLAN ===")
    if active_margin is not None:
        print(f"  margin: {current_margin_in:.3f}in -> {active_margin:.3f}in")
    print(f"  cut {len(cuts)} bullet(s):")
    for idx in sorted(cuts):
        print(f"    - {spans[idx][2]}  ({heights[idx]:.1f}pt)")
    final_pages = compile_variant(build_variant(base_lines, spans, cuts, active_margin), "final")
    print(f"  verified result: {final_pages} page(s)")

    if args.apply:
        apply_plan(tex_path, source, base_lines, spans, cuts, active_margin)


def apply_plan(tex_path, source, base_lines, spans, cuts, active_margin):
    new_source = build_variant(base_lines, spans, cuts, active_margin)
    tex_path.write_text(new_source)
    print(f"\napplied to {tex_path} -- recompile and read it before considering this done.")


if __name__ == "__main__":
    main()
