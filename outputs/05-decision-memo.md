# 05 Decision memo: the next screening as a date, in the optician's name
Summary: 5.5% of non-referral 40+ customers return within 15 months (n=2,452, Jan–Jun 2025).
Recommendation: an ophthalmologist interval in the report, plus an optician-named reminder for consenting customers.
Inputs: 03, 04, CP1/CP2, `constraints.md`. Data synthetic.

**Problem.** No interval in the report; Mirantus sends nothing afterwards; optician follow-up is self-reported and varies. 54.0% of non-referral customers consented to reminders (n=8,116). Ophthalmologist (04, interviewer's translation): "I would fill it in if it were there. It takes five seconds."

**Recommendation.** The ophthalmologist records the interval. A box on report page 1 repeats it in the customer's language. Four weeks before it ends, consenting customers get an e-mail from their optician with a booking link. Non-referral results only.

**Ships first:**
1. Week 1: legal (consent scope), medical sign-off (intervals, templates).
2. Interval field.
3. Report box, 6 languages.
4. Consent re-ask on the report page; optician opt-in.
5. Reminder scheduler and optician template.
6. Tracking.

Fallback A (items 1–3, 6) if sign-off is open by week 3.

**Cut:** optician due list (new surface, store time); SMS (no channel consent); full translation; 2025 customers (no interval); chains; mobile units; posters; price bundles.

**Success metric.**
- Pilot: return within the stated interval + 3 months (40+, non-referral).
- Company trend: 15-month return rate for 40+, baseline 5.5% (CI 4.7–6.5).
- One quarter at independents detects only ≥4.4 points (01 §9). Reminders fire ≥11 months after launch, so leading indicators decide.

**Leading indicators:** share of reports that carry an interval; re-ask opt-in rate; customers able to state when to return (asked in person).

**Guardrails:** referral bookings at independents don't drop beyond the CI (baseline 49.9%, n=479); unsubscribes and optician opt-outs; ophthalmologist time per evaluation; no reminder more than 4 weeks early; no fear wording.

**Riskiest assumptions:**
- Customers accept an optician-named sender. 02 disagrees: "I'd want it from whoever has my results."
- Intervals can be individual without risk-factor data (04).

**Two-week test:**
- **Customers:** 12–16, aged 40+, with a recent non-referral result, recruited in person by 3 independent opticians. They read the prototype box and reminder: can they state the interval, recognise the sender, would they opt in?
- **Ophthalmologists:** 3, using a mock form on 20 evaluations each (nothing sent): coverage, seconds added, intervals chosen.
- **Opticians:** 5 independents review the reminder: would they opt in?

**Kill/change** (directional, given small n):
- Under half can state the interval: redesign the box.
- Under a third would opt in, or the sender isn't recognised: ship A.
- The field adds more than 30 s: rethink it.
- Fewer than 3 of 5 opticians would opt in: rethink the reminder.
