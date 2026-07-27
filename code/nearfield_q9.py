#!/usr/bin/env python3
"""Reproduce Remark 11 (rem:q9): the q = 9 nearfield matrix of order 180.

Theorem 2 says fixing q does not fix the matrix.  At q = 9 the delta-slot is
rigid but the T-slot is not: besides T(r,a) = a*r over F_9 there is the
Dickson nearfield product

    r o a = r*a      (r a square),        r o a = r*a^3    (r a non-square),

and a |-> r o a is additive, with r o a - s o a vanishing only at a = 0 for
r != s.  So T(r,a) = r o a is a (Z_3^2, 9; 1)-difference matrix and Theorem 2
yields a second Hadamard matrix of order 180.  This script builds both and
shows they are inequivalent, via the multiset of |4-row correlations| -- an
invariant of Hadamard equivalence.

The paper's claim: over the C(180,4) = 42,296,805 row quadruples the value 44
is attained on 112,752 quadruples for the nearfield matrix and on none for
the matrix of Theorem 1, in all four row/column orientations.

    python nearfield_q9.py

The fast profile routine is validated against a direct O(n^4) reference at
q = 5 (order 60) before being used at order 180, and the q = 5 row profile is
checked against the value recorded in q5_equivalence/profile_results.txt.
"""

import sys
from collections import Counter

import numpy as np

from ps_p1mod4 import GF, PaleyScarpis


# --------------------------------------------------------------- construction
class NearfieldScarpis(PaleyScarpis):
    """The construction of Theorem 2 with T(r,a) = r o a, the Dickson
    nearfield product, in place of T(r,a) = a*r.

    Only the T-slot changes; the cap band M_infty does not depend on T, so
    cap_row is inherited unchanged."""

    def _cube(self, a):
        F = self.F
        return F.mul(F.mul(a, a), a)

    def nearfield_mul(self, r, a):
        """r o a.  chi(r) == -1 marks r a non-square; r = 0 (chi = 0) and r a
        square both take the ordinary product."""
        F = self.F
        if F.chi[r] == -1:
            return F.mul(r, self._cube(a))
        return F.mul(r, a)

    def finite_row(self, r, x, ap):
        q, F = self.q, self.F
        parts = [self._strip(r)[ap]]                 # border block B_r
        for a in range(q):                           # block a = K_{T(r,a)}
            t = F.add(x, self.nearfield_mul(r, a))
            parts.append(self._strip(t)[ap])
        return np.concatenate(parts)


def build(ps):
    """Assemble H from the documented row API: cap band, then finite bands."""
    q, N = ps.q, ps.N
    rows = [ps.cap_row(e, alpha) for e in range(q) for alpha in range(2)]
    for r in range(q):
        for x in range(q):
            for ap in range(2):
                rows.append(ps.finite_row(r, x, ap))
    H = np.array(rows, dtype=np.int8)
    assert H.shape == (N, N)
    return H


def check_difference_matrix(ps):
    """T(r,a) = r o a is a (G, n; 1)-difference matrix: for r != s the map
    a |-> T(r,a) - T(s,a) is a bijection of G."""
    q, F = ps.q, ps.F
    for r in range(q):
        for s in range(q):
            if r == s:
                continue
            img = {F.sub(ps.nearfield_mul(r, a), ps.nearfield_mul(s, a))
                   for a in range(q)}
            if len(img) != q:
                return False
    return True


# ------------------------------------------------------------------- profiles
def _pair_index(n):
    """Pairs (i,j), i<j, in lexicographic order, plus start[i] = index of the
    first pair whose first element is i (start[n] = number of pairs)."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    start = np.zeros(n + 1, dtype=np.int64)
    k = 0
    for i in range(n):
        start[i] = k
        k += n - 1 - i
    start[n] = k
    return pairs, start


def profile4_reference(H):
    """Direct O(n^4) multiset of |4-row correlations|.  Reference only."""
    n = H.shape[0]
    pairs, _ = _pair_index(n)
    idx = {p: t for t, p in enumerate(pairs)}
    V = np.array([H[i].astype(np.int64) * H[j].astype(np.int64) for i, j in pairs])
    S = V @ V.T
    c = Counter()
    for a, (i, j) in enumerate(pairs):
        for k in range(j + 1, n):
            for l in range(k + 1, n):
                c[abs(int(S[a, idx[(k, l)]]))] += 1
    return c


def profile4(H, chunk=1024):
    """Same multiset, vectorized.  Each 4-subset i<j<k<l is harvested once via
    the pairing ({i,j},{k,l}); because pairs are lexicographic, the admissible
    partners of (i,j) are exactly the contiguous suffix starting at start[j+1].

    Entries are +-1 and n <= 2^24, so the float32 products are exact."""
    n = H.shape[0]
    pairs, start = _pair_index(n)
    npairs = len(pairs)
    V = np.empty((npairs, n), dtype=np.float32)
    for t, (i, j) in enumerate(pairs):
        V[t] = H[i] * H[j]
    js = np.array([j for _, j in pairs], dtype=np.int64)
    hist = np.zeros(n + 1, dtype=np.int64)
    for c0 in range(0, npairs, chunk):
        c1 = min(c0 + chunk, npairs)
        S = np.abs(V[c0:c1] @ V.T).astype(np.int32)
        for a in range(c1 - c0):
            seg = S[a, start[js[c0 + a] + 1]:]
            if seg.size:
                hist += np.bincount(seg, minlength=n + 1)
    return Counter({v: int(hist[v]) for v in range(n + 1) if hist[v]})


def fmt(c, top=6):
    items = sorted(c.items())
    return " ".join(f"{v}:{k}" for v, k in items[:top]) + (" ..." if len(items) > top else "")


# ------------------------------------------------------------------------ main
def main():
    fails = []

    def check(ok, label, got, want=None):
        print(f"[{'OK ' if ok else 'FAIL'}] {label}: {got}"
              + ("" if ok or want is None else f"   (expected {want})"))
        if not ok:
            fails.append(label)

    # -- validate the fast profile against the reference, at order 60 -------
    print("Validation at q = 5 (order 60) -- fast path vs direct reference")
    H5 = build(PaleyScarpis(5))
    check(np.array_equal(H5.astype(np.int64) @ H5.astype(np.int64).T,
                         60 * np.eye(60, dtype=np.int64)),
          "  order-60 matrix is Hadamard", True)
    p_fast, p_ref = profile4(H5), profile4_reference(H5)
    check(p_fast == p_ref, "  fast profile == reference profile",
          "identical" if p_fast == p_ref else "DIFFER")
    check(sum(p_fast.values()) == 487635, "  quadruples counted",
          sum(p_fast.values()), 487635)
    # the value recorded in q5_equivalence/profile_results.txt as NOTE_rows
    expected_q5 = {4: 359000, 12: 103125, 20: 25510}
    check(dict(p_fast) == expected_q5, "  matches recorded NOTE_rows",
          fmt(p_fast), "4:359000 12:103125 20:25510")

    # -- q = 9 -------------------------------------------------------------
    print("\nq = 9: the two order-180 matrices")
    ps_field = PaleyScarpis(9)
    ps_near = NearfieldScarpis(9)
    check(check_difference_matrix(ps_near),
          "  T(r,a) = r o a is a (Z_3^2, 9; 1)-difference matrix", True)

    H_field, H_near = build(ps_field), build(ps_near)
    for name, H in (("Theorem 1", H_field), ("nearfield", H_near)):
        G = H.astype(np.int64) @ H.astype(np.int64).T
        check(np.array_equal(G, 180 * np.eye(180, dtype=np.int64)),
              f"  {name} matrix is Hadamard of order 180", True)
    check(not np.array_equal(H_field, H_near),
          "  the two matrices differ entrywise", True)

    print("\n4-profiles over C(180,4) = 42,296,805 quadruples")
    profiles = {}
    for name, H in (("Theorem 1", H_field), ("nearfield", H_near)):
        for orient, M in (("rows", H), ("cols", H.T)):
            p = profile4(M)
            profiles[(name, orient)] = p
            tot = sum(p.values())
            print(f"    {name:>9} {orient}: total={tot}  count[44]={p.get(44, 0)}"
                  f"   {fmt(p)}")
            if tot != 42296805:
                fails.append(f"{name}/{orient} total")

    check(profiles[("nearfield", "rows")].get(44, 0) == 112752,
          "  nearfield attains 44 on", profiles[("nearfield", "rows")].get(44, 0), 112752)
    check(profiles[("Theorem 1", "rows")].get(44, 0) == 0,
          "  Theorem 1 attains 44 on", profiles[("Theorem 1", "rows")].get(44, 0), 0)

    print("\n  inequivalence in all four row/column orientations:")
    allne = True
    for oa in ("rows", "cols"):
        for ob in ("rows", "cols"):
            eq = profiles[("nearfield", oa)] == profiles[("Theorem 1", ob)]
            allne &= not eq
            print(f"    nearfield {oa} == Theorem 1 {ob} : {eq}")
    check(allne, "  all four comparisons differ", allne, True)

    print()
    if fails:
        print(f"FAILED: {len(fails)} check(s): {fails}")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
