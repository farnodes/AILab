# Phase 0 — Bootstrap (server & API)

**Days:** 1–7 · **Next:** [phase1.md](./phase1.md)

**Section order:** 1 API → 2 Tokens → 3 Context → 4 GGUF preview (full detail in Phase 1).

---

## 1. OpenAI-compatible API

`GET /health`, `GET /v1/models`, `POST /v1/chat/completions` (stream & non-stream).

[README.md](./README.md) — Qwen3 via `llama-server` on port 8080.

---

## 2. Tokens

Subword units; `usage` in responses; shorter prompts leave room for answers.

---

## 3. Context window

`-c 4096` — prompt + history + completion must fit; test long-input behavior on Day 5.

---

## 4. GGUF preview

Quantized weights on disk (~1.2 GB for Qwen3 1.7B Q4_K_M). **Phase 1** covers formats and VRAM math.

---

## Done when

- [ ] Start/stop server; curl demos
- [ ] Journal: token & context
- [ ] Ready for Day 8 (quantization)

---

## Related

[phase1.md](./phase1.md) · [DAILY_30MIN.md](./DAILY_30MIN.md)
