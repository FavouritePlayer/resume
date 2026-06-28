# CLAUDE.md — Resume Repo

Context for working on Arjun's resume. Read this fully before editing the `.tex`.

## Who this is for

Arjun Nanduri — rising junior, UC Berkeley CS/CDSS, GPA 3.972, grad May 2027. Currently SWE intern at Aver (computer vision pipeline, PyTorch). Strong shipper: cuts scope under pressure, leads scrappy teams from nothing, CalHacks prize. Real technical range across CV, NLP, agentic/full-stack.

## The goal driving this resume

Two tailored profiles off one base of facts. Same truth, different ordering and emphasis:

1. **ML / CV profile** — proves *technical acumen*. Leads with depth signal: BART low-resource NLP work, Aver CV pipeline, MuJoCo RL, PyTorch. Demotes web/mobile history.
2. **SWE / Founder profile** — proves *shipping*. Leads with PotBot (won, led 3, shipped working demo in 36h over feature-completeness), full-stack range, ownership decisions. Technical depth appears as supporting evidence, not the headline.

Near-term target: **a computer-vision research position for Fall 2026.** This is about building skill in the vision direction, not collecting a prestige label. Research roles screen on research signal (a defensible result vs. a baseline), not polish — so the ML/CV profile must foreground anything with a measurable result.

Self-understanding to respect: *Founder = shipping, not technical depth. But depth isn't dead — the resume should display enough technical acumen to be credible.* Don't overclaim depth; do make the real depth legible.

## Required changes (agreed, non-negotiable)

- **Add PyTorch to Skills.** It's currently missing and it's the single most important framework for these roles. He uses it at Aver.
- **Deepen the BART / CDSS bullet** with real technical teeth: what the custom distance metric was, corpus/dataset scale, why low-resource matters. This is his strongest research-shaped line — the template is "custom metric beat open-source baseline by 15%."
- **Cut the certifications line entirely.** Inspirit "AI Scholar" actively hurts (reads as padding); Azure AI Fundamentals and Bloomberg are noise for ML roles.
- **Drop the SAT (1590).** Reads high-school for a junior with internships and a prize. Keep the GPA.
- **Trim pure-SWE history.** IT Hired Guns (gas-station loyalty apps) and Floras (carbon app) to one line each or cut. They dilute the ML narrative and eat the one-page budget. CACI can compress.
- **Kill fluff bullets.** Remove "aligning with data-driven sustainability goals" and "scalable, production-ready codebases that enhanced user retention and data visibility for client partners." Replace with a metric or delete.
- **MuJoCo line:** add once the baseline actually runs and there's a result to state. Don't list as "in progress." (RL — proves general depth, not vision specifically; for the CV-research target a focused CV project with a defensible result may serve better. Open fork.)

## Phrasing principles

- Every bullet leads with an action verb and lands a concrete result or decision. No process-description without outcome.
- Quantify where real; delete where not. A vague metric is worse than none.
- Cut adjectives that don't carry information ("scalable," "production-ready," "robust") unless backed by a number.
- One page, hard constraint. Density over whitespace. Compile and visually verify it's one page before declaring done.
- Clean, single-column, no color, ATS-readable, recruiter-skimmable in 10 seconds. The ML profile's top third must surface ML signal (PyTorch, BART, CV, results) above the web/mobile work.
- For the ML/CV profile, the interview these resumes target is project-depth-driven ("tell me about the hardest thing you built") — so bullets should give him something deep to talk about, not just list tools.

## Workflow

- Edit the `.tex` directly. Compile with local MacTeX, read the rendered PDF, iterate against real output until it's clean and one page.
- Maintain both profiles as separate `.tex` files (e.g. `resume_ml.tex`, `resume_swe.tex`) sharing the same factual base.
- Push after each working session.
