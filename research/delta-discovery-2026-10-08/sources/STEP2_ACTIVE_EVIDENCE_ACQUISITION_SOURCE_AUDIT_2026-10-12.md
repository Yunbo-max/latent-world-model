# Source and nearest-work audit: active evidence before a Delta write

Date: 2026-10-12  
Artifact: `STEP2_ACTIVE_EVIDENCE_ACQUISITION_2026-10-12.md`  
Scope: primary-source formulas, current LLM-memory mechanisms, and native measurement assets. No model or project code was executed.

## 1. Controlled sensing is the decisive mathematical parent

Nitinawarat, Atia, and Veeravalli, “Controlled Sensing for Multihypothesis Testing,” arXiv:1205.0858v6 (2013-09-04), https://arxiv.org/abs/1205.0858.

- Section II, equations (1)--(4): finite control alphabet, action-dependent observation laws, conditional independence, and open-loop/causal policies.
- Section III-A, Proposition 1 and equations (6)--(8): the binary fixed-sample asymptotic exponent is the maximum Chernoff information over controls.
- Remark 2: a pure stationary open-loop control suffices for that binary asymptotic exponent.
- Section III-B, equations (9)--(10): multihypothesis mixtures and causal posterior/ML-dependent control.

The artifact's probe is a sensing control, provenance is the hidden hypothesis, and write amplitude is the terminal decision. Its one-probe finite-sample Bayes formula is not claimed to be the paper's Chernoff-exponent result. Verdict: decisive mechanism collision.

## 2. Comparison of experiments and decision-directed tests

- Blackwell, “Equivalent Comparisons of Experiments,” 1953, https://doi.org/10.1214/aoms/1177729032. The garbling order is generic statistical decision theory.
- Javdani et al., “Near Optimal Bayesian Active Learning for Decision Making,” AISTATS 2014, https://proceedings.mlr.press/v33/javdani14.html. Section 2, equations (1)--(2), selects tests to identify a decision region rather than reduce uncertainty for its own sake.
- Chen, Hassani, and Krause, “Near-optimal Bayesian Active Learning with Correlated and Noisy Tests,” AISTATS 2017, https://proceedings.mlr.press/v54/chen17b.html. The formulation covers correlated/noisy tests and prevents multiplying copied web sources as independent evidence.

These sources block novelty of downstream-risk-directed probe selection.

## 3. Recent memory-system neighbours

### RIME

Zhou et al., “Remember by Asking: Retrieval-Induced Memory Evolution for LLM Agents,” arXiv:2609.34438v1, https://arxiv.org/abs/2609.34438.

- Section 3.1, equations (1)--(6): fixed generic formation questions retrieve dialogue evidence and expand context.
- Equations (7)--(11): retrieve historical memories, then emit ADD/UPDATE/DELETE/NOOP while preserving temporal/provenance information.
- Section 3.2, equations (12)--(13): source-dialogue fallback.
- Anonymous author code linked by the paper: https://anonymous.4open.science/r/RIME_official-4BC7. No stable author commit was available, so no commit pin is claimed.

RIME is a direct retrieve-before-consolidate baseline, though it does not optimize a calibrated external channel for Delta stakes.

### REALM

Song et al., “Retrieval-Driven Memory Reconsolidation for Long-Term LLM Agents,” arXiv:2609.16053v1, https://arxiv.org/abs/2609.16053.

Section 3.3 and Appendix C describe retrieval plans and sufficiency-controlled expansion; Appendix C equation (14) scores graph edges. It is a broader graph-memory reconsolidation neighbour, not the binary Delta Bayes rule.

### SAGE novelty gate

Wang, Brahma, and Henao, “SAGE: A Novelty Gate for Efficient Memory Evolution in Agentic LLMs,” arXiv:2605.30711v2, https://arxiv.org/abs/2605.30711; author repository https://github.com/swang1024/SAGE.

The repository is a mem0 fork. Relevant root-relative paths are `mem0/memory/novelty_gate.py`, `mem0/memory/main.py`, and `mem0/llms/usage_tracker.py`. No reliable code commit was exposed in the inspected short history, so no code pin is claimed. SAGE blocks novelty of same-information novelty-aware pre-write gating, but does not acquire an action-dependent external observation channel.

### SAGE statistical acceptance gate

Wang et al., “SAGE: A Statistical Acceptance Gate for Self-Evolving Agents,” arXiv:2609.36043v1, https://arxiv.org/html/2609.36043v1. Sections 3.1--3.3 describe paired candidate/incumbent validation, asymmetric regression penalties, a one-sided paired test, and abstention. This is a post-edit acceptance gate over a fixed validation set, not prospective selection of a provenance-evidence channel before one Delta write.

## 4. Native measurement assets

- LoCoMo project/repository: https://snap-research.github.io/locomo/ and https://github.com/snap-research/locomo. The native entry `task_eval/evaluation.py::eval_question_answering` reports F1 for most QA categories; the adversarial category uses an abstention check. Evidence recall is available only when supporting dialogue IDs are supplied.
- LongMemEval: https://github.com/xiaowu0162/LongMemEval and the ICLR 2025 proceedings record https://proceedings.iclr.cc/paper_files/paper/2025/hash/d813d324dbf0598bbdc9c8e79740ed01-Abstract-Conference.html. Native paths `src/evaluation/evaluate_qa.py` and `print_qa_metrics.py` use the official GPT-4o answer judge; `answer_session_ids` and `has_answer` are retrieval/evaluation labels, not deployable evidence actions. The asset supports timestamped sessions, QA, and evidence-session analysis, not a pre-write probe decision.
- CounterFact and zsRE through the official EasyEdit repository, https://github.com/zjunlp/EasyEdit, support edit efficacy, paraphrase/generalization, and locality. They do not natively label incumbent validity, provenance, protected old-capability panels, or Delta-specific `A,B` stakes.

The strongest native comparator uses the same archive/history access, answerer or judge, context/token budget, and tool/API-call budget, with retrieval and probe costs logged. Full-history is an added-information upper bound unless those resources are genuinely matched. For model editing, edit/no-edit and established-editor controls use the same cases; compute/API costs must be measured or explicitly reported rather than assumed equal from a matched case budget. Retrieval recall is diagnostic, not a substitute for QA. None of the inspected assets supplies the complete prospective active-probe causal object. New provenance-validity labels, legal probe actions, protected-query annotations, logged actions, calibrated costs, and matched outcomes would be required.

## 5. Audit verdict

The exact retained difference is

\[
\text{normalized Delta direction}\rightarrow(A,B)\rightarrow b^*(p)\rightarrow\text{risk-weighted probe value}.
\]

The Delta stake reduction is transparent and useful. The active acquisition and comparison machinery is classical controlled sensing, Blackwell ordering, and decision-directed testing. Verdict: useful scoped theorem/control; mechanism-level collision; not a candidate. Empirical effect remains unknown.
