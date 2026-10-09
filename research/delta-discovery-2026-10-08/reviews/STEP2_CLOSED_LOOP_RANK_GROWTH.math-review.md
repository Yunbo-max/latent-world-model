# Independent mathematics review: closed-loop Delta tangent rank growth

Reviewer: `/root/full_loop_rank_math_review`  
Assignment: independent semantic review of differentiation, dimensions, rank bounds, tight shared-gate construction, contraction scope, Eckart--Young tail, ordered truncation recursion, costate error and overclaim boundaries.  
Artifact: `research/delta-discovery-2026-10-08/STEP2_CLOSED_LOOP_RANK_GROWTH.md`  
Reviewed SHA256: `4839d87111588059f3db84e01f77de3aa836f15e7746c055beaae449da39a789`  
Mode: static mathematics only; no project/upstream execution, tests, training, inference, scoring, downloads, GPU or Docker.

## Decision

**ACCEPT** as a conditional Delta-specific theorem/control, not a candidate or empirical result.

## Reasoning checked

1. For fixed future `D,k,v` and state-dependent scalar gate, differentiating
   `F(S)=(I-beta(S)kk^T)DS+beta(S)kv^T`
   gives exactly
   `X^+=((I-beta kk^T)D)X+k e^T<G,X>_F`; dimensions and residual convention are consistent.
2. Left multiplication cannot increase matrix rank and each feedback injection is rank at most one, so the stated finite-horizon rank bound follows by subadditivity.
3. The shared sigmoid gate, unused successive key rows and matching value residuals form a legal nominal Delta path and attain rank H with the document's indexing.
4. The strictly contractive statement is correctly limited to nominal one-step Jacobians; it separates algebraic rank growth from numerical retention and does not claim global nonlinear contraction.
5. The embedded-identity construction has the stated best rank-r Frobenius and spectral errors by Eckart--Young--Mirsky.
6. With `Q_j=A_j hat X_j-T_r(A_j hat X_j)`, the exact error recursion is `E_(j+1)=A_jE_j+Q_j`; the ordered variation-of-constants, product-norm and final costate bounds follow.
7. The artifact explicitly avoids the invalid stronger claims that matrix rank is a general memory/communication lower bound, that a scalar current VJP keeps full forward sensitivity low rank, or that rank growth proves forgetting/RSI/scientific value.

Optional editorial clarification noted by the reviewer: one may state `C>=1` and compatible matrix/operator norms in the product bound. This is not a correctness blocker and no byte change was required.
