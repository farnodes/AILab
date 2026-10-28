# Session progress (update after every 30 min block)

**Fresh start:** track progress in the **roadmap UI** → [learner/progress.json](../progress.json)

```bash
./lab-ui.sh   # http://127.0.0.1:8765
```

| Field | Value |
|-------|--------|
| **Last completed** | *(reset — none)* |
| **Phase** | 0 — Bootstrap |
| **Active day** | Day 1 (see progress JSON) |
| **LLM runtime** | `./server.sh` |

---

## After each session

1. Mark steps **done** in the roadmap UI (`./lab-ui.sh`).
2. Optional: `learner/journal/YYYY-MM-DD.md` notes.
3. Set **Last completed** here when the day file’s **Day progress** is **done**.

---

## Revision index (later chapters)

| Phase | Chapter revision |
|-------|------------------|
| 0 | [phase0-bootstrap.md](../../docs/revision/phase0-bootstrap.md) |
| 1 | [phase1-slms.md](../../docs/revision/phase1-slms.md) |
| 2 | [phase2-rag-context.md](../../docs/revision/phase2-rag-context.md) |
| 3 | [phase3-agents.md](../../docs/revision/phase3-agents.md) |
| 4 | [phase4-ide.md](../../docs/revision/phase4-ide.md) |
| 5 | [phase5-production.md](../../docs/revision/phase5-production.md) |

Per-day one-liners: [revision/daily.md](../../docs/revision/daily.md)
