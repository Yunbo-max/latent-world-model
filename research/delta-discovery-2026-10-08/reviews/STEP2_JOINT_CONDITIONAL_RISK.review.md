# Independent review — Step 2 joint conditional risk

Artifact: `STEP2_JOINT_CONDITIONAL_RISK.md`, final SHA256 `fd7ae10d232494447b1ade1f9323228118946d6f95b94ab705622eacff3b2eb5`.
Reviewers: `/root/noisy_key_math`, `/root/noisy_key_sources`. Both independently read final bytes and verified that hash. Read-only mathematical/source review; no edits or project/author execution.

## Mathematical verdict and corrections

`/root/noisy_key_math`: **accept conditional theory/target-construction lead**. Independently derived the expanded quadratic, unique ridge solution, ridge-matched factorized comparison, exact excess risk and equivalence iff the mixed-moment discrepancy annihilates the proposed edit. Checked scalar excess `9u^2/40`, PSD sandwich and contraction only in the stated metric, realizable-subspace solver, full endogenous Delta differential with chronological order, Taylor boundary and moment-estimator perturbation bound. No important mathematical error remains under the declared assumptions.

Draft hash `42ae8bf0247698c09dfbee8c405888f6ec7903c451f1cc8511e444b15fc97c3d` required two precision fixes: directional derivatives can vanish even for state-dependent features; at zero ridge the estimated Gram itself needs an inverse lower bound. Both were applied and reread. Output dimension was also renamed to avoid the posterior symbol. The fixed-law assumption explicitly excludes edits that change the law being optimized.

## Independent source/consequence verdict

`/root/noisy_key_sources`: **accept the conditional lead; no originality or candidate admission**. The strong comparator includes equally informed joint Bayesian decision/teacher models, not only an artificially factorized gate. D01/PF-RNN/general Bayesian mixtures can preserve validity–geometry dependence by conditioning future risk on branches. Full Jacobian/local-surrogate and information-access limits are correctly retained. Quadratic moment sufficiency does not establish diffusion necessity or any empirical advantage.

Actual primary readings:

- Ramírez-Hassan & Guerra-Urzola, [MELO paper](https://link.springer.com/article/10.1007/s11579-019-00246-w), version of record 2019-09-07, Math Finan Econ 14:97–120 (2020), Sec 3 Proposition 1/Corollary 1: risk-weighted posterior action already uses a joint target/weight moment divided by expected weight. Scalar zero-ridge specialization directly covers the decision principle here. Matrix/ridge result is normal-equation algebra, not a claimed first theorem. Supplement-proof download timed out, not marked read.
- Bae et al., [Amortized Proximal Optimization](https://papers.neurips.cc/paper_files/paper/2022/file/3af25aa3de8b7b02ddbd1b6be5031be8-Paper-Conference.pdf), NeurIPS 2022 archival version, Sec 3.1 Eq. 3, Sec 3.2 Eq. 4, Sec 4.1 Eq. 8/Algorithm 1, Sec 4.3 Theorem 1: function-space discrepancy, parameter ridge and inverse-Hessian geometry already exist. Separate loss/discrepancy batches do not supply unknown edit-validity labels. Paper algorithm read; dedicated author-code pin pending.
- [ROME](https://arxiv.org/html/2202.05262v5), arXiv:2202.05262v5, 2023-01-13, Sec 3.1 Eqs. 2–4/Appendix A: existing covariance-preserving rank-one edit with an explicitly supplied target. [Unified model-editing framework](https://aclanthology.org/2024.findings-emnlp.903.pdf), Findings EMNLP 2024, Sec 3 Eqs. 1–5, and [AlphaEdit](https://arxiv.org/html/2410.02355v2), v2 2024-10-21, Sec 3.2–3.3 Eqs. 8–14, further cover preservation/memorization normal equations and projected ridge. None is asserted to solve unknown validity from residuals; these are mathematical nearest works, not new pinned-code receipts.

Root independently opened MELO Proposition 1 and APO archival text; expanded editing readings above were performed by the identified source reviewer. These reads do not constitute exhaustive novelty certification.

## Native endpoint check

Source reviewer independently fetched/read `xiaowu0162/LongMemEval@9e0b455f4ef0e2ab8f2e582289761153549043fc`:

| File | Git blob SHA |
|---|---|
| README.md | `3490db4f796c14903788ecb3e33f056cab438bb0` |
| src/evaluation/evaluate_qa.py | `4732f3772b04a2b9069121ade304e6320494abc2` |
| src/generation/run_generation.py | `8e9e0f25b804d3d0afbadc9619264b0c7a275dc0` |

Knowledge-update QA is a relevant natural endpoint lead. It has history/evidence labels, not per-edit `r,u,J` or mixed-moment labels; `prepare_prompt` strips `has_answer`. The update judge accepts old information alongside the required newer answer, so it does not certify old-state release. Generation catches failures and continues; scoring skips unknown IDs and averages provided logs, requiring separate full-inventory/denominator accounting. Existing official-judge cost restrictions remain; no substitute benchmark, judge or label was created. No data acquisition/execution occurred.

**Unclosed obligations:** Delta-specific contribution and importance; real observation/supervision contract; closest joint-risk methods; estimable moments and legal deployed edit interface; native mechanism measurement and cost. The lead can support theory/target/representation research without requiring a new recurrence, but is not an active D-card, selection or scientific finding. Candidate counts stay unchanged.

## Concurrent original Step2 entry: additional independent mathematical review

`/root/noisy_key_math` also read/hash-verified the original `STEP2_REENTRY_2026-10-09.zh-CN.md` at parent `a00997c07ed02394d55cfb951542afc0a7b7de6c`, SHA256 `30fe78ef6d4cb980d5aa9ee535a50c416ce67ae562d771297dad1b4e8263a399`, Git blob `838e6146f5049e51a9f473553237eaa7810f01a6`. All four conditional mathematical propositions pass: chronological telescoping difference, matrix mixed-moment optimizer/risk and the `1/8` example, inverse perturbation bound, independent randomized-edit penalty, and observed-evidence risk value. No algebra repair required. Its two-branch specialization requires current `k,e` to be prefix-measurable; otherwise they remain inside the joint moment. Equally informed joint Bayes and matched ridge comparisons are explicit in this supplement. This closes the original note's independent mathematical-review gap, not its full source/originality/native admission gaps. The original file's bytes are preserved. Both documents belong to the same R2-C/R2-J/R2-D exploration and are not separate candidates.
