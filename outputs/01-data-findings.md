# 01 Data findings

Summary: Few customers come back so far. 4.8% of non-referral customers return within 15 months (Jan–Jun 2025 cohorts, n=3,170), and returns cluster at months 10–15.
Return is associated with opening the report, consent, minor findings, age 60+ and self-reported phone follow-up. Non-German speakers open the report far less often (37.8% vs 71.8% for German speakers).
Only 54.2% of customers can legally get a reminder (38.5% at mobile units). Locations differ little beyond chance. All data is synthetic and all associations are correlational.

Inputs used: `data/screenings.csv`, `data/README.md`, `CLAUDE.md`, `data/constraints.md`, `data/customer-journey.md` (context only).
Script: `scripts/analyze.py` (Python 3.9, standard library; pandas not installed). Tables: `outputs/tables/*.csv`.
Export date constant: 2026-09-30. Every number below is printed by the script; section refs (§) point to its output.

## 0. Input check against the data dictionary (§1)
- **No differences found.** 14 columns as documented, no new or missing ones. 9,000 rows, unique `customer_id`, all first screenings in 2025, every category value as documented, export date 2026-09-30 consistent (latest `second_screening_date` = 2026-09-30).
- Consistency checks are all 0: no second screening on/before the first or after export, `report_opened` and `report_opened_days_after` always agree, `referral_booked` is set only for `referral_recommended`. Each of the 60 locations has exactly one (type, city, follow_up).
- **Oddity:** `report_opened_days_after` only takes the values 0, 1, 2, 3, 5, 9. It looks binned or synthetic. Treat "days to open" as coarse.
- Population: 8,116 non-referral customers (unremarkable + minor_findings) and 884 `referral_recommended` customers, analysed separately.
- Pooled, censored count of anyone back by the export date: 304. **This is not a metric.**

## 1. Observation window and time to return (§2, §3)
- Observation time runs from 20 months (Jan 2025 cohort) to 9 months (Dec 2025). The full 12 / 15 / 18-month windows exist only for the Jan–Sep / Jan–Jun / Jan–Mar 2025 cohorts.
- **No one returns before month 7.** Earliest return: 199 days after the first screening. Median: 380 days.
- In the cohorts with at least 18 months observed (Jan–Mar 2025, n=1,574, 105 returners), the median is 13 completed months. 33.3% of returners came back within <12 completed months, 78.1% within <15 and 97.1% within <18.
- Same cohort (Jan–Mar, non-referral, n=1,426): the return rate is 2.4% within 12 months, 5.3% within 15 and 6.7% within 18. A 12-month window catches only 34/96 = 35.4% of 18-month returners; a 15-month window catches 76/96 = 79.2%.
- Implication for measurement: returns are near zero until month 9 (0.2% returned within 9 months, n=8,116 non-referral). Any leading indicator has to be a proxy (see §2 of this file).

## 2. Metric proposal and baseline (§4)
**Proposed metric: 15-month return rate.** It is the share of non-referral customers (unremarkable + minor_findings) whose next mira screening falls within 15 months of their first, counted only for customers whose full 15-month window has passed.

| Population | 12 m | 15 m | 18 m |
|---|---|---|---|
| Non-referral | 2.1% (n=5,209; Jan–Sep; CI 1.7–2.5) | **4.8% (n=3,170; Jan–Jun; CI 4.1–5.6)** | 6.7% (n=1,426; Jan–Mar; CI 5.5–8.2) |
| referral_recommended | 1.2% (n=564) | 3.5% (n=341) | 4.1% (n=148) |

- **Why 15 months:** observed returns peak at 10–15 months, and 12 months cuts the curve at its steepest point (35.4% of 18-month returners captured). 15 months captures 79.2% of them, with n=3,170 instead of 1,426 at 18 months. 18 months gives the best coverage, but only one quarter of cohorts qualifies and it reads a quarter later.
- **The window is a measurement choice, not a medical interval.** The right interval per customer can only come from the ophthalmologist. If the ophthalmologist states different intervals by result, the window should follow them.
- **Excluded:** `referral_recommended` customers (their next step is an ophthalmologist; track `referral_booked` instead, 50.5% booked, n=884), and customers whose window has not yet passed (Jul–Dec 2025 first screenings for 15 months).
- **Baseline: 4.8%** (non-referral, Jan–Jun 2025 cohorts, n=3,170, 95% CI 4.1–5.6%). Cohort drift at 12 months is small: Q1 2.4%, Q2 1.8%, Q3 2.1% with overlapping CIs.
- **Leading indicator candidates (readable within days):** report open rate (65.6% non-referral, n=8,116) and consent rate (54.0% non-referral). Both are associated with return (see §3 below). Neither is shown to cause it. The cumulative curve (`outputs/tables/cumulative_return_curve_nonreferral.csv`) gives an intermediate read at 12 months.

## 3. Return rate by segment (§5; non-referral, 15-month window, Jan–Jun 2025 cohorts unless stated)
Full 12/15/18-month values are in `outputs/tables/segment_*.csv` and `interaction_*.csv`.

| Cut | Segment: rate (n) | Confidence |
|---|---|---|
| result_category | minor_findings 9.4% (742) vs unremarkable 3.4% (2,428); at 18 months 14.4% vs 4.4% | High (CIs don't overlap at any window) |
| report_opened | opened 6.1% (2,054) vs never 2.4% (1,116); at 12 months 2.8% vs 0.6% | High (association) |
| days to open | 0–1 d 6.6% (1,041), 2–3 d 5.7% (492), 4+ d 5.6% (521), never 2.4% (1,116) | Low: the gradient among openers sits inside overlapping CIs; the step is opened vs never |
| marketing_consent | yes 5.6% (1,788) vs no 3.8% (1,382) | Medium (CIs overlap slightly: 4.7–6.8 vs 2.9–4.9) |
| consent × opened | consent+opened 7.3% (1,159); no consent+opened 4.6% (895); consent+not opened 2.5% (629); neither 2.3% (487) | Medium |
| age_band | 60+ 6.5% (1,145), 40–59 4.7% (1,307), 18–39 2.5% (718) | Medium-high (60+ vs 18–39 CIs separate) |
| location_type | independent 5.5% (1,703), chain 4.4% (1,279), mobile 1.6% (188) | Medium for mobile (n=188, only 3 returns); low for independent vs chain |
| optician_follow_up (**self-reported**) | phone 7.5% (389), email 4.8% (1,018), none 4.3% (1,763) | Low-medium. Phone sits almost entirely at independents. Within independents: phone 7.2% (360) vs none 5.2% (783), CIs overlap. Chain+phone n=29 [n<100] |
| follow_up × consent | phone+consent 10.4% (240) vs phone+no consent 2.7% (149); email/none show smaller consent gaps (5.3 vs 4.1; 4.7 vs 3.8) | Low: consistent with optician follow-up only reaching consenting customers, but small n |
| preferred_language | de 5.1% (2,592); en 3.7% (187); tr 5.7% (159); ru 2.0% (98) [n<100]; pl 0.0% (70) [n<100]; ar 3.1% (64) [n<100] | Low: all non-de groups are small with wide CIs |
| language × opened | de: opened 6.2% (1,844) vs not 2.4% (748); non-de: opened 5.2% (210) vs not 2.4% (368) | Medium: the gap follows opening more than language |

**Referral_recommended (separate, §5b):** 50.5% booked a partner appointment (446/884). Booking: report opened 61.7% (n=577, CI 57.7–65.6) vs not opened 29.3% (n=307, CI 24.5–34.6), high confidence for the association. By language: de 53.6% (n=722); every non-de group is n<100 (en 32.8%, n=61; tr 35.4%, n=48). Second mira screenings in this group are few (12 of 341 within 15 months), so there is no useful split by `referral_booked` (n<100 at 18 months).

## 4. Reach: who may legally receive a reminder (§6)
- **54.2% of all 2025 customers gave marketing_consent (4,880/9,000).** Non-referral: 54.0% (4,386/8,116).
- By location type: independent 55.9% (n=4,825), chain 54.0% (n=3,715), **mobile unit 38.5% (n=460)**.
- Other cuts are flat: age 52.3–56.2%, language 49.4% (tr, n=474) to 57.9% (ru, n=266), result 54.0–55.9%, follow_up label 52.8–57.4%.
- Non-referral, consent × opened: consent and opened 35.6% (2,889); no consent but opened 30.1% (2,439); no consent and never opened 15.9% (1,291). The last group is reachable only through service messages, which they also tend not to open.

## 5. Report engagement (§7, all customers)
- Open rate: 65.6% overall (n=9,000). **de 71.8% (n=7,367) vs non-de 37.8% (n=1,633)**: en 39.0%, tr 37.6%, ru 38.0%, pl 40.9%, ar 31.8% (pl n=181, ar n=179). Confidence: high. The report is German only; the data cannot show whether language causes the gap.
- By age: 18–39 68.6%, 40–59 67.4%, 60+ 61.6%. Language × age: de 60+ 67.2% (n=2,641); non-de 60+ 34.2% (n=546).
- Opened within 1 day: de 36.0% vs 16.8–23.8% for non-de languages. Median days to open is 1–2 everywhere (coarse field).
- Open rate does not differ by result category (64.7–66.0%), so customers with referral or minor findings open no more often.

## 6. Spread across locations (§8)
- Every location is small in the 15-month window (22–94 eligible customers, all n<100). Locations were therefore compared on cohort-adjusted observed/expected (O/E) returns by export, using all 8,116 non-referral customers.
- **No small set of locations drives returns.** Sum of z² = 66.4 on ~59 df, close to chance. 3 locations have z>1.96 (L033, L054, L059), and about 3 are expected by chance. The top 10 locations by returns hold 35.4% of returns and 23.0% of customers, while their expected share is 22.9%. That is a moderate tilt, not concentration.
- Bottom O/E: the three lowest locations are mobile units (L002, L003, L004), each with 0 returns against an expected count of 2.5–2.8.
- **Self-reported label vs outcome:** phone locations have a pooled O/E of 1.58 (7 locations, 6/7 above 1, minimum 0.96). Email locations have 1.02 (18 locations, range 0.23–1.68; 7/18 sit at or below the median "none" location). None locations have 0.86. The "phone" label is consistent with outcomes. The "email" label shows no measurable difference from "none", which could mean email follow-up has no effect, or that the self-report is inaccurate.

## 7. Limits
- **Synthetic data**: patterns illustrate the case and are not real Mirantus figures.
- **Censoring:** returns are only visible up to 2026-09-30, and the latest cohorts are unusable for fixed windows. The 18-month figures rest on one quarter (n=1,426 non-referral).
- **Few events:** 153 returns in the 15-month baseline. Many segment cells have under 30 returns, and ru, pl and ar in the 15-month window, as well as mobile units at 18 months, are n<100.
- **Self-reported** `optician_follow_up`: from a partner survey, one value per location, no dates, no dose. It is confounded with location type (phone: 1,058 of 1,148 customers at independents).
- **Correlation, not cause:** opening, consent, age and findings are likely markers of underlying engagement or health concern. Establishing cause would need a randomised test, e.g. randomising a report or e-mail change (or an optician-branded reminder to consenting customers) at the customer or location level and comparing the return rate and its leading indicator.
- Not in the data: where the second screening happened (same optician or another), whether an ophthalmologist visit replaced a screening, booking channel, e-mail opens of the "result ready" e-mail, and the interval each ophthalmologist recommended (none today, per `customer-journey.md`).
- `report_opened_days_after` takes only 6 distinct values, so days-to-open analysis is coarse.

## 8. Open questions for the research synthesis
1. What interval does the ophthalmologist consider sensible per result category? Does it support a 15-month window, or different windows for unremarkable vs minor findings?
2. Why do non-German speakers open the German report so rarely, and is the report or the e-mail the barrier?
3. What do "phone" opticians actually do, to whom (consenting customers only?) and when? Do "email" opticians really send e-mails?
4. Do customers who return at ~13 months do so because of an optician prompt, their own habit, or a glasses purchase cycle?
5. Why is consent lower at mobile units (38.5%), and can those customers return at all without a fixed store?
6. Do referral customers who didn't open the report (29.3% booked) know they were referred?

## 9. Addendum (added in step 3, same script, §5 output)
Non-referral, Jan–Jun 2025 cohorts, 15-month window unless stated. Tables: `interaction_result_x_age.csv`, `segment_age_40plus.csv`, `interaction_40plus_x_consent.csv`.
- **Result × age:** unremarkable 60+ 4.9% (n=878), unremarkable 40–59 3.0% (n=990), unremarkable 18–39 1.8% (n=560); minor_findings 60+ 11.6% (n=267), 40–59 9.8% (n=317), 18–39 5.1% (n=158). At 18 months, minor_findings 18–39 is n=77 [n<100].
- **Metric scope option, 40+ vs 18–39:** 40+ 5.5% (n=2,452, CI 4.7–6.5); 18–39 2.5% (n=718, CI 1.6–3.9). At 12 / 18 months, 40+ is 2.3% (n=4,017) / 7.4% (n=1,108).
- **40+ × consent:** consent 6.6% (n=1,383, CI 5.4–8.0) vs no consent 4.1% (n=1,069, CI 3.1–5.5).
- **Report opened within ≤5 days** (non-referral, all 2025 cohorts; the field has no values between 5 and 9, so "within 7 days" equals "≤5"): 57.2% (n=8,116, CI 56.2–58.3); de 62.6% (n=6,645); non-de 33.0% (n=1,471); 40+ 56.1% (n=6,279). Script §9.
- **60+ × self-reported follow-up** (15 months): phone 9.5% (n=126, CI 5.5–15.9), email 7.5% (n=360), none 5.3% (n=659, CI 3.8–7.3). CIs overlap. At 18 months, phone is n=55 [n<100]. Table `interaction_60plus_x_followup.csv`.
- **Consent among non-referral 40+** (all 2025 cohorts): 53.4% (3,355/6,279); unremarkable 53.3% (n=4,750); minor findings 54.0% (n=1,529).
- **Minimum detectable effect** (two-arm 50/50, alpha .05, power .8, 40+ baseline 5.5%; volume per quarter = 2025 volume / 4):
  - independents only: 1 quarter of screenings n=834 → ~4.4 pp; 2 quarters n=1,668 → ~3.1 pp; 4 quarters n=3,336 → ~2.2 pp.
  - all locations: 1 quarter n=1,570 → ~3.2 pp; 2 quarters n=3,140 → ~2.3 pp; 4 quarters n=6,279 → ~1.6 pp.
- **40+ non-referral, consent × opened** (15 months): consent+opened 8.7% (n=876); no consent+opened 5.0% (n=677); consent+not opened 3.0% (n=507); neither 2.6% (n=392). Report ever opened, 40+ (all 2025 cohorts): 64.7% (4,063/6,279). Neither consent nor opened: 16.5% (1,039/6,279).
- **40+ non-referral, self-reported follow-up × consent** (15 months): email+consent 6.6% (n=438) vs none+consent 5.4% (n=754), with overlapping CIs; phone+consent 11.0% (n=191); phone without consent 3.7% (n=109). Low confidence: the label is self-reported.
- **referral_booked by location type** (all 2025): independent 49.9% (239/479, CI 45.4–54.4); chain 52.4% (189/361); mobile 40.9% (18/44) [n<100].
