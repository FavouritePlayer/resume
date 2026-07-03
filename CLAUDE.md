# CLAUDE.md — Resume Repo

Context for working on Arjun's resume. Read this fully before editing any `.tex`.

## Who this is for

Arjun Nanduri — rising junior, UC Berkeley CS/CDSS, GPA 3.972, grad May 2027. Currently Machine Learning Engineer at Aver (computer vision pipeline, PyTorch). Strong shipper: cuts scope under pressure, leads scrappy teams from nothing, CalHacks prize. Real technical range across CV, NLP, agentic/full-stack.

## File structure — one master + N specialized profiles

1. **`resume_master.tex`** — verbose superset, **as complete as possible.** Every bullet, every project, every piece of real detail that exists should live here — full technical mechanism, real numbers, full history, no trimming for space. NO page limit, and none should ever be imposed on it. **Never sent out.** This is the reservoir every specialized profile cuts from. When a role needs a bullet that was trimmed from a profile, pull it from here instead of rewriting from memory. Keep it complete and current — anything true and relevant belongs in the master even if no profile currently uses it.
2. **`resume_mle.tex`** — ONE PAGE. ML / CV emphasis. Sendable.
3. **`resume_swe.tex`** — ONE PAGE. SWE / Founder emphasis. Sendable.

These two (`_mle`, `_swe`) are the specialized profiles that exist today, not a hard ceiling — **more specialized profiles may be added later** (e.g. a data-science-specific cut, a new-grad full-time version, a role-specific one-off). Every specialized profile, current or future, follows the same rule: it is a filtered, reordered, one-page view of the master, never an independently drafted document.

**Duplication rule:** every specialized profile shares the SAME preamble, formatting, fonts, and macros as the master. Each is a *filtered, reordered view* of the master's content — not an independently styled document. If a formatting/layout change is made, apply it consistently across master + every specialized profile (ideally edit a shared style and mirror it). Content differs per profile; look does not.

## One-page policy

- **Every specialized profile is hard one page.** This applies to `_mle`, `_swe`, and any specialized profile added in the future — no exceptions. For an undergrad with no PhD, a multi-page applied/SWE resume reads as not knowing the convention; recruiters skim page one anyway. The one-page constraint is what forces the weak bullets out — that's the point.
- **`resume_master.tex` is the opposite: intentionally unbounded and as verbose as possible.** It should contain everything — it's the superset, never sent, never trimmed for length. More detail in the master is always better; the page limit only applies once content is filtered into a specialized profile.
- Compile and **visually verify** each specialized profile is actually one page before declaring it done. Do not trust line counts; read the rendered PDF.

## The specialized profiles (currently two)

**`resume_mle.tex` — ML / CV — proves technical acumen.**
Leads with depth signal: BART low-resource NLP work, Aver CV pipeline, MuJoCo RL, PyTorch. Web/mobile history demoted to one line or cut. Top third of page one must surface ML signal (PyTorch, BART, CV, measurable results) above everything else.

**`resume_swe.tex` — SWE / Founder — proves shipping.**
Leads with PotBot (won CalHacks prize, led team of 3, shipped working SF demo in 36h over an unfinished feature set — the founder signal stated perfectly), full-stack range, ownership/scoping decisions. Technical depth appears as supporting evidence, not the headline.

Same facts in both — different ordering, emphasis, and which bullets are included.

## Near-term target

A **computer-vision research position for Fall 2026** is the live goal — about building skill in the vision direction, not collecting a prestige label. Research roles screen on a *defensible result vs. a baseline*, not polish, so `resume_mle.tex` must foreground anything with a measurable outcome. The interview these target is project-depth-driven ("tell me about the hardest thing you built"), so bullets should give him something deep to talk about, not just list tools.

Self-understanding to respect: *Founder = shipping, not technical depth. But depth isn't dead — show enough technical acumen to be credible.* Don't overclaim depth; do make the real depth legible.

## Required changes (agreed, apply to master + both profiles as relevant)

- **Add PyTorch to Skills.** Currently missing; the single most important framework for these roles. He uses it at Aver.
- **Deepen the BART / CDSS bullet** with real technical teeth: what the custom distance metric was, corpus/dataset scale, why low-resource matters. His strongest research-shaped line. Template: "custom metric beat open-source baseline by 15%."
- **Cut the certifications line entirely.** Inspirit "AI Scholar" actively hurts (padding); Azure Fundamentals and Bloomberg are noise for ML roles.
- **Drop the SAT (1590).** Reads high-school for a junior with internships and a prize. Keep GPA.
- **Trim pure-SWE history.** IT Hired Guns (gas-station loyalty apps) and Floras (carbon app) to one line each or cut on the profiles (keep full in master). CACI compress.
- **Kill fluff bullets.** Remove "aligning with data-driven sustainability goals" and "scalable, production-ready codebases that enhanced user retention and data visibility for client partners." Replace with a metric or delete.
- **MuJoCo line:** add once the baseline runs and there's a result to state. Don't list as "in progress." (RL proves general depth, not vision specifically; for the CV-research target a focused CV project with a defensible result may serve better — OPEN FORK, Arjun decides, don't auto-resolve.)

## Unresolved questions — need answers from Arjun before deepening bullets

Do NOT invent technical detail for these. Bullets stay as currently written (vague-but-true) until answered.

1. **Aver CV pipeline** — what's the actual task: object detection, segmentation, or OCR/keypoint extraction on the pile markings? What model/architecture is it built on (specific CNN/ViT backbone, YOLO variant, fine-tuned existing detector)? Currently the bullet just says "computer vision pipeline in PyTorch" with no task or architecture named.
2. **BART custom distance metric** — what did it actually compute? (e.g. edit-distance over lemma forms, embedding-space distance, a phonological/morphological similarity score?) "Custom distance metric" with no mechanism is unfalsifiable in a depth interview.
3. **ORACC corpus scale** — how many tokens/lemmas/texts did the fine-tuning set actually contain? A real number turns "low-resource" from a claim into a quantified, defensible setup.

Once answered, fold the full detail into `resume_master.tex` first (no trimming — that's what the master is for), then propagate a page-appropriate cut to each specialized profile (`resume_mle.tex`/`resume_swe.tex`, and any future ones) as relevant.

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