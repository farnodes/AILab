# Farnodes AI Lab — Roadmap

Local-first curriculum: run **small language models (SLMs)** on your machine, then stack **RAG, agents, IDE workflows, and production guardrails**.

**Server:** [README.md](./README.md) — Qwen3 via `llama-server` at `http://127.0.0.1:8080/v1`  
**Daily practice:** [DAILY_30MIN.md](./DAILY_30MIN.md)  
**Topic order:** [TOPIC_SEQUENCE.md](./TOPIC_SEQUENCE.md) · **Full checklist:** [COVERAGE.md](./COVERAGE.md)  
**Phase deep dives:** [phases.md](./phases.md)

---

## Curriculum overview

| Phase | Guide | You master |
|-------|--------|------------|
| **0** | [phase0.md](./phase0.md) | Bootstrap: server, tokens, OpenAI-compatible API |
| **1** | [phase1.md](./phase1.md) | **Local AI execution & SLMs** — quantization, runtimes, sampling, serving |
| **2** | [phase2.md](./phase2.md) | **RAG & context engineering** — embeddings, chunking, hybrid search, GraphRAG |
| **3** | [phase3.md](./phase3.md) | **Multi-agent architectures & orchestration** — ReAct, memory, LangGraph-class patterns |
| **4** | [phase4.md](./phase4.md) | **Agentic developer tooling & IDE workflows** — Cursor, rules, autonomous coding loops |
| **5** | [phase5.md](./phase5.md) | **Production MLOps, guardrails & observability** — tracing, JSON enforcement, sandboxing |

```text
phase0 (bootstrap)
    → phase1 SLMs & serving
    → phase2 RAG & context
    → phase3 agents & orchestration
    → phase4 IDE & dev agents
    → phase5 production hardening
```

**Optional depth:** model adaptation (SFT/LoRA) lives in [phase1.md](./phase1.md#optional-model-adaptation) and [phase5.md](./phase5.md#evals-and-regression); skills packaging in [phase4.md](./phase4.md#skills-and-repo-instructions).

---

## North star outcomes

1. Choose **quantization and runtime** for a memory budget and latency target.
2. Build **enterprise-grade RAG** (hybrid retrieval, re-ranking, context pipelines).
3. Design **multi-agent systems** with state, tools, and human-in-the-loop.
4. Use **AI-native IDE/CLI** workflows safely on real repos.
5. Ship with **observability, guardrails, and sandboxed execution**.

**Capstone tracks** (pick one):

| Track | Idea |
|-------|------|
| Dev platform | RAG over your repos + agent that runs tests and opens PRs with guardrails |
| Knowledge product | Hybrid RAG + GraphRAG Q&A with citations |
| Automation | Multi-agent workflow: classify → retrieve → draft → approve → act |
| Learning lab | 30-min curriculum you extend (this repo) |

---

## Decide first: prompt vs RAG vs train vs workflow vs agent

| Need | Try first | Then | Last resort |
|------|-----------|------|-------------|
| Facts from docs | Chunking + hybrid RAG | Re-ranker, GraphRAG | Fine-tune *style*, not facts |
| Reliable JSON | Schema + Pydantic/Outlines | Few-shot in prompt | SFT on format examples |
| New capability | Tool + MCP | Skill / rules file | Train tool-calling (rare) |
| Business process | **Workflow graph** (LangGraph) | Agent inside one node | Full autonomous pipeline |
| IDE behavior | `.cursor/rules`, skills | RAG on codebase | — |

**Facts → retrieval & tools. Process → workflows. Habits → prompts, then LoRA.**

---

## Phase summaries

### Phase 0 — Bootstrap

Server up, health checks, tokens, context window. *~1 week.*  
→ [phase0.md](./phase0.md)

### Phase 1 — Local AI execution & SLMs

Quantization (GGUF, EXL2, AWQ, GPTQ), VRAM budgeting, llama.cpp / Ollama / LM Studio, intro to vLLM/TGI/SGLang, sampling and thinking-model tuning. Code client against local `/v1`.  
→ [phase1.md](./phase1.md)

### Phase 2 — RAG & context engineering

**Order:** structured prompts & golden evals → RAG ingest/query → hybrid, re-rank, GraphRAG.  
→ [phase2.md](./phase2.md)

### Phase 3 — Multi-agent architectures & orchestration

**Order:** tools & MCP → workflows & checkpoints → ReAct agents & hybrid.  
→ [phase3.md](./phase3.md)

### Phase 4 — Agentic developer tooling & IDE workflows

Cursor, Windsurf, Copilot-style flows, CLI coding agents, rules files, test-fix loops, skills.  
→ [phase4.md](./phase4.md)

### Phase 5 — Production MLOps, guardrails & observability

LangSmith / Phoenix / Helicone-style tracing, Pydantic/Outlines/Guidance, injection defense, E2B/Modal sandboxes, eval gates.  
→ [phase5.md](./phase5.md)

---

## Repo layout (evolves with you)

```text
Local/
├── docs/           Guides, journal, roadmap
├── experiments/    Day exercises
├── tools/          Clients, RAG, agents
├── apps/           Demos & capstone
├── evals/          Golden sets & runners
├── skills/         SKILL.md bundles (phase 4)
├── training/       Optional LoRA datasets (phase 1 / 5)
└── .llama/         Local binaries (gitignored)
```

---

## Milestones

Track in [journal/MILESTONES.md](./journal/MILESTONES.md).

- [ ] Phase 0: Server + API literacy
- [ ] Phase 1: Quantization choice + local serve + tuned sampling
- [ ] Phase 2: Hybrid RAG with re-rank + citations
- [ ] Phase 3: Stateful multi-step agent with tools
- [ ] Phase 4: IDE/rules workflow on a real repo
- [ ] Phase 5: Traces + guardrails + eval CI
- [ ] Capstone shipped

---

## Resources

- [llama.cpp](https://github.com/ggml-org/llama.cpp) · [Ollama](https://ollama.com) · [vLLM](https://github.com/vllm-project/vllm) · [SGLang](https://github.com/sgl-project/sglang)
- [LangGraph](https://github.com/langchain-ai/langgraph) · [CrewAI](https://www.crewai.com) · [MCP](https://modelcontextprotocol.io)
- [Qdrant](https://qdrant.tech) · [pgvector](https://github.com/pgvector/pgvector)
- [Anthropic: building effective agents](https://www.anthropic.com/research/building-effective-agents)
- [Cursor docs](https://cursor.com/docs) — rules & agent skills

---

## What to do next

1. [DAILY_30MIN.md](./DAILY_30MIN.md) — continue Day 2+ (mapped to new phases in that file).
2. Read [phase1.md](./phase1.md) when starting Week 2.
3. Push journal to [GitHub](./GITHUB.md): `swetank01/local-ai-lab`.
