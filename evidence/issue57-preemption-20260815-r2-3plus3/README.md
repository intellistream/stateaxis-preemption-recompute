# Issue 57 preemption/recompute: frozen R2 3+3 result

This directory is the complete formal Qwen2.5-14B BF16 real-NPU 3+3 bundle.
It includes preregistration, all six arm runs, raw requests, effect/lifecycle
telemetry, NPU snapshots, environment and cleanup records. `SHA256SUMS` covers
every imported file except itself.

All arms were exact. ON improved pressure-request TTFT p50 by 55.780%, but the
protected long request's sojourn increased by 113.375% (1,200.447 ms to
2,561.459 ms), failing the preregistered 5% no-harm guard. Throughput changed
by only +0.490%, and peak HBM was unchanged. This is a workload-scoped matched
negative, not a claim that recompute cannot help other pressure patterns.
