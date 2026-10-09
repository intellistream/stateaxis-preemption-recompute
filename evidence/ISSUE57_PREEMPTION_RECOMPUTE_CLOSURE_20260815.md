# Issue #57 generation-safe preemption/recompute closure

> **Point-in-time report — not current repository status or a task
> assignment.** Current classification and defaults live in
> [`NATIVE_ENGINE_STATUS.md`](../../NATIVE_ENGINE_STATUS.md).

Issue #57 adds a narrow, default-off production preemption authority for a
complete-token-lineage, cold-origin decode request. At a worker batch boundary
and under hard state-slot pressure, the runtime may release the request's write
lease, invalidate its resident generation, checkpoint the original prompt plus
already consumed output tokens, and suspend the request outside the scheduler.
It resumes only after queued state-demand work drains and must reproduce the
frozen next token exactly. Stateful-origin, session, program, APC, host-tier,
forced-input and chunked-prefill combinations fail closed.

The implementation binds `preemption_recompute_enabled` and the positive
per-request limit into workflow identity. It reports pressure opportunities,
applied decisions, fallbacks, resumes, invalidated generations, recomputed
tokens and bounded recent decisions. The default remains off.

## Correctness repairs found before and during the real gate

Two offline regressions exposed lifecycle bugs. Immediate re-enqueue let the
older arrival reclaim the only free state slot before the pressure request;
the repair keeps recompute work suspended outside the scheduler until queued
state demand drains. Cancellation originally searched only the scheduler and
could miss such a suspended request; cancellation now removes the suspended
checkpoint atomically. Stale generation, cancellation, double-resume,
per-request bound and recompute-token-mismatch tests all pass without weakening
generation, lease or digest checks.

The first real R1 run found a frozen-fixture capacity error. Each 2,177-token
state needs 18 KV blocks, so 16 retained seeds already need 288 blocks and 17
simultaneous states need 306. The 256-block plan stopped at
`submitted=15/completed=14/backend_inflight=0`. The run was boundedly stopped,
marked incomplete with no performance claim, and retained append-only. R2
provisions 320 blocks (306 required plus 14 spare) and raises dynamic HBM
admission to the audited 54,335,087,888-byte plan requirement.

## Frozen experiment

- version: `issue57-preemption-20260815-r2`
- identity: `c66186228d6da10982eb5b4af604bf9da63fdc30b8d95d0effd153c2f3f9a7b3`
- native Rust bundle: `2a0f19c0187a4eaecee8c92a2304e0d93f5f82eaab026a68d20e63f01a0c8f88`
- official local image: `quay.io/ascend/vllm-ascend:v0.23.0rc1-openeuler`, ID
  `sha256:f4c89c293e076453e9eef9edb5fb9669740dccbd3c48619a9f976d775fc29b81`
- workload: Qwen2.5-14B BF16, one 2,177-token prompt/oracle, 16 retained
  seed states, one 32-output-token long request and four concurrent
  one-output-token pressure requests
- capacity: 17 states, 320 physical KV blocks, scheduler batch one
- control: preemption off; candidate: one bounded recompute preemption
- order: control/candidate, candidate/control, control/candidate; fresh server
  and worker per arm
- timing: after all seed states, through completion of long plus pressure work

R2 binds the previously independently full-byte-verified canonical-mount digest
cache, SHA-256
`3cfa499de77b60f739645074f4d6650cedfea80093416a6413f93ec2e9b8725a`.
Stat identity changes still force a full-byte rehash.

## Result and decision

The 1+1 gate and all six formal arms were token exact and lifecycle exact. Every
control preemption counter was zero. Every candidate run applied and resumed
exactly once, invalidated exactly one generation, recomputed 2,178 tokens, and
reported zero fallback. Final active-state delta was 16 in every arm. Peak HBM
was 55,085 MiB in both arms.

| metric | control median | candidate median | candidate change |
|---|---:|---:|---:|
| pressure TTFT p50 | 1,566.811 ms | 692.851 ms | -55.780% |
| pressure TTFT p95 | 1,927.006 ms | 1,054.702 ms | -45.267% |
| pressure TTFT max | 1,967.119 ms | 1,094.908 ms | -44.340% |
| long TTFT | 292.752 ms | 292.912 ms | +0.055% |
| long TPOT | 29.280 ms | 73.170 ms | +149.893% |
| long sojourn | 1,200.447 ms | 2,561.459 ms | +113.375% |
| matched wall interval | 3,248.745 ms | 3,232.890 ms | -0.488% |
| request/s | 1.539056 | 1.546604 | +0.490% |
| request/s CV | 0.763% | 0.999% | — |
| peak HBM | 55,085 MiB | 55,085 MiB | 0 |

The candidate substantially reduces pressure-request wait, but recomputing the
long request more than doubles its sojourn and exceeds the preregistered 5%
protected-regression limit. The frozen candidate is therefore a **matched
negative** and remains default-off/rejected for production use. This result is
not a speedup claim and provides no comparison with vLLM or vLLM-HUST.

Raw request traces, per-arm JSON, startup logs, HBM samples, status and cleanup
evidence are retained under `results/issue57-preemption-20260815-r1-1plus1/`,
`results/issue57-preemption-20260815-r2-1plus1/` and
`results/issue57-preemption-20260815-r2-3plus3/`.
