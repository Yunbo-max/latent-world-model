"""Actual installed bytes and resolved software identities, collected on Local."""
import importlib.metadata as metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
from .io import canonical_hash, sha256_file


def distribution_identity(name, module):
    distribution = metadata.distribution(name)
    if not distribution.files:
        raise ValueError(f"No installed file inventory for {name}")
    files = {}
    resolved = set()
    for relative in distribution.files:
        path = Path(distribution.locate_file(relative)).resolve()
        if path.is_file() and path.suffix in {".py", ".so", ".pyd", ".yaml", ".yml", ".json"}:
            files[str(relative)] = sha256_file(path)
            resolved.add(path)
    spec = importlib.util.find_spec(module)
    if spec is None or spec.origin is None or Path(spec.origin).resolve() not in resolved:
        raise ValueError(f"Imported {module} is not the verified installed distribution")
    direct = distribution.read_text("direct_url.json")
    return {"version": distribution.version, "files_sha256": canonical_hash(files),
            "files": files, "direct_url": json.loads(direct) if direct else None}


def environment_identity(evaluator_spec=None):
    critical = {"torch": "torch", "numpy": "numpy", "transformers": "transformers",
                "tokenizers": "tokenizers", "accelerate": "accelerate",
                "safetensors": "safetensors", "huggingface-hub": "huggingface_hub"}
    if evaluator_spec:
        critical.update({"lm-eval": "lm_eval", "datasets": "datasets", "pyarrow": "pyarrow"})
    packages = {name: distribution_identity(name, module) for name, module in critical.items()}
    if evaluator_spec:
        direct = packages["lm-eval"]["direct_url"] or {}
        if direct.get("vcs_info", {}).get("commit_id") != evaluator_spec["revision"]:
            raise ValueError("Installed lm-eval is not the pinned VCS commit; reinstall requirements")
    import torch
    return {"python": platform.python_version(), "platform": platform.platform(),
            "packages": packages,
            "resolved_versions": sorted((d.metadata["Name"], d.version) for d in metadata.distributions()),
            "torch_cuda": torch.version.cuda, "cudnn": torch.backends.cudnn.version(),
            "device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "cublas_workspace_config": os.environ.get("CUBLAS_WORKSPACE_CONFIG"),
            "deterministic_algorithms": torch.are_deterministic_algorithms_enabled()}
