# Teaching Notes

## User preferences
- Wants **concept + code + holistic education**: every lesson ties a concept to where it lives in the repo, and
  prerequisites are taught DAG-style so significance and depth both land.
- Wants **runnable coding assignments** per session — Python scripts or Jupyter notebooks, locally executable
  (no GPU machine; macOS). Assert-based self-checks give instant feedback.
- Background: between *fresh* and *intermediate* on transformers/KV cache/MoE/kernels. Define terms crisply as
  encountered; don't re-teach APIs-from-scratch, don't assume serving-systems fluency.

## Workspace facts
- Learning workspace: `/Users/tenzinjampa/Documents/learning-repos/DeepInfer-learning-repo` (this directory).
- Target repo clone: `/Users/tenzinjampa/Documents/learning-repos/DeepInfer` (sibling dir, referred to as `../DeepInfer`).
  3 commits: initial commit (d585e65) → Q&A docs update (8b16149) → QA EN update (774ce24). Fresh release, Oct 20 2026.
- Repo fact worth remembering: the batch `Scheduler` is **native code** in `deepinfer/_C` (`csrc/engine/`,
  `engine.pyi` stubs); Python side creates it in `engine/llm_engine.py::_create_scheduler`.
- `vendor/` DeepGEMM/DeepEP/FlashMLA/DeepSelect are git submodules (have Ascend twins), so don't count them as
  DeepInfer's own diff.
- HN reception (Oct 20 2026): 1,998 points, ~778 comments, front page. Claims to probe skeptically: the 155 T
  tokens/day + $38/GPU-hr disclosure (commenters redo the math), "nuclear bomb" label.

## Subagent audit — 2026-10-20 (two scouts)

### Codebase explorer findings (correct ground truth; file:line references verified)
- Boot path confirmed exactly, incl. `Scheduler` native (`csrc/engine/scheduler.hpp`, pybind),
  instantiated `llm_engine.py:308`. `examples/offline_inference.py` enters via `_config.create_llm`.
- **DSML does not exist in DeepInfer** — external deepseek-recipe handles token protocol. (Lesson C2 + repo map corrected.)
- **DFlash IS the draft (NextN) model**: `models/mtp/dflash.py:82`; own MoE pool with independent EPLB rounding
  (`benchmark.py:531-533`); Confidence Head exists (`DEEPINFER_DFLASH_CONFIDENCE_HEAD_TEMPERATURE`, environ.py:135).
- zos = zero-overhead scheduling (`DEEPINFER_ZERO_OVERHEAD_SCHEDULING`, default ON); per-step flow:
  C++ `scheduler.schedule` → `MetadataZOS` (pinned CPU remap + seqlens) → `prepare_tensor_input_zos.py` →
  GPU delta-fix by `tilelang_ops/compute_seqlens_k_zos.py` (fused `seqlens_k += seqlens_q − (nextn − accepted)`).
- Batch-invariance is default-ON in offline examples on NVIDIA (`offline_inference.py:43`); eval labels it "(slower)".
- Structured outputs are **all XGrammar** (compiler → SOMatcherBuilder pump → matcher → bitmask applied in sampler).
- Tests co-located in kernel sources with `_ref` Python reference ports (e.g. `compute_seqlens_k_zos.py:35-45`) —
  **great source of future assignments** (fused kernel + reference + pytest in one file is the repo's idiom).
- `ca_state`/`ica_state` are `cache_engine.py:209-214` fields (StateBlock `[stored SWA | dropped]` :221-235);
  "20 stored layers" derives from config. `cross_layer.py` = share-kv/index/index-k topology (closest home of
  "block KV projected across layers"); `engram_*.py` = Engram hash n-gram vocab layer (separate deepseek-ai/Engram repo).
- Engine comments are largely **Chinese** — pair code reading with the QA doc when teaching 0002+.
- Benchmark constants: prefill warmup 5/measure 10/profile 2 (:103-105); decode 50/60/3 (:108-110);
  `decode_tokens_per_s_per_gpu = avg_sps × decode_num_requests × (1+nextn) / cp_size` (:408), full-acceptance.
- Vendor: DeepSelect IS a submodule; TileKernels is referenced by README but NOT vendored here.

### Resource-scout findings
- All links alive; Zhihu = 403 bot-wall (use browser). HN thread now 2,007 pts. deepseek-ai org also has
  `DeepSpec`, `LPLB`, `Engram`, `open-infra-index` repos.
- Big gap-close: **V4.1-Flash has English architecture sources** (HF model card incl. CED 20+20, 1+384 experts,
  DSpark, 890B/token global KV). Remaining half-gap: production cluster ops (Chinese-primary).
- Economics teaching pair: abound's "plausibly real" math (HN 50163753) vs yfontana's ~70k-GPU rebuttal (50172066);
  CellCog's "valley pricing = floor not average" nuance.
- RESOURCES.md fully rebuilt from the scout's report (topic packs a–l; heavyweight HN comments annotated there).

## Lesson sequencing (updated)
- 0001 done (prerequisite DAG; corrected once from the audit). Assignment 0001 live.
- 0002 (next): prefill vs decode in motion + the engine's batching (A1, A3, B3; read `examples/benchmark.py` metrics;
  use the HN economics pair as the opener hook).
- 0003: KV cache & paged KV + parallelism suite (A2, A4, A5, B5) — Mooncake + SGLang blog as secondary sources.
- 0004: model architecture (C1, C2) — lab: `models/deepseek.py`, `v4_modules/` (cross_layer, compress, yoco, engram);
  primary = HF model card English section + V2/V3 reports.
- 0005: the novel serving tricks (C3 SWA replay, C4 DSpark/DFlash) — lab: `input_metadata/yoco.py`,
  `mtp/dflash.py`; reuse `_ref` kernel-port idiom for an assignment.
- 0006: measurement & ethics of numbers (D6, D3; also determinism C5) — build an assignment inverting the
  full-acceptance accounting; teach Benchmarking-honesty sources.
- Spacing: quiz re-take of 0001 blocks at 2d and 7d spread (remind user in next session).

