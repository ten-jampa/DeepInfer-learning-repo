#!/usr/bin/env python3
"""Assignment 0001 — Trace DeepInfer's boot path (no GPU required).

Your job: fill in the ANSWERS dict by reading the code in ../DeepInfer, then run:

    python3 0001-trace-boot-path.py

Every answer gets an instant PASS/FAIL with a hint at the exact file to open.
This is the grounding for Lesson 0001: know the boot path cold before Lesson 0002
digs into the scheduler and model runner.
"""
from pathlib import Path
import ast
import sys

REPO = Path(__file__).resolve().parents[1] / "DeepInfer"

# ---------------------------------------------------------------------------
# TODO: Fill your answers below (keep the keys; replace None with a string).
# ---------------------------------------------------------------------------

# 1. File: deepinfer/entrypoints/llm.py — the class a user instantiates offline.
ANSWER_USER_FACING_CLASS = None          # e.g. "Transformer"

# 2. File: deepinfer/engine/llm_engine.py — the engine class the user-facing
#    class wraps (the docstring says "__n__ wrap this class for offline
#    batched inference").
ANSWER_ENGINE_CLASS = None

# 3. File: deepinfer/engine/llm_engine.py — the method that creates the
#    scheduler (name only, without parentheses).
ANSWER_SCHEDULER_FACTORY = None

# 4. The scheduler lives in the *compiled* extension. In deepinfer/_C/engine.pyi
#    there is a stub class for it — what is its name?
ANSWER_NATIVE_SCHEDULER_CLASS = None

# 5. File: deepinfer/worker/model_runner.py — the per-worker class that runs
#    the model forward pass on the GPU(s).
ANSWER_RUNNER_CLASS = None

# 6. File: deepinfer/model_executor/models/deepseek.py — the top-level model
#    class nn.Module that calls the decoder layers (the "...ForCausalLM" one).
ANSWER_TOP_LEVEL_MODEL_CLASS = None

# ---------------------------------------------------------------------------
TRUTH = {
    "ANSWER_USER_FACING_CLASS":      ("LLM",                  "deepinfer/entrypoints/llm.py, class ll.23"),
    "ANSWER_ENGINE_CLASS":           ("LLMEngine",            "deepinfer/engine/llm_engine.py, class ll.130"),
    "ANSWER_SCHEDULER_FACTORY":      ("_create_scheduler",    "deepinfer/engine/llm_engine.py, ll.307"),
    "ANSWER_NATIVE_SCHEDULER_CLASS": ("Scheduler",            "deepinfer/_C/engine.pyi, ll.309"),
    "ANSWER_RUNNER_CLASS":           ("ModelRunner",          "deepinfer/worker/model_runner.py, class ll.53"),
    "ANSWER_TOP_LEVEL_MODEL_CLASS":  ("DeepseekForCausalLM",  "deepinfer/model_executor/models/deepseek.py, class ll.251"),
}


def classes_in(path: Path):
    try:
        tree = ast.parse(path.read_text())
    except (OSError, SyntaxError):
        return []
    return [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]


def main() -> int:
    print(f"Repo: {REPO}\n")
    checks = {
        "ANSWER_USER_FACING_CLASS":      classes_in(REPO / "deepinfer/entrypoints/llm.py"),
        "ANSWER_ENGINE_CLASS":           classes_in(REPO / "deepinfer/engine/llm_engine.py"),
        "ANSWER_SCHEDULER_FACTORY":      None,
        "ANSWER_NATIVE_SCHEDULER_CLASS": classes_in(REPO / "deepinfer/_C/engine.pyi"),
        "ANSWER_RUNNER_CLASS":           classes_in(REPO / "deepinfer/worker/model_runner.py"),
        "ANSWER_TOP_LEVEL_MODEL_CLASS":  classes_in(REPO / "deepinfer/model_executor/models/deepseek.py"),
    }
    passed = 0
    for key, (truth, hint) in TRUTH.items():
        mine = globals().get(key)
        if mine is None:
            print(f"○ {key}: not filled in yet")
            continue
        ok = mine == truth and (checks[key] is None or truth in checks[key])
        passed += int(ok)
        mark = "✓ PASS" if ok else "✗ FAIL"
        print(f"{mark}  {key} = {mine!r}" + ("" if ok else f"  → correct: {truth!r}  (hint: {hint})"))
    filled = sum(globals().get(k) is not None for k in TRUTH)
    total = len(TRUTH)
    print(f"\n{passed}/{total} correct — {filled} filled in.")
    if filled < total:
        print("Keep reading and fill the rest in. Reading tip: search for 'class' "
              "declarations in each file listed under TRUTH once you've tried honestly.")
    elif passed == total:
        print("Boot path locked in. You're ready for Lesson 0002 (scheduler & batching).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
