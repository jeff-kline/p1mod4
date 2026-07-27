#!/usr/bin/env python3
"""Reproduce Theorem 3 and Remark 13 (rem:c30) at q = 5.

Theorem 3 says the construction factors through a Butson matrix
Gamma in BH(q(q+1), 4) whose Turyn double is H, i.e. H = phi(Gamma).
Remark 13 says Gamma is not the classical Butson matrix of its order: at
q = 5 both Gamma and Turyn's C_30 + iI lie in BH(30,4), and they are
inequivalent.

The invariant used is the multiset of

    |sum_c g[i,c] conj(g[j,c]) g[k,c] conj(g[l,c])|^2

over ordered quadruples of distinct rows -- invariant under row and column
permutations, multiplication of rows and columns by fourth roots of unity,
and complex conjugation.  The paper's claim: it takes the value 500 on 240
quadruples for Gamma and on none for C_30 + iI, in both orientations.

    python gaussian_c30.py

Checked here as well: Gamma is Butson, C_30 + iI is Butson, and
phi(Gamma) is entrywise equal to the order-60 matrix of Theorem 1.
"""

import sys
from collections import Counter

import numpy as np

from ps_p1mod4 import GF, PaleyScarpis, psi

# the 2x2 blocks of section 2
P = np.array([[1, 1], [1, -1]], dtype=np.int64)
Z = np.array([[1, -1], [-1, -1]], dtype=np.int64)
R = np.array([[0, -1], [1, 0]], dtype=np.int64)


def rho(w):
    """The real 2x2 representation of Z[i]: rho(a+bi) = a*I + b*R."""
    a, b = int(round(w.real)), int(round(w.imag))
    return a * np.eye(2, dtype=np.int64) + b * R


def phi(w):
    """phi(w) = rho(w) P.  phi(1)=P, phi(-1)=-P, phi(i)=-Z, phi(-i)=Z."""
    return rho(w) @ P


def phi_matrix(G):
    """The Turyn double: replace each entry by its 2x2 block phi(.)."""
    n = G.shape[0]
    out = np.empty((2 * n, 2 * n), dtype=np.int64)
    for u in range(n):
        for v in range(n):
            out[2 * u:2 * u + 2, 2 * v:2 * v + 2] = phi(G[u, v])
    return out


# ------------------------------------------------------------------- matrices
def gamma(q):
    """Gamma of Theorem 3.  Rows and columns are indexed by F followed by
    F x F (in both cases the pair index is major-then-minor)."""
    F = GF(q)
    n = q * (q + 1)

    def e(z):
        """e(z) = chi(z) for z != 0, and e(0) = -i."""
        c = F.chi[z]
        return complex(c) if c != 0 else -1j

    def col(idx):
        return ("fin", idx) if idx < q else ("pair", (idx - q) // q, (idx - q) % q)

    G = np.zeros((n, n), dtype=complex)
    for ri in range(n):
        rk = col(ri)
        for ci in range(n):
            ck = col(ci)
            if rk[0] == "fin" and ck[0] == "fin":
                G[ri, ci] = 1
            elif rk[0] == "fin" and ck[0] == "pair":
                x, a = rk[1], ck[1]
                G[ri, ci] = -1j * e(F.sub(a, x))
            elif rk[0] == "pair" and ck[0] == "fin":
                r, y = rk[1], ck[1]
                G[ri, ci] = e(F.sub(y, r))
            else:
                r, x = rk[1], rk[2]
                a, y = ck[1], ck[2]
                G[ri, ci] = e(F.sub(F.sub(y, x), F.mul(a, r)))
    return G


def turyn_conference(p):
    """C + iI, where C is the Paley conference matrix of order p+1 indexed by
    {infinity} union F_p (C[u,u] = 0, C[inf,x] = C[x,inf] = 1,
    C[x,y] = chi(y-x)).  For p = 1 mod 4 this is a Butson matrix."""
    F = GF(p)
    n = p + 1
    C = np.zeros((n, n), dtype=complex)
    for x in range(p):
        C[p, x] = 1
        C[x, p] = 1
        for y in range(p):
            C[x, y] = F.chi[F.sub(y, x)]
    return C + 1j * np.eye(n)


# ------------------------------------------------------------------ invariant
def quad_profile(G):
    """Multiset of |sum_c g[i,c] conj(g[j,c]) g[k,c] conj(g[l,c])|^2 over
    ordered quadruples of four distinct rows.

    Writing A[(i,j)] = row_i * conj(row_j) elementwise, the sum is the plain
    (unconjugated) inner product of A[(i,j)] with A[(k,l)]."""
    n = G.shape[0]
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    idx = {p: t for t, p in enumerate(pairs)}
    A = np.array([G[i] * np.conj(G[j]) for i, j in pairs])
    S = A @ A.T                       # no conjugation on the second factor
    c = Counter()
    for (i, j), a in idx.items():
        for (k, l), b in idx.items():
            if k in (i, j) or l in (i, j):
                continue
            c[int(round(abs(S[a, b]) ** 2))] += 1
    return c


def is_butson(G, n, m=4):
    """Entries are m-th roots of unity and G G* = n I."""
    roots = {1 + 0j, -1 + 0j, 1j, -1j}
    ok_entries = all(min(abs(v - r) for r in roots) < 1e-9 for v in G.ravel())
    return ok_entries and np.allclose(G @ G.conj().T, n * np.eye(n), atol=1e-8)


# ------------------------------------------------------------------------ main
def main():
    q, n = 5, 30
    fails = []

    def check(ok, label, got, want=None):
        print(f"[{'OK ' if ok else 'FAIL'}] {label}: {got}"
              + ("" if ok or want is None else f"   (expected {want})"))
        if not ok:
            fails.append(label)

    print("Theorem 3 at q = 5")
    G = gamma(q)
    check(is_butson(G, n), "  Gamma is in BH(30,4)", True)

    # phi(Gamma) must be the order-60 matrix of Theorem 1, entry for entry
    ps = PaleyScarpis(q)
    rows = [ps.cap_row(e, al) for e in range(q) for al in range(2)]
    for r in range(q):
        for x in range(q):
            for ap in range(2):
                rows.append(ps.finite_row(r, x, ap))
    H = np.array(rows, dtype=np.int64)
    PG = phi_matrix(G)
    check(np.array_equal(PG, H), "  phi(Gamma) == H of Theorem 1, entrywise",
          "identical" if np.array_equal(PG, H) else "DIFFER")

    print("\nRemark 13: Gamma vs Turyn's C_30 + iI")
    T = turyn_conference(29)
    check(is_butson(T, n), "  C_30 + iI is in BH(30,4)", True)

    profiles = {}
    for name, M in (("Gamma", G), ("C_30+iI", T)):
        for orient, X in (("rows", M), ("cols", M.T)):
            p = quad_profile(X)
            profiles[(name, orient)] = p
            tot = sum(p.values())
            print(f"    {name:>8} {orient}: total={tot}  count[500]={p.get(500, 0)}"
                  f"   {' '.join(f'{v}:{k}' for v, k in sorted(p.items())[:5])} ...")
            if tot != 30 * 29 * 28 * 27:
                fails.append(f"{name}/{orient} total")

    check(profiles[("Gamma", "rows")].get(500, 0) == 240,
          "  Gamma attains 500 on", profiles[("Gamma", "rows")].get(500, 0), 240)
    for orient in ("rows", "cols"):
        check(profiles[("C_30+iI", orient)].get(500, 0) == 0,
              f"  C_30+iI attains 500 on ({orient})",
              profiles[("C_30+iI", orient)].get(500, 0), 0)

    print("\n  inequivalence in both orientations:")
    allne = True
    for oa in ("rows", "cols"):
        for ob in ("rows", "cols"):
            eq = profiles[("Gamma", oa)] == profiles[("C_30+iI", ob)]
            allne &= not eq
            print(f"    Gamma {oa} == C_30+iI {ob} : {eq}")
    check(allne, "  all comparisons differ", allne, True)

    print()
    if fails:
        print(f"FAILED: {len(fails)} check(s): {fails}")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
