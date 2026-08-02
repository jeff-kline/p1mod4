# P1 prior-work and claim-boundary audit

**Status:** PASS for the bounded claim used in the paper

**Search date:** August 2, 2026

**Claim at risk:** the necessity direction of Theorem 2

**Confidence:** moderate, not exhaustive

## Admission question

For the specific block matrix `H(G, δ, T)` defined in Section 5, has an earlier
source proved the converse

```text
H(G, δ, T) Hadamard
    implies
δ is of Paley type and T is a (G,n;1)-difference matrix?
```

This is narrower than asking whether Paley-type partial difference sets,
difference matrices, generalized Hadamard matrices, or Scarpis-style lifts are
known. All four are prior work.

## Findings

1. **Existence at order `2q(q+1)` is prior work.** Farouk and Wang construct
   this order family from a Paley-II seed. The release claims a direct,
   choice-free formula, not a new order family.
2. **The forward construction is prior work in greater generality.** Seberry's
   generalized-Hadamard construction and Nuñez Ponasso's Theorem 4.3.3 show
   how a generalized Hadamard/difference matrix supplies the lifted Butson
   matrix. Sargent–Lee–Rushall give the corresponding complex Scarpis route.
3. **Difference-matrix and projective-plane correspondences are prior work.**
   Jungnickel's papers supply the standard bounds and the correspondence with
   regular complete sets of mutually orthogonal Latin squares.
4. **The converse was not located in the bounded corpus below.** The available
   de Launey and de Launey–Flannery material treats generalized Hadamard
   matrices, developed/cocyclic matrices, orthogonality sets, Gram properties,
   and construction/substitution schemes. No located theorem decomposes the
   Hadamard property of this particular `ψ(δ)` block layout and forces both the
   Paley autocorrelation equations and uniform differences in `T`.

The admitted wording is therefore **“apparently new within this bounded
corpus.”** The repository makes no claim of global priority.

## Primary and near-primary corpus

| Source | Mechanism inspected | Result for the claim boundary |
|---|---|---|
| [Farouk–Wang (2020)](https://doi.org/10.2298/FIL2003815F) | Real Paley-II lift to order `2q(q+1)` | Prior existence and closest real procedure; no converse located. Current publisher retrieval returned HTTP 503, so the audit also used the repository's provenance-preserving extract and earlier ledgered inspection. |
| [Farouk–Wang (2022)](https://doi.org/10.2298/FIL2206025F) | Eligible Latin-square arrays | Related shift-array abstraction; no necessity theorem for the present group-developed layout located. |
| [Seberry (1980)](https://doi.org/10.1016/0378-3758(80)90021-X) | Construction from generalized Hadamard matrices | Sufficiency/construction only. Full four-page article inspected. |
| [Nuñez Ponasso (arXiv:2404.09040v2)](https://arxiv.org/abs/2404.09040) | `BH(n+1,m)` plus `GH(n,G)` gives `BH(n(n+1),m)` | Sufficiency in greater generality; no converse. Full thesis version inspected, especially Theorem 4.3.3. |
| [Sargent–Lee–Rushall (2024)](https://doi.org/10.61091/jcmcc119-11) | Complex Scarpis construction | Constructive antecedent and equivalent Gaussian output; no converse. Full article inspected. |
| [Đoković (2016)](https://arxiv.org/abs/1601.00635) | Prime-power Scarpis theorem | Motivating lift for the other Paley residue class; no present converse. Full preprint inspected. |
| Jungnickel (1979, 1980) | Difference matrices, transversal designs, regular Latin squares | Standard difference-matrix bounds and equivalences; no `ψ(δ)` necessity statement located. |
| [de Launey (1992)](https://doi.org/10.1016/0012-365X(92)90624-O) | Generalized Hadamard matrices developed modulo a group | Developed-matrix constructions, equivalences, and nonexistence restrictions; no matching converse located in the accessible article record. |
| [de Launey, Handbook chapter (2007)](https://doi.org/10.1201/9781420010541) | Generalized Hadamard survey | Relevant definitions, existence landscape, and prime-power supply statement. Full chapter was not accessible in this session. |
| [de Launey–Flannery (2011)](https://doi.org/10.1090/surv/175) | Orthogonality sets, Gram properties, Paley and substitution chapters | The publisher's contents, index/end matter, and accessible chapter text/snippets were searched. Full monograph access was unavailable; no matching theorem was located. |
| [de Launey (1986)](https://combinatorialpress.com/um/vol30/) | Survey of generalized Hadamard and large difference matrices | Bibliographic record and indexed text searched; full article was not available from the journal archive. |

## Search protocol

The search combined exact phrases and mechanism terms rather than title-only
queries. Query families included:

- `"Paley type" "difference matrix" Hadamard`;
- `Scarpis generalized Hadamard converse`;
- `quadratic character difference matrix Hadamard construction`;
- `orthogonality set de Launey Flannery`;
- `Paley type partial difference set generalized Hadamard`;
- title/author searches for de Launey's 1986, 1992, and 2007 surveys and the
  de Launey–Flannery monograph;
- forward and backward browsing from Seberry, Jungnickel, and the accessible
  generalized-Hadamard surveys.

Exact-phrase searches for the joint Paley-type/difference-matrix mechanism
returned no matching theorem. Broader searches returned the standard objects
and construction results listed above, not the two-factor necessity statement.

## Limits and retraction trigger

- MathSciNet, zbMATH, and subscription-only full text were not available.
- The de Launey–Flannery monograph and de Launey's Handbook chapter were not
  read cover to cover; this is the main reason confidence is moderate.
- The Farouk–Wang publisher was temporarily unavailable during this pass.
- Terminology varies: “difference matrix,” “generalized Hadamard matrix,”
  “orthogonality set,” “developed matrix,” and “eligible Latin squares” do not
  index the same way.

Discovery of an earlier necessity theorem is an attribution correction, not a
failure of the proof or construction. It would require removing the novelty
wording from the abstract, introduction, README, and citation metadata, and
recording the correction in `CORRECTIONS.md`.
