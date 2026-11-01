# Closure Pre-Registration — Paper 11 Elevation, Closure Cycle

## Deriving the transport bound for the EO/DP gap statistics

**Commissioned:** Ranadhir Ghosh, 2026-11-01 — the closure commission,
issued after the bound-only rebuild's fresh tester named the structural
objection verbatim (`rebuild/FRESH_TESTER_AND_SCREEN.md`, Objection 1):
*"Theorem 1 bounds the false-alarm rate, while the monitored/audited
statistics are the EO and DP gaps, for which no bound is derived — not
answerable from the text; closing it needs new mathematics or narrowing
all claims to FAR."* This cycle is the new-mathematics route. If it does
not close at the registered strength, the narrowing route is what the
revised draft (Stage 3) executes, at whatever coverage the closure
actually reaches.

**Freeze discipline.** This document is frozen before any derivation
outcome is scored and before any gap-transport quantity is computed
from the saved artifacts. Its SHA-256 and the freeze timestamp are
recorded in `ELEVATION_LOG.md` in the entry that accompanies this
freeze. Any later change is appended as a dated amendment with its
reason, under the paper's amendment discipline. No silent
re-registration.

---

## 1. The three objects in the record (fixed inputs; the mismatch stated exactly)

The rebuild's screen failure is, at root, an object mismatch among
three distinct quantities. All three are fixed here, from their
sources, so the closure's target is unambiguous.

- **T1 as audited (the theorem the accounting actually tests).**
  `upgrade_preregistration.md` WS3: a step-level alarm score S ∈ [0,1]
  computed by any forecaster; P_s^0 = the distribution of S over
  no-breach-within-H steps (the null) in state s;
  FAR_s(θ) = P_s^0(S ≥ θ); **T1:** |FAR_s(θ) − FAR_{s′}(θ)| ≤
  TV(P_s^0, P_{s′}^0) for any state-blind threshold rule. **T4
  (accounting protocol):** per headline cell and class, per LOSO fold
  of the CTRL forecaster, the fold's null step-score TV (50-bin
  histograms on [0,1]) against the achieved |FAR_fold − FAR_train@θ|;
  criterion: median fold TV ≥ 0.05 AND T1's inequality holds on
  ≥ 99% of folds up to a slack of 0.02. Ported verbatim by E2 §1/§8
  and E4.
- **The monitored statistics (the closure's target objects).**
  The pipelines' definitions, `src/common.py` and ported verbatim in
  `elevation/src/common2.py`: with alarm = 1{score ≥ 0.5} at the
  family-1 decision cut,
  **dp_gap** = |Pr[Ŷ=1 | A=1] − Pr[Ŷ=1 | A=0]|;
  **eo_gap** = max( |TPR₁ − TPR₀|, |FPR₁ − FPR₀| ), where
  TPR_a = Pr[Ŷ=1 | Y=1, A=a], FPR_a = Pr[Ŷ=1 | Y=0, A=a], with the
  code's NaN convention (a rate with an empty stratum is NaN; the max
  is over the non-NaN components; both NaN ⇒ gap NaN).
  These — not the rebuild §2's TPR-only restatement — are the
  statistics the E2/E4 monitors, labels, and population tables use.
- **Theorem 1 as printed in the rebuild.** `rebuild/Paper_11_Rebuilt.tex`
  §3 states a label-0 *covariate* form: |FAR_s(θ) − FAR_{s′}(θ)| ≤
  TV(P_s^0, P_{s′}^0) with FAR = Pr[s(X) > θ | Y=0] and P^0 the
  label-0 covariate law. This matches neither the audited T1 (null
  step-score laws) nor the monitored statistics (EO/DP gaps), and
  rebuild §4's accounting definition speaks of "realised gap
  differences" where the pipelines in fact compute FAR differences.
  Stage 3's revised draft must repair this three-way conflation at
  whatever coverage the closure reaches; Stages 1–2 derive the
  missing mathematics.

**Recorded accounting verdicts (the re-adjudication list, §6).**
V1 F1 LR **met** (median TV50 0.3481, 50/50 folds);
V2 F1 GB **not met** (0.1358, 50/51);
V3 F2-2024 LR **met** (0.4784, 9/9);
V4 F2-2024 GB **met** (0.2865, 9/9);
V5 F2-2025 GB **met** (0.3475, 7/7 evaluable folds).
Sources: `upgrade_report.md` + `upgrade_tester_report.md` §5 (V1, V2);
`E2_RESULTS.md` + `results/accounting.json` + `results/fold_detail.csv`
(V3, V4); `E4_RESULTS.md` + `results4/accounting4.json` +
`results4/accounting_folds4.csv` (V5). All five are verdicts about the
**FAR functional under T1/T4**. Whether any of them is also a verdict
about the gap statistics is precisely what §6 adjudicates.

---

## 2. Setting and notation (fixed)

A **population** p is a probability law over records (S, A, Y), where
S = s(X) ∈ [0,1] is the output of one fixed deployed scoring rule
(state-blind: the same function s for every population — in family 2,
one model trained on pooled base-month data and frozen; in family 1,
one LR per task trained on pooled 2014 data and frozen), A ∈ {0,1} is
the binarised protected attribute as the pipelines code it, and
Y ∈ {0,1} the label. The decision is Ŷ = 1{S ≥ c} with **c = 0.5**
(the pipelines' `DECISION_CUT`; `alarm = (s >= DECISION_CUT)`).

For a stratum C ∈ {A=a} ∪ {(Y=y, A=a)}, write
R_p(C) = Pr_p[Ŷ=1 | C] (defined iff Pr_p(C) > 0) and
μ_p^C = Law_p(S | C), the conditional **score** law. Because Ŷ is a
function of S alone, R_p(C) = μ_p^C([c, 1]).

The monitored statistics, as population functionals:
DP_p = |R_p(A=1) − R_p(A=0)|;
EO_p = max( |R_p(Y=1,A=1) − R_p(Y=1,A=0)|,
            |R_p(Y=0,A=1) − R_p(Y=0,A=0)| ),
defined when the strata involved have positive mass (the pipelines'
NaN convention is the finite-sample shadow of this condition).

**TV convention (the paper's, fixed):** population TV is the
variational distance; its estimator is `tv_hist` — 50-bin equal-width
histograms on [0,1], TV̂ = ½·Σ|p̂ᵢ − q̂ᵢ| — exactly as T4 uses it,
with the registered slack 0.02 and criterion constants of §5.

---

## 3. The registered derivation targets

Claim tiers: **[P]** proved analytically in this cycle; **[C]**
certified by exact computation on the saved artifacts.

- **G1 — DP transport [P].** For any two populations p, q and the
  fixed state-blind rule:
  |DP_p − DP_q| ≤ **D_DP(p,q)** :=
  TV(μ_p^{A=1}, μ_q^{A=1}) + TV(μ_p^{A=0}, μ_q^{A=0}).
- **G2 — EO transport, the pipelines' max form [P].**
  |EO_p − EO_q| ≤ **D_EO(p,q)** := max(D_TPR, D_FPR), where
  D_TPR = Σ_{a∈{0,1}} TV(μ_p^{Y=1,A=a}, μ_q^{Y=1,A=a}) and
  D_FPR = Σ_a TV(μ_p^{Y=0,A=a}, μ_q^{Y=0,A=a});
  and the componentwise bounds |TPR-gap_p − TPR-gap_q| ≤ D_TPR,
  |FPR-gap_p − FPR-gap_q| ≤ D_FPR hold individually.
  *Scope condition (part of the primary statement, registered now,
  not a demotion):* all four (Y,A) strata have positive mass under
  both p and q (for G2), resp. both A strata (for G1). Populations
  failing it are the degeneracy territory already covered by E3's C3;
  the fold convention of §7 handles finite-sample emptiness.
- **G3 — Reduction to Theorem 1's objects [P].** (i) The single-stratum
  case of the stratum lemma (PO1) *is* T1's argument: T1 is the
  one-event bound applied to the null-step score law; the gap bounds
  are its composition over the strata that define the gaps — no new
  inequality is used. (ii) Prevalence decomposition: with
  π_p(a) = Pr_p[Y=1 | A=a],
  R_p(A=a) = π_p(a)·R_p(Y=1,A=a) + (1−π_p(a))·R_p(Y=0,A=a),
  yielding a bound on |DP_p − DP_q| whose terms are the component
  transports of G2 weighted by prevalences, plus prevalence-difference
  terms |π_p(a) − π_q(a)| multiplied by named rates — i.e. the gap
  quantity bounded by FAR-type (label-0) and TPR-type transports plus
  named, measurable terms, as the commission allows. (iii) Covariate
  corollary: replacing each score law μ by the corresponding covariate
  law ν weakens each TV term (data processing), giving the
  covariate-TV form — a corollary, not the primary statement.
- **G4 — Tightness of form [P].** For each stratum term, two-point
  score laws attain the term's TV with the realised stratum-rate
  difference equal to it, the other strata held fixed; hence the
  sum form (G1, components of G2) and the max form (G2) are best
  possible as functions of the stratum TVs alone (the T2/T3 posture
  of the original WS3, stratum-wise).
- **G5 — Accounting form [C].** The T4 criterion transported to gap
  objects: per fold (§7), realised_G = |Gap_test − Gap_train-pooled|
  and D̂_G = the tv_hist(50-bin) plug-in of D_G on the fold's
  conditional score samples, for G ∈ {EO, DP}; a fold **passes** iff
  realised_G ≤ D̂_G + 0.02; a cell's gap-criterion is **met** iff
  median fold D̂_G ≥ 0.05 AND pass fraction ≥ 0.99 — T4's constants,
  verbatim, applied to the gap functionals.

**What counts as the bound being derived (registered):** G1 and G2
proved at the forms above, for the pipelines' definitions of §1, at
per-fold granularity, with no assumption beyond the §3 scope
condition and state-blindness. Anything weaker is a demotion under §5
or a kill.

---

## 4. Proof obligations (fixed list)

- **PO1.** Stratum lemma: |R_p(C) − R_q(C)| ≤ TV(μ_p^C, μ_q^C) for
  every stratum C, from R_p(C) = μ_p^C([c,1]) and the variational
  definition of TV. Includes the observation that this is T1's own
  argument (G3(i)).
- **PO2.** G1: triangle inequality over the two group terms, with an
  explicit definitional match to `dp_gap` (group coding, absolute
  value, cut ≥ 0.5).
- **PO3.** G2: the max-form step |max(u,v) − max(u′,v′)| ≤
  max(|u−u′|, |v−v′|); the component bounds via PO1 + triangle
  inequality; explicit definitional match to `eo_gap` (max of
  TPR/FPR differences, NaN convention ↔ the scope condition).
- **PO4.** G3(ii): the prevalence identity and the resulting bound,
  every term named and measurable from the same artifacts; G3(iii):
  data-processing step for the covariate corollary.
- **PO5.** G4: the two-point attainability constructions, per
  stratum, including the max-form attainability (one component
  attains while the other is held equal).
- **PO6.** G5's estimation honesty: binned TV ≤ population TV
  (binning is a channel; data processing), so D̂_G estimates D_G
  from below up to sampling fluctuation; the 0.02 slack's role is
  stated exactly as T4 states it — a registered design constant
  absorbing histogram-estimation error, **not** a derived
  concentration bound. No stronger claim about the slack may be made.
- **PO7.** Fold computation: the Stage-2 recompute implements §7's
  fold definitions exactly; the independent checker (§8 of the
  commission pattern) recomputes every fold quantity from the raw
  per-record score files by separately written code and grades
  PO1–PO6 from a separate read of the proof text.

---

## 5. Demotion list (exhaustive) and the one-cycle kill criterion (binding)

**Demotions** (each, if taken, is reported with the scoped claim text
it leaves standing):
- **DM1 — one statistic only:** G1 or G2 closes and the other does
  not; coverage is claimed for the closed statistic only.
- **DM2 — covariate form only:** the score-law form fails and only
  the G3(iii) covariate-TV corollary survives (weaker constants).
- **DM3 — coarser granularity:** the bound/criterion is evaluated
  programme-pooled rather than per-fold.
- **DM4 — stronger assumption:** a further assumption beyond §3's
  scope condition and state-blindness is required; the assumption is
  NAMED in the theorem statement and the claim is scoped to it.

**Kill criterion.** If G1+G2 cannot both be proved for the
pipelines' definitions at per-fold granularity, and the surviving
form falls outside DM1–DM4 — in particular, if the bound is provable
only for a *different* gap definition than the pipelines' (e.g. a
TPR-only "EO"), or the max form resists the bound — the closure is
**KILLED at registered strength**: `CLOSURE_RESULTS.md` reports the
failed obligation and the exact point of failure; Stage 3's draft
then narrows its claims to FAR-only at the points the closure did
not reach. **No second closure cycle exists** without Ranadhir's new
decision.

**Re-adjudication is not under the kill criterion.** A recorded
verdict standing outside the gap bound (§6) is a reportable outcome
of the cycle, not a failure of the derivation; each such verdict
keeps its original FAR-accounting meaning and loses nothing it ever
had — what it never had is a gap-statistic meaning, and §6 says
which ones those are.

---

## 6. The re-adjudication list (fixed in advance) and its decision rule

**Decision rule.** A recorded verdict **FOLLOWS under the gap bound**
iff (a) per-record (score, y, A) artifacts for that cell's **own fold
partition** survive in the workspace, and (b) the §5/G5 gap-form
criterion, computed on those folds for EO and for DP separately,
reproduces the recorded met/not-met outcome for **both** statistics.
If exactly one statistic reproduces it, the verdict **FOLLOWS FOR
EO ONLY / DP ONLY** (partial; reported as such). Otherwise the
verdict **STANDS OUTSIDE** the gap bound, with the reason recorded
(artifact absence under (a), or non-reproduction under (b) with the
recomputed numbers). A "not met" verdict follows iff the gap-form
criterion is likewise not met (for both statistics, with the partial
rule applied symmetrically).

| # | Recorded verdict | Fold partition | Artifacts expected |
|---|---|---|---|
| V1 | F1 LR **met** (TV50 0.3481, 50/50) | upgrade LOSO, 51 jurisdictions | upgrade tree **absent** (E2 log; E3 prereg §7) |
| V2 | F1 GB **not met** (0.1358, 50/51) | upgrade LOSO, 51 jurisdictions | absent, as V1 |
| V3 | F2-2024 LR **met** (0.4784, 9/9) | E2 LOSO, 9 forces | `data/scores/*.parquet` (y, A, score_lr, score_gb) |
| V4 | F2-2024 GB **met** (0.2865, 9/9) | E2 LOSO, 9 forces | same |
| V5 | F2-2025 GB **met** (0.3475, 7/7) | E4 LOSO, 8-force set, 7 evaluable folds | `data/scores25/*.parquet` |

**Registered expectation (not an outcome):** V1 and V2 are expected
to stand outside under rule (a) — their folds' per-record artifacts
did not survive the archive migration, and no computation on other
folds may re-adjudicate them. The expectation is recorded so that
the outcome, whichever way the (a) check lands, is read against a
prior statement.

**C-F1 — family-1 corollary recompute [C] (non-adjudicative).**
The gap-form criterion computed on the E4 family-1 secondary arm's
own fold partition (LOSO over CA/FL/NY/PA/TX/WA; population per
state = pooled records over 3 tasks × 2014–2019 from
`results/scores/*.npz`, whose score is the original deployed LR's —
`DESIGN.md`: "a single frozen classifier per task (logistic
regression…)"; train pool = the other five states pooled likewise).
C-F1 tests the gap criterion where family-1 artifacts exist; it
re-adjudicates **nothing** about V1/V2 (different folds, different
scope) and is labelled accordingly wherever reported.

---

## 7. Fold definitions for the gap recompute (fixed)

- **F2-2024 folds.** Analysis set = E2's 9 forces. Fold f: **test**
  = all usable records of force f pooled over months 2024-01…12
  (from `data/scores/<force>_<month>.parquet`); **train** = all
  usable records of the other 8 forces pooled likewise. Classes:
  `score_lr`, `score_gb` columns of the same files (V3, V4 share the
  partition). Statistics: EO and DP by `common2.eo_gap` /
  `common2.dp_gap` applied verbatim to the pooled records at
  alarm = 1{score ≥ 0.5}; D̂_EO, D̂_DP by tv_hist (50 bins) on the
  §3 conditional score samples of test vs train.
- **F2-2025 folds.** Analysis set = E4's 8 forces; folds = the 7
  evaluable GB accounting folds of `results4/accounting_folds4.csv`
  (V5's scope). Fold f: test = f's usable records pooled over
  2025-01…12 (`data/scores25/`), train = the other 7 analysis-set
  forces pooled. Class: `score_gb`. The 2025 LR gap quantities are
  computed **descriptively only** (no recorded LR accounting verdict
  exists for 2025; the LR statistic degenerates there — E4) and are
  labelled non-adjudicative wherever reported.
- **C-F1 folds.** As §6: LOSO over the 6 states; per state, pooled
  records over the 18 (task, year) cells from `results/scores/*.npz`
  (keys scores/y/a); class = the original deployed LR (the files'
  single score); train = other 5 states pooled.
- **Stratum convention.** A stratum sample is the score column of
  the records in the named cell of the pooled fold population. If a
  stratum is empty in either population, that component's D̂ is
  undefined and the fold is **non-evaluable for that statistic**
  (count disclosed in the results; pass fractions are over evaluable
  folds, mirroring E4's "7 of 8 folds evaluable" precedent). Gaps
  themselves are computed by the pipelines' functions verbatim,
  NaN conventions included.
- **Determinism.** Every quantity is a full-population functional of
  saved files; there is no sampling and no seed anywhere in this
  cycle's computations.

---

## 8. What this cycle does not do

No new data; no re-run of any E2/E4 pipeline stage (fold quantities
are computed from the saved per-record score files only); no edit to
the submitted AI & Society files or to `rebuild/Paper_11_Rebuilt.tex`
(Stage 3 writes a new draft); no submission; no journal contact;
$0 spend. Stage 3 (registered in outline by the commission): the
revised rebuild with claims matched to the closure's actual
coverage; the DMKD handling-editor memo from the journal's last 12
months of published contents; a fresh tester and a fresh prospective
editor screen at DMKD; a desk-reject risk page; and a gate
re-verdict appended to `ELEVATION_LOG.md`.
