# DeepInfer / LLM Inference Serving Resources

Curated for the course in `MISSION.md`. Verified live on 2026-10-20 by a resource-scout subagent; Zhihu posts reply
403 to plain fetches (bot-wall, not dead) — open in a browser. Grouped the way the course consumes them.

## Knowledge

### Ground truth (the course anchors)

- **The DeepInfer repo itself** — local clone at `/Users/tenzinjampa/Documents/learning-repos/DeepInfer`,
  [on GitHub](https://github.com/deepseek-ai/DeepInfer) (12k★, Apache-2.0). `README.md` = features.
  `doc/inference_deployment_qa.md` = densest design doc. `examples/README.md` = benchmark methodology.
- [HN thread (2,007 pts, ~750 comments)](https://news.ycombinator.com/item?id=50163277) — the public reception; see
  Wisdom below for heavyweight comments.
- [HF model card: DeepSeek-V4.1-Flash(-1017)](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)
  **English architecture section exists**: CED 20+20 layer split, asymmetric 8B/16B activation, 1 shared + 384 routed
  experts, DSpark description, 890 B/token global KV — resolves our "no English source" gap. [NVIDIA NIM card](https://build.nvidia.com/deepseek-ai/deepseek-v4.1-flash/modelcard)
  adds CSA2/SWA-Bounded-Replay/Single-Pass-mHC/FP4-KV renderings.

### (a/b/c) Serving fundamentals — papers that define the vocabulary

- [DistServe (OSDI'24)](https://arxiv.org/abs/2401.09670) — prefill/decode disaggregation + per-SLO (TTFT/TPOT
  goodput) resource planning. Reach for first when explaining *why* P/D split.
- [Sarathi-Serve (OSDI'24)](https://arxiv.org/abs/2403.02310) — chunked prefill, stall-free scheduling, defined
  TTFT/TBT-vs-throughput trade in one place.
- [Orca (OSDI'22)](https://www.usenix.org/conference/osdi22/presentation/yu) — iteration-level scheduling origin;
  the "before continuous batching" picture.
- [PagedAttention (SOSP'23)](https://arxiv.org/abs/2309.06180) — paged KV cache; vLLM lineage (DeepInfer's parent).
- [SGLang RadixAttention paper](https://arxiv.org/abs/2312.07104) — radix-tree KV *reuse*, what paged blocks
  don't give you; the academic frame for DeepInfer's 72h prefix-retention story.
- [Mooncake (v5, Oct 2026)](https://arxiv.org/abs/2407.00079) — KV-cache-first disaggregated cluster (Kimi).
  Closest published system to DeepInfer's KV tiering; treats KV as a distributed object across HBM/DRAM/SSD.
- [Splitwise (ISCA'24)](https://arxiv.org/abs/2311.18677) — phase-splitting economics lens (Microsoft).

### (d/e) Speculative decoding & MoE EP

- [Leviathan et al. (ICML'23)](https://arxiv.org/abs/2211.17192) — lossless speculative decoding; accepted-rate math.
- DeepSeek-V3 report [§MTP](https://arxiv.org/abs/2412.19437) — multi-token prediction, how draft-then-verify serving
  works at DeepSeek.
- [DeepSpec](https://github.com/deepseek-ai/DeepSpec) (7k★) — DeepSeek's own speculative-decoding training/eval
  stack; nearest open muscle to DSpark (which has no paper — see Gaps).
- [NVIDIA blog: Wide-EP on NVL72](https://developer.nvidia.com/blog/scaling-large-moe-models-with-wide-expert-parallelism-on-nvl72-rack-scale-systems) — large-scale EP + scale-up fabric economics.
- [vLLM blog: large-scale EP @ 2.2k tok/s/H200](https://vllm.ai/blog/2025-12-17-large-scale-serving) — DeepEP all-to-all
  (HT/LL), dual-batch overlap, EPLB, `FULL_AND_PIECEWISE` CUDA graphs in the open.
- [SGLang: PD-disagg + large-scale EP on 96×H100](https://www.lmsys.org/blog/2025-05-05-large-scale-ep) — first
  independent open implementation matching DeepSeek-style numbers; good replication reading.

### (f) Precision formats

- [OCP Microscaling (MX) v1.0 spec](https://www.opencompute.org/documents/ocp-microscaling-formats-mx-v1-0-spec-final-pdf) — ground truth: MXFP4 = E2M1 elements + one E8M0 ("ue8m0") scale per 32-block; defines e4m3/e8m0.
- [FP8 Formats for Deep Learning](https://arxiv.org/abs/2209.05433) — origin of E4M3/E5M2.
- [Microscaling FP4 study](https://arxiv.org/abs/2509.23202) — MXFP4 vs NVFP4 (per-16, E4M0... E4M3 scale,
  two-level) accuracy/kernel comparison; answers "why KV FP4 per-16 without global scale".

### (g/h) SWA/YOCO & MLA — the model-architecture canon

- [YOCO paper (arXiv 2405.05254)](https://arxiv.org/abs/2405.05254) + [Microsoft code](https://github.com/microsoft/unilm/tree/master/YOCO) — "You Only Cache Once": decoder-on-decoder,
  cache-once; the actual lineage of DeepInfer's YOCO-style decoder KV projected from encoder state.
- [Mistral 7B](https://arxiv.org/abs/2310.06825) — the canonical sliding-window-attention citation.
- [planetbanatt: "On MLA"](https://planetbanatt.net/articles/mla.html) — best English MLA explainer (latent
  compression, weight absorption).
- [DeepSeek-V2 report](https://arxiv.org/abs/2405.04434) — MLA's original paper; ablation table MHA/GQA/MLA.
- [FlashMLA](https://github.com/deepseek-ai/FlashMLA) (13k★) — the production decode kernels; pair with
  [Raschka's MLA summary](https://sebastianraschka.com/llm-architecture-gallery/mla).

### (i) Execution & scheduling

- [NanoFlow](https://arxiv.org/abs/2408.12757) — intra-device overlap; DeepInfer's async scheduler credits SGLang/NanoFlow.
- [SGLang v0.4: zero-overhead batch scheduler](https://www.lmsys.org/blog/2024-12-04-sglang-v0-4) — CPU/GPU overlap ship log.
  Honest counterpoint: [sglang#19347](https://github.com/sgl-project/sglang/issues/19347) — documented cases the claimed overlap
  doesn't materialize. Teach both.

### (j) DeepSeek infrastructure lineage

- [open-infra-index](https://github.com/deepseek-ai/open-infra-index) — official hub: Open-Source-Week summary,
  "Path to open-sourcing the inference engine", Insights into DeepSeek-V3 hardware.
- [3FS performance journal](https://maknee.github.io/blog/2025/3FS-Performance-Journal-1) — independent hands-on
  3FS analysis; the skeptical look at the 6.6 TiB/s claims. [+ 3FS repo](https://github.com/deepseek-ai/3FS).

### (k) The economics (teach both sides)

- [CellCog read of the Q&A](https://cellcog.ai/blog/deepseek-deepinfer-open-source) — flags that $38/GPU-hr is
  revenue **at valley (off-peak) pricing** — a floor, not an average; the nuance most summaries miss.
- [Reuters](https://www.reuters.com/technology/chinas-deepseek-claims-theoretical-cost-profit-ratio-545-per-day-2025-03-01) /
  [SCMP](https://www.scmp.com/tech/big-tech/article/3300734) /
  [Business Insider](https://www.businessinsider.com/deepseek-cost-profit-margin-revenue-inference-financials-paying-users-2025-3) — the journalistic critique pattern of
  DeepSeek margin arithmetic ("theoretical", free users, partial coverage); SCMP has the node-leasing math ($2/GPU-hr, 226.75 avg occupancy).
- [SemiAnalysis InferenceX: DeepSeek-V4.1-Flash](https://inferencex.semianalysis.com/inference/deepseek-v41-flash) (+ profit estimator) — closest thing to independent
  third-party throughput/cost tracking for this exact model.

### (l) The served model's architecture (besides the model card)

- [Baseten: why prefill drops to 8B](https://www.baseten.co/blog/deepseek-v41-flash-more-efficient-prefill-for-coding-agents) — serving-side interpretation.
- [Gingerlabs: V4.1-Flash architecture & benchmarks](https://gingerlabs.ai/blog/deepseek-v4-1-flash-benchmarks-capabilities-and-architecture) — faithful summary incl. FP4 KV ≈ 890 B/token.
- [andlukyane review](https://andlukyane.com/blog/paper-review-deepseek-v41-flash) — healthy skepticism: the report
  lacks controlled ablations isolating CED / FP4-KV / bounded-replay contributions.

### Benchmarking honesty (cross-course utility)

- [NVIDIA: LLM inference benchmarking fundamentals](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts) — TTFT/ITL/TPOT defined properly; how GenAI-Perf/LLMPerf mislead. The "best single source on honest benchmarking".
- [Meta-metrics for inference benchmarking](https://arxiv.org/abs/2508.10251) — the scholarly version; pairs with DeepInfer's own `examples/README.md` severity notes (profiler inflates step times up to ~50%).

## Wisdom (Communities)

- [HN thread above](https://news.ycombinator.com/item?id=50163277) — heavyweight comments to anchor lessons:
  [abound: the margin arithmetic is plausibly real](https://news.ycombinator.com/item?id=50163753) ·
  [yfontana: ~70k GPUs implied by 155T tok/day — "seems doubtful"](https://news.ycombinator.com/item?id=50172066) ·
  [Tepix: the bullish node math](https://news.ycombinator.com/item?id=50164639) ·
  [entrope: the real moat is the un-opened KV pipeline](https://news.ycombinator.com/item?id=50164340) ·
  [benjiro29: China energy/tax structure confounds the economics](https://news.ycombinator.com/item?id=50165437) ·
  [neutronicus: the release markets Ascend hardware](https://news.ycombinator.com/item?id=50167974) ·
  [rknos314: latency wins on private benchmarks, cite Artificial Analysis](https://news.ycombinator.com/item?id=50168191).
- [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) — practitioner deployment talk; kernel-report threads.
- [vLLM community](https://blog.vllm.ai) + Discord — widest practitioner pool for async-scheduler/DP-disagg practice.
- [SGLang / LMSYS blog + Discord](https://lmsys.org) — most DeepSeek-matched open stack; fastest follow-ups on DeepSeek releases.
- [GPU MODE (cuda-mode)](https://www.youtube.com/@GPUMODE) — UNVERIFIED-as-of-writing but well-known: kernel
  engineering lectures; where serving kernels are discussed in the open.
- [SemiAnalysis](https://semianalysis.com) — the independent scoreboard; cite methodology, not just numbers.
- [llm-d](https://llm-d.ai) — K8s-native serving community; wide-EP + disagg runbook-quality docs.
- [MLPerf Inference / MLCommons](https://mlcommons.org) — standardized honest benchmarking.

## Gaps

1. **No independent benchmark of DeepInfer itself.** Pareto plots are self-reported; as of 2026-10-20 nobody has
   published third-party numbers. Expect first numbers in GitHub issues, not papers.
2. **DSpark has no paper/repo** of its own (DeepSpec is adjacent but generic). When we teach C4, the Q&A + code is the
   only primary.
3. **The production KV-cache tiering is un-open-sourced and unexplained anywhere else** (3FS deep-dives don't cover
   DeepInfer's 100 PiB / 72h layer). Biggest unavoidable hole.
4. **$38/GPU-hr & 155T tok/day: no independent audit.** yfontana's ~70k-GPU arithmetic is unresolved; InferenceX
   estimator is the closest tool.
5. **Ascend 950 performance data: essentially none independent** — repo evidence only.
6. Production-cluster ops details (EP counts in prod, VE role behavior) remain Chinese-primary (Zhihu). Though
   V4.1-Flash model architecture now has solid English sources (model card), so the earlier gap shrinks to: *cluster
   ops*, not *model*.
