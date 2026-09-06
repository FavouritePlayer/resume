# resume

LaTeX source for Arjun Nanduri's resume. See `CLAUDE.md` for the content strategy and editing guidelines.

## Files

- `cv_master.tex` — verbose superset, every bullet, no page limit. Never sent out; the reservoir the specialized profiles are cut from. Named `cv_` rather than `resume_` since it's not a resume at all — it's the unbounded reference document.
- `resume_mle.tex` — one-page, ML/CV-emphasis. Sendable.
- `resume_swe.tex` — one-page, SWE/Founder-emphasis. Sendable.
- `resume_pm.tex` — one-page, Product Management-emphasis. Sendable.
- `resume_research_ai.tex` — one-page, Academic/Research-emphasis (AI/NLP/CV/agents audience). Sendable.
- `resume_research_robotics.tex` — one-page, Academic/Research-emphasis (Robotics/RL audience). Sendable.

All five share the same preamble/macros (though margins/spacing are tuned per profile) — content differs, formatting mechanism does not.

## Checking a resume (fast, no vision tokens)

```
pip3 install --user pymupdf pillow numpy   # one-time
python3 scripts/check_resume.py            # checks every resume_*.tex
python3 scripts/check_resume.py --render   # also saves a per-page PNG
                                            # under .build/previews/
```

Reports exact page count, any `Overfull \hbox` lines (orphan/wrap proxy),
and trailing-whitespace/margin slack for each file — see `CLAUDE.md`'s
Workflow section for how this fits into the editing loop. It's a fast
pre-filter, not a substitute for actually reading the rendered PDF before
calling an edit done.

## Measuring exact per-bullet height (for a big trim)

```
python3 scripts/measure_layout.py resume_mle.tex
python3 scripts/measure_layout.py resume_mle.tex --suggest-cuts --overflow-in 0.4
```

When a profile needs real trimming (not just a one-line fix), this reports
the *exact* height (via pdfTeX's own `\pdfsavepos`/`\pdflastypos`, not a
pixel estimate) of every bullet and section, so you can see precisely which
bullets are the biggest space cost before deciding what to cut.
`--suggest-cuts --overflow-in <n>` (get `<n>` from `check_resume.py`'s
"extra slack" or from `11 - trailing` on the overflow page) ranks bullets
largest-first and shows a running total of how much cutting closes a given
overflow — a starting point to apply real content judgment against (per
CLAUDE.md's cutting-priority rules), not a decision to apply blindly.

**Validated, and validated to have a real limit**: predicting a whitespace
change from removing an item on the *last* page matched a real recompile
almost exactly. Predicting *across* a page break does not work by
arithmetic alone — removing earlier content can pull material back from
the next page (a real, non-linear `\needspace`-driven TeX reflow effect),
so a cut that crosses a page boundary needs `check_resume.py` re-run
afterward to confirm the actual result. See the script's module docstring
for the specific numbers from that test.

## Finding a minimal, verified fix when a profile is over one page

```
python3 scripts/autofit.py resume_mle.tex               # dry run: reports the plan
python3 scripts/autofit.py resume_mle.tex --apply        # writes it, then re-read/recompile
python3 scripts/autofit.py resume_mle.tex --floor-in 0.5 # override the margin floor (default 0.5in)
```

Searches for a combination of (margin reduction, bullets cut) that brings
a file back to one page — but unlike a prediction, every candidate is
verified by an actual compile, so it's robust across the page-break
non-linearity `measure_layout.py` can't predict through. Policy: margin
room down to the floor is used first since it costs no content (skipped
entirely if the file's margin is already at/below the floor — true for
all five profiles as of this writing); only once that's exhausted does it
search content cuts, ranked largest-first by `measure_layout.py`'s exact
heights purely to keep the search efficient — that ranking is not a
content-value judgment, review the proposed cut list against CLAUDE.md's
cutting-priority rules before using `--apply`. Each file's margin is read
from and written back to that file's own geometry block independently —
nothing here shares a margin value across profiles. Validated end-to-end
against three real, controlled scenarios (margin already at floor →
content-only; margin insufficient alone → margin maxed + minimal cuts on
top; margin alone sufficient → zero cuts) before being trusted.

## Setup: LaTeX + VS Code rendering (macOS)

Steps to get the `.tex` files compiling and previewing inside VS Code's LaTeX Workshop extension on a fresh Mac.

### 1. Check current state first

```
which pdflatex tlmgr latexmk
defaults read /Applications/Visual\ Studio\ Code.app/Contents/Info.plist CFBundleShortVersionString
```

If `pdflatex`/`tlmgr` are missing, do step 2. If VS Code isn't in `/Applications` (e.g. still in `~/Downloads`), do step 4 — this matters, don't skip it.

### 2. Install BasicTeX (needs an interactive Terminal — sudo password prompt, can't be scripted non-interactively)

```
brew install --cask basictex
```

### 3. Install the LaTeX packages this resume needs, plus latexmk (also needs sudo — run in Terminal)

```
export PATH=/Library/TeX/texbin:$PATH
sudo tlmgr update --self
sudo tlmgr install latexmk titlesec tabularx xcolor enumitem fontawesome5 amsmath eso-pic calc bookmark lastpage changepage paracol ifthen needspace iftex lm charter
```

### 4. Make sure VS Code is in `/Applications`, not `~/Downloads`

If it's still in Downloads, it runs under **App Translocation** (a macOS quarantine quirk) which silently breaks extension webviews — this caused a blank PDF preview the first time around. Quit VS Code, drag the app from Downloads into `/Applications`, relaunch from there.

### 5. Update VS Code itself

LaTeX Workshop's current release needs VS Code **≥1.114.0**. In VS Code: **Code menu → Check for Updates...**, let it download, restart when prompted.

### 6. Install/update the LaTeX Workshop extension

Extensions panel (Cmd+Shift+X) → search "LaTeX Workshop" (`james-yu.latex-workshop`) → Install or Update → reload window.

If an update leaves a stale old version folder behind causing a "Cannot read the extension" scan error, delete the old one:

```
ls ~/.vscode/extensions | grep latex-workshop
rm -rf ~/.vscode/extensions/james-yu.latex-workshop-<OLD_VERSION>
```

### 7. Verify compile works from the CLI (sanity check, no GUI needed)

```
export PATH=/Library/TeX/texbin:$PATH
cd "<path to Resume repo>"
latexmk -pdf -aux-directory=.build -emulate-aux-dir -interaction=nonstopmode resume_mle.tex
```

Should produce a 1-page `resume_mle.pdf` in the repo root with no errors. The `-aux-directory=.build` flag keeps `.aux`/`.log`/`.fls`/etc. out of the root directory entirely (tucked into a gitignored `.build/` folder) instead of cluttering `ls`/Finder. Same command applies to `resume_swe.tex`, `resume_pm.tex`, and `resume_research.tex`; `cv_master.tex` has no page-count requirement. VS Code's LaTeX Workshop is already configured (see `.vscode/settings.json`) to build the same way.

### 8. Use it in VS Code

- Open the `.tex` file you're editing and make sure its tab is **focused** (not the LaTeX Workshop output panel) before running build/view commands.
- Save (Cmd+S) to auto-build, or Cmd+Shift+P → "LaTeX Workshop: Build LaTeX project".
- Click the preview icon (top-right of editor) to view the PDF in-editor.

### Fallback if the in-editor preview still shows blank/grey with "0/0 pages"

Check the real error via Cmd+Shift+P → "Developer: Open Webview Developer Tools" → Console tab, while the PDF panel is focused. If it's a PDF.js bug (`hashOriginal.toHex is not a function` or similar), updating the extension (step 6) usually fixes it. If not, force the browser viewer instead by adding to `.vscode/settings.json` in the repo:

```json
{
    "latex-workshop.view.pdf.viewer": "browser"
}
```
