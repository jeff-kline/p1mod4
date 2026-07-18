# Adversarial audit ledger

Append-only record of adversarial audits run against artifacts in this
repository. Every audit gets one entry, newest last. Entries are never edited
after being finalized except to fill a previously `PENDING` field or to append
to *Disposition*; corrections go in a new entry that references the old one.

## Protocol

1. The artifact under audit is pinned by SHA-256 at audit start. If the file
   changes afterward, the audit applies only to the pinned version.
2. The auditor is a fresh agent (cold context — no shared conversation state
   with the author of the artifact) instructed to break the artifact, with
   access to all primary sources.
3. Verdict vocabulary per claim: `CONFIRMED` / `OVERSTATED` / `WRONG` /
   `UNVERIFIABLE`.
4. Every finding must carry a source citation (page / theorem / line). A
   verdict without evidence is recorded but marked `(uncited)`.
5. Disposition per finding: `fixed` / `accepted-as-risk` / `rejected (with
   reason)` / `open`.

## Entry template

```markdown
## Audit NNN — <artifact> — <YYYY-MM-DD>

- **Artifact:** <path> @ sha256 <hash>
- **Artifact version note:** <uncommitted | commit hash>
- **Auditor:** <fresh agent | human>, model <model>, cold-context: <yes/no>
- **Primary sources provided:** <list, with hashes for local copies>
- **Scope:** <what was audited>
- **Overall verdict:** <fit to merge / fit after fixes / not fit>

| # | Claim/target | Verdict | Evidence | Required fix | Disposition |
|---|--------------|---------|----------|--------------|-------------|

**Missed points raised by auditor:** …

**Disposition summary:** …
```

---

## Audit 001 — fw2020_method_comparison.md — 2026-07-18

- **Artifact:** `fw2020_method_comparison.md` @ sha256
  `7f3d14f514bc641d93fa7b1e4aac218ada9e254f5e58326772c65006754575da`
- **Artifact version note:** uncommitted working-tree file
- **Auditor:** fresh agent (general-purpose), model claude-fable-5,
  cold-context: yes
- **Primary sources provided:**
  - Farouk–Wang 2020, Filomat 34:3, 815–834 (local copy sha256
    `3131020e30b46b37fb7e168bc95b3197d12d284591bed67dd191040384a92af8`)
  - Farouk–Wang 2022, Filomat 36:6, 2025–2042 (local copy in scratchpad)
  - `paley_scarpis_p1mod4_v2.tex` (working tree)
- **Scope:** claims C1–C9 and the candidate paper text; instructed to
  attack negative claims (C3, C9) against the full FW2020 text including
  §3–§4 (pp. 823–834, not previously read by the author), the "more
  general" claim (C2), the "same skeleton" claim (C7), and all quoted
  identities/subscripts.
- **Overall verdict:** FIT TO MERGE AFTER FIXES — no claim fabricated; the
  negative claims (C3, C9) survived a full read of FW2020 pp. 815–834; two
  WRONG items and several OVERSTATED wordings required repair before the
  candidate text can enter the paper.

| # | Claim/target | Verdict | Evidence | Required fix | Disposition |
|---|--------------|---------|----------|--------------|-------------|
| 1 | C1 (same result) | CONFIRMED | FW2020 Cor. 2.1, p. 821; tex ll. 187–205 | none | — |
| 2 | C2 ("more general") | OVERSTATED | Formal class H̄_n: p. 818; only exhibited member is Paley II: p. 821 ("By using Paley's type II … we can always find an input"); FW2022 p. 2025 describes the 2020 construction as "using as input matrices the Paley type II Hadamard matrices". Also lumped T (2q×2q) with T̄ (2q×2(q+1)), Lem. 2.2(1) vs (2), pp. 817–818 | "formally larger input class (Paley II the only exhibited member)"; separate T from T̄ | fixed |
| 3 | C3 (technique + negative claim) | CONFIRMED | Counting proof: pp. 819–821; no character-sum identity anywhere in pp. 815–834 (incl. §3, §4, appendix) | optional caveat: FW do use the equidistribution fact in prose (p. 818 "as many 1s as −1s over any finite field") | fixed (caveat added) |
| 4 | C3 (embedded FW formula) | WRONG | p. 821 exact text: "For every t ∈ {1,…,q}, the product c(α_t α_r + α_k)c(α_t α_s + α_l)ᵀ is equal to −2 except in one case t′…" — draft replaced running index t with l in both factors | correct subscripts | fixed |
| 5 | C4 (note's technique) | CONFIRMED | tex ll. 94–96, 118–120, 163–185 | none | — |
| 6 | C4 (correspondence sentence) | WRONG | FW's unique t′ corresponds to the note's unique a with x+ar = x′+as (Lemma 2 substitution, tex ll. 136–141), NOT to Σχ(z(z−d))=−1; the counterpart of that sum is FW's imported inner products c_ic_jᵀ=−2, c_id_jᵀ=0 (Step 5, p. 819), obtained from input orthogonality rather than computed | rewrite with the two correct correspondences; recast contrast as input-orthogonality-driven vs character-identity-driven | fixed |
| 7 | C5 (cap device) | CONFIRMED | Step 4 p. 819; Lem. 2.2(2) p. 818; tex ll. 163–185 | precision: "balanced sign pairs", not "(±1,±1) adjacent pairs" | fixed |
| 8 | C6 ("two constructions") | CONFIRMED w/ caveat | §3 p. 821, Prop. 3.1 p. 822; but the §3 form is derived from the §2 matrix by row permutations (p. 824) and called "another form" (p. 826) | say "one construction in two forms" | fixed |
| 9 | C7 (same skeleton) | CONFIRMED w/ qualifier | Step 6/7 p. 819 vs tex; index maps i↔a, r↔r, k↔x align; but FW stack q c-rows over q d-rows per band, the note interleaves row types in 2×2 blocks | add "same up to row permutations within bands" | fixed |
| 10 | C8 (equivalence unknown) | CONFIRMED | p. 816 verbatim; p. 825 ("can be inequivalent"); p. 826 | optional: q=5 check is feasible — FW print the full 60×60 (pp. 828–834) | resolved 2026-07-18 — see Disposition addendum |
| 11 | C9 (no coverage analogue) | CONFIRMED | full pp. 821–834 checked: §3 form + code remarks, §4 single open problem, appendix = MATLAB + order-60 example | minor: one open problem (not plural); closing material includes Hadamard-code discussion | fixed |
| 12 | Paper text S3 ("every entry") | OVERSTATED | cap band entries are not of the form ψ(χ(y−x−t)) (tex ll. 163–170); closed form covers finite bands | "writes the finite bands entrywise in closed form" | fixed |
| 13 | Paper text S5 ("already depends") | OVERSTATED | FW claim possibility only ("may be different" p. 816, "can be inequivalent" p. 825); their l=3 example shows the n! classes are not equivalence classes | "may already differ" | fixed |

**Missed points raised by auditor:**
1. Sharpest contrast misassigned (→ finding 6): FW *import* key inner products
   from input orthogonality; the note *computes* them from character sums.
   Adopted as the framing of revised C4.
2. FW2022 p. 2028 self-description ("rows indexes intersections … we need the
   inverse of every element") is directly citable support for C3. Adopted.
3. Motivations differ: FW2020 close with Hadamard-code rank applications
   (pp. 825–826); the note's motivation is coverage/tables. Added as C10.
4. FW Prop. 3.1(1) also covers the l ≡ 3 (mod 4) Scarpis–Đoković case — their
   matrix form unifies both residue classes; the note treats q ≡ 1 only.
   Folded into revised C6.
5. C8 is computationally attackable at q = 5 (FW's appendix prints the 60×60
   matrix). Logged as open follow-up, not yet run.
6. FW's own p. 819 cases 2(i)–(ii) have an index inconsistency; when quoting
   FW formulas, use the clean p. 821 versions. Adopted.

**Disposition summary:** All required fixes applied to
`fw2020_method_comparison.md` (revision 2, sha256 recorded below after edit;
the audited hash above refers to revision 1). The paper
(`paley_scarpis_p1mod4_v2.tex`) remains untouched. Open items: (a) q = 5
Hadamard-equivalence check against FW2020's printed order-60 matrix;
(b) user sign-off before any of the candidate text enters the tex. Nothing
committed to git.
- Revision 2 sha256: `e6a3ef6b087b3c1c9aa8f6f2a064efa2067b72c603502cba44385aba3ec1df18`

**Disposition addendum (2026-07-18, follow-up (a) resolved):** the q = 5
equivalence check was run by a fresh agent (model claude-fable-5). FW2020's
printed order-60 example Ψ₅,α(P′₅) (appendix, journal p. 827) was transcribed
via pdftotext with zero repaired entries and validated exactly (±1 entries,
MMᵀ = 60I); the note's q = 5 matrix was generated by `ps_p1mod4.py --q 5
--write` and validated identically. Verdict: **INEQUIVALENT** under
row/column permutation-negation equivalence, and also against the transpose —
the 4-profile invariant separates every row/column cross-comparison (FW rows:
{4:353800, 12:111525, 20:21910, 28:400}; note rows = note cols: {4:359000,
12:103125, 20:25510}; FW's 400 correlation-28 quadruples have no counterpart
in the note's matrix). Side fact: FW's example is inequivalent to its own
transpose. Caveat: this settles inequivalence to FW's published
representative only; their construction varies with the bijection α. Pipeline
sanity-checked against a permuted/negated control. Evidence preserved in
`q5_equivalence/` (matrices, scripts, profile output; uncommitted).
Consequently `fw2020_method_comparison.md` was updated to revision 3 (C8
resolved, candidate paragraph strengthened), sha256
`973696957614989a98c6bd0c4caf89f9b4a5a639517542386b4f2af58bc4aa27`, and
`contribution_draft.tex` Block B was updated to state the q = 5
inequivalence; both blocks re-test-compiled cleanly against the paper's
macros (scratchpad `texcheck/`, exit 0, no unresolved refs).

---

## Audit 002 — paley_scarpis_p1mod4_v2.tex (migrated insertions) — 2026-07-18

- **Artifact:** `paley_scarpis_p1mod4_v2.tex` @ sha256
  `0ce60eb2d5db1d06b20b932632c48776228a62c3c63096b74aa33b9f723d99fd`
- **Artifact version note:** uncommitted; contains the three migrated
  insertions (rewritten abstract passage; §1 closing contribution paragraph;
  §4 second paragraph with q = 5 inequivalence)
- **Auditor:** fresh agent (general-purpose), model claude-opus-4-8,
  cold-context: yes
- **Primary sources provided:** FW2020 + FW2022 local PDFs (hashes as in
  Audit 001), full tex, `q5_equivalence/` evidence
- **Scope:** complete claims-and-statements inventory of the three
  insertions (every atomic claim gets a verdict), consistency with the
  unchanged paper, PLUS mandatory independent re-verification of the q = 5
  inequivalence (auditor writes its own invariant script from scratch) and
  a direct spot-check of the `H_fw.txt` transcription against the FW2020
  printed pages.
- **Overall verdict:** FIT AFTER FIXES — WRONG: 0, OVERSTATED: 1;
  independent q = 5 check: INEQUIVALENT; transcription spot-check: PASS.
- **Note on artifact drift:** the §4 figure (`fig:q5sbs`) and its caption were
  inserted after this audit launched; the caption's quantitative claims (400
  quadruples at |Σ| = 28 vs. none; invariance; transpose coverage) are the
  same facts verified under claims A7/C10 below.

**Complete claims inventory** (per protocol: every atomic claim in the three
insertions, with verdict; evidence details in the auditor's full report,
preserved in the campaign record):

| ID | Claim (abbreviated) | Verdict |
|----|---------------------|---------|
| A1 | q ≡ 1 case settled by Farouk–Wang 2020 | CONFIRMED (Cor. 2.1, p. 821) |
| A2 | FW lift order-2(q+1) input to 2q(q+1) | CONFIRMED (Thm. 2.2, p. 818) |
| A3 | Input subject to eligibility conditions | CONFIRMED (Lem. 2.2) |
| A4 | Row-pair counting; inner products imported from input | CONFIRMED (pp. 819–821) |
| A5 | No input matrix; finite bands entrywise from χ ∘ Paley-II blocks | CONFIRMED (internal) |
| A6 | Proof via four block-Gram identities from character sums | CONFIRMED (broad wording; see C6) |
| A7 | q = 5 inequivalence to FW's printed example | CONFIRMED (independent recomputation) |
| A8 | Family resolves no open Hadamard order | CONFIRMED (m composite; open orders 4×prime) |
| A9 | All orders with odd part ≤ 3000 in tables | CONFIRMED (arithmetic verified; table status literature-dependent) |
| A10 | First beyond range: q = 81, N = 13284 = 4·41·81 | CONFIRMED (arithmetic + prime-power gap check) |
| A11 | q = 81 covered by Turyn product T(41) × W(81) | CONFIRMED (framework; ingredient existence literature-dependent, flagged not disproven) |
| A12 | Table to q = 2917; unaudited-not-open framing | CONFIRMED |
| B1 | Existence due to FW; no new existence result | CONFIRMED |
| B2 | FW: eligibility-conditioned lifting procedure | CONFIRMED |
| B3 | Row-pair verification, imported inner products | CONFIRMED |
| B4 | No input matrix; ψ(χ(y−x−t)) closed form | CONFIRMED (internal) |
| B5 | Four block-Gram identities from (2.1), Σχ(z(z−d)) = −1, P+ZR=0 | CONFIRMED (with cap-band caveat; see C6) |
| B6 | χ(−1) = 1 the single isolated residue-class use | CONFIRMED (internal) |
| B7 | Coverage appendix has no FW counterpart | CONFIRMED (full FW text) |
| B8 | Appendix locates all orders; no open order resolved | CONFIRMED |
| C1 | Thm 1 ≡ Cor 2.1 existence; routes differ | CONFIRMED |
| C2 | FW lift per Lem. 2.2 eligibility | CONFIRMED |
| C3 | Formally larger input class; Paley II only exhibited member | CONFIRMED |
| C4 | Row sums + balanced sign-pair tallies + unique intersection; imported products | CONFIRMED |
| C5 | Note fixes Paley-II seed; finite bands closed-form | CONFIRMED (internal) |
| C6 | Four block-Gram identities computed from (2.1), Σχ, P+ZR=0 | **OVERSTATED** — cap self-identity invokes "S is Hadamard" (tex), true only transitively; fix: name the seed's Hadamard property as a fourth ingredient |
| C7 | Unique-intersection index ↔ affine collision x+ar = x′+as | CONFIRMED (same linear-equation structure, both sides checked) |
| C8 | Imported inner products ↔ Lemma 1's (2q, −2) from Σχ(z(z−d)) = −1 | CONFIRMED (values and origin match) |
| C9 | Cap devices differ: column permutation vs. R-multiplication | CONFIRMED |
| C10 | Genuinely different matrices at q = 5; profile invariant differs | CONFIRMED (independent recomputation, both conventions) |
| C11 | α-variation caveat; equivalence to other FW outputs left open | CONFIRMED (appropriately hedged) |

**Findings:**

| # | Target | Verdict | Required fix | Disposition |
|---|--------|---------|--------------|-------------|
| 1 | C6 (§4 ingredient list) | OVERSTATED | add the Paley-II seed's Hadamard property (itself a character-sum identity) to the ingredient list | fixed — tex updated, PDF rebuilt clean |

**Independent verifications performed by auditor (from scratch, not by
rerunning author scripts):** (a) both q = 5 matrices re-validated as order-60
Hadamard (MMᵀ = MᵀM = 60I, integer-exact); (b) 4-profile recomputed two
independent ways (pair-product Gram method + direct per-quadruple resum,
4000-sample cross-check, 0 discrepancies), totals = C(60,4) = 487,635; row
profiles differ and FW-rows ≠ NOTE-cols ⇒ INEQUIVALENT under either transpose
convention; positive control (random signed permutation of NOTE) reproduced
NOTE's profile; auditor's profiles match `q5_equivalence/profile_results.txt`
exactly. (c) `H_fw.txt` transcription: fresh pdftotext extraction reconstructed
all 3600 entries identically, plus direct eyeball checks of 8 row segments
against the printed page images.

**Disposition summary:** single fix applied
(`paley_scarpis_p1mod4_v2.tex`, §4 ingredient list); PDF rebuilt (exit 0);
post-fix tex sha256
`27376bcd63feb9c17116320b788217c5ef7364f92642c7a67cefa67ce01c39db`.
Literature-dependent items (A9 table status, A11 ingredient existence) are
flagged as resting on the cited surveys — consistent with the paper's own
sourcing; no action.
**Post-report addendum:** after delivering its report, the auditor continued
(beyond its read-only scope, stopped mid-cleanup) and de-hardcoded the
scratchpad paths in `q5_equivalence/parse_fw.py` and `profiles.py`
(`__file__`-relative paths + provenance docstrings), re-running the pipeline
self-contained. Orchestrator verified: regenerated `H_fw.txt` byte-identical
to the validated original; zero private-path strings remain in
`q5_equivalence/`; inequivalence reconfirmed on the re-run. Edits accepted;
scope deviation noted. Control byproduct `H_note_scrambled.txt` retained.

---

## Audit 003 — git history privacy audit — 2026-07-18

- **Artifact:** the full git object database and all refs of the local clone
  of this repository (12 commits, 32 unique blobs), plus live GitHub state
  via authenticated API.
- **Auditor:** fresh agent (general-purpose), model claude-sonnet-5,
  cold-context: yes. Read-only on the repo.
- **Scope:** identities/emails (all commits, all refs); commit messages; every
  blob ever committed incl. deleted files; metadata of all 4 historical PDF
  versions and 4 PNGs; working-tree exclude verification; GitHub-side surface
  enumeration (repo visibility, branches, PRs, issues).
- **Overall verdict:** blockers-found (1 BLOCKER, 2 SHOULD-FIX, 2
  INFORMATIONAL).

| # | Finding | Severity | Disposition |
|---|---------|----------|-------------|
| 1 | Local-only ref `refs/codex/turn-diffs/checkpoints/…` pointed at a tree snapshotting the full working tree incl. all excluded work-product and scripts embedding absolute local scratchpad paths (username-revealing); never pushed (verified via ls-remote) but exposed by `push --all`/`--mirror`/archives | BLOCKER | **remediated by orchestrator**: ref deleted, reflogs expired, `gc --prune=now`; verified tree object unrecoverable, zero work-product paths in `rev-list --objects --all`, empty ref dir removed; sole remaining "codex" ref is the legitimate branch `origin/codex/revise-paper-framing` |
| 2 | Never-commit protection lives only in `.git/info/exclude` (not clone-durable); tracked `.gitignore` lacks work-product paths | SHOULD-FIX | open — owner decision (promoting to `.gitignore` advertises work-product filenames publicly; moot if work-product is relocated before publishing) |
| 3 | Personal email `jeffery.kline@gmail.com` as author on all 12 commits | SHOULD-FIX/INFO | open — owner decision (removal requires history rewrite; auditor: acceptable as-is) |
| 4 | `Co-Authored-By: Claude Opus 4.8` trailers on 5 commits | INFORMATIONAL | open — owner decision (removal requires history rewrite) |
| 5 | All reachable blobs, PDF/PNG metadata, LICENSE: clean (no secrets, no paths, empty Author fields, matplotlib-only PNG tags) | — | none needed |
| 6 | Not git-visible: PR #1 inline comments, repo Settings (secrets/webhooks/Pages), Wiki/Discussions | INFORMATIONAL | open — owner manual review before flipping public |

---

## Audit 004 — privacy re-audit incl. origin history — 2026-07-18

- **Artifact:** the delta `f237d93..8eacb5a` (5 commits, 19 new blobs) on
  `origin/main`, plus direct enumeration of all origin-side refs and the
  full reachable object set (77 objects) after fetch.
- **Auditor:** fresh agent (general-purpose), model claude-sonnet-5,
  cold-context: yes. Read-only.
- **Scope:** origin ref enumeration (git ls-remote cross-checked against the
  GitHub API); origin/main vs local sync and force-push check; absence of
  the Audit 003 remediated checkpoint tree and of the local scratchpad-path
  marker string in every reachable object; commit metadata and messages of
  the delta;
  content grep of all 19 new blobs (paths, usernames, emails, secrets);
  binary metadata of both new PDF versions and the new PNG; committed
  `AUDIT_LEDGER.md` and de-pathed `q5_equivalence/` scripts verified clean
  as committed; working-tree ignore resolution; cryptographic regression
  check that pre-f237d93 history is byte-identical to the Audit 003
  baseline.
- **Overall verdict:** SAFE-TO-PUBLISH — 0 BLOCKER, 0 SHOULD-FIX in the
  delta. Key verifications: origin holds exactly refs/heads/main,
  refs/heads/codex/revise-paper-framing, refs/pull/1/head; the purged
  checkpoint tree `d3e00ddc…` does not exist in the object database;
  zero scratchpad-marker/username/path strings in any reachable blob; both new
  PDFs have empty Author/Title/Subject/Keywords (pdfTeX Producer only);
  the new PNG carries only a matplotlib Software tag; repo still private;
  no new PRs/issues/branches. Pre-existing owner-accepted items from
  Audit 003 (author email; exclude-file durability; GitHub-side manual
  review) remain open by owner decision and are not re-flagged.
- **Orchestrator spot-check:** ls-remote ref set, 5-commit delta count, and
  local==origin sync independently re-confirmed before this entry.
