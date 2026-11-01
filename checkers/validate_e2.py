"""E2 independent validation — tester-probe style.

Recomputes, WITHOUT importing any builder module:
  1. Population metrics for a sample of (force, month, class) cells from the
     saved per-record score parquets (EO/DP gaps at cut 0.5).
  2. Monitor completeness: rows per (class, force, seed) and batch months.
  3. Instance labels for the headline cell from population_metrics.csv
     breach months vs the labels implied by monitor.parquet label columns
     (count of defined labels per class).
  4. The full headline accounting from results/fold_scores.npz: candidate
     thresholds (99 quantiles of pooled [p_tr, plv_tr]), pick rule, fold
     FARs, null TVs (50/20 bins), margins, pass flags, medians, criterion —
     compared number-by-number against results/accounting.json.
Exit 0 only if every check passes.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
SCORES = os.path.join(HERE, "data", "scores")
FAILS = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" | {detail}" if detail
                                                   else ""))
    if not cond:
        FAILS.append(name)


def tv_hist(a, b, bins):
    a = np.clip(np.asarray(a, float), 0, 1)
    b = np.clip(np.asarray(b, float), 0, 1)
    ha, _ = np.histogram(a, bins=bins, range=(0.0, 1.0))
    hb, _ = np.histogram(b, bins=bins, range=(0.0, 1.0))
    return float(0.5 * np.abs(ha / ha.sum() - hb / hb.sum()).sum())


def eo_dp(y, a, alarm):
    def rate(av, yv):
        m = (a == av) & (y == yv)
        return alarm[m].mean() if m.any() else np.nan
    eo = np.nanmax([abs(rate(1, 1) - rate(0, 1)), abs(rate(1, 0) - rate(0, 0))])
    dp = abs(alarm[a == 1].mean() - alarm[a == 0].mean())
    return float(eo), float(dp)


def main():
    acc = json.load(open(os.path.join(RESULTS, "accounting.json")))
    tau_star = acc["tau_star"]
    pm = pd.read_csv(os.path.join(RESULTS, "population_metrics.csv"))
    aset = json.load(open(os.path.join(RESULTS, "analysis_set.json")))
    forces = aset["included"]
    months = [f"2024-{m:02d}" for m in range(1, 13)]

    # 1. population metric recompute (sample: first/last force x 3 months)
    ok = True
    for force in (forces[0], forces[len(forces) // 2], forces[-1]):
        for month in ("2024-01", "2024-06", "2024-12"):
            df = pd.read_parquet(os.path.join(SCORES, f"{force}_{month}.parquet"))
            for cls, scol in (("lr", "score_lr"), ("gb", "score_gb")):
                alarm = (df[scol].to_numpy() >= 0.5).astype(int)
                eo, dp = eo_dp(df.y.to_numpy(), df.A.to_numpy(), alarm)
                row = pm[(pm.force == force) & (pm.month == month)
                         & (pm.model == cls)].iloc[0]
                if abs(eo - row.eo) > 1e-9 or abs(dp - row.dp) > 1e-9:
                    ok = False
    check("population metrics recompute (sample)", ok)

    # 2. monitor completeness
    mon = pd.read_parquet(os.path.join(RESULTS, "monitor.parquet"))
    exp_rows = 2 * len(forces) * 25 * 12
    check("monitor row count", len(mon) == exp_rows,
          f"{len(mon)} vs {exp_rows}")
    per = mon.groupby(["model", "force", "seed"]).size()
    check("monitor rows per (class, force, seed) == 12",
          bool((per == 12).all()))

    # 3. headline label counts consistent with population breach months
    lab = f"lab_eo_{tau_star}_h2"
    ok = True
    for cls in ("lr", "gb"):
        sub = pm[pm.model == cls]
        gaps = {f: sub[sub.force == f].set_index("month").eo.to_dict()
                for f in forces}
        n_def_expected = 0
        for f in forces:
            b = next((i for i, m in enumerate(months)
                      if gaps[f][m] >= tau_star), None)
            for t, m in enumerate(months):
                if gaps[f][m] < tau_star and t + 2 <= 11:
                    n_def_expected += 25
        n_def = int(mon[(mon.model == cls)][lab].notna().sum())
        if n_def != n_def_expected:
            ok = False
            print("  label count mismatch", cls, n_def, n_def_expected)
    check("headline defined-label counts (both classes)", ok)

    # 4. accounting recompute from fold_scores.npz
    z = np.load(os.path.join(RESULTS, "fold_scores.npz"))
    ok = True
    for cls in ("lr", "gb"):
        rep = acc["headline"][cls]
        acc_folds = {a["fold"]: a for a in rep["folds"]}
        tvs, npass = [], 0
        for force in forces:
            k = f"{cls}_fold_{force}"
            p_tr, y_tr = z[k + "_p_tr"], z[k + "_y_tr"]
            plv_tr = z[k + "_plv_tr"]
            p_te, y_te = z[k + "_p_te"], z[k + "_y_te"]
            cand = np.unique(np.quantile(np.r_[p_tr, plv_tr],
                                         np.linspace(0.01, 0.99, 99)))
            fars = [float((p_tr[y_tr == 0] >= c).mean()) for c in cand]
            ci = min(range(len(cand)),
                     key=lambda i: (abs(fars[i] - 0.10), fars[i]))
            theta = float(cand[ci])
            far_train = fars[ci]
            far_fold = float((p_te[y_te == 0] >= theta).mean())
            tv50 = tv_hist(p_te[y_te == 0], p_tr[y_tr == 0], 50)
            tv20 = tv_hist(p_te[y_te == 0], p_tr[y_tr == 0], 20)
            dev = abs(far_fold - far_train)
            passed = dev <= tv50 + 0.02
            tvs.append(tv50)
            npass += int(passed)
            a = acc_folds[force]
            for name, mine, theirs in (
                    ("theta", theta, a["theta"]),
                    ("far_fold", far_fold, a["far_fold"]),
                    ("far_train", far_train, a["far_train"]),
                    ("tv50", tv50, a["tv50"]), ("tv20", tv20, a["tv20"])):
                if abs(mine - theirs) > 1e-9:
                    ok = False
                    print("  mismatch", cls, force, name, mine, theirs)
            if passed != a["pass"]:
                ok = False
                print("  pass mismatch", cls, force)
        if abs(float(np.median(tvs)) - rep["median_tv50"]) > 1e-9:
            ok = False
        if npass != rep["pass_count"]:
            ok = False
        crit = bool(np.median(tvs) >= 0.05 and npass / len(forces) >= 0.99)
        if crit != rep["criterion_met"]:
            ok = False
    check("headline accounting recompute (all folds, both classes)", ok)

    print("VALIDATION:", "ALL PASS" if not FAILS else f"FAILURES {FAILS}")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main())
