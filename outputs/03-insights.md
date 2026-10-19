# 03 Insight synthesis

Summary: Few customers come back, and they come back late. Within 15 months, 4.8% of non-referral customers return (Jan–Jun 2025 cohorts, n=3,170), and no one returns before month 7.
Nothing in today's journey asks anyone to come back. The report states no interval, and consenting customers receive no reminder. The one unremarkable customer interviewed and the ophthalmologist both describe "unremarkable" being read as "healthy".
Legal reach for reminders is capped by consent (54.0% of n=8,116 non-referral). Report content reaches only openers (65.6% of all customers). All data is synthetic, and all associations are correlational.

Inputs used: `outputs/01-data-findings.md` (incl. §9 addendum), `outputs/02-research-synthesis.md`, `outputs/tables/*.csv`, `scripts/analyze.py`, `data/constraints.md`, `data/customer-journey.md`, `CLAUDE.md`.
Conventions:
- Unless stated otherwise, rates are non-referral customers (unremarkable + minor_findings), Jan–Jun 2025 first-screening cohorts, 15-month return window, only customers who had the full window.
- Quotes: file · original → English. Interview 03 is partly, and interview 04 entirely, in the interviewer's English only.
- [n<100] marks small groups.
- "Implication for options" lines are inputs to step 4, not decisions.

---

## Insights

### I1. Return is rare and late: the metric is slow and needs leading indicators
- **Data:**
  - Return rate by window:
    - 12 months: 2.1% (n=5,209, Jan–Sep)
    - 15 months: 4.8% (n=3,170, CI 4.1–5.6)
    - 18 months: 6.7% (n=1,426, Jan–Mar)
  - Earliest return 199 days; median 380 days. 0.2% had returned within 9 months (n=8,116).
  - In the Jan–Mar cohort, a 12-month window catches 35.4% of 18-month returners; 15 months catches 79.2% (01 §1).
- **Voices:**
  - 02 · "Honestly I'd love a reminder. Just WhatsApp me in a year. I will forget otherwise." (orig. EN)
  - 01 · "Warum? War doch alles in Ordnung." → "Why? Everything was fine."
- **Confidence:** high for the rate and the timing. They describe the status quo, in which there is no prompt at all.
- **So what:**
  - A cohort's 15-month rate is complete only 15 months after its last customer was screened. The first full read of a change shipped this quarter comes roughly 15+ months after launch.
  - A 12-month partial read covers only about a third of returners (35.4%).
  - Leading indicators are therefore mandatory (see Metric).

### I2. Nothing in the journey asks the customer to come back, and the interval has nowhere to live
- **Journey:**
  - "The report has **no** recommendation for when to come back for the next screening."
  - Unremarkable/minor results: "**no further contact** from Mirantus" (`customer-journey.md` §3–4).
  - The booking checkbox reads "I'd like reminders and offers" (§1). No reminder flow exists.
- **Voices:**
  - 04 · Interviewer note (paraphrase): her evaluation form has no interval field. Quoted: "I would fill it in if it were there. It takes five seconds." (interviewer EN)
  - 04 · Her general guidance "depends on the person" (paraphrase):
    - under 40 without risk factors: 2–3 years;
    - 40+: 1–2 years;
    - with risk factors: yearly.
  - 02 · Interviewer note (paraphrase): he ticked the reminders box and has received nothing since the report.
- **Data:**
  - Return with consent 5.6% (n=1,788) vs without 3.8% (n=1,382). The CIs overlap slightly.
  - Nothing is sent to consenting customers today, so this gap reflects who chooses to consent, not an effect of reminders.
- **Confidence:**
  - High that the gap exists.
  - Unknown whether closing it raises return. Only survey 6 ("dann glauben die Leute das auch" → "people will believe it") and 02's wish support it.
- **Implication for options:**
  - An interval for a specific customer can only exist if the ophthalmologist states it (`constraints.md`). She has nowhere to record one today.
  - Delivering the promised reminders closes a gap between promise and delivery. Its effect on return is untested.

### I3. "Unremarkable" customers are the largest group and return least
- **Data** (15 months):

  | Result | All ages (n) | 60+ | 40–59 | 18–39 |
  |---|---|---|---|---|
  | Unremarkable | 3.4% (2,428) | 4.9% (878) | 3.0% (990) | 1.8% (560) |
  | Minor findings | 9.4% (742) | 11.6% (267) | 9.8% (317) | 5.1% (158) |

  The gap holds at every window. At 18 months: 14.4% vs 4.4%.
- **Voices:**
  - 04 · "An unremarkable result is a snapshot, not a guarantee. Patients read it as 'I'm healthy'." (interviewer EN)
  - 04 · "It's the 'unremarkable' 60-year-olds who disappear." (interviewer EN)
  - 01 (67, unremarkable) · "Ich hab nur geguckt, ob irgendwo was Rotes steht. Stand nichts, also war alles gut." → "I only looked whether there was anything red anywhere. There wasn't, so everything was fine."
- **Contradiction:**
  - Survey 2 says "our customers come back for glasses anyway" (orig. EN).
  - A glasses visit is, by definition, not a second screening. 4.9% of unremarkable 60+ customers (n=878) returned for a screening within 15 months.
- **Confidence:**
  - High for the association.
  - The cause is unproven: misreading the result, or simply lower need. The misreading rests on n=1 customer plus 1 ophthalmologist.
- **Implication for options:**
  - The main target is unremarkable customers aged 40+.
  - Copy should frame the result as a snapshot, carry only the ophthalmologist's interval, and avoid fear. 04: "If you scare people, the ones who come are the anxious ones, not the ones at risk."

### I4. Content that lives only in the German PDF misses many customers, and most non-German speakers
- **Data:**
  - Report open rate (all customers, ever opened):
    - overall 65.6% (n=9,000)
    - German speakers 71.8% (n=7,367) vs non-German speakers 37.8% (n=1,633)
    - 60+ 61.6% (n=3,187)
  - Opened within ≤5 days (non-referral): 57.2% (n=8,116); de 62.6% (n=6,645) vs non-de 33.0% (n=1,471).
  - Return rate by opening:
    - opened 6.1% (n=2,054) vs never opened 2.4% (n=1,116)
    - non-de only: 5.2% (n=210) vs 2.4% (n=368)
- **Voices:**
  - 02 · "half of it made no sense" (orig. EN, after Google Translate)
  - 01 · "Da standen lauter Fachbegriffe drin." → "It was full of technical terms."
  - 04 · "They are written for colleagues, honestly. Not for patients." (interviewer EN)
- **Confidence:**
  - High for the language gap in opening.
  - Medium that opening matters for return. Opening may simply mark engaged customers.
- **Implication for options:**
  - An interval in the report reaches only openers.
  - Whether a plain-language interval line may also appear in the "result ready" e-mail needs a legal/medical ruling (see What we don't know). The default is the report only.
  - Report language is a separate lever.

### I5. About half of the target group can legally receive a reminder
- **Data:**
  - Consent among non-referral customers: 54.0% (4,386/8,116).
  - Consent among non-referral 40+: 53.4% (n=6,279); unremarkable 40+: 53.3% (n=4,750).
  - Mobile units, non-referral: 38.7% (n=416). Other cuts (all customers) range from 49% to 58%.
  - 15.9% of non-referral customers neither consented nor opened the report. E-mail opening is not measured.
  - 15-month return rate among 40+: with consent 6.6% (n=1,383), without 4.1% (n=1,069).
- **Journey:**
  - The checkbox is unticked by default.
  - The journey doesn't say whether consent is captured at counter bookings. Counter booking is the main channel at independent stores (02 §3, B1).
- **Rules:** consent may be re-asked only in a message the customer already receives legitimately, or in person.
- **Confidence:**
  - High for the reach numbers.
  - No evidence on the opt-in rate when consent is re-asked (A6).
- **Implication for options:**
  - A reminder alone can reach at most about 53% of the target group.
  - Re-asking consent at a legitimate moment determines reach. Candidate moments: the "result ready" e-mail, the report page, in person at the screening.

### I6. Self-reported phone follow-up is associated with higher return (low confidence), and opticians want their name on it without extra work
- **Data** (self-reported `optician_follow_up`):
  - Phone 7.5% (n=389) vs none 4.3% (n=1,763).
  - Phone + consent 10.4% (n=240) vs phone without consent 2.7% (n=149).
  - Within independents: phone 7.2% (n=360) vs none 5.2% (n=783). CIs overlap.
  - Cohort-adjusted observed/expected returns, all 8,116 non-referral customers, by export date:
    - phone locations 1.58 (6 of 7 above 1)
    - email locations 1.02
    - none 0.86
- **Voices:**
  - 01 · "Wenn Herr K. sagt, ich soll wieder kommen, dann komm ich wieder." → "If Mr K. tells me to come back, I'll come back."
  - 03 · "The customers are mine. If someone writes to them, it's me." (interviewer EN)
  - Survey 4 · "Bitte keine Mails von Mirantus an meine Kunden." → "Please no e-mails from Mirantus to my customers."
  - Survey 1 · "Eine automatische Erinnerung an den Kunden, aber mit unserem Logo." → "An automatic reminder to the customer, but with our logo."
- **Contradictions:**
  - **Automatic or manual?**
    - Survey 9 · "Wir haben keine Zeit, Kunden anzurufen. Es muss automatisch gehen." → "We have no time to call customers. It has to be automatic."
    - 03 · "A list. Who should come back this month. Then my people can call." (interviewer EN)
  - **Who should send it?** 02 wants it "not from the optician… from whoever has my results" (orig. EN).
  - **Is a call welcome?** 03 thinks older customers find calls "pushy" (interviewer EN). 01 (67) would return if her optician told her to.
- **Confidence:** low–medium. The label is self-reported and confounded with store type, and the voices conflict.
- **Implication for options:**
  - A reminder must go out in the optician's name, only to customers with `marketing_consent`.
  - It must need no work from the store. At most an opt-in, and nothing to configure.
  - An optional "who is due" list could serve stores that want to call.
  - Open questions: does the existing consent cover reminders on the optician's behalf, and who is the controller?

### I7. Mobile units and chains don't fit a one-size solution
- **Data:**
  - Mobile units: 1.6% return (n=188, 3 returns) and 38.7% consent (n=416). The three lowest-O/E locations are all mobile units.
  - Chain vs independent: 4.4% (n=1,279) vs 5.5% (n=1,703). Low confidence.
- **Voices:**
  - Survey 7 · "Our chain HQ decides about customer communication, not the store. Talk to them." (orig. EN)
  - Mobile units: no voice.
- **Confidence:** low. Small groups, and one chain voice.
- **Implication for options:**
  - Pilot at independents.
  - Chains depend on HQ sign-off.
  - Mobile units are out of scope until we know where their customers could return.

---

## Proposed return metric

| | |
|---|---|
| **CP1 decision (Lars, 2026-10-19)** | **Primary metric = 15-month return rate, non-referral, age 40+. Baseline 5.5% (n=2,452, Jan–Jun 2025, CI 4.7–6.5).** 18–39 and all-ages reported as secondary |
| **Name** | 15-month return rate (non-referral) |
| **Definition** | Share of customers with an `unremarkable` or `minor_findings` first screening whose next mira screening (at any location) falls within 15 months |
| **In** | Non-referral customers whose full 15-month window has passed |
| **Out** | `referral_recommended` customers, who are tracked via `referral_booked` as a guardrail (50.5%, n=884). Customers whose window has not passed yet |
| **Baseline** | **4.8%** (n=3,170, Jan–Jun 2025, CI 4.1–5.6). Sensitivity: 12 months 2.1% (n=5,209); 18 months 6.7% (n=1,426) |
| **Scope option for CP1** | 04's general guidance is 2–3 years for under-40s without risk factors. Option: primary metric for 40+ only, **5.5%** (n=2,452, CI 4.7–6.5). Report 18–39 separately (2.5%, n=718). Even 40+ may be told up to 2 years, so a fixed window still miscounts some customers |
| **Target definition** | Once the ophthalmologist states an interval per customer: "returned within stated interval + 3 months". This replaces the fixed window |
| **Read cadence** | Monthly, by first-screening cohort. First full read ~15+ months after launch. Partial 12-month read covers ~35% of returners |
| **Detectable effect** | Two-arm test at the 40+ baseline. Independents only: ~4.4 pp after 1 quarter of screenings (n=834), ~2.2 pp after 4 quarters (n=3,336). All locations: ~3.2 pp after 1 quarter (n=1,570). The 15-month metric cannot detect small lifts quickly; leading indicators carry the early decision |

**Leading indicators** (associated with return, not proven causes):
1. **Interval coverage.** Share of non-referral reports with an ophthalmologist-stated interval. Today 0%: the field doesn't exist. Readable within days.
2. **Comprehension.** Share of customers who can say when to return after reading the report. Today no measurement. Measured in task-based tests in the 2-week test. Tests the riskiest assumption (A2).
3. **Report opened within ≤5 days**, non-referral. Today 57.2% (n=8,116); 40+ 56.1% (n=6,279). Readable within days.
4. **Remindable share.** Share of non-referral customers with consent, including re-asked consent. Today 54.0% (n=8,116). Readable within days.

**Lagging intermediate indicator:**
- Booking within 30 days of a reminder.
- Readable only once reminders fall due, about 1–2 years after launch.
- It cannot be applied to the 2025 backlog: those customers have no ophthalmologist-stated interval.
- It needs new tracking. Bookings are not in the data, and counter bookings are not captured online.

**Guardrails:**
- `referral_booked` (50.5%, n=884)
- reminder opt-out/unsubscribe rate
- optician complaints and opt-outs
- ophthalmologist time per evaluation
- share of customers reminded sooner than their stated interval
- complaints about fear or pressure

**What would establish cause:** a randomised test, by location or by customer, against today's journey. Read first on indicators 1–4, then on the 15-month rate.

---

## What we don't know

- **Whether customers act on a stated interval.** Only survey 6's belief supports it. C6: customers skim the report.
- **Whether other ophthalmologists fill in the field** (n=1, A4). 04 evaluates ~200 a month (paraphrase).
- **How far intervals can be personalised.** Risk factors are not collected. 04 (paraphrase) often can't tell who should come back sooner (A7). Intervals may default to generic age-based values.
- **Two legal/medical questions:**
  - May an interval line appear in the "result ready" e-mail? It would put result-derived health data in an e-mail, and for customers without consent it could read as a reminder in Mirantus's name.
  - Does a generic "annual" in-store norm count as a medical statement (C7)? Until ruled: interval in the report only, no blanket interval.
- **Consent scope and controller.** Does "reminders and offers" consent, captured on Mirantus's or the optician's page, cover reminders sent in the optician's name?
- **Opt-in rate when consent is re-asked** (A6).
- **Where people return.** We only know they returned to some mira location, not whether it was the same optician.
- **What "phone"/"email" opticians actually do, and to whom** (C10).
- **Price.**
  - 01 · "für einmal okay, aber jedes Jahr? Weiß ich nicht." → "okay for once, but every year? I don't know."
  - Survey 5 · "69 € every year is a lot for pensioners." (orig. EN)
- **Mobile units.** There is no voice and only 3 returns.

## Where data and voices disagree

| Topic | Voices say | Data says |
|---|---|---|
| Customers "come back for glasses anyway" (survey 2) | No action needed | 4.9% of unremarkable 60+ customers return for a screening within 15 months (n=878) |
| Older customers find calls pushy (03) | Don't call | 60+ phone-labelled 9.5% (n=126) vs none 5.3% (n=659). CIs overlap; the label is self-reported. This does not show whether calls feel pushy. 01 (67) would return if her optician told her to |
| A reminder from "whoever has my results" (02), or "the customers are mine" (03, survey 4) | Conflict over who sends | The data can't answer this. The rules settle it: the optician's name goes on it. Recognition must be tested |
| Opticians "email" customers (self-report) | Follow-up happens | Email-labelled locations look like "none" (cohort-adjusted O/E 1.02 vs 0.86) |
