# Closure Results — the Transport Bound for the EO/DP Gap Statistics

**Cycle:** Paper 11 closure cycle, under `CLOSURE_PREREGISTRATION.md`
(frozen 2026-11-01T18:14:37Z, SHA-256
`4f4b10625ea08618fbc05098daa9c5d5492154847bb8cb8a8875538e925c56f3`).
**Proof:** `CLOSURE_PROOF.md`. **Independent check:**
`CLOSURE_CHECKER_REPORT.md` (own recomputation,
`src_closure_checker/check_closure.py`: ALL PASS; obligations
PO1–PO7 all DISCHARGED; no assumption-added verdicts).

---

## 1. Status: CLOSED AT REGISTERED STRENGTH

The transport bound is derived for the gap statistics exactly as
the E2/E4 pipelines define them:

- **G1 (DP):** |DP_p − DP_q| ≤ TV(μ_p^{A=1}, μ_q^{A=1}) +
  TV(μ_p^{A=0}, μ_q^{A=0}) — the sum of the two group-conditional
  score-law TVs.
- **G2 (EO, the pipelines' max form):** |EO_p − EO_q| ≤
  max(D_TPR, D_FPR), with D_TPR / D_FPR the sums of the
  label-stratified score-law TVs; the componentwise bounds hold
  individually.
- **G3:** both are compositions of Theorem 1's own single-event
  argument over strata (no new inequality); the prevalence
  decomposition reduces DP transport to FAR-type (label-0) and
  TPR-type transports plus named, measurable prevalence terms; the
  covariate-TV form follows as a weaker corollary.
- **G4:** the forms are best possible as functions of the stratum
  TVs alone (attained on the non-vacuous region).
- **G5:** the T4 accounting criterion transported to the gap
  functionals (tv_hist 50-bin, slack 0.02, median ≥ 0.05, pass
  fraction ≥ 0.99), computed per fold in §3 below.

**Demotions taken: none** (DM1–DM4 all unused). **Kill criterion:
not triggered.** The one scope condition — positive stratum mass in
both populations, with state-blindness — was registered in the
primary statement (§3 of the pre-registration), not added en route.

The structural objection that commissioned this cycle — *Theorem 1
bounds the FAR while the monitored statistics are the EO/DP gaps* —
is therefore closed at the level of the theorem: the audited
statistics now have their own transport bound, in the same form,
for the same objects, at the same per-fold granularity.

## 2. What the closure does not change

- It proves a bound for the gaps; it does not make the family-2 gap
  accounting *strong* evidence. On family 2 the realised gap
  transports are tiny (max 0.0165 across all 2024/2025 folds)
  because the deployed gaps there are small (test-fold EO gaps
  ≤ 0.024) and barely move; the transport quantities are 0.20–0.50.
  The criterion passes with minimum margins of 0.22–0.31 — the
  accounting is correct and loose. The binding accounting evidence
  on family 2 remains the FAR accounting of E2/E4.
- Per PO6, a criterion pass is an empirical accounting fact, not a
  corollary of the theorem (the theorem bounds realised transport
  by the *unbinned* D_G; the criterion compares against the binned
  D̂_G plus the registered 0.02 slack — the same status T4's pass
  has for FAR).
- Nothing here touches the forecasting record: both FALSIFIER-U
  results, the vacuity mechanisms, and E3's boundary stand exactly
  as recorded. The gap bound also *explains part of that record's
  shape* without rescuing any claim: where gaps are small and
  strata transports are large, threshold crossings of the gaps are
  rare events priced loosely by transport — consistent with E3's
  C2 (crossing rarity), now statable for the gap statistics
  themselves.

## 3. The gap-form accounting (G5), computed

Per-fold quantities: `results_closure/folds_2024.csv`,
`folds_2025.csv`, `folds_f1arm.csv`; summary
`results_closure/closure_summary.json`. Anchors: 24 recorded
population-table cells reproduced exactly from the score files
(builder and checker independently).

| Cell | Statistic | Median D̂ | Pass | Min margin (fold) | Max realised |
|---|---|---|---|---|---|
| F2-2024 LR | EO | 0.4149 | 9/9 | 0.2718 (kent) | 0.0058 |
| F2-2024 LR | DP | 0.3135 | 9/9 | 0.2667 (devon-and-cornwall) | 0.0055 |
| F2-2024 GB | EO | 0.5011 | 9/9 | 0.3112 (kent) | 0.0165 |
| F2-2024 GB | DP | 0.4427 | 9/9 | 0.2958 (devon-and-cornwall) | 0.0040 |
| F2-2025 GB | EO | 0.3442 | 7/7 | 0.2886 (avon-and-somerset) | 0.0043 |
| F2-2025 GB | DP | 0.3241 | 7/7 | 0.2819 (kent) | 0.0014 |
| F2-2025 LR *(descriptive)* | EO | 0.2845 | 7/7 | 0.2358 (kent) | 0.0059 |
| F2-2025 LR *(descriptive)* | DP | 0.2787 | 7/7 | 0.2154 (kent) | 0.0044 |
| F1 arm (C-F1) | EO | 0.1104 | 6/6 | 0.0854 (WA) | 0.0523 |
| F1 arm (C-F1) | DP | 0.1020 | 6/6 | 0.0745 (WA) | 0.0244 |

The criterion (median ≥ 0.05 AND pass fraction ≥ 0.99) is **met for
both statistics in every computed cell**. The family-1 arm is the
tightest and most informative: realised gap transports up to 0.052
priced by transport quantities with median ≈ 0.10–0.11 — the
accounting there is doing real work, as the FAR accounting did on
the same folds (E4: median TV50 0.4053, 6/6).

## 4. Re-adjudication of the recorded verdicts (pre-registration §6 rule)

| # | Recorded verdict | Under the gap bound | Reason |
|---|---|---|---|
| V1 | F1 LR **met** (0.3481, 50/50) | **STANDS OUTSIDE** | Rule (a): the upgrade tree with its 51-jurisdiction folds did not survive; no per-record artifacts for *those* folds exist, and no other folds may re-adjudicate them. The verdict remains exactly what it was: a FAR-accounting verdict under T1/T4. |
| V2 | F1 GB **not met** (0.1358, 50/51) | **STANDS OUTSIDE** | Rule (a), as V1. The near-miss (one fold beyond slack by 0.0034) remains a FAR-accounting fact. |
| V3 | F2-2024 LR **met** (0.4784, 9/9) | **FOLLOWS** | Gap-form criterion met for EO (0.4149, 9/9) and DP (0.3135, 9/9) on the verdict's own folds. |
| V4 | F2-2024 GB **met** (0.2865, 9/9) | **FOLLOWS** | EO (0.5011, 9/9) and DP (0.4427, 9/9) met on its own folds. |
| V5 | F2-2025 GB **met** (0.3475, 7/7) | **FOLLOWS** | EO (0.3442, 7/7) and DP (0.3241, 7/7) met on its own (evaluable) folds. |

**C-F1 (corollary, non-adjudicative):** on the E4 family-1 arm's own
folds (LOSO over 6 states, original deployed LR), the gap-form
criterion is met for both statistics (EO median D̂ 0.1104, 6/6; DP
0.1020, 6/6). This shows the gap accounting holds where family-1
artifacts exist to test it; it re-adjudicates nothing about V1/V2,
whose folds are different and lost.

**Net position after the closure.** Of the five recorded accounting
verdicts, the three whose artifacts survive now hold under **both**
the FAR bound (T1/T4, as recorded) and the gap-statistic bound
(G1/G2/G5, this cycle). The two family-1 verdicts stand outside the
gap bound for an archival reason, stated as such wherever they are
cited — and the family-1 corollary shows the gap criterion met on
the family-1 folds that do survive.

## 5. Consequences registered for Stage 3

The revised draft (Stage 3) may now:
- state the transport bound for the gap statistics themselves
  (G1/G2, with G3's reduction and G4's tightness), repairing the
  rebuild's three-way object conflation (audited T1 vs printed
  Theorem 1 vs monitored statistics);
- attribute V3–V5 to both accountings, V1/V2 to the FAR accounting
  only (with the artifact-absence reason), and cite C-F1 as the
  family-1 gap evidence, labelled corollary;
- carry the looseness honesty of §2 verbatim in substance: on
  family 2 the gap accounting is correct but loose, and the FAR
  accounting is the binding one there.
It may not: claim any re-adjudication of V1/V2; present a criterion
pass as a theorem corollary; or revive any forecasting claim.
