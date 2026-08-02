#!/usr/bin/env python3
"""Regenerate images/q5_side_by_side.png: this note's q=5 matrix (left)
next to Farouk-Wang's printed order-60 example (right).

Inputs (this directory): H_note_q5.txt, H_fw.txt.
Both are validated as order-60 Hadamard matrices before plotting.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "paper", "images", "q5_side_by_side.png")


def load(path):
    M = np.loadtxt(path, dtype=np.int64)
    assert M.shape == (60, 60), M.shape
    assert set(np.unique(M)) <= {-1, 1}
    G = M @ M.T
    assert np.array_equal(G, 60 * np.eye(60, dtype=np.int64)), "Gram check failed"
    return M


H_note = load(os.path.join(HERE, "H_note_q5.txt"))
H_fw = load(os.path.join(HERE, "H_fw.txt"))

q, N = 5, 60
fig, axes = plt.subplots(1, 2, figsize=(11.4, 5.6))
titles = [
    r"This note: $H$ of Theorem 1, $q=5$, $N=60$",
    r"Farouk–Wang (2020): printed example $\Psi_{5,\alpha}(P_5')$",
]
for ax, M, title in zip(axes, [H_note, H_fw], titles):
    ax.imshow(M, cmap="gray", vmin=-1, vmax=1, interpolation="nearest")
    for k in range(1, q + 2):
        z = 2 * q * k - 0.5
        if z < N - 0.5:
            ax.axvline(z, color="#d6336c", lw=0.35, alpha=0.5)
            ax.axhline(z, color="#d6336c", lw=0.35, alpha=0.5)
    ax.axhline(2 * q - 0.5, color="#e8590c", lw=1.6)
    ax.axvline(2 * q - 0.5, color="#1971c2", lw=1.6)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("white $=+1$, black $=-1$; lattice spacing $2q=10$", fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout()
fig.savefig(OUT, dpi=150, bbox_inches="tight")
print("wrote", os.path.normpath(OUT))
