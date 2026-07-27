#!/usr/bin/env python3
"""Reproduce the coverage analysis of Appendix A.

Three things are checked, all of which the paper states as computed:

  A.1  the audited range q <= 73: the twelve odd parts m = q(q+1)/2 are
       each absent from Table 4 of Cati-Pasechnik, so every N in that
       range is a known Hadamard order;
  A.4  the elementary-witness screen over the 232 orders with q <= 3000:
       128 covered, 104 without a witness;
  A.4  the smallest failure of the screen is q = 109, N = 23980.

Run with no arguments to check every published number and exit nonzero if
any disagrees:

    python coverage_table.py

Add --table to print the 104 failing orders.

The screen implemented here is (C.1) of the paper, recomputed from actual
divisor splits.  The earlier factorwise test is withdrawn (Remark 7) and is
deliberately NOT implemented.
"""

import argparse
import sys

# ---------------------------------------------------------------------------
# Table 4 of Cati-Pasechnik, "A database of constructions of Hadamard
# matrices", arXiv:2411.18897v2 -- the odd n <= 2999 for which the least t
# with a known Hadamard matrix of order 2^t n has t > 2.  Transcribed from
# the published table; m = 2 entries are not listed there and not here.
# ---------------------------------------------------------------------------
CP_TABLE4 = [
    167, 179, 223, 283, 311, 347, 359, 419, 443, 479, 487, 491, 515,
    523, 537, 571, 573, 599, 643, 647, 659, 669, 719, 721, 739, 751,
    789, 823, 839, 859, 863, 883, 907, 917, 919, 933, 947, 955, 971,
    991, 1019, 1031, 1039, 1051, 1063, 1087, 1103, 1115, 1123, 1133,
    1169, 1187, 1223, 1255, 1257, 1259, 1283, 1291, 1303, 1315, 1319,
    1327, 1359, 1367, 1423, 1427, 1437, 1439, 1441, 1447, 1451, 1471,
    1473, 1483, 1487, 1499, 1509, 1527, 1543, 1559, 1567, 1571, 1579,
    1583, 1589, 1619, 1661, 1663, 1667, 1689, 1699, 1703, 1713, 1719,
    1747, 1751, 1783, 1787, 1793, 1795, 1823, 1831, 1841, 1847, 1871,
    1879, 1883, 1893, 1907, 1915, 1929, 1949, 1957, 1963, 1969, 1979,
    1981, 1987, 2027, 2039, 2063, 2083, 2087, 2095, 2099, 2119, 2143,
    2155, 2171, 2203, 2207, 2215, 2227, 2251, 2287, 2293, 2315, 2327,
    2335, 2339, 2347, 2369, 2371, 2383, 2399, 2423, 2429, 2459, 2489,
    2503, 2513, 2515, 2531, 2543, 2545, 2571, 2579, 2589, 2591, 2629,
    2647, 2659, 2661, 2671, 2677, 2683, 2687, 2699, 2711, 2731, 2733,
    2767, 2803, 2815, 2819, 2823, 2841, 2843, 2855, 2865, 2879, 2887,
    2893, 2899, 2903, 2913, 2927, 2939, 2951, 2963, 2971, 2973, 2987,
    2995, 2999,
]


# ------------------------------------------------------------------ arithmetic
def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def is_prime_power(n):
    """True if n = p^k for a prime p and k >= 1."""
    if n < 2:
        return False
    for p in range(2, int(n ** 0.5) + 1):
        if n % p == 0:
            if not is_prime(p):
                continue
            m = n
            while m % p == 0:
                m //= p
            return m == 1
    return True  # n is prime


def factor(n):
    """Return the factorization of n as a list of (prime, exponent)."""
    out, m, p = [], n, 2
    while p * p <= m:
        if m % p == 0:
            k = 0
            while m % p == 0:
                m //= p
                k += 1
            out.append((p, k))
        p += 1 if p == 2 else 2
    if m > 1:
        out.append((m, 1))
    return out


def fmt_factor(n):
    parts = []
    for p, k in factor(n):
        parts.append(str(p) if k == 1 else f"{p}^{k}")
    return "*".join(parts)


def divisors(n):
    ds = set()
    d = 1
    while d * d <= n:
        if n % d == 0:
            ds.add(d)
            ds.add(n // d)
        d += 1
    return sorted(ds)


# ------------------------------------------------------------------- the screen
def is_paley_order(N):
    """N is a Paley I order (N = p+1, p = 3 mod 4 a prime power) or a
    Paley II order (N = 2(p+1), p = 1 mod 4 a prime power)."""
    p = N - 1
    if p >= 3 and p % 4 == 3 and is_prime_power(p):
        return True
    if N % 2 == 0:
        p = N // 2 - 1
        if p >= 5 and p % 4 == 1 and is_prime_power(p):
            return True
    return False


def t_known(t):
    """T-matrices of odd order t are available for t <= 59, via the base
    sequences BS((t+1)/2, (t-1)/2)."""
    return t % 2 == 1 and t <= 59


def w_known(w):
    """Williamson-type matrices of odd order w: directly for w <= 33, or
    from Turyn's (P+1)/2 family when P = 2w-1 is a prime power."""
    if w % 2 != 1:
        return False
    return w <= 33 or is_prime_power(2 * w - 1)


def turyn_witness(m):
    """An exhibited factorization m = t*w with t T-known and w W-known,
    i.e. (C.1).  Returns (t, w) or None."""
    for t in divisors(m):
        if t_known(t) and w_known(m // t):
            return t, m // t
    return None


def screen(q):
    """Classify the order N = 2q(q+1).  Returns (verdict, detail)."""
    N = 2 * q * (q + 1)
    m = q * (q + 1) // 2
    if m <= 3000:
        return "audited", "table lookup (A.1)"
    if is_paley_order(N):
        return "paley", "Paley I/II order"
    tw = turyn_witness(m)
    if tw:
        return "turyn", f"Turyn 4*{tw[0]}*{tw[1]}"
    return "none", "no restricted elementary witness"


def prime_powers_1mod4(limit):
    return [q for q in range(5, limit + 1) if q % 4 == 1 and is_prime_power(q)]


# ------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--table", action="store_true",
                    help="print the 104 orders with no elementary witness")
    args = ap.parse_args()

    fails = []

    def check(ok, label, got, want):
        mark = "OK " if ok else "FAIL"
        print(f"[{mark}] {label}: {got}" + ("" if ok else f"   (expected {want})"))
        if not ok:
            fails.append(label)

    # -- A.1: the audited range -------------------------------------------
    audited = prime_powers_1mod4(73)
    odd_parts = [q * (q + 1) // 2 for q in audited]
    open_set = set(CP_TABLE4)
    hits = [m for m in odd_parts if m in open_set]
    print("Appendix A.1 -- audited range q <= 73")
    check(len(audited) == 12, "  prime powers q = 1 mod 4 with q <= 73", len(audited), 12)
    check(max(odd_parts) <= 3000, "  largest odd part", max(odd_parts), "<= 3000")
    print(f"       odd parts m = q(q+1)/2: {odd_parts}")
    check(not hits, "  odd parts absent from Cati-Pasechnik Table 4",
          "all 12 absent" if not hits else f"{hits} PRESENT", "all absent")

    # the two statistics quoted in A.1 about Table 4 itself
    n_open = len(CP_TABLE4)
    n_comp = sum(1 for n in CP_TABLE4 if not is_prime(n))
    check(n_open == 195, "  Table 4 entries (odd n <= 2999, t > 2)", n_open, 195)
    check(n_open - n_comp == 124, "  of which prime", n_open - n_comp, 124)
    check(n_comp == 71, "  of which composite", n_comp, 71)
    check(min(CP_TABLE4) == 167, "  smallest entry", min(CP_TABLE4), 167)
    smallest_comp = min(n for n in CP_TABLE4 if not is_prime(n))
    check(smallest_comp == 515, "  smallest composite entry", smallest_comp, 515)

    # -- A.4: the elementary-witness screen -------------------------------
    print("\nAppendix A.4 -- elementary-witness screen, q <= 3000")
    qs = prime_powers_1mod4(3000)
    verdicts = {q: screen(q) for q in qs}
    covered = [q for q in qs if verdicts[q][0] != "none"]
    none = [q for q in qs if verdicts[q][0] == "none"]

    check(len(qs) == 232, "  orders with q <= 3000", len(qs), 232)
    check(len(covered) == 128, "  covered (audited, Paley, or Turyn)", len(covered), 128)
    check(len(none) == 104, "  no restricted elementary witness", len(none), 104)
    check(none and none[0] == 109, "  smallest failure", none[0] if none else None, 109)
    if none and none[0] == 109:
        q = 109
        N, m = 2 * q * (q + 1), q * (q + 1) // 2
        check(N == 23980 and fmt_factor(m) == "5*11*109",
              "  smallest failure order", f"N={N}, m={fmt_factor(m)}",
              "N=23980, m=5*11*109")

    if args.table:
        print(f"\nThe {len(none)} orders with no restricted elementary witness:\n")
        print(f"  {'q':>5}  {'N = 2q(q+1)':>12}  odd part m")
        for q in none:
            print(f"  {q:>5}  {2*q*(q+1):>12}  {fmt_factor(q*(q+1)//2)}")

    print()
    if fails:
        print(f"FAILED: {len(fails)} check(s): {fails}")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
