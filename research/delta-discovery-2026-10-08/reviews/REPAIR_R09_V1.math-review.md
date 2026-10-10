# Independent mathematical review — R09 v1

- Reviewer: `/root/r09_frontier_math`
- Assignment: independent derivation followed by adversarial final-byte review; reviewer did not write the integrated artifact.
- Artifact: `research/delta-discovery-2026-10-08/repairs/R09_FINITE_BUDGET_OVERWRITE_PROTECTION.v1.md`
- Artifact SHA256: `d0bfe49d133abebf4574d4868cc12889a9ba97d7a6e02bb0117b8f169be625ab`
- Byte check: matched.
- Verdict: **PASS, conditional theory/control only; no candidate upgrade**.

## Checks performed

1. Dimensions and residual: `(Delta S)^T k=gamma e` gives post-edit residual `(1-gamma)e`; the general-matrix quadratic decomposes by value column.
2. Representer theorem: for `H_mu=G+mu I`, `mu>0`, the unique optimum is `gamma H_mu^{-1}k e^T/(k^T H_mu^{-1}k)` with the stated cost.
3. Frontier monotonicity: increasing `mu` weakly decreases update norm and weakly increases declared protected displacement.
4. Ordinary Delta: it is the unique minimum-energy endpoint at fixed correction, not a dominated method. The scalarized cost ratio and eigen-alignment equality condition are correct.
5. Singular limits: both `P_{ker G}k!=0` and `k in range(G)` cases, pseudoinverse formula, zero-damage feasibility, and `1/rho^2` energy blow-up are correct.
6. Hard budget: finite KKT is correctly restricted to `B>|gamma|/||k||`; the equality boundary is the singleton ordinary-Delta direction and generally the `mu->infinity` limit. Multiplier degeneracy is stated.
7. Two-cap support: the KKT direction and exact dual support formula are correct under positive caps, Slater and range conditions; boundary cases are by limits.
8. Soft solve, determinant `det(I-xk^T)=1-gamma`, protected-loss cross term, and one-step/future-path distinction are correct.

The reviewed object is a sharp static geometric certificate. It does not identify temporal validity, prove full recurrent protection, supply the metric for free, or establish empirical benefit.

## Independent adversarial check

`/root/r09_adversarial` independently attacked the minimum-budget endpoint, multiplier degeneracy, displacement-versus-loss wording, hidden state/solve/release costs, and closest-work collision. After the boundary and AlphaEdit+ corrections, the final math/source bytes received **PASS** with no remaining blocking issue.
