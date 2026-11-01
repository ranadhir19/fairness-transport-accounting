# Closure — Proof of the Transport Bound for the EO/DP Gap Statistics

**Cycle:** Paper 11 closure cycle, under `CLOSURE_PREREGISTRATION.md`
(frozen 2026-11-01T18:14:37Z, SHA-256
`4f4b10625ea08618fbc05098daa9c5d5492154847bb8cb8a8875538e925c56f3`).
**Obligations:** PO1–PO6 are discharged in this document; PO7 (fold
computation) is discharged by `src_closure/closure_accounting.py` as
checked independently in `CLOSURE_CHECKER_REPORT.md`.
**Notation and definitions** are exactly the pre-registration's §2:
populations p, q over records (S, A, Y); S = s(X) ∈ [0,1] from one
fixed state-blind rule s; Ŷ = 1{S ≥ c}, c = 0.5;
R_p(C) = Pr_p[Ŷ=1 | C] = μ_p^C([c, 1]) for a stratum C, with
μ_p^C = Law_p(S | C);
DP_p = |R_p(A=1) − R_p(A=0)|;
EO_p = max( |R_p(1,1) − R_p(1,0)|, |R_p(0,1) − R_p(0,0)| ),
writing R_p(y,a) = R_p(Y=y, A=a) — the pipelines' `dp_gap` / `eo_gap`
(`src/common.py` lines 34–44, 64–67; ported in
`elevation/src/common2.py` lines 65–83), including the convention
that a component whose stratum is empty is dropped (population
reading: the component is undefined; see the scope remark after PO3).

---

## PO1 — The stratum lemma (and G3(i): this is T1's own argument)

**Lemma.** For every stratum C with Pr_p(C), Pr_q(C) > 0,
|R_p(C) − R_q(C)| ≤ TV(μ_p^C, μ_q^C).

**Proof.** R_p(C) = μ_p^C(E) and R_q(C) = μ_q^C(E) for the single
fixed event E = [c, 1] ⊆ [0,1] (the same event for both populations,
because the rule s and the cut c are state-blind). By the variational
definition of total variation,
|μ_p^C(E) − μ_q^C(E)| ≤ sup_B |μ_p^C(B) − μ_q^C(B)| = TV(μ_p^C, μ_q^C).
∎

**G3(i).** T1 of the upgrade WS3 is this lemma with the stratum
taken to be the null-step population and μ the forecaster's
step-score law: FAR_s(θ) = P_s^0(S ≥ θ) is one event's probability
under P_s^0. Nothing in the lemma is specific to that choice of
stratum or score. The gap bounds below are therefore compositions of
T1's own argument over the strata that define the gaps; **no new
inequality is used anywhere in this proof.** ∎

## PO2 — G1: DP transport

**Claim.** |DP_p − DP_q| ≤ D_DP(p,q) :=
TV(μ_p^{A=1}, μ_q^{A=1}) + TV(μ_p^{A=0}, μ_q^{A=0}).

**Proof.** Write u_a = R_p(A=a), v_a = R_q(A=a). Then
|DP_p − DP_q| = ||u₁ − u₀| − |v₁ − v₀}|
≤ |(u₁ − v₁) − (u₀ − v₀)|  (reverse triangle inequality)
≤ |u₁ − v₁| + |u₀ − v₀|
≤ TV(μ_p^{A=1}, μ_q^{A=1}) + TV(μ_p^{A=0}, μ_q^{A=0})  (PO1, twice). ∎

**Definitional match.** `dp_gap(a, alarm)` returns
|mean(alarm | A=1) − mean(alarm | A=0)| with alarm = 1{score ≥ 0.5}:
exactly |R̂(A=1) − R̂(A=0)| on a finite population. The population
functional DP_p is its population limit, group coding A ∈ {0,1} as
coded by the pipelines in both families. ∎

## PO3 — G2: EO transport (the pipelines' max form)

**Claim.** With D_TPR = Σ_a TV(μ_p^{1,a}, μ_q^{1,a}) and
D_FPR = Σ_a TV(μ_p^{0,a}, μ_q^{0,a}):
(i) |TPR-gap_p − TPR-gap_q| ≤ D_TPR and
    |FPR-gap_p − FPR-gap_q| ≤ D_FPR, componentwise;
(ii) |EO_p − EO_q| ≤ D_EO(p,q) := max(D_TPR, D_FPR).

**Proof.** (i) Each component is a two-group difference of stratum
rates, so PO2's argument applies verbatim within the stratum family
{(1,a)} resp. {(0,a)}: e.g.
|TPR-gap_p − TPR-gap_q| ≤ Σ_a |R_p(1,a) − R_q(1,a)| ≤ D_TPR by PO1.
(ii) For nonnegative u, v, u′, v′:
|max(u,v) − max(u′,v′)| ≤ max(|u−u′|, |v−v′|).
(Indeed, if max(u,v) ≥ max(u′,v′), say max(u,v) = u, then
max(u,v) − max(u′,v′) ≤ u − u′ ≤ |u−u′|; the other case is
symmetric.) Apply with (u,v) = (TPR-gap_p, FPR-gap_p),
(u′,v′) = (TPR-gap_q, FPR-gap_q) and use (i):
|EO_p − EO_q| ≤ max(D_TPR, D_FPR). ∎

**Definitional match.** `eo_gap` computes the max of |TPR₁ − TPR₀|
and |FPR₁ − FPR₀| over the components whose strata are non-empty
(family 1: `np.nanmax` over the two components; family 2's port: max
over non-NaN components). The population statement is made under the
pre-registration's scope condition (all four (Y,A) strata positive
in both populations), where both components are defined and the code
and the functional coincide exactly.

**Scope remark (registered, not a demotion).** The componentwise
bounds (i) hold stratum-family by stratum-family whenever the
relevant strata are positive in both populations, whether or not the
other family is. Where a stratum has mass zero in one population,
that component of the gap is undefined in the pipelines too — the
statistic and the bound lose the same component at the same place.
The 2025-LR degeneracy (E4) is the extreme case: there the gaps are
defined (strata are positive; the *scores* sit below the cut), the
bound applies, and the gaps are identically 0 because every R_p(C)
for the affected cells is 0 — the bound prices a difference of
zeros correctly.

## PO4 — G3(ii): prevalence decomposition (reduction to FAR-type transports); G3(iii): covariate corollary

**Identity.** For each group a, with π_p(a) = Pr_p[Y=1 | A=a], the
law of total probability over Y given A=a gives
R_p(A=a) = π_p(a)·R_p(1,a) + (1 − π_p(a))·R_p(0,a).

**Reduction bound.** Subtracting the identity for q and regrouping,
R_p(A=a) − R_q(A=a)
= π_p(a)·[R_p(1,a) − R_q(1,a)]
+ (1 − π_p(a))·[R_p(0,a) − R_q(0,a)]
+ [π_p(a) − π_q(a)]·[R_q(1,a) − R_q(0,a)].
Applying PO2's triangle step and PO1 stratum by stratum:
|DP_p − DP_q| ≤ Σ_a { π_p(a)·TV(μ_p^{1,a}, μ_q^{1,a})
+ (1 − π_p(a))·TV(μ_p^{0,a}, μ_q^{0,a})
+ |π_p(a) − π_q(a)|·|R_q(1,a) − R_q(0,a)| }.
Every quantity on the right is measurable from the same per-record
artifacts as the gaps themselves: the label-1 and label-0 stratum
transports (the TPR-type and **FAR-type** — label-0 — transports,
i.e. the stratum-wise form of Theorem 1's own object), the
prevalences π_p(a), and one realised rate difference per group. This
is the commissioned reduction form: the DP transport is bounded by
FAR-type quantities plus named, measurable terms. (It is weaker than
G1 — the prevalence weights and the extra terms only add slack
relative to the direct stratum bound on R(A=a) — and is recorded as
the reduction, not as the primary statement.) ∎

**G3(iii) — covariate corollary.** Each μ_p^C is the pushforward of
the covariate law ν_p^C = Law_p(X | C) under the common map s. Total
variation contracts under a common channel (data processing):
TV(μ_p^C, μ_q^C) ≤ TV(ν_p^C, ν_q^C). Hence G1 and G2 hold with every
score law replaced by the corresponding covariate law, at weaker
constants. This is a corollary of the primary statements, recorded
so the manuscript can state the covariate form honestly as the
weaker version. ∎

## PO5 — G4: tightness of form

**Single stratum (T2's construction).** For any δ ∈ [0,1] and base
rate r with r + δ ≤ 1, score laws on the two points {u, v},
u < c ≤ v: μ = (1 − r)δ_u + rδ_v, μ′ = (1 − r − δ)δ_u + (r + δ)δ_v
give TV(μ, μ′) = δ and μ′([c,1]) − μ([c,1]) = δ. So PO1's bound is
attained stratum by stratum (this is WS3's T2, restated in stratum
form).

**Sum form (G1, and G2's components).** Fix (δ₀, δ₁) with
δ₀ + δ₁ ≤ 1. In population q set R_q(A=1) = R_q(A=0) = δ₀; in p set
R_p(A=1) = δ₀ + δ₁ and R_p(A=0) = 0, realising each group's rate
through the two-point construction above (stratum TVs exactly δ₁
for A=1 — the rate moves δ₀ → δ₀ + δ₁ — and δ₀ for A=0 — the rate
moves δ₀ → 0). Then DP_q = 0, DP_p = δ₀ + δ₁, so
DP_p − DP_q = δ₁ + δ₀ = D_DP: equality in G1. Where D_DP > 1 the bound is vacuous
(|DP_p − DP_q| ≤ 1 always) and no tightness claim is needed; the
registered claim — best possible as a function of the stratum TVs
alone — is the claim on the non-vacuous region, and it holds there.

**Max form (G2).** Hold the label-0 strata identical between p and
q (D_FPR = 0, FPR gaps equal) and realise D_TPR = δ₀ + δ₁ ≤ 1 inside
the label-1 strata exactly as above; then EO_p − EO_q = D_TPR =
max(D_TPR, D_FPR) whenever D_TPR ≥ the (equal) FPR gaps, which the
construction arranges by giving both populations FPR gap 0. Equality
in G2 on its non-vacuous region. The componentwise bounds inherit
tightness from the component constructions. ∎

## PO6 — G5: the estimation form, stated at its exact strength

The fold criterion (pre-registration §3 G5, §7) replaces each
population TV by `tv_hist` on the fold's conditional score samples:
50 equal-width bins on [0,1], TV̂ = ½Σ|p̂ᵢ − q̂ᵢ|.

**Binning step.** The binned law is the pushforward of μ under the
binning map b: [0,1] → {1,…,50}; by data processing,
TV(b#μ_p^C, b#μ_q^C) ≤ TV(μ_p^C, μ_q^C). So each binned term
estimates its stratum TV **from below**: D̂_G ≤ D_G(binned
populations) ≤ D_G whenever the samples are the populations.

**What the fold quantities are.** In this cycle's recompute the
"populations" are the complete usable record sets of the fold
partitions (the pipelines' analysis populations, in full). Realised
gap differences and D̂_G are therefore exact functionals of those
record sets — there is no sampling step and no seed. The sampling
fluctuation T4's slack was designed against enters only if the
record sets are themselves read as samples of a super-population;
the criterion is applied, exactly as T4 applies it, at the level of
the record sets.

**The slack's role — stated exactly, per the pre-registration.**
The theorem guarantees realised_G ≤ D_G (unbinned). The criterion
tests realised_G ≤ D̂_G + 0.02, with D̂_G ≤ D_G: the criterion's
pass is therefore an empirical fact about the accounting (the same
status T4's pass has for FAR), **not** a corollary of the theorem,
and the 0.02 is the registered design constant inherited from T4 —
not a derived concentration bound. No stronger claim is made
anywhere in this cycle's outputs. (Symmetrically, a fold failing
the criterion would not falsify G1/G2; it would show the binned
accounting does not price that fold's gap transport at the
registered slack — the F1-style reportable outcome.) ∎

---

## Discharge summary

| Obligation | Status in this document |
|---|---|
| PO1 stratum lemma | Proved |
| PO2 G1 (DP) | Proved, definitional match shown |
| PO3 G2 (EO, max form) + components | Proved, definitional match shown |
| PO4 G3(ii) reduction; G3(iii) covariate corollary | Proved |
| PO5 G4 tightness | Proved on the non-vacuous region, as registered |
| PO6 G5 estimation honesty | Stated at exact strength; no claim beyond it |
| PO7 fold computation | By `src_closure/closure_accounting.py`; independently checked in `CLOSURE_CHECKER_REPORT.md` |

**Demotions taken: none.** The bound is derived for both statistics,
at the registered forms, at per-fold granularity, with no assumption
beyond the registered scope condition and state-blindness. The kill
criterion is not triggered by the derivation. (The re-adjudication
of §6 of the pre-registration is a separate, computational question
— `CLOSURE_RESULTS.md` — and is not under the kill criterion.)
