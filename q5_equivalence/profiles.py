"""4-profile invariant comparison for two order-60 Hadamard matrices.

For each unordered quadruple of rows {i,j,k,l}, the value
|sum_c H[i,c]H[j,c]H[k,c]H[l,c]| is invariant under column permutation,
column negation (absolute value kills the sign ambiguity? no --) ...

Careful: column negation multiplies each term by d_c and does NOT preserve
the sum in general. Correct invariance argument: row negation flips the
sign of the sum for a quadruple containing the negated row (abs kills it);
column permutation permutes summands (invariant); column negation D2:
H -> H D2 changes term c by d_c^4 = +1, so the sum is invariant. Row
permutation permutes quadruples. So the multiset of absolute quadruple
sums IS a Hadamard-equivalence invariant of the row set. Same applied to
H^T gives the column profile.
"""
import os
import sys
from collections import Counter
import numpy as np

def load(path):
    H = np.loadtxt(path, dtype=np.int64)
    assert H.shape == (60, 60) and set(np.unique(H)) <= {-1, 1}
    assert np.array_equal(H @ H.T, 60 * np.eye(60, dtype=np.int64))
    return H

def profile4(H):
    """Multiset (Counter) of |4-row correlations| over all C(60,4) quadruples."""
    n = H.shape[0]
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    pair_idx = {p: t for t, p in enumerate(pairs)}
    V = np.array([H[i] * H[j] for i, j in pairs], dtype=np.int64)  # 1770 x 60
    S = V @ V.T  # 1770 x 1770
    c = Counter()
    # harvest each quadruple i<j<k<l once via pairing ({i,j},{k,l})
    for a, (i, j) in enumerate(pairs):
        for k in range(j + 1, n):
            for l in range(k + 1, n):
                c[abs(int(S[a, pair_idx[(k, l)]]))] += 1
    total = sum(c.values())
    assert total == 487635, total
    return c

def fmt(c):
    return " ".join(f"{v}:{c[v]}" for v in sorted(c))

if __name__ == "__main__":
    # Self-contained: read the two order-60 matrices from this directory.
    #   H_note_q5.txt : this note's q=5 construction, produced by
    #       python ps_p1mod4.py --q 5 --write q5_equivalence/H_note_q5.txt
    #   H_fw.txt      : Farouk-Wang's printed order-60 example, produced by
    #       python q5_equivalence/parse_fw.py
    SP = os.path.dirname(os.path.abspath(__file__))
    H_fw = load(f"{SP}/H_fw.txt")
    H_nt = load(f"{SP}/H_note_q5.txt")

    profs = {}
    for name, M in [("FW_rows", H_fw), ("FW_cols", H_fw.T),
                    ("NOTE_rows", H_nt), ("NOTE_cols", H_nt.T)]:
        profs[name] = profile4(M)
        print(f"{name}: {fmt(profs[name])}")

    print()
    print("FW_rows == NOTE_rows :", profs["FW_rows"] == profs["NOTE_rows"])
    print("FW_cols == NOTE_cols :", profs["FW_cols"] == profs["NOTE_cols"])
    # transpose convention: H1 ~ H2^T needs FW rows vs NOTE cols etc.
    print("FW_rows == NOTE_cols :", profs["FW_rows"] == profs["NOTE_cols"])
    print("FW_cols == NOTE_rows :", profs["FW_cols"] == profs["NOTE_rows"])

    # sanity control: random row/col permutation + negation of H_note
    rng = np.random.default_rng(20260718)
    P = rng.permutation(60); Q = rng.permutation(60)
    d1 = rng.choice([-1, 1], 60); d2 = rng.choice([-1, 1], 60)
    Hs = (d1[:, None] * H_nt)[P][:, Q] * d2[None, :]
    assert np.array_equal(Hs @ Hs.T, 60 * np.eye(60, dtype=np.int64))
    print("control scrambled-NOTE rows == NOTE rows:", profile4(Hs) == profs["NOTE_rows"])
    print("control scrambled-NOTE cols == NOTE cols:", profile4(Hs.T) == profs["NOTE_cols"])
    np.savetxt(f"{SP}/H_note_scrambled.txt", Hs, fmt="%d")
