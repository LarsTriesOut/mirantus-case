<!-- Written by the critic subagent (returned as text; it has no Write tool); saved by the main session. Only change: in issue 8 the critic's pronoun for interviewee 02 was replaced with "02", because the source uses a different one. -->
# Review: outputs/04-options.md

**Verdict: PASS WITH FIXES.** None of the options breaks `constraints.md`: consent gating, the optician's name, the interval coming only from the ophthalmologist, no fear, opt-in only, and no CRM integration are all respected. Issues 1–4 must be fixed before CP2, because they change how fair the A/B/C comparison is and how much weight the recommendation for B can carry.

Checked: `data/constraints.md` (re-read; matches the doc's summary), the CLAUDE.md "Never" list, `01-data-findings.md` §1–§9, `tables/segment_age_40plus.csv`, `tables/segment_report_opened.csv`, `03-insights.md` (CP1 metric, leading indicators), all 4 interviews, the survey, `customer-journey.md` and `README.md`.

## Issues

1. **The metric works against the intervention.**
   - Quoted: "an optional 'next screening recommended in: 12 / 24 / 36 months / not applicable' field" and "Read the 15-month return rate when it matures."
   - Rule broken: CLAUDE.md "Product thinking" (the metric must fit the intervention); 01 §2: "If the ophthalmologist states different intervals by result, the window should follow them."
   - Why it matters: 04 gives "40 and over every 1–2 years". Any 40+ customer told 24 months gets the reminder at about 23 months and is correctly *not* back within 15 months. B could leave the primary metric flat or push it down while working as designed. 03 line 172 already notes this ("Even 40+ may be told up to 2 years"); 04-options ignores it.
   - Fix: add a short section. Define success as "returned by stated interval + 3 months" (an interval-adherent return rate), or restrict the 15-month read to customers given 12 months. State this as an open decision for CP2.

2. **Invented fact: a "partner portal".**
   - Quoted: "a one-click opt-in in the existing partner contract/portal" and "Partner portal view".
   - Rule broken: Never invent data or sources; never add outside "facts" about Mirantus. No file in `data/` mentions a partner portal or dashboard. Survey 3's "Liste im Dashboard" is an optician's wish ("A list in the dashboard"), not proof that one exists.
   - Knock-on effect: if no portal exists, C's "~9–10 weeks" and B's "one-click opt-in" effort are unsupported. C would need authentication, roles and a new surface, which probably makes it bigger than B.
   - Fix: write "opt-in via contract addendum or a simple form (no portal is known to exist)" and re-estimate C on the basis of a new surface.

3. **The comparison leaves out the closest existing analogue to B.**
   - Quoted: "Largest plausible effect … The upper reference is phone+consent at 10.4% (n=240 …)".
   - Rule broken: CLAUDE.md "Surface contradictions explicitly", plus fair comparison.
   - Why it matters: B is an e-mail reminder. The evidence for optician e-mail follow-up is flat: email 4.8% (n=1,018) vs none 4.3% (n=1,763); email+consent 5.3% vs none+consent 4.7%; email-location O/E 1.02 vs 0.86 (01 §3, §6). Meanwhile the phone label is used as B's "upper reference", yet C is cut because "its evidence is a self-reported label (low confidence)". Same label, used in opposite directions.
   - Fix: add the e-mail-label result as counter-evidence in B's effect cell. Either use the phone label for both B and C or for neither.

4. **None of the leading indicators can tell B apart from A.**
   - Quoted: "Read on interval coverage, comprehension, opt-in rate and ≤5-day open rate within weeks."
   - Rule broken: CLAUDE.md requires a leading indicator readable within weeks for the chosen intervention.
   - Why it matters: indicators 1–4 in 03 all measure A's components. The only B-specific signal (booking within 30 days of a reminder) is readable "about 1–2 years after launch" (03). So nothing in the quarter shows whether B adds anything over A.
   - Fix: say so explicitly. Add a B-specific early proxy, e.g. stated reminder intent, or click-through on a test reminder sent to a consenting 2026 cohort that already has a stated interval. Otherwise the case for B over A rests on reasoning, not evidence.

5. **The power numbers do not match the pilot design.**
   - Quoted: "Randomise at location level" alongside "independents only, 1 quarter of screenings (n=834): minimum detectable effect ~4.4 pp".
   - Rule broken: overstated confidence / numbers that don't fit the design.
   - Why it matters:
     - 01 §9 computes the MDE for a two-arm 50/50 split on 834 customers. Location-level randomisation (clustering) and "independents that opt in" (fewer than all independents) both raise the MDE.
     - The reminder only reaches consenting customers (53.4%), which dilutes the intention-to-treat effect.
     - The doc says "A alone is unlikely to produce a lift this size". That implies B might, but nothing supports that. The largest supported gap, 40+ consent vs no consent (6.6% vs 4.1%), is 2.5 pp, which is below every quarter-length MDE.
   - Fix: state that the MDE is a lower bound under cluster randomisation and opt-in selection, and that B is unlikely to clear it in one cohort quarter. Also flag the opt-in selection bias (stores that opt in may already be the "phone" stores).

6. **Unexplained arithmetic.**
   - Quoted: "Reminders for pilot customers fire only from roughly 8–32 months after launch … (12–36 months minus 4 weeks)".
   - Rule broken: every number from the script, no mental arithmetic.
   - Why it matters: 12 months minus 4 weeks is about 11 months after the screening, and 36 months minus 4 weeks is about 35. "8–32" does not follow from the stated inputs.
   - Fix: correct it (about 11–35 months after each screening), or derive it in the script.

7. **Populations are mixed within the 40+ comparison.** Quoted: "consent+opened returns 7.3% (n=1,159) vs 2.3% neither (n=487)" and "65.6% open at all, all customers, n=9,000".
   - Rule broken: every rate must state n, cohort and window, and match the population being compared.
   - Why it matters: the first pair is non-referral, all ages (01 §3); the second includes referral customers (01 §5). Both sit beside 40+ figures (56.1%, 53.4%), so the cells compare different populations.
   - Fix: label the cohort and window on each cell ("non-referral, all ages, Jan–Jun 2025, 15 m"; "all customers incl. referral"). Use 40+ figures if the script produces them, and add them if it doesn't.

8. **A contradicting voice is used as support for B.**
   - Quoted: "Signals: 02 'I will forget otherwise'".
   - Rule broken: surface contradictions; overstated support.
   - Why it matters: the same interviewee says "But not from the optician. I don't even remember which store it was. I'd want it from whoever has my results." That speaks directly against an optician-named reminder. 02 is also `referral_recommended`, so outside the 40+ non-referral target.
   - Fix: quote both lines in B's effect cell and note that 02 is a referral customer.

9. **Problem statement overstated.**
   - Quoted: "customers aged 40+ read the report as 'all fine'. Nobody, not the ophthalmologist, Mirantus or the optician, tells them when to come back".
   - Rule broken: no generalising from n=1; no claims beyond the evidence.
   - Why it matters: "read as all fine" rests on 01 (n=1) and 04's opinion. Some opticians self-report email or phone follow-up (01 §3).
   - Fix: "The report states no interval and Mirantus sends nothing (customer-journey.md); optician follow-up is self-reported and varies. 01 and 04 (signals, n=1 each) describe reading an unremarkable result as 'healthy'."

10. **Survey answers are presented as customer evidence.**
    - Quoted: "Survey 6 says people 'believe' a stated interval." and "It delivers what consenting customers were already promised (I2, C11)."
    - Rule broken: overstated confidence; qualitative claims need the original-language quote.
    - Why it matters: survey 6 is one optician's belief about customers, not customer behaviour. The consent box ("I'd like reminders and offers") is permission, not a promise.
    - Fix: quote it as "Wenn im Befund steht 'Nächstes Screening in 12 Monaten', dann glauben die Leute das auch." → "If the report says 'next screening in 12 months', people believe it." Attribute it as an optician's opinion. Change "promised" to "permitted".

11. **Unsourced claim used to cut mobile units.**
    - Quoted: "mobile units (1.6% return, n=188; no store to return to)".
    - Rule broken: no claims without evidence.
    - Why it matters: 01 §8 Q5 lists this as an open question, not a finding. Also note n=188 and only 3 returns (01 §3).
    - Fix: "low return (1.6%, n=188, 3 returns) and lower consent (38.5%, n=460); whether customers can return to a mobile unit is unknown."

12. **The consent re-ask channel needs a precise legal question.**
    - Quoted: "**Report download page** (part of the service the customer bought): one unticked checkbox".
    - Rule broken: `constraints.md` says consent can be re-asked "only in a message the customer already receives legitimately". A web page reached from E-mail 3 is arguably covered, but that is not settled.
    - Why it matters: non-openers never see the page. That is 15.9% of non-referral customers with neither consent nor an open (01 §4), so the re-ask cannot reach the group that most needs it.
    - Fix: name this as a reach limit in A's reach cell. Add to the week-1 legal list: "Does the download page count as a legitimate message for the re-ask, or must it sit in E-mail 3 itself?"

13. **The three options are nested, not materially different.**
    - Quoted: "B. A + …" and "C. A + …".
    - Rule broken: CLAUDE.md asks for options compared on effect, reach, fit, effort and risk. Here the choice is really A vs A+B vs A+C. The constraint argument justifies making A a prerequisite, but there is no alternative that does not depend on the interval field.
    - Fix: say plainly that A is a prerequisite and the real decision is the add-on. Alternatively, add one materially different option within constraints, e.g. a service-only change to E-mail 3 (result sentence plus optician name in the e-mail body) aimed at the 34.4% who never open.

14. **Effort estimates leave out external lead times.**
    - Quoted: "~5–6 weeks: … translated templates (6 languages)" and "~10–11 weeks … Fits with buffer".
    - Rule broken: the squad-capacity check must be plausible.
    - Why it matters: medically reviewed translations into 6 languages, ophthalmologist sign-off on the templates, and a legal ruling on the controller question are all outside the squad's control. The reminder engine also depends on the legal answer in week 1. A buffer of about 2 weeks on a roughly 13-week quarter is thin.
    - Fix: list these as external dependencies with owners. Make the reminder engine conditional on the week-1 legal answer, and name a fallback scope (A only) if it slips.

15. **Interval choices are fixed by Mirantus.**
    - Quoted: "12 / 24 / 36 months / not applicable".
    - Rule broken: interval wording must come from the ophthalmologist's evaluation. The options are offered as a fixed list, not stated by the ophthalmologist herself.
    - Why it matters: 04 uses ranges ("every 1–2 years", "2–3 years").
    - Fix: say that the option set itself needs sign-off from the evaluating ophthalmologist(s), together with the template sentences.
