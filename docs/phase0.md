# Phase 0 — Runtime & mental model

**Duration:** ~1 week (Days 1–7 in [DAILY_30MIN.md](./DAILY_30MIN.md))  
**Prerequisites:** None  
**Next:** [phase1.md](./phase1.md) — Clients & application skeleton

---

## Purpose

Learn what “running AI” actually means on your machine before you write application code. You are not training anything yet—you are operating an **inference server** and reading its HTTP API like any other backend service.

By the end of Phase 0 you should comfortably answer: *What is a token? What is context? Why Q4_K_M? What does the server expose?*

---

## What you are running

| Piece | In this repo |
|-------|----------------|
| **Runtime** | `llama-server` (llama.cpp) in `.llama/llama-b11724/` |
| **Weights** | Qwen3 1.7B GGUF, quantized `Q4_K_M` (~1.2 GB) |
| **API** | OpenAI-compatible HTTP at `http://127.0.0.1:8080/v1` |
| **Context** | `-c 4096` → up to ~4096 tokens in the window (prompt + reply) |

See [README.md](./README.md) for start/stop commands.

---

## Core concepts

### Tokens

Text is split into **tokens** (subword pieces). The model predicts the next token repeatedly until it stops.

- Shorter prompts cost less time and leave more room for the answer inside the context window.
- `usage` in API responses reports `prompt_tokens`, `completion_tokens`, `total_tokens`.

### Context window

Everything the model “sees” in one request must fit in the **context** (here, 4096 tokens). That includes system message, chat history, RAG chunks (later), and the generated reply.

If you exceed it, you get truncation, errors, or silent clipping—behavior depends on the server. Phase 0 includes an exercise with an intentionally long prompt.

### Quantization (Q4_K_M)

Full weights are huge; **quantization** compresses them for faster inference and less RAM. `Q4_K_M` is a common tradeoff: good speed/size with acceptable quality for a 1.7B model.

Larger models or higher quant quality (e.g. Q8) improve answers but need more memory and time.

### Local vs cloud inference

| Local (`llama-server`) | Cloud API |
|------------------------|-----------|
| Data stays on device | Data leaves your network |
| No per-token bill | Usage-based cost |
| You manage RAM/speed | Provider scales hardware |
| Good for learning & privacy | Good for strongest models |

This lab is **local-first**; Phase 1 can add `LLM_BASE_URL` for a cloud endpoint later.

### OpenAI-compatible API

Many tools speak the same shape as OpenAI’s chat API:

- `POST /v1/chat/completions` — messages in, assistant message out
- `GET /v1/models` — list loaded model id
- `GET /health` — server alive

That compatibility lets you reuse SDKs and tutorials with only a base URL change.

---

## Key API fields (chat completion)

After a non-streaming request, inspect the JSON:

| Field | Meaning |
|-------|---------|
| `choices[0].message.content` | Assistant text |
| `choices[0].finish_reason` | e.g. `stop`, `length` |
| `usage` | Token counts |
| `model` | Model id string |

**Streaming:** same endpoint with `"stream": true`; response is SSE chunks with `delta.content`.

---

## Exercises

1. Start server; `curl` `/health` and `/v1/models`.
2. Non-streaming chat (README example); save full JSON.
3. Streaming chat; note time-to-first-token.
4. Compare terse vs verbose system instructions (or temperature if exposed).
5. Oversized prompt vs `-c 4096` limit.
6. Skim [ROADMAP.md](./ROADMAP.md) “Decide first” table for your capstone.

---

## Done when

- [ ] You can start and stop the server without the README.
- [ ] You can explain **token**, **context**, and **quantization** in plain language.
- [ ] You have run streaming and non-streaming completions and read `usage` / `finish_reason`.

---

## Common pitfalls

- **Server not listening** — check port 8080; another process may hold it.
- **First run slow** — model load from disk; later requests are faster.
- **Verbose / “thinking” output** — some models (Qwen3) have reasoning modes; adjust prompts or model docs if replies are oddly long.

---

## Related docs

- [README.md](./README.md) — commands
- [phase1.md](./phase1.md) — wrap this API in code
