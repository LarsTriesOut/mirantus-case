---
description: Run the Mirantus case pipeline end to end, or from a given step (e.g. /run-case from 4)
argument-hint: "[from <step>]"
---
Run the pipeline below. Arguments: $ARGUMENTS

Follow CLAUDE.md throughout. Never skip a checkpoint (✋).
- No argument: start at step 0 and run everything.
- `from 1`: rerun only the data-analyst (keep `02`), then continue at step 3.
- `from 2`: rerun only the research-synthesizer (keep `01`), then continue at step 3.
- `from N` (N ≥ 3): read the existing outputs of earlier steps first, then start at step N.
Always run step 0 first, whatever the argument.

## Step 0: Preflight → `outputs/00-run-log.md`
- List all files in `data/` and compute checksums (`shasum`). Compare with the last entry in
  `outputs/00-run-log.md`, if it exists.
- Report which inputs changed and, using the dependency table in `README.md`, which steps must
  rerun. If no `from` argument was given and earlier outputs exist, propose the start step and ask
  Lars before continuing.
- Append a run entry: date, inputs with checksums, start step.

## Steps 1 + 2 (in parallel)
- Launch the `data-analyst` subagent → `outputs/01-data-findings.md`.
- Launch the `research-synthesizer` subagent → `outputs/02-research-synthesis.md`.
- Wait for both, then read both files in full.

## Step 3: Insight synthesis → `outputs/03-insights.md`
- Max. 7 insights. Each: statement, quantitative evidence (n and window), qualitative evidence
  (quotes with source), confidence, so-what for the return metric.
- The proposed return metric: definition, window, who is in and out, current baseline, and a
  leading indicator.
- What we don't know, and where data and voices disagree.
- Run the `critic` on it and fix what it flags.
- ✋ CP1: show a short summary and ask Lars: approve the metric definition? Which insights to build on? Anything missing?

## Step 4: Options → `outputs/04-options.md`
- Frame the problem in one sentence: who, at which moment, why they don't come back.
- 3 materially different options, including the smallest viable one. Compare in a table: effect on
  the metric (evidence), reach (customers legally contactable), constraint fit, effort for the
  squad, riskiest assumptions.
- Recommend one: what ships first, what is cut.
- Run the `critic` and fix what it flags.
- ✋ CP2: ask Lars which option to take forward (he may combine or change).

## Step 5: Decision memo → `outputs/05-decision-memo.md`
- Max. 1 page (≤ 450 words): problem, recommendation, what ships first, what is cut and why,
  success metric + guardrails (incl. the leading indicator), how to test with real users in the
  next two weeks (who, how many, what we learn, kill criteria).
- Run the `critic`, fix all issues, re-check the word count.

## Step 6: Prototype brief → `outputs/06-prototype-brief.md`
- The one flow that matters most for the recommendation: screens / states in order, the actor in
  each, exact copy (consent, optician's name, interval only from the ophthalmologist, no fear),
  edge cases, and what is deliberately left out.
- End with a self-contained prompt Lars can paste into Claude Design to build the clickable prototype.
- Run the `critic` on the copy and fix what it flags.
- ✋ CP3: ask Lars to build the prototype in Claude Design and paste the link into
  `outputs/07-prototype-link.md`. Wait for him.

## Step 7: Wrap-up
- Add to `outputs/00-run-log.md`: what each step produced, critic verdicts, open issues.
- Remind Lars that `verdict.md` is his to write. Don't write it.
