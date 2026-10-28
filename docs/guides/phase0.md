# Phase 0 — Bootstrap (server & API)

**Days:** 1–7 · **Runtime:** [README.md](../README.md) — **Ollama** `lfm3` at `http://127.0.0.1:11434/v1` · **Next:** [phase1.md](./phase1.md)

Hands-on steps live in the roadmap UI (`curriculum/curriculum.json`). This page is the map.

---

## What you practice

| Day | Skill | Check |
|-----|--------|--------|
| **1** | `./server.sh`, `ollama list`, `GET /api/tags` | Service up; model id is `lfm3` |
| **2** | `POST /v1/chat/completions` (no stream) | `content`, `reasoning`, `usage`, `finish_reason`; history only if you resend `messages` |
| **3** | Same URL with `stream: true` | SSE `data:` lines, time to first token, join `delta.content` |
| **4** | System prompt + temperature | Same question, terse (temp 0) vs coach (temp 1) |
| **5** | Context budget | Small prompt vs oversized prompt; why RAG exists |
| **6** | Capstone | One row from [ROADMAP](./ROADMAP.md) “Decide first”; one track |
| **7** | Exit demo | Batch + stream from memory; score the checklist below |

Stay on **`lfm3`** all week. Extra models are scheduled in [ROADMAP](./ROADMAP.md) (embeddings ~Day 38, stronger instruct model before tools).

---

## 1. API (Days 1–3)

| Call | Use |
|------|-----|
| `GET http://127.0.0.1:11434/api/tags` | Ollama inventory — “is it up, which models?” |
| `POST http://127.0.0.1:11434/v1/chat/completions` | OpenAI-compatible chat. Omit `stream` or `false` for one JSON body; `stream: true` for SSE |

`/v1/*` is the layer your later Python client will call. `/api/tags` is the Ollama health check (there is no llama.cpp `GET /health` on this port).

---

## 2. Tokens (Day 1 journal, Day 2 numbers)

Subword pieces, not words. Read `usage.prompt_tokens`, `usage.completion_tokens`, `usage.total_tokens`. On LFM3, completion tokens include **reasoning** even when the UI only shows `message.content`.

---

## 3. Context (Day 5)

Prompt + history you resend + the new reply share one budget. This lab’s working cap is **~4096 tokens**. A huge paste truncates, errors, or drops the middle. Phase 2 retrieves chunks instead of stuffing a whole doc into one call.

---

## 4. Sampling preview (Day 4)

`messages[].role`: `system` sets policy, `user` carries the task. `temperature` 0 for stable short answers; higher for variation. Phase 1 goes deeper (Top-P, Top-K, repetition penalty). GGUF and VRAM math start on **Day 8**.

---

## Done when

- [ ] `./server.sh` and a tags check without the README open
- [ ] Journal: token and context window
- [ ] Saved `examples/day02-response.json` and a Day 3 streaming note
- [ ] You can say: base URL, model id `lfm3`, stream vs batch, `finish_reason`
- [ ] Ready for Day 8 (quantization)

---

## Related

[phase1.md](./phase1.md) · [DAILY_30MIN.md](./DAILY_30MIN.md) · [revision/phase0-bootstrap.md](../revision/phase0-bootstrap.md)
