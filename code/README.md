# code

Verification code for the paper in [`../paper/main.tex`](../paper/main.tex).
Every script here re-derives numbers that the paper states as computed, and
exits nonzero if any of them disagrees. Requires Python 3 and `numpy`
(`matplotlib` only for the figures).

| Script | Covers | Checks |
|---|---|---|
| `ps_p1mod4.py` | Theorem 1 | The construction itself, plus a small finite-field layer so extension fields (`q = 9, 25, 49, 81, 125`) work. Full Gram `HHᵀ = N·I` for `q ≤ 49`; streamed sampled row-orthogonality above that. Also exports matrices and regenerates the figures. |
| `coverage_table.py` | Appendix A | The audited range, and the elementary-witness screen: 232 orders, 128 covered, 104 without a witness, smallest failure `q = 109`. `--table` prints the 104 rows. |
| `nearfield_q9.py` | Remark 11 | The `q = 9` Dickson-nearfield matrix of order 180 and its inequivalence to the matrix of Theorem 1, over all `C(180,4) = 42,296,805` row quadruples. |
| `gaussian_c30.py` | Theorem 3, Remark 13 | `Γ ∈ BH(30,4)`, that `φ(Γ)` is the order-60 matrix entrywise, and inequivalence to Turyn's `C₃₀ + iI`. |
| `q5_equivalence/` | §4 | The `q = 5` comparison against the order-60 example printed by Farouk–Wang, including a positive control. See its own README. |

## Run everything

```bash
cd code
python ps_p1mod4.py          # default sweep, full Gram      -> ALL PASS
python coverage_table.py     # Appendix A                    -> ALL PASS
python nearfield_q9.py       # Remark 11 (about 8 seconds)   -> ALL PASS
python gaussian_c30.py       # Theorem 3 + Remark 13         -> ALL PASS
cd q5_equivalence && python profiles.py
```

Common flags on `ps_p1mod4.py`:

```bash
python ps_p1mod4.py --q 81 --sampled --pairs 5000        # headline order 13284
python ps_p1mod4.py --big                                # add q=81 to the sweep
python ps_p1mod4.py --figures ../paper/images --figq 5,9,13
python ps_p1mod4.py --q 5 --write - --which H --fmt signs
```

## A note on trusting the fast paths

Two of these scripts replace an obvious `O(n⁴)` computation with a vectorized
one. In both cases the fast path is validated against a direct reference at a
size where the reference is affordable, *before* being used at the size that
matters: `nearfield_q9.py` checks its profile routine against an explicit
quadruple loop at order 60, and against the recorded `q = 5` profile in
`q5_equivalence/profile_results.txt`, before running at order 180.
