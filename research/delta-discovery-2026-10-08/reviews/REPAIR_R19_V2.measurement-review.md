# R19 v2 independent native-measurement review

- Reviewer identity: `/root/r19_v2_measurement`
- Assignment: verify fixed benchmark/interface claims, same-information controls, resource statements, mechanism observability, and cost accounting.
- Artifact SHA256: `0d771029d39677e8077b7c23d761c90b2c9ffaecf03b81781a078ec8561ed105`
- Source-audit SHA256: `c002bc988c7aab890307e21f9051c1922c1a41ac34aef55e7a090165d6baf7f8`
- Verdict: **PASS; no blocking measurement correction**

## Reasoning

LongMemEval, LongMemEval-V2, EvoMemBench, AToKE and SEAL expose useful downstream update, retrieval, temporal, forgetting, or continual-editing outcomes, but none natively exposes the destructive fiber, lawful branch relation, visible label, exact release-confusability graph, minimum code, or paired same-state release counterfactual. Computing those objects on an instrumented finite state set would be a new diagnostic with coverage assumptions, not native benchmark evidence.

The fixed repository/interface descriptions and resource limits are accurate, including SEAL's multi-GPU/default-7B and hosted-grader path. The source audit now limits external-service wording to hosted API credentials/services rather than asserting universal billing.

Required controls include direct target-signature/full-state retention, R18's ledger, no/never-release and always-release Delta, R08 with identical evidence, time-conditioned KV, matched-context full history, same-capacity replay/external KV, with oracle branch/future validity only as an upper bound. State and compute accounting includes quantization, reachable-set coverage, codebook, decoder, branch-label reliability, precision metadata, coloring construction, bytes and update cost. The measurement gap, `candidate_delta=0`, and empirical-unknown status are supported.
