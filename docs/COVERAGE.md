# Curriculum coverage checklist

Every **Farnodes** topic + **original lab** topic mapped to a **day** and **phase section**.  
When all rows show ✅, the path is complete. Partial = named in guide; do the linked day.

**Legend:** ✅ daily task · 📖 phase guide only · 🔜 extension day (92+)

---

## Phase 0 — Bootstrap

| Topic | Day | Doc |
|-------|-----|-----|
| llama-server / health / models | 1 | [phase0](./phase0.md) |
| Chat completions JSON & `usage` | 2 | phase0 |
| Streaming SSE | 3 | phase0 |
| Temperature / system prompt (preview) | 4 | phase0 |
| Context limit / truncation | 5 | phase0 |
| Decide-first / capstone | 6 | [ROADMAP](./ROADMAP.md) |
| Review | 7 | — |

---

## Phase 1 — SLMs & local execution

| Topic | Day | Doc |
|-------|-----|-----|
| GGUF | 8 | [phase1 §1](./phase1.md) |
| AWQ, GPTQ, EXL2 | 8–9 | phase1 §1 |
| VRAM ≈ Params×Bits/8 | 10 | phase1 §2 |
| KV-cache + context RAM | 11 | phase1 §2 |
| llama.cpp / `llama-server` | 12 | phase1 §3 |
| Ollama | 13 | phase1 §3 |
| LM Studio | 13 | phase1 §3 |
| vLLM | 14 | phase1 §3 |
| TGI (Text Generation Inference) | 14 | phase1 §3 |
| SGLang | 14 | phase1 §3 |
| Temperature (deep) | 15 | phase1 §4 |
| Top-P, Top-K, Min-P | 15 | phase1 §4 |
| Repetition penalty | 16 | phase1 §4 |
| Thinking / reasoning models (Qwen3) | 16 | phase1 §4 |
| HTTP client `health/chat/stream` | 17–20 | phase1 §5 |
| Env `LLM_BASE_URL` / cloud-compatible API | 20 | phase1 §5 |
| Mocked tests (CI without GPU) | 21 | phase1 §5 |
| LoRA / SFT / GGUF export | 105 | phase1 §6 |
| DPO / preference tuning | 📖 | phase1 §6 |
| Distillation (teacher → student) | 106 | phase1 §6 |

---

## Phase 2 — Context & RAG

| Topic | Day | Doc |
|-------|-----|-----|
| Versioned prompt files | 22 | [phase2 §1](./phase2.md) |
| JSON + Pydantic + retry | 24–25 | phase2 §1 |
| Extractor prompts | 26 | phase2 §1 |
| Prompt changelog | 27 | phase2 §1 |
| Golden sets | 29 | phase2 §2 |
| Baseline accuracy / adversarial | 30–31 | phase2 §2 |
| `prompt_version` tracing | 33 | phase2 §2 |
| Dense retrieval (embeddings) | 38 | phase2 §3 |
| Chroma | 38, 107 | phase2 §3 |
| Qdrant | 📖, 107 | phase2 §3 |
| pgvector | 📖, 107 | phase2 §3 |
| Pinecone | 📖 | phase2 §3 |
| Fixed-size chunking + overlap | 37 | phase2 §4 |
| Semantic chunking | 37, 108 | phase2 §4 |
| Parent-document retrieval | 108 | phase2 §4 |
| Sliding window chunking | 📖 | phase2 §4 |
| MMR (diversity) | 109 | phase2 §4 |
| Ingest CLI & persisted index | 40–41 | phase2 §4 |
| Retrieve + cite + refuse | 43–46 | phase2 §4 |
| RAG on/off comparison | 47 | phase2 §4 |
| Hybrid BM25 + dense | 50 | phase2 §5 |
| BGE-Reranker / Cohere Rerank | 51 | phase2 §5 |
| GraphRAG / entities | 52–53 | phase2 §6 |
| Neo4j / NetworkX | 53, 📖 | phase2 §6 |
| `rag_qa.jsonl` eval | 54–55 | phase2 §2 |

---

## Phase 3 — Tools & orchestration

| Topic | Day | Doc |
|-------|-----|-----|
| Tool registry & schemas | 57 | [phase3 §1](./phase3.md) |
| Tool-call loop | 58–59 | phase3 §1 |
| Sandboxed file tools | 60–61 | phase3 §1 |
| Tool traces / logging | 63 | phase3 §1 |
| Deny dangerous tools | 64 | phase3 §2 |
| Git read-only tool | 65 | phase3 §2 |
| MCP overview | 67 | phase3 §2 |
| Tool output truncation | 68 | phase3 §2 |
| Workflow state machine | 71–72 | phase3 §3 |
| Classify → RAG → draft pipeline | 73–75 | phase3 §3 |
| Checkpoints / durable steps | 76 | phase3 §3 |
| Human-in-the-loop approve | 80 | phase3 §3 |
| ReAct | 78 | phase3 §4 |
| Plan-and-execute | 99 | phase3 §4 |
| Reflection & self-correction | 100 | phase3 §4 |
| Tree-of-Thought (ToT) | 📖, 100 | phase3 §4 |
| DAG task decomposition | 71, 📖 | phase3 §3 |
| Hybrid workflow + agent | 81 | phase3 §4 |
| Short-term sliding context | 83 | phase3 §5 |
| Long-term episodic memory (vector) | 101 | phase3 §5 |
| LangGraph | 102 | phase3 §5 |
| CrewAI | 103 | phase3 §5 |
| OpenAI Agents SDK | 103 | phase3 §5 |
| AutoGen | 103 | phase3 §5 |

---

## Phase 4 — IDE & dev agents

| Topic | Day | Doc |
|-------|-----|-----|
| Cursor rules / `AGENTS.md` | 85 | [phase4](./phase4.md) |
| `.cursor/rules` (vs legacy `.cursorrules`) | 85 | phase4 §3 |
| Windsurf / `.windsurfrules` | 104 | phase4 §1 |
| GitHub Copilot / Workspace | 104 | phase4 §1 |
| Skills `SKILL.md` | 86–87 | phase4 §3 |
| Skill evals & versioning | 88, 90 | phase4 §3 |
| Skill router | 89 | phase4 §3 |
| Tool allowlist per skill | 90 | phase4 §3 |
| CLI agent (read-only → bounded bash) | 110 | phase4 §2 |
| Test-fix agent loop | 91, 110 | phase4 §4 |
| Git safety (no auto-push main) | 📖 | phase4 §2 |

---

## Phase 5 — Production

| Topic | Day | Doc |
|-------|-----|-----|
| `run_eval` + exit codes | 92 | [phase5](./phase5.md) |
| RAG eval in `run_all` | 93 | phase5 §4 |
| `history.csv` / `--tag` | 94 | phase5 §4 |
| Prompt injection defense | 95 | phase5 §3 |
| Secret redaction in logs | 95 | phase5 §3 |
| Output validation / policy filters | 95 | phase5 §3 |
| Pydantic (in pipeline) | 25, 92 | phase5 §2 |
| Outlines | 96 | phase5 §2 |
| Guidance | 96 | phase5 §2 |
| LangSmith | 97 | phase5 §1 |
| Arize Phoenix | 97 | phase5 §1 |
| Helicone | 97 | phase5 §1 |
| jsonl traces (lab minimum) | 83, 97 | phase5 §1 |
| E2B sandbox | 98 | phase5 §3 |
| Modal sandbox | 98 | phase5 §3 |
| LLM-as-judge (bias note) | 111 | phase5 §4 |
| Auth / Docker / rate limits | 112 | phase5 §5 |
| LoRA decision + baseline | 105 | phase1 §6 |

---

## Original lab extras (still covered)

| Topic | Day | Doc |
|-------|-----|-----|
| MCP tools (future) | 67 | phase3 |
| Capstone sprint | 113+ | [DAILY_30MIN](./DAILY_30MIN.md) |
| GitHub journal push | daily | [GITHUB](./GITHUB.md) |
| TOPIC_SEQUENCE order | — | [TOPIC_SEQUENCE](./TOPIC_SEQUENCE.md) |

---

## How to use

1. After each day, tick the row in your journal or copy this table to `docs/journal/COVERAGE-progress.md`.
2. Finish **Days 92–112** for 📖/🔜 items even if core path ended at Day 91.
3. Capstone should touch at least one topic from each phase section above.
