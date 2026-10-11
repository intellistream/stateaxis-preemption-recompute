import hashlib
import json
from pathlib import Path

import pytest
from vllm_hust_ext.manifest import activation_blocker, load_manifest

import stateaxis_preemption_recompute


def test_policy_is_discoverable_and_experimentally_activatable() -> None:
    manifest = load_manifest(
        Path(stateaxis_preemption_recompute.__file__).with_name(
            "vllm-hust-extension-v0.3.json"
        )
    )
    assert manifest.bundle_id == "org.vllm-hust.stateaxis-preemption-recompute"
    assert manifest.bundle_version == "0.2.0"
    assert manifest.schema_version == "0.3-experimental"
    assert activation_blocker(manifest) is None
    additional = dict(manifest.activation.additional_config)
    research_manifest = Path(stateaxis_preemption_recompute.__file__).parents[2] / (
        "RESEARCH_MANIFEST.json"
    )
    assert (
        additional["stateaxis_mod"]["manifest_sha256"]
        == hashlib.sha256(research_manifest.read_bytes()).hexdigest()
    )
    assert additional["stateaxis_mod"]["performance_qualified"] is False
    assert additional["stateaxis_preemption_recompute"] == {
        "enabled": True,
        "max_preemptions_per_request": 1,
        "state_slot_pressure_only": True,
        "cold_origin_only": True,
        "complete_token_checkpoint": True,
        "generation_invalidation_required": True,
        "exact_recompute_token_required": True,
        "suspend_until_state_demand_drains": True,
        "fail_closed": True,
    }


def test_research_manifest_matches_package_contract() -> None:
    research_manifest = Path(stateaxis_preemption_recompute.__file__).parents[2] / (
        "RESEARCH_MANIFEST.json"
    )
    payload = json.loads(research_manifest.read_text())
    assert payload["mod_id"] == stateaxis_preemption_recompute.MOD_ID
    assert payload["version"] == "0.2.0"
    assert payload["mechanism"]["max_preemptions_per_request"] == 1
    assert payload["qualification"]["performance_qualified"] is False
    assert payload["qualification"]["evidence_label"] == "matched-real-npu-negative"
    provenance = json.loads((research_manifest.parent / "PROVENANCE.json").read_text())
    assert (
        provenance["implementation_boundary"]["research_manifest_sha256"]
        == hashlib.sha256(research_manifest.read_bytes()).hexdigest()
    )


def test_python_contract_fails_closed() -> None:
    assert (
        stateaxis_preemption_recompute.preemption_recompute().max_preemptions_per_request
        == 1
    )
    with pytest.raises(ValueError, match="one bounded"):
        stateaxis_preemption_recompute.PreemptionRecomputeConfig(
            max_preemptions_per_request=2
        )
