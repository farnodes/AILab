# 30 minutes/day — step-by-step plan

**Companion:** [COVERAGE.md](./COVERAGE.md) (all topics ✅) · [TOPIC_SEQUENCE.md](./TOPIC_SEQUENCE.md) · [phases.md](./phases.md) · [ROADMAP.md](./ROADMAP.md)

Topics follow **Phase 0 → 1 → 2 → 3 → 4 → 5**: bootstrap → SLM & client → context & RAG → tools & orchestration → IDE → production.

**Default language:** Python 3.11+

---

## Daily ritual (~30 min)

| Block | Time | Do this |
|-------|------|---------|
| **Warm-up** | 5 min | Read [PROGRESS.md](../../learner/journal/PROGRESS.md); `./server.sh` if needed. |
| **Hands-on** | 22 min | One day below—stop when timer ends. |
| **Close-out** | 3 min | Journal + update [PROGRESS.md](../../learner/journal/PROGRESS.md); optional [push](../../CONTRIBUTING.md). |

---

## Before Day 1

- [ ] Model ready: `./server.sh` (first pull of `lfm3` may take **45–60 min**; later runs ~30 min)
- [ ] `learner/journal/` exists (copy `PROGRESS.md` if you are starting fresh)
- [ ] Roadmap UI: `./lab-ui.sh` → http://127.0.0.1:8765

---

## Before Day 6

- [ ] Skim capstone tracks in [ROADMAP](./ROADMAP.md) — you pick a track on Day 6

---

## Phase 0 — Bootstrap (Days 1–7)

| Day | Topic | Hands-on (22 min) | Done |
|-----|--------|-------------------|------|
| **1** | Ollama & API | `ollama list`; `curl /api/tags`; token & context via **Save locally** (gitignored) | Journal |
| **2** | Chat JSON | `POST /v1/chat/completions` model `lfm3`; save `examples/day02-response.json` | File |
| **3** | Streaming | `stream: true`; time to first token | Timing note |
| **4** | Sampling preview | Terse vs verbose system prompt (temp 0 vs 1 if supported) | Compare |
| **5** | Context limit | Tiny prompt, then the MAGICEND long prompt | You saw miss or error |
| **6** | Roadmap | “Decide first” table + capstone needs | 3 bullets |
| **7** | Review | Repeat Days 2–3 in &lt; 5 min | Demo |

→ [phase0.md](./phase0.md)

---

## Phase 1 — SLMs & client (Days 8–21)

| Day | Topic | Hands-on (22 min) | Done |
|-----|--------|-------------------|------|
| **8** | GGUF & quantization | Read [phase1 §1](./phase1.md); journal: GGUF vs AWQ/GPTQ vs EXL2 | Table |
| **9** | Quant in practice | Why Q4_K_M-style quants matter for ~1.7B SLMs; disk vs quality | Note |
| **10** | Memory budget | Formula `Params×Bits/8`; estimate 1.7B Q4 vs 7B Q4 | Numbers |
| **11** | KV-cache | How `-c 4096` adds RAM beyond weights | Paragraph |
| **12** | llama.cpp | Re-read [README](../README.md) flags; one flag you hadn’t tried | Note |
| **13** | Ollama deep dive | You use `ollama run lfm3`; journal: API port, model list, vs raw llama.cpp | Compare |
| **14** | Prod engines | Journal: when teams use vLLM / TGI / SGLang | 1 paragraph each |
| **15** | Top-P / Top-K / Min-P | Same prompt, two settings via `curl` or client | Saved outputs |
| **16** | LFM3 sampling | Tune temperature / repeat penalty if outputs loop (Liquid defaults) | Fix note |
| **17** | Client setup | `mkdir -p tools/llm_client experiments`; venv + `httpx` | Project |
| **18** | `health()` | GET `/health`; clear error if down | Works |
| **19** | `chat()` | POST completions; 30s timeout | One-shot OK |
| **20** | `stream_chat()` + env | Streaming; `LLM_BASE_URL` in mini README | Stream OK |
| **21** | Tests & review | Mock `httpx` pytest; `examples/01_hello_chat.py` | Demo |

→ [phase1.md](./phase1.md)

---

## Phase 2A — Context engineering (Days 22–35)

| Day | Topic | Hands-on (22 min) | Done |
|-----|--------|-------------------|------|
| **22** | Prompt files | `tools/prompts/classify_v1.md` intents | File |
| **23** | Parse v1 | 5 manual phrases; log parse failures | Journal |
| **24** | JSON output | `{intent, confidence}` only | Raw saved |
| **25** | Pydantic + retry | `parse_json_from_llm()` one retry | Recovered once |
| **26** | Extractor prompt | `extract_v1.md` → actions list; 3 notes | 3 tests |
| **27** | Prompt versioning | `classify_v2.md`; changelog; re-run 5 phrases | Diff note |
| **28** | Classify CLI | `examples/02_classify.py` stdin → JSON | Runs |
| **29** | Golden set | `evals/sets/intent_golden.jsonl` × 10 | File |
| **30** | Baseline accuracy | Script scores 10; % in journal | Score |
| **31** | Adversarial cases | +2 ambiguous; document errors | Notes |
| **32** | Low-confidence rule | Re-prompt rule; re-score | New score |
| **33** | Trace version | `prompt_version` on eval output | Traceable |
| **34** | Capstone samples | `data/capstone_samples.txt` × 5 | File |
| **35** | Review | Week 22–34; accuracy trend | Journal |

→ [phase2.md](./phase2.md) §1–2

---

## Phase 2B — RAG (Days 36–56)

| Day | Topic | Hands-on (22 min) | Done |
|-----|--------|-------------------|------|
| **36** | Corpus | `data/corpus/` ← `docs/*.md` + 2 notes | Folder |
| **37** | Chunking strategies | Fixed 500/overlap 50 → `chunks.jsonl`; journal: semantic, parent-doc, sliding window | Chunks + table |
| **38** | Embeddings & vector DBs | Embed 10 chunks; journal: Chroma vs Qdrant vs pgvector vs Pinecone | Vectors + compare |
| **39** | Vector search | Cosine top-3 one query | 3 sources |
| **40** | Ingest CLI | `tools/rag/ingest.py` rebuild | Command |
| **41** | Persist index | Save under `data/index/` | Index |
| **42** | Ingest review | Edit doc; re-ingest; count Δ | Verified |
| **43** | `retrieve()` | Top 5 + scores | Function |
| **44** | Citations prompt | `answer_with_citations()` template | Template |
| **45** | Answerable Qs | 3 Q&A with correct source paths | Journal |
| **46** | Refusal | 1 OOD question → “don’t know” | Honest |
| **47** | RAG on/off | Same Q with/without retrieval | Compare |
| **48** | Ask CLI | `apps/ask_my_docs/cli.py` | CLI |
| **49** | RAG mini-eval | 5 Qs; manual citation score % | Score |
| **50** | Hybrid search | Add BM25 or keyword fallback (simple) | Hybrid |
| **51** | Re-rank | Skim BGE/Cohere rerank; try or document skip | Note |
| **52** | GraphRAG intro | Read phase2 §Graph; list entities from 1 doc | Entity list |
| **53** | Graph stretch | NetworkX edges optional OR journal plan | Plan |
| **54** | `rag_qa.jsonl` | 5 eval cases for RAG | File |
| **55** | Wire RAG eval | Script checks citation substring | Script |
| **56** | Phase 2 review | Demo: classify + ask docs | Demo |

→ [phase2.md](./phase2.md) §3–6

---

## Phase 3A — Tools (Days 57–70)

| Day | Topic | Hands-on (22 min) | Done |
|-----|--------|-------------------|------|
| **57** | Registry | `register()` + `add(a,b)` | Works |
| **58** | Tool shape | Manual paste loop; diagram in journal | Diagram |
| **59** | `run_tool_loop()` | Max 5 steps; `logs/traces/day59.jsonl` | Trace |
| **60** | `read_file` | Sandbox under `data/`; block `..` | Test |
| **61** | `list_dir` | Same sandbox | 2 tools |
| **62** | Tool use chat | “What files in data?” | Success |
| **63** | Structured logs | Name, args, duration, result len | Logs |
| **64** | Deny shell | Unregistered tool → error observation | Safe |
| **65** | `git_status` | Read-only subprocess | Real output |
| **66** | REPL | `apps/tool_runner/repl.py` + trace | Session |
| **67** | MCP | Read MCP docs; 3 future tools | Bullets |
| **68** | Truncate | Max 8KB tool result | Test |
| **69** | Multi-tool | 3-turn, ≥2 tools | Demo |
| **70** | Review | Replay trace aloud | Done |

→ [phase3.md](./phase3.md) §1–2

---

## Phase 3B — Orchestration (Days 71–84)

| Day | Topic | Hands-on (22 min) | Done |
|-----|--------|-------------------|------|
| **71** | Workflow diagram | `CLASSIFY→RETRIEVE→DRAFT→DONE` | Drawing |
| **72** | `RunState` | `apps/agent_lab/workflow.py` skeleton | Code |
| **73** | Classify step | Wire Phase 2 classifier | Wired |
| **74** | Retrieve step | RAG if intent=question | Wired |
| **75** | Draft step | `chat()` + context | E2E dry run |
| **76** | Checkpoints | `checkpoints/{run_id}.json` per step | Files |
| **77** | Workflow review | Two runs, two checkpoints | Demo |
| **78** | ReAct agent | `agent_loop.py` max 8; read-only tools | Runs |
| **79** | Research task | Summarize `data/corpus/` | Markdown |
| **80** | Human approve | Gate before `write_file` | Gate |
| **81** | Hybrid | Workflow calls `run_agent()` → JSON | Handoff |
| **82** | Crash test | Kill mid-run; resume or document gap | Note |
| **83** | Session traces | jsonl: `run_id`, step, tokens | Trace |
| **84** | Review | Workflow vs agent — 5 sentences | Journal |

→ [phase3.md](./phase3.md) §3–5

---

## Phase 4 — IDE & skills (Days 85–91)

| Day | Topic | Hands-on (22 min) | Done |
|-----|--------|-------------------|------|
| **85** | Project rules | `.cursor/rules` or `AGENTS.md` for this repo | Committed |
| **86** | Skill 1 | `skills/classify-intent/SKILL.md` | File |
| **87** | Skill 2 | `skills/ask-docs-rag/SKILL.md` | File |
| **88** | Skill evals | `evals.yaml` × 5 cases | Cases |
| **89** | Router | `route(message)` → skill | Router |
| **90** | Tool allowlist | Skill → registry subset | Allowlist |
| **91** | IDE review | Router → skill → answer × 3; test-fix loop journal | Demo |

→ [phase4.md](./phase4.md)

---

## Phase 5 — Production (Days 92–112)

Complete [COVERAGE.md](./COVERAGE.md) rows for Phase 5 + any 📖 gaps from Phases 1–4.

| Day | Topic | Hands-on (22 min) | Done |
|-----|--------|-------------------|------|
| **92** | Eval CI | `run_eval.py`; exit 1 if intent accuracy &lt; 80% | Script |
| **93** | RAG in CI | `run_all` includes `rag_qa.jsonl` | Wired |
| **94** | Regression history | `evals/history.csv` + `--tag` | CSV |
| **95** | Guardrails | Injection defense + secret redaction checklist for capstone | Doc |
| **96** | Outlines / Guidance | Read docs; optional: constrain JSON generation one experiment | Note |
| **97** | Observability | LangSmith + Phoenix + Helicone skim; standardize jsonl trace fields | Note |
| **98** | Sandboxes | E2B vs Modal vs local deny-shell — when to use | Note |
| **99** | Plan-and-execute | Planner lists steps; executor uses your tools (mini script) | Demo |
| **100** | Reflection | Agent critiques draft; one revision pass max | Demo |
| **101** | Episodic memory | Store tool-result summaries in vector store; recall in new thread | Demo |
| **102** | LangGraph | Official quickstart skim; map to your workflow.py | Journal |
| **103** | Multi-framework | CrewAI vs Agents SDK vs AutoGen — 1 paragraph each | Compare |
| **104** | IDE compare | Windsurf / Copilot vs Cursor; rules file formats | Journal |
| **105** | LoRA optional | `training/README` baseline + train/skip decision | Doc |
| **106** | Distillation | Read teacher→student; journal fit for your capstone | Note |
| **107** | Vector DB depth | Chroma → Qdrant or pgvector migration plan | Plan |
| **108** | Advanced chunking | Parent-document or semantic chunk on one file | Experiment |
| **109** | MMR retrieval | Diversify top-k vs plain cosine on one query | Compare |
| **110** | CLI coding agent | Bounded bash allowlist; run tests; no auto-push | Session |
| **111** | LLM-as-judge | 3 RAG cases judged; document bias risk | Write-up |
| **112** | Deploy survey | Auth in front of server, Docker, rate limits | Checklist |

→ [phase5.md](./phase5.md) · Full matrix: [COVERAGE.md](./COVERAGE.md)

---

## Capstone sprint (after Phase 5)

1. Scope + acceptance tests  
2. Build with workflow + RAG + skills  
3. Eval gate in README  
4. Use 3×; fix top annoyance  

---

## Quick reference

| Days | Phase | Topics |
|------|-------|--------|
| 1–7 | 0 | Bootstrap |
| 8–21 | 1 | Quant, runtimes, sampling, **client** |
| 22–35 | 2A | Prompts, JSON, golden eval |
| 36–56 | 2B | RAG, hybrid, graph stretch |
| 57–70 | 3A | Tools, MCP, safety |
| 71–84 | 3B | Workflow, agent, hybrid |
| 85–91 | 4 | Rules, skills, router |
| 92–112 | 5 + gaps | Eval, guardrails, frameworks, memory, deploy — [COVERAGE.md](./COVERAGE.md) |

---

## Journal template

```markdown
# YYYY-MM-DD — Day N (Phase X — topic)

- **Time boxed:** 30 min
- **Did:**
- **Stuck:**
- **Tomorrow:** Day N+1
```
