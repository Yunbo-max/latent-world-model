# R14 v3 observable-equivalence source and novelty audit

Audit date: 2026-10-11. Scope: primary theory sources, already pinned R14 sources and native-measurement feasibility. No project code, benchmark, training, inference, scorer, data/model download or GPU work was executed.

## Decision

The v3 certificate-collapse and risk-floor derivations are self-contained and mathematically checkable. Their general mechanisms are not novel: meaningful distribution-free conditional coverage is known to be impossible without assumptions; two-point/Le-Cam arguments convert indistinguishable observation laws into minimax risk; data processing prevents a statistic from increasing total-variation separation; robust Bayes/minimax routing already covers the attaining action. Retain the exact Delta-slot specialization as a terminal theorem/debug control, not a new updater.

## Primary sources actually inspected

| Source | Fixed version / part inspected | Coverage and residual |
|---|---|---|
| Barber, *Is distribution-free inference possible for binary regression?* | arXiv:2004.09477v3 (7 Oct 2020), Electronic Journal of Statistics 14(2), Definition 1 Eq. (3), Theorems 1--2 | directly studies confidence intervals for the conditional Bernoulli probability and proves sample-size-independent expected-length lower bounds without structural assumptions for nonatomic distributions. This is the closest published collision for a distribution-free interval around `P(J=1|F)`. Its i.i.d. random-covariate setting does not itself prove R14's sequential prefix theorem, so v3 keeps a separate self-contained two-world proof. |
| Barber, Candès, Ramdas & Tibshirani, *The limits of distribution-free conditional predictive inference* | arXiv:1903.04684v2 (15 Apr 2020), Eqs. (1)--(3), Sec. 2.2 Proposition 1, Sec. 3 | distinguishes marginal from object-conditional coverage and states that distribution-free exact conditional coverage forces uninformative/infinite-length sets at nonatomic covariates. This is a stronger general collision for broad “tokenwise certificate without assumptions” claims. R14 v3 uses a simpler finite binary two-world lemma tailored to a posterior parameter rather than a response prediction interval. |
| Vovk, *Conditional validity of inductive conformal predictors* | arXiv:1209.2673v2 (24 Sep 2012), Secs. 2 and 5; Proposition 1 for unconditional exchangeable validity and the negative object-conditional discussion | confirms that standard inductive conformal validity is unconditional/exchangeability based and that precise useful object-conditional validity is generally unavailable away from atoms. It does not construct a tokenwise provenance-posterior interval. |
| Tibshirani, Barber, Candès & Ramdas, *Conformal Prediction Under Covariate Shift* | NeurIPS 2019 primary paper, abstract and weighted-exchangeability setup | shows that moving beyond exchangeability requires a stated shift model/likelihood ratio (known or estimated). This supports charging a changed observation law or shift assumption as new information, not treating “conformal” as an automatic deployment certificate. |
| Polyanskiy & Wu, *Dualizing Le Cam's method for functional estimation I: General theory* | Annals of Statistics 54(1):1--24 (2026), DOI 10.1214/25-AOS2498; arXiv:1902.05616v2, Sec. 1 and proof of Theorem 1, Eqs. (20)--(21) | directly covers the general principle that statistically close observation laws impose minimax lower bounds. R14 v3's factor `(1-TV) lambda/(1+lambda)` is a direct common-measure specialization to the declared two-slot loss. |
| Qiu & Luedtke; Chen et al.; Perez-Lebel et al.; Zhou & Zhu | fixed versions and author interfaces already recorded in `R14_V2_CREDAL_PROVENANCE_SOURCE_AUDIT.md` | cover Gamma-minimax/credal decisions, posterior error to decision regret and certificate assumptions. They remain authoritative for v2; v3 does not recount them as new work. |
| R14 v1/v2 project records | exact artifacts and independent reviews on live `main` | v1 gives the point-posterior Bayes action and identity ambiguity floor; v2 gives the posterior-set minimax action and misspecification boundary. V3 closes the remaining certificate-oracle gap and preserves both. |

## Formula-level collision and retained delta

The generic two-point principle is classical: if `Q_1` and `Q_2` overlap, no decision rule can behave as an oracle on their common mass. Likewise, a uniformly valid interval for opposite endpoint targets must contain both endpoints wherever the two coverage events overlap. Data processing for total variation prevents a residual, hidden state or learned score computed from the same record from making the worlds more distinguishable.

The retained project-specific delta is narrow:

1. an exact finite binary certificate-collapse probability `(1-2 alpha-delta)_+` for the R14 posterior interval;
2. the exact common-measure lower bound `(1-delta) lambda/(1+lambda)` for the R14 two-slot loss;
3. equality at `delta=0` with the v2 symmetric continuous action and the contrasting hard-action no-write rule;
4. an explicit proof that the remaining “certificate” assumption is an information/assumption requirement rather than a Delta geometry problem.

These are theorem and debugging contributions, not architecture novelty or a priority claim.

## Implementation and measurement boundary

No inspected primary source offers a native Delta-memory provenance benchmark or all-action potential-outcome scorer. The theorem does not require author code: its observable-law and loss statements are analytic, and code execution would not establish universal coverage or novelty.

Current native assets can measure end-task accuracy, language loss, retrieval, or post-edit efficacy/locality. They do not jointly expose the hidden slot identity, paired worlds with the same pre-action record, a valid per-token posterior set, and losses for all counterfactual writes. Therefore `native_measurement_supported=false` for the mechanism. A future custom paired record would change the current benchmark contract and is not invented here.

## Final source verdict

- `math_support`: primary theory supports the general tools; exact constants require independent derivation review;
- `novel_method_supported=false`;
- `useful_theory_control=true`;
- `native_measurement_supported=false`;
- `experiment_status=unknown`;
- `candidate_delta=0`;
- `disposition=park_attempt3_exhausted`.

