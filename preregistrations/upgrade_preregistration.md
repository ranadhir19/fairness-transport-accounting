# Paper 11 — Upgrade-Loop Pre-Registration

**Written:** 2026-10-29, BEFORE any upgrade experiment, forecaster run, or
theorem numerics. **Approved scope (site owner, 2026-10-29):** full upgrade —
(1) broader study, (2) transport-robust forecaster, (3) one theorem attempt.

**Baseline this loop builds on (all preserved untouched):** the reframed
Paper 11 (`files/Paper_11_FairnessBreachForecasting.tex/.pdf`), certified 4/10
by the fresh tester (`tester_report.md`) and verified at its 5/10 reframe
ceiling (`reframe_verification.md`). The verifier's five caps are this loop's
work order: *one benchmark family, one classifier class, 7 forecastable
trajectories, a falsified headline method, a batch-silent certificate.*

**Amendment discipline (binding):** this file is append-only. Any change
after this timestamp is appended as a dated amendment with its reason, BEFORE
the affected run wherever the change is a protocol change. No silent
re-registration, no headline shopping. In particular, the original build's
Amendment A1 (τ re-registration after the population audit) is **not**
repeatable here: if a headline cell defined below is vacuous at the expanded
scope, the vacuity is reported as a finding, not cured by re-registration.

**Artifact discipline (binding):** every upgrade artifact lives under
`hidden_files/paper11_work/upgrade/` (`src/`, `data/`, `results/`). The
baseline tree (`src/`, `results/`, `validate.py` stages 1–6) is read-only
input. Every number in the upgrade report and any upgraded manuscript is
produced by a script from saved artifacts, in the generator pattern of the
original build.

---

## WS1 — Broader study (foundation)

### Data scope (fixed)
- **Source:** folktables (Ding et al. 2021) ACS 1-year PUMS, via the pinned
  venv (folktables 0.0.12). Natural temporal and geographic shift only;
  injected/synthetic drift remains FORBIDDEN as evidence.
- **States (51):** the 50 US states plus the District of Columbia:
  AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS
  MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI
  WY. **Puerto Rico is excluded**: the Puerto Rico Community Survey is a
  separate survey instrument from the ACS, and the claim scope is US states.
- **Years (9):** 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023.
  **2020 is excluded**: the Census Bureau released 2020 ACS 1-year data as an
  experimental product with non-standard methodology and cautions against
  comparing it with other years; the original design excluded it on the same
  ground. Consequence, disclosed here: the 2019→2021 monitoring step spans
  two calendar years. Steps are per available ACS release; all lead times
  and horizon labels are computed in **calendar years**, so the gap is
  handled arithmetically, not hidden.
- **Tasks (3, unchanged):** ACSIncome, ACSEmployment, ACSPublicCoverage.
  Groups unchanged: A = 1 iff RAC1P == 1. Protected attribute excluded from
  features. The 2019+ RELP→RELSHIPP alias from the original build applies to
  every year lacking RELP.
- **Encoding (fixed):** one-hot for all non-continuous features; continuous =
  {AGEP, WKHP} standardised by pooled base-year mean/SD. The category spec is
  the **union over all included years and states** for the task, computed in
  a preliminary pass before any model is trained (a fixed encoding, not fit
  to outcomes). *Registered difference from the original build*, which used a
  base-year-only spec; the union spec avoids silently dropping post-2018
  occupation-code revisions.

### Deployed models (two classes, both frozen at 2014)
Per task, trained on pooled all-51-state 2014 data, never retrained:
- **LR:** LogisticRegression(C=1.0, lbfgs, max_iter=2000) on the sparse
  one-hot design, 70% train split with rng seed 0 — the original protocol,
  with the pool widened from 6 states to 51.
- **GB:** HistGradientBoostingClassifier(max_iter=300, learning_rate=0.06,
  max_leaf_nodes=31, min_samples_leaf=200, early_stopping=False) on the
  dense one-hot design, trained on a deterministic subsample of at most
  **300,000** pooled base-year rows (rng seed 0) — a compute constraint of
  the 7 GB build box, fixed here in advance, not a results-driven choice.
- Both models score every (task, state, year) population cell; scores,
  labels, groups saved per (task, model, state, year).

### Protocol (unchanged from DESIGN.md unless stated)
- Trajectories: (task × state × model class) = 3 × 51 × 2 = **306**.
- Monitoring: one batch of n = 2,000 per (trajectory, seed, year), R = 25
  seeds, `stable_seed` including the model-class tag. Base year 2014 is the
  deployment-audit step; forecast/detection instances are the 8 monitor
  years. Batch features identical to the original monitor (same feature
  definitions, including the per-group and per-group-and-label histogram-TV
  drift budgets ε_dp, ε_eo, 50 bins).
- Population truth: metrics on each state-year's FULL population under the
  frozen model of that class. Breach = first calendar year the population
  metric ≥ τ.
- Metrics/thresholds/horizons (unchanged): EO gap (headline), DP gap;
  τ ∈ {0.05, 0.10}; H ∈ {1, 2} calendar years; FAR targets {0.05, 0.10,
  0.20}; decision cut 0.5.
- Population metrics at this scope are a **new study**: the frozen models
  are retrained on the 51-state pool, so expanded-scope population numbers
  supersede — and will differ from — the 18-trajectory numbers of the
  baseline paper. The baseline artifacts are not expected to be reproduced
  and no equality with them is asserted anywhere.

### WS1 deliverables (fixed)
1. Population audit at expanded scope, per (metric, τ, model class):
   trajectory count, ever-crossing count, first-crossings-after-base-year
   count with the list, base-year-breach count, never-crossing count.
2. **Certificate population-exact re-check** at expanded scope (both
   metrics, both model classes): the drift-budget inequality must hold at
   every (trajectory, t, h). Expected exactly 0 violations; any violation
   is an implementation error to be fixed, not a finding.
3. **Batch certificate re-run** with the original construction (batch upper
   bound + batch histogram-TV budgets) at n = 2,000: bound coverage and
   number of certified positive safe horizons, per (metric, τ, model
   class). Reported whatever it shows — including if it is still silent.

---

## WS2 — Transport-robust forecaster

### Diagnosis being designed against (from the verified baseline)
A single global alarm threshold, calibrated to FAR 0.10 on training states,
fires on a held-out state at per-fold FAR 0.005–1.000 (fold mean 0.293):
**false-alarm calibration does not transport across states**, because the
null (no-breach) distribution of the alarm score shifts by state.

### Methods (fixed)
- **CTRL (control):** the original proposed forecaster, unchanged — logistic
  regression on the original batch-observable feature set (per metric,
  including the ε drift budgets), Platt-calibrated
  (CalibratedClassifierCV, sigmoid, cv=3) on training-fold instances, single
  global threshold per (cell, FAR target) chosen on training trajectories by
  the original pick rule (closest train FAR to target, ties toward smaller
  FAR) — re-run at the expanded scope.
- **TRA-Q (the transport-robust forecaster; the only new method with
  headline standing):**
  - Score: the SAME fitted model as CTRL in the same fold (identical
    instance scores; only the alarm rule differs).
  - Alarm at step t of a seed-series in target state s iff p_t ≥ θ_{s,t},
    where θ_{s,t} is the weighted (1−q) quantile of a two-component pool:
    the global pool G = all training-fold instance scores of the cell
    (weight (1−λ_t)/|G| per point) and the series' OWN pool O_t = its own
    scores at steps 2014…t inclusive (weight λ_t/|O_t| per point), with
    **λ_t = |O_t| / (|O_t| + κ), κ = 3** (step-score units). Only
    batch-observable, deployment-available information is used: the own
    pool is the series' own past and current step scores — no other seed's
    batches, no population quantities, no labels.
    (Equivalently: alarm iff the mixture CDF at p_t reaches 1−q; q is
    calibrated exactly over the candidate set induced by training
    instances, no grid approximation.)
  - q calibration: per (cell, FAR target, fold), simulate the full TRA-Q
    rule on the training trajectories — each training state in turn treated
    as target, its global pool being the other training states' scores
    under the fold's score model (in-sample-score caveat: this mirrors the
    original protocol, which also calibrated thresholds on the trajectories
    its score model was fit on) — and choose q minimising |achieved train
    FAR − target|, ties toward smaller FAR. q is then frozen for the test
    state.
- **Baselines (unchanged, all calibrated on the same training trajectories
  to the same FAR targets):** last-value, linear extrapolation, CUSUM
  (slack 0.02, original h grid), FairCanary-style point and CI detection,
  climatology (calibration reference).
- **Secondary, reported without headline standing:** pure-own ablation
  (κ → 0, λ ≡ 1 after the first step), TRA-Q sensitivity κ ∈ {1, 10},
  TRA-R (alarm iff p_t ≥ CTRL's global θ AND p_t is a strict record over
  the series' own previous step scores), LOTO fold scheme for all methods,
  per-task and per-fold breakdowns of everything.

### Evaluation integrity gate (before any expanded result is trusted)
The restructured evaluation code must first reproduce, from the BASELINE
`results/monitor_steps.csv`, the baseline headline cell's pooled coverages,
median leads, and falsifier verdicts exactly (tolerance 1e-9) for CTRL
(= original proposed), last-value, extrapolation, and CUSUM. If it cannot,
the expanded runs are void until it can.

### Headline cells and the falsifier (fixed, binding)
- **Headline cell, per model class:** EO gap, τ = 0.05, H = 2, LOSO —
  the Amendment-A1 cell of the baseline, carried over unchanged; FAR
  target **0.10** is the falsifier's operating point (0.05 and 0.20 are
  reported with the same comparisons, without headline force).
- **FALSIFIER-U.** For each model class separately: if TRA-Q's pooled
  median lead time in the headline cell does not **strictly exceed BOTH**
  last-value's and linear extrapolation's pooled median lead times, the
  forecasting claim is DEAD for that model class and is reported dead.
  No re-thresholding, no cell-shopping, no re-scoping.
- **Vacuity clause.** The pooled instance set of the headline cell must
  contain breaching trajectories from all 3 tasks for a model class;
  otherwise that is reported and the "across ≥3 tasks" condition is
  recorded as failed for that class. The cell is not moved.
- **Transport criteria (binding for the transport claim).** In the
  headline cell at FAR target 0.10, per model class, TRA-Q vs CTRL:
  (i) the max−min spread of per-fold achieved FAR is strictly smaller,
  AND (ii) |fold-mean achieved FAR − 0.10| is strictly smaller. Both must
  hold to claim transport improvement; both quantities are reported
  regardless, for every cell.
- **All-cells reporting:** every (metric × τ × H × scheme × model class)
  cell is reported for every method — including all DP cells (the baseline's
  proposed forecaster was silent there; whether TRA-Q is too is a result,
  not an embarrassment to be omitted) and every fold's achieved FAR.

---

## WS3 — Theorem attempt: choice and statements

### Prior-art check (concept level, executed 2026-10-29 before this choice)
Searches run: (1) false-alarm-rate transport across sites under distribution
shift in fairness monitoring; (2) prediction-model calibration
transportability across hospitals/sites. Findings: cross-site performance
and calibration degradation is extensively documented **empirically** in
clinical prediction (cross-site readmission/AKI/stroke studies; local
recalibration is the standard remedy); drift-detector false-alarm behaviour
is studied empirically (e.g. batch-size dependence of detector FAR); the
classical domain-adaptation bounds (Ben-David et al.) bound target *error*
by source error plus a divergence plus a shared-hypothesis term. No work was
found stating a tight bound/impossibility for a monitoring alarm's
**false-alarm rate transport across sites** in terms of the null score
distribution, and none in the fairness-monitoring setting. This is a
concept-level check, not an exhaustive review; the fresh tester judges
anticipation independently.

### Why (b) and not (a) (recorded analysis)
Option (a) — a finite-sample certificate certifying POSITIVE safe horizons
at n ≈ 2,000 — is expected to collapse as specified, for a quantifiable
reason: the operational budget is a sum of plug-in histogram-TV estimates
(50 bins; 2 cells for DP, 4 for EO). The plug-in TV estimator's upward bias
alone is of order √(K/n_cell) per cell; at batch n = 2,000 the per-cell
n is a few hundred, so the bias term summed over cells is of order
0.2–0.5 per step — an order of magnitude above the τ = 0.05 scale — before
any concentration term is added. Positive horizons at n ≈ 2,000 would
require assumptions (e.g. a parametric score family) strong enough to
defeat the certificate's model-free purpose. (a) is therefore not
attempted; this analysis itself is reported in the theorem note.
Option (b) is attainable, can be made tight, and speaks directly to the
paper's headline empirical finding.

### Statements attempted (fixed)
Setup: a step-level alarm score S ∈ [0,1] computed from batch-observable
history by any forecaster. A threshold rule is **state-blind** if the score
map and threshold θ are functions of training-state data only. For state s,
P_s^0 is the distribution of S over no-breach-within-H steps (the null);
FAR_s(θ) = P_s^0(S ≥ θ).
- **T1 (transport bound).** For any states s, s′ and any state-blind
  threshold rule: |FAR_s(θ) − FAR_{s′}(θ)| ≤ TV(P_s^0, P_{s′}^0).
  *Posture:* this is the definitional TV bound applied to the alarm event;
  **classical, no novelty claimed for the inequality itself.**
- **T2 (tightness).** For every δ ∈ [0,1] and α ∈ [0, 1−δ] there exist
  distributions P, Q on [0,1] with TV(P,Q) = δ and a threshold θ with
  P(S ≥ θ) = α and Q(S ≥ θ) = α + δ. (Constructive proof.)
- **T3 (state-blind impossibility, corollary).** If a target state's null
  may be any distribution within TV distance D of the pooled training null,
  then no state-blind threshold rule calibrated to FAR α on the training
  states can guarantee target-state FAR below min(1, α + D); by T2 the
  bound is best possible. Rules using the target state's own batch data
  (e.g. TRA-Q) are outside the corollary's scope: T3 prices
  state-blindness, not adaptivity.
- **T4 (empirical accounting protocol).** Per headline cell and model
  class, for each LOSO fold of CTRL: TV between the test state's null
  step-score distribution and the pooled training null step-score
  distribution (50-bin histograms on [0,1], the paper's TV convention;
  20-bin sensitivity), against the achieved |FAR_fold − FAR_train@θ|.
  Report: the empirical check of T1 across folds; the distribution
  (median, max) of fold TV; and the fold(s) closest to the bound.
  **Accounting success criterion (fixed):** the theorem is said to
  *account for* the observed transport failure iff median fold TV ≥ 0.05
  AND T1's inequality holds on ≥ 99% of folds up to a histogram-estimation
  slack of 0.02. If fold TVs are small while FAR spreads are large, the
  conclusion is the opposite — the null-score TV does NOT explain the
  failure — and that is reported instead.
- **Novelty posture (binding on all write-ups):** the claimed delta, to be
  judged by the fresh tester, is only: the scoping of the bound to
  fairness-monitor FAR transport, the tightness/impossibility form, and
  the at-scale empirical accounting. If the tester judges this a
  restatement, the report says so.

---

## What counts as a lifter landing (fixed)

- **Lifter (ii) — validated forecasting result:** credited for a model
  class iff FALSIFIER-U passes for that class. A manuscript claim may be
  scoped only to class(es) where it passes, with the failing class
  reported alongside.
- **Lifter (i)-upgrade — theorem:** credited iff T1–T3 are proved
  correctly (proofs written out in full in the theorem note, checkable
  line by line) AND T4's accounting meets its fixed success criterion.
- **WS1** is the foundation for both and is reported in full regardless of
  either lifter's fate.
- **Manuscript rule:** an upgraded manuscript
  (`files/Paper_11_..._upgraded.tex/.pdf`, NEW files alongside the
  reframed ones, which are never overwritten) is produced **only if at
  least one lifter lands**, and its claims are stated exactly as the
  evidence supports (including any model-class scoping and any falsified
  component, reported dead as the baseline paper reports H1).
- **No submission anywhere.** The fresh tester certifies after this loop;
  the site owner verifies any final paper first.

## Compute/reproducibility notes (fixed)
- All upgrade code in `upgrade/src/`; deterministic seeds via the original
  `stable_seed` (model-class tag appended for the new scope); long stages
  resumable (existing per-cell files are skipped, as in the original
  build); logs saved beside artifacts.
- `validate.py` gains NEW stages for the upgrade tree (equivalence gate,
  expanded artifact completeness, population recompute sample, certificate
  exactness at expanded scope, falsifier-U recompute from saved lead-time
  distributions, transport-criteria recompute). Original stages 1–6 are
  not modified.


---

## Amendment U1 (2026-10-29, recorded BEFORE any expanded-scope run; found by the equivalence gate)

**Discovery.** The restructured evaluator initially failed the equivalence
gate on exactly the two series baselines (CUSUM, linear extrapolation) and
nothing else. Cause, verified by re-reading `src/forecast.py`: in the
original code the per-fold calibration loop calls
`store.update(series_alarms(best_parameter))` where `series_alarms` covers
**all** trajectories — so each successive fold overwrites every
trajectory's alarms with its own calibrated parameter, and the shipped
baseline lead-time distributions for CUSUM/extrapolation were computed
with the **last fold's parameter applied to all trajectories** (LOSO:
the PA fold's parameter, chosen on the other five states' training
instances; LOTO: the last task fold's). The probability methods (proposed,
last-value) and detection baselines are unaffected — they store per-test-
instance alarms or are parameter-free — and they reproduce exactly.

**Gate redefinition (the minimal change that keeps the gate's purpose —
proving the restructure faithful — without enshrining a defect):**
equivalence is now checked in two runs. (1) With the legacy semantics
replicated behind a `--legacy-series-leak` switch, the new evaluator must
reproduce the baseline artifacts EXACTLY for all shared methods (this is
the faithfulness proof). (2) Production runs (expanded scope, and a
corrected baseline-scope run kept for the record) use the **documented**
protocol: each fold's calibrated parameter applies to that fold's test
trajectories only. The baseline-scope corrected CUSUM/extrapolation
numbers, and whether the baseline-scope H1 verdict changes under corrected
calibration, are reported in the upgrade report as a baseline-integrity
finding. FALSIFIER-U's comparisons at expanded scope use the corrected
semantics for every method, TRA-Q included (TRA-Q's rule is fold-local by
construction). Nothing else in this pre-registration changes.


## Amendment U2 (2026-10-29, recorded BEFORE any expanded-scope run; second equivalence-gate finding)

The gate also exposed how the original fold loop interacts with its
single-class guard (`train.y.nunique() < 2 → fold skipped`): in cells
whose positive instances concentrate in one state (e.g. DP, τ = 0.05 —
positives only in WA trajectories), the held-out fold is skipped for
every calibrated method, yet the original's detection baselines still
scored that fold because their (fold-independent) alarm series was
written globally inside other folds' iterations. Corrected semantics,
fixed here: (i) the parameter-free detection baselines (FairCanary
point/CI) are written once, globally, in all runs — identical values
under legacy and corrected semantics; (ii) calibrated methods (CTRL,
last-value, CUSUM, extrapolation, TRA-Q family) produce no alarms for a
fold whose training pool is single-class, and such folds are reported
as skipped wherever they occur. At the expanded scope (51 states) this
is expected to be a non-issue except in degenerate cells; occurrences
are counted in the upgrade artifacts.


## Amendment U3 (2026-10-29, recorded BEFORE any expanded-scope run; refines U2 clause (ii))

U2's lumped treatment — no calibrated method alarms a fold whose training
pool is single-class — is methodologically wrong for the methods whose
calibration never needed both classes: last-value, CUSUM and extrapolation
calibrate purely on NEGATIVE training instances (their thresholds are set
by train FAR), so a positives-free training pool leaves them perfectly
well defined; only the logistic-regression-fit methods (CTRL, and TRA-Q
whose score is CTRL's) genuinely cannot be fit there. Keeping U2 as
written would have zeroed the strongest baseline (CUSUM) on exactly the
DP cells where it was strongest, biasing FALSIFIER-U in TRA-Q's favour —
a distortion in the new method's favour is as disqualifying as one
against it. **Corrected semantics, final:** the single-class guard applies
per method family — LR-fit methods are skipped when the training pool is
single-class; analytic/series methods are calibrated whenever the
training pool contains at least one negative instance (for last-value in
such a fold, the candidate threshold set is built from its own training
probabilities alone, the shared candidate set being undefined without
the LR model — a case the original protocol never reached because its
lumped guard skipped the fold entirely). Legacy mode (equivalence gate
only) retains the original lumped guard exactly. U2 clause (i)
(detection baselines written globally) is unchanged.

---

## Amendment WS1-A (2026-10-29, appended BEFORE the affected training run)

**GB training-row cap for ACSPublicCoverage only: 76,655 rows (in place of
300,000).** Reason: pure memory constraint of the 7 GB build box — the case
the pre-registration's compute notes pre-authorize. The union category spec
for ACSPublicCoverage is 4,892 columns wide (PINCP enters the task as a
one-hot feature; measured by the preliminary pass: ACSIncome 932,
ACSEmployment 109, ACSPublicCoverage 4,892). A dense float32 training
matrix at the nominal cap would be 300,000 x 4,892 x 4 B = 5.9 GB, and
even the 250,000-row fallback would be 4.9 GB — both far above the
~1.5 GB dense budget. The cap was therefore set by the same budget rule
used in the build (largest row count whose dense matrix fits ~1.5 GB):
floor(1.5e9 / (4 x 4,892)) = 76,655 rows, deterministic subsample with
rng seed 0 exactly as registered. ACSIncome (932 cols, 1.12 GB at cap)
and ACSEmployment (109 cols) are unaffected and train at the full
300,000-row cap. No other protocol element changes.
