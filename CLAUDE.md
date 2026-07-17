# CLAUDE.md — Resume Repo

Context for working on Arjun's resume. Read this fully before editing any `.tex`.

## Who this is for

Arjun Nanduri — rising junior, UC Berkeley CS/CDSS, GPA 3.9, grad May 2028. Currently Machine Learning Engineer at Aver (computer vision pipeline, PyTorch). Strong shipper: cuts scope under pressure, leads scrappy teams from nothing, CalHacks prize. Real technical range across CV, NLP, agentic/full-stack.

## File structure — one master + N specialized profiles

1. **`cv_master.tex`** — verbose superset, **as complete as possible.** Named `cv_` rather than `resume_` deliberately: it isn't a resume, it's never sent, and calling it one invited confusion. Every bullet, every project, every piece of real detail that exists should live here — full technical mechanism, real numbers, full history, no trimming for space. NO page limit, and none should ever be imposed on it. **Never sent out.** This is the reservoir every specialized profile cuts from. When a role needs a bullet that was trimmed from a profile, pull it from here instead of rewriting from memory. Keep it complete and current — anything true and relevant belongs in the master even if no profile currently uses it.
2. **`resume_mle.tex`** — ONE PAGE. ML / CV emphasis. Sendable.
3. **`resume_swe.tex`** — ONE PAGE. SWE / Founder emphasis. Sendable.
4. **`resume_pm.tex`** — ONE PAGE. Product management emphasis. Sendable.

These profiles (`_mle`, `_swe`, `_pm`) are the specialized profiles that exist today, not a hard ceiling — **more specialized profiles may be added later** (e.g. a data-science-specific cut, a new-grad full-time version, a role-specific one-off). Every specialized profile, current or future, follows the same rule: it is a filtered, reordered, one-page view of the master, never an independently drafted document.

**Duplication rule:** every specialized profile shares the SAME preamble structure, fonts, and macros as the master — the same packages, the same named environments (`highlights`, `twocolentry`, etc.), the same overall visual style. Each is a *filtered, reordered view* of the master's content — not an independently styled document. If a structural/mechanism change is made (a new environment, a font change, a different bullet style), apply it consistently across master + every specialized profile.

**Exception — spacing/margin values are tuned per profile, not shared.** Page margins, `\titlespacing`, the entry-gap `\vspace`, and bullet `itemsep`/`parsep` may differ between `resume_mle.tex` and `resume_swe.tex` (and any future profile), since each has different content density. Only the underlying macros/structure stay shared; content differs per profile, and so does spacing.

**Don't chase "page fullness" as a goal — it isn't one.** Recruiters scan for content (results, keywords, structure), not for whether a page runs to the bottom margin; a resume that looks stretched to avoid whitespace reads worse, not better. Concrete rule of thumb:
- Keep margins in the normal range (~0.5–0.75in). If a profile already lands with modest trailing whitespace (roughly 10–15% of the page or less), leave it — that's normal and clean, not a defect to fix.
- Only if the empty space is conspicuously large (e.g., the bottom quarter of the page is blank) does it make sense to trim the bottom margin slightly to rebalance — and even then, not so much that the margins look noticeably tighter than a normal template.
- Never loosen line/section spacing specifically to erase whitespace once margins are already normal — that's optimizing for an appearance metric nobody is evaluating, and it risks looking padded. (Loosening spacing *for legibility* — because bullets read as cramped — is a legitimate, different reason and is fine.)

## One-page policy

- **Every specialized profile is hard one page.** This applies to `_mle`, `_swe`, `_pm`, and any specialized profile added in the future — no exceptions. For an undergrad with no PhD, a multi-page applied/SWE resume reads as not knowing the convention; recruiters skim page one anyway. The one-page constraint is what forces the weak bullets out — that's the point.
- **`cv_master.tex` is the opposite: intentionally unbounded and as verbose as possible.** It should contain everything — it's the superset, never sent, never trimmed for length. More detail in the master is always better; the page limit only applies once content is filtered into a specialized profile.
- Compile and **visually verify** each specialized profile is actually one page before declaring it done. Do not trust line counts; read the rendered PDF.

## The specialized profiles (currently three)

**`resume_mle.tex` — ML / CV — proves technical acumen.**
Leads with depth signal: BART low-resource NLP work, Aver CV pipeline, `ant_sim` PPO/MuJoCo quadruped-locomotion project, PyTorch. Web/mobile history demoted to one line or cut. Top third of page one must surface ML signal (PyTorch, BART, CV, measurable results) above everything else.

**`resume_swe.tex` — SWE / Founder — proves shipping.**
Leads with PotBot (retitled to "PotBot — Civic Reporting Agent" so the title matches what the project actually does — it validates infrastructure damage photos and auto-submits repair requests to SF city government, not a "survey browser"; won CalHacks prize, led team of 3, shipped working SF demo in 36h over an unfinished feature set — the founder signal stated perfectly), plus `DealScout` (resale-arbitrage agent) and `ContextCustodian` (workspace-hygiene agent) condensed to one bullet each — sponsor-specific tech names (HydraDB, Scalekit) were dropped since they're not real engineering decisions, keeping only the portable skill/judgment each bullet demonstrates. `ant_sim` (Quadruped Locomotion with PPO) also lives here now, reframed around testing discipline (automated regression-test suite, multi-seed replication) rather than RL metrics, so it reads as engineering rigor rather than a second technical-depth headline competing with `resume_mle.tex`.

**`resume_pm.tex` — Product Management — proves product judgment.**
Targets PM internships (fintech, e.g. Capital One). Governing principle: PM resumes emphasize leadership, user contact, decisions under uncertainty, and impact — not languages or features implemented, so the same underlying project is re-emphasized rather than re-invented. Metrics are kept but reattached to decisions, not implementations. Aver's field-interview bullet (user research directly changing model design decisions) leads Experience — it's the single strongest PM line available and was previously buried second. PotBot leads Projects, framed around the scoping call (ship a working demo over an unfinished feature set under a 36-hour deadline) rather than the CV mechanism. `ant_sim` leads with the negative-result story (validated a leg-damage policy, found it didn't transfer, killed that direction and built a router instead of shipping an unsupported claim) and keeps the 2.1x terrain-adaptation result as the supporting number, not the headline — "killing a direction on evidence" is the product-judgment signal, not the reward multiplier. `DealScout`/`ContextCustodian` are one line each (engineering-depth signal, lower product signal) — first in line to cut if a future edit needs the space. Adds ECON 101B (Macroeconomics) to Courses for fintech relevance. Skills demoted to the bottom and shortened (narrow RL-specific tools dropped) since a technical PM signal is a supporting asset here, not the headline.

Same facts across all three — different ordering, emphasis, and which bullets are included. Travel Tracker Web App and the Chinese Web Novel Translator are cut from all three one-pagers (still live in full in `cv_master.tex` — pull them back if a specific role calls for them).

## Near-term target

A **computer-vision research position for Fall 2026** is the live goal — about building skill in the vision direction, not collecting a prestige label. Research roles screen on a *defensible result vs. a baseline*, not polish, so `resume_mle.tex` must foreground anything with a measurable outcome. The interview these target is project-depth-driven ("tell me about the hardest thing you built"), so bullets should give him something deep to talk about, not just list tools.

Self-understanding to respect: *Founder = shipping, not technical depth. But depth isn't dead — show enough technical acumen to be credible.* Don't overclaim depth; do make the real depth legible.

`ant_sim` resolves the MuJoCo-vs-CV-project fork noted below: it's RL, not CV, but it clears the "defensible result vs. baseline" bar cleanly (control/treatment comparisons across matched seeds, honestly-reported negative results, multi-seed replication) and is on `resume_mle.tex` now. If a sharper CV-specific project with its own baseline comparison comes together later, evaluate swapping it in — don't assume `ant_sim` is permanent just because it's the current occupant.

## Known gaps / things to keep honest

- **ORACC corpus scale** (`cv_master.tex`, CDSS bullet) is a published ORACC-wide estimate ($\sim$1M words / $\sim$10K texts), not verified against Arjun's specific fine-tuning subset — flagged with a `% TODO(Arjun)` comment in the master `.tex`. Confirm before this number goes out on a profile that hasn't been checked against it.
- **DealScout / ContextCustodian** have no quantified outcome metric (no eval numbers, no before/after) — bullets sell the mechanism and engineering judgment, not a result. Don't force a fake metric onto either.

## Traceability rule (hard requirement)

**Every bullet on every specialized profile must trace to real content in `cv_master.tex`.** Reframing, reordering, compressing, and merging two real bullets into one are all fine — inventing a fact, a qualifier, or a characterization that isn't in the source is not, even if it sounds plausible or is individually minor (a single invented adjective is enough to break this — see the "personalized" incident below).

- If a profile needs a rewritten framing (e.g. leading with a decision instead of a mechanism, recasting an ML metric as a product-judgment story), do the reframing — but the underlying facts, numbers, and claims must still be the ones already in the master. Don't add a new specific (a client characterization, a causal claim, a descriptive word) that isn't already stated or directly derivable from the master text.
- If a specialized profile needs content the master doesn't have, either (a) pull it from the master's fuller version of that same bullet if one exists, or (b) **ask the user rather than writing something plausible.** Do not fill a gap with an invented-but-reasonable-sounding detail.
- If a reframing gets explicitly approved for one profile (e.g. a rewritten project description), consider updating `cv_master.tex` to match, so the framing has a real source and every future profile can trace to it cleanly — don't leave the master as the only un-updated, stale version.
- **After any edit to a specialized profile that touches bullet wording, diff every changed bullet against its source in `cv_master.tex`** before considering the edit done. This isn't optional cleanup — a resume with one invented fact is a real risk (interview questions probe specifics; recruiters cross-check), not a style nitpick.
- Real incident this rule exists because of: a rewrite of `resume_pm.tex`'s IT Hired Guns bullet changed master's "dynamic updates on nearby stations, fuel prices, and offers" to "personalized offers on nearby stations and fuel prices" — "personalized" was never stated anywhere and wasn't caught until an explicit audit. Small, plausible-sounding word substitutions are exactly what this rule is meant to catch.

## Phrasing principles

- Every bullet leads with an action verb and lands a concrete result or decision. No process-description without outcome.
- Quantify where real; delete where not. A vague metric is worse than none.
- Cut adjectives that carry no information ("scalable," "production-ready," "robust") unless backed by a number.
- Recruiter-skimmable in 10 seconds. Clean, single-column, no color, ATS-readable.
- **Bold exactly one phrase per bullet, in the specialized profiles only** — the concrete result (a number, a %, a multiplier) if the bullet has one, otherwise the single decision/mechanism that makes the bullet worth reading. Never more than one bolded span per bullet: over-bolding defeats the purpose, since a skimmer's eye needs somewhere specific to land. Use `\textbf{...}` inline. `cv_master.tex` stays unbolded — it's never shown to a reviewer, so there's nothing to guide a skimmer's eye toward.

## Workflow

- Edit `.tex` directly. Compile with local MacTeX using `latexmk -pdf -aux-directory=.build -emulate-aux-dir -interaction=nonstopmode <file>.tex` (never plain `pdflatex`/`xelatex` directly — that dumps `.aux`/`.log`/etc. into the repo root instead of the gitignored `.build/` folder). Read the rendered PDF, iterate against real output until clean and (for specialized profiles) one page. See `README.md` for full setup.
- Keep the master as complete and verbose as possible; derive every specialized one-pager from it by cutting, not by drafting fresh.
- **Orphan-line check (mandatory after any edit that changes wrapping, including adding bold spans):** after compiling, render each page to an image and read every bullet's line breaks specifically — not just the page count. Look for any line where only one or two words spill onto their own line (a "widow"/orphan). Bold text is slightly wider than regular text, so adding a bold span can introduce a new orphan on a line that was previously fine — always re-run this check after bolding, not just after content edits.
  When an orphan appears, resolve it in this order, not by reflexively cutting:
  1. **Page budget first.** If the profile is already over one page, the orphan gets fixed by cutting (a word, a clause, or a whole bullet) — a page-count violation outranks everything else, no exceptions.
  2. **Otherwise, judge the word/clause causing the wrap.** Is it genuinely redundant — already established elsewhere in the same job/project's other bullets, a filler adjective, a repeated qualifier — or is it real, distinguishing information (a number, a named cause, a specific decision)? Redundant → cut it, regardless of how much space exists. Real → don't cut it by default.
  3. **If it's real information and there's trailing whitespace below the last section** (room to spare on the page), prefer restoring or adding real, already-verified detail over deleting real content — check `cv_master.tex` first, since a profile bullet is often a trimmed-down cut of a fuller master bullet. The goal is a stronger bullet, not merely a full line: never pad with vague filler just to occupy space, and never invent a metric or specific that isn't already known/verified (this is the same rule as the "Known gaps" section below — it doesn't get relaxed just because there's room on the page).
  4. **If there's no real extra detail available and no room to spare**, cutting the word is still correct even if it's not strictly redundant — recruiters skim in ~10 seconds and won't miss one word, and a clean one-pager beats a technically-more-complete one that overflows or reads padded.
- Push after each working session.