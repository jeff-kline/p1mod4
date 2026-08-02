# q5_equivalence — evidence for the q = 5 inequivalence claim

Backs the claim (paper §4, Figure 1; README top): at `q = 5`, the matrix of
Theorem 1 is **not Hadamard-equivalent** to the order-60 example printed in
the appendix of Farouk & Wang, Filomat 34:3 (2020) 815–834.

Contents:

- `H_note_q5.txt` — this note's q=5 matrix; regenerate with
  `cd .. && python3 ps_p1mod4.py --q 5 --write q5_equivalence/H_note_q5.txt`.
- `fw_appendix.txt` — plain-text extraction of the printed order-60 example
  from the published Farouk–Wang PDF (see `parse_fw.py` docstring for the
  exact `pdftotext` recipe).
- `parse_fw.py` — rebuilds and validates `H_fw.txt` from `fw_appendix.txt`
  (the reconstruction must satisfy `M·Mᵀ = 60·I` exactly, so a transcription
  error would be detected).
- `H_fw.txt` — the validated Farouk–Wang matrix.
- `profiles.py` — the inequivalence proof: computes the 4-profile (the
  multiset of `|Σ_c h_ic·h_jc·h_kc·h_lc|` over all C(60,4) row quadruples,
  an invariant of Hadamard equivalence), compares all row/column
  orientations (covering the transpose convention), and runs a positive
  control (a random signed permutation of the note's matrix, which must —
  and does — reproduce its profile). Writes the control to
  `H_note_scrambled.txt` (gitignored).
- `profile_results.txt` — captured output: the profiles differ (their matrix
  has 400 quadruples with value 28; ours has none) ⇒ inequivalent.
- `make_side_by_side.py` — regenerates
  `../../paper/images/q5_side_by_side.png`.

Caveat, stated precisely: Farouk–Wang note their construction's output may
vary with a choice of bijection α, so this establishes inequivalence to their
*published* example, not to every output their procedure could produce.
