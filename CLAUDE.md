# CLAUDE.md — Resume Repo

Context for working on Arjun's resume. Read this fully before editing any `.tex`.

## Who this is for

Arjun Nanduri — rising junior, UC Berkeley CS/CDSS, GPA 3.972, grad May 2027. Currently Machine Learning Engineer at Aver (computer vision pipeline, PyTorch). Strong shipper: cuts scope under pressure, leads scrappy teams from nothing, CalHacks prize. Real technical range across CV, NLP, agentic/full-stack.

## File structure — one master + N specialized profiles

1. **`cv_master.tex`** — verbose superset, **as complete as possible.** Named `cv_` rather than `resume_` deliberately: it isn't a resume, it's never sent, and calling it one invited confusion. Every bullet, every project, every piece of real detail that exists should live here — full technical mechanism, real numbers, full history, no trimming for space. NO page limit, and none should ever be imposed on it. **Never sent out.** This is the reservoir every specialized profile cuts from. When a role needs a bullet that was trimmed from a profile, pull it from here instead of rewriting from memory. Keep it complete and current — anything true and relevant belongs in the master even if no profile currently uses it.
2. **`resume_mle.tex`** — ONE PAGE. ML / CV emphasis. Sendable.
3. **`resume_swe.tex`** — ONE PAGE. SWE / Founder emphasis. Sendable.

These two (`_mle`, `_swe`) are the specialized profiles that exist today, not a hard ceiling — **more specialized profiles may be added later** (e.g. a data-science-specific cut, a new-grad full-time version, a role-specific one-off). Every specialized profile, current or future, follows the same rule: it is a filtered, reordered, one-page view of the master, never an independently drafted document.

**Duplication rule:** every specialized profile shares the SAME preamble, formatting, fonts, and macros as the master. Each is a *filtered, reordered view* of the master's content — not an independently styled document. If a formatting/layout change is made, apply it consistently across master + every specialized profile (ideally edit a shared style and mirror it). Content differs per profile; look does not.

## One-page policy

- **Every specialized profile is hard one page.** This applies to `_mle`, `_swe`, and any specialized profile added in the future — no exceptions. For an undergrad with no PhD, a multi-page applied/SWE resume reads as not knowing the convention; recruiters skim page one anyway. The one-page constraint is what forces the weak bullets out — that's the point.
- **`cv_master.tex` is the opposite: intentionally unbounded and as verbose as possible.** It should contain everything — it's the superset, never sent, never trimmed for length. More detail in the master is always better; the page limit only applies once content is filtered into a specialized profile.
- Compile and **visually verify** each specialized profile is actually one page before declaring it done. Do not trust line counts; read the rendered PDF.

## The specialized profiles (currently two)

**`resume_mle.tex` — ML / CV — proves technical acumen.**
Leads with depth signal: BART low-resource NLP work, Aver CV pipeline, `ant_sim` PPO/MuJoCo quadruped-locomotion project, PyTorch. Web/mobile history demoted to one line or cut. Top third of page one must surface ML signal (PyTorch, BART, CV, measurable results) above everything else.

**`resume_swe.tex` — SWE / Founder — proves shipping.**
Leads with PotBot (won CalHacks prize, led team of 3, shipped working SF demo in 36h over an unfinished feature set — the founder signal stated perfectly), plus two more recent hackathon agent projects (`DealScout` — resale-arbitrage agent, LangGraph/Playwright/HydraDB; `ContextCustodian` — workspace-hygiene agent, FastAPI/Scalekit), full-stack range, ownership/scoping decisions. Technical depth appears as supporting evidence, not the headline.

Same facts in both — different ordering, emphasis, and which bullets are included. Travel Tracker Web App and the Chinese Web Novel Translator were cut from the one-pagers to make room for these (still live in full in `cv_master.tex` — pull them back if a specific role calls for them).

## Near-term target

A **computer-vision research position for Fall 2026** is the live goal — about building skill in the vision direction, not collecting a prestige label. Research roles screen on a *defensible result vs. a baseline*, not polish, so `resume_mle.tex` must foreground anything with a measurable outcome. The interview these target is project-depth-driven ("tell me about the hardest thing you built"), so bullets should give him something deep to talk about, not just list tools.

Self-understanding to respect: *Founder = shipping, not technical depth. But depth isn't dead — show enough technical acumen to be credible.* Don't overclaim depth; do make the real depth legible.

`ant_sim` resolves the MuJoCo-vs-CV-project fork noted below: it's RL, not CV, but it clears the "defensible result vs. baseline" bar cleanly (control/treatment comparisons across matched seeds, honestly-reported negative results, multi-seed replication) and is on `resume_mle.tex` now. If a sharper CV-specific project with its own baseline comparison comes together later, evaluate swapping it in — don't assume `ant_sim` is permanent just because it's the current occupant.

## Known gaps / things to keep honest

- **ORACC corpus scale** (`cv_master.tex`, CDSS bullet) is a published ORACC-wide estimate ($\sim$1M words / $\sim$10K texts), not verified against Arjun's specific fine-tuning subset — flagged with a `% TODO(Arjun)` comment in the master `.tex`. Confirm before this number goes out on a profile that hasn't been checked against it.
- **DealScout / ContextCustodian** have no quantified outcome metric (no eval numbers, no before/after) — bullets sell the mechanism and engineering judgment, not a result. Don't force a fake metric onto either.

## Phrasing principles

- Every bullet leads with an action verb and lands a concrete result or decision. No process-description without outcome.
- Quantify where real; delete where not. A vague metric is worse than none.
- Cut adjectives that carry no information ("scalable," "production-ready," "robust") unless backed by a number.
- Recruiter-skimmable in 10 seconds. Clean, single-column, no color, ATS-readable.

## Workflow

- Edit `.tex` directly. Compile with local MacTeX, read the rendered PDF, iterate against real output until clean and (for specialized profiles) one page.
- Keep the master as complete and verbose as possible; derive every specialized one-pager from it by cutting, not by drafting fresh.
- **Orphan-line check (mandatory after any edit that changes wrapping):** after compiling, render each page to an image and read every bullet's line breaks specifically — not just the page count. Look for any line where only one or two words spill onto their own line (a "widow"/orphan). These waste a full line of vertical space and read as sloppy. Fix by trimming a redundant word/clause from that bullet (don't pad neighboring bullets to compensate) and recompile. Do this for every bullet, not just the ones that look long — short bullets can still orphan a word depending on column width.
- Push after each working session.