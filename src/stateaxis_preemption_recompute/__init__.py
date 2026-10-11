"""Contract constants for bounded StateAxis preemption and recompute."""

from dataclasses import dataclass

MOD_ID = "org.vllm-hust.stateaxis-preemption-recompute"


@dataclass(frozen=True, slots=True)
class PreemptionRecomputeConfig:
    """Manifest-owned configuration consumed by the StateAxis host."""

    enabled: bool = True
    max_preemptions_per_request: int = 1
    state_slot_pressure_only: bool = True
    cold_origin_only: bool = True
    complete_token_checkpoint: bool = True
    generation_invalidation_required: bool = True
    exact_recompute_token_required: bool = True
    suspend_until_state_demand_drains: bool = True
    fail_closed: bool = True

    def __post_init__(self) -> None:
        if (
            not self.enabled
            or self.max_preemptions_per_request != 1
            or not self.state_slot_pressure_only
            or not self.cold_origin_only
            or not self.complete_token_checkpoint
            or not self.generation_invalidation_required
            or not self.exact_recompute_token_required
            or not self.suspend_until_state_demand_drains
            or not self.fail_closed
        ):
            raise ValueError(
                "preemption-recompute 0.2.0 admits only one bounded, "
                "pressure-only, cold-origin, generation-invalidating, "
                "exact-replay, fail-closed preemption"
            )


def preemption_recompute() -> PreemptionRecomputeConfig:
    """Return the default-off candidate's admitted ON configuration."""

    return PreemptionRecomputeConfig()


__all__ = ["MOD_ID", "PreemptionRecomputeConfig", "preemption_recompute"]
