# Closure — Independent Checker Report

**Cycle:** Paper 11 closure cycle. **Checked artifacts:**
`CLOSURE_PROOF.md` (PO1–PO6), `src_closure/closure_accounting.py`
(PO7) and its outputs in `results_closure/`, against
`CLOSURE_PREREGISTRATION.md` (frozen 2026-11-01T18:14:37Z, SHA-256
`4f4b10625ea08618fbc05098daa9c5d5492154847bb8cb8a8875538e925c56f3`).

**Independence.** The numerical check (`src_closure_checker/
check_closure.py`) imports nothing from `src_closure/` and nothing
from the pipelines' `common.py`/`common2.py`; the gap and TV
quantities are implemented there directly from the definitions
frozen in the pre-registration §§1–2, reading only the raw saved
artifacts. The proof obligations are graded from a separate read of
the proof text. Verdict vocabulary: DISCHARGED / GAP /
ASSUMPTION-ADDED, as in the E3 checker pattern.

## Numerical recomputation (all from the raw artifacts)

```
PASS anchors: 24 population_metrics cells            max diff 0.00e+00
PASS F2-2024: builder fold quantities reproduced     max abs diff 0.00e+00 over 18 folds
PASS F2-2024 score_lr eo criterion met   median 0.4149, pass 1.000, evaluable 9/9
PASS F2-2024 score_lr dp criterion met   median 0.3135, pass 1.000, evaluable 9/9
PASS F2-2024 score_gb eo criterion met   median 0.5011, pass 1.000, evaluable 9/9
PASS F2-2024 score_gb dp criterion met   median 0.4427, pass 1.000, evaluable 9/9
PASS F2-2025: builder fold quantities reproduced     max abs diff 0.00e+00 over 14 folds
PASS F2-2025 GB eo criterion met         median 0.3442, pass 1.000, evaluable 7/7
PASS F2-2025 GB dp criterion met         median 0.3241, pass 1.000, evaluable 7/7
PASS F1-arm: builder fold quantities reproduced      max abs diff 0.00e+00 over 6 folds
PASS F1-arm eo criterion met (corollary) median 0.1104, pass 1.000, evaluable 6/6
PASS F1-arm dp criterion met (corollary) median 0.1020, pass 1.000, evaluable 6/6
PASS MC: G1 (DP bound) on 400 random population pairs    worst violation 0.00e+00
PASS MC: G2 (EO bound, max form) on 400 random pairs     worst violation 0.00e+00
PASS MC: prevalence identity exact                       max residual 1.67e-16
PASS PO5 tightness arithmetic on grid
CHECKER RESULT: ALL PASS
```

The zero differences are expected, not suspicious: every fold
quantity is an exact rational functional of the same saved record
sets, and the checker's independent binning (searchsorted into the
same 50 equal-width bins) coincides with `tv_hist`'s histogram
binning on every record. The Monte Carlo block validates the
*population-level* claims independently of the fold code: G1, G2
(incl. the max step) and the prevalence identity hold exactly on
400 randomised discrete population pairs (finite laws; no sampling
error), and the PO5 attainability arithmetic checks on its grid.

## Obligation-by-obligation grading

- **PO1 (stratum lemma) — DISCHARGED.** The proof is the variational
  definition applied to the single event [c, 1]; the identification
  of T1 as the same argument on the null-step stratum is correct
  (WS3's FAR is one event's probability under the step-score law).
- **PO2 (G1, DP) — DISCHARGED.** Reverse-triangle then triangle
  step is valid; the definitional match to `dp_gap` was verified
  against both code copies (`src/common.py` 64–67;
  `common2.py` 77–83): |selection-rate difference|, cut ≥ 0.5.
- **PO3 (G2, EO max form) — DISCHARGED.** The max step
  |max(u,v) − max(u′,v′)| ≤ max(|u−u′|, |v−v′|) is proved correctly;
  component bounds are PO2's argument within stratum families; the
  definitional match to `eo_gap` (max over defined components) was
  verified against both code copies. The scope remark is accurate:
  statistic and bound lose the same component at the same place.
- **PO4 (G3 reduction + covariate corollary) — DISCHARGED.** The
  prevalence identity's algebra was re-derived independently in
  this pass and is numerically exact (MC residual ≤ 1.67e-16). The
  reduction's terms are as registered: label-stratified (FAR-type
  and TPR-type) transports, prevalences, one realised rate
  difference per group — all measurable from the same artifacts.
  Data processing for the covariate corollary is correctly invoked.
- **PO5 (G4 tightness) — DISCHARGED, with one presentational defect
  found and fixed during this pass.** The proof's first draft
  carried a discarded intermediate arrangement in the sum-form
  paragraph whose populations do not attain equality; the attaining
  construction that follows it is correct (verified arithmetically
  on the grid, and its stratum TVs are as claimed). The paragraph
  was rewritten to the attaining construction only; the correction
  is recorded here, per the cycle's corrections-on-record practice.
  The restriction of the tightness claim to the non-vacuous region
  (D ≤ 1) is stated in the text and is the correct scope.
- **PO6 (G5 estimation honesty) — DISCHARGED.** The binning step
  (binned TV ≤ population TV) is correct, and the document states
  the slack's status exactly as registered: the criterion's pass is
  an empirical accounting fact, not a corollary of the theorem; the
  0.02 is T4's inherited design constant. This checker additionally
  requires — and `CLOSURE_RESULTS.md` carries — the companion
  observation that on family 2 the gap criterion passes with very
  wide margins because the realised gap transports there are tiny
  (≤ 0.017) relative to the transport quantities (0.20–0.50): the
  gap accounting on family 2 is *loose*, and no text downstream of
  this cycle may present it as the binding evidence on that family.
- **PO7 (fold computation) — DISCHARGED.** Fold partitions match
  the pre-registration §7 exactly (2024: LOSO over the 9-force set,
  train = other 8; 2025: the 7 evaluable GB folds, train = other 7
  of the 8-force analysis set; F1 arm: LOSO over the 6 states,
  pooled 3 tasks × 2014–2019); all quantities reproduced
  independently (above); the 24 anchor cells tie the score files to
  the recorded population table exactly.

**ASSUMPTION-ADDED verdicts: none.** The only scope condition in
the proved statements (positive stratum mass; state-blindness) is
the one registered in the pre-registration §3 as part of the
primary statement. No demotion from DM1–DM4 was needed or taken.
