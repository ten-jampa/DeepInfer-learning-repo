# Mission: Understand DeepInfer — DeepSeek's production inference framework

## Why

Three goals, in the user's own words: **career edge** (ML infra / inference engineering skillset worth putting on a resume),
**understand the frontier** (know exactly what state-of-the-art LLM serving looks like and why HN called the release a
"nuclear bomb" in Oct 2026), and **build on it** (be able to take the code and construct on top of it).

## Success looks like

- Explain every feature bullet in DeepInfer's README and every major concept in `doc/inference_deployment_qa.md` at
  whiteboard depth — including *which file in `../DeepInfer` implements it*.
- Can draw and teach the prerequisite DAG (fundamentals → serving primitives → hardware → DeepSeek deltas → repo map)
  to another engineer from memory.
- Completes a small runnable programming assignment each session (Python script or Jupyter notebook, no GPU needed).
- Can evaluate DeepInfer vs vLLM/SGLang/TensorRT-LLM for a hypothetical deployment, justifying with the repo's own
  benchmark methodology (and knowing its caveats).

## Constraints

- Local machine is a MacBook: **no SM100 GPUs, no Ascend NPUs** — no executing the engine. All assignments must be
  statically analysis- or simulation-based against the `../DeepInfer` clone.
- Sessions should stay short (~30–45 min); each ends with one tangible win.

## Out of scope

- Writing CUDA/CANN kernels or SASS-level optimization (appreciate them; don't write them).
- Training-side ML (unless it explains a serving decision).
- Deep math of quantization formats beyond what's needed to read `e4m3` / `ue8m0` / MXFP4 intelligently.
