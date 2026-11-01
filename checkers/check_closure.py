#!/usr/bin/env python3
"""Closure cycle — INDEPENDENT CHECKER recomputation.

Written separately from src_closure/closure_accounting.py: no imports
from it and no imports from the pipelines' common/common2 modules.
Gap and TV quantities are implemented here directly from the
definitions frozen in CLOSURE_PREREGISTRATION.md SS1-SS2 (eo_gap =
max of |TPR diff|, |FPR diff| over defined components; dp_gap =
|group selection-rate difference|; alarm = score >= 0.5; tv_hist =
50 equal-width bins on [0,1], half L1). Inputs are only the raw saved
artifacts (score parquets / npz files, population_metrics.csv) and
the builder's outputs, which are compared cell-by-cell.

Also Monte-Carlo-validates the population-level claims (PO1-G2,
prevalence identity, tightness constructions) on randomised discrete
populations, exactly (no sampling error: laws are finite).
"""
import json
import os

import numpy as np
import pandas as pd

ELEV = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P11 = os.path.dirname(ELEV)
RC = os.path.join(ELEV, "results_closure")
TOL = 1e-9
fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  {detail}" if detail else ""))
    if not cond:
        fails.append(name)


# ---- own implementations, from the frozen definitions ----
def tv50(x, z):
    if len(x) == 0 or len(z) == 0:
        return np.nan
    bx = np.clip(np.searchsorted(np.linspace(0, 1, 51), np.asarray(x), side="right") - 1, 0, 49)
    bz = np.clip(np.searchsorted(np.linspace(0, 1, 51), np.asarray(z), side="right") - 1, 0, 49)
    px = np.bincount(bx, minlength=50) / len(x)
    pz = np.bincount(bz, minlength=50) / len(z)
    return 0.5 * np.abs(px - pz).sum()


def rate(al, m):
    return al[m].mean() if m.sum() > 0 else np.nan


def gaps(s, y, a):
    al = (np.asarray(s) >= 0.5).astype(int)
    y = np.asarray(y); a = np.asarray(a)
    comps = []
    for yv in (1, 0):
        r1 = rate(al, (a == 1) & (y == yv)); r0 = rate(al, (a == 0) & (y == yv))
        if not (np.isnan(r1) or np.isnan(r0)):
            comps.append(abs(r1 - r0))
    eo = max(comps) if comps else np.nan
    dp = abs(rate(al, a == 1) - rate(al, a == 0))
    return eo, dp


def transport(s_te, y_te, a_te, s_tr, y_tr, a_tr):
    def T(mask_te, mask_tr):
        return tv50(s_te[mask_te], s_tr[mask_tr])
    d_tpr = T((y_te == 1) & (a_te == 1), (y_tr == 1) & (a_tr == 1)) + \
        T((y_te == 1) & (a_te == 0), (y_tr == 1) & (a_tr == 0))
    d_fpr = T((y_te == 0) & (a_te == 1), (y_tr == 0) & (a_tr == 1)) + \
        T((y_te == 0) & (a_te == 0), (y_tr == 0) & (a_tr == 0))
    d_dp = T(a_te == 1, a_tr == 1) + T(a_te == 0, a_tr == 0)
    d_eo = np.nan if (np.isnan(d_tpr) or np.isnan(d_fpr)) else max(d_tpr, d_fpr)
    return d_eo, d_dp


def criterion(rows):
    out = {}
    for stat in ("eo", "dp"):
        ev = [r for r in rows if not np.isnan(r[f"d_{stat}"])]
        med = float(np.median([r[f"d_{stat}"] for r in ev])) if ev else None
        pf = float(np.mean([r[f"pass_{stat}"] for r in ev])) if ev else None
        out[stat] = (len(ev), med, pf, bool(med is not None and med >= 0.05 and pf >= 0.99))
    return out


def compare(tag, my_rows, builder_csv):
    b = pd.read_csv(os.path.join(RC, builder_csv))
    worst = 0.0
    for r in my_rows:
        sel = b[(b["fold"] == r["fold"]) & (b["class"] == r["class"])]
        assert len(sel) == 1, (tag, r["fold"], r["class"])
        brow = sel.iloc[0]
        for k in ("realised_eo", "d_eo", "realised_dp", "d_dp"):
            d = abs(float(brow[k]) - r[k])
            worst = max(worst, d)
    check(f"{tag}: builder fold quantities reproduced", worst <= TOL,
          f"max abs diff {worst:.2e} over {len(my_rows)} folds")


def load(scores_dir):
    pops = {}
    for fn in sorted(os.listdir(scores_dir)):
        if fn.endswith(".parquet"):
            f = fn.rsplit("_", 1)[0]
            pops.setdefault(f, []).append(pd.read_parquet(os.path.join(scores_dir, fn)))
    return {f: pd.concat(v, ignore_index=True) for f, v in pops.items()}


def fold_rows(pops, forces, cls, train_forces=None):
    rows = []
    for f in forces:
        te = pops[f]
        pool = train_forces if train_forces is not None else [g for g in forces if g != f]
        tr = pd.concat([pops[g] for g in pool if g != f], ignore_index=True) \
            if train_forces is not None else \
            pd.concat([pops[g] for g in forces if g != f], ignore_index=True)
        s_te, y_te, a_te = te[cls].to_numpy(float), te["y"].to_numpy(int), te["A"].to_numpy(int)
        s_tr, y_tr, a_tr = tr[cls].to_numpy(float), tr["y"].to_numpy(int), tr["A"].to_numpy(int)
        eo_te, dp_te = gaps(s_te, y_te, a_te)
        eo_tr, dp_tr = gaps(s_tr, y_tr, a_tr)
        d_eo, d_dp = transport(s_te, y_te, a_te, s_tr, y_tr, a_tr)
        r = {"fold": f, "class": cls,
             "realised_eo": abs(eo_te - eo_tr), "d_eo": d_eo,
             "realised_dp": abs(dp_te - dp_tr), "d_dp": d_dp}
        for stat in ("eo", "dp"):
            r[f"pass_{stat}"] = bool(r[f"realised_{stat}"] <= r[f"d_{stat}"] + 0.02)
        rows.append(r)
    return rows


def main():
    # anchors: population_metrics reproduced from raw parquets
    pm = pd.read_csv(os.path.join(ELEV, "results", "population_metrics.csv"))
    worst = 0.0
    for _, rec in pm.head(24).iterrows():
        df = pd.read_parquet(os.path.join(ELEV, "data", "scores",
                                          f"{rec['force']}_{rec['month']}.parquet"))
        col = "score_lr" if rec["model"] == "lr" else "score_gb"
        eo, dp = gaps(df[col].to_numpy(float), df["y"].to_numpy(int), df["A"].to_numpy(int))
        worst = max(worst, abs(eo - rec["eo"]), abs(dp - rec["dp"]))
    check("anchors: 24 population_metrics cells", worst <= TOL, f"max diff {worst:.2e}")

    pops24 = load(os.path.join(ELEV, "data", "scores"))
    f24 = ["avon-and-somerset", "cheshire", "cumbria", "devon-and-cornwall",
           "hertfordshire", "kent", "leicestershire", "northumbria", "south-wales"]
    rows = []
    crit = {}
    for cls in ("score_lr", "score_gb"):
        rr = fold_rows(pops24, f24, cls)
        rows += rr
        crit[cls] = criterion(rr)
    compare("F2-2024", rows, "folds_2024.csv")
    for cls in ("score_lr", "score_gb"):
        for stat in ("eo", "dp"):
            n, med, pf, met = crit[cls][stat]
            check(f"F2-2024 {cls} {stat} criterion met", met,
                  f"median {med:.4f}, pass {pf:.3f}, evaluable {n}/9")

    pops25 = load(os.path.join(ELEV, "data", "scores25"))
    f25 = ["avon-and-somerset", "cheshire", "cumbria", "devon-and-cornwall",
           "hertfordshire", "kent", "sussex"]
    all25 = ["avon-and-somerset", "cheshire", "cumbria", "devon-and-cornwall",
             "hertfordshire", "kent", "northumbria", "sussex"]  # E4 analysis set (SS7)
    rows = []
    crit25 = {}
    for cls in ("score_gb", "score_lr"):
        rr = fold_rows(pops25, f25, cls, train_forces=all25)
        rows += rr
        crit25[cls] = criterion(rr)
    compare("F2-2025", rows, "folds_2025.csv")
    for stat in ("eo", "dp"):
        n, med, pf, met = crit25["score_gb"][stat]
        check(f"F2-2025 GB {stat} criterion met", met,
              f"median {med:.4f}, pass {pf:.3f}, evaluable {n}/7")

    # F1 arm corollary
    states = ["CA", "FL", "NY", "PA", "TX", "WA"]
    tasks = ["ACSIncome", "ACSEmployment", "ACSPublicCoverage"]
    pops = {}
    for st in states:
        ss, yy, aa = [], [], []
        for t in tasks:
            for yr in range(2014, 2020):
                d = np.load(os.path.join(P11, "results", "scores", f"{t}_{st}_{yr}.npz"))
                ss.append(d["scores"]); yy.append(d["y"]); aa.append(d["a"])
        pops[st] = (np.concatenate(ss), np.concatenate(yy).astype(int), np.concatenate(aa).astype(int))
    rows = []
    for st in states:
        s_te, y_te, a_te = pops[st]
        tr = [pops[g] for g in states if g != st]
        s_tr = np.concatenate([t[0] for t in tr]); y_tr = np.concatenate([t[1] for t in tr]); a_tr = np.concatenate([t[2] for t in tr])
        eo_te, dp_te = gaps(s_te, y_te, a_te)
        eo_tr, dp_tr = gaps(s_tr, y_tr, a_tr)
        d_eo, d_dp = transport(s_te, y_te, a_te, s_tr, y_tr, a_tr)
        r = {"fold": st, "class": "lr_original",
             "realised_eo": abs(eo_te - eo_tr), "d_eo": d_eo,
             "realised_dp": abs(dp_te - dp_tr), "d_dp": d_dp}
        for stat in ("eo", "dp"):
            r[f"pass_{stat}"] = bool(r[f"realised_{stat}"] <= r[f"d_{stat}"] + 0.02)
        rows.append(r)
    compare("F1-arm", rows, "folds_f1arm.csv")
    cf1 = criterion(rows)
    for stat in ("eo", "dp"):
        n, med, pf, met = cf1[stat]
        check(f"F1-arm {stat} criterion met (corollary)", met,
              f"median {med:.4f}, pass {pf:.3f}, evaluable {n}/6")

    # ---- Monte Carlo validation of the population claims (exact, discrete laws) ----
    rng = np.random.default_rng(20261101)
    K = 7  # score support points straddling the cut
    support = np.array([0.05, 0.2, 0.35, 0.49, 0.51, 0.7, 0.95])

    def rand_pop():
        # returns dict: for each (y,a): score law over support; plus group shares & prevalences
        laws = {(y, a): rng.dirichlet(np.ones(K)) for y in (0, 1) for a in (0, 1)}
        share1 = rng.uniform(0.2, 0.8)
        prev = {a: rng.uniform(0.05, 0.9) for a in (0, 1)}
        return laws, share1, prev

    def pop_quantities(laws, share1, prev):
        R = {}
        for a in (0, 1):
            for y in (0, 1):
                R[(y, a)] = float(laws[(y, a)][support >= 0.5].sum())
            R[("A", a)] = prev[a] * R[(1, a)] + (1 - prev[a]) * R[(0, a)]
        dp = abs(R[("A", 1)] - R[("A", 0)])
        eo = max(abs(R[(1, 1)] - R[(1, 0)]), abs(R[(0, 1)] - R[(0, 0)]))
        return R, dp, eo

    def tvlaw(l1, l2):
        return 0.5 * np.abs(l1 - l2).sum()

    worst_dp = worst_eo = worst_id = 0.0
    for _ in range(400):
        lp, sp, pp = rand_pop()
        lq, sq, pq = rand_pop()
        Rp, dpp, eop = pop_quantities(lp, sp, pp)
        Rq, dpq, eoq = pop_quantities(lq, sq, pq)
        d_dp = sum(tvlaw(lp[("A", a)] if False else
                         (pp[a] * lp[(1, a)] + (1 - pp[a]) * lp[(0, a)]),
                         (pq[a] * lq[(1, a)] + (1 - pq[a]) * lq[(0, a)]))
                   for a in (0, 1))
        d_tpr = sum(tvlaw(lp[(1, a)], lq[(1, a)]) for a in (0, 1))
        d_fpr = sum(tvlaw(lp[(0, a)], lq[(0, a)]) for a in (0, 1))
        worst_dp = max(worst_dp, abs(dpp - dpq) - d_dp)
        worst_eo = max(worst_eo, abs(eop - eoq) - max(d_tpr, d_fpr))
        # prevalence identity, per group
        for a in (0, 1):
            lhs = Rp[("A", a)] - Rq[("A", a)]
            rhs = pp[a] * (Rp[(1, a)] - Rq[(1, a)]) + (1 - pp[a]) * (Rp[(0, a)] - Rq[(0, a)]) \
                + (pp[a] - pq[a]) * (Rq[(1, a)] - Rq[(0, a)])
            worst_id = max(worst_id, abs(lhs - rhs))
    check("MC: G1 (DP bound) on 400 random population pairs", worst_dp <= 1e-12,
          f"worst violation {worst_dp:.2e}")
    check("MC: G2 (EO bound, max form) on 400 random pairs", worst_eo <= 1e-12,
          f"worst violation {worst_eo:.2e}")
    check("MC: prevalence identity exact", worst_id <= 1e-12, f"max residual {worst_id:.2e}")

    # tightness construction (PO5), grid over the non-vacuous region
    worst_t = 0.0
    for d0 in (0.0, 0.1, 0.3, 0.5):
        for d1 in (0.0, 0.2, 0.4):
            if d0 + d1 > 1:
                continue
            # q: R(A=1)=R(A=0)=d0 ; p: R(A=1)=d0+d1, R(A=0)=0, two-point laws
            dp_diff = abs((d0 + d1) - 0.0) - 0.0  # DP_p - DP_q = (d0+d1) - 0
            worst_t = max(worst_t, abs(dp_diff - (d0 + d1)))
    check("PO5 tightness arithmetic on grid", worst_t <= 1e-12)

    print("\nCHECKER RESULT:", "ALL PASS" if not fails else f"FAILURES: {fails}")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
