# Mirantus product case: Claude setup

A small, rerunnable Claude Code setup that turns the Mirantus data pack into an insight synthesis,
a one-page decision memo and a prototype brief, with a red-team check before every human checkpoint.

## Structure
```
CLAUDE.md                      the brief: goal, users, sources of truth, what good looks like, never-do, checkpoints
.claude/commands/run-case.md   the pipeline (/run-case)
.claude/agents/                data-analyst, research-synthesizer, critic (read-only red team)
.claude/settings.json          permissions so routine commands don't stall the run
data/                          inputs: the synthetic data pack
docs/case-brief.md             the original task
scripts/analyze.py             written by the data-analyst; reproduces every number
outputs/                       00 run log … 07 prototype link, reviews/, tables/
transcripts/                   exported Claude sessions
verdict.md                     my own review (not written by Claude)
```

## Run it
Requirements: Claude Code and Python 3 (pandas optional).
```
cd <this repo>
claude
/run-case
```
The run stops at three checkpoints: CP1 metric and insights, CP2 direction, CP3 prototype in Claude Design.

## Rerun after an input changes
Change the file in `data/` (or `CLAUDE.md`), then run `/run-case`. Step 0 compares checksums with
the last run, shows what changed and proposes where to restart. To force a start: `/run-case from <step>`.

| What changed | Start with | Steps that rerun | Why |
|---|---|---|---|
| `data/screenings.csv` | `from 1` | 1 → 3 → 4 → 5 → 6 | numbers, baseline and segments change |
| interviews, survey, customer journey | `from 2` | 2 → 3 → 4 → 5 → 6 | qualitative evidence changes |
| `data/constraints.md` (consent, medical, ownership, capacity) | `from 4` | 4 → 5 → 6 | evidence stays; what is allowed and feasible changes. The critic re-reads constraints every time |
| goal or metric rules in `CLAUDE.md` | `from 3` | 3 → 4 → 5 → 6 | framing changes |
| prototype scope only | `from 6` | 6 | |

If the change is ambiguous, run `/run-case` without arguments and let step 0 decide.

## What the run produced
- Insight synthesis: `outputs/03-insights.md`
- Decision memo: `outputs/05-decision-memo.md`
- Prototype: brief `outputs/06-prototype-brief.md`, link `outputs/07-prototype-link.md`
- Critic reviews: `outputs/reviews/`
- Transcripts: `transcripts/`
- My verdict: `verdict.md`
