# Phase 1 — Local AI execution & small language models (SLMs)

**Days:** 8–21 · **Prerequisites:** [phase0.md](./phase0.md) · **Next:** [phase2.md](./phase2.md)

Read sections **1 → 6** in order (matches [TOPIC_SEQUENCE.md](./TOPIC_SEQUENCE.md)).

---

## Purpose

Run, serve, and tune **SLMs** locally—then wrap them in a **tested HTTP client**.

---

## 1. Quantization & formats (Days 8–10)

| Format | Use |
|--------|-----|
| **GGUF** | llama.cpp, Metal/CPU — **this lab** |
| **EXL2** | ExLlama / GPU |
| **AWQ / GPTQ** | vLLM, TGI |

Lower bits → less RAM, faster inference, some quality loss.

---

## 2. Memory & KV-cache (Day 11)

```text
Weight memory ≈ Parameters × Bits_per_weight / 8
Total ≈ weights + KV-cache + runtime overhead
```

KV-cache grows with **context length** (`-c 4096`) and concurrency.

---

## 3. Serving engines & runtimes (Days 12–14)

**Local:** llama.cpp (`llama-server`), Ollama, LM Studio.

**Production (survey):** vLLM, TGI, SGLang — higher throughput, GPU clusters.

---

## 4. Parameter tuning & sampling (Days 15–16)

Temperature, Top-P, Top-K, Min-P, repetition penalty.

**Thinking models (Qwen3):** concise system prompt; lower temp; cap `max_tokens`; adjust penalty if looping.

*(Phase 0 Day 4 was a preview; deepen here.)*

---

## 5. Application layer — client code (Days 17–21)

```text
tools/llm_client/     health(), chat(), stream_chat()
examples/01_hello_chat.py
tests/                  mocked httpx
```

Env: `LLM_BASE_URL`, `LLM_MODEL`, optional `LLM_API_KEY`.

---

## 6. Model adaptation (Days 105–106)

| Method | Coverage |
|--------|----------|
| **LoRA / SFT** | Day 105 — merge → GGUF → `llama-server` |
| **DPO / preference** | 📖 [COVERAGE.md](./COVERAGE.md) — after SFT |
| **Distillation** | Day 106 — teacher (cloud) → student (local SLM) |

Always **before/after** evals ([phase5](./phase5.md), [COVERAGE](./COVERAGE.md)).

---

## Done when

- [ ] GGUF vs AWQ/GPTQ explained
- [ ] Memory estimate for one model you run
- [ ] Sampling experiment documented
- [ ] Client + offline test

---

## Related

[README.md](../README.md) · [phase2.md](./phase2.md)
