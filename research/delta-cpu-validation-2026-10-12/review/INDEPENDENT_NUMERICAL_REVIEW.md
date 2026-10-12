# Independent numerical source/result audit

Reviewed on 2026-10-12 under `delegations/cpu_numeric_review.json`. This is a minimal-context source and produced-result audit. The reviewer did not execute numerical workloads, build a separate implementation, obtain unseen samples, alter producer scripts, or confirm a scientific method independently. Its independence is reviewer judgment about the supplied code and raw records, not independent experiment replication.

## Finding and scope

The inspected algebra implementations have useful non-identical references: affine/full-state rollouts, elementary-matrix transpose construction, equality-KKT systems, lifted ODE exponentials, SVD versus Gram eigensystems, finite graph coloring, finite action enumeration, convex optimization, and quadrature. The observed completed records reproduce their declared identities and boundary examples. I found no consequential numerical formula error in those records. This does not establish all assertions in a source document, native model efficacy, deployment safety, originality, or practical superiority.

One genuine source assumption defect is reproduced: `rejected/LYAPUNOV_OBLIQUE_METRIC.md` states the SPD-certificate iff `0<c<=2` without excluding the identity update. With `w=0`, `r!=0`, the map is identity, `c=0`, and every SPD metric is a certificate. The legacy check correctly records `archived_statement_needs_degeneracy_clause`. Preserve the archived bytes and issue an erratum: either restrict the theorem to `wr^T!=0`, or handle identity factors separately. This is an assumption omission in the printed source, not failure of its nontrivial oblique construction.

Pass counts must mean diagnostic assertions passed. In particular, a passed impossibility/counterexample check means the intended failure boundary was reproduced; it is not a successful updater. Report check executions, unique check definitions, and repair-lineage coverage separately. Several deterministic examples are identical across seeds; three seeds are not three independent scientific experiments.

## Audited bytes and available raw records

Initial assigned script hashes matched the delegation:

| File | Initial SHA256 |
|---|---|
| `scripts/check_algebra.py` | `fd7da3dbce525e674a8d965eb61d324e186f11c8c1e47b11619469c56acc54ee` |
| `scripts/check_statistics.py` | `84d1c41e0551dfe5a87cc90f8c89b999b3edeec54d3340fc7941cd0fd1f10403` |
| `scripts/check_feedback.py` | `c039c6dcbe02c4c5c61a7016eb6f24e784cdb5a2b52bd1c8127d469d1740b258` |
| `scripts/check_legacy_controls.py` | `0af849e641a9ada1776a4b482482ad531287ce2531e72a3117fbaf47b6922b33` |
| `scripts/guard_cpu.py` | `13dc421cb6e5c4bdd768051fb205a1bd6faca8133603b0f42245c9691e2c64f8` |

During review, the controller and statistics producer made disclosed repairs, preserving checkpoints. I inspected the revised feedback four-arm code, resource-label clarification, HiGHS options, and executed-zero-score R17 branches statically. At that inspection their hashes were:

- Feedback: `dfc7760f9da83b027c15ad1286fc84a15d8dce2b1186f74e5f83c33254cfc65f`.
- Statistics: `f3a846763770aa63a0c271667d6693970f30562d86571696d263a918fe7b89f6`.
- Guard: `1d23798c360ec669abb32ad2be08cbca5d61030e14fb10d367867d086126a934`.

The initially inspected completed records were algebra seeds 0, 1, 2 (24 passed each), statistics seed 0 (23 numerical checks plus one source-integrity check passed), legacy seeds 0, 1, 2 (12 passed each), and feedback seeds 0, 1, 2 under the earlier witness implementation (5 passed each). Raw feedback seed 1 gives immediate displacement energy 0 and later displacement energy `0.053388066758518156`; its finite-difference sensitivity is `0.3985196846689742` versus analytic `0.39851968468229415`. Algebra seed 0 full-feedback Jacobian errors across three stepsizes are well below the declared finite-difference tolerance, and its frozen versus actual memory block gap is `0.08861776262700743`.

Old records are not evidence that newly added code executed. Result filenames, runner records, exact script hashes, and the final evidence manifest must identify the bytes actually used; the feedback/legacy JSON shorthand `source_refs` alone does not hash-bind their source snapshots. Revised result inspection is recorded below when available.

## Consequential interpretation and remaining limitations

### 1. Local protection and feedback

The original feedback witness is a valid two-step Delta example: writing to the first coordinate immediately leaves the second protected coordinate unchanged, but a later gate reads the first coordinate and changes the second-coordinate output. The reported `damage` is squared displacement from the no-write output. Calling it increased semantic or task loss additionally requires a protected target; none is supplied.

The revised code now supplies four named rules: no write, ordinary Delta, a local-score gate, and a future-informed audit control. Ordinary and local-gate actions coincide because the local protected score is zero; this is expected for the chosen witness. The future-informed rule uses the analytic future response and is correctly labeled extra information. It is a useful audit control, not a same-information baseline demonstrating a method advantage. This fixture refutes the unqualified local-to-global implication; it does not test every protected updater or learn a local-protection method. The `gamma=0` rows provide the no-feedback positive case. The complete-Jacobian algebra fixture more broadly includes state-dependent key, value, gate, decay and updater feedback, but remains a smooth tiny constructed system.

### 2. Cost comparison and resource accounting

The feedback factor/dense equality is valid in the stated C-order coordinates. Timing the dense arm includes constructing a Kronecker Jacobian and a dense rank-one outer product on every call; the factor arm uses already available `A,K,G,X`. The factor arm also uses a dense `A@X`, rather than exploiting the original erase factor directly. These are two representations of a supplied tangent, not full forward/reverse training paths. Seven paired randomized repetitions are transparent exploratory timings. Their results cannot establish superiority over ordinary matrix-free JVP/VJP, checkpointed reverse mode, or a direct credit predictor. Basis discovery, quotient SVD, feature/derivative acquisition, calibration, and full recurrent execution are absent.

`factor_stored_bytes` counts `A,K,G,X`; `dense_jacobian_bytes` counts only the Jacobian. They are explicitly different object counts, not comparable complete peak-memory measurements. Dense construction temporaries and common inputs are not included in the latter. Report them as named array payloads. Whole-command RSS/CPU telemetry cannot attribute peak memory or CPU seconds to either arm.

All inspected initial resource JSONs have `proc_rss_samples=0`. Their kernel child-max-RSS readings are usable Linux command-level telemetry but can include pages inherited on fork. The sampled RSS stop condition was inactive in these runs. `RLIMIT_DATA` caps data allocations, not total RSS, so do not claim a hard 256 MiB RSS guarantee. The revised guard accurately labels the requested thread environment and `actual_solver_threads: not_measured`. The new statistics script adds `threads=1, parallel=False` to all HiGHS calls; this repairs the previous solver-specific omission, but configuration still does not measure realized thread count. Do not interpret old `threads:1` metadata as measurement.

### 3. Some asserted boundaries were stipulated, not separately derived

`r08_action_identification` supplies `H,UR,UK`, sets identical keep-record arrays in both worlds, then checks interval arithmetic. It does not instantiate both complete action-specific hidden-state/signal/loss experiments and derive their record laws and action values. The source contains a sound explicit world construction; the script only checks its reduced numerical consequences. To claim a fully executed two-world experiment, enumerate validity and signals under each channel and calculate both complete observable keep laws and reoptimized terminal risks.

The QWRD one-bit observation result is assigned the same residual expression as observation error instead of evaluating an explicit encoder/decoder. Its non-Gaussian one-bit zero-distortion example is assigned `0.0`; compound correlated-source distortions are assigned analytical formulas. These are useful sanity boundaries but not separately implemented coding experiments. Explicit finite lookup encoders/decoders would strengthen the former. Do not present convex rate allocation as implementation or achievability of an asymptotic Gaussian code.

The original R17 zero-residual and gate metrics were constants. The revised source now actually evaluates the zero-residual and nonzero-residual/orthogonal-score branches, checks energies and finite outputs, and resolves this specific omission in the revised executed records. Its `missing_tail_true_score` evaluates the certificate envelope `U`, not actual protected Gram `G`: a positive value shows omitted certificate curvature, not a separately observed protected-loss or interference-budget violation. Its interpretation's "unsafe direction" should be read as an invalid tail-free certificate; a direct budget-failure claim would require evaluating actual output energy along that direction. Other constant boundary labels, such as R18 path-specific zero tails, must be distinguished from computed quantities; R18 does separately evaluate its full-ledger zero projector.

### 4. Algebra coverage is conditional and usually partial

The random A01 case has minimum right width 4, equal to its ambient value width 4. It supports minimality/credit reconstruction, not useful compression. The separate zero-coupling case shows a proper smaller transported envelope. A01 generic `K` is permitted by the source's declared tangent law; the separate feedback map uses rank-one Delta `K`.

R06 allocation tests the uncapped endpoint only; it does not cover active probability caps or long-horizon floating-point underflow. R09 verifies Gramian/core inverse action and robust projection, not a general robust QCQP optimizer. R13 tests a one-dimensional overwrite kernel and zero-budget tail; it does not verify every nonzero-rank approximation budget. R18 validates fixed-ledger Rayleigh equality and a safe sum-PSD envelope; its robust optimum is independently checked only in the two-dimensional complementary-path example. R19 enumerates small prime fields 2 and 3, not extension-field arithmetic or a physical quantized Delta implementation.

In the initial A21 record, `common_ledger_worst_leakage` and `common_envelope_tail_certificate` are eigenvalue coefficients `Lambda(V)` and `lambda_(r+1)(Gamma)`. To obtain absolute paired-output energy multiply by `R^2`. Here `R=1.4`, so seed-0 coefficients `0.2179501661994297` and `0.493289883119291` must each be multiplied by `1.96`. The earlier attained path-energy comparisons already include radius squared. Keep coefficient and energy units explicit.

### 5. Tolerances and numerical conditioning

The algebra suite records norm error, scale and allowable error. Observed selected direct identities are at roughly machine precision, not merely just inside a broad threshold. Its finite-difference checks use multiple stepsizes, a useful check against one accidental stepsize. Statistical optimizer comparisons use `2e-6`, appropriately looser than deterministic FP64 equality checks, but most optimization records do not expose constraint residuals, stationarity, or conditioning. Solver success plus objective agreement supports these small examples, not every optimum. Add primal residuals/dual or KKT gaps for consequential future optimizer comparisons.

Ranks use fixed relative/absolute SVD thresholds, while graph closure uses exact `!=0` on deliberately sparse coordinates. The nearzero-edge example is meaningful in that fixture; exact-zero graph decisions should not be carried into learned floating-point keys without an error contract. Most random matrices are well conditioned by construction, so the batch is not a numerical robustness stress test. An isolated relative error of 1 for an expected-zero output is harmless when its absolute residual is at machine precision; summaries should use the absolute criterion in such cases.

## Recommendation

Accept the completed records as scoped constructed numerical diagnostics after binding them to their actual script/source hashes. Preserve the expected-negative classification and the Lyapunov degeneracy erratum. Do not upgrade conditional theorem/control status or claim native, scientific, causal-deployment, or full-cost validation. The highest-value additional work would be fully enumerated R08 channels, explicit finite encoders for stated coding examples, solver feasibility/KKT metrics, near-degenerate/rank-threshold cases, and same-information matrix-free full-path cost controls. These are coverage improvements, not prerequisites to reporting the narrower observed numerical agreement.

## Revised result inspection

The revised raw records arrived and were inspected before finalizing this review:

| Records | Observed outcome | Consequential repaired metric |
|---|---|---|
| `statistics-seed-1-v2.json`, `statistics-seed-2-v2.json` | 23 numerical checks plus one integrity check passed per record | R17 actually evaluates zero-residual and orthogonal nonzero-residual cases: each score and energy is 0, gate is 1, finite-value assertions pass. |
| `feedback-seed-0-v4.json`, `feedback-seed-1-v4.json` | Six checks passed per record | Local gate and ordinary Delta both use beta 1 and later displacement energy `0.053388066758518156` against budget `0.01`; future-informed beta `0.4054651081081642` yields later energy `0.009999999999999995`, with new-write residual `0.35347173767683693`. |
| `algebra-seed-3-v3.json` | 24 checks passed | A21 separates coefficients `0.7432838797972847`, `1.3959020791226129` from radius-scaled energies `1.4568364044026778`, `2.735968075080321`. |

The revised algebra bytes have SHA256 `b1987232f887ea87f3c16ce0dd41dc0a5b0775a07b6e5a1c329ade04ce9b1cf8`. Diff inspection shows the change adds explicit coefficient and scaled-energy fields while retaining the earlier coefficient fields; it does not change the scientific calculation. The revised statistics and feedback hashes are those listed above. Resource records from revised runs now distinguish requested thread configuration from unmeasured actual solver threads and continue to disclose zero `/proc` RSS samples.

All listed original and revised raw outcomes are consistent with the code's intended scoped assertions. The resolved omissions are the missing executed four-rule audit, the R17 zero-score branches, HiGHS-specific thread configuration, ambiguous resource labels, and A21 energy-unit labeling. The remaining limitations above still apply. The reportable final union is 65 distinct numerical check IDs plus one source-integrity ID, with representative diagnostic coverage of all 20 latest repair lineages; neither check IDs nor lineage coverage are independent scientific replications or full-source verification.
