# 04 Options

Summary: The report states no interval and Mirantus sends nothing after it. Optician follow-up is self-reported and varies. So for customers aged 40+ with an unremarkable or minor result, nothing reliably prompts a return: 5.5% return within 15 months (n=2,452).
A customer-specific interval may only come from the ophthalmologist, so all three options start with her interval in the report (A). They then differ in the trigger: none (A), an automatic e-mail in the optician's name (B), or an optional "who is due" list (C).
Recommendation: B, piloted at independent opticians, with A as the fallback if the legal check on the consent scope fails. Open decision for Lars: the pilot needs an interval-based success measure, because the fixed 15-month window works against intervals of 24 months or more.

Inputs used: `outputs/03-insights.md` (CP1: primary metric = 15-month return, non-referral 40+, baseline 5.5%, n=2,452), `outputs/01-data-findings.md` (incl. §9), `outputs/02-research-synthesis.md`, `data/constraints.md` (re-read 2026-10-19, unchanged since step 0), `data/customer-journey.md`, `CLAUDE.md`, `outputs/reviews/04-options-review.md`.
Numbers come from `scripts/analyze.py`. Unless stated otherwise: non-referral, age 40+, Jan–Jun 2025 cohorts, 15-month window. All data is synthetic.

---

## Problem in one sentence
Customers aged 40+ leave an unremarkable or minor result without a date or a prompt to return:
- The report states no interval, and Mirantus sends nothing after it (`customer-journey.md` §3–4).
- Optician follow-up is self-reported and varies.
- 01 and 04 (signals, n=1 each) describe "unremarkable" being read as "healthy".

## Why the options share a base
- `constraints.md`: an interval for a specific customer "must come from the ophthalmologist's evaluation". A reminder sent at a set time states an interval implicitly, so no option can remind anyone until the ophthalmologist has recorded one.
- Her form has no field for this today. 04: "I would fill it in if it were there. It takes five seconds." (interviewer EN)
- So A is a prerequisite. What really separates the options is **the trigger**: none, automatic, or manual by the optician.
- Customers screened in 2025 have no stated interval and cannot be reminded under any option.

## The options

**A. Interval in the report (smallest viable). Trigger: none.**
- **The field:** an optional "next screening recommended in …" field in the evaluation form, empty by default.
  - The choice set (e.g. 12 / 24 / 36 months / not applicable) needs sign-off from the evaluating ophthalmologists. 04 speaks in ranges ("1–2 years").
- **The report box:** a plain-language box on page 1 of the report containing:
  - the result in one sentence;
  - "a snapshot of today, not a guarantee";
  - the ophthalmologist's interval, if one was given;
  - the optician's name and address.
  - The box comes in the customer's `preferred_language` from fixed, medically approved sentence templates. The rest of the report stays in German.
- **Not included:** no consent re-ask, because A sends nothing that consent would be needed for.

**B. A + automatic reminder in the optician's name. Trigger: automatic e-mail.**
- **Everything in A.**
- **Consent re-ask:** on the report download page, one unticked checkbox: "Remind me when my next screening is due, from [Optician name]."
- **The reminder e-mail:**
  - Sent 4 weeks before the stated interval ends.
  - Only to customers with `marketing_consent` (original or re-asked).
  - Sender name, signature and booking link are the optician's; Mirantus sends on their behalf.
  - The copy repeats only the ophthalmologist's interval, without fear.
- **Optician:** opts in through a contract addendum or a simple form; we know of no partner portal. Nothing to configure: name and address come from location data. Opt-out at any time. No CRM or cash-register integration.

**C. A + optional "who is due" list. Trigger: the optician calls.**
- **Everything in A,** plus the consent re-ask from B.
- **The list:** a new web view for opticians showing consenting customers whose stated interval ends this month, with contact details. Staff may call. Nothing is sent automatically.
- **New surface:** no partner portal is known to exist, so this needs login, roles and access control.

## Comparison

| | A. Interval in report | B. A + optician-named e-mail reminder | C. A + optional due list |
|---|---|---|---|
| **Expected effect on 40+ metric (evidence)** | **Small/unknown.** One optician's belief, survey 6: "Wenn im Befund steht „Nächstes Screening in 12 Monaten", dann glauben die Leute das auch." → "If the report says 'Next screening in 12 months', people will believe it." The box is seen only by people who open the report (64.7% of 40+, n=6,279). No data on behaviour change | **Plausible but unproven.** For: consent+opened 8.7% (n=876) vs neither 2.6% (n=392), correlation only; 01 · "Wenn Herr K. sagt, ich soll wieder kommen, dann komm ich wieder." → "If Mr K. tells me to come back, I'll come back." **Against:** optician *e-mail* follow-up today shows no clear lift, email+consent 6.6% (n=438) vs none+consent 5.4% (n=754), CIs overlap (self-reported label, without a stated interval). 02 (a referral customer, outside the target) wants a reminder ("I will forget otherwise") but "not from the optician … from whoever has my results" | **Depends on stores calling.** Phone+consent 11.0% (n=191) vs none+consent 5.4% (n=754), self-reported label, low confidence. The same label caveat applies to B's evidence. Survey 9 · "Wir haben keine Zeit, Kunden anzurufen." → "We have no time to call customers." 03 and survey 3 say they would call |
| **Reach (legally contactable)** | Every customer receives the report, but only openers see the box: 64.7% of 40+ (n=6,279). Non-German speakers open less often: 37.8% (all customers, n=1,633) | The report box reaches the same as A. **The reminder** reaches only customers with consent: 53.4% of 40+ (n=6,279), plus re-ask opt-ins at an unknown rate. The re-ask on the download page misses non-openers: 16.5% of 40+ have neither consent nor an opened report (n=6,279) | Same legal reach as B, limited to stores that use the list. Phone contact may need its own consent: "reminders and offers" doesn't name a channel |
| **Constraint fit** | Good. The interval comes from the ophthalmologist, in the report. No new message, no store work | Good, **if** the consent covers reminders sent on the optician's behalf (legal question). The optician's name is on it ✓. Opt-in only ✓. No integration ✓ | Optional tool ✓. Risk: phone calls without channel consent; staff turnover (03, survey 12) |
| **Effort (2 eng, 1 design, 1 PM; ~13 weeks)** | **~4–5 weeks:** form field, PDF box, 6-language templates, tracking. External: medical sign-off and translation of the templates | **~10 weeks:** A + re-ask and consent record + scheduler + optician-branded template + opt-in form + unsubscribe + booking link. External: the legal ruling in week 1 | **~11–13 weeks:** A + re-ask + a new authenticated optician-facing surface. Little or no buffer |
| **Riskiest assumptions** | Customers read and act on the box (A2). Ophthalmologists fill in the field (A4). Intervals stay generic without risk factors (A7) | As A, plus: customers recognise and trust an optician-named mail about their results (A3, C1); the consent scope covers it (legal); opticians opt in | As A, plus: stores call (C4); older customers don't find the call pushy (C2, A8) |

### What the pilot can and cannot show
- **Early indicators readable within weeks:**
  - **A:** interval coverage, comprehension, and opened ≤5 days (03).
  - **B only:** the **re-ask opt-in rate** ("remind me … from [Optician name]") and, in the 2-week test, whether customers recognise and would act on an optician-named reminder mock-up. These are the only early signals that separate B from A. The first real reminders go out 4 weeks before each stated interval ends, i.e. long after this quarter.
- **Power:** two arms at the 5.5% baseline (01 §9):
  - independents, 1 quarter of screenings (n=834): MDE ~4.4 pp;
  - all locations, 1 quarter (n=1,570): MDE ~3.2 pp.
  - These are **lower bounds**. Randomising by location, opt-in stores only, and reaching only the ~53% with consent all raise the MDE.
  - The largest observed gap we could build on is 40+ consent vs no consent, 6.6% vs 4.1% (2.5 pp). It is below every one-quarter MDE.
  - **One cohort-quarter cannot prove B on the return rate.** The go/no-go has to rest on the leading indicators. The return read needs several quarters of cohorts.
- **Selection bias:** stores that opt in may already be the "phone" stores. Randomise among stores that opt in, not against stores that don't.

### Metric conflict, a decision for Lars at CP2
- The CP1 metric counts a return within 15 months.
- 04's general guidance for 40+ is 1–2 years. A customer told 24 months who comes back on time counts as "not returned". B could work as designed and leave the metric flat.
- The 03 "target definition" (returned within the stated interval + 3 months) solves this. It can only be measured for customers who have an interval, i.e. after A ships.
- Options:
  - (i) the pilot's success measure is interval-adherent return, and the 15-month 40+ metric stays the company-level trend;
  - (ii) read the 15-month metric only for customers who were given 12 months.

## Recommendation: B, piloted at opted-in independents

**Why B:**
- It is the only option that reaches the customer at the moment they would return, with a reason that comes from the ophthalmologist.
- It needs no store work, which survey 9 requires. It carries the optician's name, as 03 and survey 4 want.
- It uses the permission that customers with consent already gave and which is unused today (C11).

**Why not C:**
- It needs store time that survey 9 says some stores don't have.
- It needs a new authenticated surface, which is the biggest build.
- Phone consent is unclear.
- Its only evidence is the same self-reported label that is flat for e-mail.

**What ships first:**
1. Week 1: the legal and medical checks below.
2. The interval field.
3. The page-1 report box (6 languages).
4. Tracking for the leading indicators.
5. Consent re-ask + optician opt-in form.
6. The reminder scheduler and the optician-named template. This is conditional on the legal answer. **Fallback if legal blocks it or the work slips: ship A plus the re-ask only.**

**Cut:**
- **C**, for the reasons above. Revisit if pilot opticians ask for it.
- **Full report translation or a plain-language rewrite.** Too big for the quarter; the page-1 box carries the key sentence.
- **SMS/WhatsApp** (02, survey 14). It needs phone numbers and channel consent.
- **Reminders for the 2025 backlog.** There is no ophthalmologist interval for them.
- **A risk-factor questionnaire** (A7). It touches the 15-minute slot and the store workflow.
- **Chains.** They need HQ sign-off (survey 7).
- **Mobile units.** Low return (1.6%, n=188, 3 returns) and lower consent (38.5%, n=460, all customers). Whether their customers can return to a unit is unknown.
- **"Come yearly" posters** (survey 8). A blanket interval is unresolved under C7.
- **Price bundles** (survey 10). That is the optician's commercial decision.

**External dependencies (week 1–3):**

| Dependency | Owner |
|---|---|
| Consent scope for reminders on the optician's behalf; controller | Legal |
| Is the download page a legitimate place for the re-ask, or must it sit in E-mail 3? | Legal |
| The interval choice set and the template sentences | Medical lead / evaluating ophthalmologists |
| Translations of the templates | Medical lead (medically reviewed) |
| Pilot opticians | Partner team |
