# stateaxis-preemption-recompute

Extension ID: `org.vllm-hust.stateaxis-preemption-recompute`

This experimental, default-off MOD owns StateAxis's bounded token-checkpoint
preemption and generation-safe recompute policy. Under hard state-slot pressure
it may suspend one cold-origin request, invalidate its old generation, serve the
waiting state demand, then reconstruct the complete checkpoint exactly before
resuming.

The Extension Manager is the only supported activation path. It verifies the
exact `RESEARCH_MANIFEST.json` digest and renders the pinned policy through
`--additional-config`; StateAxis rejects stale digests, unsafe variants, and
direct command-line activation.

## Evidence boundary

Status: **matched real-NPU negative; experimental only**.

The frozen issue #57 Qwen2.5-14B BF16 cell completed three fresh-service pairs
per arm with exact tokens and lifecycle. Pressure-request TTFT improved, but the
long request's sojourn regressed **113.375%**, violating the 5% no-harm guard.
This is workload-scoped evidence, not a universal claim that recompute cannot
help. It also does not qualify this revision for performance use.
The complete formal 3+3 bundle is vendored under
`evidence/issue57-preemption-20260815-r2-3plus3/`.

Current ECPA evidence proves activation, identity binding, strict failure,
effect counters, exact deterministic mock-worker output, and clean shutdown. It
does not execute accelerator kernels or supersede the negative real-NPU result.
See `EVIDENCE.md`.

## Install and validate

```bash
python -m pip install -e '.[test]'
ruff check .
ruff format --check .
pytest -q

VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261010/manager-config.json \
  vllm-hust-ext extension check org.vllm-hust.stateaxis-preemption-recompute
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261010/manager-config.json \
  vllm-hust-ext extension plan org.vllm-hust.stateaxis-preemption-recompute
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261010/manager-config.json \
  vllm-hust-ext run --dry-run -- /bin/true
```

Disabling the extension restores ordinary resident-generation scheduling; no
preemption/recompute authority or MOD identity remains.

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.
