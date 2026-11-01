# E3 — Proof Document

## The forecastability-limit package, as it stands after the one registered cycle

Companion to `E3_PREREGISTRATION.md` (frozen 2026-11-01T17:46:07Z,
SHA-256 `f5e38081…f7b03`). Every claim below carries the tier the
pre-registration assigned it: **[P]** proved, **[C]** certified by
exact computation on measured inputs, **[M]** mapped/reported.
Obligation references (O1–O8) are to the pre-registration §4. The
independent checker's obligation-by-obligation table is in
`E3_RESULTS.md`.

**Standing notation.** Steps t = 0, …, T; population gap Δ_t;
threshold τ; breach time t\* = min{t : Δ_t ≥ τ}; batch history
σ-field ℱ_t; reference information 𝒢_t = σ(Ŷ_{t−1}, Ŷ_t), the last
two batch gap estimates. Alarms do not affect the process (the
classifier is frozen; monitoring is observational) — used in O1.

---

## Lemma L1 (history-value bound) [P]

**Statement (per-step form).** Fix a step t and let X be any
measurable function of the future evolution after t (in particular
X_t = (Δ_{t+1}, …, Δ_{t+H})). Suppose
δ_t := E[ TV( Law(X | ℱ_t), Law(X | 𝒢_t) ) ] ≤ δ.
Let A be any ℱ_t-measurable alarm rule (fire / no-fire at t, with
external randomisation allowed). Then the randomised 𝒢_t-rule A′
that fires with probability q := P(A fires | 𝒢_t) satisfies, for
every measurable B in the range of X:

| P(A fires, X ∈ B) − P(A′ fires, X ∈ B) | ≤ δ.

**Proof.** Write a := P(A fires | ℱ_t) ∈ [0,1] (the rule's firing
probability given the full history; the rule's external
randomisation is independent of X given ℱ_t, since alarms do not
affect the process). By the tower property,
P(A fires, X ∈ B) = E[ a · b ], where b := P(X ∈ B | ℱ_t).
Also q = E[a | 𝒢_t], and
P(A′ fires, X ∈ B) = E[ q · P(X ∈ B | 𝒢_t) ] = E[ E[a|𝒢_t] · E[b|𝒢_t] ].
Hence
P(A fires, X∈B) − P(A′ fires, X∈B)
= E[ a·b ] − E[ E[a|𝒢_t] E[b|𝒢_t] ]
= E[ (a − E[a|𝒢_t]) (b − E[b|𝒢_t]) ],
the last equality because E[(a − E[a|𝒢_t]) · E[b|𝒢_t]] = 0
(conditioning on 𝒢_t). Therefore
|difference| ≤ E[ |a − E[a|𝒢_t]| · |b − E[b|𝒢_t]| ]
≤ E[ |b − E[b|𝒢_t]| ]  (since |a − E[a|𝒢_t]| ≤ 1)
≤ E[ TV( Law(X|ℱ_t), Law(X|𝒢_t) ) ] ≤ δ,
where the third line uses |P(X∈B|ℱ_t) − P(X∈B|𝒢_t)| ≤
TV(Law(X|ℱ_t), Law(X|𝒢_t)) and E[·|𝒢_t] preserves the inequality.
∎

**Pooled passage (O1, second half).**
- **FAR — exact at δ.** The falsifier's FAR instances are steps;
  FAR(A) is the average of per-step firing indicators over negative
  instances. Apply the per-step statement at each negative step with
  B = the whole space (marginal firing probabilities) and average:
  |FAR(A) − FAR(A′)| ≤ δ. ∎
- **Coverage and joint lead — at (T−1)δ, a recorded weakening.**
  Coverage of a breaching instance is the event that A fires at ≥ 1
  of the instance's pre-breach steps, and {lead ≥ ℓ ∧ covered} is
  the event that A fires at ≥ 1 step t with t\* − t ≥ ℓ. These are
  unions over at most T−1 monitored steps. Applying the per-step
  statement step-wise (with B the breach/lead pattern of the future
  path) and the union bound over the ≤ T−1 alarm opportunities
  gives |P(A: E) − P(A′: E)| ≤ (T−1)δ for E ∈ {covered,
  lead ≥ ℓ ∧ covered}. **The frozen L1 statement asserted these two
  clauses at δ; the proof as executed carries them at (T−1)δ. This
  is recorded here as a weakening of L1's coverage/lead clauses
  found by the proof itself (demotion rule, pre-registration §3):
  the FAR clause and the per-step statement stand at δ as
  registered.** No verdict in this cycle turns on the factor: C1
  fails already at δ (see the adjudication in `E3_RESULTS.md`), and
  (T−1)δ̂ = 5 × 0.289 = 1.45 is vacuous, so the weakened clauses
  certify nothing and are used nowhere.

## Theorem T2 (the size of δ in Model G) [P reduction; C evaluation]

**Model G** (pre-registration §3): Δ_{t+1} = Δ_t + μ_t + η_t;
μ_{t+1} = φμ_t + ζ_t; η ~ N(0, σ_η²), ζ ~ N(0, σ_ζ²); Y_t = Δ_t + ε_t,
ε ~ N(0, σ_n²); σ_μ² = σ_ζ²/(1−φ²). Assumption AB as registered.

**Reduction [P].** Given the state x_t = (Δ_t, μ_t), the future path
X_t is Gaussian under both information sets, with a common
innovation covariance Σ_inn (the η/ζ terms after t) and means
A·m + (deterministic 0), covariances A·P·Aᵀ + Σ_inn, where m, P are
the posterior mean/covariance of x_t under the information set, and
A's rows are [1, c_{φ,h}], c_{φ,h} = Σ_{j=0}^{h−1} φ^j (O4's
coefficient: Δ_{t+h} = Δ_t + Σ_{j=0}^{h−1} μ_{t+j} + Ση, and
E[μ_{t+j}|x_t] = φ^j μ_t). By Pinsker's inequality applied
conditionally and Jensen's inequality (√ is concave),
E[TV] ≤ √( KL̄ / 2 ), KL̄ := E[ KL( Law(X_t|ℱ_t) ‖ Law(X_t|𝒢_t) ) ].
For Gaussians,
KL = ½[ tr(Σ_𝒢⁻¹Σ_ℱ) − H + (m_𝒢−m_ℱ)ᵀΣ_𝒢⁻¹(m_𝒢−m_ℱ)
+ ln(det Σ_𝒢 / det Σ_ℱ) ],
and the **orthogonality identity** for exact Bayesian posterior
means under a common prior (both filters are the same Bayesian rule
at different data, in the diffuse-level limit):
E[ (m_ℱ − m_𝒢)(m_ℱ − m_𝒢)ᵀ ] = P̃_𝒢 − P̃_ℱ,
the difference of the posterior-mean covariance matrices propagated
through A — because E[m_ℱ | 𝒢_t] = m_𝒢 (tower property of
conditional expectation under the common law). Hence the mean term
of KL̄ is exactly tr( Σ_𝒢⁻¹ A (P_𝒢 − P_ℱ) Aᵀ ). The covariance
terms are ≥ 0 in aggregate (they are part of a KL), and the
registered scalar bound for them, when a bound rather than the
exact value is wanted, is ½[x − 1 − ln x] ≤ (x−1)²/2 for x ≥ 1
applied eigenwise — the inequality holds because
(x−1)²/2 − ½[x − 1 − ln x] has derivative (x−1) − (1 − 1/x)/2·1…
directly: define g(x) = (x−1)² − (x − 1 − ln x); g(1) = 0 and
g′(x) = 2(x−1) − (1 − 1/x) = (2x² − 3x + 1)/x = (2x−1)(x−1)/x ≥ 0
for x ≥ 1. ∎ (O2 discharged: reduction, orthogonality, Pinsker +
Jensen, scalar inequality.)

**Level channel, closed forms [P] (O3).** Set σ_μ = 0 (drift-free).
*V_pair:* Δ_{t−1} diffuse; Y_{t−1} observes Δ_t through
Δ_t = Δ_{t−1} + η with noise variance σ_η² + σ_n²; Y_t observes Δ_t
with noise σ_n². Two independent Gaussian observations of Δ_t give
posterior precision 1/σ_n² + 1/(σ_η² + σ_n²), so
V_pair = σ_n²(σ_η² + σ_n²)/(σ_η² + 2σ_n²). ∎
*V_∞:* the steady-state filtering variance V satisfies the Riccati
fixed point V = ((V + σ_η²)⁻¹ + σ_n⁻²)⁻¹, i.e.
V² + Vσ_η² − σ_η²σ_n² = 0, whose non-negative root is
V_∞ = (−σ_η² + √(σ_η⁴ + 4σ_η²σ_n²))/2. ∎
*Cross-validation of the [C] evaluation:* the exact Kalman
recursions of the regime computation return P_ℱ[0,0] = 4.6713e-4
and P_𝒢[0,0] = 7.4704e-4, against the closed forms V_∞ = 4.6713e-4
and V_pair = 7.4704e-4 — agreement to the digits shown.

**Drift channel (O4).** Two routes, both recorded:
 (a) *Exact [C]:* the two-state Kalman recursions compute P_ℱ and
 P_𝒢 exactly within Model G for any (φ, σ_μ²); the drift channel
 is inside KL̄'s exact evaluation, not bounded separately.
 (b) *Analytic fallback [P]:* E‖μ̂_ℱ − μ̂_𝒢‖² = E Var(μ_t|𝒢_t) −
 E Var(μ_t|ℱ_t) ≤ E Var(μ_t|𝒢_t) ≤ σ_μ² (orthogonality again;
 conditioning reduces variance in expectation), so the drift
 channel's mean-term contribution is ≤ c_{φ,H}² σ_μ² ·
 ‖Σ_𝒢⁻¹‖-weighting as it appears in the trace.
 At every parameterisation the family-1 moments permit (see the
 evaluation), σ_μ² = 0: the moment map fails identification
 (γ₁ < 0) and the registered boundary projection sets σ_μ² = 0,
 and the φ-sensitivity grid inherits σ_μ² = 0 because γ₁ < 0 admits
 no positive attribution. **The drift channel is therefore exactly
 zero in this evaluation — not by the fallback's looseness but
 because the measured increments carry no positively-persistent
 component for either filter to know.** At φ = 0 this is exact in
 the model too: μ_t first enters Δ_{t+1}, so at time t it is
 unobserved by both information sets with the same prior, and
 contributes identically to both predictive laws.

**Evaluation [C] (O8; `src3/regime_e3.py`, outputs
`results3/regime_e3.json` + `regime_e3_followup.json`).**
Family-1 population EO-gap increments (90 increments, 18
trajectories × 5): mean +0.00272; γ₀ = 2.3785e-4 (σ_inc = 0.01542);
γ₁ = −9.64e-6 (lag-1 autocorr −0.041); γ₂ = −3.02e-5 (lag-2
autocorr −0.127). Moment map: **identification failure** (γ₁ ≤ 0)
→ registered boundary projection (φ = 0, σ_μ² = 0,
σ_η² = γ₀ = 2.3785e-4, σ_η = 0.01542).
σ_n: monitor's saved SE mean 0.03721; seed-replicate SD mean
0.02889 (median 0.02846); registered larger ⇒ **σ_n = 0.03721**
(σ_n/σ_η ≈ 2.41).
Exact Kalman evaluation at (φ=0, σ_μ²=0, σ_η²=2.3785e-4,
σ_n²=1.3846e-3), H = 2: **KL̄ = 0.16718, δ̂ = √(KL̄/2) = 0.28912.**
Mean term 0.28421 (inside KL̄'s ½[·]); covariance part 0.02510.
Sensitivity: δ̂ = 0.28912 across φ ∈ {0, 0.2, 0.4, 0.6} (all with
σ_μ² = 0, as γ₁ < 0 forces); δ̂ = 0.22257 at the smaller σ_n
(replicate SD) — the kill below is robust to both choices.
Decomposition: with the drift channel zero, δ̂ is **entirely the
level channel**: V_pair − V_∞ = 2.799e-4 against a two-step
innovation variance Hσ_η² = 4.757e-4. At batch n = 2,000 the gap
estimate's noise exceeds the population gap's own per-step
movement, so six years of batches denoise the current level
materially beyond the last two batches — and any bound on history's
value must price that. This one does; the price is 0.289.

## Corollary C2 (crossing rarity) [P] (O5)

**Claim.** E[# first crossings after base] ≤ N(T−1)·p_τ for any
process with marginal exceedance frequency p_τ at τ.
**Proof.** A first crossing after base at step t requires
Δ_t ≥ τ. Hence #{first crossings} = Σ_trajectories 1{∃ first
crossing} ≤ Σ_{t=2}^{T} #{trajectories: Δ_t ≥ τ} (each trajectory's
first crossing is counted once on the left and at least once on the
right). Taking expectations with per-step marginal p_τ over N
trajectories and T−1 post-base steps gives the bound. ∎
**Checks [C].** Family 2 LR, τ = 0.05: p̂ = 2/108 = 0.01852;
bound = 9 × 11 × 0.01852 = **1.833 < 3** (the E2 design's
non-vacuity requirement); observed crossings after base,
recomputed from `results/population_metrics.csv`: **2** — the E2
headline cell was vacuity-exposed at its own marginals, as
registered. Family 1, τ = 0.05: share ≥ 0.05 = 0.3056 (33/108
cells); bound = 18 × 5 × 0.3056 = **27.5 ≫ 3** — non-vacuity
consistent with R1/R2. (The bound is on an expectation; the check
is the registered one: requirement vs marginal-implied ceiling.)

## Corollary C3 (cut degeneracy) [P] (O6)

**Claim.** If on a population cell P(s(X) ≥ c) = 0 within every
(group × label) stratum, the cell's DP gap and both EO component
gaps are exactly 0.
**Proof.** Ŷ = 1{s(X) ≥ c} ≡ 0 on every stratum, so every
group-conditional decision rate Pr(Ŷ=1 | A=a) and
Pr(Ŷ=1 | A=a, Y=y) equals 0; DP gap = |0 − 0| = 0; both EO
components are |0 − 0| = 0, and the EO gap (their max) is 0. ∎
**Consequences.** A gap distribution with point mass ≥ q at 0 has
Q_q = 0; at τ\* = 0 the forecasting instance definition (population
gap < τ at base) is empty, since gap ≥ 0 everywhere. Cells with
O(1) alarm counts instead have gaps quantised at multiples of the
reciprocal stratum size (spikes) — registered remark, with the
recorded family-2 spike maximum 0.20.
**Check [C] (R4).** Family 2, 2025, LR (`results4/
population_metrics.csv`): EO = 0 in **81/96 cells (84.4%)**, DP = 0
in 81/96, both = 0 in 81/96; τ\* = 0 at q ∈ {0.60, 0.70, 0.80}
(`tau_star.json`); observed crossings 0, defined instances 0 —
the corollary's consequence is the observed one. The deployed-score
condition (max sampled score 0.46–0.496 < c = 0.5, alarm share 0.0)
is from `E4_RESULTS.md` / the §4 recording; the gap-side conditions
are recomputed here from the saved population table.

## Proposition P4 (separation) [P] (O7)

δ_G's definition enumerates its inputs: (σ_η, σ_μ, φ, σ_n, H) —
properties of one population's gap process and of the batch design
— plus, through L1, the single population's instance distribution
at the falsifier's matched-FAR construction. No cross-population
quantity appears; in particular the null-score TV of the transport
bound (upgrade T1–T3) is not an input, an output, or a relaxation
of δ_G. Hence driving achieved-FAR transport error to zero changes
δ_G by exactly zero: calibration transport and lead-time
forecastability are priced by different quantities. The record's
conjunction — R1: transport repaired on both registered criteria
in both classes ∧ FALSIFIER-U fired in both classes — is the
configuration the proposition predicts. ∎ (dependency inspection,
as registered).

## Remark R-τ\* (scale adaptation's price) [M]

Adapted thresholds retire C2's rarity by construction (Q₀.₇₀ ⇒
p̂ ≈ 0.30) and move the binding constraint to the distance scale:
the threshold becomes the family's own upper-tail scale. Family-2
instance [C inputs]: GB τ\* = 0.003329 against family 2's batch
noise at n = 200 — σ_n = 0.01964 (seed-replicate SD of the batch EO
estimate, `results/monitor.parquet`) and 0.02172 (the monitor's
saved SE mean). The adapted threshold sits ≈ 6× below the batch
noise SD of the monitored statistic: crossings of the batch
statistic at that scale are noise-scale events. Registered as a
remark (the L1-with-trivial-reference promotion was not executed);
no claim in the rebuild may state it as a theorem.

## What does not close — Corollary C1 (adjudicated in E3_RESULTS.md)

C1 required δ̂ to fit inside the reference rule's lead-CDF gaps at
its median, under the registered ladder. The computed numbers:
δ̂ = 0.28912 (0.22257 at the alternative σ_n). Covered-only
convention (ladder i): the registered coverage inflation gives
δ_marg = 0.747 (K1) / 0.738 (K2) — the requirement F(m) ≥ ½ + δ_marg
exceeds 1; impossible. All-instances convention (ladder ii), under
its own median: reference all-instances median = 1 (both arms),
F(1) = 0.5086 against the required ≥ 0.7891, F(0) = 0.4743 against
the required ≤ 0.2109 — fails on both sides. Even the uninflated
joint gaps are too small: extrapolation's covered CDF has
F(3) − ½ ≈ 0.098 (K1) / 0.109 (K2) and ½ − F(2) ≈ 0.152 / 0.141,
all < δ̂. **C1 is at ladder step (iii) for both family-1 arms: NOT
COVERED.** The descriptive record, for scale: the observed joint
lead curves of the ℱ-rule and extrapolation differ by at most
0.103 (K1) / 0.154 (K2) in sup over ℓ ∈ {1,…,5} — inside δ̂, as L1
requires, but the bound is far too weak to *force* the observed
median tie. The theorem permits the record; it does not explain
the falsifications. Per pre-registration §5, second kill clause,
that is the kill event, reported in `E3_RESULTS.md`.
