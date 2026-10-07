"""Read-only source capture before the existing host harness stages an attempt."""
import argparse
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "src"))
from latent_world_model.io import git_identity, write_json

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()
identity = git_identity(root, allow_staged=False)
if identity["status"]:
    raise SystemExit("Commit source first; source capture requires a clean checkout")
output = Path(args.output)
if output.exists():
    raise SystemExit("Preserve prior source capture; choose a new output")
write_json(output, identity)
print(output.resolve())
