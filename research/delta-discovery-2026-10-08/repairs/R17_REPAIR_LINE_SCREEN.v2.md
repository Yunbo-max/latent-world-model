# R17 repair-line screen v2 — causal predictive-leakage certificate

Scope: second bounded mathematical repair of the R17 lineage. The v1 bytes, counterexamples and reviews remain unchanged. This pass is mathematics/source review only; it runs no project code, model, benchmark, training, inference, scorer, data/model download, GPU job or Docker workload.

## Three evidence-bearing patches screened

| Patch | Concrete change from v1 | What it repairs | Strongest collision/control | Decision |
|---|---|---|---|---|
| Prefix-issued upper certificate | Replace the oracle realized future Gram by an `F_t`-measurable PSD upper certificate or an ambiguity set that is fixed before the write. | Removes illegal access to the realized suffix and separates expected from pathwise protection. | robust unobservability/observability, matrix concentration, DRO, R09 dynamic Gramian, direct protected-coordinate ledger | selected for v2 theorem/control |
| Partial overwrite, `0 <= beta < 1` | Replace exact projection by `I-beta kk^T`. | Removes the exact kernel. | ordinary Delta gate/ridge shrinkage; the lost direction becomes merely condition-number amplified by `1/(1-beta)` | rejected as a candidate patch; retained as a boundary |
| Randomized quotient probes | Inject controlled perturbations along the overwrite kernel and observe later losses. | Can identify relevance that an observational prefix cannot. | experimental design/causal intervention, internal R02 and R15; changes information and consumes probe budget | parked as a separate information-changing lead, not silently composed into R17 |

## Attempt-2 delta

R17 v1 proved an exact factorization test for a *declared realized* frozen suffix, but deployment does not know that suffix. V2 does not pretend that a learned average Gram is the realized one. It derives three distinct contracts:

1. a deterministic robust ambiguity-set certificate;
2. a training-sample confidence bound for **conditional expected** leakage;
3. a separate, necessarily weaker, high-probability realized-leakage statement.

The old scalar overwrite counterexample remains. The patch therefore repairs a causal-interface error and produces a usable diagnostic, but it does not identify semantic validity, beat a direct ledger, or create a new updater.

## Decision

The selected child is `R17_CAUSAL_PREDICTIVE_LEAKAGE_CERTIFICATE.v2.md`. Its robust support function is exact, and its mean-versus-realized distinction prevents a common false safety claim. The strongest lawful rule is still an abstain/ledger control: overwrite only when the prefix-issued upper leakage falls below a declared tolerance, otherwise keep the protected sufficient coordinates directly. If write direction is optimized under the same PSD upper metric, the result collapses to R09's inverse-metric edit.

R17 remains parked after substantive attempt 2/3 as a conditional theorem/control. Candidate, admission and selection increments are zero; experimental effect is unknown. Reopen attempt 3 only with a prefix-valid certificate whose construction is justified under the deployed continuation law, whose recurring cost is below an equal-information direct sufficient-coordinate ledger, and whose mechanism claim is natively measurable rather than inferred from endpoint accuracy alone.
