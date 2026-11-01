# E3 Pre-Registration — Paper 11 Elevation, Cycle E3

## The forecastability-limit theorem

**Commissioned:** Ranadhir Ghosh, 2026-11-01 — *"Commission E3 as a
limit theorem, then rebuild bound-only."* E3 is commissioned in exactly
the form E4's closing assessment declared eligible: a limit theorem
that *explains the accumulated record*. It is not a claim rescue, not
a third empirical cycle, and nothing produced by this cycle may cite
the E4 confirmatory arm as a forecasting falsification (that arm was
a degeneracy, not a falsification; the falsification evidence is
family 1's, twice over).

**Freeze discipline.** This document is frozen before any proof is
scored and before any regime quantity is computed from the saved
artifacts. Its SHA-256 and the freeze timestamp are recorded in
`ELEVATION_LOG.md` in the entry that accompanies this freeze. Any
later change is appended as a dated amendment with its reason, under
the paper's amendment discipline. No silent re-registration.

---

## 1. The record this theorem must explain (fixed inputs)

All validator-confirmed; sources named; no new empirical run is part
of E3.

- **R1 — FALSIFIER-U at absolute τ (family 1, upgrade scope).** 51
  jurisdictions, 306 trajectories per class, headline cell EO /
  τ = 0.05 / H = 2 / LOSO / FAR target 0.10. TRA-Q's pooled median
  lead did not strictly exceed both trivial forecasters in either
  class (LR: 3.0 vs extrapolation 3.0; GB: 3.0 vs extrapolation 4.0),
  while TRA-Q **did** repair calibration transport on both registered
  criteria in both classes (per-fold FAR spread and fold-mean
  deviation both strictly smaller than CTRL). Source:
  `upgrade_report.md`, `upgrade_tester_report.md`, submitted
  manuscript §7.
- **R2 — FALSIFIER-U at adapted scale (family 1, E4 secondary arm).**
  Original 18 trajectories, τ\* = Q₀.₇₀ = 0.050533. Non-vacuous
  (7/18 cross after base; prong 1 PASS), accounting PASS (TV50
  0.4053, 6/6). TRA-Q median lead 3.0 yr, coverage 0.606; vs
  extrapolation Δ = 0.0 (tie), vs last-value Δ = +1.0 with 95% CI
  [−1.0, 4.0] (includes 0); prong 2 FAIL. Source: `E4_RESULTS.md`,
  `results4/f1_arm.json`, `results4/f1_arm_leads.parquet`.
- **R3 — E2 scale-boundedness vacuity (family 2, 2024).** LR
  population EO gaps reach 0.05 in 2/108 force-month cells; crossings
  after base 2/1/0/0 at τ = 0.05/0.10/0.15/0.20 against ≥ 3 required
  (failure mode F3). Source: `E2_RESULTS.md`,
  `results/population_metrics.csv`.
- **R4 — E4 statistic-degeneracy vacuity (family 2, 2025).** Primary
  class LR: deployed scores max 0.46–0.496 in the sampled populations,
  alarm share exactly 0.0 at the registered 0.5 cut; population gaps
  identically 0 in 84.4% of cells (81/96); τ\* = 0.0 at Q₀.₆₀/Q₀.₇₀/
  Q₀.₈₀; 0 crossings, 0 defined instances. Source: `E4_RESULTS.md`,
  `results4/population_metrics.csv`, `results4/tau_star.json`.
- **R5 — the bound's accounting travels (context, not a forecasting
  input).** Family 1: LR TV50 0.3481 50/50 MET, GB 0.1358 50/51 not
  met. Family 2 2024: LR 0.4784 9/9, GB 0.2865 9/9, both MET. Family
  2 2025 (GB scope): 0.3475, 7/7, MET. Sources: `upgrade_report.md`,
  `E2_RESULTS.md`, `E4_RESULTS.md`.

## 2. Setting and notation (fixed)

Steps t = 0, …, T. A frozen deployed classifier; population fairness
gap Δ_t ∈ [0, 1] (EO or DP gap, per the manuscript's §3 definitions)
at step t; compliance threshold τ; breach time
t\* = min{t : Δ_t ≥ τ}. At each step the monitor observes one batch
and may compute any statistic of the batches seen so far; ℱ_t is the
σ-field of the full batch history to t. A **forecaster** is any alarm
rule measurable w.r.t. batch history, with per-step alarm decisions
at t made from ℱ_t. Operating characteristics are the manuscript's:
step-level FAR over negative instances (pre-breach steps whose
H-window contains no breach), coverage over breaching instances, and
lead time t\* − t_alarm for the first alarm at or before t\*;
FALSIFIER-U compares **pooled median lead over covered instances** at
matched FAR target.

The **reference information** is 𝒢_t = σ(Ŷ_{t−1}, Ŷ_t), the last two
batch gap estimates — the information the two trivial forecasters
(last-value, linear extrapolation) actually use. The theorem's
question: *how much can ℱ_t be worth over 𝒢_t, in this regime?*

## 3. The registered theorem package

Claim tiers are fixed here and may not be upgraded after the fact:
**[P]** = proved analytically in this cycle; **[C]** = certified
numerically by exact computation on measured inputs (the computation
and its inputs are artifacts); **[M]** = mapped/reported only.

### Lemma L1 — history-value bound [P]

Let X_t = (Δ_{t+1}, …, Δ_{t+H}) and suppose
δ_t := E[ TV( Law(X_t | ℱ_t), Law(X_t | 𝒢_t) ) ] ≤ δ.
Then for every ℱ_t-measurable alarm rule A there exists a
𝒢_t-measurable randomised rule A′ with, over the instance
distribution: |FAR(A) − FAR(A′)| ≤ δ; |coverage(A) − coverage(A′)| ≤
δ; and for every ℓ ≥ 1,
|P(A: lead ≥ ℓ ∧ covered) − P(A′: lead ≥ ℓ ∧ covered)| ≤ δ.
*No distributional assumption. The lead statement is joint with
coverage — deliberately: it is the form that does not divide by a
coverage probability.*

### Model G and Theorem T2 — the size of δ in the batch-monitoring regime

**Model G.** Δ_{t+1} = Δ_t + μ_t + η_t; μ_{t+1} = φμ_t + ζ_t;
η_t ~ N(0, σ_η²), ζ_t ~ N(0, σ_ζ²), all independent;
Y_t = Δ_t + ε_t, ε_t ~ N(0, σ_n²). Write σ_μ² = σ_ζ²/(1 − φ²) for
the drift state's stationary variance (the *predictable increment
variance* is bounded by σ_μ²; the increment variance is
σ_inc² = σ_μ²(1 + O(1)) + σ_η² — the exact decomposition is part of
the proof obligations, not assumed here).

**Assumption AB (auxiliary batch statistics).** Forecasters in the
record use, beyond {Y_s}, further statistics of the same batches
(drift budgets, score-distribution TVs, base rates). The theorem is
registered under the explicit assumption that these enter the
predictive law of X_t only through the posterior of the state
(Δ_t, μ_t) — i.e. ℱ_t's predictive content for X_t is that of the
batch microdata's posterior on the state, whose precision is in turn
bounded by the batches' own Fisher information (the plug-in gap
estimate's σ_n is the Cramér–Rao scale for the gap from one batch).
If the proof needs AB in a stronger form than this, the stronger
form is named here in an amendment *before* it is used, or the
affected claim is demoted. AB is the theorem's one named modelling
assumption; everything else in T2 is Model G itself.

**Theorem T2 [P for the reduction and the closed forms; C for the
steady-state evaluation].** In Model G, both predictive laws of
X_t given ℱ_t resp. 𝒢_t are Gaussian, and
E[TV] ≤ δ_G := sqrt( KL̄ / 2 ), where KL̄ = E[KL(Law(X_t|ℱ_t) ‖
Law(X_t|𝒢_t))] decomposes exactly into a **level channel** and a
**drift channel**, each a stated functional of the two posterior
covariance matrices P_ℱ, P_𝒢 of the state (Δ_t, μ_t):
- the mean term is exactly
  tr( Σ_𝒢⁻¹ (P̃_𝒢 − P̃_ℱ) ) with P̃ the posterior-mean covariances
  propagated to X_t (orthogonality of Bayesian posterior means);
- the covariance term is bounded by the registered scalar inequality
  ½[x − 1 − ln x] ≤ (x − 1)²/2 (x ≥ 1) applied eigenwise.
In the drift-free limit (σ_μ → 0) the level channel is closed form:
V_pair = σ_n²(σ_η² + σ_n²)/(σ_η² + 2σ_n²) (two-observation posterior
variance of Δ_t), V_∞ = (−σ_η² + √(σ_η⁴ + 4σ_η²σ_n²))/2
(steady-state Kalman variance), and the level mean-term is
(V_pair − V_∞)/(Hσ_η² + V_pair) up to the registered covariance-term
bound. The full two-state evaluation at measured parameters is by
exact Kalman recursion [C]. **Regime reading (part of the claim):**
δ_G is small when (i) the drift's predictable share is small
(σ_μ² ≪ σ_inc², or φ ≈ 0 so history cannot sharpen μ_t beyond the
last increment), and (ii) σ_n is not small against σ_η (batch
resolution), so V_pair − V_∞ ≪ Hσ_η². δ_G is *not* claimed small in
general: with a persistent, precisely estimable drift, or with
batches large enough that σ_n ≪ σ_η, the bound correctly permits a
real forecasting advantage. The theorem is a boundary, not a
universal impossibility.

### Corollary C1 — the two family-1 falsifications [P given T2; C for the regime check]

If, at family 1's measured regime quantities, δ_G ≤ δ̂ [C], and the
reference rule's lead distribution (from the saved lead artifacts)
satisfies the **median-gap condition**
P_G(lead ≤ m) ≥ ½ + δ̂_marg and P_G(lead ≤ m − 1) ≤ ½ − δ̂_marg
at its pooled median m (under the falsifier's covered-only
convention, with δ̂_marg = δ̂ inflated by the registered
coverage-division factor (1/cov_A + 1/cov_G − 1) using the two
rules' coverages), then every ℱ_t-forecaster's pooled median lead
equals m: **strict exceedance — FALSIFIER-U's requirement — is
impossible in the regime**, for R1 and, with its own saved lead
distribution and regime quantities, for R2.
**Registered demotion ladder for C1** (fixed now, applied in order,
each step reported):
 (i) full strength, as above, per arm;
 (ii) if the coverage-division factor blocks (i) but the
 *all-instances* convention (uncovered := lead 0) satisfies its
 median-gap condition with δ̂ uninflated, C1 is claimed in the
 joint/all-instances form, and the covered-only gap is reported as
 a named limitation with its numbers;
 (iii) if neither holds for an arm, that arm is listed **NOT
 COVERED** with the computed δ̂ and the computed CDF gaps — the
 kill/demotion record, not a rhetorical bridge.

### Corollary C2 — crossing rarity (E2 scale-boundedness) [P]

For N trajectories observed for T steps with marginal exceedance
frequency p̂_τ = #{cells with Δ ≥ τ}/#{cells}, the number of
forecastable (first-crossing-after-base) trajectories is at most the
number of trajectories whose path ever reaches τ after base, and
E[# first crossings after base] ≤ N·(T − 1)·p_τ under any process
with those marginals (each first crossing at step t requires
Δ_t ≥ τ). Hence a design requiring ≥ K crossing units is
vacuity-exposed whenever N(T − 1)p̂_τ < K. *Registered check (R3):*
family 2 LR at τ = 0.05: p̂ = 2/108, N(T−1) = 9 × 11 = 99 ⇒ bound
1.83 < 3 — the E2 headline cell could not have been non-vacuous at
its own marginals; observed crossings after base: 2. Family 1 at
τ = 0.05 (share ≥ 0.05 = 0.306 on the frozen 108-cell table):
18 × 5 × 0.306 ≈ 27.5 ≫ 3 — non-vacuity consistent with R1/R2.
Adapted thresholds set p̂ by construction (Q₀.₇₀ ⇒ p̂ ≈ 0.30) and
thereby retire rarity — at the price registered in Remark R-τ\*
below.

### Corollary C3 — cut degeneracy (E4 statistic degeneracy) [P]

Let the monitored gap be any function of the decisions
Ŷ = 1{s(X) ≥ c}. If on a population cell the deployed score satisfies
P(s(X) ≥ c) = 0 within every (group × label) stratum, then Ŷ ≡ 0 on
the cell, every group-conditional decision rate is 0, and the DP gap
and both EO component gaps on that cell are **exactly 0** —
deterministically, for every τ and every threshold adaptation.
Consequently any quantile rule applied to a gap distribution with a
point mass ≥ q at 0 returns τ\* = 0, at which the forecasting
instance definition (population gap < τ at base, crossing = reaching
τ) is empty. *Registered check (R4):* family 2 2025 LR — alarm share
0.0 in the sampled populations, gap = 0 in 81/96 cells (84.4%), and
τ\* = 0 at q ∈ {0.60, 0.70, 0.80}: the corollary's condition holds on
≥ 84.4% of cells and the consequence (0 crossings, 0 instances) is
the observed one. The residual cells are registered as the
corollary's boundary: cells with O(1) alarm counts have quantised
gap spikes (multiples of the reciprocal stratum count), whose
crossings carry no drift signal — stated as a remark with the
recorded spike maximum (0.20), not as part of the lemma.

### Proposition P4 — separation of transport and forecastability [P]

Lemma L1 and Theorem T2 are statements *within one population's
instance distribution at matched achieved FAR*: no cross-population
quantity (in particular not the null-score TV of the transport
bound, T1–T3 of the upgrade) enters δ_G. Therefore repairing
calibration transport — driving the achieved-FAR mismatch to zero —
does not relax the lead bound by any amount; the two failures have
independent prices. *Registered check:* R1 is the empirical instance
— TRA-Q repaired transport on both registered criteria in both
classes and FALSIFIER-U fired in both classes. The proposition is
proved by inspection of the bound's dependencies; its content is
that the record's conjunction (transport repaired ∧ lead tied) is
the configuration the theory predicts, not a coincidence to be
explained away.

### Remark R-τ\* — what scale adaptation can and cannot buy [M → P if the algebra closes]

At an adapted threshold τ\* = Q_q of the family's own gap
distribution, rarity (C2) is retired by construction, but the
distance-to-threshold scale becomes the gap distribution's own
upper-tail scale; when that scale is at or below the batch noise
σ_n, batch-statistic crossings are noise events and no forecaster's
alarm can carry drift signal at matched FAR (a corollary of L1 with
𝒢_t = σ(∅) — the same bound with the trivial reference). Registered
as a remark with the family-2 GB instance reported descriptively
(τ\*_GB = 0.003329 against family 2's batch σ_n at n = 200, to be
computed [C]); promotion to corollary requires the L1-with-trivial-
reference derivation to be written out in the proof, failing which
it stays a remark.

## 4. Proof obligations (fixed list)

- **O1.** L1 in full: the covariance-identity step, the passage from
  per-step to pooled FAR/coverage/joint-lead statistics, and the
  randomised reference rule's measurability.
- **O2.** T2 reduction: Gaussianity of both predictive laws;
  orthogonality identity E‖m_ℱ − m_𝒢‖² = tr(P̃_𝒢 − P̃_ℱ);
  Pinsker + Jensen step; the scalar inequality
  ½[x − 1 − ln x] ≤ (x−1)²/2 for x ≥ 1.
- **O3.** Level channel closed forms: V_pair (two-observation Schur
  complement, diffuse level prior) and V_∞ (Riccati fixed point
  V² + Vσ_η² − σ_η²σ_n² = 0, the non-negative root).
- **O4.** Drift channel: exact expression for the propagated drift
  coefficient c_{φ,H} = Σ_{h=0}^{H−1} φ^h and a bound on
  Var(μ̂_ℱ − μ̂_𝒢) that is *proved*, not asserted — either the exact
  two-observation Schur complement for μ_t in the joint
  (μ_t, Δ_t, Y_{t−1}, Y_t) Gaussian, or the registered fallback
  Var(μ̂_ℱ − μ̂_𝒢) ≤ E Var(μ_t | 𝒢_t) ≤ σ_μ² with the regime cost
  stated. Use of the fallback is a *recorded proof-route choice*,
  not a demotion, provided the resulting δ̂ still meets C1's
  condition; if it does not, C1 follows its ladder.
- **O5.** C2's counting bound (union/marginal argument) and both
  registered checks recomputed from the saved population tables.
- **O6.** C3's determinism argument and the R4 check recomputed
  from the saved population/deployed artifacts.
- **O7.** P4's dependency inspection, written out: every quantity in
  δ_G's definition enumerated and shown population-internal.
- **O8.** The regime computation [C]: σ_inc, σ_η, σ_μ, φ̂ estimated
  from the saved family-1 population trajectories by the registered
  estimators (increment variance; lag-1 increment autocorrelation
  mapped to (φ, σ_μ², σ_η²) by the Model-G moment identities, with
  the mapping's own identification failure — negative implied
  variances — reported if it occurs and handled by the registered
  fallback: project to the boundary φ = 0 and report); σ_n from the
  monitor's own saved standard errors *and* from seed-replicate SDs
  of the batch gap at fixed cells (both reported; the larger is
  used in δ̂ — conservative direction registered now); exact Kalman
  steady-state evaluation of KL̄; the lead-CDF median-gap checks
  from the saved lead distributions. All estimators are named here;
  none may be swapped after seeing δ̂.

## 5. The one-cycle kill criterion (binding, from the audit)

**If the theorem does not close at the registered strength within
this cycle, E3 stops and reports the gap exactly.** Operationally:
- If any of O1–O3, O5–O7 fails to close, the theorem package is
  **killed at registered strength**; `E3_RESULTS.md` reports the
  failed obligation and the exact point of failure.
- If the proof closes but C1 lands at ladder step (iii) for *both*
  family-1 arms — the theory true but too weak to explain the
  record it was commissioned to explain — that is also a kill at
  registered strength, reported as such (a true-but-vacuous bound is
  the failure mode this criterion exists to catch).
- Ladder step (ii) for one or both arms, or O4's fallback route, is
  a **demotion**, reported with the scoped claim text — not a kill.
- **No second E3 cycle exists** without Ranadhir's new decision.
  Whatever this cycle produces is what the bound-only rebuild may
  use, verbatim in strength.

## 6. Corollary coverage list (fixed in advance)

| # | Record item | Covering result | Condition to verify |
|---|---|---|---|
| K1 | FALSIFIER-U at absolute τ (R1) | C1 (arm R1) | δ̂ and the median-gap condition on the upgrade-scope lead distribution, or the recorded absence of that artifact tree (see §7) |
| K2 | FALSIFIER-U at adapted τ (R2) | C1 (arm R2) | δ̂ and the median-gap condition on `results4/f1_arm_leads.parquet` |
| K3 | E2 scale-boundedness vacuity (R3) | C2 | N(T−1)p̂ < 3 recomputed from `results/population_metrics.csv` |
| K4 | E4 statistic-degeneracy vacuity (R4) | C3 | alarm-share/gap-zero conditions recomputed from `results4/` artifacts |

Any item whose condition fails is listed in `E3_RESULTS.md` as
**NOT COVERED** with the reason and the computed numbers. No
corollary by assertion.

## 7. Artifact note (registered before the work)

The upgrade-scope (`upgrade/`) artifact tree is absent from this
workspace copy (recorded in the E2 log entry). K1's lead
distribution therefore cannot be recomputed from per-instance leads;
the registered substitute, fixed now: K1 is verified against (a) the
original-scope lead distribution (`results/leadtime_distributions.csv`,
same family, same falsifier, same H/FAR conventions — the scope at
which H1 first died) and (b) the upgrade tester's independently
recomputed headline medians for the expanded scope. If (a)'s
median-gap check passes and (b) agrees in medians, K1 is covered at
the original scope with the expanded scope cited through the tester
— and that scoping is stated in the results, not smoothed over.

## 8. What E3 does not do

No new data, no new forecaster, no re-run of any pipeline stage, no
manuscript edit (the rebuild is Stage 3 of the commission and takes
E3's outcome as it stands), no venue work inside the E3 stages, no
journal contact, $0 spend. Numbers come only from the saved
artifacts named above or from computations on them registered in O8.
