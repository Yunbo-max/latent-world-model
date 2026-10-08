# Native scorer environments: Local installation card

**Status: source_inspected / generated_unexecuted; native_qualification = pending_local.** These are proposed Linux x86-64, Python 3.11 CPU environments for `lwm.scoring replay`, plus a separate legacy Python 3.8 candidate for the full author bAbI teacher/export stack. No installation, import, dependency resolution, scorer invocation or scientific test was executed by Web. Direct versions are specified below; Local must retain actual installation reports, full dependency freezes and import/replay receipts before calling an environment qualified.

Use separate `lwm-parlai` and `lwm-lmeval` environments. The pinned [ParlAI requirements](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/requirements.txt) specify `torch==2.0.0`, `numpy~=1.23.0` and `datasets<2.2.2`; the pinned [harness base requirements](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/pyproject.toml) require `datasets>=2.16.0`. These full-package constraints conflict with each other and ParlAI conflicts with the main model's torch 2.5.1 / NumPy 2.1.3 profile. Moreover, ParlAI's [setup.py](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/setup.py) removes `==` suffixes when constructing `install_requires`; a commit-pinned `pip install` does not preserve its exact requirement pins.

The ParlAI card deliberately installs the complete **import dependencies for the selected metrics/message replay**, then imports clean author source directly. It is not a full ParlAI training, teacher-export, documentation or CLI environment. The LAMBADA card installs the **whole harness base package with normal dependency resolution**, without model backend extras. Neither card downloads pretrained weights or native datasets. Dataset preparation is specified separately in `DATA_PROTOCOL_PROPOSAL.md` and `configs/assets.json`.

## Acquire the two immutable source checkouts

Run these commands through Local's existing execution owner, from the actual staged project root. For already existing matching clean checkouts, reuse them and perform the revision checks; do not repeat `remote add`, reset local work or overwrite an unrelated directory.

```bash
set -euo pipefail
LWM_TASK_ROOT="$(pwd -P)"
export GIT_LFS_SKIP_SMUDGE=1
mkdir -p external artifacts/native-env

git init external/ParlAI
git -C external/ParlAI remote add origin https://github.com/facebookresearch/ParlAI.git
git -C external/ParlAI fetch --depth 1 origin a29567f7ce76992fd1f03c51ba9e3b155a37ea51
git -C external/ParlAI checkout --detach FETCH_HEAD
test "$(git -C external/ParlAI rev-parse HEAD)" = a29567f7ce76992fd1f03c51ba9e3b155a37ea51
test -z "$(git -C external/ParlAI status --porcelain --untracked-files=no)"

git init external/lm-evaluation-harness
git -C external/lm-evaluation-harness remote add origin https://github.com/EleutherAI/lm-evaluation-harness.git
git -C external/lm-evaluation-harness fetch --depth 1 origin d6de81643928d653435c431bae19945d41d32520
git -C external/lm-evaluation-harness checkout --detach FETCH_HEAD
test "$(git -C external/lm-evaluation-harness rev-parse HEAD)" = d6de81643928d653435c431bae19945d41d32520
test -z "$(git -C external/lm-evaluation-harness status --porcelain --untracked-files=no)"
```

## bAbI: ParlAI metrics/message only

Source closure: [metrics.py](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/core/metrics.py) imports torch, Message, `utils.misc` and `utils.typing`; [misc.py](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/utils/misc.py) reaches [io.py](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/utils/io.py), strings and logging. I/O requires iopath; coloredlogs is optional but installed here. [iopath v0.1.8 metadata](https://github.com/facebookresearch/iopath/blob/v0.1.8/setup.py) requires tqdm and portalocker on Python 3.11. `TeacherMetrics(metrics_list="accuracy")` also computes its built-in precision/recall/F1; BLEU and ROUGE imports are conditional and are not reached by this replay. No NLTK corpus is needed for this path.

Torch 2.0.0's [base dependency declaration](https://github.com/pytorch/pytorch/blob/v2.0.0/setup.py) names filelock, typing-extensions, sympy, networkx and jinja2. The official [CPU index](https://download.pytorch.org/whl/cpu/torch/) lists `torch-2.0.0+cpu-cp311-cp311-linux_x86_64.whl`; the CPU installation route is documented in [PyTorch's previous versions](https://pytorch.org/get-started/previous-versions/). Remaining versions below are explicit proposed environment pins, not an author-supplied lock or a claim of tested compatibility.

```bash
conda create -n lwm-parlai python=3.11 pip=24.3.1 -y
conda run -n lwm-parlai python -m pip install \
  setuptools==75.6.0 wheel==0.45.1 packaging==24.2
conda run -n lwm-parlai python -m pip install \
  numpy==1.23.5 iopath==0.1.8 portalocker==2.7.0 tqdm==4.62.3 \
  coloredlogs==14.0 humanfriendly==10.0 typing-extensions==4.5.0 \
  filelock==3.13.1 sympy==1.12 mpmath==1.3.0 networkx==3.2.1 \
  jinja2==3.0.3 MarkupSafe==2.1.5 \
  --report artifacts/native-env/parlai-dependencies.install.json
conda run -n lwm-parlai python -m pip install torch==2.0.0+cpu \
  --index-url https://download.pytorch.org/whl/cpu \
  --report artifacts/native-env/parlai-torch.install.json
conda run -n lwm-parlai python -m pip check
conda run -n lwm-parlai python -m pip freeze --all > artifacts/native-env/parlai.freeze.txt
conda list -n lwm-parlai --explicit > artifacts/native-env/parlai.conda-explicit.txt
```

No `pip install ParlAI`, `pip install -r external/ParlAI/requirements.txt` or `--no-deps` installation is part of this scoped card. The replay inserts the verified source checkout into `sys.path`. `pip check` therefore checks installed distributions; it does not certify the omitted full ParlAI application stack. Extending this environment to `parlai.core.teachers` or a model backend requires a separately source-qualified dependency closure and receipt.

**Unqualified acceptance prerequisite:** native bAbI author-teacher export/parity remains mandatory before qualifying bAbI. This metrics environment does not close that prerequisite. The full candidate card immediately below supplies the author package installation and all 60 exports; it remains blocked from qualification until actual resolution, import and complete row-parity receipts exist. Do not treat a successful metrics import/replay as satisfying teacher parity.

## bAbI: full author Teacher/export candidate

Use a third environment, `lwm-parlai-teacher`, solely for the author's exporter. The pinned setup declares Python>=3.8. Choose Python 3.8 because the published [PyYAML 5.4](https://pypi.org/project/PyYAML/5.4/) and [pyzmq 18.1.0](https://pypi.org/project/pyzmq/18.1.0/) files include CPython 3.8 Linux x86-64 wheels; [pandas 1.4.0](https://pypi.org/project/pandas/1.4.0/) supports Python>=3.8, and the official torch CPU index also lists its cp38 wheel. This is a legacy compatibility candidate, not the model runtime. Do not import or install this Python>=3.11 project into it. It uses the complete, unmodified author `requirements.txt` together with the editable author checkout in **one normal pip resolver invocation**, preserving the `==` constraints that setup.py alone would drop.

There is a source-confirmed conflict in the lowest allowed LiteLLM candidate: ParlAI requires `openai<=0.27.7`, while [LiteLLM 0.1.400's exact release source](https://github.com/BerriAI/litellm/blob/a5aa6228e48d5696f7457b42b56c9f86a009e069/pyproject.toml) requires `openai ^0.27.8`, meaning >=0.27.8,<0.28.0. Those two requirements cannot be satisfied together. ParlAI permits **any** `litellm>=0.1.400`; this observation does not prove every later candidate is inconsistent. Therefore the card does not invent a LiteLLM pin or claim a solved full lock: let the normal resolver consider the declared range within Local's bounded installation attempt. A resolution failure keeps full teacher/export **blocked**, with its exact resolver conflict retained. Do not remove LiteLLM/OpenAI from the author requirements, change their bounds, use `--no-deps`, or treat the metrics-only environment as a successful full install.

```bash
conda create -n lwm-parlai-teacher python=3.8 pip=24.3.1 -y
conda run -n lwm-parlai-teacher python -m pip install \
  setuptools==68.2.2 wheel==0.41.3 packaging==23.2
cat > artifacts/native-env/parlai-teacher.constraints.txt <<'EOF'
torch==2.0.0+cpu
torchvision==0.15.1+cpu
numpy==1.23.5
datasets==2.2.1
setuptools==68.2.2
wheel==0.41.3
packaging==23.2
EOF
conda run -n lwm-parlai-teacher python -m pip install \
  --constraint artifacts/native-env/parlai-teacher.constraints.txt \
  torch==2.0.0+cpu torchvision==0.15.1+cpu \
  --extra-index-url https://download.pytorch.org/whl/cpu \
  --report artifacts/native-env/parlai-teacher-torch.install.json
conda run -n lwm-parlai-teacher python -m pip install --no-build-isolation \
  --constraint artifacts/native-env/parlai-teacher.constraints.txt \
  --requirement external/ParlAI/requirements.txt \
  --editable external/ParlAI \
  --report artifacts/native-env/parlai-teacher.install.json
conda run -n lwm-parlai-teacher python -m pip check
conda run -n lwm-parlai-teacher python -m pip freeze --all > artifacts/native-env/parlai-teacher.freeze.txt
conda list -n lwm-parlai-teacher --explicit > artifacts/native-env/parlai-teacher.conda-explicit.txt
```

The CPU local-version pins satisfy the author's corresponding public-version `==` pins and prevent replacement by CUDA torch/torchvision builds. The other explicit choices stay inside the author NumPy/datasets bounds. All remaining loose direct/transitive requirements are those of the immutable author source; the actual freeze and pip reports, not this candidate, record their resolution. The bootstrap versions here support the older interpreter; do not reuse the Python 3.11 bootstrap pins. Run the block under the preceding `set -euo pipefail` and the existing bounded execution owner. Continue only after installation and `pip check` succeed, preserving stderr and exit status on any failure.

Then verify the actual teacher and exporter imports from that same clean checkout. This reaches the native [teacher module](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/core/teachers.py), [Task10kTeacher](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/tasks/babi/agents.py) and [author conversion script](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/scripts/convert_data_to_parlai_format.py), without constructing a model or downloading a dataset:

```bash
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/external/ParlAI" \
  conda run -n lwm-parlai-teacher python -c '
import hashlib, inspect, json, pathlib, subprocess, sys
root = pathlib.Path("external/ParlAI").resolve()
assert subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip() == "a29567f7ce76992fd1f03c51ba9e3b155a37ea51"
assert not subprocess.check_output(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], text=True).strip()
from parlai.core.teachers import FbDeprecatedDialogTeacher
from parlai.tasks.babi.agents import Task10kTeacher
from parlai.scripts.convert_data_to_parlai_format import dump_data
paths = {x.__name__: pathlib.Path(inspect.getfile(x)).resolve() for x in (FbDeprecatedDialogTeacher, Task10kTeacher, dump_data)}
assert all(root in p.parents for p in paths.values())
print(json.dumps({"python": sys.version, "imports": {k: {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for k, p in paths.items()}}, indent=2))
' > artifacts/native-env/parlai-teacher.imports.json
```

The following is the exact per-task/per-split export protocol from `DATA_PROTOCOL_PROPOSAL.md`, now bound to this interpreter. **Prerequisite:** the existing archive has already passed its SHA256 check and safe-extraction/member checks from that protocol; all expected native files are present. Check the existing bytes again below, then use the author's [build marker](https://github.com/facebookresearch/ParlAI/blob/a29567f7ce76992fd1f03c51ba9e3b155a37ea51/parlai/tasks/babi/build.py) so the builder uses those verified local assets. Do not mark missing/unverified data as built. No archive download is part of this card.

```bash
printf '%s  %s\n' \
  f7f0bee187efca0d81c3daac1b162cda4eb7f9505dee5ad6846eabbed3dbf92e \
  assets/parlai/bAbI/babi.tar.gz | sha256sum --check -
test -d assets/parlai/bAbI/tasks_1-20_v1-2/en-valid-10k-nosf
mkdir -p assets/babi/native
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/external/ParlAI" \
  conda run -n lwm-parlai-teacher python -c \
  'from parlai.core import build_data; build_data.mark_done("assets/parlai/bAbI", version_string="None")'
for task in $(seq 1 20); do
  for split in train valid test; do
    dtype="$split"
    if [ "$split" = train ]; then dtype='train:ordered'; fi
    test ! -e "assets/babi/native/task-$task-$split.txt"
    env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/external/ParlAI" \
      conda run -n lwm-parlai-teacher \
      python -m parlai.scripts.convert_data_to_parlai_format \
      --task "babi:Task10k:$task" --datatype "$dtype" \
      --datapath assets/parlai --num-examples -1 --ignore-fields '' \
      --outfile "assets/babi/native/task-$task-$split.txt"
  done
done
```

Reuse already completed, verified export files instead of overwriting them; the loop intentionally stops if a target exists. The author CLI's successful exit and 60 files alone do not establish parity. This full installation/export card is **unexecuted; resolution and teacher parity remain pending**, with the documented LiteLLM/OpenAI lower-bound conflict still unresolved.

### Compare all 60 author exports with prepared records

After the real full-teacher exports exist, run the complete comparison in the separate Python 3.11 `lwm-parlai` environment above. Its selected metrics/message dependencies include the native `str_to_msg` parser; it is sufficient to **read** the exports, and does not replace the full teacher environment that must **produce** them. Do not run the Python 3.11 project module in `lwm-parlai-teacher` (Python 3.8).

```bash
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" \
  conda run -n lwm-parlai python -m lwm.native_parity \
  --data data/babi --exports assets/babi/native \
  --native-source external/ParlAI \
  --output artifacts/babi-teacher-parity
```

The command requires exactly 20 tasks × three splits, verifies prepared source identities and full native denominators, then compares all **220,000 questions / 68,928 episodes** in export order. It uses the pinned author's `str_to_msg` for escaped text and labels; compares exact text, labels, reward (including the omitted zero default), episode end/index/turn; validates the author's blank episode separators; and rechecks all input hashes and export inventory before publishing. Explicit `episode_done:False` is rejected because the author exporter omits False and the native parser's `bool(value)` would otherwise treat that string as True.

Success creates `babi-teacher-parity.json` with exact input/source hashes and all 60 per-task counts. On an error it raises nonzero and preserves `failure.json` with the error and completed-task inventory; it never writes a success receipt for a partial comparison. Use a fresh output directory on retry and retain failed receipts. The command does not run a model or scorer and does not qualify the separate exporter installation; retain its real install/import/export logs alongside the comparison receipt.

`tests/test_native_parity_semantics.py` adds ordinary software contracts for mismatch, missing/extra rows, episode boundaries, malformed flags, invalid rewards, input changes and failure preservation. The full-native integration test requires `LWM_NATIVE_BABI_DATA`, `LWM_NATIVE_BABI_EXPORTS`, and `LWM_NATIVE_BABI_SOURCE` and otherwise skips. Skips do not qualify native data. All these commands/tests remain **generated_unexecuted** until Local supplies actual receipts.

## LAMBADA: harness base package

The pinned harness [package initializer](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/__init__.py) queries installed `lm_eval` distribution metadata and lazily loads its evaluator, so install the package rather than relying only on `PYTHONPATH`. Its [task module](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/api/task.py), [utils](https://github.com/EleutherAI/lm-evaluation-harness/blob/d6de81643928d653435c431bae19945d41d32520/lm_eval/utils.py), registry, filters and metrics are sufficient for the existing `ConfigurableTask` replay. The base dependency list contains no torch/transformers/accelerate/peft requirement; those belong to the optional `hf` backend.

The selected `datasets==3.1.0` [metadata](https://github.com/huggingface/datasets/blob/3.1.0/setup.py) requires pyarrow>=15, dill<0.3.9, multiprocess<0.70.17, fsspec<=2024.9.0 and requests>=2.32.2. The following pins respect those declared bounds and the [evaluate v0.4.3 metadata](https://github.com/huggingface/evaluate/blob/v0.4.3/setup.py). They pin every harness direct dependency plus the main compatibility-sensitive transitive packages; remaining indirect distributions are resolved by pip and become frozen only in Local's actual receipt. Do not describe this candidate constraints file as a solved full lock.

```bash
conda create -n lwm-lmeval python=3.11 pip=24.3.1 -y
conda run -n lwm-lmeval python -m pip install \
  setuptools==75.6.0 wheel==0.45.1 packaging==24.2
cat > artifacts/native-env/lmeval.constraints.txt <<'EOF'
datasets==3.1.0
numpy==2.1.3
evaluate==0.4.3
jinja2==3.1.4
pytablewriter==1.2.0
rouge-score==0.1.2
sacrebleu==2.4.3
scikit-learn==1.5.2
sqlitedict==2.1.0
dill==0.3.8
word2number==1.1
more-itertools==10.5.0
typing-extensions==4.12.2
tqdm==4.67.1
pyarrow==18.1.0
huggingface-hub==0.34.4
pandas==2.2.3
fsspec==2024.9.0
multiprocess==0.70.16
requests==2.32.3
PyYAML==6.0.2
scipy==1.14.1
nltk==3.9.1
joblib==1.4.2
threadpoolctl==3.5.0
packaging==24.2
setuptools==75.6.0
wheel==0.45.1
EOF
conda run -n lwm-lmeval python -m pip install --no-build-isolation \
  --constraint artifacts/native-env/lmeval.constraints.txt \
  --editable external/lm-evaluation-harness \
  --report artifacts/native-env/lmeval.install.json
conda run -n lwm-lmeval python -m pip check
conda run -n lwm-lmeval python -m pip freeze --all > artifacts/native-env/lmeval.freeze.txt
conda list -n lwm-lmeval --explicit > artifacts/native-env/lmeval.conda-explicit.txt
```

`--no-build-isolation` uses the explicitly installed setuptools/wheel; it does not disable runtime dependency installation. Preserve dependency conflicts instead of silently lifting pins. A change to this candidate requires a recorded reason, replacement constraints/freeze and requalification. No Hugging Face login, model backend extra, online evaluation metric download or LLM judge is required for the selected accuracy/perplexity replay.

## Full native LAMBADA tokenizer-boundary acceptance

The source-inspected `TemplateLM._encode_pair` in the pinned harness does not load a model or require an HF model backend. For the authored full-row parity test, extend only the CPU harness environment with the project's tokenizer versions and pytest; do not install the project distribution or model weights:

```bash
conda run -n lwm-lmeval python -m pip install \
  --constraint artifacts/native-env/lmeval.constraints.txt \
  transformers==4.46.3 tokenizers==0.20.3 huggingface-hub==0.34.4 pytest==8.3.4 \
  --report artifacts/native-env/lmeval-tokenizer.install.json
conda run -n lwm-lmeval python -m pip check
conda run -n lwm-lmeval python -m pip freeze --all > artifacts/native-env/lmeval.freeze.txt
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" \
  LWM_NATIVE_LAMBADA_DATA="$PWD/data/lambada" \
  LWM_NATIVE_LAMBADA_SOURCE="$PWD/external/lm-evaluation-harness" \
  LWM_NATIVE_LAMBADA_TOKENIZER="$PWD/data/tokenizer" \
  conda run -n lwm-lmeval python -m pytest tests/test_scoring_semantics.py \
  -k 'split_on_real_full_native_source or pairs_match_the_pinned_harness_token_boundary'
```

This checks the actual 5153 passages and verified tokenizer bytes against the pinned author's pair helper. Retain the real test receipt and any skip; absence of required assets is not a pass. It establishes token-boundary parity only, not correct model likelihoods or native aggregation. This command remains unexecuted here.

## Check imported locations, then replay the complete native records

Do not install this project with its model dependencies into either scorer environment. Its `lwm/__init__.py` and pre-replay `lwm.scoring` imports are stdlib-only; expose `src` explicitly in every invocation. Each command below runs on Local only and requests **zero GPUs** through the existing execution owner. `CUDA_VISIBLE_DEVICES` is empty as an additional CPU-only setting.

```bash
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" conda run -n lwm-parlai python -c '
import inspect, json, pathlib, sys
from lwm.scoring import verify_native_source
root = pathlib.Path("external/ParlAI").resolve()
identity = verify_native_source(root, "babi")
sys.path.insert(0, str(root))
from parlai.core.metrics import TeacherMetrics, ExactMatchMetric
from parlai.core.message import Message
locations = {x.__name__: str(pathlib.Path(inspect.getfile(x)).resolve()) for x in (TeacherMetrics, ExactMatchMetric, Message)}
assert all(pathlib.Path(p).is_relative_to(root) for p in locations.values())
print(json.dumps({"python": sys.version, "source": identity, "imports": locations}, indent=2))
' > artifacts/native-env/parlai.imports.json

env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" conda run -n lwm-lmeval python -c '
import inspect, json, pathlib, sys, importlib.metadata
from lwm.scoring import verify_native_source
root = pathlib.Path("external/lm-evaluation-harness").resolve()
identity = verify_native_source(root, "lambada")
sys.path.insert(0, str(root))
from lm_eval.api.task import ConfigurableTask
from lm_eval import utils
locations = {"ConfigurableTask": str(pathlib.Path(inspect.getfile(ConfigurableTask)).resolve()), "utils": str(pathlib.Path(utils.__file__).resolve())}
assert all(pathlib.Path(p).is_relative_to(root) for p in locations.values())
print(json.dumps({"python": sys.version, "lm_eval": importlib.metadata.version("lm_eval"), "source": identity, "imports": locations}, indent=2))
' > artifacts/native-env/lmeval.imports.json

env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" conda run -n lwm-parlai \
  python -m lwm.scoring replay --task babi --data data/babi \
  --predictions results/memory-loop4-babi/predictions.jsonl \
  --native-source external/ParlAI --output results/memory-loop4-babi-native
env CUDA_VISIBLE_DEVICES="" PYTHONPATH="$PWD/src" conda run -n lwm-lmeval \
  python -m lwm.scoring replay --task lambada --data data/lambada \
  --predictions results/memory-loop4-100m-lambada/predictions.jsonl \
  --native-source external/lm-evaluation-harness --output results/memory-loop4-lambada-native
```

Substitute actual completed prediction directories from the admitted command manifest and a new result directory for each replay. These commands verify clean pinned checkout identity, loaded module locations, native data contents/order, complete denominators and author per-example/aggregate scoring. They do **not** establish tokenizer/model-forward parity, native bAbI teacher-export parity or successful training. Preserve native exit status and stdout/stderr even on failure; empty/partial receipts and import-only success never qualify a benchmark. The `model_adapter_parity` field remains `pending_local` after aggregation replay by design.

Local's reproducible receipt consists of the execution commit/dirty diff, exact interpreter/Conda explicit records, installed freezes, pip JSON reports (download URLs and available archive hashes), source revisions/file hashes, import locations, complete predictions and actual `native-replay.json`. Retain resolved packages in the existing package cache or a bounded wheelhouse if offline reproduction is required; `pip freeze` alone does not archive package bytes. Installation/import/native replay remain **unexecuted and unqualified** until those real receipts exist.
