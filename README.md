# resume

LaTeX source for Arjun Nanduri's resume. See `CLAUDE.md` for the content strategy and editing guidelines.

## Files

- `cv_master.tex` — verbose superset, every bullet, no page limit. Never sent out; the reservoir the other two are cut from. Named `cv_` rather than `resume_` since it's not a resume at all — it's the unbounded reference document.
- `resume_mle.tex` — one-page, ML/CV-emphasis. Sendable.
- `resume_swe.tex` — one-page, SWE/Founder-emphasis. Sendable.

All three share the same preamble/macros — content differs, formatting does not.

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

Should produce a 1-page `resume_mle.pdf` in the repo root with no errors. The `-aux-directory=.build` flag keeps `.aux`/`.log`/`.fls`/etc. out of the root directory entirely (tucked into a gitignored `.build/` folder) instead of cluttering `ls`/Finder. Same command applies to `resume_swe.tex`; `cv_master.tex` has no page-count requirement. VS Code's LaTeX Workshop is already configured (see `.vscode/settings.json`) to build the same way.

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
