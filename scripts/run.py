"""Run the staged checkout's source rather than an editable install elsewhere."""
from pathlib import Path
import runpy
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))
if len(sys.argv) < 2:
    raise SystemExit("usage: python scripts/run.py latent_world_model.MODULE [arguments]")
module = sys.argv.pop(1)
allowed = {"assets", "prepare", "training", "evaluation", "coconut", "collect"}
if module not in {"latent_world_model." + name for name in allowed} | {"pytest"}:
    raise SystemExit("Unsupported entry point")
runpy.run_module(module, run_name="__main__", alter_sys=True)
