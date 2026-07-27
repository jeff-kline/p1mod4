#!/usr/bin/env python3
"""Reproduce Remark 11 (\\label{rem:q9}) and Section 7 Problem 2's delta-slot
count for q = 9:

    "of the 2^4 = 16 even sign patterns on Z_3^2 vanishing at 0, exactly 6
     are of Paley type, and all are equivalent to chi under Aut(Z_3^2)."

Definitions (Section 5 of the paper, the paragraph beginning "Call delta of
Paley type"):

    delta: G -> {0, +-1} is of Paley type if
        delta(0) = 0,
        delta(z) != 0 for z != 0,
        delta(-z) = delta(z)                       ["even"]
        sum_{z in G} delta(z) delta(z - d) = -1     for every d != 0.

Here G = Z_3^2, taken to be the additive group (F_9, +) exactly as built by
ps_p1mod4.GF(9) -- this script checks that identification explicitly rather
than assuming it.

"Even sign pattern vanishing at 0" (as opposed to an arbitrary even function
G -> {0,+-1} vanishing at 0, of which there would be more than 16) means:
delta(0) = 0 and, for each of the 4 antipodal pairs {z,-z} with z != 0,
delta takes a single value +1 or -1 on the whole pair -- i.e. an actual +-1
sign pattern, not merely delta(z) in {0,+1,-1}.  That reading is forced by
the stated count 2^4 = 16: four independent pairs, two choices each.  (Note
this also means every one of the 16 already satisfies the Paley-type clause
"delta(z) != 0 for z != 0"; what separates Paley type from merely-even-and-
vanishing is only the difference-sum condition.)

This script verifies BOTH halves of the claim:
  (1) exactly 6 of the 16 patterns satisfy the difference-sum condition;
  (2) those 6 form a single orbit under Aut(Z_3^2) = GL(2,3), |GL(2,3)| = 48.

This file is meant to live at code/paley_patterns_q9.py, alongside
ps_p1mod4.py, and imports GF from there directly; no separate reimplementation
of F_9 is used, per the paper's identification G = (F_9, +).
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ps_p1mod4 import GF


# --------------------------------------------------------------------------
# Z_3^2 as coefficient vectors: index i <-> (c0, c1) = (i % 3, i // 3),
# matching how ps_p1mod4.GF._build_extension indexes F_{p^k} elements
# (index = sum c_m p^m).  This is the same convention the construction code
# itself uses, not an independent choice.
# --------------------------------------------------------------------------

def vector_of(i):
    return (i % 3, i // 3)


def index_of(v):
    return (v[0] % 3) + 3 * (v[1] % 3)


def check_additive_agreement(F):
    """Confirm GF(9)'s additive table literally *is* Z_3^2 vector addition
    under the index <-> (c0,c1) correspondence above -- not assumed."""
    for i in range(9):
        for j in range(9):
            vi, vj = vector_of(i), vector_of(j)
            want = index_of((vi[0] + vj[0], vi[1] + vj[1]))
            if F.add(i, j) != want:
                return False
    return True


# --------------------------------------------------------------------------
# The 16 even sign patterns vanishing at 0, and the Paley-type filter.
# --------------------------------------------------------------------------

def antipodal_pairs(F):
    """The 4 pairs {z, -z}, z != 0, in Z_3^2 (char 3 => z != -z for z != 0,
    since 2z = 0 would force z = 0)."""
    seen = set()
    pairs = []
    for z in range(1, 9):
        if z in seen:
            continue
        nz = F.neg_t[z]
        assert nz != z, "char-3 group should have no order-2 elements"
        seen.add(z)
        seen.add(nz)
        pairs.append((z, nz))
    return pairs


def even_patterns_vanishing_at_0(pairs):
    """All 2^4 = 16 functions delta: {0..8} -> {-1,0,+1} with delta(0) = 0
    and delta constant +-1 on each antipodal pair."""
    patterns = []
    for signs in itertools.product((1, -1), repeat=len(pairs)):
        delta = [0] * 9
        for (z, nz), s in zip(pairs, signs):
            delta[z] = s
            delta[nz] = s
        patterns.append(tuple(delta))
    return patterns


def is_paley_type(F, delta):
    """delta(0)=0, delta(z)!=0 for z!=0, delta(-z)=delta(z), and
    sum_z delta(z) delta(z-d) = -1 for every d != 0."""
    if delta[0] != 0:
        return False
    if any(delta[z] == 0 for z in range(1, 9)):
        return False
    if any(delta[F.neg_t[z]] != delta[z] for z in range(9)):
        return False
    for d in range(1, 9):
        s = sum(delta[z] * delta[F.sub(z, d)] for z in range(9))
        if s != -1:
            return False
    return True


# --------------------------------------------------------------------------
# Aut(Z_3^2) = GL(2,3): all 48 invertible 2x2 matrices over F_3, each
# realised as the permutation it induces on indices 0..8.
# --------------------------------------------------------------------------

def gl2_3_permutations():
    mats = [(a, b, c, d)
            for a, b, c, d in itertools.product(range(3), repeat=4)
            if (a * d - b * c) % 3 != 0]
    perms = []
    for (a, b, c, d) in mats:
        perm = [0] * 9
        for i in range(9):
            v0, v1 = vector_of(i)
            w0 = (a * v0 + b * v1) % 3
            w1 = (c * v0 + d * v1) % 3
            perm[i] = index_of((w0, w1))
        perms.append(tuple(perm))
    return mats, perms


def apply_perm(delta, perm):
    return tuple(delta[perm[i]] for i in range(9))


def orbits_under(pattern_set, perms):
    remaining = set(pattern_set)
    orbs = []
    while remaining:
        start = next(iter(remaining))
        orb = {apply_perm(start, g) for g in perms}
        orbs.append(orb)
        remaining -= orb
    return orbs


def fmt_pattern(delta):
    return "".join("0" if v == 0 else ("+" if v == 1 else "-") for v in delta)


# --------------------------------------------------------------------------
# Main.
# --------------------------------------------------------------------------

def main():
    fails = []

    def check(ok, label, got, want=None):
        mark = "OK " if ok else "FAIL"
        print(f"[{mark}] {label}: {got}" + ("" if ok or want is None else f"   (expected {want})"))
        if not ok:
            fails.append(label)

    F = GF(9)

    print("Setup: Z_3^2 as the additive group of GF(9) from ps_p1mod4")
    check(check_additive_agreement(F),
          "  GF(9).add matches Z_3^2 vector addition (index = c0 + 3*c1)", True)
    check(all(F.add(z, F.add(z, z)) == 0 for z in range(9)),
          "  every element z satisfies 3z = 0 (exponent 3)", True)

    pairs = antipodal_pairs(F)
    check(len(pairs) == 4, "  antipodal pairs {z,-z}, z != 0", len(pairs), 4)

    all_even = even_patterns_vanishing_at_0(pairs)
    check(len(all_even) == 16, "  even sign patterns vanishing at 0 (2^4)", len(all_even), 16)
    check(len(set(all_even)) == 16, "  ... and all 16 are distinct", len(set(all_even)), 16)

    paley = [d for d in all_even if is_paley_type(F, d)]
    print("\nClaim (Remark 11 / Sec.7 problem 2): exactly 6 of the 16 are of Paley type")
    check(len(paley) == 6, "  count of Paley-type patterns among the 16", len(paley), 6)

    print("\n  the Paley-type patterns found (index 0..8; '0'=origin, "
          "'+'=+1, '-'=-1):")
    for d in paley:
        print(f"    {fmt_pattern(d)}")

    chi_pattern = tuple(F.chi)
    check(chi_pattern in set(paley),
          "  the quadratic character chi is among them", chi_pattern in set(paley), True)

    mats, perms = gl2_3_permutations()
    check(len(perms) == 48, "  |Aut(Z_3^2)| = |GL(2,3)|", len(perms), 48)
    check(len(set(perms)) == 48, "  ... all 48 induced permutations distinct", len(set(perms)), 48)

    even_set, paley_set = set(all_even), set(paley)
    closed_16 = all(apply_perm(d, g) in even_set for d in all_even for g in perms)
    check(closed_16, "  the 16-pattern set is closed under Aut(Z_3^2)", closed_16, True)
    closed_6 = all(apply_perm(d, g) in paley_set for d in paley for g in perms)
    check(closed_6, "  the 6-pattern (Paley-type) set is closed under Aut(Z_3^2)", closed_6, True)

    orbs = orbits_under(paley_set, perms)
    print(f"\nOrbit structure of the {len(paley)} Paley-type patterns under the "
          f"48 automorphisms:")
    check(len(orbs) == 1, "  number of orbits", len(orbs), 1)
    if orbs:
        sizes = sorted(len(o) for o in orbs)
        print(f"    orbit sizes: {sizes}")
        if len(orbs) == 1:
            stab = 48 // len(orbs[0])
            print(f"    |orbit| * |stabilizer| = 48  =>  |stabilizer(chi)| = {stab}")
            check(len(orbs[0]) == 6, "  the single orbit has size", len(orbs[0]), 6)

    print()
    if fails:
        print(f"FAILED: {len(fails)} check(s): {fails}")
        return 1
    print("ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
