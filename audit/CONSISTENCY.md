# A1 adversarial consistency audit

**Status:** PASS

**Audit date:** August 2, 2026

**Scope:** mathematical derivation, claim boundaries, paper/code/README agreement

**Excluded:** global novelty and archive integrity, which are P1 and R1

## Verdict

No contradiction, missing hypothesis, dimension error, or counterexample was
found in the three stated theorems. The main construction and the generalized
converse are admitted as internally consistent. This is an audit verdict, not
peer review.

## Main construction

- Every `K_t` and `B_r` is `2q × 2q`; each finite band `M_r` is
  `2q × 2q(q+1)`; the cap has the same width; stacking `q+1` bands gives the
  advertised order `2q(q+1)`.
- The four block-Gram identities use exactly two finite-field facts: the
  quadratic-character correlation sum and bijectivity of
  `a ↦ a(r-s)` for `r ≠ s`.
- The cap cancellation uses `χ(-1)=1`, so the hypothesis
  `q ≡ 1 (mod 4)` is both visible and used at the stated point.
- A cold implementation written from the paper alone, recorded in
  `AUDIT_LEDGER.md`, reproduced exact Hadamard matrices for
  `q = 5, 9, 13, 17, 25`. The maintained implementation independently passes
  full Gram checks through `q = 49`.

## Theorem 2: necessity

The proof was re-derived in the order below.

1. The nine products of `ψ(c)ψ(c')ᵀ` separate into an identity coefficient
   and a skew coefficient, giving equation (5.1).
2. For `r = s`, the shift multiplicity is concentrated at zero. Off-diagonal
   vanishing of the finite-band Gram block forces `B(d) = -2I` for every
   nonzero `d`.
3. The cap/finite Gram block is a linear combination of the independent
   matrices `I` and `R`. Its vanishing forces `σ = 0` and
   `n₀ = n₀² + σ²`. Since `δ(0)=0`, this leaves only `n₀ = 1`.
4. With a unique zero, the identity and skew coefficients of `B(d) = -2I`
   force the Paley autocorrelation equation and evenness of `δ`.
5. For `r ≠ s`, substituting `B(0)=2nI` and `B(d)=-2I` reduces each Gram
   block to `2(n+1)(μ_rs(d)-1)I`. Vanishing for every row difference `d`
   forces `μ_rs(d)=1`, exactly the `(G,n;1)` difference-matrix condition.

No step assumes a field or multiplication on `G`; commutativity is used where
the paper says it is.

## Theorem 2: sufficiency and corollaries

- Paley autocorrelation gives `σ² = Σ_d A(d) = 0`, so the cap cross-terms
  vanish and the diagonal Gram blocks have the target value.
- Uniform difference multiplicities cancel every off-diagonal finite-band
  block.
- Expanding the even group-ring element
  `δ = 2D - G + 1` yields the regular Paley-type partial-difference-set
  parameters and forces `n ≡ 1 (mod 4)`.
- Normalizing the difference matrix by its zero row yields `n-1`
  group-developed mutually orthogonal Latin squares; the standard completion
  gives a projective plane of order `n`.

The earlier exhaustive checks recorded in `AUDIT_LEDGER.md` cover all 243 sign
functions at `n = 5`, representative cases at `n = 9` and `13`, and all
90,000 normalized `(Z₅,5;1)` difference matrices. They agree with the proof.

## Theorem 3 and equivalence claims

- The map from Gaussian units to `2 × 2` real blocks respects multiplication
  and conjugate transpose, so `BH(n,4)` orthogonality is equivalent to real
  Hadamard orthogonality after doubling.
- `code/gaussian_c30.py` checks the `q = 5` instance and its entrywise double.
- The row-quadruple statistic is stated and proved invariant before it is used.
  Exact scripts cover the order-60, order-180, and Gaussian comparisons.
- The README and paper both limit the `q = 5` claim to Farouk–Wang's printed
  representative and label the broader `alpha_family.py` result unrefereed.

## Cross-surface reconciliation

| Topic | Paper | README/code | Verdict |
|---|---|---|---|
| Order family | Prior existence credited to Farouk–Wang | Same | Consistent |
| New contribution | Formula, bounded converse claim, Gaussian structure | Same, in plainer language | Consistent |
| Coverage | Restricted failures through `q = 2969`, not open orders | Same corrected range | Consistent |
| Computation | Full exact checks distinguished from sampled large-order checks | Same commands and caveat | Consistent |
| Visual evidence | Two order-60 figures are illustrative; profile is the certificate | Same | Consistent |
| AI role | Assistance and reruns disclosed; not treated as validation | Same | Consistent |

## Findings resolved during this gate

- Corrected the README's last coverage-table value from `2917` to `2969`.
- Corrected Appendix equation `(C.1)` to `(A.1)`.
- Repaired the used figure's output path and verified byte-identical output.
- Changed the Farouk–Wang parser so either row or column Gram failure aborts
  before writing the reconstructed matrix.
- Replaced inaccessible bitmap text fonts in the PDF build; the release PDF
  now contains only embedded Type 1 fonts and a readable text layer.
- Reconciled all bibliography keys: 37 cited keys and 37 bibliography entries.

## Residual limits

- The literature-dependent novelty judgment belongs to P1 and remains bounded.
- Sampled checks at `q = 81` and `125` are not exhaustive.
- Historical computations described only in `AUDIT_LEDGER.md` are not promoted
  to release evidence unless a maintained script or proof covers them.
- No audit substitutes for independent expert review.
