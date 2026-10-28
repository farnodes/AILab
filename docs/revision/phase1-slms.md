# Phase 1 — SLMs & client (revision)

**Days 8–21** · Guide: [phase1.md](../guides/phase1.md)

---

## Big picture

Choose **how** models are stored (quantization), **where** they run (llama.cpp / Ollama / vLLM…), **how** you sample outputs, then wrap everything in a **tested HTTP client**.

---

## Must remember

| Topic | Recall |
|-------|--------|
| **GGUF / AWQ / GPTQ / EXL2** | Trade RAM vs speed vs quality; GGUF = llama.cpp. |
| **VRAM ≈** | `Params × Bits/8` + **KV-cache** + overhead. |
| **Local** | llama-server, Ollama, LM Studio. |
| **Prod scale** | vLLM, TGI, SGLang — throughput/GPU. |
| **Sampling** | Low temp for JSON; top-p/k/min-p; repetition penalty; thinking models need concise prompts. |
| **Client** | `health()`, `chat()`, `stream_chat()`; `LLM_BASE_URL`; mock tests. |

---

## Phase 1 exit check

Estimate memory for one SLM; run client + pytest without live server.
