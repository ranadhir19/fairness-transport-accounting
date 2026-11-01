# E4 Pre-registration — Paper 11 Elevation, Cycle E4

## A scale-adapted test of the forecasting half

**Status:** FROZEN at the timestamp and SHA-256 recorded in `ELEVATION_LOG.md`.
Written **before any contact with the confirmatory corpus** (family-2 year
2023): no 2023 record has been fetched, counted, scored, or inspected in any
form at freeze time. Amendments, if any, are appended at the end of this
file, dated, with reasons, **before** the run they affect (the paper's
U1–U3 / A-E2 discipline). The two pre-authorised dated recordings — the
primary-class determination (§5) and the τ\* values (§4) — follow the
Amendment-A1 / A-E2-2 precedent: mechanical applications of rules frozen
here, recorded before the runs they affect.

**Commission.** Ranadhir Ghosh, 2026-11-01, after E2's split verdict: *"New
pre-registered cycle: scale-adapted design to test the forecasting half."*
Governing question: **does any forecasting claim survive when the breach
threshold τ is defined relative to the family's gap scale instead of
absolutely — i.e., was TRA-Q's death a property of forecasting, or of the
absolute-τ design?**

**What E2 established (starting facts, all validator-confirmed;
`E2_RESULTS.md`).** The calibration-transport bound's accounting travels:
on family 2 (UK Police stop-and-search 2024, 9 forces, 71,347 records)
the ported T4 criterion was MET on both classes (LR median fold TV50
0.4784, 9/9 folds within slack; GB 0.2865, 9/9). E2's conjunctive bar
failed only on prong 1, vacuity (failure mode F3): at the registered
absolute τ grid, breach crossings on the frozen LR headline scope were
2/1/0/0 at τ = 0.05/0.10/0.15/0.20 against ≥ 3 required — the breach
phenomenon is scale-bounded at absolute thresholds on that family. On the
secondary GB scope at τ = 0.05 there were 6 crossings. E3 (theory) never
started. Upstream, the forecasting claim this cycle re-tests was falsified
twice on family 1 under absolute τ: the original falsifier (DESIGN.md §2,
as amended by A1: headline EO, τ = 0.05, H = 2 — the proposed forecaster
did not beat both trivial forecasters) and FALSIFIER-U at expanded scope
(`upgrade_tester_report.md` §2: TRA-Q pooled median lead 3.0 vs last-value
3.0 and extrapolation 3.0 on LR; 3.0 vs 2.0 and 4.0 on GB; fails at all
three FAR targets in both classes).

---

## 1. Design overview

Two arms, one gating:

- **Confirmatory arm (gates E4).** Family 2, calendar **2023** — the year
  E2 did not touch (E2 used 2024 for acquisition, inclusion, deployed
  models, population audit, and accounting). The full E2 apparatus is
  re-run on 2023 under the scale-adapted design of §4–§6: same 13
  candidate forces (inherited verbatim from E2 §3), same §5 inclusion
  rule applied mechanically to 2023, deployed models trained on pooled
  base month (2023-01) exactly as E2 §6, monitor/batch protocol identical
  (batch 200, 25 seeds), then the forecasting suite (§6), the ported T4
  accounting (§7), and the conjunctive bar (§8).
- **Secondary arm (reported, never gates).** Family 1 (ACS, original
  18-trajectory scope — the surviving baseline artifacts; the expanded
  `upgrade/` tree is absent from this workspace) re-tested under the same
  adapted-τ rule (§9), LR only (the original scope's only class), with
  the corrected evaluator semantics of Amendments U1–U3.

## 2. The scale-adaptation rule (frozen)

**Rule.** For each model class c ∈ {LR, GB} and each metric m ∈ {EO, DP}:

> **τ\*(c, m) = Q₀.₇₀ of the pooled population gaps of class c on metric
> m** — the 0.70 quantile (numpy `quantile`, linear interpolation) of the
> multiset {pop_gap(c, m, force, month) : force ∈ analysis set, month ∈
> all 12 months of the confirmatory year, base month included}.

One threshold per (class, metric). The headline cell is (EO, τ\*(primary,
EO), H = 2). DP cells use τ\*(c, DP) and are descriptive only. The rule,
the constant 0.70, and the τ-selection procedure (population audit →
dated amendment recording the four τ\* values → monitor/forecast runs)
are frozen here; §4's amendment records the computed values before any
forecaster or accounting computation, exactly as in E2 §7.

**Justification from the estimand.** The claim under test (H1, DESIGN.md
§1) is about *forecasting skill*: positive lead time at matched
false-alarm rate for threshold crossings of a monitored gap process.
Three properties of that estimand fix the design:

1. **Lead time and FAR are properties of the crossing process, not of
   the level.** Both are defined relative to when the gap crosses τ and
   how often alarms fire on non-crossing steps. Rescaling the gap axis
   by any strictly increasing transformation (difference vs ratio vs
   logit reporting of the same underlying rates) leaves the monitoring
   problem — the ordering dynamics of the gap process — unchanged, but
   moves every absolute τ. A design whose headline cell is defined by
   an absolute level therefore tests the *units* jointly with the
   forecasting. A quantile-defined threshold is invariant under exactly
   those re-expressions: it is the scale-free form of the same design.
2. **"Breach" is an extreme-excursion event class.** The threshold's
   role in the estimand is to separate the gap process's ordinary range
   from its upper tail. Fixing the threshold's *distributional position*
   (the same upper-tail position in each family's own gap distribution)
   holds the event class fixed across families while the level adapts —
   which is the commensurability a cross-family forecasting test needs.
   Fixing the level instead conflates "the family generates smaller
   gaps" with "crossings cannot be forecast", which is precisely the
   ambiguity E2's F3 left behind.
3. **The constant 0.70 is anchored to the original design, not to any
   outcome of E2.** In family 1's original population audit (DESIGN.md
   Amendment A1, 2026-10-28 — before E2 existed, before TRA-Q), the
   operative headline threshold τ = 0.05 sits at the **69.4th percentile
   of family 1's pooled population EO gap distribution** (108
   (task, state, year) cells; share of cells ≥ 0.05 is 0.306; recomputed
   from `results/population_metrics.csv` at this freeze). A1's audit is
   also where the event structure the design intends was fixed: several
   trajectories crossing strictly after the base period, a majority
   below threshold at base. The adapted design places its threshold at
   that same distributional position — the 0.70 quantile (0.694 rounded
   to the clean constant; any value in [0.65, 0.75] states the same
   anchor) — in each new family's own distribution. §3 states exactly
   what E2 did and did not contribute to this choice.

**Alternative considered and rejected (recorded).** A dispersion rule
(τ = median + k·MAD, or a multiple of the gap SD) is equivariant only
under affine re-expression, centres the threshold on a location
statistic with no monitoring meaning (gap distributions are bounded
below at 0 and right-skewed, so the centre is not an operating point),
and its constant k carries no event-frequency interpretation. The
quantile rule is the one whose constant *means* something in the
estimand: the exceedance position of the breach event.

## 3. Design provenance and seen-data hygiene (binding disclosure)

E2's family-2 (2024) results are known to the designer. This section
states exactly which E4 design choices they did or did not influence.
Anything not listed as influenced was fixed from family 1's frozen
record (DESIGN.md, Amendments A1/U1–U3, `upgrade_preregistration.md`)
or from the estimand argument of §2.

**Influenced by E2 (disclosed):**
- *The cycle's existence and target.* Ranadhir commissioned a
  scale-adapted test of the forecasting half in response to E2's F3
  verdict. That is this cycle's stated premise, not a hidden input.
- *The dual-class primary rule (§5).* E2 froze LR as the headline scope
  and GB — which would have met the τ rule's crossing condition —
  became a counterfactual. §5 repairs that ambiguity structurally. The
  repair is motivated by the *existence* of the ambiguity in E2's
  record; the rule's content (base-period holdout discrimination) uses
  no 2024 gap, crossing, or accounting quantity.
- *The choice of 2023 as the confirmatory year* — dictated by hygiene
  (it is the adjacent year E2 did not use), per the commissioning brief.

**Not influenced by E2 (fixed independently):**
- The quantile form (§2) — justified by re-expression invariance of the
  estimand. No 2024 gap magnitude entered it.
- The constant 0.70 — anchored to family 1's original population audit
  (§2, point 3). **Specifically not** chosen because GB recorded 6
  crossings at the absolute τ = 0.05 in 2024, nor from LR's 2024 gap
  distribution (whose maximum cell, 0.100, is the kind of absolute-scale
  fact the adapted design exists to stop depending on).
- The CUSUM scale port (§6) — derived from family 1's constants
  (slack 0.02 at τ = 0.05; the h grid), expressed in threshold units.
- The advantage criterion's form (§6) — FALSIFIER-U's pooled-median
  comparison (family 1, 2026-10-29) plus the uncertainty/coverage
  strengthening the commission requires; its constants (FAR 0.10
  operating point, H = 2) are the upgrade's frozen headline constants.
- The accounting criterion (§7) — family 1's T4 criterion, verbatim,
  as ported by E2.

**Confirmatory-validity rule.** Every confirmatory number in
`E4_RESULTS.md` comes from the 2023 arm (primary) or the family-1
re-test (secondary, labelled). No 2024 quantity is an input to any E4
computation: the 2023 deployed models are trained on 2023-01, the 2023
analysis set is produced by E2's inclusion rule applied to 2023 data,
and τ\* is computed from the 2023 population audit by §2's formula. If
any part of this design is later found to rest on a 2024 outcome, the
affected claim is demoted to exploratory in the results — this sentence
is the standing instruction for that case.

## 4. τ\* computation and recording (pre-authorised amendment)

After the 2023 population audit (stage: train/score, E2's stage-3
port) and **before** the monitor, forecaster, or accounting stages run,
the four values τ\*(LR, EO), τ\*(GB, EO), τ\*(LR, DP), τ\*(GB, DP) are
computed by §2's formula from `population_metrics23.csv` and recorded
in a dated amendment appended to this file, together with the §8
prong-1 quantities' inputs (per-force base-month gaps and first-crossing
months at τ\*(primary, EO)) — population quantities only, the A1/A-E2-2
precedent. The monitor's labels are then built at these τ\* values
(class-specific, as E2's monitor built class-specific labels).

## 5. Headline scope and the primary-class rule (frozen)

Both model classes are deployed, monitored, forecast, and accounted in
full, and both are reported in full. The **gating scope** is one class,
fixed by this a priori rule, computed on the **base period only**:

> **Primary class = the class with the higher holdout AUC** on the
> pooled base-month (2023-01) 70/30 split (rng seed 0) produced by the
> deployed-model stage — the same split that trains the deployed
> models. If |AUC_LR − AUC_GB| ≤ 0.005, the primary class is **LR**
> (family 1's class; the tie-break is symmetric and frozen here).

Rationale, from the design: the headline monitoring question attaches
to the model one would actually deploy, and base-period holdout
discrimination is the deployment-relevant, outcome-blind selector —
it is computed from base-month labels and scores only, before any gap,
crossing, or forecast quantity exists. The determination is recorded in
the §4 amendment (the AUCs are stage-3 outputs). The secondary class's
§8 prong quantities are computed and reported identically but labelled
secondary; they cannot rescue or sink the E4 verdict. The E2 pattern —
a frozen primary whose counterfactual alternative "would have
qualified" — cannot recur: whichever class the rule selects, the
selection predates every quantity the bar adjudicates.

## 6. The forecasting test (frozen)

**Cell and operating point (gating):** metric EO, τ = τ\*(primary, EO),
H = 2 months, LOSO folds over the 2023 analysis set, FAR target **0.10**.
Also computed and reported, without gating force: FAR targets
{0.05, 0.20}; H = 1; the DP cell at τ\*(primary, DP), H = 2, FAR 0.10;
the secondary class throughout; the q-sensitivity of §10.

**Instances and labels** (E2 §6 port, at τ\*): breach month per
(force, metric) = first month of 2023 whose *population* gap ≥ τ (that
class's τ\* for the metric). An instance at step t (month index) has
label_H = 1 iff pop_gap(t) < τ, t + H ≤ Dec index, and the breach month
lies in (t, t+H]; label_H = 0 iff pop_gap(t) < τ, t + H ≤ Dec index,
and no breach month lies in (t, t+H]; otherwise undefined (excluded).
Instances are monitor rows at any month — base month included — whose
label is defined (Amendment A-E2-1's clarification, carried over).

**Monitor** (E2's `monitor2` port, unchanged definitions): per (class,
force, seed), batches of 200 usable records drawn without replacement
(`np.random.default_rng(stable_seed("e4", class, force, month, seed))`;
whole population if usable n < 200), 25 seeds; family-1 batch features
verbatim (m_eo, m_dp, se_eo, se_dp, score_gap, share_a1, prev_diff,
eps_dp, eps_eo, lags/diffs/slopes, d_share_a1, d_prev_diff).

**Methods** (all calibrated on the same training folds to the same FAR
targets; corrected semantics per Amendments U1–U3 — each fold's
calibrated parameter applies to that fold's test forces only; the
parameter-free detection baselines are computed once, globally;
single-class guard per method family: LR-fit methods are skipped in a
fold whose training pool is single-class, analytic/series methods are
calibrated whenever the training pool has ≥ 1 negative instance):

1. **CTRL** (control forecaster; family 1's "proposed"): per (metric,
   τ, H) cell and LOSO fold, CalibratedClassifierCV(StandardScaler +
   LogisticRegression(C=1.0, max_iter=2000), sigmoid, cv=3) on the
   family-1 FEATS feature set (NaN → 0); single global threshold per
   (cell, FAR target) from the 99 unique quantiles of pooled
   [p_train, plv_train], pick rule = closest train step-FAR to target,
   ties toward smaller FAR.
2. **TRA-Q** (the claimant; `upgrade_preregistration.md` WS2 verbatim):
   the same fitted model as CTRL in the same fold — identical instance
   scores p; the alarm rule differs. For a series (force, seed) in
   target force s, at step t: alarm iff u_t ≥ 1 − q, where
   u_t = (1 − λ_t)·F̂_G(p_t) + λ_t·F̂_{O_t}(p_t); F̂_G is the empirical
   CDF of the global pool G = all training-fold instance scores of the
   cell; O_t is the series' own instance scores at steps ≤ t (all
   monitor rows of the series up to and including t, base month
   included, whether or not their labels are defined); λ_t =
   |O_t| / (|O_t| + κ), **κ = 3**. q is calibrated per (cell, FAR
   target, fold) by simulating the rule on the training forces — each
   training force in turn as pseudo-target, its global pool being the
   other training forces' instance scores under the fold's score
   model — over the candidate set induced by the training instances'
   u values (no grid approximation), choosing the candidate whose
   achieved train step-FAR is closest to the target, ties toward
   smaller FAR; q is then frozen for the test force.
3. **Last-value** (trivial): score 1 − Φ(z)^H, z = (τ − m_t)/σ, σ = SD
   of the training forces' population step-to-step gap changes,
   floored at 1e-3; thresholds as CTRL (shared candidate set).
4. **Linear extrapolation** (trivial): OLS slope over the last ≤ 3
   batch metrics (the monitor's slope feature construction); alarm
   iff slope > 0 and (τ − m_t)/slope ≤ H + δ; δ calibrated per fold
   over the family-1 grid δ ∈ {−1.0, −0.5, 0, 0.5, 1.0, 1.5, 2.0}
   (step units) by the pick rule on train step-FAR.
5. **CUSUM** (sequential detector): one-sided CUSUM on the batch
   metric series, S_t = max(0, S_{t−1} + (m_t − k)), alarm iff
   S_t ≥ h. **Scale port (frozen):** family 1's constants were slack
   0.02 at τ = 0.05 (slack = 0.4τ) and h ∈ {0.005, 0.01, 0.02, 0.03,
   0.05, 0.08, 0.12, 0.2, 0.3, 0.5} (h/τ = {0.1, 0.2, 0.4, 0.6, 1.0,
   1.6, 2.4, 4.0, 6.0, 10.0}). At adapted scale: **k = τ − 0.4τ =
   0.6τ**, **h ∈ τ × {0.1, 0.2, 0.4, 0.6, 1.0, 1.6, 2.4, 4.0, 6.0,
   10.0}**, h calibrated per fold by the pick rule on train step-FAR.
   Detector parameters are scale quantities in the original design;
   the port preserves the family-1 operating geometry in threshold
   units.
6. **FairCanary-style detection** (reference): point — alarm iff
   m_t ≥ τ; CI — alarm iff m_t − 1.96·se_t ≥ τ. No calibration
   (parameter-free); lead ≤ 0 relative to the population breach by the
   design's construction (DESIGN.md §3). Reported in every table;
   not a gating comparator.
7. **Climatology** (calibration reference only): constant score =
   training-fold label base rate; Brier reported beside CTRL's in the
   headline cell. No lead times (DESIGN.md §3).

**Lead time** (family-1 semantics, month units): for a (force, seed)
whose force's population breach month b is strictly after the base
month, over the force's issue steps (steps with defined labels, ≤ b):
lead = b − (first alarmed issue step), in months; no alarm at or
before b = missed (lead undefined; counted in the coverage
denominator). Pooled median lead per method = median over covered
(force, seed) pairs; coverage = covered / all breaching (force, seed)
pairs. Full per-pair lead rows are saved for every method and target
(never best runs).

**The advantage criterion (binding; the forecasting prong).** On the
gating cell/scope, for each gating baseline b ∈ {last-value, linear
extrapolation, CUSUM}:

- **Effect:** Δ_b = median_lead(TRA-Q) − median_lead(b) over covered
  pairs (the FALSIFIER-U quantity, per baseline).
- **Uncertainty:** 95% percentile CI for Δ_b from a cluster bootstrap
  over breaching forces: resample the breaching-force set with
  replacement (all 25 seeds of a resampled force carried together),
  recompute both pooled medians and Δ_b per replicate, B = 2000
  replicates, rng `np.random.default_rng(stable_seed("e4", "boot",
  "primary"))`. (If a replicate leaves either method with no covered
  pairs, that replicate is dropped and the drop count reported.)
- **Criterion:** Δ_b > 0 **and** CI lower bound > 0 **and**
  coverage(TRA-Q) ≥ coverage(b) − 0.05.

And the prong additionally requires **median_lead(TRA-Q) > 0** — a
positive validated median lead, H1's minimal content. The forecasting
prong **passes iff the criterion holds against all three baselines
and the positivity condition holds**. TRA-Q's death under FALSIFIER-U
was by tie/trail on the bare median (LR 3.0 vs 3.0/3.0; GB 3.0 vs
4.0 against extrapolation) at coverages well below extrapolation's
(0.321 vs 0.528) — the coverage condition exists so that an
"advantage" bought by alarming on fewer breaches cannot pass here.

## 7. The accounting prong (ported T4, frozen)

On the gating cell (EO, τ\*(primary, EO), H = 2, FAR target 0.10), per
LOSO fold of CTRL, exactly E2 §8's port of family 1's T4: θ = the
fold's CTRL θ(0.10); FAR_fold and FAR_train@θ over null instances;
TV50 (and TV20 sensitivity) between the test force's null scores and
the pooled training null scores; a fold passes iff |FAR_fold −
FAR_train@θ| ≤ TV50 + 0.02. **Criterion (family 1, verbatim):** median
fold TV50 ≥ 0.05 **and** fold pass fraction ≥ 0.99, on the primary
class. The secondary class is computed and reported under the
identical criterion, non-gating (E2's per-class adjudication pattern).

## 8. The E4 bar (conjunctive) and verdict labels

**E4 CLEARS iff all three prongs pass on the confirmatory arm:**

1. **Non-vacuity at adapted scale** (primary class, EO, τ\*): (a) ≥ 3
   included forces record a first population EO crossing strictly
   after the base month; (b) ≥ 40% of included forces have population
   EO gap < τ\* in the base month; (c) the pooled headline instance
   set contains label-1 instances from ≥ 3 distinct forces (the
   upgrade's vacuity clause, forces in place of tasks).
2. **Forecasting advantage:** §6's criterion, in full.
3. **Accounting:** §7's criterion, on the primary class.

**Verdict labels (the plain consequence, stated in `E4_RESULTS.md`):**
- Prong 1 fails → **VACUOUS AGAIN** (failure mode F3 at adapted scale:
  the adapted design still produces no forecastable headline cell —
  e.g., if crossings separate by force level rather than dynamics).
- Prong 1 passes, prong 2 fails → **forecasting claim DEAD at adapted
  scale too** (the F3 escape is closed: the cell was non-vacuous and
  the advantage still did not materialise).
- Prongs 1–2 pass → **forecasting claim ALIVE at adapted scale**
  (scoped exactly: this family, this scale rule, this class, this
  operating point). If prong 3 then fails, E4's full bar is NOT
  cleared and the accounting failure is reported as its own finding —
  the forecasting verdict and the bar verdict are never merged.

**Failure modes (all reportable; none absorbed):** F1 — the bound does
not price 2023 transport (prong 3 fails with small TVs / ≥ 2 folds
beyond slack); F2 — no material transport failure on 2023 (deviations
≈ 0, TVs small: accounting untested, not falsified); F3 — vacuity
(prong 1). Plus the forecasting outcomes of §6, which are verdicts,
not failure modes.

## 9. Secondary arm — family 1 re-test under the adapted rule

Scope: the original build's surviving artifacts (`results/
monitor_steps.csv`, `results/population_metrics.csv`; 18 trajectories,
LR — the original scope's only deployed class; the expanded upgrade
tree is absent and is not reconstructed). τ\*_F1(EO) = Q₀.₇₀ of the
108 pooled population EO gaps of `population_metrics.csv` (computed
from that frozen file; its value is recorded in the results, and for
the record sits just above the original τ = 0.05, whose ecdf position
is 0.694). Labels are recomputed at τ\*_F1 from the population table
by DESIGN.md §3's rule; the method suite of §6 is run at the yearly
scale (H ∈ {1, 2} years, FAR targets as §6, LOSO over the 6 states)
under the **corrected semantics** of Amendments U1–U3 (the original
build's series-baseline leak is not reproduced); CUSUM uses §6's
scale port at τ\*_F1. All three §8 prongs are computed and reported,
labelled **SECONDARY — does not gate E4**, including the advantage
criterion with its bootstrap (cluster unit: breaching trajectories).
This arm answers the design question on the family where the claim
originally died; it cannot resurrect or kill the confirmatory verdict.

## 10. Sensitivity (descriptive only, frozen)

On the confirmatory arm's primary class, the §6 gating quantities
(pooled median leads, coverages, Δ_b without CIs) are also computed
at q ∈ {0.60, 0.80} (τ\* recomputed by §2's formula at those
quantiles; all other protocol elements identical). Reported in full,
labelled descriptive: they show whether the confirmatory verdict is
a knife-edge artefact of the quantile constant. They carry no verdict
language and cannot alter §8's adjudication.

## 11. Data, inclusion, deployed models (inherited apparatus)

- **Candidates (13, inherited from E2 §3 verbatim):**
  avon-and-somerset, cheshire, cleveland, cumbria, devon-and-cornwall,
  hertfordshire, humberside, kent, leicestershire, northumbria,
  south-wales, staffordshire, sussex. The list is **not** re-derived
  from 2023 metadata; no 2023 volume probe is taken before the freeze
  (E2's June-2024 probe has no E4 analogue — acquisition sizing is
  inherited from E2's observed file sizes).
- **Acquisition:** `GET https://data.police.uk/api/stops-force?force=
  <force>&date=<YYYY-MM>` for every candidate × month 2023-01…2023-12,
  raw JSON cached at `elevation/data/raw23/<force>_<YYYY-MM>.json`,
  alphabetical force order, checkpointed (existing valid files
  skipped); if the raw23 cache reaches 70 MB, acquisition stops and
  any force left with missing months fails inclusion rule (i) — E2
  §3's budget rule, inherited. No other data source.
- **Usable record / label / attribute / features:** E2 §§4–5 verbatim
  (involved_person, SDE present, outcome present; y = 1 iff outcome
  "Arrest"; A = 1 iff SDE starts with "White"; the 8 frozen features;
  ethnicity never a feature). Officer-defined grouping remains a
  population-audit sensitivity only.
- **Inclusion rule:** E2 §5 verbatim, applied mechanically to the
  2023 corpus: (i) all 12 monthly files present and non-empty;
  (ii) median monthly usable ≥ 300; (iii) minimum monthly usable
  ≥ 150; (iv) SDE-present share ≥ 0.80; (v) non-White share ∈
  [0.04, 0.96]; (vi) arrest base rate ∈ [0.03, 0.60]. Every
  candidate's disposition and numbers are reported. The included
  count is whatever the rule yields; if it is < 3, prong 1 fails
  mechanically and the verdict records the inclusion collapse as the
  cause.
- **Deployed models:** trained once on pooled 2023-01 usable records
  of the included forces (70/30 split, `np.random.default_rng(0)`;
  OneHotEncoder(handle_unknown="ignore") fit on the training rows —
  E2's `train_score` construction): LR LogisticRegression(C=1.0,
  lbfgs, max_iter=2000); GB GradientBoostingClassifier(n_estimators=
  100, max_depth=3, learning_rate=0.1, random_state=0) (E2's disclosed
  family-2 estimator for the class). Frozen, then applied to every
  (force, month) population. Population metrics at the 0.5 decision
  cut (family-1 `eo_gap`/`dp_gap` definitions).
- **Artifacts** live under `elevation/` in the E4 tree (`data/raw23`,
  `data/populations23`, `data/scores23`, `results4/`, `src4/`,
  `logs4/`). E2's trees are read-only inputs and are never written.

## 12. Determinism, checkpointing, validation

- `stable_seed` (CRC32, family 1 verbatim) with the "e4" tag for all
  E4 stochastic draws; the bootstrap uses its own frozen seed (§6).
  No wall-clock or hash-order dependence.
- Every stage skips work whose artifacts exist (E2's resumability),
  so a host reboot (~90-minute cadence) costs at most the in-flight
  stage. Acquisition is per-file checkpointed.
- `elevation/validate_e4.py` independently recomputes, from saved
  artifacts only (no builder module imported): a sample of 2023
  population metrics from the saved score parquets; monitor
  completeness; defined-label counts at τ\* against the population
  table; the headline accounting from saved fold scores (E2's
  validator pattern); the §8 prong-1 quantities from the population
  table; and the forecasting prong's inputs (pooled median leads,
  coverages, Δ_b, and the bootstrap CIs with the frozen seed) from
  the saved per-pair lead rows and alarm stores. **The verdicts in
  `E4_RESULTS.md` may rest only on numbers this validation
  reproduces; validation must print ALL PASS before the results are
  written as final.**

## 13. Scope limits (binding)

E4 edits no manuscript file, chooses no venue, contacts no journal,
and spends $0. It does not re-run E2, does not alter any frozen
constant of E2 or of family 1, and does not touch the 2024 corpus.
TRA-Q's ablations (pure-own, κ sensitivity, TRA-R) and the LOTO
scheme — secondary in the upgrade — are out of scope: this cycle
tests the falsifier pair at adapted scale, nothing else. E3 is not
part of this cycle; `E4_RESULTS.md` closes with an E3-eligibility
statement only.

---

## Amendment log

*(append-only; each entry dated, with reason, written before the run it
affects)*

— none at freeze —

### Amendment A-E4-1 — 2026-11-01T16:51Z — confirmatory year 2023 → 2025 (data-availability failure of the frozen source; recorded before any confirmatory run)

**What happened.** Acquisition of the frozen corpus (2023, §11) was
attempted from 2026-11-01T16:17Z under the frozen protocol. Result
after the initial pass plus repeated checkpointed retries: 52 of 156
files fetched — **exactly Sep–Dec 2023 for all 13 forces** — and every
Jan–Aug 2023 request returned **HTTP 502**, persistently, across ~500
requests over ~35 minutes. Diagnostic probes (status codes only; no
payload inspected): the API's metadata endpoints respond 200
(`/api/forces`, `/api/crimes-street-dates`); stops-force responds 200
for 2023-09, 2024-04, 2025-06 and 502 for 2023-08 and 2022-06. The
frozen endpoint therefore serves only a rolling recent window
(boundary between 2023-08 and 2023-09 at probe time); the earlier
months of the frozen confirmatory year are **not obtainable from the
frozen source at all**, and aged-out months do not return. No 2023
record was ever parsed, counted, scored, or inspected: the pipeline
never ran on the partial cache (build_populations was never executed
for E4), and the 52 partial files were **deleted** when this amendment
was recorded. The family-1 secondary arm (§9), which needs no network,
had already run; it is unaffected.

**The amendment.** Everywhere this document specifies the confirmatory
corpus as calendar 2023 (months 2023-01…2023-12, base month 2023-01),
read calendar **2025** (months 2025-01…2025-12, base month 2025-01).
Artifact trees are renamed accordingly (`data/raw25`,
`data/populations25`, `data/scores25`). **Nothing else changes**: the
candidate list, acquisition protocol and budget, usable-record
definition, inclusion rule, deployed models, monitor, scale-adaptation
rule and its constant, primary-class rule, forecasting test and
criterion, accounting port, conjunctive bar, sensitivity, and
validation are exactly as frozen.

**Why this preserves the design.** (i) The hygiene property the year
choice carried — *a complete calendar year E2 did not touch* — holds
for 2025 exactly as for 2023: E2 used 2024 only, and no 2025 record
had been fetched, counted, or inspected at the time of this amendment
(the single 2025 probe above returned a status code, not data).
(ii) The choice between candidate replacement years was made on
outcome-blind criteria only — completeness within the served window
and non-overlap with E2 — before any 2025 data existed on disk; 2025
is the only complete untouched calendar year the source serves (2026
is partial). (iii) No design constant was derived from 2023 in the
first place (§§2–3 anchor them to family 1 and the estimand), so no
constant's justification is disturbed. The confirmatory claim's scope
narrows in one stated respect: the confirmatory arm is family 2 in
2025 rather than 2023; `E4_RESULTS.md` will carry that scope verbatim.

### §4 recording — 2026-11-01T17:03Z — primary-class determination and τ\* values (population quantities only; recorded before the monitor, forecaster, or accounting stages run)

**Acquisition and inclusion (frozen §§11/5, as amended by A-E4-1).**
156/156 files fetched for 2025 (one legitimately empty month:
humberside 2025-06, n = 0; budget not reached). The §5 rule applied
mechanically yields an **8-force analysis set**: avon-and-somerset,
cheshire, cumbria, devon-and-cornwall, hertfordshire, kent,
northumbria, sussex. Excluded: cleveland (SDE share 0.712 < 0.80),
humberside (min monthly usable 0), leicestershire (min 65 < 150; SDE
share 0.743), south-wales (min 0), staffordshire (min 1).

**Primary class (§5 rule).** Base-month (2025-01) holdout AUCs from
the deployed stage: LR **0.638995**, GB **0.639791**; |Δ| = 0.000795
≤ 0.005 → tie → **primary class = LR**; GB is the secondary class.

**τ\* values (§2 formula, Q₀.₇₀ confirmatory; Q₀.₆₀/Q₀.₈₀ sensitivity),
96 pooled (force × month) cells per class:**

| class | metric | Q₀.₆₀ | Q₀.₇₀ (τ\*) | Q₀.₈₀ |
|---|---|---|---|---|
| LR | EO | 0.0 | **0.0** | 0.0 |
| LR | DP | 0.0 | **0.0** | 0.0 |
| GB | EO | 0.0 | **0.0033289** | 0.0093458 |
| GB | DP | 0.0 | **0.0019343** | 0.0031746 |

**What the audit shows (stated plainly, because it decides what this
cycle can and cannot test).** On the 2025 corpus the deployed LR's
scores never reach the registered 0.5 decision cut in any population
(maximum score 0.46–0.496 in the sampled cells; alarm share 0.0), so
the population EO and DP gaps of the primary class are **identically
zero in at least 75% of cells** (75th percentile = 0; maximum cell
0.20) and the frozen quantile rule returns τ\* = 0. At τ = 0 the
prong-1 population inputs are already determined: crossings strictly
after the base month = **0**, share of forces below τ\* at base =
**0.0**, every force nominally "breached" at the base month — prong 1
cannot pass on the primary scope, and the LR headline cell will
contain no labelled instances (a label requires pop gap < τ).
**No repair is applied.** Any post-audit modification of the rule
(a nonzero-gap quantile, a different decision cut, a primary-class
switch) would be a design change chosen because the frozen rule
degenerated on the confirmatory data — outcome-adaptive on this arm,
and barred by §3's hygiene rule. The pipeline runs exactly as frozen;
the monitor, forecasting, and accounting stages will record the
consequence, the GB secondary scope will be reported in full, and the
verdict language of §8 applies as written (prong-1 failure ⇒ VACUOUS
AGAIN — here with a named sub-cause: the monitored gap process is
degenerate at the registered decision cut on this family-year, a
distinct mechanism from E2's F3 scale-boundedness).
