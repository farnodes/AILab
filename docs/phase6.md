# Phase 6 — Evaluation, observability & production habits

**Duration:** ~1 week (Days 71–77 in [DAILY_30MIN.md](./DAILY_30MIN.md))  
**Prerequisites:** [phase2.md](./phase2.md) (golden sets started), apps from phases 3–5  
**Next:** [phase7.md](./phase7.md) — Training (optional) or capstone hardening

---

## Purpose

Know whether a change **helped or hurt** before you ship it. Phase 6 turns “it feels better” into **scores, traces, and regressions**—the same discipline you use for non-AI code.

Evals are not a one-time phase; they run continuously after Phase 6.

---

## Core concepts

### Golden datasets

Files of test cases, e.g. `evals/sets/intent_golden.jsonl`:

```json
{"input": "reset my password", "expected_intent": "task"}
```

Expectations can be:

- Exact label or field match
- Schema validity only
- Substring in output (citation path)
- Custom predicate in code

Hold out a **test** split you do not tune prompts on.

### Rule-based vs LLM-as-judge

| Method | Pros | Cons |
|--------|------|------|
| Rules / schema / regex | Cheap, deterministic | Brittle on free text |
| LLM-as-judge | Flexible rubrics | Bias, cost, variance |

Prefer rules for structure (JSON, citations); use judges sparingly with fixed rubrics.

### Tracing

Per request or per workflow run, log:

- `prompt_version` or hash
- Model id
- Latency, token `usage`
- Tool calls (name, args size, duration)
- `run_id`, `step` for workflows

Store as **jsonl** under `logs/traces/` for grep and notebooks.

### Regression workflow

```text
Change prompt / RAG / model
    → run_eval --tag my-change
    → compare to evals/history.csv
    → exit non-zero if below threshold
```

Same idea as unit tests failing CI.

---

## What you build

```text
evals/
  sets/
    intent_golden.jsonl
    rag_qa.jsonl
  run_eval.py          # scores + exit code
  run_all.sh           # optional umbrella
  history.csv          # tag, date, metric, value
logs/
  traces/              # session / run logs
```

**Metrics examples**

| Component | Metric |
|-----------|--------|
| Classifier | accuracy % |
| RAG | citation contains expected path |
| Tools | required tool was called (in test harness) |
| Workflow | final state field equals expected |

---

## Exercises

1. Intent eval: 20 cases; fail if accuracy &lt; 80%.
2. RAG eval: 10 questions; assert citation substring.
3. Append results with `--tag v0.3` to history.
4. Run eval before and after a prompt change; record delta.
5. Optional: one LLM-judge experiment + short bias note in journal.
6. Single command runs all evals.

---

## Done when

- [ ] `run_eval` (or equivalent) exits non-zero on regression.
- [ ] Traces include version/tag fields you can correlate with scores.
- [ ] You have a habit: **no prompt merge without eval**.

---

## Connection to training

[phase7.md](./phase7.md) **requires** Phase 6 baselines. Never train without before/after numbers on the same held-out set.

---

## Related docs

- [phase2.md](./phase2.md) — golden files origin
- [phase7.md](./phase7.md) — post-training comparison
- [journal/MILESTONES.md](./journal/MILESTONES.md) — checklist
