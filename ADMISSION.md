# Admission record

**Current verdict: NOT YET ADMITTED**

**Release state:** CANDIDATE

**Proposed version:** 0.1.0

**Reviewed tree:** branch `codex/release-v0.1.0`; candidate freeze in progress
**Last updated:** August 2, 2026

This is the live gate record for the first public research release. A passing
computation is not, by itself, an admission verdict. The project advances only
when the prior-work, adversarial-consistency, and reproducibility gates all
close against the same frozen commit.

## Gate status

| Gate | Status | Required before admission | Present evidence and remaining work |
|---|---|---|---|
| P1 — prior work and claim boundary | PASS | Search exact and nearby mechanisms; inspect primary sources where available; state the bounded corpus and confidence next to the novelty claim. | Prior existence and constructive antecedents are credited. The necessity direction was not located in the bounded corpus, including targeted de Launey/Flannery searches. The paper now says only “apparently new within that corpus”; confidence and access limits are recorded in `audit/PRIOR_WORK.md`. |
| A1 — adversarial consistency | PASS | Re-derive the main and converse proofs; reconcile paper, code, README, figures, and claimed scope; classify findings. | The main construction, both directions of Theorem 2, its corollaries, and the Gaussian reformulation were re-derived and reconciled with every public surface. No contradiction or counterexample was found. See `audit/CONSISTENCY.md`. |
| R1 — reproducibility and release integrity | PASS (pre-freeze) | Run every documented command from a clean environment; regenerate figures; build and inspect the paper; freeze hashes; verify the tagged archive. | Every maintained command passes in the pinned environment; all five figures and the imported matrix regenerate byte-for-byte; the source-date-pinned PDF is deterministic, visually inspected, and uses only embedded Type 1 fonts. Final tree and archive hashes are recorded during the CANDIDATE → TAGGED and TAGGED → ARCHIVED transitions. |

## Claim boundary

- **Proved here:** a choice-free formula for a real Hadamard matrix of order
  `2q(q+1)` for every prime power `q ≡ 1 (mod 4)`; the generalized
  characterization in Theorem 2; and the Gaussian/Butson reformulation.
- **Not claimed:** a new Hadamard order, global priority for the converse, or
  equivalence separation from every output of Farouk–Wang.
- **Computational support:** selected exact Gram checks, deterministic sampled
  checks at larger orders, the printed order-60 comparison, and the coverage
  screen. Sampled checks do not replace proof.
- **Unrefereed report:** `code/alpha_family.py` concerns the choice-dependent
  Farouk–Wang family at `q = 5` and is labeled as such in the paper.

## Supply-first assessment

The structural supply is strong: every prime power `q ≡ 1 (mod 4)` supplies a
finite field and quadratic character, and the parameter map is uniformly
`q ↦ 2q(q+1)`. The family therefore has genuine infinite realization yield.
Its new-order yield is zero within the checked literature because existence at
these orders is prior work. The release value rests on the canonical formula,
the converse characterization if P1 and A1 close, and the structural link to a
Gaussian Butson matrix. The order-60 profile is an equivalence invariant, not
an existence mechanism.

## State transitions

| State | Condition | Status |
|---|---|---|
| DRAFT → CANDIDATE | P1, A1, and pre-freeze R1 pass; prose and artifacts agree. | Passed August 2, 2026 |
| CANDIDATE → TAGGED | Freeze one clean commit and create one immutable tag. | Pending |
| TAGGED → ARCHIVED | Archive the tagged tree; verify the downloaded archive byte-for-byte. | Pending |
| ARCHIVED → ADMITTED | Activate DOI, reconcile all public surfaces, and issue the final verdict. | Pending |

No DOI has been reserved, no tag has been created, and no archive has been
published.
