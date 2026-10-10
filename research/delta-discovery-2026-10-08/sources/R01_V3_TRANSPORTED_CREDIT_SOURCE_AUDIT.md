# R01 v3 transported-credit quotient — source and implementation audit

Audit date: 2026-10-10  
Artifact under audit: `repairs/R01_TRANSPORTED_CREDIT_QUOTIENT.v3.md`  
Scope: closest-work/source audit only; no reproduction or model execution.

## Frozen atomic claim

For a declared future scalar-credit family along a fixed Delta tangent path, adjoint-transported credit covectors determine the exact minimum width of a value-side right quotient `X -> XW`; the formal suffix/credit class permitting arbitrary rank-one terminal covectors and ambient perturbations can force full value width. Realizability by a lawful language-model/native-loss suffix and reachable tangent is unproved.

## Primary-source and implementation comparison

| Neighbor | Inspected material and fixed locator | Mechanism overlap | Residual difference / status |
|---|---|---|---|
| Linear/nonlinear bisimulation and exact quotienting | George J. Pappas, *Bisimilar Linear Systems*, Automatica 39 (2003), DOI `10.1016/j.automatica.2003.07.003`, §6.1 Theorem 16/equation (19), Corollary 17/equations (26),(28), §7 Theorem 21/equations (39)–(41), §8.1 before/at equation (47); Paulo Tabuada and George J. Pappas, *Bisimilar Control Affine Systems*, Systems & Control Letters 52(1) (2004), DOI `10.1016/j.sysconle.2003.09.013`, Theorems 4.1 and 4.4–4.6. Exact retained URLs and excerpts are in the pinned R18 source audit below. | Output-equivalent states form a quotient defined by invariance under dynamics and indistinguishability under outputs. | R01 is a restricted matrix/right-quotient specialization, not a new quotient principle. |
| Variational observability Gramians | `mhkazma/ObsNonSys-VarGram@2bb5060454ddc63cd57681355fa6300fb9c6dc2e`, `AVarObsGram.m` blob `d2c548fe310b3e76463e5524a476199f5c482d8a`, `AVarDyn.m` blob `da73adbc53352c9a4eb24f8ae45b0bdb5677fe62` | The inspected code constructs ordered state transition products `Phi`, linear full/vectorized-state output sensitivity `Psi=C*Phi`, and `Wo=Psi'*Psi`; null directions are future-output invisible. | This evidences ordered forward sensitivity/Gramian machinery only. It neither implements a value-side right factor nor proves R01's minimum-width theorem. |
| CLUE exact lumping | CLUE paper, arXiv:2004.11961; `clue-developers/CLUE@0576e9b8477bc511e3fea29a3c296c5d30b688aa`, `clue/clue.py` blob `3226783022746ea3eeeddd207e95495be18a427b`, `clue/linalg.py` blob `c774c461e4584870b070ef3ad99f3929ec609003` | The inspected implementation computes minimal invariant subspaces/lumpings preserving declared observables. | Strong closest baseline; R01 has a closed-form adjoint specialization for a linearized Delta path, but no broader exact-lumping novelty. |
| Minimal recurrent behavioral memory and its DIACRITIC author code | Xianyao Li et al., arXiv:2609.25757v1; author implementation `XianyaoLi/DIACRITIC@08858b1c20958a2e3a4687a3502b9087ee80d0f5`, `toy/gamma_solver.py` blob `0c9b9249ed676787f92541bbf5a5d2a66b45f17b`, `certify/core.py` blob `94b5b93cd247e0312734cc2c8b9fcd33fb19794a` | Under enumerable finite histories and reset/oracle access, the inspected code refines behavioral classes with `GammaSolver.solve/gamma_J` and records/certifies environment histories. | One canonical work/evidence unit, not a generic invariant-relation certifier and not an online Delta Jacobian construction. It still covers recurrent behavioral compatibility machinery. |
| R18 recursive joint quotient in this packet | At live parent `49e6beea2d1ab454dfbdd6c34c312db5b17194df`: `repairs/R18_RECURSIVE_JOINT_QUOTIENT.v1.md`, Git blob `9fdab23b529b254b670eda326e954c3721aa300f`, SHA256 `c3b32f912637b5ba3f1e6978f0c981d517a3d561736e246a7b2d392011d8f559`; `sources/R18_RECURSIVE_JOINT_QUOTIENT_SOURCE_AUDIT.md`, Git blob `db9f2039c3e7bfc224af898b07ef444ce55a0c83`, SHA256 `235699ba4d48e4bb427e4b43bb5371f77e6f00875f789b2ed8f92c47d63ae72f` | Backward recursion `N_{j:H}=ker C_j cap J_j^{-1}N_{j+1:H}` and complete observability characterize the minimal future-output quotient of the full joint state. | R18 is broader in state/output scope. R01's residual is the explicit Delta adjoint `A^TY+G<K,Y>` and minimum right-width formula for right factors. |

## Formula/code facts checked on 2026-10-10

1. `AVarObsGram.m` explicitly orders transition products, applies the output map, and builds an observability Gramian from the resulting sensitivities; this supports the observability collision, not R01-specific novelty.
2. CLUE's inspected files expose minimal invariant-subspace/lumping routines, so exact preservation of selected observables cannot be advertised as new here.
3. DIACRITIC's inspected solver/certification files implement finite-history behavioral refinement and certification under their enumerable/reset-oracle assumptions; a stored boolean or name is not equivalent to such a certificate. DIACRITIC is the author implementation of arXiv:2609.25757, not an independent work.
4. R18 already contains the full-state backward kernel recursion and the same closest-work families. This audit explicitly depends on R18's pinned primary-source locators for the Pappas/Tabuada-Pappas and predictive-fiber families rather than reasserting title-level identity here. The v3 semantic change therefore requires a new byte-bound review but does not reset the general-mechanism collision.

## Source limits

- This run performed static primary-paper and author-code inspection only; no repository code was run and no reproduction claim is made.
- The exact R01 theorem is derived in the artifact, not attributed to any source.
- Canonical identities remain those retained in the prior audits; no title-only DOI/proceedings merge was introduced.
- No claim of exhaustive prior-art absence is made. The bounded finding is already sufficient to park because observability/bisimulation/lumping/R18 cover the quotient mechanism. Objective/goal-oriented adjoint model reduction and ordinary reverse-mode VJP/BPTT remain an additional nearest-work family to screen before any broader field claim; this open search cannot rescue the present novelty claim.

## Native measurement audit

Existing language-memory benchmarks may measure end predictions, but their native data formats/scorers do not expose the transported costates, row-span rank, or quotient-equivalence relation required by the frozen claim. This statement reuses the exact fixed assets in R18 source-audit §5: bAbI/ParlAI `a29567f7ce76992fd1f03c51ba9e3b155a37ea51`, LAMBADA/lm-eval `d6de81643928d653435c431bae19945d41d32520`, RULER official `c3f5e3b4f87f97e048793bb510a3a6b19a46bf3a` plus pipeline `e8bbff677ca2c239640dc90f93310dcf32408c93`, LongMemEval `9e0b455f4ef0e2ab8f2e582289761153549043fc`, and BABILong `7a6efee29f5cac03c3c410e6799c80fd2ffe3610`. This is an empirical mechanism-attribution gap, not a negative result or a barrier to checking the theorem itself. A custom diagnostic would not satisfy the current native-benchmark obligation.

## Verdict

`REROUTE_REPLICATION_OR_TRANSFER` / theory-control only. Mathematical specialization may be useful, but the essential mechanism collides with established observability, bisimulation, exact lumping, and the packet's broader R18 construction. No novelty pass; candidate delta remains zero.

