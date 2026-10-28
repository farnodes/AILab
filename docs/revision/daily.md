# Daily revision one-liners

After completing day **N**, skim **Day N** here + the phase chapter file.  
Update [PROGRESS.md](../../learner/journal/PROGRESS.md) to point at the right phase revision.

## Phase 0 (Days 1–7)

### Day 1 {#day-1}
Server `/health` & `/v1/models`; **token** = subword unit; **context** ≈ 4096 tokens total per request.

### Day 2 {#day-2}
Non-streaming chat JSON; **`usage`** token counts; **`finish_reason`**.

### Day 3 {#day-3}
Streaming (`stream: true`); time-to-first-token.

### Day 4 {#day-4}
System prompt / temperature affects verbosity and randomness.

### Day 5 {#day-5}
Long prompts vs context limit `-c 4096`.

### Day 6 {#day-6}
Decide-first: prompt vs RAG vs workflow vs train.

### Day 7 {#day-7}
Review: health, models, one chat without notes.

---

## Phase 1 (Days 8–21)

| Day | Recall |
|-----|--------|
| 8 | GGUF vs AWQ/GPTQ/EXL2 |
| 9 | Q4_K_M tradeoff for 1.7B |
| 10 | VRAM ≈ Params×Bits/8 |
| 11 | KV-cache grows with context |
| 12 | llama-server flags |
| 13 | Ollama / LM Studio vs llama.cpp |
| 14 | vLLM, TGI, SGLang when to use |
| 15 | Top-P, Top-K, Min-P |
| 16 | Thinking models + repetition penalty |
| 17–21 | Client: health, chat, stream, env, pytest |

Chapter: [phase1-slms.md](./phase1-slms.md)

---

## Phase 2 (Days 22–56)

| Block | Recall |
|-------|--------|
| 22–28 | Prompt files, JSON, Pydantic, classify CLI |
| 29–35 | Golden set, accuracy, prompt_version |
| 36–49 | Corpus, chunk, embed, retrieve, cite, refuse |
| 50–56 | Hybrid, rerank, GraphRAG, rag eval |

Chapter: [phase2-rag-context.md](./phase2-rag-context.md)

---

## Phase 3–5 (Days 57+)

| Phase | Days | Chapter |
|-------|------|---------|
| 3A Tools | 57–70 | [phase3-agents.md](./phase3-agents.md) |
| 3B Orchestration | 71–84 | same |
| 4 IDE | 85–91 | [phase4-ide.md](./phase4-ide.md) |
| 5 Prod | 92–112 | [phase5-production.md](./phase5-production.md) |

Full task list: [DAILY_30MIN.md](../guides/DAILY_30MIN.md)
