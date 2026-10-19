#!/usr/bin/env python3
"""Mirantus case, step 1: reproducible analysis of data/screenings.csv.

Standard library only (pandas is not installed in this environment).
Run:  python3 scripts/analyze.py
Prints every number used in outputs/01-data-findings.md and writes CSV tables
to outputs/tables/. All data is synthetic.
"""
import csv
import datetime as dt
import math
import os
import statistics
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
EXPORT_DATE = dt.date(2026, 9, 30)          # from data/README.md; change here only
WINDOWS = [12, 15, 18]                      # return windows in months
PRIMARY_WINDOW = 15                         # proposed metric window (see findings)
SMALL_N = 100                               # flag groups below this size

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "screenings.csv")
TABLES = os.path.join(ROOT, "outputs", "tables")

EXPECTED_COLUMNS = [
    "customer_id", "location_id", "location_type", "city", "optician_follow_up",
    "first_screening_date", "age_band", "preferred_language", "result_category",
    "report_opened", "report_opened_days_after", "marketing_consent",
    "referral_booked", "second_screening_date",
]
EXPECTED_CATEGORIES = {
    "location_type": {"optician_chain", "independent_optician", "mobile_unit"},
    "optician_follow_up": {"none", "email", "phone"},
    "age_band": {"18-39", "40-59", "60+"},
    "preferred_language": {"de", "en", "tr", "ru", "ar", "pl"},
    "result_category": {"unremarkable", "minor_findings", "referral_recommended"},
    "report_opened": {"true", "false"},
    "marketing_consent": {"true", "false"},
    "referral_booked": {"true", "false", ""},
}
ORDER = {
    "location_type": ["independent_optician", "optician_chain", "mobile_unit"],
    "optician_follow_up": ["none", "email", "phone"],
    "age_band": ["18-39", "40-59", "60+"],
    "preferred_language": ["de", "en", "tr", "ru", "pl", "ar"],
    "result_category": ["unremarkable", "minor_findings", "referral_recommended"],
    "report_opened": ["true", "false"],
    "marketing_consent": ["true", "false"],
    "referral_booked": ["true", "false"],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def add_months(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    y += d.year
    mo += 1
    last = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1]
    return dt.date(y, mo, min(d.day, last))


def months_between(a, b):
    """Whole calendar months completed from a to b (b >= a)."""
    m = (b.year - a.year) * 12 + (b.month - a.month)
    if add_months(a, m) > b:
        m -= 1
    return m


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (c - h, c + h)


def pct(x):
    return "n/a" if x != x else f"{100 * x:.1f}%"


def flag(n):
    return " [n<100]" if n < SMALL_N else ""


def write_table(name, header, rows):
    os.makedirs(TABLES, exist_ok=True)
    with open(os.path.join(TABLES, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow([f"{v:.4f}" if isinstance(v, float) else v for v in r])


def section(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# Load + data quality
# ---------------------------------------------------------------------------
with open(DATA, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    columns = reader.fieldnames
    raw = list(reader)

section("1. SCHEMA AND DATA QUALITY")
print(f"Export date constant: {EXPORT_DATE}")
print(f"Rows: {len(raw)}")
missing_cols = [c for c in EXPECTED_COLUMNS if c not in columns]
new_cols = [c for c in columns if c not in EXPECTED_COLUMNS]
print(f"Missing columns vs dictionary: {missing_cols or 'none'}")
print(f"New columns vs dictionary: {new_cols or 'none'}")
for col, allowed in EXPECTED_CATEGORIES.items():
    vals = Counter(r[col] for r in raw)
    unexpected = {v: n for v, n in vals.items() if v not in allowed}
    print(f"  {col}: {dict(sorted(vals.items()))}  unexpected={unexpected or 'none'}")

empties = {c: sum(1 for r in raw if r[c] == "") for c in columns}
print("Empty values per column:", {c: n for c, n in empties.items() if n})
print("Duplicate customer_id:", len(raw) - len({r['customer_id'] for r in raw}))

issues = Counter()
rows = []
for r in raw:
    d1 = dt.date.fromisoformat(r["first_screening_date"])
    d2 = dt.date.fromisoformat(r["second_screening_date"]) if r["second_screening_date"] else None
    if d1.year != 2025:
        issues["first_screening not in 2025"] += 1
    if d2 and d2 <= d1:
        issues["second_screening on/before first"] += 1
    if d2 and d2 > EXPORT_DATE:
        issues["second_screening after export date"] += 1
    if r["report_opened"] == "true" and r["report_opened_days_after"] == "":
        issues["opened=true but days_after empty"] += 1
    if r["report_opened"] == "false" and r["report_opened_days_after"] != "":
        issues["opened=false but days_after set"] += 1
    if r["report_opened_days_after"] and int(r["report_opened_days_after"]) < 0:
        issues["days_after negative"] += 1
    if r["result_category"] == "referral_recommended" and r["referral_booked"] == "":
        issues["referral_recommended but referral_booked empty"] += 1
    if r["result_category"] != "referral_recommended" and r["referral_booked"] != "":
        issues["non-referral but referral_booked set"] += 1
    rows.append(dict(r, d1=d1, d2=d2,
                     obs_months=months_between(d1, EXPORT_DATE),
                     ttr=months_between(d1, d2) if d2 else None,
                     ttr_days=(d2 - d1).days if d2 else None))
print("Consistency checks (0 = clean):")
for k in ["first_screening not in 2025", "second_screening on/before first",
          "second_screening after export date", "opened=true but days_after empty",
          "opened=false but days_after set", "days_after negative",
          "referral_recommended but referral_booked empty",
          "non-referral but referral_booked set"]:
    print(f"  {k}: {issues[k]}")

# location attributes stable per location_id?
loc_attrs = defaultdict(set)
for r in rows:
    loc_attrs[r["location_id"]].add((r["location_type"], r["city"], r["optician_follow_up"]))
inconsistent = [l for l, s in loc_attrs.items() if len(s) > 1]
print(f"Locations: {len(loc_attrs)}; with >1 (type, city, follow_up) combination: {len(inconsistent)}")
loc_type_counts = Counter(next(iter(s))[0] for s in loc_attrs.values())
loc_fu_counts = Counter(next(iter(s))[2] for s in loc_attrs.values())
print(f"Locations by type: {dict(loc_type_counts)}")
print(f"Locations by self-reported follow_up: {dict(loc_fu_counts)}")
days_vals = Counter(r["report_opened_days_after"] for r in rows if r["report_opened_days_after"])
print(f"Distinct report_opened_days_after values: {sorted(days_vals, key=int)} "
      f"counts={dict(sorted(days_vals.items(), key=lambda kv: int(kv[0])))}")
print(f"second_screening_date range: {min(r['d2'] for r in rows if r['d2'])} .. "
      f"{max(r['d2'] for r in rows if r['d2'])}")
print(f"Customers with any second screening by export (pooled, censored, NOT a metric): "
      f"{sum(1 for r in rows if r['d2'])}")

NONREF = [r for r in rows if r["result_category"] != "referral_recommended"]
REF = [r for r in rows if r["result_category"] == "referral_recommended"]
print(f"Non-referral customers (unremarkable + minor_findings): {len(NONREF)}; "
      f"referral_recommended: {len(REF)}")


def eligible(rs, w):
    """Customers whose first screening + w months <= export date (full window observed)."""
    return [r for r in rs if add_months(r["d1"], w) <= EXPORT_DATE]


def returned(r, w):
    return r["d2"] is not None and r["d2"] <= add_months(r["d1"], w)


def rate(rs, w):
    e = eligible(rs, w)
    k = sum(1 for r in e if returned(r, w))
    lo, hi = wilson(k, len(e))
    return len(e), k, (k / len(e) if e else float("nan")), lo, hi


# ---------------------------------------------------------------------------
# 2. Observation window per cohort
# ---------------------------------------------------------------------------
section("2. OBSERVATION WINDOW PER COHORT (month of first screening)")
cohort_rows = []
print(f"{'cohort':8} {'n':>5} {'obs_mo min-max':>15} " +
      " ".join(f"{'full'+str(w)+'m':>8}" for w in WINDOWS) + f" {'any_return_so_far':>18}")
by_month = defaultdict(list)
for r in rows:
    by_month[r["first_screening_date"][:7]].append(r)
for m in sorted(by_month):
    rs = by_month[m]
    om = [r["obs_months"] for r in rs]
    full = [len(eligible(rs, w)) for w in WINDOWS]
    anyret = sum(1 for r in rs if r["d2"])
    print(f"{m:8} {len(rs):>5} {min(om):>7}-{max(om):<7} " +
          " ".join(f"{x:>8}" for x in full) + f" {anyret:>18}")
    cohort_rows.append([m, len(rs), min(om), max(om)] + full + [anyret])
write_table("cohort_observation.csv",
            ["cohort_month", "n", "obs_months_min", "obs_months_max"] +
            [f"full_window_{w}m" for w in WINDOWS] + ["any_second_screening_by_export"],
            cohort_rows)
for w in WINDOWS:
    print(f"Full {w}-month window = first screening on/before "
          f"{max(r['d1'] for r in rows if add_months(r['d1'], w) <= EXPORT_DATE)}")

# ---------------------------------------------------------------------------
# 3. Time to return
# ---------------------------------------------------------------------------
section("3. TIME TO RETURN")
ret = [r for r in rows if r["d2"]]
print(f"Returners (any cohort, censored): {len(ret)}")
print(f"Days first->second: min {min(r['ttr_days'] for r in ret)}, "
      f"median {statistics.median(r['ttr_days'] for r in ret)}, "
      f"max {max(r['ttr_days'] for r in ret)}")
# Uncensored-ish view: cohorts with >= 18 months of observation (Jan-Mar 2025)
early = [r for r in rows if r["obs_months"] >= 18]
early_ret = [r for r in early if r["d2"]]
print(f"Cohorts with >=18 months observed: n={len(early)}, returners={len(early_ret)}")
hist = Counter(r["ttr"] for r in early_ret)
cum = 0
ttr_rows = []
print(f"{'month':>5} {'returns':>8} {'cum_share_of_returners':>24}")
for m in range(0, max(hist) + 1):
    cum += hist[m]
    print(f"{m:>5} {hist[m]:>8} {pct(cum / len(early_ret)):>24}")
    ttr_rows.append([m, hist[m], cum / len(early_ret)])
write_table("time_to_return_cohorts_obs18plus.csv",
            ["completed_months_to_return", "returns", "cum_share_of_returners"], ttr_rows)
print("Median completed months to return (>=18m cohorts):",
      statistics.median(r["ttr"] for r in early_ret))
print("Share of these returners back within <9 / <12 / <15 / <18 completed months: " +
      ", ".join(pct(sum(1 for r in early_ret if r["ttr"] < k) / len(early_ret))
                for k in (9, 12, 15, 18)))

# Cumulative return curve: for month k, customers with >= k months observed
print("\nCumulative return curve (non-referral). At k months: among customers observed >= k "
      "months, share returned within k months.")
curve_rows = []
for k in range(3, 21):
    e = [r for r in NONREF if add_months(r["d1"], k) <= EXPORT_DATE]
    if not e:
        continue
    kk = sum(1 for r in e if returned(r, k))
    lo, hi = wilson(kk, len(e))
    print(f"  k={k:>2}: n={len(e):>5} returned={kk:>4} rate={pct(kk / len(e))} "
          f"[{pct(lo)}-{pct(hi)}]")
    curve_rows.append([k, len(e), kk, kk / len(e), lo, hi])
write_table("cumulative_return_curve_nonreferral.csv",
            ["months_k", "n_observed_k", "returned_within_k", "rate", "ci_lo", "ci_hi"],
            curve_rows)

# ---------------------------------------------------------------------------
# 4. Return rate by window (sensitivity)
# ---------------------------------------------------------------------------
section("4. RETURN RATE WITHIN FIXED WINDOW (full-window customers only)")
sens_rows = []
for label, rs in [("non_referral", NONREF), ("referral_recommended", REF), ("all", rows)]:
    for w in WINDOWS:
        n, k, p, lo, hi = rate(rs, w)
        cohorts = sorted({r["first_screening_date"][:7] for r in eligible(rs, w)})
        print(f"{label:22} {w}m: cohorts {cohorts[0]}..{cohorts[-1]} n={n} returned={k} "
              f"rate={pct(p)} [95% CI {pct(lo)}-{pct(hi)}]{flag(n)}")
        sens_rows.append([label, w, f"{cohorts[0]}..{cohorts[-1]}", n, k, p, lo, hi])
write_table("return_rate_by_window.csv",
            ["population", "window_months", "cohorts", "n", "returned", "rate", "ci_lo", "ci_hi"],
            sens_rows)

# Same-cohort comparison to separate window effect from cohort effect
print("\nSame cohort (Jan-Mar 2025, non-referral) under each window:")
jm = [r for r in NONREF if r["first_screening_date"] < "2025-04-01"]
for w in WINDOWS:
    n, k, p, lo, hi = rate(jm, w)
    print(f"  {w}m: n={n} returned={k} rate={pct(p)} [{pct(lo)}-{pct(hi)}]")
k18 = rate(jm, 18)[1]
print("  Share of the 18m returners already back within 12m / 15m: " +
      ", ".join(f"{rate(jm, w)[1]}/{k18} = {pct(rate(jm, w)[1] / k18)}" for w in (12, 15)))
print("Quarterly cohorts, non-referral, 12m window:")
for q, (a, b) in {"Q1": ("2025-01", "2025-03"), "Q2": ("2025-04", "2025-06"),
                  "Q3": ("2025-07", "2025-09")}.items():
    qs = [r for r in NONREF if a <= r["first_screening_date"][:7] <= b]
    n, k, p, lo, hi = rate(qs, 12)
    print(f"  {q} 2025: n={n} returned={k} rate={pct(p)} [{pct(lo)}-{pct(hi)}]")


# ---------------------------------------------------------------------------
# 5. Segment cuts
# ---------------------------------------------------------------------------
def seg_table(rs, key, name, title, order=None):
    groups = defaultdict(list)
    for r in rs:
        groups[key(r)].append(r)
    keys = order or sorted(groups)
    out = []
    print(f"\n{title}")
    for g in keys:
        if g not in groups:
            continue
        line = [g]
        txt = f"  {str(g):24}"
        for w in WINDOWS:
            n, k, p, lo, hi = rate(groups[g], w)
            line += [n, k, p, lo, hi]
            txt += f" | {w}m n={n:>5} k={k:>3} {pct(p):>6} [{pct(lo)}-{pct(hi)}]{flag(n)}"
        print(txt)
        out.append(line)
    hdr = ["segment"]
    for w in WINDOWS:
        hdr += [f"n_{w}m", f"returned_{w}m", f"rate_{w}m", f"ci_lo_{w}m", f"ci_hi_{w}m"]
    write_table(name, hdr, out)
    return out


section("5. RETURN RATE BY SEGMENT (non-referral customers unless stated)")
for col in ["location_type", "optician_follow_up", "age_band", "preferred_language",
            "result_category", "marketing_consent", "report_opened"]:
    seg_table(NONREF, lambda r, c=col: r[c], f"segment_{col}.csv",
              f"-- {col} (non-referral)", ORDER[col])


def days_bucket(r):
    if r["report_opened"] != "true":
        return "never"
    d = int(r["report_opened_days_after"])
    return "0-1" if d <= 1 else ("2-3" if d <= 3 else "4+")


seg_table(NONREF, days_bucket, "segment_report_opened_days.csv",
          "-- report_opened_days_after bucket (non-referral)", ["0-1", "2-3", "4+", "never"])
seg_table(NONREF, lambda r: r["report_opened_days_after"] or "never",
          "segment_report_opened_days_exact.csv",
          "-- report_opened_days_after exact (non-referral)",
          ["0", "1", "2", "3", "5", "9", "never"])
seg_table(NONREF, lambda r: f"consent={r['marketing_consent']}|opened={r['report_opened']}",
          "interaction_consent_x_opened.csv", "-- consent x report_opened (non-referral)")
seg_table(NONREF, lambda r: f"{r['location_type']}|{r['optician_follow_up']}",
          "interaction_loctype_x_followup.csv",
          "-- location_type x self-reported follow_up (non-referral)")
seg_table(NONREF, lambda r: f"{'de' if r['preferred_language']=='de' else 'non-de'}"
          f"|opened={r['report_opened']}",
          "interaction_language_x_opened.csv", "-- language (de/non-de) x opened (non-referral)")
seg_table(NONREF, lambda r: f"{r['age_band']}|opened={r['report_opened']}",
          "interaction_age_x_opened.csv", "-- age x opened (non-referral)")
seg_table(NONREF, lambda r: f"follow_up={r['optician_follow_up']}|consent={r['marketing_consent']}",
          "interaction_followup_x_consent.csv", "-- follow_up x consent (non-referral)")
seg_table(NONREF, lambda r: f"{r['result_category']}|{r['age_band']}",
          "interaction_result_x_age.csv", "-- result x age (non-referral)")
# Ophthalmologist's general guidance (interview 04) differs for under-40s, so the metric scope is a choice
seg_table(NONREF, lambda r: "18-39" if r["age_band"] == "18-39" else "40+",
          "segment_age_40plus.csv", "-- age 18-39 vs 40+ (non-referral, metric scope option)")
seg_table([r for r in NONREF if r["age_band"] != "18-39"],
          lambda r: f"40+|consent={r['marketing_consent']}",
          "interaction_40plus_x_consent.csv", "-- 40+ x consent (non-referral)")

section("5b. REFERRAL_RECOMMENDED CUSTOMERS (separate population)")
print(f"referral_recommended n={len(REF)}; referral_booked: "
      f"{dict(Counter(r['referral_booked'] for r in REF))} "
      f"-> booked share {pct(sum(1 for r in REF if r['referral_booked']=='true') / len(REF))}")
for col in ["report_opened", "preferred_language", "age_band", "location_type",
            "marketing_consent"]:
    g = defaultdict(list)
    for r in REF:
        g[r[col]].append(r)
    print(f"  booked share by {col}: " + "; ".join(
        f"{k} {pct(sum(1 for r in v if r['referral_booked']=='true') / len(v))} (n={len(v)}){flag(len(v))}"
        for k, v in sorted(g.items())))
seg_table(REF, lambda r: r["referral_booked"], "referral_by_booked.csv",
          "-- second mira screening by referral_booked (referral_recommended only)",
          ["true", "false"])
ref_booked = [r for r in REF]
rb_rows = []
for col in ["report_opened"]:
    for v in ["true", "false"]:
        g = [r for r in REF if r[col] == v]
        k = sum(1 for r in g if r["referral_booked"] == "true")
        lo, hi = wilson(k, len(g))
        rb_rows.append([f"{col}={v}", len(g), k, k / len(g), lo, hi])
        print(f"  referral_booked | {col}={v}: n={len(g)} booked={k} {pct(k/len(g))} "
              f"[{pct(lo)}-{pct(hi)}]")
write_table("referral_booked_by_opened.csv",
            ["segment", "n", "booked", "share", "ci_lo", "ci_hi"], rb_rows)

# ---------------------------------------------------------------------------
# 6. Reach (marketing consent)
# ---------------------------------------------------------------------------
section("6. REACH: SHARE WITH MARKETING_CONSENT (all 2025 customers)")


def share_table(rs, field_true, cols, name, label):
    out = []
    tot = sum(1 for r in rs if field_true(r))
    print(f"{label} overall: {tot}/{len(rs)} = {pct(tot / len(rs))}")
    for col in cols:
        g = defaultdict(list)
        for r in rs:
            g[r[col]].append(r)
        for v in ORDER.get(col, sorted(g)):
            if v not in g:
                continue
            k = sum(1 for r in g[v] if field_true(r))
            lo, hi = wilson(k, len(g[v]))
            out.append([col, v, len(g[v]), k, k / len(g[v]), lo, hi])
            print(f"  {col:20} {v:22} n={len(g[v]):>5} yes={k:>5} {pct(k / len(g[v]))} "
                  f"[{pct(lo)}-{pct(hi)}]{flag(len(g[v]))}")
    write_table(name, ["dimension", "segment", "n", "yes", "share", "ci_lo", "ci_hi"], out)


consent = lambda r: r["marketing_consent"] == "true"
share_table(rows, consent, ["location_type", "optician_follow_up", "age_band",
                            "preferred_language", "result_category", "report_opened"],
            "reach_consent.csv", "marketing_consent (all customers)")
share_table(NONREF, consent, ["location_type"], "reach_consent_nonreferral.csv",
            "marketing_consent (non-referral)")
n_both = sum(1 for r in NONREF if consent(r) and r["report_opened"] == "true")
n_noc_open = sum(1 for r in NONREF if not consent(r) and r["report_opened"] == "true")
n_noc_noopen = sum(1 for r in NONREF if not consent(r) and r["report_opened"] != "true")
print(f"Non-referral: consent & opened={n_both}; no consent & opened={n_noc_open}; "
      f"no consent & never opened={n_noc_noopen} (of {len(NONREF)})")
print(f"  shares: consent & opened {pct(n_both/len(NONREF))}; no consent & opened "
      f"{pct(n_noc_open/len(NONREF))}; no consent & never opened {pct(n_noc_noopen/len(NONREF))}")

# ---------------------------------------------------------------------------
# 7. Report engagement
# ---------------------------------------------------------------------------
section("7. REPORT ENGAGEMENT BY LANGUAGE AND AGE (all customers)")
eng_rows = []
_op = sum(1 for r in rows if r["report_opened"] == "true")
_opn = sum(1 for r in NONREF if r["report_opened"] == "true")
print(f"  overall: n={len(rows)} opened={_op} {pct(_op/len(rows))}; non-referral n={len(NONREF)} "
      f"opened={_opn} {pct(_opn/len(NONREF))}")
for col in ["preferred_language", "age_band", "location_type", "result_category"]:
    g = defaultdict(list)
    for r in rows:
        g[r[col]].append(r)
    for v in ORDER[col]:
        rs = g[v]
        op = [r for r in rs if r["report_opened"] == "true"]
        days = [int(r["report_opened_days_after"]) for r in op]
        lo, hi = wilson(len(op), len(rs))
        med = statistics.median(days) if days else float("nan")
        within1 = sum(1 for d in days if d <= 1)
        print(f"  {col:20} {v:22} n={len(rs):>5} opened={pct(len(op)/len(rs))} "
              f"[{pct(lo)}-{pct(hi)}] median_days={med} opened_within_1d={pct(within1/len(rs))}"
              f"{flag(len(rs))}")
        eng_rows.append([col, v, len(rs), len(op), len(op) / len(rs), lo, hi, med,
                         within1 / len(rs)])
dn = [r for r in rows if r["preferred_language"] != "de"]
dno = sum(1 for r in dn if r["report_opened"] == "true")
print(f"  non-de pooled: n={len(dn)} opened={pct(dno/len(dn))}")
write_table("engagement.csv", ["dimension", "segment", "n", "opened", "open_rate", "ci_lo",
                               "ci_hi", "median_days_to_open", "share_opened_within_1d"],
            eng_rows)
print("Language x age open rate:")
for lang in ["de", "non-de"]:
    for a in ORDER["age_band"]:
        rs = [r for r in rows if r["age_band"] == a and
              ((r["preferred_language"] == "de") == (lang == "de"))]
        k = sum(1 for r in rs if r["report_opened"] == "true")
        print(f"  {lang:6} {a:6} n={len(rs):>5} opened={pct(k/len(rs))}{flag(len(rs))}")

# ---------------------------------------------------------------------------
# 8. Locations
# ---------------------------------------------------------------------------
section("8. SPREAD ACROSS LOCATIONS (non-referral)")
# Per-location n is small in any fixed window, so locations are compared with indirect
# standardisation: each customer's expected probability of having returned by the export date
# is the pooled non-referral rate of their first-screening month (which fixes observation time).
# Observed (O) vs expected (E) returns by export per location; variance = sum p(1-p).
cm_rate = {}
for m in sorted(by_month):
    rs = [r for r in by_month[m] if r["result_category"] != "referral_recommended"]
    cm_rate[m] = sum(1 for r in rs if r["d2"]) / len(rs)
locs = defaultdict(list)
for r in NONREF:
    locs[r["location_id"]].append(r)
loc_rows = []
for l in sorted(locs):
    rs = locs[l]
    t, c, fu = next(iter(loc_attrs[l]))
    O = sum(1 for r in rs if r["d2"])
    E = sum(cm_rate[r["first_screening_date"][:7]] for r in rs)
    V = sum(cm_rate[r["first_screening_date"][:7]] * (1 - cm_rate[r["first_screening_date"][:7]])
            for r in rs)
    z = (O - E) / math.sqrt(V)
    n12, k12, p12, _, _ = rate(rs, 12)
    nP, kP, pP, _, _ = rate(rs, PRIMARY_WINDOW)
    cons = sum(1 for r in rs if consent(r)) / len(rs)
    opn = sum(1 for r in rs if r["report_opened"] == "true") / len(rs)
    loc_rows.append([l, t, c, fu, len(rs), O, E, O / E, z, n12, k12, p12, nP, kP, pP, cons, opn])
write_table("locations.csv",
            ["location_id", "location_type", "city", "follow_up_self_reported", "n_nonreferral",
             "observed_returns_by_export", "expected_returns_cohort_adjusted", "o_e_ratio", "z",
             "n_12m", "returned_12m", "rate_12m", f"n_{PRIMARY_WINDOW}m",
             f"returned_{PRIMARY_WINDOW}m", f"rate_{PRIMARY_WINDOW}m", "consent_share",
             "open_share"], loc_rows)
n_all = [x[4] for x in loc_rows]
n12s = [x[9] for x in loc_rows]
nPs = [x[12] for x in loc_rows]
print(f"Locations: {len(loc_rows)}. Non-referral customers per location: min {min(n_all)}, "
      f"median {statistics.median(n_all)}, max {max(n_all)}")
print(f"  in 12m window: min {min(n12s)}, median {statistics.median(n12s)}, max {max(n12s)}, "
      f"locations n<100: {sum(1 for x in n12s if x < SMALL_N)}")
print(f"  in {PRIMARY_WINDOW}m window: min {min(nPs)}, median {statistics.median(nPs)}, "
      f"max {max(nPs)}, locations n<100: {sum(1 for x in nPs if x < SMALL_N)}")
print("  -> every location is small (n<100) in the proposed window; location-level rates are noisy.")
oe = sorted(x[7] for x in loc_rows)
print(f"O/E ratio across locations: min {oe[0]:.2f}, p25 {oe[len(oe)//4]:.2f}, "
      f"median {statistics.median(oe):.2f}, p75 {oe[3*len(oe)//4]:.2f}, max {oe[-1]:.2f}")
chi = sum(x[8] ** 2 for x in loc_rows)
print(f"Heterogeneity: sum of z^2 = {chi:.1f} on ~{len(loc_rows)-1} df "
      f"(value close to df = spread consistent with chance)")
sig_hi = [x[0] for x in loc_rows if x[8] > 1.96]
sig_lo = [x[0] for x in loc_rows if x[8] < -1.96]
print(f"Locations with z>1.96: {len(sig_hi)} {sig_hi}; z<-1.96: {len(sig_lo)} {sig_lo} "
      f"(about {0.05*len(loc_rows):.0f} expected by chance alone at 5%)")
tot_O = sum(x[5] for x in loc_rows)
tot_n = sum(x[4] for x in loc_rows)
tot_E = sum(x[6] for x in loc_rows)
srt = sorted(loc_rows, key=lambda x: -x[5])
for top in (5, 10):
    k = sum(x[5] for x in srt[:top])
    n = sum(x[4] for x in srt[:top])
    e = sum(x[6] for x in srt[:top])
    print(f"Top {top} locations by observed returns: {k}/{tot_O} = {pct(k/tot_O)} of returns; "
          f"{n}/{tot_n} = {pct(n/tot_n)} of customers; their expected share {pct(e/tot_E)}")
print("Top 5 locations by O/E (all n):")
for x in sorted(loc_rows, key=lambda x: -x[7])[:5]:
    print(f"  {x[0]} {x[1]} {x[2]} follow_up={x[3]} n={x[4]} O={x[5]} E={x[6]:.1f} "
          f"O/E={x[7]:.2f} z={x[8]:.2f}")
print("Bottom 5 locations by O/E:")
for x in sorted(loc_rows, key=lambda x: x[7])[:5]:
    print(f"  {x[0]} {x[1]} {x[2]} follow_up={x[3]} n={x[4]} O={x[5]} E={x[6]:.1f} "
          f"O/E={x[7]:.2f} z={x[8]:.2f}")

print("\nSelf-reported follow_up label vs location-level O/E (cohort-adjusted returns by export):")
fu_rows = []
for fu in ORDER["optician_follow_up"]:
    sub = [x for x in loc_rows if x[3] == fu]
    O = sum(x[5] for x in sub)
    E = sum(x[6] for x in sub)
    r_ = sorted(x[7] for x in sub)
    above = sum(1 for x in sub if x[7] > 1)
    types = dict(Counter(x[1] for x in sub))
    print(f"  {fu:6} locations={len(sub)} types={types} customers={sum(x[4] for x in sub)} "
          f"O={O} E={E:.1f} pooled O/E={O/E:.2f}; location O/E min {r_[0]:.2f} "
          f"median {statistics.median(r_):.2f} max {r_[-1]:.2f}; locations with O/E>1: "
          f"{above}/{len(sub)}")
    fu_rows.append([fu, len(sub), sum(x[4] for x in sub), O, E, O / E, r_[0],
                    statistics.median(r_), r_[-1], above])
write_table("followup_label_vs_location_oe.csv",
            ["follow_up_self_reported", "locations", "customers", "observed", "expected",
             "pooled_o_e", "min_loc_o_e", "median_loc_o_e", "max_loc_o_e", "locations_o_e_gt_1"],
            fu_rows)
none_med = statistics.median(x[7] for x in loc_rows if x[3] == "none")
for fu in ["email", "phone"]:
    sub = [x for x in loc_rows if x[3] == fu]
    below = [x[0] for x in sub if x[7] <= none_med]
    print(f"  {fu}-labelled locations at or below the median 'none' location O/E "
          f"({none_med:.2f}): {len(below)}/{len(sub)} {below}")
print("Customers by location_type x follow_up label (all customers):")
for t in ORDER["location_type"]:
    print(f"  {t:22} " + ", ".join(
        f"{fu}={sum(1 for r in rows if r['location_type']==t and r['optician_follow_up']==fu)}"
        for fu in ORDER["optician_follow_up"]))

section("9. ADDENDUM FOR STEP 3 (leading-indicator baselines, reach, power)")
# Report opened within 5 days (field only takes 0/1/2/3/5/9, so "within 7 days" == "<= 5")
print("Report opened within <=5 days of availability (non-referral, all 2025 cohorts):")
for lab, sub in [("all", NONREF),
                 ("de", [r for r in NONREF if r["preferred_language"] == "de"]),
                 ("non-de", [r for r in NONREF if r["preferred_language"] != "de"]),
                 ("40+", [r for r in NONREF if r["age_band"] != "18-39"])]:
    k = sum(1 for r in sub if r["report_opened"] == "true" and int(r["report_opened_days_after"]) <= 5)
    p, lo, hi = k / len(sub), *wilson(k, len(sub))
    print(f"  {lab:7} n={len(sub)} opened<=5d={k} {pct(p)} [{pct(lo)}-{pct(hi)}]")

seg_table([r for r in NONREF if r["age_band"] == "60+"],
          lambda r: f"60+|follow_up={r['optician_follow_up']}",
          "interaction_60plus_x_followup.csv", "-- 60+ x follow_up (non-referral, self-reported label)")

print("\nmarketing_consent share, non-referral 40+ by result (all 2025 cohorts):")
for res in ["unremarkable", "minor_findings"]:
    sub = [r for r in NONREF if r["age_band"] != "18-39" and r["result_category"] == res]
    k = sum(1 for r in sub if r["marketing_consent"] == "true")
    print(f"  {res:15} 40+ n={len(sub)} consent={k} {pct(k / len(sub))}")
sub = [r for r in NONREF if r["age_band"] != "18-39"]
k = sum(1 for r in sub if r["marketing_consent"] == "true")
print(f"  {'all non-ref':15} 40+ n={len(sub)} consent={k} {pct(k / len(sub))}")

# Minimum detectable effect (absolute pp) for a 50/50 two-arm test, alpha 0.05 two-sided, power 0.8,
# at the 40+ non-referral 15-month baseline. n = customers screened per period (2025 volume / 4 per quarter).
p0 = rate([r for r in NONREF if r["age_band"] != "18-39"], 15)[2]
print(f"\nMDE (two-arm 50/50, alpha .05, power .8) at 40+ 15m baseline {pct(p0)}:")
for lab, pool in [("independents 40+ non-ref", [r for r in NONREF if r["age_band"] != "18-39"
                                                 and r["location_type"] == "independent_optician"]),
                  ("all locations 40+ non-ref", [r for r in NONREF if r["age_band"] != "18-39"])]:
    for quarters in [1, 2, 4]:
        n_total = round(len(pool) * quarters / 4)
        n_arm = n_total / 2
        mde = (1.96 + 0.8416) * math.sqrt(2 * p0 * (1 - p0) / n_arm)
        print(f"  {lab:26} {quarters}q of screenings: n={n_total} (arm {n_arm:.0f}) "
              f"MDE ~ {mde*100:.1f} pp")

O40 = [r for r in NONREF if r["age_band"] != "18-39"]
seg_table(O40, lambda r: f"40+|consent={r['marketing_consent']}|opened={r['report_opened']}",
          "interaction_40plus_consent_x_opened.csv", "-- 40+ x consent x opened (non-referral)")
seg_table(O40, lambda r: f"40+|follow_up={r['optician_follow_up']}|consent={r['marketing_consent']}",
          "interaction_40plus_followup_x_consent.csv", "-- 40+ x follow_up x consent (non-referral, self-reported)")
k = sum(1 for r in O40 if r["report_opened"] == "true")
print(f"\n40+ non-referral report ever opened: {k}/{len(O40)} {pct(k / len(O40))}")
k = sum(1 for r in O40 if r["report_opened"] == "false" and r["marketing_consent"] == "false")
print(f"40+ non-referral neither consent nor opened: {k}/{len(O40)} {pct(k / len(O40))}")

for lt in ORDER["location_type"]:
    sub = [r for r in REF if r["location_type"] == lt]
    k = sum(1 for r in sub if r["referral_booked"] == "true")
    lo, hi = wilson(k, len(sub))
    print(f"referral_booked at {lt}: {k}/{len(sub)} {pct(k / len(sub))} [{pct(lo)}-{pct(hi)}]{flag(len(sub))}")

print("\nDone. Tables written to", TABLES)
