"""Hadamard generator for the experimental q == 1 (mod 4) Scarpis/Paley-II lift.

The public entry point is ``paley2_scarpis_hadamard(q)``.
"""

from __future__ import annotations

import math

import numpy as np


P = np.array([[1, 1], [1, -1]], dtype=np.int8)
Z = np.array([[1, -1], [-1, -1]], dtype=np.int8)
R90 = np.array([[0, -1], [1, 0]], dtype=np.int8)


def _prime_power_decomposition(n: int) -> tuple[int, int]:
    """Return (p, e) when n = p**e for prime p; raise otherwise."""
    if n < 2:
        raise ValueError("q must be a prime power")
    if n % 2 == 0:
        p = 2
    else:
        p = None
        limit = math.isqrt(n)
        for d in range(3, limit + 1, 2):
            if n % d == 0:
                p = d
                break
        if p is None:
            return n, 1

    exponent = 0
    rest = n
    while rest % p == 0:
        exponent += 1
        rest //= p
    if rest != 1:
        raise ValueError("q must be a prime power")
    return p, exponent


def _prime_divisors(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def _poly_trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def _poly_sub(a: list[int], b: list[int], p: int) -> list[int]:
    size = max(len(a), len(b))
    out = [0] * size
    for i in range(size):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return _poly_trim(out)


def _poly_mod(a: list[int], modulus: list[int], p: int) -> list[int]:
    out = [x % p for x in a]
    degree = len(modulus) - 1
    if degree <= 0:
        raise ValueError("modulus must have positive degree")
    while len(out) >= len(modulus):
        coeff = out[-1] % p
        if coeff:
            offset = len(out) - len(modulus)
            for i in range(degree):
                out[offset + i] = (out[offset + i] - coeff * modulus[i]) % p
        out.pop()
    return _poly_trim(out or [0])


def _poly_mul_mod(a: list[int], b: list[int], modulus: list[int], p: int) -> list[int]:
    product = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                product[i + j] = (product[i + j] + x * y) % p
    return _poly_mod(product, modulus, p)


def _poly_pow_mod(base: list[int], exponent: int, modulus: list[int], p: int) -> list[int]:
    result = [1]
    base = _poly_mod(base, modulus, p)
    while exponent:
        if exponent & 1:
            result = _poly_mul_mod(result, base, modulus, p)
        base = _poly_mul_mod(base, base, modulus, p)
        exponent >>= 1
    return result


def _poly_divmod(a: list[int], b: list[int], p: int) -> tuple[list[int], list[int]]:
    a = _poly_trim([x % p for x in a])
    b = _poly_trim([x % p for x in b])
    if b == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [0] * max(1, len(a) - len(b) + 1)
    inv_lead = pow(b[-1], -1, p)
    while len(a) >= len(b) and a != [0]:
        coeff = a[-1] * inv_lead % p
        offset = len(a) - len(b)
        quotient[offset] = coeff
        for i, value in enumerate(b):
            a[offset + i] = (a[offset + i] - coeff * value) % p
        _poly_trim(a)
    return _poly_trim(quotient), a


def _poly_gcd(a: list[int], b: list[int], p: int) -> list[int]:
    a = _poly_trim([x % p for x in a])
    b = _poly_trim([x % p for x in b])
    while b != [0]:
        _, remainder = _poly_divmod(a, b, p)
        a, b = b, remainder
    inv = pow(a[-1], -1, p)
    return [(x * inv) % p for x in a]


def _is_irreducible(poly: list[int], p: int) -> bool:
    """Rabin irreducibility test for a monic polynomial over F_p."""
    degree = len(poly) - 1
    x_poly = [0, 1]
    if _poly_sub(_poly_pow_mod(x_poly, p**degree, poly, p), x_poly, p) != [0]:
        return False
    for divisor in _prime_divisors(degree):
        test = _poly_sub(_poly_pow_mod(x_poly, p ** (degree // divisor), poly, p), x_poly, p)
        if len(_poly_gcd(poly, test, p)) > 1:
            return False
    return True


def _find_irreducible_polynomial(p: int, degree: int) -> list[int]:
    if degree == 1:
        return [0, 1]
    for packed in range(1, p**degree):
        coeffs = []
        x = packed
        for _ in range(degree):
            coeffs.append(x % p)
            x //= p
        if coeffs[0] == 0:
            continue
        candidate = coeffs + [1]
        if _is_irreducible(candidate, p):
            return candidate
    raise ValueError(f"could not find an irreducible polynomial over F_{p}")


class PrimePowerField:
    """Tiny finite field F_q implementation for odd prime powers.

    Elements are integers 0..q-1 encoding polynomial coefficients in base p.
    This is intentionally small and boring: it is enough to build the Paley
    character tables without requiring Sage or another CAS.
    """

    def __init__(self, q: int):
        p, exponent = _prime_power_decomposition(q)
        if p == 2:
            raise ValueError("q must be odd")
        self.q = q
        self.p = p
        self.exponent = exponent
        self.modulus = _find_irreducible_polynomial(p, exponent)
        self._powers = np.array([p**i for i in range(exponent)], dtype=np.int64)
        self.coeffs = self._coeff_table()
        self.neg = np.array([self._pack((-row) % p) for row in self.coeffs], dtype=np.int32)
        self.add = self._add_table()
        self.sub = self.add[:, self.neg]
        self.mul = self._mul_table()

    def _coeff_table(self) -> np.ndarray:
        rows = np.zeros((self.q, self.exponent), dtype=np.int16)
        for value in range(self.q):
            x = value
            for i in range(self.exponent):
                rows[value, i] = x % self.p
                x //= self.p
        return rows

    def _pack(self, coeffs: np.ndarray | list[int]) -> int:
        return int(np.dot(np.asarray(coeffs, dtype=np.int64), self._powers))

    def _add_table(self) -> np.ndarray:
        table = np.empty((self.q, self.q), dtype=np.int32)
        for a in range(self.q):
            sums = (self.coeffs[a] + self.coeffs) % self.p
            table[a] = [self._pack(row) for row in sums]
        return table

    def _mul_coeffs(self, a: int, b: int) -> list[int]:
        degree = self.exponent
        product = [0] * (2 * degree - 1)
        for i, x in enumerate(self.coeffs[a]):
            if x:
                for j, y in enumerate(self.coeffs[b]):
                    product[i + j] = (product[i + j] + int(x) * int(y)) % self.p
        reduced = _poly_mod(product, self.modulus, self.p)
        return reduced + [0] * (degree - len(reduced))

    def _mul_table(self) -> np.ndarray:
        table = np.empty((self.q, self.q), dtype=np.int32)
        for a in range(self.q):
            for b in range(self.q):
                table[a, b] = self._pack(self._mul_coeffs(a, b))
        return table

    def pow(self, value: int, exponent: int) -> int:
        result = 1
        base = value
        while exponent:
            if exponent & 1:
                result = int(self.mul[result, base])
            base = int(self.mul[base, base])
            exponent >>= 1
        return result


def _chi(field: PrimePowerField, x: int) -> int:
    """Quadratic character on F_q, with chi(0) = 0."""
    if x == 0:
        return 0
    return 1 if field.pow(x, (field.q - 1) // 2) == 1 else -1


def _psi(value: int) -> np.ndarray:
    """Map 0, +1, -1 to the 2x2 signed blocks used in Paley II."""
    if value == 0:
        return Z
    return P if value == 1 else -P


def _k_matrix(field: PrimePowerField, t: int) -> np.ndarray:
    """The 2q x 2q Paley-II block matrix K_t."""
    q = field.q
    out = np.empty((2 * q, 2 * q), dtype=np.int8)
    for x in range(q):
        for y in range(q):
            y_minus_x = int(field.sub[y, x])
            value = int(field.sub[y_minus_x, t])
            out[2 * x:2 * x + 2, 2 * y:2 * y + 2] = _psi(_chi(field, value))
    return out


def _border_matrices(q: int, k0: np.ndarray) -> list[np.ndarray]:
    """Rank-2-row border blocks B_r extracted from the two rows over point r."""
    out = []
    for r in range(q):
        even_row = k0[2 * r]
        odd_row = k0[2 * r + 1]
        block = np.empty((2 * q, 2 * q), dtype=np.int8)
        block[0::2] = even_row
        block[1::2] = odd_row
        out.append(block)
    return out


def _paley2_small(field: PrimePowerField) -> np.ndarray:
    """Paley-II Hadamard matrix of order 2(q+1)."""
    q = field.q
    size = q + 1
    conference = np.zeros((size, size), dtype=np.int8)
    for a in range(size):
        for b in range(size):
            if a == b:
                value = 0
            elif a == 0 or b == 0:
                value = 1
            else:
                value = _chi(field, int(field.sub[b - 1, a - 1]))
            conference[a, b] = value

    return np.block([
        [_psi(int(conference[a, b])) for b in range(size)]
        for a in range(size)
    ]).astype(np.int8, copy=False)


def _cap_rows(field: PrimePowerField) -> np.ndarray:
    """The missing 2q-row cap that completes the Scarpis-style finite rows."""
    q = field.q
    small = _paley2_small(field)
    rows = []
    for g in range(1, q + 1):
        rows.extend([2 * g, 2 * g + 1])

    cap = []
    for row_index in rows:
        pieces = [np.tile(small[row_index, 0:2], q)]
        for g in range(1, q + 1):
            pair = (small[row_index, 2 * g:2 * g + 2] @ R90).astype(np.int8)
            pieces.append(np.tile(pair, q))
        cap.append(np.concatenate(pieces))
    return np.array(cap, dtype=np.int8)


def paley2_scarpis_hadamard(q: int, *, verify: bool = False) -> np.ndarray:
    """Return a +/-1 Hadamard matrix of order 2*q*(q+1), for prime-power q == 1 mod 4.

    TL;DR construction:
    - Work over the finite field F_q. This is the Djokovic/Scarpis move:
      replace integer arithmetic by field arithmetic so the same affine
      indexing identities still hold for prime powers.
    - Paley II replaces the 0,+1,-1 entries of the q == 1 mod 4 conference
      matrix by 2x2 blocks Z, P, -P, giving a small H_{2(q+1)}.
    - For each t in F_q, K_t is the same 2x2 block lift of chi(y-x-t).
      These blocks have the right "almost orthogonal" Gram matrix, but with
      a repeated-row defect R = J_q tensor I_2.
    - The finite Scarpis rows are [B_r | K_{0*r} | K_{1*r} | ... | K_{a*r} | ...],
      with a ranging over F_q.
      The B_r border block cancels the R defect between different r values.
    - A final 2q-row cap is cut from the small Paley-II matrix, with each finite
      column pair rotated by R90 and repeated q times. This supplies the missing
      rows orthogonal to all finite Scarpis rows.

    The result is a deterministic q == 1 mod 4 analogue of the Scarpis lift:
    it targets order 2q(q+1), the Paley-II analogue of q(q+1).
    """
    if q % 4 != 1:
        raise ValueError("q must satisfy q == 1 mod 4")

    field = PrimePowerField(q)
    k_mats = [_k_matrix(field, t) for t in range(q)]
    borders = _border_matrices(q, k_mats[0])
    finite_rows = [
        np.hstack([borders[r]] + [k_mats[int(field.mul[i, r])] for i in range(q)])
        for r in range(q)
    ]
    h = np.vstack([_cap_rows(field)] + finite_rows).astype(np.int8, copy=False)

    if verify:
        assert is_hadamard(h), "construction did not verify as Hadamard"
    return h


def _chi_values(field: PrimePowerField) -> np.ndarray:
    return np.array([_chi(field, x) for x in range(field.q)], dtype=np.int8)


def _psi_row(character: int, bit: int) -> np.ndarray:
    if character == 0:
        return Z[bit]
    if character == 1:
        return P[bit]
    return (-P)[bit]


def _k_streamed_row(
    field: PrimePowerField,
    chi_values: np.ndarray,
    *,
    t: int,
    x: int,
    bit: int,
) -> np.ndarray:
    """Return one row of K_t without building K_t."""
    q = field.q
    out = np.empty(2 * q, dtype=np.int8)
    for y in range(q):
        y_minus_x = int(field.sub[y, x])
        value = int(field.sub[y_minus_x, t])
        out[2 * y:2 * y + 2] = _psi_row(int(chi_values[value]), bit)
    return out


class Paley2ScarpisRowSampler:
    """Generate and test selected rows without materializing the full matrix.

    A full matrix has order N = 2q(q+1), so storing H costs O(N^2). This class
    stores only GF(q) tables, O(q^2), and creates O(N)-length rows on demand.
    """

    def __init__(self, q: int):
        if q % 4 != 1:
            raise ValueError("q must satisfy q == 1 mod 4")
        self.q = q
        self.n = 2 * q * (q + 1)
        self.field = PrimePowerField(q)
        self.chi_values = _chi_values(self.field)

    def row(self, index: int) -> np.ndarray:
        """Return row ``index`` of H as a +/-1 int8 vector of length N."""
        if not 0 <= index < self.n:
            raise IndexError(f"row index must be in 0..{self.n - 1}")

        q = self.q
        if index < 2 * q:
            return self._cap_row(index)

        finite_index = index - 2 * q
        r = finite_index // (2 * q)
        local = finite_index % (2 * q)
        x = local // 2
        bit = local % 2

        pieces = [
            _k_streamed_row(self.field, self.chi_values, t=0, x=r, bit=bit)
        ]
        for a in range(q):
            t = int(self.field.mul[a, r])
            pieces.append(_k_streamed_row(self.field, self.chi_values, t=t, x=x, bit=bit))
        return np.concatenate(pieces).astype(np.int8, copy=False)

    def rows(self, indices: list[int] | np.ndarray) -> np.ndarray:
        """Return a stacked matrix containing only the requested rows."""
        return np.vstack([self.row(int(index)) for index in indices]).astype(np.int8, copy=False)

    def dot(self, left: int, right: int) -> int:
        """Return the exact dot product of two streamed rows."""
        a = self.row(left).astype(np.int32, copy=False)
        b = self.row(right).astype(np.int32, copy=False)
        return int(a @ b)

    def sample_indices(self, count: int = 48, *, seed: int = 0) -> list[int]:
        """Choose deterministic row indices that cover cap, boundaries, and random rows."""
        rng = np.random.default_rng(seed)
        fixed = {
            0,
            1,
            2 * self.q - 1,
            2 * self.q,
            2 * self.q + 1,
            self.n // 3,
            self.n // 2,
            self.n - 2,
            self.n - 1,
        }
        if count <= len(fixed):
            return sorted(fixed)[:count]

        needed = count - len(fixed)
        random_rows = set(int(x) for x in rng.integers(0, self.n, size=max(needed * 3, 1)))
        while len(fixed | random_rows) < count:
            random_rows.add(int(rng.integers(0, self.n)))
        extras = [row for row in sorted(random_rows) if row not in fixed]
        return sorted(list(fixed) + extras[:needed])

    def test_sample(
        self,
        count: int = 48,
        *,
        seed: int = 0,
        indices: list[int] | np.ndarray | None = None,
        max_failures: int = 10,
    ) -> dict:
        """Test all pairwise dot products among a sampled row set.

        The returned dictionary is small and JSON-friendly. It includes the
        maximum absolute Gram error over the sampled rows, plus up to
        ``max_failures`` explicit failures.
        """
        chosen = [int(x) for x in (indices if indices is not None else self.sample_indices(count, seed=seed))]
        chosen = sorted(dict.fromkeys(chosen))
        sampled_rows = {index: self.row(index).astype(np.int32, copy=False) for index in chosen}

        max_error = 0
        failures = []
        pairs_tested = 0
        for pos, left in enumerate(chosen):
            for right in chosen[pos:]:
                expected = self.n if left == right else 0
                observed = int(sampled_rows[left] @ sampled_rows[right])
                error = abs(observed - expected)
                max_error = max(max_error, error)
                pairs_tested += 1
                if error and len(failures) < max_failures:
                    failures.append({
                        "left": left,
                        "right": right,
                        "expected": expected,
                        "observed": observed,
                    })

        return {
            "q": self.q,
            "order": self.n,
            "rows_tested": len(chosen),
            "pairs_tested": pairs_tested,
            "max_abs_error": max_error,
            "ok": max_error == 0,
            "indices": chosen,
            "failures": failures,
        }

    def _cap_row(self, index: int) -> np.ndarray:
        q = self.q
        element = index // 2
        bit = index % 2
        pieces = [np.tile(P[bit], q)]
        for y in range(q):
            if y == element:
                pair = Z[bit]
            else:
                value = int(self.field.sub[y, element])
                pair = _psi_row(int(self.chi_values[value]), bit)
            pieces.append(np.tile(pair @ R90, q))
        return np.concatenate(pieces).astype(np.int8, copy=False)


def sample_row_test(q: int, count: int = 48, *, seed: int = 0) -> dict:
    """Convenience wrapper for sampled row-dot testing without building H."""
    return Paley2ScarpisRowSampler(q).test_sample(count=count, seed=seed)


def is_hadamard(h: np.ndarray) -> bool:
    """Return True when h is a square +/-1 Hadamard matrix."""
    if h.ndim != 2 or h.shape[0] != h.shape[1]:
        return False
    if not np.isin(h, (-1, 1)).all():
        return False
    n = h.shape[0]
    gram = h.astype(np.int32) @ h.astype(np.int32).T
    return bool(np.array_equal(gram, n * np.eye(n, dtype=np.int32)))


if __name__ == "__main__":
    for order in (5, 9, 13, 17, 25, 73):
        h_matrix = paley2_scarpis_hadamard(order, verify=True)
        print(f"q={order}: built Hadamard order {h_matrix.shape[0]}")
        import numpy as np
        import numpy.linalg as nl
        h_matrix = h_matrix.astype(np.int32)
        print(f"||HH'-2q(q+1)I|| = {nl.norm(h_matrix@h_matrix.T - h_matrix.shape[0]*np.eye(h_matrix.shape[0])):5.3e}")
        print(f"{h_matrix.shape[0]:8d} {2*order*(order+1):8d}; agree? {h_matrix.shape[0]==2*order*(order+1)}")
        print(f"{set(h_matrix.flatten())}")
        print(f"-"*50)
