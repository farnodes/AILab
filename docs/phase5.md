# Phase 5 — Agents & multi-step workflows

**Duration:** ~2 weeks (Days 57–70 in [DAILY_30MIN.md](./DAILY_30MIN.md))  
**Prerequisites:** [phase3.md](./phase3.md) (tools), [phase4.md](./phase4.md) (RAG optional but common)  
**Next:** [phase6.md](./phase6.md) — Evaluation & observability

---

## Purpose

Move from single requests to **multi-step systems with state**. The critical distinction:

| Pattern | Who decides the next step? |
|---------|----------------------------|
| **Workflow** | Your code / explicit graph |
| **Agent** | Model + tool loop inside a bounded step |
| **Hybrid** | Workflow calls an agent for one messy subtask |

Workflows own **order, retries, and side effects**. Agents own **ambiguous planning** when the path is not fixed.

---

## Core concepts — Workflows

### State machine / DAG

Example pipeline:

```text
RECEIVED → CLASSIFY → RETRIEVE → DRAFT → APPROVE → DONE
```

- Each step reads/writes a **state object** (dataclass or dict).
- Branching is **code**: `if confidence < 0.8: escalate`.
- LLM steps should be **small**: input state slice → structured patch.

### Durable execution

Persist after each step:

```text
checkpoints/{run_id}.json   # step name, payload, timestamps
```

If the process crashes, resume at step 3 instead of re-running from scratch.

### Human-in-the-loop

Before **write**, **send**, **pay**, or **delete**: block on approval (CLI prompt, queue, or UI). The workflow records `approved_by` and time.

---

## Core concepts — Agents

### ReAct loop

Reason → choose tool → observe result → repeat until stop or max steps.

Use read-only tools first; cap steps (e.g. 8–10).

### Plan-and-execute

Optional pattern: planner outputs a list of steps; executor runs tools; replan on failure.

### Context hygiene

One clear goal per thread. Summarize or drop old turns when the window fills.

---

## Comparison table

| | Workflow | Agent |
|---|----------|--------|
| Predictability | High | Lower |
| Best for | Billing, ETL, ticket pipelines | Research, exploration |
| Debugging | Step logs | Tool traces |
| Failure mode | Stuck step | Tool loop / hallucinated args |

---

## What you build

```text
apps/agent_lab/
  workflow.py          # steps + checkpoint save/load
  agent_loop.py        # ReAct + max_steps
  memory.py            # thread history (optional)
  checkpoints/
logs/traces/           # jsonl: run_id, step, tools, tokens
```

**Example hybrid**

1. Workflow classifies ticket (Phase 2 JSON).
2. If `billing`, RAG over `data/billing/` (Phase 4).
3. Draft reply via `chat()`.
4. Optional: `run_research_agent(goal)` for open-ended file research (Phase 3 tools).
5. `human_approve` before any write.

---

## Exercises

1. Draw state diagram in `docs/journal/`.
2. Implement workflow with checkpoint after each step.
3. Agent: summarize all files in `data/corpus/` (read-only).
4. Hybrid handoff: agent returns JSON summary consumed by next workflow step.
5. Crash test: document resume behavior.
6. Full jsonl trace for one run.

---

## Done when

- [ ] One **workflow** end-to-end with checkpoints.
- [ ] One **agent** task with tool trace.
- [ ] At least one **hybrid** path documented.
- [ ] You can explain when you would *not* use an agent for the whole pipeline.

---

## Libraries (after hand-rolling)

LangGraph, Temporal, Prefect, or asyncio + sqlite—only after you understand the loop yourself.

For larger orchestration (queues, supervisor workers), see **Phase 8** in [ROADMAP.md](./ROADMAP.md) (optional depth—not required for phase0–7 path).

---

## Related docs

- [phase6.md](./phase6.md) — measure workflow/agent quality
- [phase3.md](./phase3.md) — tool execution details
