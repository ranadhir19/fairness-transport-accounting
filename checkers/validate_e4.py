"""E4 independent validator.

Recomputes every number E4_RESULTS.md rests on, from saved artifacts
only. Imports NO builder module (common4/engine4/forecast4 are not
used); all definitions (eo/dp gap, TV histogram, stable_seed, the
cluster bootstrap) are re-implemented here from the frozen documents.
Prints PASS/FAIL per check and ALL PASS at the end; exit code 0 only
if every check passes.
"""
import json
import os
import sys
import zlib

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
R4 = os.path.join(HERE, "results4")
BASE = os.path.join(HERE, "..")
MONTHS = [f"2025-{m:02d}" for m in range(1, 13)]
BASELINES = ["lastvalue", "extrap", "cusum"]
FAILURES = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail
                                                 else ""))
    if not ok:
        FAILURES.append(name)
    return ok


def close(a, b, tol=1e-9):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False


def stable_seed(*parts):
    s = "|".join(str(p) for p in parts)
    return zlib.crc32(s.encode()) & 0xFFFFFFFF


def eo_gap(y, a, alarm):
    y = np.asarray(y); a = np.asarray(a); alarm = np.asarray(alarm)
    def rate(av, yv):
        m = (a == av) & (y == yv)
        return alarm[m].mean() if m.any() else np.nan
    vals = [v for v in (abs(rate(1, 1) - rate(0, 1)),
                        abs(rate(1, 0) - rate(0, 0))) if not np.isnan(v)]
    return float(max(vals)) if vals else float("nan")


def dp_gap(a, alarm):
    a = np.asarray(a); alarm = np.asarray(alarm)
    r1 = alarm[a == 1].mean() if (a == 1).any() else np.nan
    r0 = alarm[a == 0].mean() if (a == 0).any() else np.nan
    return float(abs(r1 - r0)) if not (np.isnan(r1) or np.isnan(r0)) \
        else float("nan")


def tv_hist(a, b, bins=50):
    a = np.clip(np.asarray(a, float), 0, 1)
    b = np.clip(np.asarray(b, float), 0, 1)
    ha, _ = np.histogram(a, bins=bins, range=(0.0, 1.0))
    hb, _ = np.histogram(b, bins=bins, range=(0.0, 1.0))
    return float(0.5 * np.abs(ha / ha.sum() - hb / hb.sum()).sum())


def bootstrap_deltas(leads_g, baselines, seed, B=2000):
    """Mirror of the frozen §6 bootstrap, re-implemented: cluster
    resample over breaching units, medians over covered pairs."""
    units = sorted(leads_g.unit.unique())
    by_unit = {u: leads_g[leads_g.unit == u] for u in units}
    rng = np.random.default_rng(seed)

    def med(frame, meth):
        cov = frame[(frame.method == meth) & frame.covered]
        return float(cov.lead.median()) if len(cov) else np.nan

    out = {}
    for base in baselines:
        delta = med(leads_g, "traq") - med(leads_g, base)
        ds = []
        for _ in range(B):
            draw = rng.choice(units, size=len(units), replace=True)
            frame = pd.concat([by_unit[u] for u in draw],
                              ignore_index=True)
            mc, mb = med(frame, "traq"), med(frame, base)
            if np.isnan(mc) or np.isnan(mb):
                continue
            ds.append(mc - mb)
        ds = np.array(ds)
        out[base] = {"delta": float(delta),
                     "ci_lo": float(np.percentile(ds, 2.5)),
                     "ci_hi": float(np.percentile(ds, 97.5)),
                     "n_kept": int(len(ds))}
    return out


def main():
    aset = json.load(open(os.path.join(R4, "analysis_set.json")))
    diag = json.load(open(os.path.join(R4, "deployed_diag.json")))
    tau_info = json.load(open(os.path.join(R4, "tau_star.json")))
    headline = json.load(open(os.path.join(R4, "headline4.json")))
    accounting = json.load(open(os.path.join(R4, "accounting4.json")))
    pm = pd.read_csv(os.path.join(R4, "population_metrics.csv"))
    mon = pd.read_parquet(os.path.join(R4, "monitor.parquet"))
    forces = aset["included"]
    primary = tau_info["primary_class"]

    # V1: analysis-set / monitor integrity
    expect_rows = 2 * len(forces) * 25 * 12
    check("V1 monitor rows", len(mon) == expect_rows,
          f"{len(mon)} vs {expect_rows}")
    dup = mon.duplicated(subset=["model", "force", "seed", "month"]).sum()
    check("V1 monitor no duplicates", dup == 0, f"dup={dup}")

    # V2: population metrics recomputed from saved score parquets
    rng = np.random.default_rng(7)
    cells = [(f, m) for f in forces for m in MONTHS]
    pick = [cells[i] for i in rng.choice(len(cells), size=8,
                                         replace=False)]
    ok, worst = True, 0.0
    for (f, m) in pick:
        sdf = pd.read_parquet(os.path.join(
            HERE, "data", "scores25", f"{f}_{m}.parquet"))
        for cls, col in (("lr", "score_lr"), ("gb", "score_gb")):
            alarm = (sdf[col].to_numpy() >= 0.5).astype(int)
            eo = eo_gap(sdf.y.to_numpy(), sdf.A.to_numpy(), alarm)
            dp = dp_gap(sdf.A.to_numpy(), alarm)
            row = pm[(pm.model == cls) & (pm.force == f)
                     & (pm.month == m)].iloc[0]
            worst = max(worst, abs(eo - row.eo), abs(dp - row.dp))
            ok = ok and close(eo, row.eo, 1e-9) and close(dp, row.dp, 1e-9)
    check("V2 population metrics from scores25", ok, f"worst={worst:.2e}")

    # V3: tau* and primary-class rule recomputed
    ok = True
    for cls in ("lr", "gb"):
        sub = pm[pm.model == cls]
        for metric in ("eo", "dp"):
            gaps = sub[metric].to_numpy(float)
            for q, tag in ((0.60, "q60"), (0.70, "q70"), (0.80, "q80")):
                ok = ok and close(np.quantile(gaps, q),
                                  tau_info["taus"][cls][metric][tag],
                                  1e-12)
    check("V3 tau* quantiles", ok)
    al, ag = diag["auc_holdout_lr"], diag["auc_holdout_gb"]
    exp_primary = "lr" if abs(al - ag) <= 0.005 else (
        "lr" if al > ag else "gb")
    check("V3 primary-class rule", exp_primary == primary,
          f"auc lr={al:.4f} gb={ag:.4f} -> {primary}")

    # V4: prong-1 (a)/(b) recomputed from the population table
    tau_star = tau_info["taus"][primary]["eo"]["q70"]
    sub = pm[pm.model == primary]
    n_cross, n_below = 0, 0
    for f in forces:
        s = sub[sub.force == f].set_index("month")["eo"]
        series = [float(s[m]) for m in MONTHS]
        b = next((i for i, v in enumerate(series) if v >= tau_star), None)
        n_cross += bool(b is not None and b >= 1)
        n_below += bool(series[0] < tau_star)
    p1 = headline["prong1_nonvacuity"]
    check("V4 prong1(a) crossings",
          n_cross == p1["n_cross_after_base"]
          and p1["cond_a_ge3_crossings"] == (n_cross >= 3),
          f"crossings={n_cross}")
    check("V4 prong1(b) share below",
          close(n_below / len(forces), p1["share_below_at_base"], 1e-12)
          and p1["cond_b_share_below_ge_0.40"]
          == (n_below / len(forces) >= 0.40),
          f"share={n_below / len(forces):.3f}")

    # V5: labels recomputed from population table (EO/DP, q70, H=2, full)
    pop = {}
    for cls in ("lr", "gb"):
        s2 = pm[pm.model == cls]
        for metric in ("eo", "dp"):
            for f in forces:
                s = s2[s2.force == f].set_index("month")[metric]
                pop[(cls, metric, f)] = [float(s[m]) for m in MONTHS]
    ok = True
    for metric in ("eo", "dp"):
        tau_m = {cls: tau_info["taus"][cls][metric]["q70"]
                 for cls in ("lr", "gb")}
        col = f"lab_{metric}_q70_h2"
        for _, r in mon.iterrows():
            gaps = pop[(r.model, metric, r.force)]
            tau = tau_m[r.model]
            b = next((i for i, v in enumerate(gaps) if v >= tau), None)
            t = int(r.mi)
            if gaps[t] < tau and t + 2 <= 11:
                exp = 1.0 if (b is not None and t < b <= t + 2) else 0.0
            else:
                exp = np.nan
            got = r[col]
            if np.isnan(exp) and np.isnan(got):
                continue
            if not close(exp, got, 0):
                ok = False
                break
        if not ok:
            break
    check("V5 labels recomputed (q70 H2, both metrics)", ok)
    pos = sorted(mon[(mon.model == primary)
                     & (mon.lab_eo_q70_h2 == 1.0)].force.unique())
    check("V5 prong1(c) label-1 forces",
          pos == p1["forces_with_label1"]
          and p1["cond_c_ge3_forces_with_label1"] == (len(pos) >= 3),
          f"forces={pos}")

    # V6: accounting recomputed from saved fold scores
    folds_df = pd.read_csv(os.path.join(R4, "accounting_folds4.csv"))
    scores = pd.read_parquet(os.path.join(R4, "accounting_scores4.parquet"))
    ok = True
    crit = {}
    for cls in ("lr", "gb"):
        if len(folds_df[folds_df.model == cls]) == 0:
            crit[cls] = False
            ok = ok and accounting[cls]["criterion_met"] is False
            continue
        meds, passes = [], 0
        for _, fr in folds_df[folds_df.model == cls].iterrows():
            sc = scores[(scores.model == cls) & (scores.fold == fr.fold)]
            tr = sc[sc.role == "train"]
            te = sc[sc.role == "test"]
            th = float(fr.theta)
            tv = tv_hist(te.loc[te.y == 0, "p"], tr.loc[tr.y == 0, "p"])
            far_f = float((te.loc[te.y == 0, "p"] >= th).mean())
            far_t = float((tr.loc[tr.y == 0, "p"] >= th).mean())
            dev = abs(far_f - far_t)
            ok = ok and close(tv, fr.tv50) and close(far_f, fr.far_fold) \
                and close(far_t, fr.far_train) and close(dev, fr.deviation) \
                and bool(dev <= tv + 0.02) == bool(fr["pass"])
            meds.append(tv)
            passes += bool(dev <= tv + 0.02)
        crit[cls] = bool(np.median(meds) >= 0.05
                         and passes / len(meds) >= 0.99)
        ok = ok and crit[cls] == accounting[cls]["criterion_met"] \
            and close(np.median(meds), accounting[cls]["median_tv50"])
    check("V6 accounting recomputed + criteria", ok,
          f"primary criterion={crit[primary]}")
    check("V6 prong3 matches headline",
          headline["prong3_accounting"]["pass"] == crit[primary])

    # V7: forecasting prong recomputed from saved lead rows
    leads = pd.read_parquet(os.path.join(R4, "forecast_leads4.parquet"))
    summ = pd.read_csv(os.path.join(R4, "forecast_summary4.csv"))
    g = leads[(leads.model == primary) & (leads.metric == "eo")
              & (leads.qtag == "q70") & (leads.H == 2)]
    ok = True
    for _, srow in summ[(summ.model == primary) & (summ.metric == "eo")
                        & (summ.qtag == "q70") & (summ.H == 2)].iterrows():
        if pd.isna(srow.far_target):
            grp = g[(g.method == srow.method) & g.far_target.isna()]
        else:
            grp = g[(g.method == srow.method)
                    & (g.far_target == srow.far_target)]
        cov = grp[grp.covered]
        ok = ok and len(grp) == int(srow.n_pairs) \
            and close(len(cov) / len(grp), srow.coverage) \
            and close(cov.lead.median(), srow.median_lead)
    check("V7 summary medians/coverages from lead rows", ok)
    p2 = headline["prong2_forecasting"]
    traq_rows = summ[(summ.model == primary) & (summ.metric == "eo")
                     & (summ.qtag == "q70") & (summ.H == 2)
                     & (summ.method == "traq")
                     & (summ.far_target == 0.10)]
    if len(traq_rows) == 0:
        # Degenerate gating cell: prong 2 must be recorded as failed
        # with no evaluable per-baseline criterion.
        ok = p2["pass"] is False and all(
            not v["criterion_met"] for v in p2["per_baseline"].values())
        check("V7 degenerate gating cell recorded as prong-2 fail", ok)
        prong2 = False
        boot = None
    else:
        g10 = g[g.far_target == 0.10]
        boot = bootstrap_deltas(g10, BASELINES,
                                seed=stable_seed("e4", "boot", "primary"))
        ok = True
        traq_row = traq_rows.iloc[0]
        prong2 = bool(traq_row.median_lead > 0)
        for b in BASELINES:
            hb = p2["per_baseline"][b]
            brow = summ[(summ.model == primary) & (summ.metric == "eo")
                        & (summ.qtag == "q70") & (summ.H == 2)
                        & (summ.method == b)
                        & (summ.far_target == 0.10)].iloc[0]
            ok = ok and close(boot[b]["delta"], hb["delta"], 1e-9) \
                and close(boot[b]["ci_lo"], hb["ci_lo"], 1e-9) \
                and close(boot[b]["ci_hi"], hb["ci_hi"], 1e-9) \
                and boot[b]["n_kept"] == hb["n_boot_kept"]
            crit_b = bool(boot[b]["delta"] > 0 and boot[b]["ci_lo"] > 0
                          and traq_row.coverage >= brow.coverage - 0.05)
            ok = ok and crit_b == hb["criterion_met"]
            prong2 = prong2 and crit_b
        check("V7 bootstrap CIs + per-baseline criteria", ok)
    prong1_all = bool(p1["cond_a_ge3_crossings"]
                      and p1["cond_b_share_below_ge_0.40"]
                      and p1["cond_c_ge3_forces_with_label1"])
    check("V7 prong passes + verdict labels",
          prong1_all == headline["prong1_nonvacuity"]["pass"]
          and prong2 == p2["pass"]
          and headline["e4_bar_cleared"] == bool(
              prong1_all and prong2 and crit[primary])
          and headline["forecasting_verdict"] == (
              "VACUOUS AGAIN" if not prong1_all else
              "FORECASTING ALIVE AT ADAPTED SCALE" if prong2 else
              "FORECASTING DEAD AT ADAPTED SCALE TOO"))

    # V8: family-1 secondary arm recomputed
    f1 = json.load(open(os.path.join(R4, "f1_arm.json")))
    pm1 = pd.read_csv(os.path.join(BASE, "results", "population_metrics.csv"))
    tau_f1 = float(np.quantile(pm1.eo_gap.to_numpy(float), 0.70))
    check("V8 f1 tau*", close(tau_f1, f1["tau_star_f1_eo"], 1e-12),
          f"tau*_F1={tau_f1:.6f}")
    pop1 = {}
    for (task, state), grp in pm1.groupby(["task", "state"]):
        s = grp.set_index("year")["eo_gap"]
        pop1[f"{task}|{state}"] = [float(s[y]) for y in
                                   (2014, 2015, 2016, 2017, 2018, 2019)]
    n_cross = sum(1 for ser in pop1.values()
                  if any(v >= tau_f1 for v in ser)
                  and next(i for i, v in enumerate(ser)
                           if v >= tau_f1) >= 1)
    share_below = float(np.mean([ser[0] < tau_f1
                                 for ser in pop1.values()]))
    fp1 = f1["prong1_nonvacuity"]
    check("V8 f1 prong1",
          n_cross == fp1["n_cross_after_base"]
          and close(share_below, fp1["share_below_at_base"], 1e-12),
          f"cross={n_cross} share={share_below:.3f}")
    l1 = pd.read_parquet(os.path.join(R4, "f1_arm_leads.parquet"))
    g1 = l1[(l1.H == 2) & (l1.far_target == 0.10)]
    boot1 = bootstrap_deltas(g1, BASELINES,
                             seed=stable_seed("e4", "boot", "f1"))
    ok = True
    for b in BASELINES:
        hb = f1["prong2_forecasting"]["per_baseline"][b]
        ok = ok and close(boot1[b]["delta"], hb["delta"], 1e-9) \
            and close(boot1[b]["ci_lo"], hb["ci_lo"], 1e-9) \
            and close(boot1[b]["ci_hi"], hb["ci_hi"], 1e-9)
    check("V8 f1 bootstrap deltas/CIs", ok)
    f1folds = pd.read_csv(os.path.join(R4, "f1_accounting_folds.csv"))
    f1scores = pd.read_parquet(os.path.join(R4, "f1_accounting_scores.parquet"))
    meds, passes = [], 0
    ok = True
    for _, fr in f1folds.iterrows():
        sc = f1scores[f1scores.fold == fr.fold]
        tr = sc[sc.role == "train"]
        te = sc[sc.role == "test"]
        tv = tv_hist(te.loc[te.y == 0, "p"], tr.loc[tr.y == 0, "p"])
        dev = abs(float((te.loc[te.y == 0, "p"] >= fr.theta).mean())
                  - float((tr.loc[tr.y == 0, "p"] >= fr.theta).mean()))
        ok = ok and close(tv, fr.tv50) and close(dev, fr.deviation)
        meds.append(tv)
        passes += bool(dev <= tv + 0.02)
    crit1 = bool(np.median(meds) >= 0.05 and passes / len(meds) >= 0.99)
    check("V8 f1 accounting", ok and crit1
          == f1["prong3_accounting"]["pass"], f"criterion={crit1}")

    # V9: sensitivity rows consistent with the summary table
    try:
        sens = pd.read_csv(os.path.join(R4, "sensitivity4.csv"))
    except pd.errors.EmptyDataError:
        sens = pd.DataFrame()
    if len(sens) == 0:
        subset = summ[(summ.model == primary) & (summ.metric == "eo")
                      & (summ.qtag.isin(["q60", "q80"])) & (summ.H == 2)
                      & (summ.far_target == 0.10)]
        check("V9 sensitivity empty (degenerate taus)", len(subset) == 0)
        sens = None
    if sens is not None:
        ok = len(sens) > 0
        for _, srow in sens.iterrows():
            match = summ[(summ.model == srow.model)
                         & (summ.metric == srow.metric)
                         & (summ.qtag == srow.qtag) & (summ.H == srow.H)
                         & (summ.method == srow.method)
                         & (summ.far_target == srow.far_target)]
            ok = ok and len(match) == 1 \
                and close(match.iloc[0].median_lead, srow.median_lead) \
                and close(match.iloc[0].coverage, srow.coverage)
        check("V9 sensitivity subset consistency", ok)

    print()
    if FAILURES:
        print("FAILURES:", FAILURES)
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
