# Phase 1 — Clients & application skeleton

**Duration:** ~1 week (Days 8–14 in [DAILY_30MIN.md](./DAILY_30MIN.md))  
**Prerequisites:** [phase0.md](./phase0.md)  
**Next:** [phase2.md](./phase2.md) — Prompting & structured logic

---

## Purpose

Treat the LLM as a **network dependency**: timeouts, errors, tests, and a single place in code that talks to `http://127.0.0.1:8080/v1`. Everything later (RAG, tools, agents) should call your client—not scatter raw `curl` everywhere.

---

## Core concepts

### Messages and roles

Chat APIs use an array of messages:

| Role | Typical use |
|------|-------------|
| `system` | Rules, persona, output format |
| `user` | End-user input |
| `assistant` | Model replies (include in history for multi-turn) |

**Conversation state** is just this list growing over turns. The server does not magically remember past sessions unless you send history again (or add your own DB later).

### SDK vs HTTP

- **Raw HTTP** (`httpx`, `fetch`): full control, easy to mock in tests.
- **OpenAI SDK** with `base_url` pointing at local server: less boilerplate, same API shape.

For learning, a thin `httpx` wrapper is enough.

### Streaming

Streaming improves perceived latency: print tokens as they arrive. Implementation reads SSE or chunked JSON lines until `[DONE]`.

### Configuration

Use environment variables so one codebase switches targets:

```text
LLM_BASE_URL=http://127.0.0.1:8080/v1
LLM_API_KEY=optional-for-local
LLM_MODEL=enacimie/Qwen3-1.7B-Q4_K_M-GGUF
```

### Reliability

- **Timeout** (e.g. 30s) — local model can hang on huge prompts.
- **Clear errors** — distinguish connection refused vs HTTP 4xx/5xx.
- **Mocked tests** — CI should not require `llama-server` running.

---

## What you build

```text
tools/
  llm_client/
    __init__.py      # health(), chat(), stream_chat()
    config.py        # env defaults
experiments/
  01_hello_chat.py   # CLI entry
tests/
  test_llm_client.py # mocked HTTP
```

**Minimum API:**

| Function | Behavior |
|----------|----------|
| `health()` | `GET /health` or lightweight completion |
| `chat(messages, **kwargs)` | Returns assistant string |
| `stream_chat(messages, **kwargs)` | Yields content deltas |

---

## Exercises

1. `health()` with friendly error if server is down.
2. `chat()` with timeout and model id from env.
3. `stream_chat()` printing to stdout.
4. One pytest with mocked response body.
5. CLI: `python experiments/01_hello_chat.py "question"`.

---

## Done when

- [ ] Library + CLI demo work against your local server.
- [ ] Tests pass **without** the server running.
- [ ] `LLM_BASE_URL` documented in a short README under `tools/llm_client/`.

---

## Design tips

- Keep the client **dumb** — no business prompts here; Phase 2 owns prompts.
- Log request id / latency at the call site in apps, not necessarily inside the client.
- Return raw response objects optionally for debugging (`return_full=True`).

---

## Related docs

- [phase0.md](./phase0.md) — HTTP API basics
- [phase2.md](./phase2.md) — prompts on top of `chat()`
