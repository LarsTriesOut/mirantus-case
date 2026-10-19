# 00 Run log

Summary: Preflight checksums of all inputs per run, start step, and what each step produced.
Inputs used: all files in `data/`.
Rerun rule: see dependency table in `README.md`.

## Run 2026-10-19 (no argument)
Previous run: none (first run). Start step: 0 → all steps.

| File | shasum |
|---|---|
| data/README.md | b853ea1bdf031507d60ca0a513486b4134988d54 |
| data/constraints.md | 8b924d3f7187cccdba6ea7e795792700fd60e1b1 |
| data/customer-journey.md | 107abf2748cd1e793f157064d453392e42c6f35e |
| data/interviews/01-customer-leipzig.md | 842525bee70b1b00e529c1f25996bdb5c64aa7ec |
| data/interviews/02-customer-berlin.md | 8d3b52fbdb1805865946bf11f11f9d5cdc1a0c4d |
| data/interviews/03-optician-bavaria.md | 2aa56b86453d49f97c9faab86794b77c369a3237 |
| data/interviews/04-ophthalmologist.md | afdf38ebc7bf664432e93c83cb75b3dbe7d7f675 |
| data/optician-survey.md | 0dcd0c8562798c5ecf8b307633adabc22471902f |
| data/screenings.csv | 5779def58bf08c8277539cb5c470efa7ac6cdaa0 (9,000 rows + header) |
- Step 3: 03-insights.md written; critic PASS WITH FIXES (22 issues), all fixed; script extended (§5 result×age, 40+ cuts; §9 open≤5d, 60+×follow-up, consent 40+, MDE). Setup gap: critic has no Write tool, so the main session saved its review verbatim.
- CP1 (Lars): primary metric = 15-month return rate, non-referral 40+ (baseline 5.5%, n=2,452); build on I2–I7 (all four groups); nothing missing.
- Step 4: 04-options.md written; critic PASS WITH FIXES (15 issues), all fixed; removed an assumed 'partner portal' (not in data); added 40+ cuts to script §9. Metric-vs-intervention conflict raised at CP2.
- CP2 (Lars): option B with fallback A; pilot success = interval-adherent return (stated interval + 3 months); 15-month 40+ rate stays company trend.
- Step 5: 05-decision-memo.md written (446 words); critic PASS WITH FIXES (16 issues), all fixed; added referral_booked by location type to script.
- Step 6: 06-prototype-brief.md written; critic PASS WITH FIXES (15 issues), all fixed (fictional names + label, full-name salutation, minor-findings copy neutralised, consent/opt-in state precedence, reply-to, DE/EN parity).
- CP3 (Lars): prototype built in Claude Design; link saved in 07-prototype-link.md.

### Step 7 wrap-up
| Step | Output | Critic verdict |
|---|---|---|
| 1 | 01-data-findings.md, scripts/analyze.py, tables/ | no critic step (input to 3); addendum §9 extended during steps 3–5 |
| 2 | 02-research-synthesis.md | no critic step (input to 3) |
| 3 | 03-insights.md | PASS WITH FIXES (22), all fixed |
| 4 | 04-options.md | PASS WITH FIXES (15), all fixed |
| 5 | 05-decision-memo.md (446 words) | PASS WITH FIXES (16), all fixed |
| 6 | 06-prototype-brief.md | PASS WITH FIXES (15), all fixed |
| CP3 | 07-prototype-link.md | — |

Decisions: CP1 metric = 15-month return, non-referral 40+ (5.5%, n=2,452). CP2 = option B (interval in report + optician-named reminder), fallback A; pilot success = return within stated interval + 3 months.

Open issues:
- Legal: does consent cover optician-named reminders; is the report page a legitimate re-ask place; may the interval be repeated in the reminder; who is the controller.
- Medical: interval option set and template sentences need ophthalmologist sign-off; intervals may stay generic without risk-factor data.
- One quarter cannot prove a return lift (MDE ~4.4 pp at independents); the decision rests on leading indicators.
- Setup: the critic agent has no Write tool, so the main session saved its reviews (one pronoun corrected in the 04 review). The critic ran once per step; no re-check after fixes.
- Setup: the step-1 script was extended by the main session in steps 3–5 rather than by the data-analyst agent.
