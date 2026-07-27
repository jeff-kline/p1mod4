"""Parse the Farouk-Wang order-60 Hadamard matrix from pdftotext output and validate.

Provenance / reproducibility (self-contained within this directory):

    fw_appendix.txt  is a plain-text extraction of the printed order-60 example
    in the appendix of Farouk & Wang, "An infinite family of Hadamard matrices
    constructed from Paley type matrices", Filomat 34:3 (2020), 815-834
    (pp. 827-834). It was produced from the published PDF with

        pdftotext -layout -f <first> -l <last> farouk_wang_2020.pdf - \\
          | awk '/Columns [0-9]+ through [0-9]+/{p=1} p' > fw_appendix.txt

    Only the +-1 matrix data (as five "Columns a through b" blocks) is kept.
    Running this script regenerates H_fw.txt from fw_appendix.txt; H_fw.txt is
    also committed directly, so downstream scripts do not require the PDF.
"""
import os
import re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
txt = open(os.path.join(HERE, "fw_appendix.txt")).read().splitlines()

blocks = []          # list of (start_col, end_col, rows)
cur = None
for line in txt:
    m = re.match(r"\s*Columns (\d+) through (\d+)", line)
    if m:
        if cur is not None:
            blocks.append(cur)
        cur = (int(m.group(1)), int(m.group(2)), [])
        continue
    if cur is None:
        continue
    toks = line.split()
    if toks and all(t in ("1", "-1") for t in toks):
        cur[2].append([int(t) for t in toks])
if cur is not None:
    blocks.append(cur)

print("blocks found:")
cols_total = 0
for (a, b, rows) in blocks:
    widths = set(len(r) for r in rows)
    print(f"  cols {a}-{b}: {len(rows)} rows, widths {sorted(widths)}")
    assert len(rows) == 60, f"block {a}-{b} has {len(rows)} rows"
    assert widths == {b - a + 1}, f"block {a}-{b} width mismatch: {widths}"
    cols_total += b - a + 1
assert cols_total == 60, cols_total
assert [(a, b) for a, b, _ in blocks] == [(1,13),(14,26),(27,39),(40,52),(53,60)]

H = np.hstack([np.array(rows, dtype=np.int64) for _, _, rows in blocks])
assert H.shape == (60, 60)
assert set(np.unique(H)) <= {-1, 1}

G = H @ H.T
D = G - 60 * np.eye(60, dtype=np.int64)
bad = np.argwhere(D != 0)
if bad.size:
    print("GRAM DEFECTS (row pairs):")
    seen = set()
    for i, j in bad:
        if i < j:
            print(f"  rows {i},{j}: inner product {G[i,j]}")
    print(f"total off-diagonal defects: {len([1 for i,j in bad if i<j])}")
else:
    print("Gram check PASSED: H @ H.T == 60*I exactly")

Gc = H.T @ H
assert np.array_equal(Gc, 60 * np.eye(60, dtype=np.int64)) == (bad.size == 0)

np.savetxt(os.path.join(HERE, "H_fw.txt"), H, fmt="%d")
print("saved H_fw.txt")
print("row0 all ones:", np.all(H[0] == 1), " col0 all ones:", np.all(H[:,0] == 1))
