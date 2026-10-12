# Independent math/adversarial review — query-shift successive refinement

Date: 2026-10-12  
Reviewer: `/root/query_shift_sr_final_math`  
Host: native ChatGPT sub-agent, read-only  
Verdict: **PASS — final exact bytes**

## Exact-byte binding

- artifact: `research/delta-discovery-2026-10-08/STEP2_QUERY_SHIFT_SUCCESSIVE_REFINEMENT_2026-10-12.md`
- artifact SHA256: `e0f618e770f522d29bb60149e5d7af0d0ce1ed229817d8e5d0f244a8fbb7aef9`
- source audit SHA256: `44f41e44656f240a1f8f6857cf1a2fb80a4311d0912c57d258bdb7fcd80edb57`
- assignment bytes reviewed at launch: `a9cf36dfb1a745101fff315ca6ad4a4374bd3049d8b41754da13270c4b8cb2f0`
- repository parent: `main@4d30446a0a03ca3b3c84b9a528b500c82a263146`

## Reasoning checked

The reviewer independently checked the Gaussian two-stage ledger. From the first-message rate and the scalar Gaussian rate--distortion converse,

\[
I(B^n;M_1\mid A^n)\le n\epsilon_n.
\]

Independence gives (I(B^n;M_1)\le I(B^n;M_1\mid A^n)); adding an (n\Delta)-bit message therefore gives (I(B^n;M_1,M_2)\le n(\epsilon_n+\Delta)), followed by the exact finite-block Gaussian converse in the artifact. The asymptotic equality and factor (2^{2R_1}) were checked only on the Shannon boundary with lawful source revisit. Dimensions of (W_j=I_{d_v}\otimes G_j), rate bookkeeping, sharpness, and the Delta rank-one witness are consistent.

The review also checked the repaired boundary conditions:

- no (o(1)) is inserted into the finite-block exponent;
- the general Markov criterion is restricted to attained memoryless RDF settings, with closure/approximating-sequence language otherwise;
- the two-coordinate reverse-water-filling iff is explicitly an asymptotic Gaussian Shannon-boundary statement, not a finite-block claim;
- (R_1=0), (D_1\ge\sigma^2), (D_1=0), first-stage slack, correlation, side information, shared randomness, metadata and source-archive access are scoped;
- zero refinement loss includes the rate ordering as well as compatible RDF-optimal test channels.

## Review history retained

An earlier exact-byte round failed because the assignment file changed after the reviewer was launched; that unbound result was not reused. It also exposed the two scope defects above. The artifact was repaired and re-reviewed at the exact hashes recorded here. A subsequent source-audit-only repair changed the source hash but not the artifact; the reviewer re-read the final pair and confirmed that the source edits do not contradict the mathematics.

## Decision

No mandatory mathematical repair remains. The review passes a scoped theorem/debug control only. It does not certify originality, candidate admission, native measurement validity or empirical benefit. `candidate_delta=0`; empirical effect unknown; no code or experiment was run.
