"""Local-only acceptance on actual acquired model and corpus bytes."""
import os
from pathlib import Path
import pytest


@pytest.mark.native
def test_checkpoint_resume_matches_uninterrupted_native_training(tmp_path):
    # This invokes the existing native trainer on the same released corpus blocks.
    # It verifies resume mechanics only, never a method quality claim.
    corpus = os.environ.get("LWM_NATIVE_CORPUS")
    assets = os.environ.get("LWM_ASSETS")
    if not corpus or not assets:
        pytest.fail("Set LWM_NATIVE_CORPUS and LWM_ASSETS; no invented native data fallback")
    from latent_world_model.acceptance import verify_resume
    result = verify_resume(Path(corpus), Path(assets), tmp_path)
    assert result["same_data_position"]
    assert result["same_optimizer_steps"]
    assert result["same_trained_tokens"]
    assert result["same_optimizer"]
    assert result["same_scaler"]
    assert result["same_rng"]
    assert result["max_parameter_difference"] <= 1e-6
