# Observed predictive target: primary/interface/native source audit

Date: 2026-10-09. Subject: ../STEP2_OBSERVED_PREDICTIVE_TARGET.md. Source/meaning inspection only; no code, tests, autodiff, solve, scoring, dataset/model download or experiments executed. Root is the only integration writer. Independent source reader: `/root/predictive_sources_review`; independent mathematics reader: `/root/predictive_target_review`. Read scope below is finite, not a complete literature/IPCG audit or reproduction.

## Closest primary objects actually inspected

**TTT:** [2407.04620v1](https://arxiv.org/html/2407.04620v1), §§2.1–2.4, particularly learned key/value/query views Eq4–5 and outer next-token objective. Root reread §§2.2–2.3; independent source worker read the broader listed scope. [PMLR final metadata](https://proceedings.mlr.press/v267/sun25h.html) checked separately; final paper not fully reread. Learned inner reconstruction optimized through outer future token prediction already exists. This does not prove every constrained future-risk construction equivalent, but future CE alone is no new supervisory mechanism.

Official code read by source worker, pinned commits:

| Repository/commit | File / Git blob | Actual functions and finding |
|---|---|---|
| test-time-training/ttt-lm-pytorch @ cd831db10c8c9a0f6340f02da5613316a8a92b67 | README.md / 43a3580ab0cd5f40a589e3c91bdf1c891abef12a; ttt.py / da267f4a88196fd4709fa1e5e62235a3fa746ec6 | TTTLinear.ttt, TTTMLP.ttt, TTTForCausalLM.forward; currently observed hidden projections supply inner XV−XK; labels only enter shifted CE after forward. README calls it naive implementation and recommends JAX for training. Root additionally fetched/read these ttt.py portions at the same blob. |
| test-time-training/ttt-lm-jax @ 6f529b124c7fb5879b33c06926408b15add1d82f | ttt/train.py / ef415b6ec7c0ac517e048d5872f51af58703d882 | make_train_step_fn lines68–98: input_tokens go to model; target_tokens/loss_masks to CE; value_and_grad on outer parameters. |
| same JAX pin | ttt/models/ttt_layer.py / 7831e6cef773d62f46b2bf5c08058094141ecd7b | get_qkv_projections; ttt scan290–325; TTTLinear.process_mini_batch368–428. Inner hidden state and causal query outputs retained in differentiable outer graph. |

These code observations do not qualify hardware speed, long-horizon efficacy or2080Ti fit.

**GGN/Fisher:** [Martens, JMLR21(2020),17-678](https://jmlr.org/papers/volume21/17-678/17-678.pdf), §§8–11 formula-bearing portions; root and independent source worker read. Loss curvature pulled through a Jacobian omits network second derivatives. Softmax logits as categorical natural parameters yield model Fisher/GGN equivalence; empirical observed-label gradient outer products generally differ. Matrix-vector products need actual forward/reverse computation. State/edit coordinates in our note are a local pullback application, not a new foundational theorem. No dedicated author implementation audited or global descent/stability certificate inferred.

**APO:** [Bae,Vicol,HaoChen,Grosse,NeurIPS2022](https://papers.neurips.cc/paper_files/paper/2022/file/3af25aa3de8b7b02ddbd1b6be5031be8-Paper-Conference.pdf), §3.1Eq3,§3.2Eq4,§4.1Eq8/Algorithm1,§4.3Theorem1,§4.4Eq9–10,§4.5. Root reread central proximal/inverse and theorem sections; source worker read the full listed scope. Function-space proximity, parameter distance and learned update/preconditioner already exist. Theorem1 uses linearized loss/quadratic proximity and nonsingular gradient second moment. It does not certify arbitrary nonlinear future-state edits. Official author code was not located by bounded paper/author-page/title-GitHub search; **no code pin or full implementation audit claimed**. Missing code does not erase foundational prior work.

**DeltaTTT:** [2610.08553v1](https://arxiv.org/html/2610.08553v1), Background,§4Eq7–12/pre-post,§5.3 read by source worker; existing same-packet original reentry also records reading. Current-value reconstruction and nonlinear two-matrix readout are not absent in neighboring work. Default is pre variant. Actual authors are Yining Li,Dongchen Han,Jie Fu,Gao Huang; retain correction to old audit metadata without re-certifying its old bytes. Official implementation not located from this bounded reading/search.

**Decision sufficiency:** the note's information-refinement identity is an application of conditional quadratic Bayes risk with a random risk matrix. Its specialized decision-focused/representation nearest-work audit is **pending**. Neither reviewer certifies novelty; the note expressly does not equate optimal-action sufficiency with full future-distribution sufficiency.

## Actual latent repository interface

All below were fetched at `Yunbo-max/latent-world-model@12bf91d20444ec86c1ae9c15f3ed47aa5c690859` and read statically. Authoritative AGENTS at that revision has Git blob3aad48d2d1d10f4f74e7e0d3b27ef1f067dcdeae. Any stale scratch AGENTS is not the source of this review.

| File / Git blob | Inspected entry and implication |
|---|---|
| rounds/full-plan-2026-10-08/EXPANSION_SPEC.md / 92cd6ff7ce798317b2e4da8638a7665035447fbc | Full spec: causal event selection, per-token text plan, fixed forcing, legal first-next-segment-token target. No identified semantic codec. |
| src/lwm/model.py / 2a10f22f9243febc09a688cad63a5f17c65a9c1c | MemoryWriter.forward,_workspace,_read,_write,realize_plan,plan_prefix,predict_future,forward_segment,commit_segment. Writer gated bounded slots, not Delta; old M/completed prelude evidence enter writer. Episodic reader enters workspace, not writer. Z-only realization is a text bottleneck. |
| src/lwm/train.py / 3f4e46bb0252ca1a2b548c65275aa53fa4512a7b | window_objective60–105; caller362–390. Main CE already trains earlier writer through later segments inside window; detach at TBPTT boundary. Last window write has no downstream main loss within that window. Auxiliary only first next segment token if mask[0]/same history eligible. |
| src/lwm/realization.py / a1add8ae23dbdded464607db39df04185909cf55 | Full file: persisted plan/context/checkpoint identity; CLI consumes saved plan without reader/writer callback. Not new evidence or unique sentence/action meaning. |

A derivative or state-action solve in the note is not implemented in these sources. No source edits, engineering completion reopen, software pass or Local result asserted.

## Native fit, label boundaries and a prior-table correction

Source worker actually read the following official bytes; none executed or downloaded native data.

| Native source pin | Actual file / Git blob | Fit/limitation |
|---|---|---|
| ParlAI @ a29567f7ce76992fd1f03c51ba9e3b155a37ea51 | parlai/tasks/babi/agents.py / 7e0d4c5d63f5bc1dd7be89df3176baf62dd63b3a | Task10k/All10k; tasks8/19 comma-to-space labels; official text/answer endpoint. Preserve20tasks/20000. |
| same ParlAI pin | parlai/core/metrics.py / 16970e6aca78a7b2673b69aea5ff555ec285da8d | ExactMatchMetric.compute578–588, normalize_answer853–875: normalized max across supplied answers. Do not substitute latent-risk proxy for native scorer. |
| lm-evaluation-harness @ d6de81643928d653435c431bae19945d41d32520 | lm_eval/tasks/lambada/lambada_openai.yaml / e159a6c7a0f6c2cfbc50b14b7d5b6301fd591a62 | EleutherAI/lambada_openai,test,loglikelihood; literal-space prefix, leading-space final word; acc/perplexity. Preserve5153. |

**Correction, without silently rewriting history:** sources/MEASUREMENT_FEASIBILITY_2026-10-09.md at baseline blob e5716b561c0779fd040b827cec3051d21b057d14 describes lambada_standard. Actual project supports **lambada_openai**: src/lwm/scoring.py blob f0d762d4181e7d0207ad52f0483b968d140661aa has lambada_context_target101–106,loader285–288,replay496; src/lwm/prepare.py blob236049607387c8cb93f216761fe786445e0f80ef prepare_lambada669–699 and manifest use that variant. Source worker read those actual portions. Do not mix variants or label an uninspected standard conversion as qualified. No old code/evaluator assets changed here.

Permitted real train/dev text and task answers can supply loss-only predictive supervision. Test answers remain evaluation-only. Neither native task provides unique hidden value targets, latent revision-validity r, ideal state u or full Jacobian truth. Behavioral endpoints alone do not determine the claimed internal source of improvement. Strong alternatives: existing ordinary far-horizon CE/TTT; same-information direct conditional predictor; attributed GGN/proximal methods with honest total teacher/solver cost. Natural prevalence, decisive affordable comparison and specialized target/representation originality remain unclosed. This is feasibility reasoning, not a new executable experiment matrix.

## Installed skill provenance and binding scope

Current installed plugin read through `c23/research-autopilot`, root `skill://plugins_6ac8ad1eb9648191a0b6c1941de5d6b2/research-autopilot`. Entry+required modules were loaded from this same package in this invocation. Actual entry/module bytes contain autonomous-rsi branch language. Its own module says it applies to an explicitly requested branch and supplies no main/shared-skill/Web-execution authority. Owner's current instruction explicitly excludes importing that other-project runtime choice. Thus this project's binding remains same task, math-only web_supervisor, literal main, no project execution or new automation; installed prompt wording is not a service/version receipt for the project. No plugin reinstall, branch change or runtime deployment performed.

Exact UTF-8 module byte SHA256 values observed this invocation:

| Module | SHA256 |
|---|---|
| SKILL.md | 94c45c0228aee9bca712589af813ffdb6f292631cd8d132650537b453cfce63d |
| workflow-harness | 5e6d85e34ed32150992ad65d4f72879cd9e9eebd7282924302f028c4f78a4c86 |
| web-background-work | ca1c55a50a67f68adbbf8ae4a117e1bdcabedcde83ea3e88ec8bbe60ff9c613f |
| math-analysis | e27e60718518b34d4995a4f2109588aa93746665c4466ab7ac31c049334ccbc8 |
| math-operation-graph | e82711e4c307d6d901486f4da569e4572e5ce7a4fe006976789bc5d174b749a2 |
| math-derivation-paths | 787bc32d0a7620cb22a8193b3acd2828c304a4a658d0b3f3cc995e5acd0533d3 |
| method-verification | 6299c7238a70ef61e57cccaa1cfca7695e041cafa9f7e7f517c014ca54f87203 |
| research-quality-bar | cb4e4522337f6815f3c53f5e0c193783ada6a492e652c6531e90b30cb580c409 |
| literature-evidence | a3612904bc54490c6d254fe620a5057aa119a281c74bffc9bb4069cb30e619df |
| repository-round-trips | 5e2d9bc5d7757847dcf7ae4a41ffc8f1610e59333a444d22aa0f4f78a3e4b0b1 |
| autonomous-rsi (scope reconciliation only) | 532fb601760ca523fb3c54a9c2eaf2328fd9167076f270b4ddc5f03a16eb3827 |

These hashes bind read text, not a deployable runtime or scientific verification. Endpoint/ranking state remains5historical/0active/0admitted/0selected,20/15 deficit; mathematical Step2 investigation continues.
