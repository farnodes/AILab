# Session progress (update after every 30 min block)

Edit this file when you finish a day. Cursor and [OPEN.md](../../OPEN.md) use it for your **revision recap**.

| Field | Value |
|-------|--------|
| **Last completed** | Day **1** |
| **Phase** | 0 — Bootstrap |
| **Last journal** | [2026-10-19.md](./2026-10-19.md) |
| **Next up** | Day **2** — non-streaming chat → `experiments/day02-response.json` |
| **Next guide** | [phase0.md](../phase0.md) |
| **Start** | `./server.sh` |

---

## After each session (copy checklist)

1. Write `docs/journal/YYYY-MM-DD.md`
2. Update the table above (`Last completed`, `Next up`, `Last journal`)
3. Skim **Last chapter revision** below (or [revision/](../revision/))
4. Optional: `git commit -m "journal: day N — …"`

---

## Last chapter revision (auto: read linked file)

**You finished:** Phase 0 · Day 1 — Server & API  

→ Full recap: [revision/phase0-bootstrap.md](../revision/phase0-bootstrap.md) · Day 1 bullets in [revision/daily.md](../revision/daily.md#day-1)

### Quick recall (Day 1)

- **Token** — subword unit; counts appear in `usage`.
- **Context** — everything in one request; here ~**4096** tokens (`-c 4096`).
- **Endpoints** — Ollama: `GET /api/tags`, `POST /v1/chat/completions` on port **11434**.
- **Model** — **`lfm3`** via Ollama (`http://127.0.0.1:11434/v1`).

### Today’s one-liner (Day 2)

Non-streaming `curl` chat; save full JSON; note `prompt_tokens`, `completion_tokens`, `finish_reason`.

---

## Revision index by phase (chapter)

| Phase | Chapter revision |
|-------|------------------|
| 0 | [phase0-bootstrap.md](../revision/phase0-bootstrap.md) |
| 1 | [phase1-slms.md](../revision/phase1-slms.md) |
| 2 | [phase2-rag-context.md](../revision/phase2-rag-context.md) |
| 3 | [phase3-agents.md](../revision/phase3-agents.md) |
| 4 | [phase4-ide.md](../revision/phase4-ide.md) |
| 5 | [phase5-production.md](../revision/phase5-production.md) |

Per-day one-liners: [revision/daily.md](../revision/daily.md)
