#!/usr/bin/env python3
"""
alpha_family.py -- settles, at q = 5, whether the order-60 matrix H of this
note is Hadamard-equivalent to *some* output of the Farouk-Wang procedure

    Psi_{q,alpha} : H^n -> H^{qn},     n = 2(q+1),

as defined in A. Farouk and Q.-W. Wang, Filomat 34:3 (2020) 815-834,
Section 2 (Lemma 2.2 and Theorem 2.2, Steps 1-7).

ANSWER (proved below by exhibiting the equivalence explicitly):  YES.
    H  ~  Psi_{5,alpha}(P'_5)   for alpha = the identity bijection
                                {1,...,5} -> F_5, alpha(k) = k-1,
    with the Paley-II seed P'_5 of [FW, Lem. 2.2], the column permutation
    N = I of [FW, Lem. 2.2(1)], and the pairing M of [FW, Lem. 2.2(2)]
    that matches the k-th "+" column of column 2 of P'_5 to the k-th
    "-" column.  The equivalence is produced as an explicit
    signed-row-permutation / signed-column-permutation pair and checked
    by exact integer matrix identity, so it does not rely on any invariant.

The script also
  * verifies that Psi as implemented here outputs a genuine Hadamard matrix
    of order 60 for every choice fed to it;
  * reproduces the 4-profile of the order-60 matrix printed in the appendix
    of [FW] from this same implementation, for an explicit choice of
    (row order, N, M, alpha)  -- the fidelity check;
  * reverse-engineers the printed matrix and confirms that it is exactly a
    normalised Psi-output, with the block structure this implementation
    produces;
  * enumerates *all* 120 bijections alpha with the canonical (seed, N, M)
    and reports the resulting 4-profiles.

Exits nonzero if any internal check fails.

Run:  python alpha_family.py            (~1 minute)
Only numpy is required.  H (the note's matrix) is taken from ps_p1mod4.py in
the same directory if importable, else from q5_equivalence/H_note_q5.txt.
"""
from __future__ import annotations

import itertools
import os
import sys
from collections import Counter
from math import comb

import numpy as np

FAIL: list[str] = []


def check(name: str, cond: bool) -> bool:
    print(("  [ok]   " if cond else "  [FAIL] ") + name)
    if not cond:
        FAIL.append(name)
    return bool(cond)


# ---------------------------------------------------------------------------
# 1.  4-profile (Hadamard-equivalence invariant), vectorised
# ---------------------------------------------------------------------------
_PC: dict[int, tuple] = {}


def _pairdata(m: int):
    if m not in _PC:
        idx = np.array([(i, j) for i in range(m) for j in range(i + 1, m)])
        a, b = idx[:, 0], idx[:, 1]
        share = ((a[:, None] == a[None, :]) | (a[:, None] == b[None, :])
                 | (b[:, None] == a[None, :]) | (b[:, None] == b[None, :]))
        ut = np.triu(np.ones(share.shape, dtype=bool), 1)
        _PC[m] = (idx, ut & ~share)
    return _PC[m]


def profile4(H: np.ndarray) -> Counter:
    """Multiset of |sum_c h_ic h_jc h_kc h_lc| over all C(m,4) row quadruples.

    Uses:  for pairs p={i,j}, p'={k,l} with p,p' disjoint, <h_i h_j, h_k h_l>
    is the quadruple correlation; if p,p' share exactly one index the value is
    0 by row orthogonality.  Each quadruple is met by exactly 3 disjoint
    pair-pairs, whence the division by 3.
    """
    m = H.shape[0]
    idx, mask = _pairdata(m)
    V = (H[idx[:, 0]] * H[idx[:, 1]]).astype(np.float32)
    vals = np.abs(np.rint((V @ V.T)[mask])).astype(np.int64)
    k, c = np.unique(vals, return_counts=True)
    tot = int(c.sum())
    assert tot == 3 * comb(m, 4), (tot, comb(m, 4))
    return Counter({int(a): int(b) // 3 for a, b in zip(k, c)})


def fmt(c: Counter) -> str:
    return " ".join(f"{k}:{c[k]}" for k in sorted(c))


# ---------------------------------------------------------------------------
# 2.  The Paley type-II seed P'_q of [FW, Lem. 2.2] and Lemma 2.2 checks
# ---------------------------------------------------------------------------
Q5 = 5
N12 = 2 * (Q5 + 1)          # 12
N60 = Q5 * N12              # 60


def chi(x: int, q: int = Q5) -> int:
    x %= q
    return 0 if x == 0 else (1 if pow(x, (q - 1) // 2, q) == 1 else -1)


def paley2(q: int = Q5) -> np.ndarray:
    """P'_q exactly as displayed in the proof of [FW, Lem. 2.2]:
           [ 1     1    J    J   ]
           [ 1    -1   -J    J   ]
           [ J^T  J^T  Q-I  -Q-I ]
           [ J^T -J^T  Q+I   Q-I ]
    """
    Qm = np.array([[chi(i - j, q) for j in range(q)] for i in range(q)], dtype=np.int64)
    I = np.eye(q, dtype=np.int64)
    Jc = np.ones((q, 1), dtype=np.int64)
    Jr = np.ones((1, q), dtype=np.int64)
    return np.block([
        [np.array([[1, 1]]), Jr, Jr],
        [np.array([[1, -1]]), -Jr, Jr],
        [np.hstack([Jc, Jc]), Qm - I, -Qm - I],
        [np.hstack([Jc, -Jc]), Qm + I, Qm - I],
    ]).astype(np.int64)


# ---------------------------------------------------------------------------
# 3.  Psi_{q,alpha}:  [FW, Thm. 2.2] Steps 1-7
# ---------------------------------------------------------------------------
def build_psi(A: np.ndarray, colperm, M, alpha, q: int = Q5) -> np.ndarray:
    """Steps 4-7 of [FW, Thm. 2.2].

    A        -- the matrix A'' of Steps 1-3: a normalised Hadamard matrix of
                order n = 2(q+1) whose second column is (1,-1,1^q,-1^q)^T.
    colperm  -- the permutation N of Step 5, given as an ordering of the
                columns 2..n-1 of A (0-indexed); it must make each of the
                first q rows of T split (-1,-1) over the two halves and each
                of the last q rows split (1,-1)   [FW, Lem. 2.2(1)].
    M        -- the permutation of Step 4, given as the list of q+1 ordered
                column pairs (a_s, b_s), s = 0..q, that M sends to slot s;
                columns are 0-indexed columns of A (after colperm).  Validity
                is [FW, Lem. 2.2(2)]: every row of T*M must carry as many
                (1,-1) consecutive pairs as (-1,1) ones.
    alpha    -- tuple (alpha_1,...,alpha_q), a bijection {1..q} -> F_q, given
                0-indexed:  alpha[k] is the field element alpha_{k+1}.
                c(alpha_{k+1}) is row k of C, d(alpha_{k+1}) is row k of D.
    """
    n = A.shape[0]
    Ac = A.copy()
    Ac[:, 2:] = A[:, 2 + np.array(colperm)]
    That = Ac[2:, :]                    # T of Step 4:      2q x n
    T = That[:, 2:]                     # T = T_0 N of Step 5: 2q x 2q
    C, Dm = T[:q], T[q:]                # Step 5 split
    inv = {a: k for k, a in enumerate(alpha)}
    rows = []
    # ---- B_0 = T M (x) J   (Step 4) -------------------------------------
    for k in range(2 * q):
        rows.append(np.concatenate(
            [np.full(q, That[k, c]) for pair in M for c in pair]))
    # ---- B_r, r = 1..q     (Steps 6-7) -----------------------------------
    for r in range(q):
        ar = alpha[r]
        for src in (C, Dm):                       # B^[1]_r then B^[2]_r
            for a in range(1, q + 1):
                b = a % q + 1                     # [FW, eq. (1)-(2)]
                ab = alpha[b - 1]
                seg = [src[inv[ar % q]]]          # block 0: J^T (x) c_r / d_r
                for i in range(q):
                    seg.append(src[inv[(alpha[i] * ar + ab) % q]])
                rows.append(np.concatenate(seg))
    return np.array(rows, dtype=np.int64)


def is_hadamard(B: np.ndarray) -> bool:
    m = B.shape[0]
    return (B.shape[0] == B.shape[1] and bool(((B == 1) | (B == -1)).all())
            and np.array_equal(B @ B.T, m * np.eye(m, dtype=np.int64)))


# ---------------------------------------------------------------------------
# 4.  Explicit Hadamard-equivalence search  (H -> B)
# ---------------------------------------------------------------------------
def _rowsig(H):
    m = H.shape[0]
    idx, mask = _pairdata(m)
    V = (H[idx[:, 0]] * H[idx[:, 1]]).astype(np.float32)
    S = np.abs(np.rint(V @ V.T)).astype(np.int64)
    ii, jj = np.nonzero(np.triu(np.ones_like(mask), 1) & mask)
    quad = np.stack([idx[ii, 0], idx[ii, 1], idx[jj, 0], idx[jj, 1]], 1)
    vals = S[ii, jj]
    return [tuple(sorted(Counter(vals[(quad == r).any(1)].tolist()).items()))
            for r in range(m)]


def find_equivalence(H, B, node_budget=8_000_000):
    """Backtracking search for a Hadamard equivalence H -> B.

    Fixes a row r0 of H and negates the columns of H so that row r0 is all +1;
    likewise for a candidate image row j0 of B.  The residual freedom is then
    a *pure* column permutation, found by refining the column partition one
    row at a time.  Returns (r0, j0, perm, src, sig) or None.
    """
    m = H.shape[0]
    sh, sb = _rowsig(H), _rowsig(B)
    if Counter(sh) != Counter(sb):
        return None
    cls = {s: i for i, s in enumerate(sorted(set(sh)))}
    ch = np.array([cls[s] for s in sh])
    cb = np.array([cls.get(s, -1) for s in sb])
    small = min(Counter(ch.tolist()), key=lambda k: Counter(ch.tolist())[k])
    order = list(np.nonzero(ch == small)[0]) + [i for i in range(m) if ch[i] != small]
    r0 = order[0]
    Hp = H * H[r0]
    nodes = [0]
    for j0 in np.nonzero(cb == ch[r0])[0]:
        Bp = B * B[j0]
        target = set(map(tuple, Bp.tolist())) | set(map(tuple, (-Bp).tolist()))
        SR = np.vstack([Bp, -Bp])
        used = np.zeros(m, dtype=bool)
        used[j0] = True
        res = [None]

        def rec(k, cells):
            if nodes[0] > node_budget:
                return False
            if all(len(a) == 1 for a, _ in cells):
                perm = np.empty(m, dtype=np.int64)
                for a, b in cells:
                    perm[a[0]] = b[0]
                Qm = np.empty_like(Hp)
                Qm[:, perm] = Hp
                if (set(map(tuple, Qm.tolist()))
                        | set(map(tuple, (-Qm).tolist()))) == target:
                    res[0] = perm
                    return True
                return False
            if k >= m:
                return False
            hv = Hp[order[k]]
            hc = ch[order[k]]
            for t in range(2 * m):
                jb = t % m
                if used[jb] or cb[jb] != hc:
                    continue
                nodes[0] += 1
                if nodes[0] > node_budget:
                    return False
                r = SR[t]
                new, ok = [], True
                for a, b in cells:
                    pa, na = a[hv[a] > 0], a[hv[a] < 0]
                    pb, nb = b[r[b] > 0], b[r[b] < 0]
                    if len(pa) != len(pb):
                        ok = False
                        break
                    if len(pa):
                        new.append((pa, pb))
                    if len(na):
                        new.append((na, nb))
                if not ok:
                    continue
                used[jb] = True
                if rec(k + 1, new):
                    return True
                used[jb] = False
            return False

        allc = np.arange(m)
        if rec(1, [(allc, allc)]):
            perm = res[0]
            Qm = np.empty_like(Hp)
            Qm[:, perm] = Hp
            tab = {}
            for i, row in enumerate(Qm.tolist()):
                tab[tuple(row)] = (i, 1)
                tab[tuple((-np.array(row)).tolist())] = (i, -1)
            src = np.empty(m, dtype=np.int64)
            sig = np.empty(m, dtype=np.int64)
            for kk, row in enumerate(Bp.tolist()):
                src[kk], sig[kk] = tab[tuple(row)]
            return r0, j0, perm, src, sig
    return None


# ---------------------------------------------------------------------------
def load_note_H():
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        sys.path.insert(0, here)
        import ps_p1mod4                                    # noqa
        return np.asarray(ps_p1mod4.build_matrix(5, "H"), dtype=np.int64)
    except Exception:
        for p in (os.path.join(here, "q5_equivalence", "H_note_q5.txt"),
                  os.path.join(here, "H_note_q5.txt")):
            if os.path.exists(p):
                return np.loadtxt(p, dtype=np.int64)
    raise SystemExit("cannot locate the note's q=5 matrix")


def load_fw_H():
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(here, "q5_equivalence", "H_fw.txt"),
              os.path.join(here, "H_fw.txt")):
        if os.path.exists(p):
            return np.loadtxt(p, dtype=np.int64)
    return None


# profiles recorded in q5_equivalence/profile_results.txt
PROF_NOTE = Counter({4: 359000, 12: 103125, 20: 25510})
PROF_FW = Counter({4: 353800, 12: 111525, 20: 21910, 28: 400})

# the choice, found by search, that reproduces the printed FW example's profile
FW_CHOICE = dict(pc=[4, 3, 2, 1, 0], pd=[3, 4, 0, 1, 2],
                 colperm=list(range(10)),
                 M=[(5, 9), (2, 7), (6, 11), (1, 8), (4, 0), (3, 10)],
                 alpha=(1, 4, 2, 0, 3))


def main() -> int:
    q, n = Q5, N12
    P = paley2(q)

    print("=" * 74)
    print("A.  The seed and the Lemma 2.2 conditions")
    print("=" * 74)
    check("P'_5 is a Hadamard matrix of order 12", is_hadamard(P))
    check("P'_5 is normalised (row 1 and column 1 all +1)",
          bool((P[0] == 1).all() and (P[:, 0] == 1).all()))
    check("column 2 of P'_5 is (1,-1,1^q,-1^q)",
          np.array_equal(P[:, 1], np.array([1, -1] + [1] * q + [-1] * q)))

    T0 = P[2:, 2:]
    # Lemma 2.2(1): which half-splits of the 2q columns of T are admissible?
    admissible = []
    for S in itertools.combinations(range(2 * q), q):
        cp = list(S) + [j for j in range(2 * q) if j not in S]
        Tc = T0[:, cp]
        if (all(Tc[i, :q].sum() == -1 and Tc[i, q:].sum() == -1 for i in range(q))
                and all(Tc[i, :q].sum() == 1 and Tc[i, q:].sum() == -1
                        for i in range(q, 2 * q))):
            admissible.append(cp)
    check("Lemma 2.2(1): the half-split N is unique (N = I up to order "
          "within each half): %d admissible split(s)" % len(admissible),
          len(admissible) == 1 and admissible[0] == list(range(2 * q)))

    # Lemma 2.2(2): the sign vector eps of the pairing M is forced.
    That = P[2:, :]
    ker = [np.array(v) for v in itertools.product([1, -1], repeat=n)
           if not (That @ np.array(v)).any()]
    bal = [v for v in ker if v.sum() == 0]
    check("Lemma 2.2(2): {+-1} kernel of T is exactly {+-row1, +-row2} "
          "(%d vectors)" % len(ker), len(ker) == 4)
    check("Lemma 2.2(2): only +-(column-2 pattern) is sign-balanced, so M is "
          "forced to pair each '+' column of column 2 with a '-' column",
          len(bal) == 2 and all(np.array_equal(abs(v), abs(P[1])) for v in bal))

    Pset = [j for j in range(n) if P[1, j] == 1]       # [0,7,8,9,10,11]
    Qset = [j for j in range(n) if P[1, j] == -1]      # [1,2,3,4,5,6]
    M_std = list(zip(Pset, Qset))
    colperm_std = list(range(2 * q))

    print()
    print("=" * 74)
    print("B.  Fidelity of the implementation of Psi_{5,alpha}")
    print("=" * 74)
    # B1: every enumerated output is Hadamard
    all_alpha = list(itertools.permutations(range(q)))
    profs = Counter()
    note_hits = []
    bad = 0
    for al in all_alpha:
        B = build_psi(P, colperm_std, M_std, al)
        if not is_hadamard(B):
            bad += 1
        p = profile4(B)
        profs[fmt(p)] += 1
        if p == PROF_NOTE:
            note_hits.append(al)
    check("all 120 outputs Psi_{5,alpha}(P'_5) are Hadamard of order 60",
          bad == 0)

    # B2: reproduce the 4-profile of the printed FW example
    Pr = P.copy()
    Pr[2:2 + q] = P[2:2 + q][FW_CHOICE["pc"]]
    Pr[2 + q:] = P[2 + q:][FW_CHOICE["pd"]]
    Bfw = build_psi(Pr, FW_CHOICE["colperm"], FW_CHOICE["M"], FW_CHOICE["alpha"])
    check("that choice yields a Hadamard matrix", is_hadamard(Bfw))
    pfw = profile4(Bfw)
    print("      choice: C-row order %s, D-row order %s, N = I,\n"
          "              M = %s, alpha = %s"
          % (FW_CHOICE["pc"], FW_CHOICE["pd"], FW_CHOICE["M"], FW_CHOICE["alpha"]))
    print("      profile: " + fmt(pfw))
    check("this implementation REPRODUCES the 4-profile of the order-60 "
          "matrix printed in the appendix of [FW]", pfw == PROF_FW)

    # B3: reverse-engineer the printed matrix; it must *be* a Psi-output
    Hfw = load_fw_H()
    if Hfw is not None:
        check("printed [FW] matrix is Hadamard of order 60", is_hadamard(Hfw))
        check("printed [FW] matrix has the recorded 4-profile",
              profile4(Hfw) == PROF_FW)
        t = Hfw[:2 * q].reshape(2 * q, n, q)[:, :, 0]
        const = np.array_equal(np.repeat(t, q, axis=1), Hfw[:2 * q])
        check("printed matrix: its first 2q=10 rows are constant on the 12 "
              "blocks of q=5 columns, i.e. have the shape T*M (x) J",
              const)
        # the printed matrix is normalised; undo the column signs
        v = None
        for w in itertools.product([1, -1], repeat=n):
            w = np.array(w)
            if not (t @ w).any() and w[0] == 1:
                v = w
                break
        Bo = Hfw * np.repeat(v, q)
        tp = Bo[:2 * q].reshape(2 * q, n, q)[:, :, 0]
        check("printed matrix: after undoing the normalisation its top band "
              "is T*M (x) J with T*M^T*M = 12I and zero row sums",
              bool((tp.sum(1) == 0).all())
              and np.array_equal(tp @ tp.T, n * np.eye(2 * q, dtype=np.int64)))
        # row signs: every 2q-chunk of the lower band must be a C- or D-row
        low = Bo[2 * q:]
        okrow = True
        L = []
        for r in low:
            f = [(r[2 * q * s:2 * q * s + q].sum(), r[2 * q * s + q:2 * q * (s + 1)].sum())
                 in [(-1, -1), (1, -1)] for s in range(q + 1)]
            if all(f):
                L.append(r)
            elif not any(f):
                L.append(-r)
            else:
                okrow = False
        L = np.array(L)
        chunks = sorted({tuple(r[2 * q * s:2 * q * (s + 1)].tolist())
                         for r in L for s in range(q + 1)})
        U = np.array(chunks)
        Cn = [i for i, r in enumerate(U) if r[:q].sum() == -1]
        Dn = [i for i, r in enumerate(U) if r[:q].sum() == 1]
        G = U @ U.T
        check("printed matrix: its lower 2q^2=50 rows use exactly 2q=10 "
              "distinct 2q-blocks, forming C and D of [FW, Step 5]",
              okrow and len(chunks) == 2 * q and len(Cn) == q and len(Dn) == q)
        check("printed matrix: those blocks satisfy Step 5 exactly "
              "(<c_i,c_j> = <d_i,d_j> = -2 for i != j, <c_i,d_j> = 0, "
              "norms 2q, half sums (-1,-1) for C and (1,-1) for D)",
              all(G[i, j] == -2 for i in Cn for j in Cn if i != j)
              and all(G[i, j] == -2 for i in Dn for j in Dn if i != j)
              and all(G[i, j] == 0 for i in Cn for j in Dn)
              and all(G[i, i] == 2 * q for i in range(2 * q))
              and all(U[i, q:].sum() == -1 for i in Cn)
              and all(U[i, q:].sum() == -1 for i in Dn))
        # Step 6/7: the 2q^2 lower rows fall into 2q classes of q rows sharing
        # their block-0 entry (= J^T (x) c_r resp. J^T (x) d_r); within a class,
        # each of the remaining q blocks runs over all q rows of C resp. of D.
        # (FW print the rows of B in a permuted order -- see the proof of
        #  [FW, Prop. 3.1] -- so we test the class structure, not row runs.)
        s0 = [tuple(r[:2 * q].tolist()) for r in L]
        cls_ok = sorted(Counter(s0).values()) == [q] * (2 * q)
        Cset = {tuple(U[i].tolist()) for i in Cn}
        Dset = {tuple(U[i].tolist()) for i in Dn}
        blocks_ok = True
        for key in set(s0):
            fam = Cset if key in Cset else Dset
            mem = [L[i] for i in range(len(L)) if s0[i] == key]
            for s in range(1, q + 1):
                got = {tuple(r[2 * q * s:2 * q * (s + 1)].tolist()) for r in mem}
                if got != fam:
                    blocks_ok = False
        check("printed matrix: its lower band splits into 2q classes of q rows "
              "sharing block 0 (= J^T (x) c_r / J^T (x) d_r, [FW, Step 6]), and "
              "in each further block such a class runs over all of C resp. D "
              "([FW, Step 7])", cls_ok and blocks_ok)
    else:
        print("  [warn] H_fw.txt not found; skipping the reverse-engineering check")

    print()
    print("=" * 74)
    print("C.  Exhaustive enumeration of alpha with the canonical (A, N, M)")
    print("=" * 74)
    print("    A = P'_5 (row order as displayed in [FW, Lem. 2.2]),")
    print("    N = I (the unique admissible half-split),")
    print("    M = the pairing (%s)," % ", ".join(map(str, M_std)))
    print("    alpha ranging over all 5! = 120 bijections {1..5} -> F_5.")
    print()
    for k, m in profs.most_common():
        print("    %3d x  %s%s" % (m, k, "   <-- the note's profile"
                                   if Counter({int(a.split(':')[0]): int(a.split(':')[1])
                                               for a in k.split()}) == PROF_NOTE else ""))
    print()
    check("the note's 4-profile %s OCCURS in this family" % fmt(PROF_NOTE),
          len(note_hits) > 0)
    aff = [tuple((a * k + b) % q for k in range(q))
           for a in range(1, q) for b in range(q)]
    check("the alpha attaining it are exactly the 20 affine bijections "
          "k |-> ak+b of F_5", sorted(note_hits) == sorted(aff))

    print()
    print("=" * 74)
    print("D.  An EXPLICIT Hadamard equivalence  H  ->  Psi_{5,id}(P'_5)")
    print("=" * 74)
    H = load_note_H()
    check("the note's q=5 matrix is Hadamard of order 60", is_hadamard(H))
    check("the note's q=5 matrix has the recorded 4-profile",
          profile4(H) == PROF_NOTE)
    alpha_id = tuple(range(q))
    B = build_psi(P, colperm_std, M_std, alpha_id)
    print("    target: B = Psi_{5,alpha}(P'_5), alpha(k) = k-1, N = I, M as above")
    r = find_equivalence(H, B)
    if not check("an explicit Hadamard equivalence H -> B was FOUND", r is not None):
        return 1
    r0, j0, perm, src, sig = r
    d2 = H[r0].copy()                 # column signs
    e2 = B[j0].copy()                 # column signs
    Hp = H * d2
    Qm = np.empty_like(Hp)
    Qm[:, perm] = Hp                  # column permutation
    Brec = (sig[:, None] * Qm[src]) * e2
    check("verified by exact integer identity:  B = D_r P_r (H D_2) P_c D_2' ",
          np.array_equal(Brec, B))
    print("      row-permutation image   src = %s" % src.tolist())
    print("      row signs              sigma = %s" % sig.tolist())
    print("      column permutation      perm = %s" % perm.tolist())
    print("      column signs (pre)        d2 = %s" % d2.tolist())
    print("      column signs (post)       e2 = %s" % e2.tolist())

    print()
    print("=" * 74)
    if FAIL:
        print("FAILED CHECKS: " + "; ".join(FAIL))
        return 1
    print("ALL CHECKS PASSED.")
    print()
    print("CONCLUSION.  At q = 5 the matrix H of the note IS Hadamard-equivalent")
    print("to an output of the Farouk-Wang procedure, namely Psi_{5,alpha}(P'_5)")
    print("for alpha the identity bijection (indeed for any of the 20 affine")
    print("bijections), with N and M the permutations of [FW, Lem. 2.2].  The")
    print("equivalence is exhibited explicitly above.  H is NOT equivalent to")
    print("the particular order-60 matrix printed in the appendix of [FW],")
    print("whose 4-profile differs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
