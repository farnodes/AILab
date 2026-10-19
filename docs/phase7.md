# Phase 7 — Training & adaptation for a specific task

**Duration:** ~2–4 weeks optional (Days 85–91+ in [DAILY_30MIN.md](./DAILY_30MIN.md))  
**Prerequisites:** [phase6.md](./phase6.md) (baselines), [phase2.md](./phase2.md) (task definition)  
**Note:** Skip this phase if prompting + few-shot already passes your evals.

---

## Purpose

Improve **repeatable behavior**—output format, classification boundaries, tone, tool-call style—not to store a changing knowledge base in weights.

Training is **optional** in this curriculum. Most lab work should stop at prompts, RAG, tools, and workflows unless evals show a clear gap.

---

## When training helps vs hurts

| Good fit | Poor fit |
|----------|----------|
| Stable JSON / label schema | Product catalog that changes weekly |
| Support tone, disclaimers | Facts that belong in RAG or a DB |
| Tool-call trajectories (style) | Replacing a workflow engine |
| Narrow task with lots of examples | General reasoning at huge scale |

**Rule:** Facts → RAG / tools / SQL. Habits → prompts first, then SFT/LoRA.

---

## Methods (simplest → heavier)

| Method | Data | Role |
|--------|------|------|
| Few-shot in prompt | 3–20 examples | Always try first |
| **SFT** | Hundreds–thousands `(input, output)` | Teach task + format |
| **LoRA / QLoRA** | Same as SFT | Smaller trainable adapter |
| **DPO / preference** | Good vs bad pairs | Style alignment after SFT |
| **Distillation** | Teacher model outputs | Compress behavior into small local model |

Your local stack serves **GGUF** via `llama-server`. Training usually happens on a **full-precision or HF checkpoint**, then you **merge LoRA → export → quantize → serve**.

---

## Recommended pipeline

1. **Collect** failures from [phase6.md](./phase6.md) traces (bad JSON, wrong labels).
2. **Curate** 200–2k clean rows; dedupe; remove PII.
3. **Baseline** eval on held-out set (current Qwen3 + prompt).
4. **Train** LoRA (Unsloth, TRL, or MLX on Apple Silicon).
5. **Merge & export** to GGUF (Q4_K_M or similar).
6. **Serve** with same `llama-server` flags as [README.md](./README.md).
7. **Re-eval** task set + **smoke** general questions (avoid catastrophic narrow overfitting).
8. **Document** what improved and what regressed in `docs/journal/training-decision.md`.

---

## What you build

```text
training/
  README.md            # baseline score, hyperparams, export steps
  datasets/
    intent.jsonl       # chat messages or instruction/response
  scripts/
    prepare.py         # split, validate
    train_lora.py      # or notebook
    export_gguf.sh
  configs/
    qwen3-1.7b-lora.yaml
evals/
  task_specific/       # frozen test set for before/after
```

**Example jsonl row (instruction style)**

```json
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "{\"intent\": \"task\"}"}]}
```

---

## Exercises

1. Export 50–100 rows from golden set + corrected failures.
2. Record baseline accuracy in `training/README.md`.
3. Environment setup for one training stack (do not require finishing train in one session).
4. Mini run: 1 epoch on subset **or** documented dry-run plan.
5. List export steps to GGUF for your toolchain.
6. Decision doc: train vs prompt for your capstone.

---

## Done when

- [ ] You either **ship** a LoRA/GGUF that beats baseline on task eval, **or**
- [ ] You document **why not to train** with eval evidence.
- [ ] You can explain why facts were not put into weights.

---

## Tooling pointers

- [Hugging Face TRL](https://github.com/huggingface/trl) — SFT, DPO
- [Unsloth](https://github.com/unslothai/unsloth) — efficient LoRA
- MLX — Apple Silicon experiments
- `.llama/llama-b11724/llama-export-lora` — llama.cpp LoRA tooling

---

## After Phase 7

Continue capstone work under [DAILY_30MIN.md](./DAILY_30MIN.md) “After Day 84”. Optional: [ROADMAP.md](./ROADMAP.md) **Skills** (Phase 8) for packaging behavior into `SKILL.md` bundles.

---

## Related docs

- [phase6.md](./phase6.md) — required baselines
- [phase0.md](./phase0.md) — serving GGUF locally
- [ROADMAP.md](./ROADMAP.md) — decide-first ladder
