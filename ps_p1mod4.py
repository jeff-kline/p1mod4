#!/usr/bin/env python3
"""
paley_scarpis_from_tex.py

An *independent* implementation of the construction in

    paley_scarpis_p1mod4_submission.tex
    "A Paley-II Analogue of the Scarpis Construction for Prime Powers
     q = 1 (mod 4)"

written purely from that LaTeX note (no other source consulted).

The note constructs, for any prime power q = 1 (mod 4), a real Hadamard
matrix of order

    N = 2 q (q + 1).

This file (a) builds the matrix explicitly over F_q, and (b) tests the
Hadamard property H H^T = N I, either by a full Gram product (small N)
or by streamed, sampled row-dot checks (large N, e.g. q = 81 -> N = 13284).

Run:
    python paley_scarpis_from_tex.py            # default test sweep
    python paley_scarpis_from_tex.py --q 13     # one case
    python paley_scarpis_from_tex.py --q 81 --sampled --pairs 4000

Only numpy is required.
"""

from __future__ import annotations

import argparse
import time

import numpy as np


# ----------------------------------------------------------------------------
# 0. Tiny polynomial-over-F_p layer, used only to build extension fields F_{p^k}
#    (k >= 2, e.g. q = 9, 25, 49, 81). Prime fields skip all of this.
#    Polynomials are coefficient lists, low degree first; [] is the zero poly.
# ----------------------------------------------------------------------------

def _trim(a, p):
    a = [c % p for c in a]
    while a and a[-1] == 0:
        a.pop()
    return a


def _pmul(a, b, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return _trim(r, p)


def _psub(a, b, p):
    n = max(len(a), len(b))
    r = [0] * n
    for i in range(len(a)):
        r[i] = a[i]
    for i in range(len(b)):
        r[i] = (r[i] - b[i]) % p
    return _trim(r, p)


def _pmod(a, m, p):
    """Remainder of a modulo m over F_p (m nonzero)."""
    a = _trim(a[:], p)
    dm = len(m) - 1
    if dm < 0:
        raise ZeroDivisionError("modulus is zero polynomial")
    inv_lead = pow(m[-1], p - 2, p)  # p prime => Fermat inverse
    while len(a) - 1 >= dm and a:
        coef = (a[-1] * inv_lead) % p
        shift = (len(a) - 1) - dm
        for i in range(len(m)):
            a[shift + i] = (a[shift + i] - coef * m[i]) % p
        a = _trim(a, p)
    return a


def _pgcd(a, b, p):
    a = _trim(a[:], p)
    b = _trim(b[:], p)
    while b:
        a, b = b, _pmod(a, b, p)
    return a


def _ppowmod(base, e, m, p):
    """base**e mod m over F_p (e a nonnegative integer)."""
    result = [1]
    base = _pmod(base[:], m, p)
    while e > 0:
        if e & 1:
            result = _pmod(_pmul(result, base, p), m, p)
        base = _pmod(_pmul(base, base, p), m, p)
        e >>= 1
    return _trim(result, p)


def _distinct_prime_factors(n):
    f = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            f.add(d)
            n //= d
        d += 1
    if n > 1:
        f.add(n)
    return f


def _is_irreducible(f, p):
    """Rabin irreducibility test for a monic f of degree n over F_p."""
    n = len(f) - 1
    x = [0, 1]
    # 1. x^(p^n) == x (mod f)
    if _ppowmod(x, p ** n, f, p) != _trim([0, 1], p):
        return False
    # 2. gcd(x^(p^(n/d)) - x, f) is a unit for every prime divisor d of n
    for d in _distinct_prime_factors(n):
        h = _ppowmod(x, p ** (n // d), f, p)
        g = _pgcd(_psub(h, [0, 1], p), f, p)
        if len(g) - 1 != 0:  # gcd has degree >= 1 -> shares a factor
            return False
    return True


def _find_irreducible(p, k):
    """First monic irreducible of degree k over F_p (lexicographic in c0..c_{k-1})."""
    from itertools import product
    for coeffs in product(range(p), repeat=k):
        f = list(coeffs) + [1]  # monic
        if _is_irreducible(f, p):
            return f
    raise RuntimeError(f"no irreducible degree-{k} polynomial found over F_{p}")


# ----------------------------------------------------------------------------
# 1. Finite field F_q with q = p^k. Elements are indexed 0..q-1.
#    Index <-> coefficient vector (c0,...,c_{k-1}) of c0 + c1 x + ... mod f,
#    via index = sum c_m p^m. So index 0 = field 0, index 1 = field 1.
# ----------------------------------------------------------------------------

def _factor_prime_power(q):
    if q < 2:
        raise ValueError("q must be >= 2")
    for d in range(2, q + 1):
        if q % d == 0:
            p, k, n = d, 0, q
            while n % p == 0:
                n //= p
                k += 1
            if n != 1:
                raise ValueError(f"{q} is not a prime power")
            return p, k
    raise ValueError(f"{q} is not a prime power")


class GF:
    """Finite field GF(q). Exposes add/sub/mul on indices and the array chi[]."""

    def __init__(self, q):
        self.q = q
        self.p, self.k = _factor_prime_power(q)
        if self.k == 1:
            self._build_prime()
        else:
            self._build_extension()
        self._build_character()

    # -- prime field F_p ------------------------------------------------------
    def _build_prime(self):
        p = self.p
        self.add_t = [[(i + j) % p for j in range(p)] for i in range(p)]
        self.mul_t = [[(i * j) % p for j in range(p)] for i in range(p)]
        self.neg_t = [(-i) % p for i in range(p)]

    # -- extension field F_{p^k} ---------------------------------------------
    def _build_extension(self):
        p, k, q = self.p, self.k, self.q
        self.modpoly = _find_irreducible(p, k)

        def vec_of(idx):
            v = []
            for _ in range(k):
                v.append(idx % p)
                idx //= p
            return v

        def idx_of(vec):
            idx = 0
            for m in range(k - 1, -1, -1):
                idx = idx * p + vec[m]
            return idx

        vecs = [vec_of(i) for i in range(q)]
        self.add_t = [[0] * q for _ in range(q)]
        self.mul_t = [[0] * q for _ in range(q)]
        self.neg_t = [0] * q
        f = self.modpoly
        for i in range(q):
            vi = vecs[i]
            self.neg_t[i] = idx_of([(-c) % p for c in vi])
            for j in range(q):
                vj = vecs[j]
                self.add_t[i][j] = idx_of([(vi[m] + vj[m]) % p for m in range(k)])
                prod = _pmod(_pmul(vi, vj, p), f, p)
                pv = [0] * k
                for m, c in enumerate(prod):
                    pv[m] = c % p
                self.mul_t[i][j] = idx_of(pv)

    # -- quadratic character: chi(x) = x^((q-1)/2), read as +-1 ---------------
    def _build_character(self):
        q = self.q
        e = (q - 1) // 2
        chi = [0] * q
        for i in range(1, q):
            r, b, ee = 1, i, e            # r = 1 is the field identity (index 1)
            while ee > 0:
                if ee & 1:
                    r = self.mul_t[r][b]
                b = self.mul_t[b][b]
                ee >>= 1
            chi[i] = 1 if r == 1 else -1   # the only square roots of 1 are +-1
        self.chi = chi

    # -- index arithmetic -----------------------------------------------------
    def add(self, i, j):
        return self.add_t[i][j]

    def sub(self, i, j):
        return self.add_t[i][self.neg_t[j]]

    def mul(self, i, j):
        return self.mul_t[i][j]


# ----------------------------------------------------------------------------
# 2. The fixed 2x2 Paley-II replacement blocks and psi (from section 2).
# ----------------------------------------------------------------------------

P = np.array([[1, 1], [1, -1]], dtype=np.int8)
Z = np.array([[1, -1], [-1, -1]], dtype=np.int8)
R = np.array([[0, -1], [1, 0]], dtype=np.int8)
NEG_P = (-P).astype(np.int8)


def psi(c):
    """psi(0)=Z, psi(1)=P, psi(-1)=-P."""
    if c == 0:
        return Z
    if c == 1:
        return P
    return NEG_P


# ----------------------------------------------------------------------------
# 3. The construction.
#
#    Column layout of every 2q-row band (length N = 2q(q+1)):
#        block "-1" (border)  : columns [0, 2q)
#        block a (a in F)     : columns [2q(1+a), 2q(2+a))
#
#    Row layout of H:
#        rows [0, 2q)              : cap band  M_infty
#        rows [2q(1+r), 2q(2+r))   : finite band M_r,  r in F
#
#    A "Paley strip" D_t is the 2 x 2q array whose y-th 2x2 block is
#    psi(chi(y - t)). With it:
#       - K_t row a' over a 2q-block  = D_t[a']
#       - border of M_r (= B_r)       uses D_r           (independent of x)
#       - block a of M_r (= K_{a r})  uses D_{x + a r}
# ----------------------------------------------------------------------------

class PaleyScarpis:
    def __init__(self, q):
        if (q - 1) % 4 != 0:
            raise ValueError("construction requires q = 1 (mod 4)")
        self.q = q
        self.F = GF(q)
        self.N = 2 * q * (q + 1)
        self._strips = None  # cache of D_t for t = 0..q-1

    # -- D_t : 2 x 2q --------------------------------------------------------
    def _paley_strip(self, t):
        q, F = self.q, self.F
        strip = np.empty((2, 2 * q), dtype=np.int8)
        for y in range(q):
            strip[:, 2 * y:2 * y + 2] = psi(F.chi[F.sub(y, t)])
        return strip

    def _strip(self, t):
        if self._strips is None:
            self._strips = [self._paley_strip(tt) for tt in range(self.q)]
        return self._strips[t]

    # -- one finite row (band M_r), local row (x, ap) ------------------------
    def finite_row(self, r, x, ap):
        q, F = self.q, self.F
        parts = [self._strip(r)[ap]]                      # border block = B_r
        for a in range(q):                                # block a = K_{a r}
            t = F.add(x, F.mul(a, r))
            parts.append(self._strip(t)[ap])
        return np.concatenate(parts)

    # -- one cap row (band M_infty), local row (e, alpha) --------------------
    def cap_row(self, e, alpha):
        q, F = self.q, self.F
        # border: S[e, infinity] = P, tiled q times
        parts = [np.tile(P[alpha], q)]
        for a in range(q):
            # S[e, a] = psi(chi(a - e)); finite columns are right-multiplied by R
            blk = psi(F.chi[F.sub(a, e)]).astype(np.int64) @ R.astype(np.int64)
            parts.append(np.tile(blk[alpha].astype(np.int8), q))
        return np.concatenate(parts).astype(np.int8)

    # -- global row dispatcher (for streamed verification) -------------------
    def row(self, i):
        q = self.q
        if i < 2 * q:                       # cap band
            return self.cap_row(i // 2, i % 2)
        j = i - 2 * q                        # finite bands
        r = j // (2 * q)
        rem = j % (2 * q)
        return self.finite_row(r, rem // 2, rem % 2)

    # -- full matrix ---------------------------------------------------------
    def build_full(self):
        q, N, F = self.q, self.N, self.F
        # warm the strip cache once
        _ = self._strip(0)
        H = np.empty((N, N), dtype=np.int8)
        row = 0
        for e in range(q):                   # cap band: 2q rows
            for alpha in range(2):
                H[row] = self.cap_row(e, alpha)
                row += 1
        for r in range(q):                   # finite bands: 2q^2 rows
            for x in range(q):
                for ap in range(2):
                    parts = [self._strip(r)[ap]]
                    for a in range(q):
                        t = F.add(x, F.mul(a, r))
                        parts.append(self._strip(t)[ap])
                    H[row] = np.concatenate(parts)
                    row += 1
        assert row == N
        return H

    # -- seed Paley-II matrix S of order 2(q+1) (sanity sub-test) ------------
    def build_seed_S(self):
        """Order-2(q+1) Paley-II Hadamard seed; index q stands for infinity."""
        q, F = self.q, self.F
        n = q + 1
        INF = q
        S = np.empty((2 * n, 2 * n), dtype=np.int8)
        for u in range(n):
            for v in range(n):
                if u == v:
                    blk = Z                       # C_{u,u} = 0
                elif u == INF or v == INF:
                    blk = P                        # C_{inf,*} = C_{*,inf} = 1
                else:
                    blk = psi(F.chi[F.sub(v, u)])  # C_{u,v} = chi(v - u)
                S[2 * u:2 * u + 2, 2 * v:2 * v + 2] = blk
        return S


# ----------------------------------------------------------------------------
# 4. Verification.
# ----------------------------------------------------------------------------

def _is_pm1(M):
    return bool(((M == 1) | (M == -1)).all())


def verify_full(con):
    """Build H and check H H^T = N I exactly. Returns (ok, details)."""
    q, N = con.q, con.N

    S = con.build_seed_S()
    seed_ok = np.array_equal(
        S.astype(np.int32) @ S.T.astype(np.int32),
        2 * (q + 1) * np.eye(2 * (q + 1), dtype=np.int32),
    ) and _is_pm1(S)

    H = con.build_full()
    pm1 = _is_pm1(H)
    G = H.astype(np.int32) @ H.T.astype(np.int32)
    gram_ok = np.array_equal(G, N * np.eye(N, dtype=np.int32))

    # locate the worst off-diagonal entry if something is wrong
    detail = ""
    if not gram_ok:
        off = G - N * np.eye(N, dtype=np.int32)
        detail = f"max|off-diag/defect| = {int(np.abs(off).max())}"
    return (seed_ok and pm1 and gram_ok), {
        "seed_hadamard": seed_ok,
        "entries_pm1": pm1,
        "gram_ok": gram_ok,
        "detail": detail,
    }


def verify_sampled(con, num_pairs=3000, seed=0):
    """Stream rows; check sampled inner products without materializing H H^T."""
    q, N = con.q, con.N
    rng = np.random.default_rng(seed)

    # deterministic structural pairs that exercise each Gram case
    fixed = [
        (0, 0),                 # cap diagonal
        (0, 1),                 # within cap band
        (0, 2 * q),             # cap vs finite (M_infty M_r^T = 0)
        (2 * q, 2 * q + 1),     # within one finite band
    ]
    if q >= 2:
        fixed.append((2 * q, 4 * q))          # M_0 vs M_1   (r != s -> 0)
        fixed.append((2 * q, 2 * q + 2 * q - 1))  # within M_0

    rand = [(int(a), int(b)) for a, b in
            rng.integers(0, N, size=(num_pairs, 2))]
    pairs = fixed + rand

    bad = 0
    first_bad = None
    cache = {}
    # cache rows as int8 and bound total cache memory to ~300 MB
    cap = max(2000, min(20000, 300_000_000 // N))

    def get(i):
        v = cache.get(i)
        if v is None:
            v = con.row(i)               # int8, N bytes/row
            if len(cache) < cap:
                cache[i] = v
        return v

    for (i, j) in pairs:
        ri, rj = get(i), get(j)
        if not (_is_pm1(ri) and _is_pm1(rj)):
            bad += 1
            first_bad = first_bad or ("non +-1 row", i, j)
            continue
        # cast at dot time so int8 storage can't overflow the accumulation
        d = int(ri.astype(np.int32) @ rj.astype(np.int32))
        expected = N if i == j else 0
        if d != expected:
            bad += 1
            if first_bad is None:
                first_bad = ("dot mismatch", i, j, d, expected)

    return bad == 0, {
        "pairs_checked": len(pairs),
        "bad": bad,
        "first_bad": first_bad,
    }


def verify(q, num_pairs=3000, force=None, verbose=True):
    """Pick full vs sampled by N (paper uses full for N < 5000)."""
    con = PaleyScarpis(q)
    N = con.N
    mode = force or ("full" if N < 5000 else "sampled")
    t0 = time.time()
    if mode == "full":
        ok, info = verify_full(con)
    else:
        ok, info = verify_sampled(con, num_pairs=num_pairs)
    dt = time.time() - t0
    if verbose:
        tag = "OK " if ok else "FAIL"
        extra = "" if ok else f"  <-- {info}"
        print(f"[{tag}] q={q:<3} N={N:<6} mode={mode:<7} "
              f"({dt:5.2f}s){extra}")
    return ok, info, con


# ----------------------------------------------------------------------------
# 5. CLI.
# ----------------------------------------------------------------------------

DEFAULT_QS = [5, 9, 13, 17, 25, 29, 37, 41, 49]  # all N < 5000 -> full Gram


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--q", type=int, default=None,
                    help="single prime power q = 1 (mod 4) to test")
    ap.add_argument("--sampled", action="store_true",
                    help="force streamed sampled verification")
    ap.add_argument("--full", action="store_true",
                    help="force full Gram verification")
    ap.add_argument("--pairs", type=int, default=3000,
                    help="number of random row pairs in sampled mode")
    ap.add_argument("--big", action="store_true",
                    help="also run q=81 (N=13284) in sampled mode")
    args = ap.parse_args()

    force = "sampled" if args.sampled else ("full" if args.full else None)

    if args.q is not None:
        ok, _, _ = verify(args.q, num_pairs=args.pairs, force=force)
        raise SystemExit(0 if ok else 1)

    print("Paley-II / Scarpis analogue, order N = 2 q (q+1):")
    all_ok = True
    for q in DEFAULT_QS:
        ok, _, _ = verify(q, num_pairs=args.pairs, force=force)
        all_ok &= ok
    if args.big:
        ok, _, _ = verify(81, num_pairs=max(args.pairs, 4000), force="sampled")
        all_ok &= ok
    print("ALL PASS" if all_ok else "SOME FAILED")
    raise SystemExit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
