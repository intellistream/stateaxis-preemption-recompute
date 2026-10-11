# ECPA activation-contract evidence

Evidence label: `manager-contract-mock-worker-non-performance`.

The vLLM-HUST Extension Manager verified the exact research-manifest digest,
host/API/protocol ranges, and both exclusive resource claims. Its dry run
rendered exactly one `--additional-config` argument with `experiment_mode=true`.
A real Manager-owned `native_state_engine --assembly-check-only` process then
accepted that payload and emitted assembly identity
`a5c78bf9390e19be568b23e8e276874809d834b9148cf36902a572ecc5bc6da1`.

StateAxis tests cover strict parsing, stale-digest and unsafe-contract
rejection, an OFF reference, exact ON outputs, one applied preemption, one
generation invalidation, one resume, exact recompute-token accounting, live
post-resume state, and clean shutdown. The OFF fixture uses two state slots so
both retained requests can finish; ON deliberately uses one slot to exercise
the pressure mechanism. Therefore this is a semantic/correctness comparison,
not matched performance evidence.

No accelerator kernels or model weights were executed in this current record.
It makes no latency, throughput, memory, capacity, or production-performance
claim. The frozen issue #57 real-NPU negative result remains authoritative.
