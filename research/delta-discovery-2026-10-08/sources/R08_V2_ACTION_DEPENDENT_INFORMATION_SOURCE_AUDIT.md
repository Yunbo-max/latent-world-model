# R08 v2 source and novelty audit — action-dependent information value

Audit scope: exact two-stage binary Bayes-envelope identity, action-dependent observation, Blackwell ordering, controlled sensing, temporal editing assets, and native measurement. This is source/formula review only; no model or benchmark execution.

## 1. Primary decision-theory and control sources

### Blackwell comparison of experiments

- David Blackwell, **Equivalent Comparisons of Experiments**, *Annals of Mathematical Statistics* 24(2):265–272, 1953, DOI [`10.1214/aoms/1177729032`](https://doi.org/10.1214/aoms/1177729032), Project Euclid article/PDF.
- The paper proves equivalences between informativeness comparisons and decision-problem performance, including garbling-style comparisons. R08 v2 uses only the standard implication: for the **same prior and same decision problem**, a Blackwell-more-informative experiment weakly lowers optimized Bayes loss.
- It does not compare actions that change memory, immediate cost, state transition, or terminal loss table. R08 v2 explicitly retains those terms in `Q_R-Q_K`.

### Controlled-sensing POMDP

- Vikram Krishnamurthy, **POMDP Structural Results for Controlled Sensing**, [`arXiv:1701.00179v1`](https://arxiv.org/abs/1701.00179v1), 2017.
- Section II, eqs. (2)–(3) give the action-dependent Bayesian filter and Bellman equation; Section II-A, eq. (6) gives the controlled-sensing Bellman form. Theorem III.1 states concavity of the value function under concave instantaneous costs. The paper explicitly reviews monotonicity, Blackwell dominance, and quickest detection.
- This directly covers the general action-dependent observation/Bellman mechanism. R08 v2's contribution relative to it is only the finite two-stage binary absolute-margin reduction and the Delta loss-table interpretation.

### Controlled and scarce observation in change detection

- Venugopal V. Veeravalli, Georgios Fellouris, and George V. Moustakides, **Quickest Change Detection with Controlled Sensing**, [`arXiv:2310.17223v1`](https://arxiv.org/abs/2310.17223v1), 2023; later IEEE JSAIT DOI [`10.1109/JSAIT.2024.3362324`](https://doi.org/10.1109/JSAIT.2024.3362324).
- The problem statement makes observation distributions depend on the chosen action and jointly designs the sensing policy and stopping rule. Section II, Assumption 1 and eqs. (1)–(4) define the action-controlled likelihood process; Section IV, eq. (15) gives the controlled statistic. Its finite-action, uncertain post-change, minimax/asymptotic objective differs from R08's Bayesian two-stage loss table, but it is a direct collision for the claim that action-dependent evidence is new.
- Erhan Bayraktar and Ross Kravitz, **Quickest Detection with Discretely Controlled Observations**, [`arXiv:1212.4717v3`](https://arxiv.org/abs/1212.4717v3), 2014. Section 2, Definition 2.1, eqs. (2.1)–(2.7), and Proposition 2.3 state the finite observation-rights problem and posterior state; Section 5 gives the dynamic construction. It directly covers costly/limited observation as a control object.

### Expected value of sample information

- Anna Heath, Ioanna Manolopoulou, and Gianluca Baio, **Efficient Monte Carlo Estimation of the Expected Value of Sample Information Using Moment Matching**, *Medical Decision Making* 38(2):163–173, 2018, DOI [`10.1177/0272989X17738515`](https://doi.org/10.1177/0272989X17738515); preprint [`arXiv:1611.01373v1`](https://arxiv.org/abs/1611.01373v1).
- Section 1, eq. (1) defines EVSI as expected optimized posterior net benefit minus optimized current net benefit; Section 2.4 uses the posterior/preposterior distribution of incremental net benefit. This directly supports the standard value-of-information layer. R08's expected absolute affine-margin formula is an elementary binary-loss specialization, not a new EVSI principle.

## 2. Formula audit

For two affine terminal risks `L_0,L_1`, the identity

`min(L_0,L_1) = [L_0+L_1-|L_1-L_0|]/2`

is elementary. Conditional posterior calibration cancels the affine sum, leaving

`VoI = [E|delta(P')|-|delta(p)|]/2`.

This is a binary expected-value-of-sample-information specialization of standard Bayes risk/Blackwell theory, not a new theorem. The same-mean/same-variance counterexample is an internal construction; its likelihood table is explicitly given in the math artifact and does not rely on a source claim.

The actionwise decomposition

`Q_a = immediate_a + memory_baseline_a - information_value_a`

is the two-stage Bellman equation with terms exposed. It is useful debugging because it prevents an information bonus from silently absorbing memory damage or state change, but it does not escape controlled-sensing POMDP prior art.

## 3. Reused temporal-editing source pins

R08 v1's source audit remains part of the lineage and is not overwritten. It was re-read from exact remote main `4dad0e013c2b70893c42c7ddcd5824b172286c61` at `sources/REPAIR_R08_TEMPORAL_VALIDITY_SOURCE_AUDIT.md`, recorded SHA256 `dfd8c1ed84d1512698e995c708683980d6d27d9d7e4cb4a173d6cbafe1093d1a`:

- Adams and MacKay, **Bayesian Online Changepoint Detection**, [`arXiv:0710.3742v1`](https://arxiv.org/abs/0710.3742v1), eqs. (1)–(16) and Algorithm 1: posterior run-length recursion and exact online algorithm.
- Michael J. Q. Zhang and Eunsol Choi, **Mitigating Temporal Misalignment by Discarding Outdated Facts**, [`arXiv:2305.14824v3`](https://arxiv.org/abs/2305.14824v3), EMNLP 2023 DOI [`10.18653/v1/2023.emnlp-main.879`](https://doi.org/10.18653/v1/2023.emnlp-main.879): fact-duration posterior and downstream retrieval/discard routing are direct belief-to-action neighbors.
- AToKe, [`arXiv:2312.05497v3`](https://arxiv.org/abs/2312.05497v3), paper Sections 3.3–3.4, author repository pinned in v1 audit at commit [`a1b42e34e4130507220307ced3d681fb8719831f`](https://github.com/Arvid-pku/ATOKE/tree/a1b42e34e4130507220307ced3d681fb8719831f): temporal old/current QA endpoints but no action-specific sensing/propensity/paired outcome object and no executable native scorer in the audited fixed repository.
- StableEdit, [`arXiv:2605.11836v2`](https://arxiv.org/abs/2605.11836v2), paper Sections 2.1–2.2, 3.1, and 4, author repository pin [`be5769232cf5ba160d8f011dfb9a6d0b5a2a6470`](https://github.com/MINE-USTC/StableEdit/tree/be5769232cf5ba160d8f011dfb9a6d0b5a2a6470): sequential edit stabilization and parameter-shift interface, not temporal-validity sensing.
- RLEdit, [`arXiv:2502.05759v4`](https://arxiv.org/abs/2502.05759v4), paper Section 3.1.1 and Appendix D, author repository pin [`c6576a1e8e8a122c54d61ec5580ec7397e740a42`](https://github.com/zhrli324/RLEdit/tree/c6576a1e8e8a122c54d61ec5580ec7397e740a42): stateful control over prescribed edit sequences, not an identified keep/release observation channel.

No new author implementation is claimed for Blackwell's 1953 theorem or the elementary envelope identity. The controlled-sensing papers are theory baselines; R08 v2 does not copy or relabel their algorithms as a new implementation.

## 4. Native measurement audit

The required causal record would contain, before the first action, `(p,m,G_R,G_K)`, the declared action-specific likelihoods or randomized sensing propensities, the realized signal, terminal loss coefficients/action margin, query cost, and identifiable keep/release outcomes. The temporal editing assets read in v1 do not jointly expose these fields.

AToKe can assess whether supplied historical/current facts are retained after a prescribed edit. It cannot natively estimate the counterfactual differential information term because there is no randomized keep/release sensing action with paired or identifiable downstream signals. This is a measurement gap, not a negative experimental result.

## 5. Novelty and disposition

Collision status:

- binary Bayes envelope and expected information value: **known**;
- garbling/Blackwell ordering: **known**;
- action-dependent observations and Bellman control: **known**;
- scarce/costly change-detection observations: **known**;
- temporal fact validity and sequential editing: **known neighboring mechanisms**;
- explicit Delta signed-margin loss table inside the two-stage decomposition: **narrow specialization/bridge**.

The repair is source-supported and mathematically useful but not a distinct scientific method. It remains parked conditional theory/control, candidate delta 0, empirical status unknown. Reopening requires a Delta-specific smaller sufficient state or matched-budget estimation advantage, or a native causal temporal action object.
