# A choice-free Paley–II construction of Hadamard matrices

This repository gives an explicit formula for a real Hadamard matrix of order

```text
N = 2q(q + 1)
```

for every prime power `q ≡ 1 (mod 4)`. A Hadamard matrix is a square matrix of
`+1` and `−1` entries whose rows are pairwise orthogonal.

The existence of matrices at these orders was proved by Farouk and Wang in
2020. The contribution here is a different construction: their procedure
starts from an input Hadamard matrix and a chosen bijection, while this one
writes the matrix directly from the quadratic character of the finite field
`𝔽_q`. It makes no auxiliary choices and produces one canonical matrix for
each `q`.

> **Main result.** If `q ≡ 1 (mod 4)` is a prime power, then the formula in the
> paper produces a Hadamard matrix of order `2q(q + 1)`.

The complete proof is in [the paper](paper/main.pdf); its source is
[paper/main.tex](paper/main.tex).

## Release status

Version `0.1.0` is a release candidate and is **not yet admitted**. The three
pre-freeze gates have passed, but no immutable tag, verified public archive, or
permanent citation is available yet. Use the eventual tagged archive—not this
moving branch—for citation.

## What is new—and what is not

The order family is not new. Farouk and Wang already constructed Hadamard
matrices of order `2q(q + 1)` from Paley–II seeds [FW2020, FW2022]. The paper
makes three narrower contributions:

1. **A closed formula.** The finite bands are given entry by entry as
   `ψ(χ(y − x − t))`, where `χ` is the quadratic character and `ψ` replaces
   `0, +1, −1` by the standard `2 × 2` Paley–II blocks. Orthogonality follows
   from four block-Gram identities rather than from an input matrix.
2. **A converse theorem.** On a finite abelian group, the generalized formula
   is Hadamard exactly when its two ingredients are a Paley-type function and
   a `(G,n;1)` difference matrix. The forward construction was already known
   in greater generality; the claimed new part is that both conditions are
   necessary.
3. **A structural reading.** The real matrix is the Turyn double of a Butson
   matrix over the Gaussian units. That Butson matrix is equivalent to an
   output of the complex Scarpis lift of Sargent, Lee, and Rushall (2024).

At `q = 5`, the matrix produced here is not Hadamard-equivalent to the
order-60 matrix printed by Farouk and Wang. This does not separate it from
their whole family: their construction depends on choices, and an exact but
not independently refereed computation finds that another choice gives the
matrix constructed here. Equivalence beyond `q = 5` remains open.

## The two order-60 matrices

![The matrix constructed here beside Farouk–Wang's printed order-60 example](paper/images/q5_side_by_side.png)

The matrix from this paper is on the left. Its finite bands show the diagonal
pattern of the shifts `ψ(χ(y − x − ar))`; the printed Farouk–Wang example is on
the right. The visual difference is only an illustration. The mathematical
inequivalence certificate is the row-quadruple correlation multiset: the
value `28` occurs for 400 quadruples in the printed Farouk–Wang matrix and for
none in the matrix on the left. The comparison was also run after transposing
the matrices.

## How the construction fits together

The matrix `H` contains one cap band `M∞` and one finite band `M_r` for every
`r ∈ 𝔽_q`:

```text
H = [ M∞ ; M_r (r ∈ 𝔽_q) ],       M_r = [ B_r | K_ar (a ∈ 𝔽_q) ].
```

- `K_t` is a `2q × 2q` matrix of shifted Paley–II blocks:
  `K_t[x,y] = ψ(χ(y − x − t))`.
- `B_r` is a rank-two border block. Its Gram contribution cancels the
  repeated-row contribution from the family of `K_ar` blocks.
- `M∞` comes from the Paley–II matrix of order `2(q + 1)`. A fixed rotation of
  its column pairs makes the cap orthogonal to every finite band.

The proof computes the four possible block-Gram products and concludes that
`HHᵀ = 2q(q + 1)I`.

For `q = 5`, the colored regions below show the cap, border, and finite blocks
in the resulting order-60 matrix.

![Block structure of the order-60 matrix for q=5](paper/images/structure_q5_N60.png)

## Evidence and its limits

The repository separates four kinds of support:

- **Proof:** The paper proves the main construction, the generalized
  characterization, and its corollaries.
- **Exact computation:** The code checks the construction at selected prime
  powers, reproduces the matrix-comparison invariants, and regenerates the
  coverage calculations and figures.
- **Literature:** The existence theorem, the sufficiency direction of the
  generalized construction, and several coverage witnesses are credited to
  earlier work.
- **Exploration:** The list of orders not found by the restricted coverage
  screen is not a list of open Hadamard orders.

Important limitations remain:

- This construction does not settle a previously open Hadamard order.
- The claim of novelty for the converse theorem is bounded by the literature
  search recorded in the repository; it is not a claim of global priority.
- Sampled checks at large orders test selected row pairs. They are supporting
  computations, not substitutes for the proof.
- Process-separated AI audits can find mistakes, but they are not peer review
  or independent expert validation.

## Reproduce the main check

Requirements are Python 3 and NumPy. Matplotlib is needed only to regenerate
figures. For the pinned release environment:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

From the repository root, run:

```bash
cd code
python3 ps_p1mod4.py
```

The default sweep uses `q = 5, 9, 13, 17, 25, 29, 37, 41, 49` and checks
`HHᵀ = NI` entry by entry. It prints `ALL PASS` and exits with status `0` when
every case succeeds. The extension-field path is exercised by `q = 9, 25, 49`.

Other documented checks are:

```bash
cd code
python3 coverage_table.py
python3 paley_patterns_q9.py
python3 alpha_family.py
python3 nearfield_q9.py
python3 gaussian_c30.py
cd q5_equivalence
python3 profiles.py
```

The order-180 profile in `nearfield_q9.py` checks all `C(180,4) = 42,296,805`
row quadruples. Its faster vectorized routine is first compared with a direct
implementation at order 60.

To regenerate the figures:

```bash
cd code
python3 ps_p1mod4.py --figures ../paper/images --figq 5,9,13
```

To export the `q = 5` matrix as compact signs:

```bash
cd code
python3 ps_p1mod4.py --q 5 --write - --which H --fmt signs
```

See [code/README.md](code/README.md) for each script's scope and expected
output.

## Repository map

- `paper/main.tex` and `paper/main.pdf` — definitions, proofs, comparison with
  prior constructions, open problems, and coverage appendix.
- `paper/images/` — the explanatory figures, all regenerable from the code.
- `code/README.md` — commands, dependencies, and the scope of every check.
- `code/ps_p1mod4.py` — construction, finite-field arithmetic, verification,
  export, and figure generation.
- `code/q5_equivalence/` — exact comparison with the printed Farouk–Wang
  order-60 matrix, including a positive control.
- `code/alpha_family.py` — the explicitly unrefereed `q = 5` comparison with
  all choices in the Farouk–Wang procedure.
- `code/paley_patterns_q9.py` — exact enumeration of Paley-type sign patterns
  on the additive group of `GF(9)`.
- `code/coverage_table.py` — coverage table and restricted witness screen.
- `code/nearfield_q9.py` — the order-180 nearfield comparison.
- `code/gaussian_c30.py` — the Gaussian/Butson construction at `q = 5`.
- `audit/PRIOR_WORK.md` and `audit/CONSISTENCY.md` — the bounded literature
  corpus and the claim/proof/code consistency gate.
- `ADMISSION.md`, `VERIFICATION.md`, and `MANIFEST.sha256` — live gate verdict,
  exact rerun record, and frozen file hashes.
- `CITATION.cff`, `CORRECTIONS.md`, `NOTICE`, and `LICENSE` — citation,
  stewardship, provenance, and licensing surfaces.
- `AUDIT_LEDGER.md` — the historical claim and computation audit record.

## Coverage

Every order in the family has the form
`2q(q + 1) = 4q(q + 1)/2`, with an odd composite part. The paper checks the
initial range against published Hadamard-order tables rather than inferring
coverage from that factorization. All family members whose odd part is at
most `3000` were already known. The next case, `q = 81` and order `13284`, has
a classical Turyn-product witness.

The appendix also records all failures of a deliberately restricted elementary
screen for `q < 3000`; the last listed case is `q = 2969`. Those entries are
unaudited, and they are not asserted to be open.

## AI assistance and responsibility

Large language models substantially assisted with the mathematics, code,
exposition, and adversarial checks. Their agreement is evidence about the
checking process, not a certificate of correctness. Jeffery Kline directs the
work, is responsible for the claims released under his name, and will record
material corrections or withdrawals in the public history.

## Citation

There is not yet a stable release to cite. Until an immutable archive is
published, reference the living repository and include the commit hash you
used:

```bibtex
@misc{kline2026p1mod4,
  author       = {Kline, Jeffery},
  title        = {A Paley--II analogue of the Scarpis--\DJ okovi\'c construction
                  for prime powers q congruent to 1 modulo 4},
  year         = {2026},
  howpublished = {GitHub repository},
  url          = {https://github.com/jeff-kline/p1mod4},
  note         = {Release candidate; cite the commit hash used}
}
```

## References

- **FW2020:** A. Farouk and Q.-W. Wang, “An infinite family of Hadamard
  matrices constructed from Paley type matrices,” *Filomat* 34 (2020), no. 3,
  815–834. [doi:10.2298/FIL2003815F](https://doi.org/10.2298/FIL2003815F)
- **FW2022:** A. Farouk and Q.-W. Wang, “Construction of new Hadamard matrices
  using known Hadamard matrices,” *Filomat* 36 (2022), no. 6, 2025–2042.
  [doi:10.2298/FIL2206025F](https://doi.org/10.2298/FIL2206025F)

The full bibliography, including Paley, Scarpis, Đoković, Seberry, Nuñez
Ponasso, Turyn, and Sargent–Lee–Rushall, is in
[paper/main.tex](paper/main.tex).

## License

Original text, code, and figures in this repository are copyright 2026
Jeffery Kline and are licensed under the GNU General Public License v3.0 only;
see [LICENSE](LICENSE). The Farouk–Wang source extract and reconstructed matrix
in `code/q5_equivalence/` retain their cited provenance and any rights that
apply to the source publication.
