# Phase 3 — Agents & orchestration (revision)

**Days 57–84** (+ 99–103) · Guide: [phase3.md](../guides/phase3.md)

---

## Big picture

**Tools** execute side effects; **workflows** own order and checkpoints; **agents** (ReAct) plan inside bounded steps; **frameworks** after you hand-roll once.

---

## Must remember

| Topic | Recall |
|-------|--------|
| **Tool loop** | Model proposes → code runs → observation → repeat (max steps). |
| **Safety** | Sandboxed paths; deny shell; truncate tool output; MCP. |
| **Workflow** | DAG/state machine; classify→RAG→draft; checkpoints. |
| **Human gate** | Approve before write/send/delete. |
| **ReAct** | Reason → act → observe. |
| **Advanced** | Reflection, plan-execute, LangGraph, CrewAI, episodic memory. |

---

## Phase 3 exit check

Trace replay; workflow + agent hybrid explained in 5 sentences.
