<!-- Written by the critic subagent (returned as text; it has no Write tool); saved verbatim by the main session. -->
# Review: outputs/05-decision-memo.md

**Verdict: PASS WITH FIXES.**

The memo breaks no Never rule as written:
- Reminders go only to customers with `marketing_consent`, in the optician's name, and need the optician's opt-in.
- Any interval comes from the ophthalmologist.
- There is no fear copy, no CRM or cash-register work, and no mandatory work for opticians.

All required sections are there: recommendation, what ships first, what is cut, success metric, guardrails, leading indicator, and a 2-week test with who, how many, what we learn and kill criteria. Most numbers trace to 01 §2 and §9.

`wc -w` is 444, so only 6 words are free. Every fix below must cost no words overall (see the word budget at the end).

## Issues

1. **The reminder timing contradicts a guardrail.**
   - Quoted: "Four weeks before it ends, consenting customers get an e-mail" vs guardrail "no reminder before the stated interval".
   - Rule broken: the memo contradicts itself, and a guardrail that cannot be checked is not a guardrail.
   - Fix: change the guardrail to "no reminder earlier than 4 weeks before the stated interval ends".

2. **The reminder side cannot be read this quarter, and the memo doesn't say so.**
   - Quoted: "Guardrails: … unsubscribes, optician opt-outs, complaints" and the success metric section.
   - Rule broken: CLAUDE.md requires a leading indicator readable within weeks. 04-options l.65 says "The first real reminders go out 4 weeks before each stated interval ends, i.e. long after this quarter". The interviewee's intervals are 1–3 years (data/interviews/04).
   - Why it matters: no pilot customer gets a reminder in the quarter. The unsubscribe and complaint guardrails, and any effect of B over A, can be read only about 11 months or more after launch. The re-ask opt-in rate is the only early signal specific to B.
   - Fix: add one clause: "Reminders first fire ~11+ months after launch; this quarter B is read only via re-ask opt-in."

3. **A leading indicator the intervention cannot move.**
   - Quoted: "report opened within 5 days (40+ today 56.1%, n=6,279)".
   - Rule broken: the metric must fit the intervention. The box is inside the report, and the memo does not change E-mail 3. Opening the report happens before anyone sees the box.
   - Fix: drop it, or label it as a baseline context measure. If kept, add the cohort: "non-referral, all 2025 cohorts" (01 §9).

4. **"Share who can say when to return" has no measurement method and no legal channel.**
   - Rule broken: GDPR. Surveying customers without consent is neither a service message nor allowed.
   - Fix: say how it is measured. Options: in person at the store, inside the report page (the legitimate message), or only among consenting customers.

5. **Recruiting the test customers is not specified.**
   - Quoted: "12–16 customers aged 40+ with a recent unremarkable/minor result, at 3 independents".
   - Rule broken: constraints.md. Mirantus may not contact customers in its own name beyond the service, and without consent may not contact them at all.
   - Fix: "recruited in person by the optician at the counter, or by the optician among consenting customers".

6. **The ophthalmologist test uses a field that does not exist yet, on live evaluations.**
   - Quoted: "3 ophthalmologists use the field on 20 evaluations each".
   - Rule broken: medical statements need sign-off (the memo's own item 1). In two weeks there is no field, and live intervals would reach customers before sign-off.
   - Fix: "on a mock form in shadow mode; intervals not sent to customers".

7. **Overstated claim.**
   - Quoted: "54.0% consented to reminders (n=8,116); none get one."
   - Rule broken: no overstated confidence. Opticians self-report e-mail and phone follow-up (`optician_follow_up`). Mirantus sends nothing; others may send something.
   - Fix: "Mirantus sends none; optician follow-up is self-reported and varies." Also add the cohort: "non-referral, all 2025".

8. **A headline number has no cohort or window.**
   - Quoted: "5.5% of non-referral customers aged 40+ return within 15 months (n=2,452)".
   - Rule broken: CLAUDE.md requires every rate to state n, cohort and observation window.
   - Fix: add "(Jan–Jun 2025 cohorts)" (01 §9). Do the same for the company-trend baseline line.

9. **The minimum detectable effect is understated for the pilot as scoped.**
   - Quoted: "minimum detectable effect ≥3–4 points".
   - Rule broken: every number must trace to the script. 01 §9 gives ~4.4 pp for independents over one quarter (n=834), and ~3.1 pp only over two quarters. ~3.2 pp applies to all locations, which the pilot is not.
   - Fix: "~4.4 points for one quarter at independents (01 §9)".

10. **Referral customers are not handled in the box or reminder scope.**
    - Rule broken: CLAUDE.md says to treat `referral_recommended` customers separately, because their next step is an ophthalmologist. As written, the report box and reminder could tell a referred customer to "come back in X", which competes with the referral. The guardrail only partly covers this.
    - Fix: "Box and reminder for non-referral results only; referral reports keep the referral as the next step."

11. **The referral guardrail threshold does not fit the pilot.**
    - Quoted: "referral bookings ≥50.5% (n=884)".
    - Rule broken: the baseline is all locations for all of 2025 (01 §2). The pilot is at independents for one quarter, so pilot referral n will be roughly 100–150. That is too small for a hard threshold, and it is not the same population.
    - Fix: give the independents baseline from the script, and state it as "monitored, no drop beyond CI" rather than a point threshold.

12. **The riskiest assumptions are not named, and a contradicting voice is missing.**
    - Rule broken: CLAUDE.md says to name the riskiest assumptions and to surface contradictions.
    - Assumption 1: data/interviews/02-customer-berlin.md says "But not from the optician. I don't even remember which store it was. I'd want it from whoever has my results." This speaks directly against optician-named reminders.
    - Assumption 2: data/interviews/04-ophthalmologist.md says "Risk factors like family history aren't asked at the screening, so she often can't tell who should come back sooner". That puts at risk whether intervals will be individual or just by age, which is close to the "blanket interval" the memo cut with posters.
    - Fix: one line, "Riskiest assumptions: customers accept an optician-named sender (02 contradicts); ophthalmologists can set individual intervals without risk-factor data (04)." The test already probes the first one, so tie the kill criteria to it.

13. **"Fall back to A" is undefined in the memo.**
    - The memo is meant to stand alone.
    - Fix: "fall back to A (items 1–3, 6)", or rename the fallback line "Option A".

14. **The quote attribution is incomplete.**
    - Quoted: "Ophthalmologist: 'I would fill it in if it were there. It takes five seconds.'"
    - The source is a German call that the interviewer translated (data/interviews/04, l.3). No German original exists.
    - Fix: add "(interview 04, interviewer's translation)".

15. **The kill thresholds use proportions from n=12–16.**
    - Quoted: "Under half state the interval correctly"; "Under a third would opt in".
    - Rule broken: interviews are signals, not proportions. These thresholds are acceptable as pre-agreed decision rules, but the memo should say they are directional.
    - Fix: change "(our thresholds)" to "(directional, n=12–16)".

16. **Capacity is tight but plausible.**
    - 04-options estimates ~10 of ~13 weeks for B, with external dependencies: legal in week 1, medical sign-off, and template translation into 6 languages. The memo names the fallback but not who owns those dependencies or a date for deciding to fall back.
    - Fix: "Fallback decided by week 3 if legal or sign-off is open."

## Word budget

Fixes 1–16 add about 60–80 words.

Suggested cuts:
- the cut list's reasons for posters and price bundles
- "(one squad, one quarter)"
- the duplicated "Legal says no: fall back to A", which is already covered by the Fallback line
- issue 3: drop the open-rate indicator

Re-check that the memo is ≤ 450 words with `wc -w` after editing.
