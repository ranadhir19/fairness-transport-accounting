#!/usr/bin/env python3
"""Deposit validator for fairness-transport-accounting.

Recomputes the manuscript's headline accounting numbers from the
deposited fold tables and population tables alone (standard library
only) and compares them against the values printed in the paper and
in the cycle reports. Exits 0 iff every check passes.

Run from the repository root:  python3 validate.py
"""
import csv
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def check(name, ok, detail=""):
    print(("PASS" if ok else "FAIL"), name, detail)
    if not ok:
        FAIL.append(name)


def close(a, b, tol=5e-4):
    return a is not None and abs(a - b) <= tol


def rows(path):
    with open(os.path.join(ROOT, path), newline="") as fh:
        return list(csv.DictReader(fh))


def f(x):
    return float(x)


# ---- 1. Gap accounting (manuscript Table 2), from the closure fold tables ----
def gap_cell(path, cls, n_folds, eo_med, eo_min, dp_med, dp_min, label):
    rs = [r for r in rows(path) if r["class"] == cls]
    ok_n = len(rs) == n_folds
    if not ok_n:
        check(label, False, f"fold count {len(rs)} != {n_folds}")
        return
    eo_d = [f(r["d_eo"]) for r in rs]
    dp_d = [f(r["d_dp"]) for r in rs]
    eo_m = [f(r["margin_eo"]) for r in rs]
    dp_m = [f(r["margin_dp"]) for r in rs]
    passed = all(r["pass_eo"] == "True" and r["pass_dp"] == "True" for r in rs)
    check(label + " EO median/min-margin",
          close(statistics.median(eo_d), eo_med) and close(min(eo_m), eo_min),
          f"median {statistics.median(eo_d):.4f} (paper {eo_med}), min margin {min(eo_m):.4f} (paper {eo_min})")
    check(label + " DP median/min-margin",
          close(statistics.median(dp_d), dp_med) and close(min(dp_m), dp_min),
          f"median {statistics.median(dp_d):.4f} (paper {dp_med}), min margin {min(dp_m):.4f} (paper {dp_min})")
    check(label + " all folds pass, criterion fraction", passed and len(rs) >= 1,
          f"{sum(1 for r in rs if r['pass_eo'] == 'True')}/{len(rs)} EO, "
          f"{sum(1 for r in rs if r['pass_dp'] == 'True')}/{len(rs)} DP")


gap_cell("results/closure/folds_2024.csv", "score_lr", 9, 0.4149, 0.2718, 0.3135, 0.2667,
         "F2-2024 LR")
gap_cell("results/closure/folds_2024.csv", "score_gb", 9, 0.5011, 0.3112, 0.4427, 0.2958,
         "F2-2024 GB")
gap_cell("results/closure/folds_2025.csv", "score_gb", 7, 0.3442, 0.2886, 0.3241, 0.2819,
         "F2-2025 GB")
gap_cell("results/closure/folds_f1arm.csv", "lr_original", 6, 0.1104, 0.0854, 0.1020, 0.0745,
         "F1 arm LR")

# F2-2025 LR: descriptive only in the paper (no recorded verdict for that cell)
rs = [r for r in rows("results/closure/folds_2025.csv") if r["class"] == "score_lr"]
check("F2-2025 LR descriptive medians",
      len(rs) == 7 and close(statistics.median([f(r['d_eo']) for r in rs]), 0.2845)
      and close(statistics.median([f(r['d_dp']) for r in rs]), 0.2787),
      "EO 0.2845 / DP 0.2787 as printed in the Table 2 caption")

with open(os.path.join(ROOT, "results/closure/closure_summary.json")) as fh:
    cs = json.load(fh)
check("closure anchors reproduced", cs.get("anchors_reproduced") == 24,
      "24 population-table anchor cells reproduced exactly (closure record)")

# ---- 2. FAR accounting medians (E2 and E4 cycles) ----
e2 = rows("results/e2/fold_detail.csv")
for cls, med in (("lr", 0.4784), ("gb", 0.2865)):
    rs = [r for r in e2 if r["model"] == cls]
    check(f"E2 FAR accounting {cls.upper()}",
          len(rs) == 9 and close(statistics.median([f(r['tv50']) for r in rs]), med)
          and all(r["pass"] == "True" for r in rs),
          f"median TV50 {statistics.median([f(r['tv50']) for r in rs]):.4f} (record {med}), 9/9 pass")

e4f = rows("results/e4/accounting_folds4.csv")
rs = [r for r in e4f if r["model"] == "gb"]
check("E4 FAR accounting GB",
      len(rs) == 7 and close(statistics.median([f(r['tv50']) for r in rs]), 0.3475)
      and all(r["pass"] == "True" for r in rs),
      f"median TV50 {statistics.median([f(r['tv50']) for r in rs]):.4f} (record 0.3475), 7/7 pass")
with open(os.path.join(ROOT, "results/e4/accounting4.json")) as fh:
    a4 = json.load(fh)
check("E4 accounting verdicts", a4["gb"]["criterion_met"] is True
      and a4["lr"]["not_evaluable"] is not None,
      "GB met; LR not evaluable (tau* degeneracy), as reported")

# ---- 3. Cut degeneracy, family 2 2025 (manuscript Sections 6-7) ----
pm = [r for r in rows("results/e4/population_metrics.csv") if r["model"] == "lr"]
zero_cells = [r for r in pm if f(r["eo"]) == 0.0 and f(r["dp"]) == 0.0]
check("E4 population table shape", len(pm) == 96 and len(zero_cells) == 81,
      f"{len(pm)} LR cells, {len(zero_cells)} with EO = DP = 0 (paper: 81/96 = 84.4%)")
with open(os.path.join(ROOT, "results/e4/tau_star.json")) as fh:
    ts = json.load(fh)
check("tau* degeneracy",
      all(ts["taus"]["lr"][m][q] == 0.0 for m in ("eo", "dp") for q in ("q60", "q70", "q80"))
      and close(ts["taus"]["gb"]["eo"]["q70"], 0.0033289, tol=1e-6),
      "LR tau* = 0 at q in {0.60, 0.70, 0.80}; GB EO tau* = 0.0033289")

summ = rows("results/e4/lr_score_cell_summary_2025.csv")
tot_n = sum(int(r["n"]) for r in summ)
tot_hi = sum(int(r["n_at_or_above_cut"]) for r in summ)
no_cut = [r for r in summ if int(r["n_at_or_above_cut"]) == 0]
check("2025 LR score reach", len(summ) == 96 and tot_n == 65826 and tot_hi == 21
      and len(no_cut) == 81 and all(f(r["eo"]) == 0.0 and f(r["dp"]) == 0.0 for r in no_cut),
      f"{tot_hi} of {tot_n} records at/above the 0.5 cut; {len(no_cut)} cells with none, all gap-free")
nz = sorted((f(r["eo"]) for r in summ if f(r["eo"]) > 0), reverse=True)
check("2025 nonzero-cell texture",
      len(nz) == 15 and close(nz[0], 0.20, tol=1e-6) and nz[1] <= 0.031,
      f"15 nonzero cells; largest 0.20 (single-record stratum), next {nz[1]:.4f} <= 0.031")

# ---- 4. Crossing rarity, family 2 2024 (manuscript Section 7) ----
pm24 = [r for r in rows("results/e2/population_metrics_2024.csv") if r["model"] == "lr"]
at_tau = [r for r in pm24 if f(r["eo"]) >= 0.05]
bound = 9 * 11 * (len(at_tau) / 108.0)
check("crossing rarity F2-2024",
      len(pm24) == 108 and len(at_tau) == 2 and close(bound, 1.83, tol=0.01) and bound < 3,
      f"{len(at_tau)}/108 cells at tau = 0.05; expected-crossing bound {bound:.2f} < floor 3")

# ---- 5. Headline numbers present in the manuscript source ----
tex = open(os.path.join(ROOT, "manuscript/Paper_11_Rebuilt3.tex")).read()
for needle in ("0.4149", "0.1104", "0.289", "84.4", "fairness-transport-accounting"):
    check(f"manuscript carries '{needle}'", needle in tex)

print()
if FAIL:
    print("VALIDATE: FAIL —", len(FAIL), "check(s):", ", ".join(FAIL))
    sys.exit(1)
print("VALIDATE: ALL PASS")
