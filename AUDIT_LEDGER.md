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

---

## Scorecard 001 — repo-rank pass — 2026-07-26

- **Artifact:** full repository @ commit `19a69585ae9335872758d34e9db5565481f15113`
  (2026-07-19).
- **Method:** `repo-rank` skill — four independent cold agents (no shared
  context, no visibility into each other's scoring), one per axis (Novelty,
  Depth, Reach, Evidence), each instructed to search external literature
  and/or run the repo's own scripts rather than trust the paper's
  self-description. Numeric scores are intentionally not recorded here or
  anywhere in this repository (see the skill's own log for the private
  numeric record); this entry carries only the qualitative substance.
- **Overall read:** a self-consciously non-existence-result — the paper is
  explicit throughout that Farouk–Wang (2020) already proved existence at
  these orders. The scorecard axes therefore sit apart from the usual
  "new theorem" profile: methodological novelty is real but bounded, the
  proof is essentially complete with one presentation gap, the result is
  fully settled but cannot resolve any presently-open Hadamard order by
  its own arithmetic, and the computational evidence is unusually strong
  except for one unscripted table.

**Novelty.** The existence statement is verbatim Farouk–Wang's; what's new
is a choice-free, closed-form, entrywise construction from character sums
in place of Farouk–Wang's eligibility-conditioned lifting procedure (which
genuinely varies with an input matrix and a bijection α — verified against
the primary FW2020/FW2022 text, not just this repo's summary), backed by a
demonstrated non-equivalent output at q = 5. Lands mid-band: a real
structural simplification (a free parameter eliminated by two identities),
but the connecting argument substantially parallels FW's once unpacked, and
FW2022 Cor. 4.2 already identifies the same underlying affine skeleton.
*What would move it:* evidence the inequivalence persists at scale (not
just q = 5), or that no other choice-free variant exists in the wider
literature (a broader search than this pass ran).

**Depth.** The four block-Gram lemmas and the main theorem were re-derived
independently line-by-line and check out; the tiering of proved vs.
numerically-verified vs. literature-dependent claims (the coverage
appendix, the q = 81 Turyn witness) is stated honestly rather than blurred.
One soft spot: the column-alignment between the cap band and the finite
bands in the fourth lemma is disambiguated by the construction code
(`ps_p1mod4.py`) more crisply than by the prose. *What would move it:*
spelling out that alignment explicitly in the tex would remove the one
identified gap.

**Reach.** Fully settles the question the paper itself poses (a canonical,
choice-free representative where only a parameterized procedure existed),
with concrete partially-attacked follow-ons (the q = 5 inequivalence
question, the q = 81 coverage witness, the q = 109 gap named as the next
target). Structurally capped, and disclosed as such: the coverage argument
proves the family's orders are always 4×(composite), so it can never land
on a presently-open 4×prime Hadamard order. *What would move it:* an
extension to q ≡ 3 (mod 4) unifying with Đoković's case, or resolution of
the named q = 109 gap.

**Evidence.** The core numerical claims are unusually well supported:
exact-integer (not floating-point) Gram checks across the stated sweep,
independently reproduced by a cold auditor rather than merely re-run
(Audit 002); the q = 5 inequivalence check is full-scale (all C(60,4)
quadruples, not sampled), transcription-verified against the printed
source twice, and carries a positive control. One gap: the coverage
appendix's order-by-order divisor-split table (232 orders, 128 covered)
has no corresponding script anywhere in the repository — asserted as
computed, not reproducible here. *What would move it:* committing the
script that produced the coverage table.

**Disposition:** informational — no fixes required to merge; the two
"what would move it" items above (Depth's alignment prose, Evidence's
missing coverage script) are the only concrete, actionable gaps this pass
surfaced.

---

## Audit 005 — three proposed appendix/section additions (not merged) — 2026-07-27

- **Artifacts (none in this repository; all in an external scratchpad):**
  - lane 6 draft, "The construction over the Gaussian integers" @ sha256
    `7772b75c3eae6422903a07a1a5c804e2aa0bbad64fe625a0be6e7ab595d12223`
  - lane 4 draft, "What the construction needs" @ sha256
    `7ac65399f7f5b619cf05643352b317ff7c32c05d6c54e77b11720d581601b9bc`
  - lane 5 draft, "A second worked example: q = 109" @ sha256
    `6273b44a1e231e0611f2447a29f1d929dd53170601ad3a2859774532e87c3426`
- **Artifact version note:** uncommitted; external to this repository.
  **Nothing from these drafts has been merged into the paper.** This entry
  records the audit only.
- **Target paper pinned at:** `paley_scarpis_p1mod4_v2.tex` @ sha256
  `67c34a9f064752c6b7f2fb585b7fde8e82cd1c48c6dec07e92c86c7d7230920e`
  (commit c05ca65). The repository was read-only throughout; no file in it
  was modified by any auditor.
- **Auditors:** seven fresh agents, all cold-context: yes —
  six on a math/citations axis split (one pair per draft), model claude-opus-5;
  one further mathematics pass on the lane 6 draft, model claude-fable-5.
  Two additional non-audit agents performed build remediation (claude-sonnet-5).
- **Primary sources provided:** Sargent–Lee–Rushall, JCMCC 119 (2024) 105–111
  (local copy sha256 `de8c684b0f37cf56bfbdbe28086fc27367a0ec931b100107716f7e114c8a76d6`);
  Seberry–Yamada 1992, *Contemporary Design Theory* pp. 431–560 (local copy
  sha256 `01cec87b0b76e22b546bc4ed7160faed8c6680e2f7b70c438bbd92bb362f0c9c`);
  Egan–Ó Catháin arXiv:1707.08815; Heikoop et al. arXiv:1907.07024;
  Wang arXiv:1908.07055; Farouk–Wang, Filomat 36:6 (2022);
  Đoković arXiv:1008.2043 and arXiv:1002.1414; van Greevenbroek–Jedwab;
  Polhill 2009 (author copy).
- **Scope:** every theorem, proof, numeric claim and citation in the three
  proposed additions. Explicitly out of scope: the paper's existing sections.
- **Overall verdict:** FIT TO MERGE AFTER FIXES. One false statement and two
  instances of uncited borrowing were found and repaired in the drafts; no
  proposed theorem was broken. Merge remains gated pending Audit 006.

| # | Claim/target | Verdict | Evidence | Required fix | Disposition |
|---|--------------|---------|----------|--------------|-------------|
| 1 | lane 4 `cor:mod4`: δ of Paley type ⟹ Σδ=0, D regular, n ≡ 1 (mod 4) | WRONG | Counterexample on G = Z₃, δ = (1,−1,−1): satisfies the draft's written definition (A(d) = [3,−1,−1]) yet Σδ = −1, n ≡ 3 (mod 4), and 0 ∈ D so D is not regular; the proof's step δ = 2D̂ − Ĝ + 1 yields (2,−1,−1) ≠ δ. Instantiated independently by the coordinator | add `δ(0)=0` to the definition of "of Paley type" | fixed |
| 2 | lane 4 `cor:plane` first half, presented as the draft's own | OVERSTATED (uncited borrowing) | van Greevenbroek–Jedwab: "a (G, m, 1) difference matrix is equivalent to a G-regular set of m − 1 mutually orthogonal Latin squares of order \|G\| [Jun80, Theorem 1]" | cite Jungnickel, *Abh. Math. Sem. Hamburg* 50 (1980) 219–231, Thm 1 | fixed |
| 3 | lane 4 `rem:supply` scarcity claim, presented as the draft's own | OVERSTATED (uncited borrowing) | "In all known examples of a GH(\|G\|, λ) over G, the group order \|G\| is a prime power … [Lau07, p. 303]" — i.e. de Launey, *Generalized Hadamard matrices*, pp. 301–306 of the Handbook the draft already cited | cite the Handbook at p. 303 | fixed |
| 4 | lane 4: the `(G,n;1)`-difference matrix left unnamed | UNVERIFIABLE as written | The object is a generalized Hadamard matrix GH(n,1) over G, attaining Jungnickel's bound m ≤ λ\|G\| (*Math. Z.* 167 (1979) 49–60, Thm 2.2) | name it; cite Jungnickel 1979 | fixed |
| 5 | lane 4 `rem:q9`: order-180 inequivalence attributed to non-Desarguesianness | OVERSTATED | Band-relabelling the *Desarguesian* field difference matrix already yields inequivalent order-180 matrices (4-profile 44-counts 12960/17496/11664/11664/18144/18144 vs the paper's 0), while π = multiplication-by-c reproduces the paper's profile exactly | state that the nearfield supplies a canonical second choice, not the cause | fixed |
| 6 | lane 4: order 10 "excluded **only** by exhaustive computation" | OVERSTATED | Bright, Cheung, Stevens, Kotsireas, Ganesh (arXiv:2012.04715) produced machine-verifiable nonexistence certificates and report "consistency issues in both previous searches" | add the 2021 certificate-based resolution | fixed |
| 7 | lane 4 `thm:char` (the main proposed theorem), both directions | CONFIRMED | Re-derived independently from the paper's text before the draft's proof was read; necessity chain σ²+n₀²=1 → σ=0, n₀∈{0,1} → Paley type → μ_rs ≡ 1; exhaustive at n=5 (243/243), plus n=9, n=13; all 90 000 normalised (Z₅,5;1)-difference matrices give Hadamard output | none | — |
| 8 | lane 4 `cor:plane` n−1 vs n−2 MOLS off-by-one | CONFIRMED | Cross-checked by developing the difference matrix into an orthogonal array with n+1 factors, strength 2 index 1 on every pair, at n = 5, 9, 13, 25 and the order-9 nearfield | none | — |
| 9 | lane 6: the paper's H is the Turyn/Cohn double of a BH(q(q+1),4) | CONFIRMED | Read off the 2×2 blocks; every block lies in φ({±1,±i}); de-doubled Γ satisfies ΓΓ\* = nI and φ(Γ) = H exactly, verified against this repository's own `ps_p1mod4.py` at q = 5, 9, 13, 17, 25, and by a second implementation at q = 29, 37, 41, 49, 81, 121, 125 | none | — |
| 10 | lane 6: Γ **is** an output of Sargent–Lee–Rushall (2024) | OVERSTATED | The identity is SLR(N, delete ∞ row) = diag(I_q, i·I_{q²})·Γ, and that diagonal ≠ I; the scaling does lie in their equivalence group | "is equivalent to one of their outputs" | fixed |
| 11 | lane 6: SLR 2024 is closer prior art than Farouk–Wang, and Remark 2 claimed parity between the two comparisons | OVERSTATED | §4 of the paper (tex ll. 279–290) additionally asserts the paper's matrix is *not* Hadamard-equivalent to the Farouk–Wang example; against SLR the matrix is the **same** up to a diagonal row scaling, so that half does not carry over | state explicitly that no inequivalence claim is available against SLR | fixed |
| 12 | lane 6: the draft's reading of SLR Corollary 1 is "the only reading that makes the corollary true" | WRONG | Pairing seed column a with multiplier σ(a) for an arbitrary bijection σ also yields genuine complex Hadamard matrices (12/12 at q = 5, 9, 13). A q!-family of readings works | delete the uniqueness claim; justify the reading by SLR's printed subscript rule instead | fixed |
| 13 | lane 6: the general-q SLR identification | CONFIRMED | Reconstructed twice independently from SLR's printed Theorem 1 before the draft's derivation was read; exact agreement at q = 5, 9, 13, 17, 25, 29, 37, 41, 49, 81, 121, 125 (extension degrees 1–4, including the smallest applicable p³ = 125); the scaling has exactly two values, multiplicities q and q², at every one of those q | none | — |
| 14 | Dependence of the SLR output class on the bijection α | CONFIRMED (new) | Sweeping all 120 bijections at q = 5: all 120 give complex Hadamard matrices, but the 20 affine α — and exactly those — reproduce the paper's 4-profile; all 100 non-affine give a different profile and are therefore provably inequivalent. Four profile classes, sizes 40/40/20/20. For affine α the equivalence is proved for general q, requiring complex conjugation when the slope is a non-square | none; recorded so the identification is not over-generalised | — |
| 15 | lane 5: Hadamard matrix of order 23980 = 4·55·109 exists | CONFIRMED | Seberry–Yamada 1992, Cor. 8.8 part 1 (p. 505) read verbatim; Williamson matrices of order 27 attested by their class w₁ = {1,…,33,37,39,41,43} (legend p. 541, Table A.1 p. 543); T-matrices of order 55 from BS(28,27), Đoković's classification | none | — |
| 16 | lane 5: "the whole claim rests on the (q−1)/4 = 27 branch" | WRONG | Seberry–Yamada Table A.1 (p. 543) lists order 109 under method code `wk`, whose legend (p. 542) is Cor. 8.8 **part 2** — requiring only a symmetric *conference* matrix of order (q−1)/2 = 54, which exists by Paley since 53 is prime ≡ 1 (mod 4). The order is over-determined, not fragile | retract the single-branch framing; cite Table A.1 | fixed |
| 17 | lane 5: order 27 lies in an "exhaustively searched range" of Holzmann–Kharaghani–Tayfeh-Rezaie whose nonexistence orders are 35, 47, 53, 59 | OVERSTATED | Remark 1 of the paper (tex ll. 439–444) attributes order 35 to Đoković, states that HKT-R found "the **further** nonexistence orders 47, 53, and 59", and states no searched range at all | rest the argument on w ≤ 33 and on 35 > 33 instead | fixed |
| 18 | lane 5: q = 121 named as the smallest order with no witness of any kind | WRONG | For q = 121, m = 7381 = 11²·61 and 2·121 − 1 = 241 is prime, so w is already W-known; the neighbouring proposed paragraph cites T-sequences for every length ≤ 100 except 97 | delete the sentence; claim only that no entry is asserted open | fixed |
| 19 | Uncited borrowing of the lane 4 main theorem, or of the lane 5/lane 6 results | CONFIRMED ABSENT | Targeted searches plus full-text checks of nine related papers; the nearest prior work on the lane 4 axis is Đoković's prime-power extension of Scarpis, which contains no characterisation | none | — |
| 20 | Audit of the fixes themselves (coordinator-introduced defects) | OVERSTATED | Audit 006: nine repair-introduced defects, four must-fix — the most serious a wrong-source citation created by the repair round itself (an orphaned `\url` line moved the Handbook's DOI onto the Lam's-problem reference). No repair was mathematically wrong | see Audit 006 | fixed |

**Missed points raised by auditors — defects in this repository's own files,
outside the audited artifacts.** Four independent auditors surfaced these
incidentally; none was in scope, and none is fixed:

1. `Turyn1974` is cited (tex l. 404) for Turyn's 9-power family of Williamson
   matrices; that theorem is Turyn, *J. Combin. Theory Ser. A* 12 (1972)
   319–321, cited as ref [6] *by* the 1974 paper itself.
2. `KharaghaniTayfehRezaie2005` is cited (tex ll. 401–403) for the base
   sequences BS(21,20); that paper is "A Hadamard matrix of order 428" and
   concerns Turyn-type sequences of lengths 36,36,36,35. `Djokovic2010BS`
   is the correct source.
3. `Turyn1974` is cited for BS(21,20) as well; a full-text search of the 1974
   paper for "base sequence" / "T-matrices" returns nothing (scan OCR is poor,
   so this is flagged, not concluded).
4. `Djokovic2016` is cited arXiv-only (tex ll. 684–687); the published version
   is *Linear and Multilinear Algebra* 65 (2017) no. 10, 1985–1987.
5. `README.md` l. 201 says the coverage table runs "up to q = 2917"; the
   table's own caption (tex l. 496) and last row say 2969.
6. An equation inside Appendix A is manually tagged `(C.1)` (tex l. 428).
7. The `M_∞` paragraph never states that the column-pair expansion is *in
   place* — which S-pair sits over which group element. The reference
   implementation and the proposed Theorem 2 both use the in-place reading;
   any other placement permutes column blocks only.

**Disposition summary:** Of 19 resolved findings, four were WRONG (rows 1,
12, 16, 18 — one mathematical, three descriptive), and two were uncited
borrowings of classical results (rows 2, 3). All were repaired in the external
drafts; none is yet in this repository. The main proposed theorem of each
draft survived independent re-derivation. The seven repository-level defects
above are recorded as **open** and warrant a dedicated bibliography audit.
Merge is gated on Audit 006 (audit of the repairs).

---

## Audit 006 — the repairs made in response to Audit 005 — 2026-07-27

- **Artifacts (external scratchpad; post-repair state):**
  lane 4 @ sha256 `423a8a5700bc5308e3100e2f68bbfde00a85652767f3b8a88e9541dc29487d71`;
  lane 5 @ sha256 `8069741e31dc3d38b5d202713b15202b622aac7330646317775cfaecbbd49689`;
  lane 6 @ sha256 `2b31c91ac1979cf7d8ee0dcd71fcd450348dc4c917f312e68753e5e77720c686`
- **Artifact version note:** uncommitted; external to this repository. Still not merged.
- **Target paper pinned at:** unchanged, sha256
  `67c34a9f064752c6b7f2fb585b7fde8e82cd1c48c6dec07e92c86c7d7230920e`; repository
  read-only throughout.
- **Auditor:** fresh agent, model claude-opus-5, cold-context: yes.
- **Scope:** deliberately narrow — **only** text added or altered while repairing
  Audit 005's findings. The drafts were not re-audited as wholes. Rationale: the
  characteristic failure of a fix round is that the repairs introduce fresh defects,
  which then present as new findings in the next round and consume it.
- **Overall verdict:** FIT TO MERGE AFTER FIXES. Nine repair-introduced defects, four
  requiring fixes; all four have been repaired and re-verified. No repair was found to
  be mathematically wrong.

| # | Claim/target | Verdict | Evidence | Required fix | Disposition |
|---|--------------|---------|----------|--------------|-------------|
| 1 | Adding `δ(0)=0` to the definition of "of Paley type" (the Audit 005 row 1 repair) | CONFIRMED | Wang defines a *regular* PDS as one with `D⁽⁻¹⁾=D` **and `e ∉ D`**, and a Paley type PDS as a regular PDS with those parameters. Under `D={z:δ(z)=1}`, the added clause is exactly `e ∉ D` and the pre-existing `δ(−z)=δ(z)` is exactly `D⁽⁻¹⁾=D`. The pre-repair definition was missing half of Wang's regularity condition | none — the repair restores the literature's own condition | fixed |
| 2 | Whether `cor:mod4` is now circular (Wang's term presupposes `v ≡ 1 mod 4`; the corollary derives `n ≡ 1 mod 4`) | CONFIRMED not circular | Re-derived using only the four clauses of the amended definition: `σ²=Σ_d A(d)=0`, so `σ=0` and `\|D\|=(n−1)/2`; expanding `(2D̂−Ĝ+1)²` gives `μ=(n−1)/4 ∈ Z`, hence `n ≡ 1 (mod 4)`. The load-bearing input is `A(0)=n−1`, which is what `δ(0)=0` supplies. Exhaustive machine check over all sign patterns on `Z_n`, `n=3..15`: with the clause, no Paley-type `δ` at any `n ≢ 1 (mod 4)`; without it, exactly the two `n=3` patterns | none | — |
| 3 | `BrightEtAl2021` bibitem | WRONG | The entry carried `\url{https://doi.org/10.1201/9781420010541}`, which Crossref resolves to *Handbook of Combinatorial Designs* — while `ColbournDinitz2007`, whose DOI that is, was left with none. Cause: the repair's search string did not capture the Handbook entry's trailing `\url` line, orphaning it onto the last newly inserted bibitem. As printed, a reference for Lam's problem pointed at a design handbook | restore the DOI to `ColbournDinitz2007`; give `BrightEtAl2021` its own | fixed |
| 4 | `BrightEtAl2021` deliberately cited arXiv-only, published coordinates withheld as unverifiable | CONFIRMED in method, superseded in fact | The abstention was correct at the time. The coordinates are now obtained and independently confirmed via Crossref `10.1609/aaai.v35i5.16483`: *Proc. AAAI Conf. on Artificial Intelligence* **35** (2021) no. 5, 3669–3676, all five authors matching | add the published coordinates | fixed |
| 5 | "`Γ` **is** one specific output" surviving in the lane 6 self-report | WRONG | A restatement of precisely the claim Audit 005 row 10 corrected. The repair round reported correcting three sites; there were four | "is **equivalent to** one specific output" | fixed |
| 6 | "orthogonality forces `nλ_c = n`, so `λ_c = 1`" | UNVERIFIABLE as written | `λ_c` is used once and never defined, in a section where `λ` already denotes both Jungnickel's difference-matrix parameter and the PDS parameter `(n−5)/4`. The mathematics is right; none of it was on the page | replace with the explicit counting argument | fixed |
| 7 | The lane 4 self-report's claim-by-claim citation table | GAP | Four new bibliography entries and one new pinpoint had been added to the LaTeX with no corresponding row in the document's own status table, and its row C7 still read "I did not open the book, so I cannot give a chapter/theorem number" while the body now gave a page | add rows for the new entries; rewrite C7 | fixed |
| 8 | The de Launey pinpoint `p. 303` | GAP (disclosure) | The page number is quoted from van Greevenbroek–Jedwab, not read in the Handbook. Verified as *what Jedwab attributes to that page*, not as what that page says | record it as second-hand | fixed (new row C10) |
| 9 | `\cite{Turyn1970}` extended to cover the conference-matrix construction `I ± iC` | GAP | The two sources actually read corroborate Turyn 1970 for the `BH(n,4) → BH(2n,2)` doubling only, not for `I+iC`; the draft states plainly that Turyn 1970 itself was never read. The "generally credited to" hedge is doing real work | retain the hedge | accepted-as-risk |
| 10 | Every other new mathematical claim introduced by the repairs | CONFIRMED | The symmetric conference matrix of order 54 was constructed and verified (Paley over GF(53); symmetric, zero diagonal, `CCᵀ = 53·I₅₄`); the `GH(n,1)` parameter mapping checked against Jungnickel's bound; the `ρ(Z[i])`-commutativity parenthetical and the `ZR=−P` + `PR=−RP` derivation both verified exactly | none | — |
| 11 | "over-determined" phrasing implying three independent supports for order 109 | OVERSTATED | Table A.1's method code `wk` **is** Corollary 8.8(2), citing the same source; the tabulated row is an instance of that branch, not a third route. Two routes, not three | reword to name the two branches explicitly | fixed |

**Missed points raised by auditor:** the lane 5 repair left "§A.3" denoting two
different subsections under its own stated pre-insertion numbering convention
(fixed); and the new lane 5 subsection forward-references four objects defined in
the following subsection, which is pre-existing house style in this appendix rather
than a new defect.

**Disposition summary:** Of nine repair-introduced defects, the most serious was a
**wrong-source citation created by the round convened to remove wrong-source
citations** (row 3) — an orphaned `\url` line, invisible to every check that had been
run because both the source and target bibitems were otherwise well-formed and the
document compiled cleanly. This is recorded prominently because it is the strongest
available argument for auditing repairs rather than trusting them. All four must-fix
items are repaired and re-verified; all three drafts still compile with zero undefined
references, zero undefined citations and zero errors. Merge remains ungated by any
open finding in Audits 005–006, but nothing has been merged.

---

## Merge Record 001 — Audits 005–006 additions merged into the paper — 2026-07-27

The three draft additions cleared by Audits 005–006 are now **merged**. This
entry supersedes the closing sentence of Audit 006 ("nothing has been merged").
The merge was performed by a fresh subagent against a scratchpad copy and
validated independently by the coordinator before anything was written here;
the coordinator's checks did not import, read, or re-run the merge agent's own
scripts.

**Result.** `paley_scarpis_p1mod4_v2.tex` 712 → 1373 lines, 10 → 17 pages,
compiling with zero errors, zero LaTeX warnings, zero undefined references,
zero undefined citations and zero multiply-defined labels.

* New **§5 "What the construction needs"** — the characterisation, the mod-4
  corollary, and the projective-plane barrier.
* New **§6 "The construction over the Gaussian integers"** — the factorisation
  through `Z[i]` and the relation to Sargent–Lee–Rushall.
* New **§A.3** — the `q = 109` worked example, plus four edits repairing the
  appendix roadmap and the two sentences it falsifies.
* 18 new `\bibitem` entries (bibliography 14 → 32).

| # | Claim/target | Verdict | Evidence | Required fix | Disposition |
|---|---|---|---|---|---|
| 1 | The two new sections and lane 5's five edits landed at their specified anchors | CONFIRMED | Ordering in the merged file: §5 L339 < §6 L624 < `\appendix` L798 < new §A.3 L871 < existing §A.4 L946 < `\end{thebibliography}` L1371 | none | — |
| 2 | The merged document says what the audited drafts say | CONFIRMED | A line-level diff against the 712-line original decomposes into exactly 3 insert hunks + 4 replace hunks + **0 deletions**, every hunk attributable to a named draft edit; all draft LaTeX blocks byte-identical | none | — |
| 3 | Manual equation tags | WRONG before merge | §5 and §6 were drafted independently and **each** used `\tag{5.1},{5.2},{5.3}`, each having assumed it would be the sole new §5. `\tag` is literal text: LaTeX emits no warning and the document compiles cleanly while two equations both print "(5.1)". Detectable only on merge | renumber §6's tags to 6.1–6.3 | fixed |
| 4 | Bibliography integrity across an 18-entry splice | CONFIRMED | Per-key URL/DOI association recomputed from source and compared for all 32 entries; zero gained, lost, or swapped. The specific orphaned-`\url` defect of Audit 006 row 3 did **not** recur: `ColbournDinitz2007` retains its Handbook DOI and `BrightEtAl2021` its own AAAI DOI | none | — |
| 5 | Label, key and tag uniqueness | CONFIRMED | 36 labels, 32 bibitem keys, 9 manual tags — all distinct within their kind; 29 cite keys all resolve | none | — |
| 6 | Printed numbering of every numbered environment | CONFIRMED | Extracted from the compiled PDF and matched against a prediction registered **before** the merge agent reported: Lemmas 1–4 / Theorem 1 / Corollary 1 (pre-existing); Lemma 5, Theorem 2, Corollaries 2–3, Remarks 1–3 (§5); Lemma 6, Theorem 3, Remarks 4–6 (§6); Remark 7 (appendix). Exact match | none | — |
| 7 | §6's two literal `Corollary~1` references | CONFIRMED (not a defect) | Both read "**their** Corollary~1" — Sargent–Lee–Rushall's, an external result, unaffected by this document's numbering. The paper's own unlabeled corollary still prints as Corollary 1 | none | — |
| 8 | A rejected alternative in the lane 5 draft | CONFIRMED excluded | That draft contains nine fenced LaTeX blocks, one of which it explicitly rejects ("NOT RECOMMENDED"). Verified absent from the merged file, along with its marker string. A glob-all-blocks merge would have spliced in content contradicting the edit two paragraphs above it | none | — |
| 9 | `EganOCathain2019` present in the bibliography but never cited | CONFIRMED | Owner elected to leave it uncited. Consistent with existing practice: `Hadamard1893` and `Williamson1944` are likewise uncited and were so **before** this merge | none | accepted-as-risk |
| 10 | `\tag{C.1}` prints "(C.1)" inside Appendix A | CONFIRMED | The paper has exactly one appendix section, so the manual tag's letter does not match its appendix. **Pre-existing; not merge-induced** | renumber to A.1, or drop the manual tag | open |
| 11 | `README.md` against the merged paper | GAP | No statement in it is false — "the four block-Gram lemmas" and "Theorem 1 through the four lemmas" both still hold. But it predates §5 and §6 and does not mention them, and Scorecard 001's qualitative notes were written against a paper lacking both | re-read the README against the merged paper; consider a `repo-rank` re-run | open |

**Disposition summary:** the merge is complete and every check passes. The one
defect it introduced — the duplicate `\tag` — belonged to a class that no
single-lane audit could have caught, since each draft was individually correct
and only their *combination* was wrong; it was found by pre-merge collision
analysis rather than by compilation, which stayed silent throughout. Two items
remain **open**, both concerning artifacts outside the paper body (the
pre-existing appendix tag letter, and README/scorecard staleness), and neither
gates the merge.

---

## Merge Record 002 — abstract brought current with the merged body — 2026-07-27

Follow-up to Merge Record 001. The abstract had never been audited — the
standard five-axis split includes an abstract auditor and no such pass was run
on this paper — and the merge left it describing a four-section paper.

| # | Claim/target | Verdict | Evidence | Required fix | Disposition |
|---|---|---|---|---|---|
| 1 | The abstract as it stood after the merge | GAP, not WRONG | Every sentence remained true, including the coverage claims, which §A.3 strengthened rather than contradicted. But the paper carries 3 theorems and 3 corollaries and the abstract described **Theorem 1 only** — omitting Theorem 2 (the characterisation), Corollaries 2–3 (the mod-4 and projective-plane consequences) and Theorem 3 (the factorisation over `Z[i]`), i.e. two of three theorems and roughly a third of the body | add two paragraphs covering §5 and §6 | fixed |
| 2 | Attribution stance under an abstract-only reading | OVERSTATED by omission | The abstract credited the *q* ≡ 1 case to Farouk–Wang alone. Their 2020 priority is intact, so nothing was false, but §6 now records a **second route in the literature** (the complex Scarpis lift of Sargent–Lee–Rushall composed with Turyn doubling), and an abstract-only reader would not have known of it | name the second route in the abstract | fixed |
| 3 | Disclosure that `Γ` is equivalent to an SLR output | CONFIRMED present | The abstract states it explicitly rather than leaving it to §6. Phrased "**is equivalent to** one of their outputs", not "is one of" — the distinction Audit 005 row 10 and Audit 006 row 5 were convened over. Guarded by an automated regression check | none | — |
| 4 | Every factual assertion added to the abstract | CONFIRMED | 12 load-bearing claims each matched mechanically against the supporting statement in the body: the `if and only if` characterisation and its two conditions, the `δ(0)=0` hypothesis, the regular-PDS/Paley-parameter consequence, `n ≡ 1 (mod 4)`, the `n−1` MOLS and non-prime-power-plane consequence, `Γ ∈ BH(q(q+1),4)`, the Turyn double, the SLR attribution, and the second worked example. Zero mismatches | none | — |
| 5 | `δ(0)=0` carried into the abstract | CONFIRMED | Stated explicitly in the abstract's hypothesis. Its omission was the single false mathematical statement of the entire campaign (Audit 005, lane 4 `cor:mod4`); restating the definition in a new summary surface without it would have reintroduced that defect in the paper's most-read paragraph | none | — |
| 6 | Abstract length | INFORMATIONAL | 534 words, up from ~290. Long for the genre, and a deliberate trade against completeness across three theorems. Four paragraphs where the original was one — a style change, flagged for owner review | owner to trim if desired | open |
| 7 | The §1 contribution paragraph | GAP | It enumerates the contributions as the method plus "a secondary contribution\ldots the coverage analysis of Appendix A", and does not mention §5 or §6 — the same omission just repaired in the abstract. **Deliberately not fixed**: the owner scoped this change to the abstract | bring §1's enumeration into line | open |

**Disposition summary:** the abstract now covers all three theorems and
discloses the second literature route. Two items remain **open**: the §1
contribution paragraph carries the identical gap and was left alone as
out of scope, and the abstract's length is an owner call. No claim in
the paper body changed; this entry concerns summary surfaces only.

---

## Scorecard 002 — repo-rank pass — 2026-07-27

- **Artifact:** full repository @ commit `0afd56a`, branch
  `merge/audits-005-006-additions` — the paper **as merged**, carrying §5
  (characterisation), §6 (factorisation over `Z[i]`), §A.3 and the revised
  abstract.
- **Not directly comparable to Scorecard 001**, which graded `19a6958`: a
  four-section paper without any of the above. Movement on an axis between
  the two passes is expected, not noise.
- **Method:** `repo-rank` skill — four fresh cold agents, one per axis, no
  cross-visibility, each given only its own axis rubric and instructed **not
  to read this file or `README.md`** until it had independently formed a
  view. Numeric scores are deliberately absent here and everywhere in this
  repository; the private numeric record lives with the skill.
- **What distinguishes this pass from Scorecard 001:** three of the four
  agents' self-reported counter-arguments were acted on rather than noted
  and set aside — one refuted by the coordinator retrieving a primary source
  the agent could not reach, one resolved in the paper's favour, one
  accepted and the axis revised down. Two must-fix defects were found and
  independently re-verified by the coordinator before any edit was made.

### Confirmed defects and their disposition

| # | Claim/target | Verdict | Evidence | Required fix | Disposition |
|---|---|---|---|---|---|
| 1 | Appendix A.1: "the only odd `m ≤ 3000` with `t > 2` are the primes 167, 179, 223, 283" | **WRONG** | Found independently by two cold agents (Reach, from Cati–Pasechnik 2024; Depth, from a 2014 source and marked "probable"). Coordinator settled it by reparsing Table 4 of arXiv:2411.18897 from the PDF: **195** odd `m ≤ 2999` are listed with `t > 2`, so there are **191 counterexamples**, the smallest being **311**. Traced to the source of the error: Cati–Pasechnik's prose naming exactly those four is scoped to *orders* `≤ 1208` (odd part `≤ 302`); the paper re-scoped it to odd part `≤ 3000` | replace with the direct value-by-value check | fixed |
| 2 | The inference "Since `m = q(q+1)/2` is composite it is never one of these" | **WRONG** (non sequitur) | **71 of the 195** open odd parts are composite, smallest **515**. Compositeness affords no protection whatever. Note Depth's proposed repair — "the conclusion survives if every open `m ≤ 3000` is prime" — is *also* wrong for the same reason | state the twelve values and check them individually | fixed |
| 3 | The conclusion "every `N` with `m ≤ 3000` is a known Hadamard order" | **CONFIRMED** | Right conclusion reached by an invalid route. Coordinator checked all twelve in-range odd parts `m = q(q+1)/2` (15, 45, 91, 153, 325, 435, 703, 861, 1225, 1431, 1891, 2701) directly against Table 4 — **none appears**. `q = 73` (`m = 2701`) had been covered *only* by the false blanket claim | none — but the justification had to be rebuilt | fixed |
| 4 | Same broken premise at §4 ("the family never meets the dominant list of open Hadamard orders, which are 4×prime") | **WRONG** | Identical non sequitur, in the paper body rather than the appendix | replace with the honest statement + pointer to §A.1 | fixed |
| 5 | Same broken premise, twice in `README.md` | **WRONG** | The front door restated it in the Coverage section and in Scorecard 001's Reach note — exactly the "README is a second copy of every claim" failure mode | rewrite both | fixed |
| 6 | Uncited prior work subsuming §5's **sufficiency** half | **GAP (attribution)** | Nuñez Ponasso, arXiv:2404.09040v2, Thm. 4.3.3, verbatim: *"Let H be a BH(n + 1, m), and suppose that there is a GH(n, G) where \|G\| = n. Then there is a BH(n(n + 1), m) matrix."* A `GH(n,G)` with `\|G\| = n` **is** a `(G,n;1)`-difference matrix; at `m = 4`, composed with the doubling §6 already cites, this gives the "if" half for any group and any `m`. Not a survey restatement — Ponasso states "We state here our own version of this result, which is more general than the ones previously found in the literature." Seberry (1980) gave a GH form of the same construction | cite both; state plainly which half is new | fixed |
| 7 | `AUDIT_LEDGER.md` Audit 005 row 19 ("uncited borrowing CONFIRMED ABSENT") | **FALSIFIED** for the sufficiency half | Superseded by row 6 above. The finding was correct about the *necessity* direction only | superseded, recorded here | fixed |
| 8 | §5's **necessity** direction (that both conditions are forced) | **CONFIRMED NEW** | Neither Ponasso nor Seberry states it; the Reach agent searched for it specifically and could not locate it; the Depth agent re-derived it independently by a different route than the author's and calls it the sharpest argument in the paper | foreground it as the contribution | fixed |
| 9 | §3's `M∞` column alignment | **GAP (specification)** — repeat finding | Scorecard 001 named this and it was still unfixed a pass later. The Depth agent *proved* it load-bearing: it built a matrix satisfying every word of §3 under the interleaved reading and it is **not Hadamard** (`M∞M₀ᵀ ≠ 0`, max 48/336/576 at `q = 5/13/17`, failing only at `r = 0`). Also contradicts Audit 005 missed-point 7's reassurance that "any other placement permutes column blocks only" — true for reassigning S-pairs to blocks, false for the block-vs-within-block ambiguity | state the alignment explicitly in §3 | fixed |
| 10 | `rem:q9` paper numbers vs this ledger's Audit 005 row 5 numbers | **NOT an inconsistency** | Raised unresolved by the Evidence agent, which flagged that if both described the same computation there was a live numerical contradiction behind a claim stated as fact. They do not: the paper's **112,752** is the 44-count of the *nearfield* matrix; the ledger's 12960/17496/11664/11664/18144/18144 are the 44-counts of *six band-relabelled Desarguesian* matrices, supporting the separate claim in the paper's closing sentence. They agree on the only shared quantity — the Theorem 1 matrix's count of **0** | none | — |
| 11 | Reproducibility coverage of numeric claims | **GAP** | Every shipped script reproduced exactly (default sweep `ALL PASS` exit 0; `--q 81/125 --sampled` pass; regenerated figures byte-identical to the committed PNGs; `profile_results.txt` exact including its positive control; working tree clean after every run). But three confidently-stated numeric claims have **no committed script**: the 104-row coverage table, `rem:q9` and `rem:c30`. The agent independently reimplemented the coverage table and matched all 104 rows and the 232/128/104 counts | commit the three scripts | **open** |
| 12 | Provenance of that gap | **INTRODUCED BY THIS CAMPAIGN** | Verified with `git show main:` — `rem:q9` and `rem:c30` are **absent pre-merge**. The merge took the count of unscripted numeric claims from **1 to 3** without adding a script. The 104-row table is the pre-existing item Scorecard 001 already flagged | see row 11 | **open** |
| 13 | Theorems 2 and 3 as merged | **CONFIRMED** | Scorecard 001 predates them and Audit 006 was scoped only to repair-text, so they appear never to have been audited end-to-end before this pass. The Depth agent closed 41 of 43 checkable proof steps, re-deriving Lemmas 1–4 and Theorem 1 by hand *before* reading the proofs. All theorems and corollaries are **PROVED** — nothing conditional, nothing carried by numerics; the sole external import is MOLS ⟺ projective plane, correctly cited | none | — |

### Qualitative axis notes

- **Novelty.** The contrast with Farouk–Wang is real and was verified against
  their 2020 primary text, which the grading agent could not reach
  (DOISerbia was returning 503 at its root) and the coordinator recovered
  from the publisher's host: FW2020's Thm. 2.2 is a map of sets `Ψ_{q,α}`
  depending on an input matrix, a bijection `α` and two permutations whose
  existence is asserted but not exhibited, and its §3 "Other Form" pins `α`
  down but still requires an input Hadamard matrix. So *closed form relative
  to a choice* versus *choice-free closed form* — not "already present".
  Bounded on three sides all the same: FW2022 Cor. 4.2 has the same affine
  shift array, §6's `Γ` is conceded equivalent to an SLR output, and §5's
  sufficiency half is now known to be prior art (row 6).
- **Depth.** The strongest axis. Everything proved outright. Held one band
  below the top *only* because of row 9 — a construction paper's first duty
  is to specify its object unambiguously, and until this pass §3 admitted a
  reading that is not Hadamard. With that fixed the reservation is gone.
- **Reach.** Settles the question posed and gives a genuine quantitative
  delimitation — the smallest conceivable non-prime-power instance is
  `n = 5625`, order 63,292,500, gated on a projective plane of order `3²·5⁴`.
  Partially answers Farouk–Wang 2022's **published** open problem 2
  (confirmed verbatim from their PDF) for group-developed squares, which is
  what distinguishes it from answering a purely self-posed question. Adds no
  new Hadamard order. There is no open-problems section, and the one real
  program implied — every quasifield/translation plane of order `q` feeds the
  `T`-slot — is exercised once at `q = 9` and never stated as a program.
- **Evidence.** Weakest axis, and the fall from Scorecard 001 is this
  campaign's own doing (rows 11–12). Nothing checked was found *wrong*; the
  defect is that a third of the paper's confident numeric claims cannot be
  re-run from the repository.

**Disposition summary:** nine defects fixed in this pass — one false
statement and one non sequitur in the appendix, the same premise in the
body and twice in the README, a two-source attribution gap, a superseded
prior finding, and the repeat `M∞` specification gap. **Two remain open**,
both the same item: the coverage table, `rem:q9` and `rem:c30` still have no
committed script, and two of those three were introduced by the merge
recorded above. Closing them is the single highest-value action available
on this repository.

### Scorecard 002 addendum — Evidence and Depth repaired — 2026-07-27

Rows 11–12 above are **closed**, and the two remaining Depth items with them.
Three scripts were added, each re-deriving its published numbers and exiting
nonzero on any disagreement.

| # | Item | Was | Now | Evidence |
|---|---|---|---|---|
| 14 | Appendix A screen | asserted as computed, no script | `coverage_table.py` | Reproduces 232 orders / 128 covered / 104 without a witness, and the smallest failure `q = 109`, `N = 23980`, `m = 5·11·109`. `--table` prints all 104 rows. Implements (C.1) from actual divisor splits; the withdrawn factorwise test of Remark 7 is deliberately not implemented |
| 15 | The A.1 statistics added when defect 1 was fixed | newly written, unscripted | same script | Also checks the numbers that replaced the false claim: Table 4 has **195** entries, **124** prime and **71** composite, smallest **167**, smallest composite **515**, and all twelve odd parts `m = q(q+1)/2` for `q ≤ 73` absent from it. Table 4 is transcribed into the script with its provenance, so the check is self-contained |
| 16 | `rem:q9` (q = 9 nearfield) | asserted as computed, no script | `nearfield_q9.py` | Builds both order-180 matrices by subclassing the shipped `PaleyScarpis` and overriding only the T-slot, verifies both are Hadamard, verifies `T(r,a) = r∘a` really is a `(Z₃², 9; 1)`-difference matrix, and reproduces **44 on 112,752** of all 42,296,805 quadruples for the nearfield matrix against **0** for Theorem 1, with all four row/column comparisons distinct. Runtime ≈ 8 s |
| 17 | Trusting a fast path at scale | — | built into the same script | The vectorized profile routine is validated against a direct `O(n⁴)` reference at order 60 **before** being used at order 180, and the resulting `q = 5` profile is checked against the recorded `NOTE_rows` value `4:359000 12:103125 20:25510`. This is the "cross-check the fast implementation against a dense reference at small size" discipline, made permanent |
| 18 | `rem:c30` (Γ vs Turyn's `C₃₀ + iI`) | asserted as computed, no script | `gaussian_c30.py` | Confirms Γ ∈ BH(30,4) and `C₃₀ + iI` ∈ BH(30,4), and reproduces **500 on 240** ordered quadruples for Γ against **0** for `C₃₀ + iI`, in both orientations |
| 19 | Theorem 3's `H = φ(Γ)` | proved, never checked numerically | same script | `φ(Γ)` is verified **entrywise equal** to the order-60 matrix built by the shipped construction — a claim of Theorem 3 that no script previously touched |
| 20 | The character sum `Σ_z χ(z(z−d)) = −1` | used four times, never stated or cited | fixed in §2 | Flagged by the Depth agent as a silent classical import, against an abstract advertising the proof as computed "directly from character sums". Now stated as (2.2) beside (2.1) with a three-line proof (the `z = 0` term vanishes; for `z ≠ 0`, `z(z−d) = z²(1−dz⁻¹)` and `χ(z²) = 1`, so the sum is `Σ_{u≠1} χ(u) = −1`), and referenced rather than restated at its first use. Verified numerically for `q = 5, 9, 13, 17, 25, 29, 49, 81, 121, 125` |
| 21 | "because `S` is Hadamard" in Lemma 4 | silent import | fixed in §3 | Now carries the Paley citation already in the bibliography |

**Disposition summary:** every item this scorecard opened is now closed. The
paper's numeric claims are reproducible end to end from the repository:
`ps_p1mod4.py` for the construction itself, `q5_equivalence/` for the
Farouk–Wang comparison, and the three scripts above for Appendix A, Remark 11,
Remark 13 and Theorem 3. The reproducibility regression introduced by the §5/§6
merge is undone, and the paper no longer imports a character-sum identity
without proof.

### Repository layout change and §7 — 2026-07-27

**Layout.** The repository was restructured to match the layout of the
author's `geometric-difference-families` repo:

| Was | Now |
|---|---|
| `paley_scarpis_p1mod4_v2.tex` / `.pdf` | `paper/main.tex` / `paper/main.pdf` |
| `images/` | `paper/images/` |
| `ps_p1mod4.py`, `coverage_table.py`, `nearfield_q9.py`, `gaussian_c30.py` | `code/` |
| `q5_equivalence/` | `code/q5_equivalence/` |
| — | `code/README.md` (new, per-script table) |

`README.md`, `AUDIT_LEDGER.md`, `LICENSE` and `.gitignore` stay at the root.
All moves used `git mv`, so history follows the files. `images/` went under
`paper/` rather than the root so that the single `\includegraphics` path in
the source resolves unchanged when compiling inside `paper/`; the figures were
regenerated to the new location and are byte-identical. Earlier entries in
this ledger name files by their pre-move paths; those entries were accurate
when written and are left as they stand.

**One deliberate difference from the target layout:** there is no `audit/`
directory. The target repo uses it for per-round audit reports, but this
repo's audit record is this single file, and the only separate artifacts that
exist — the four per-axis grading reports and three coordinator verification
notes from Scorecard 002 — carry numeric scores, which are kept out of this
repository by policy. Adding `audit/` would mean either an empty directory or
publishing scored material.

**§7 Open problems.** Added, at the owner's direction, closing the gap
Scorecard 002 recorded on the Reach axis (no open-problems section; the
`T`-slot program exercised once at `q = 9` and never stated as a program).
Five items, each tied to an existing result rather than freestanding:

1. the `T`-slot as a program — how many Hadamard-equivalence classes arise as
   `T` ranges over the `(G,n;1)`-difference matrices, unanswered even at
   `n = 9`, where the field and Dickson-nearfield products already differ;
2. whether a Paley-type `δ` is unique up to `Aut(G)` (rigid at `n = 9`);
3. where the obstruction sits beyond the prime powers — at `n = 5625` the
   `δ`-slot is available by Polhill's construction while no
   `(G,5625;1)`-difference matrix is known, so for this construction the
   entire non-prime-power obstruction lies in the `T`-slot;
4. whether `q ≡ 3 (mod 4)` admits a choice-free closed form, the residue class
   entering in exactly one place (the proof of Lemma 1);
5. equivalence to the rest of the Farouk–Wang family, and to the
   Sargent–Lee–Rushall lift beyond the equivalence already recorded.

Item 3 is the one new observation rather than a restatement: the paper already
had both halves (Wang's classification, Polhill's construction, and the
absence of a difference matrix) but had not drawn the asymmetry between the
two slots.

---

## Scorecard 003 — repo-rank pass — 2026-07-27

- **Artifact:** full repository @ commit `5cb92e7`, branch
  `merge/audits-005-006-additions` — Scorecard 002's object plus three commits
  of repairs (`4d23bc9` false coverage claim and attribution, `0cd28b4`
  reproducibility scripts and the character sum, `5cb92e7` restructure and §7).
- **Directly comparable to Scorecard 002**, unlike 002 vs 001: same skill, same
  rubrics, same object with known deltas.
- **Method:** four fresh cold graders, no cross-visibility, each given only its
  own axis rubric and instructed not to read `README.md` or this file until its
  own view was on disk; all four confirmed compliance and named the point at
  which they read. Improvement over the previous pass: the primary-source PDFs
  were pre-supplied, removing the retrieval failure that left the last pass with
  an unresolved three-point swing. Numeric scores are absent here and everywhere
  in this repository by policy.

### Confirmed movement, and what caused it

| # | Axis | Finding | Evidence |
|---|---|---|---|
| 1 | Depth | **The `M_∞` repair is confirmed effective by the strongest available test.** A grader reimplemented the construction *from the paper's text alone*, explicitly not from `code/ps_p1mod4.py`, and obtained exact Hadamard matrices at q = 5, 9, 13, 17, 25 — i.e. the prose now determines the object, which is precisely what the repair was for. It independently confirmed the interleaved reading fails, reporting off-diagonal Gram 48 at q = 5, matching the coordinator's own earlier computation exactly. Both directions of Theorem 2 closed; 25 of 33 checkable steps closed | axis moved up one band-step |
| 2 | Evidence | **The reproducibility repair is confirmed.** Every script ran, reproduced its published numbers, and left `git status --porcelain` empty. The grader verified that `nearfield_q9.py` *genuinely* validates its fast profile against a direct O(n⁴) reference rather than merely claiming to, and cross-checked all 104 rows of `coverage_table.py --table` against the printed `tab:candidates` longtable — exact match | axis moved up two |
| 3 | Reach | **The Appendix A repair is independently confirmed by a third party.** The grader re-extracted Cati–Pasechnik Table 4 by its own script and reproduced 195 entries, 124 prime, 71 composite, smallest composite 515, and all 104 screen failures with the first at q = 109 | unchanged, but the fix is now externally corroborated |
| 4 | Reach | **§7 bought a fraction of a band, not a band.** The grader judged the five problems real and genuinely following, but noted that a section written to answer a reach criticism is worth less than it looks, and that its most consequential item is a restatement of the prime power conjecture | recorded honestly; the axis did not move |

### New findings, all open

| # | Item | Verdict | Evidence | Disposition |
|---|---|---|---|---|
| 5 | The row-quadruple statistic's **invariance** under Hadamard equivalence | **GAP** | It is the sole engine of all three inequivalence claims (§4 q=5; `rem:q9`; `rem:c30`) and is asserted, never stated as a lemma or proved. The three scripts added in `0cd28b4` make the *counts* reproducible but supply no invariance argument — that was an Evidence fix, and this is a Depth gap. The grader's own counter-argument (that this makes the distinctness claims rest on nothing) was rejected on the ground that no theorem depends on them: delete all three remarks and every theorem stands | **open** — a two-line lemma would close it |
| 6 | Nuñez Ponasso also reaches the **existence** statement | **GAP (attribution)** | Composing his Thm 4.3.3 with Thm 4.4.1 (Turyn, `BH(n,4) → BH(2n,2)`) yields a real Hadamard matrix of order 2q(q+1). **Coordinator-verified by construction**: instantiated with the Turyn `C+iI` seed and the field multiplication table, it gives a valid `BH(30,4)` at q = 5 and `BH(182,4)` at q = 13. The paper cites Ponasso only for §5's sufficiency. Mechanically this is the same move already credited to Sargent–Lee–Rushall, stated more generally — it widens the attribution rather than introducing a new mechanism | **open** — one sentence |
| 7 | The claim that Ponasso's output **is** Γ up to unimodular scaling | **REFUTED by the coordinator** | Under the paper's own invariant, over the same 657,720 ordered quadruples, the value 500 is attained on **240** quadruples for Γ and on **80** for the Ponasso matrix; the full profiles differ throughout. Differing profiles under an invariant of the stated equivalence means the two are *inequivalent*. Scope: this refutes the claim for the natural instantiation; a different seed or GH matrix might land elsewhere | closed — no change to the paper |
| 8 | The claim that this makes Ponasso "strictly stronger for every odd prime power" | **DISCOUNTED** | True but nearly vacuous on the half that strengthens: for q ≡ 3 (mod 4), q+1 is divisible by 4, so Đoković's order q(q+1) plus a Kronecker product with `H_2` already gives 2q(q+1). Checked q = 7, 11, 19, 23, 27. The substantive content is exactly the q ≡ 1 (mod 4) case | closed |
| 9 | `rem:q9`'s sub-claim "6 of the 16 sign patterns are of Paley type, all `Aut(Z₃²)`-equivalent" | **GAP (reproducibility)** | No script anywhere covers it. `nearfield_q9.py` scripts the difference-matrix property and the 44-count but not this. Introduced by the coordinator in `0cd28b4` while believing `rem:q9` fully covered; the grader verified the claim is numerically correct, which does not close the repository's gap | **open** |
| 10 | `CP_TABLE4` in `coverage_table.py` | **GAP (minor)** | The transcription of the external table has no internal consistency check, unlike the Farouk–Wang matrix transcription which self-validates via `HHᵀ = 60I` | **open** |
| 11 | The true cap on this work's reach | **GAP (framing)** | Because existence at order 2q(q+1) is Farouk–Wang's, this note *could never* contribute a new Hadamard order, whatever the coverage analysis shows. The cap is prior art, not arithmetic. Scorecard 001's version of this claim reasoned from "always 4×composite" and was invalid (fixed in `4d23bc9`); the true cap survives and is stated plainly in neither the paper nor the README | **open** |

### The dominant risk

Two graders working independently, on different axes, nominated the **same**
single item as the one that would collapse their score, and neither could check
it: whether §5's **necessity** direction already exists in the de Launey /
Flannery generalized-Hadamard ("orthogonality set") literature. Novelty would
fall to the bottom band; Reach to roughly 3. Both negative results are
therefore "not located under a constrained search", not "not in the
literature" — this session's web-search budget was exhausted before the Novelty
grader's first query, so all external work was fetch-only, with no MathSciNet,
zbMATH or Scholar traversal.

**This is the highest-value open question about the repository, and it is a
literature search rather than a computation.** §5's converse is, by every
grader's account, the one thing in the paper that is not already in print.

### Cheapest available gains, in order

1. **Reach:** settle §7 problem 5 at q = 5. There are only **120** bijections α,
   and the invariant is already implemented in `code/q5_equivalence/`.
2. **Depth:** state the row-quadruple invariance as a lemma (row 5) — two lines.
3. **Evidence:** script the 6-of-16 count and add a consistency check to
   `CP_TABLE4` (rows 9–10).
4. **Novelty/attribution:** one sentence recording the Ponasso existence route
   (row 6).

**Disposition summary:** the three repairs made since Scorecard 002 are all
independently confirmed effective, two axes moved up, and no previously-fixed
defect regressed. Seven items are open, none of them a false statement: five
are gaps of proof-status, reproducibility or framing, one is an attribution
sentence, and one — the de Launey/Flannery search — is the single question on
which two axis scores depend.

### Scorecard 003 addendum — the four open items worked — 2026-07-27

Three lanes ran read-only against the repository; the coordinator applied every
edit, after independently verifying each result. Items are numbered as in
Scorecard 003 above.

| # | Item | Outcome | Evidence |
|---|---|---|---|
| 5 | Row-quadruple invariance never stated | **CLOSED** | Now Lemma 5 in §4, stated for entries of modulus 1 so that it covers all three uses — §4 and `rem:q9` (real, `±1`) and `rem:c30` (Butson, fourth roots and conjugation). The drafted version covered only the real case, which would have left `rem:c30` uncovered while appearing closed; it was widened before being applied. Verified numerically on both the order-60 matrix and Γ, under permutations, sign and fourth-root scalings, and conjugation — with a negative control confirming a generic single-entry phase *does* change the profile, so the lemma is not vacuous |
| 6 | Ponasso also reaches the existence statement | **CLOSED** | One sentence added to `rem:slr`. The draft's stronger clause "not equivalent to Γ" was **rejected**: the coordinator's check established only that the natural instantiation is inequivalent, and a different seed or GH matrix could land elsewhere, so stating it flatly would have been an overclaim |
| 9 | `rem:q9`'s 6-of-16 sub-claim unscripted | **CLOSED** | `code/paley_patterns_q9.py`. Confirms both halves: exactly 6 of the 16 patterns are of Paley type, and all 6 form a **single orbit** of size 6 under `Aut(Z₃²) = GL(2,3)` (order 48, stabiliser order 8), with χ among them. It verifies that `GF(9)`'s additive group really is `Z₃²` rather than assuming it |
| 10 | `CP_TABLE4` had no integrity check | **CLOSED** | Added to `coverage_table.py`. The transcription was independently re-extracted from the source PDF and found identical entry for entry, so the digest pins a cross-checked state rather than freezing whatever was there. Negative control: a compensating edit (523→525, 571→569) passes count, parity, order, endpoints **and** sum, and is caught only by the digest |
| 11 | The reach cap is prior art, not arithmetic | recorded in the README scorecard note | not a paper change |

### The α-family result (item 1) — recorded as an unrefereed report

The remaining item was to settle §7 problem 5 at `q = 5`. **It came out against
the paper.** At `q = 5` the matrix of Theorem 1 *is* Hadamard-equivalent to an
output of the Farouk–Wang procedure — to `Ψ_{5,α}(P′₅)` for α any of the twenty
affine bijections `k ↦ ak+b` of `F₅` — by an explicit signed row and column
permutation, not by an invariant coincidence.

**Coordinator verification.** The H under test was confirmed byte-identical to
what `PaleyScarpis(5)` builds; the Ψ target was rebuilt from parameters derived
from the Paley-II seed rather than from saved state; the exact integer identity
was then checked. The first attempt **failed** (max difference 2) — that was a
permutation-convention error on the coordinator's part, and with row gather by
`src` and column gather by `inv(perm)` the identity holds exactly.

**What is not verified, and it is the crux.** That the implementation of
`Ψ_{q,α}` is faithful to Farouk–Wang's Steps 4–7. Building it at all required
correcting the permutation displayed in the proof of their Lemma 2.2(2), which
at `q = 5` does not satisfy their own condition (`T·ε = (0,0,0,0,0,4,4,4,4,4)`),
and their Step 6's block shape. Their Theorem 2.2 and Corollary 2.1 are
unaffected. The evidence for faithfulness is strong but interpretive: the
implementation reproduces the printed 4-profile `4:353800 12:111525 20:21910
28:400` exactly, and their printed matrix was reverse-engineered and shown to
carry the §2 block structure.

It is therefore recorded in Remark 5 as an **unrefereed computational report,
explicitly not a claim of the note**, with its scope limits stated: `q = 5`
alone; the matrix is equivalent to *some* outputs and provably inequivalent to
*others*; 66 further seed shapes unexplored; order-12 Hadamard uniqueness
quoted, not verified. `code/alpha_family.py` ships so a referee can re-run it.

**Effect on the axes.** Depth and Evidence improved and Novelty fell. Reach did
not move: answering §7 problem 5 was priced as a gain, but the answer removes a
distinctness claim the work previously leaned on, and the two cancel. The
paper's §4 inequivalence survives — it is to the printed representative — but
its significance is reduced, and the README front door was corrected to match.

**Process note against the coordinator.** The α lane was told the repository was
read-only while the coordinator was concurrently applying items 2, 3 and 4 to
it; the agent correctly flagged the changing mtimes. No contamination resulted —
its work depends on `ps_p1mod4.py` and the Farouk–Wang PDF, neither of which was
touched — but the lanes should have been sequenced or the tree frozen.

### Correction to the Scorecard 003 addendum — Novelty — 2026-07-27

The addendum above recorded that the Novelty axis fell on account of
Remark~5's `q = 5` equivalence. **That was wrong**, and is retracted. The
owner challenged it and an independent cold re-grade at commit `6e737f5`
placed the axis exactly where Scorecard 003 had it — unchanged, not lowered.

Two errors, recorded so a later pass does not repeat them:

1. **Category error.** An *object*-level fact (the `q = 5` matrix lies inside
   the Farouk–Wang family) was allowed to deflate a *method*-level claim (a
   choice-free closed form replacing a choice-dependent procedure). A canonical
   selector landing inside the known family is the success condition for such a
   claim, not a failure of it.
2. **Logic error.** Scorecard 001's `q = 5` argument was a steelman for moving
   the axis *up*. Killing an argument for raising a score is not an argument for
   lowering it; the base rests on prior-art analysis, which Remark 5 does not
   touch.

The re-grade's own mechanism is sharper than either: §6 already **proves, for
every `q` and by argument**, that Γ is equivalent to a Sargent–Lee–Rushall
output. A universal proved subsumption dominates a single-`q`, unrefereed,
machine-produced coincidence, so there was no object-novelty credit left for
Remark 5 to remove. Its verdict is *neutral* — not supporting either, since
canonical selection is precisely what Sargent–Lee–Rushall's Theorem 1 does once
seed, deleted row and α are fixed, and a property shared with the closest prior
work is not evidence of novelty.

A wrong dependency had been written into the README front door as a result:
under the retracted reading, later *refuting* Remark 5 would not have restored
the axis. The README note has been rewritten to state the §6 subsumption as the
operative fact instead.

**One real defect did come out of the re-grade, on presentation rather than
novelty.** The abstract asserted "The outputs differ as well" and §4 "genuinely
different matrices, not merely different presentations", while Remark 5 two
sections later substantially undercuts both; inequivalence to a single printed
representative of a choice-parametrised family is a weak signal at order 60.
Both are now scoped: the abstract says "the printed outputs differ" and points
at Remark 5, and §4 says the constructions "do not merely present the same
matrix differently".
