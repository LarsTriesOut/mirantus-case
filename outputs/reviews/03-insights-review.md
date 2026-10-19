<!-- Written by the critic subagent; saved verbatim by the main session because the critic has no Write tool. -->
# Review: outputs/03-insights.md

**Verdict: PASS WITH FIXES**

Checked against: `data/constraints.md` (re-read), the Never list in `CLAUDE.md`, `outputs/01-data-findings.md` §0–§9, `outputs/tables/*.csv`, `outputs/02-research-synthesis.md`, `data/interviews/01–04`, `data/optician-survey.md` and `data/customer-journey.md`.

Most numbers trace correctly: the I3 table and the I1, I2, I5, I6 and I7 figures, the metric baseline and the 40+/18–39 option all match. All quotes exist in their sources. Nothing breaks a Never rule outright. The open issues are leading indicators that cannot be read, legal points nobody has raised, and some overclaiming.

## Metric and leading indicators

1. **Indicator 4 cannot be read within weeks without breaking the interval rule.** Quoted line: "Once reminders exist: **booking rate within 30 days of a reminder.**"
   - New customers would get their reminder at roughly 12 months or later.
   - Reading it sooner would mean reminding customers screened in 2025. They have no ophthalmologist-stated interval, so any "time to come back" copy would state an interval that does not come from the evaluation (`constraints.md`, Medical advice).
   - Bookings are also not in the data. Counter bookings are not captured online, so the indicator needs new tracking.
   - Rules broken: "leading indicator readable within weeks" (CLAUDE.md); the interval rule.
   - Fix: label it a lagging intermediate indicator. State that it cannot be applied to the 2025 backlog without an ophthalmologist interval. Name the tracking it needs.

2. **Indicator 2 has no baseline for the definition given.** Quoted line: "**Report open rate within 7 days.** Today 65.6% open the report at all (n=9,000)".
   - The baseline shown is "ever opened", for all customers. The metric population is non-referral.
   - The days field only takes the values 0/1/2/3/5/9, so "within 7 days" is the same as "≤5".
   - Rule broken: every number from the script, with n and cohort stated.
   - Fix: have `analyze.py` output the non-referral open rate at ≤5 days with n, and use that as the baseline.

3. **No leading indicator for the riskiest assumption (A2: customers understand and act on the interval).**
   - Indicators 1 and 3 measure inputs and reach, not customer behaviour.
   - Fix: add a comprehension or intent indicator for the 2-week test, e.g. "customer can say when to return after reading the report/e-mail", from task-based tests with real customers.

4. **No minimum detectable effect or power estimate.** Quoted line: "a randomised test ... read first on indicators 2–4 and then on the 15-month rate."
   - The baseline has 153 events at 4.8%. Nobody has checked whether the pilot (independents only, I7) gives enough customers to detect a realistic lift.
   - Fix: compute the MDE for the pilot size in the script, not by hand.

5. **The read timing is understated.** Quoted line: "Any effect ... shows up in the metric only after 10–15 months."
   - A cohort's 15-month rate is complete only 15 months after its last member is screened.
   - "Intermediate read at 12 months" captures about 35% of returners (01 §1).
   - Fix: say "a first full cohort read about 15+ months after launch; a partial 12-month read covers only ~35% of returners."

6. **The window conflicts with 04's guidance for 40+ too, not only for under-40s.** Quoted line (scope option): "a 15-month window may count medically fine non-returners as failures".
   - 04 gives 40+ "every 1–2 years". A 40+ customer told 24 months is also counted as a failure.
   - Fix: say this explicitly, and make "returned within the stated interval + 3 months" the target definition once the field exists.

7. **Guardrails are thin.** Only `referral_booked` is named.
   - Fix: add opt-out/unsubscribe rate on reminders, optician complaints or opt-outs, ophthalmologist time per evaluation, and the share of under-40s reminded sooner than their stated interval.

## Constraints and legal

8. **Putting the interval in the "result ready" e-mail is not cleared.** Quoted line (I4): "The interval must also appear outside the PDF, in a plain sentence ... 'Result ready' is a service e-mail every customer receives legitimately."
   - `constraints.md` places ophthalmologist statements "in the report". Today the e-mail deliberately carries no result. Adding result-derived content to an e-mail exposes health data (GDPR Art. 9).
   - A "come back in X months" line in a Mirantus-sent e-mail to customers without consent could also be read as a reminder in Mirantus's own name.
   - Fix: change "must" to an option that needs a ruling. Add it to "What we don't know" next to C7. Default to the interval in the report only, and add no booking call-to-action for customers without consent.

9. **It is unclear whether existing consent covers reminders sent on the optician's behalf.** Quoted line (I6): "an automatic reminder, sent on the optician's behalf with the optician's name. That is allowed and needs no work from the store."
   - Consent is "reminders and offers", captured on Mirantus's booking page or the optician's site. Nobody has checked whether it covers reminders sent in the optician's name, or who the GDPR controller is.
   - "Needs no work" assumes the optician never has to set up a name/logo or opt in.
   - Fix: send only to customers with `marketing_consent`, and say so in this sentence. List consent scope and controller as an open legal question. State that the optician only opts in and is never required to configure anything.

10. **The interval field will default to generic intervals.** 04 says risk factors are not collected, so she "often can't tell who should come back sooner" (A7).
    - Missing from "What we don't know". Fix: add it.

## Evidence and overclaiming

11. **The summary states n=1 voices as fact.** Quoted line: "'unremarkable' is read as 'healthy'."
    - This rests on one customer (01) and one ophthalmologist's view (04).
    - Fix: "the one unremarkable customer interviewed, and the ophthalmologist, describe 'unremarkable' being read as 'healthy'."

12. **The I6 heading is causal; the confidence rating is low.** Quoted line: "A personal prompt in the optician's name looks like it works".
    - The label is self-reported and confounded with store type. Within independents the CIs overlap. The finding is rated "Low–medium".
    - Fix: "Self-reported phone follow-up is associated with higher return (low confidence)."

13. **I2 overclaims the lever.** Quoted line: "Delivering them is the most direct lever."
    - No evidence ranks levers. The checkbox also says "reminders and offers", not "reminders".
    - Fix: "Delivering them closes a gap between promise and delivery. Its effect on return is untested."
    - Related: the quote marks around "reminders and offers" in the 02 paraphrase are the journey's checkbox label, not his words. Remove them or attribute them to `customer-journey.md` §1.

14. **The rebuttal of "pushy" is a non-sequitur.** Quoted line: "60+ customers return most (6.5%, n=1,145), and phone + consent shows the highest rate (10.4%, n=240; low confidence). 01 (67) wants her optician to ask".
    - The 10.4% is not a 60+ figure. 60+ return without any prompt says nothing about calls. 01 talks about Herr K. telling her, not about being called.
    - C2 asked for 60+ × `optician_follow_up`, and it was not run.
    - Fix: run that cut in the script, or label the row "not answerable from current outputs." I6 "01 (67) says the opposite" has the same problem: change it to "01 (67) would return if her optician told her to."

15. **The data does not show that glasses visits are not screenings.** Quoted line (I3): "The data shows a glasses visit is not a second screening."
    - That is a definition, not a finding.
    - Fix: "By definition a glasses visit is not a second screening; the data shows 4.9% (n=878) of unremarkable 60+ customers returned for one within 15 months."

16. **E-mail opening is unmeasured.** Quoted line (I5): "which they also tend not to open."
    - 01 §7 says opens of the "result ready" e-mail are not in the data. Only report opening is.
    - Fix: "they never opened the report; e-mail opening is unmeasured."

17. **Opening the report is not a reach cap.** Quoted line (summary): "Reach is capped by consent (54.0%) and by report opening (65.6%)."
    - Consent caps who may legally be contacted. Opening caps engagement. Service e-mails reach everyone.
    - Fix: "Legal reach for reminders is capped by consent (54.0%, n=8,116 non-referral). Report content reaches only openers (65.6%)."

## Numbers: n, population, basis

18. **The 60+ open rate has no n and a different population.** Quoted line: "60+ 61.6%".
    - Fix: "60+ 61.6% (n=3,187, all customers)."

19. **I5 mixes populations.** Quoted line: "mobile units 38.5% (n=460); other cuts 49–58%".
    - These are all-customer figures in a section headed by non-referral reach. The non-referral mobile figure is 38.7% (n=416, `reach_consent_nonreferral.csv`).
    - Fix: use the non-referral figure, or label the population.

20. **A return rate reads like a consent rate.** Quoted line: "Among 40+: consent 6.6% (n=1,383) vs no consent 4.1% (n=1,069)."
    - Fix: "15-month return rate among 40+: with consent 6.6% ... without 4.1% ...". Also, "at most about half the target group" has no figure for unremarkable 40+. Cite the flat 52–56% consent range by age and result (01 §4), or compute it.

21. **O/E basis not stated.** Quoted line: "observed/expected returns 1.58".
    - This is cohort-adjusted O/E by export across all 8,116 non-referral customers, not the 15-month window the conventions line implies.
    - Fix: state the basis inline.

## Process

22. **The insights pre-empt CP2.** Quoted lines: "The intervention starts with an interval field..." and "The default must be an automatic reminder..."
    - The options have not been compared yet.
    - Fix: rephrase as "implication for options", and leave the choice to the option comparison after CP1.
