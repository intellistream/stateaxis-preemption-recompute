# Evidence index

## Current activation contract

- `evidence/ecpa-contract-20261010/README.md`
- `evidence/ecpa-contract-20261010/RESULT.json`
- label: `manager-contract-mock-worker-non-performance`
- disposition: activation/correctness accepted; performance unqualified

## Frozen real-NPU result

- `evidence/ISSUE57_PREEMPTION_RECOMPUTE_CLOSURE_20260815.md`
- label: `matched-real-npu-negative`
- workload: Qwen2.5-14B BF16, one 32-token long request plus four pressure
  requests, capacity 17 states / 320 blocks, scheduler B1
- result: all six arms exact; pressure TTFT improved, but long sojourn regressed
  113.375%, so the candidate failed the 5% no-harm guard
- complete bundle: `evidence/issue57-preemption-20260815-r2-3plus3/`, with all
  six arms, raw requests, effect/lifecycle/NPU records, cleanup status, and a
  repo-local SHA-256 manifest

The current mock-worker record is not a performance rerun. Neither record may
be generalized beyond its declared model, workload, runtime, and mechanism.
