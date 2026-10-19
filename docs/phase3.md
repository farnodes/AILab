# Phase 3 — Multi-agent architectures & orchestration

**Days:** 57–84 (+ 99–103) · **Prerequisites:** [phase2.md](./phase2.md) · **Next:** [phase4.md](./phase4.md)

Track [COVERAGE.md](./COVERAGE.md). Order: **tools → workflows → agents → frameworks/memory**.

| Block | Days |
|-------|------|
| 3A Tools | 57–70 |
| 3B Orchestration | 71–84 |
| 3C Patterns & frameworks | 99–103 |

---

## 1. Tools & tool-call loop (Days 57–63)

Registry, `run_tool_loop()`, sandboxed files, traces.

---

## 2. Safety, MCP & REPL (Days 64–70)

Logging, deny shell, `git_status`, MCP, truncate results.

---

## 3. Workflows & checkpoints (Days 71–77)

**DAG / state machine:** `CLASSIFY → RETRIEVE → DRAFT → DONE`.

**DAG decomposition:** subtasks as nodes with dependencies (diagram Day 71).

Checkpoints, branching in code, human-in-the-loop (Day 80).

---

## 4. Agent patterns (Days 78–84, 99–100)

| Pattern | Day |
|---------|-----|
| **ReAct** | 78 |
| **Plan-and-execute** | 99 |
| **Reflection & self-correction** | 100 |
| **Tree-of-Thought (ToT)** | 📖 + journal with 100 |
| Hybrid workflow + agent | 81 |

---

## 5. Memory & frameworks (Days 83, 101–103)

| Topic | Day |
|-------|-----|
| Short-term sliding window | 83 |
| **Long-term episodic** (vector recall of tool steps) | 101 |
| **LangGraph** | 102 |
| **CrewAI** | 103 |
| **OpenAI Agents SDK** | 103 |
| **AutoGen** | 103 |

Hand-roll loops before adopting frameworks.

---

## Done when

- [ ] [COVERAGE.md](./COVERAGE.md) Phase 3 rows ✅

---

## Related

[phase4.md](./phase4.md) · [phase5.md](./phase5.md)
