# 30 minutes/day — step-by-step plan

**Companion:** [phases.md](./phases.md) (Phase 0–7 explainers) · [ROADMAP.md](./ROADMAP.md) · [README.md](./README.md) (start server)

**Default language:** Python 3.11+ (change any day to TypeScript if you prefer—keep one language for Days 8–60).

---

## Daily ritual (~30 min)

| Block | Time | Do this |
|-------|------|---------|
| **Warm-up** | 5 min | Re-read yesterday’s journal line; start server if needed (`docs/README.md`). |
| **Hands-on** | 22 min | Exactly one day’s task below—stop when the timer ends. |
| **Close-out** | 3 min | `docs/journal/YYYY-MM-DD.md`: one sentence *what I did*, one *what confused me*. Optional: commit & push ([GITHUB.md](./GITHUB.md)). |

**Rules**

- Miss a day → do **not** skip ahead two days; resume at the next number.
- Stuck &gt; 10 min → write the blocker in journal, do the “minimum” bullet for that day, move on.
- **Sunday (optional):** 30 min review only—re-run last week’s demo, update [MILESTONES](./journal/MILESTONES.md).

---

## Before Day 1

- [ ] Server works: `curl http://127.0.0.1:8080/health` → `{"status":"ok"}`
- [ ] Create folder: `docs/journal/`
- [ ] Pick capstone track from ROADMAP (you can change later)

---

## Week 1 — Runtime & API (Phase 0)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **1** | Start/stop server once. Run `/health` and `/v1/models`. In journal, define *token* and *context* in your own words. | Two curl outputs pasted in journal |
| **2** | Non-streaming chat with `curl` (README example). Save full JSON to `experiments/day02-response.json`. Note `usage` fields. | File saved |
| **3** | Streaming completion (`stream: true`). Watch tokens in terminal. Count roughly how many seconds to first token. | One-line timing in journal |
| **4** | Same question at `temperature` 0 vs 1 (if supported) or rephrase system prompt “be terse” vs “be verbose”. Compare. | Short comparison note |
| **5** | Send a prompt longer than ~3000 tokens (paste a long article). Observe truncate/error. Read `-c 4096` in README. | Know your context limit behavior |
| **6** | Read `docs/ROADMAP.md` “Decide first” table. For your capstone, write which row you’ll need first (RAG, workflow, etc.). | 3 bullets in journal |
| **7** | **Review:** Run Days 2–3 demos in &lt; 5 min without notes. Fix anything broken. | Clean demo |

---

## Week 2 — First client (Phase 1)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **8** | `mkdir -p tools/llm_client experiments`. `uv init` or `python -m venv .venv` + `pip install httpx`. | Project exists |
| **9** | `health()` → GET `/health`. Handle connection error with clear message. | `python -c "from tools.llm_client..."` works |
| **10** | `chat(messages)` → POST `/v1/chat/completions`, return assistant text. 30s timeout. | One-shot question works |
| **11** | `stream_chat(messages)` print deltas. | Streaming in terminal |
| **12** | Env vars: `LLM_BASE_URL` default `http://127.0.0.1:8080/v1`. | Document in `tools/llm_client/README.md` (5 lines) |
| **13** | Mock test: patch `httpx` so CI needs no server. One test file, one test. | `pytest` passes offline |
| **14** | **Review:** CLI `python experiments/01_hello_chat.py "hi"` using your client. | Demo |

---

## Week 3 — Prompts as code (Phase 2)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **15** | `tools/prompts/classify_v1.md` — system prompt: intent ∈ {question, task, chitchat}. | File committed |
| **16** | Call model; parse answer with regex or “first line only”. Log failures. | 5 manual test phrases in journal |
| **17** | Ask for **JSON only** `{ "intent": "...", "confidence": 0.0 }`. | Raw output saved |
| **18** | Add Pydantic model + `parse_json_from_llm()` with one retry on validation error. | Invalid JSON recovered once |
| **19** | `tools/prompts/extract_v1.md` — extract `{ "actions": ["..."] }` from a note. | 3 test notes |
| **20** | Version bump `classify_v2.md`; change one instruction; re-run same 5 phrases; note diffs. | Prompt changelog line |
| **21** | **Review:** `experiments/02_classify.py` reads stdin, prints JSON. | Script runs |

---

## Week 4 — Structured tasks & golden files (Phase 2)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **22** | `evals/sets/intent_golden.jsonl` — 10 lines `{input, expected_intent}`. | File exists |
| **23** | Script: run classifier on all 10; print accuracy %. | Baseline score in journal |
| **24** | Add 2 “adversarial” examples (ambiguous). Document wrong answers. | Notes |
| **25** | System prompt rule: “if unsure, intent=question, confidence&lt;0.5”. Re-score. | New accuracy |
| **26** | Read ROADMAP Phase 6 skim. Add `prompt_hash` or `prompt_version` to script output. | Traceable run |
| **27** | Capstone: write 5 real user messages you’d want your app to handle. | `data/capstone_samples.txt` |
| **28** | **Review:** Week 3–4 accuracy ≥ previous week or you know why not. | Journal |

---

## Week 5 — Tool loop (Phase 3)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **29** | `tools/registry.py`: `register(name, fn, json_schema)`. One tool: `add(a,b)`. | Registry works |
| **30** | Manual loop: you paste model JSON tool call → code runs → you paste result back. Learn the shape. | Diagram in journal |
| **31** | Implement `run_tool_loop()` max 5 steps with logging to `logs/traces/day31.jsonl`. | Trace file |
| **32** | Tool `read_file(path)` — only under `data/`, reject `..`. | Path test |
| **33** | Tool `list_dir(path)` same sandbox. | Two tools |
| **34** | Prompt: “use tools when needed.” Run: “what files are in data?” | Successful tool use |
| **35** | **Review:** Replay trace; explain each step aloud in 2 min. | Review done |

---

## Week 6 — Tools + safety (Phase 3)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **36** | Log tool name, args, duration, result length every call. | Structured logs |
| **37** | Deny list: `run_shell` not registered; model asks anyway → return error observation. | Safe failure |
| **38** | `git_status` read-only tool (subprocess `git -C repo status -sb`). | Real output |
| **39** | `apps/tool_runner/repl.py` — simple chat + print tool trace. | REPL session |
| **40** | Read MCP overview (ROADMAP resources). List 3 tools you’d expose via MCP later. | Journal bullets |
| **41** | Harden: max result size 8KB truncate with message. | Test truncate |
| **42** | **Review:** 3-turn conversation using ≥2 tools. | Demo |

---

## Week 7 — RAG ingest (Phase 4)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **43** | `data/corpus/` — copy `docs/*.md` + 2 personal notes. | Corpus folder |
| **44** | Chunker: 500 chars, overlap 50, store `{text, source, chunk_id}`. | `data/chunks.jsonl` |
| **45** | Pick embedding: local model or API; embed 10 chunks test. | Vectors exist |
| **46** | In-memory index: cosine top-3 for one query. | Print 3 sources |
| **47** | `tools/rag/ingest.py` CLI rebuild index. | One command ingest |
| **48** | Embed full corpus; save index to `data/index/` (pickle/sqlite/numpy). | Persisted index |
| **49** | **Review:** Re-ingest after editing one doc; confirm chunk count changes. | Verified |

---

## Week 8 — RAG answers (Phase 4)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **50** | `retrieve(query)` → top 5 chunks with scores. | Function done |
| **51** | Prompt template: context blocks + “cite source path”. | `answer_with_citations()` |
| **52** | Ask 3 questions answerable from corpus. Check citations correct. | 3 Q&A in journal |
| **53** | Ask 1 question **not** in corpus. Prompt: say “I don’t know”. | Honest refusal |
| **54** | Compare same question with RAG off vs on. | Comparison |
| **55** | `apps/ask_my_docs/cli.py` one-shot: `ask "..."`. | CLI |
| **56** | **Review:** 5-question mini eval; score citations manually. | Score % |

---

## Week 9 — Workflows (Phase 5)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **57** | Draw states: `RECEIVED → CLASSIFY → RETRIEVE → DRAFT → DONE` on paper/`docs/journal/`. | Diagram |
| **58** | `apps/agent_lab/workflow.py` — dataclass `RunState`, pure functions per step. | Code skeleton |
| **59** | CLASSIFY uses your Phase 2 JSON classifier. | Wired |
| **60** | RETRIEVE calls RAG if intent=question. | Wired |
| **61** | DRAFT calls `chat()` with retrieved context. | End-to-end dry run |
| **62** | Persist `checkpoints/{run_id}.json` after each step. | File per run |
| **63** | **Review:** Run twice; show two checkpoint files. | Demo |

---

## Week 10 — Agents & hybrid (Phase 5)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **64** | `agent_loop.py`: ReAct, max 8 steps, read-only tools only. | Agent runs |
| **65** | Task: “summarize all files in data/corpus/” via agent. | Markdown output |
| **66** | Add `human_approve` step in workflow before any `write_file` tool. | Gate works |
| **67** | Hybrid: workflow step calls `run_agent(goal=...)` returns JSON summary. | Handoff schema |
| **68** | Crash test: kill mid-run; resume from checkpoint (document limitation if not implemented). | Journal note |
| **69** | `logs/traces/` jsonl per session with `run_id`, `step`, `tokens`. | Trace |
| **70** | **Review:** Explain workflow vs agent for your capstone in 5 sentences. | Journal |

---

## Week 11 — Evals & observability (Phase 6)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **71** | `evals/run_eval.py` runs intent golden set; exits 1 if accuracy &lt; 80%. | Script |
| **72** | RAG eval: 5 questions, assert citation path substring. | 5 cases |
| **73** | Tag runs: `--tag day73`; append results to `evals/history.csv`. | History |
| **74** | One LLM-as-judge optional: “is citation relevant?” on 3 cases—note bias risk. | Short write-up |
| **75** | Before changing prompt, run eval; after change, run again. | Two scores |
| **76** | Read trace from Week 10; find longest step. | Optimization idea |
| **77** | **Review:** Single command `evals/run_all.sh` (or makefile target). | One command |

---

## Week 12 — Skills (Phase 8)

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **78** | `skills/classify-intent/SKILL.md` — frontmatter, steps, output schema. | Skill file |
| **79** | `skills/ask-docs-rag/SKILL.md` + link to ingest CLI. | Second skill |
| **80** | `skills/classify-intent/evals.yaml` — 5 cases. | Mini eval |
| **81** | Router: keyword or tiny prompt picks skill from user message. | `route(message)` |
| **82** | Skill invokes only allowed tools from registry. | Allowlist |
| **83** | Bump `skill_version`; re-run skill evals. | Version note |
| **84** | **Review:** Run router → skill → answer for 3 inputs. | Demo |

---

## Weeks 13–14 — Training optional (Phase 7)

Skip this block if Week 4 accuracy is already good enough for your task.

| Day | Hands-on (22 min) | Done signal |
|-----|-------------------|-------------|
| **85** | Export 50 best `(input, output)` rows from traces + golden set → `training/datasets/intent.jsonl`. | Dataset |
| **86** | Document baseline eval score in `training/README.md`. | Baseline |
| **87** | Follow one LoRA tutorial (Unsloth/MLX/HF)—**do not** finish train today; env ready only. | Env works |
| **88** | Train smallest run (1 epoch, tiny subset) OR simulate with notebook cells documented. | Artifact or notes |
| **89** | Read export GGUF path for your stack; list steps you’d run. | Checklist |
| **90** | Decision doc: train vs prompt for *your* capstone (1 page). | `docs/journal/training-decision.md` |
| **91** | **Review:** ROADMAP milestone checklist update. | MILESTONES.md |

---

## After Day 84 (or 91)

**Capstone sprint** (still 30 min/day):

1. **Week A:** Scope one feature from your capstone track; user story + acceptance tests.
2. **Week B:** Implement using workflow + RAG + skills you built.
3. **Week C:** Eval gate + README for users.
4. **Week D:** Polish; use it yourself 3 times; fix top annoyance.

---

## Quick reference — which phase?

| Days | Phase |
|------|--------|
| 1–7 | 0 — Server & API |
| 8–14 | 1 — Client |
| 15–28 | 2 — Prompts & structure |
| 29–42 | 3 — Tools |
| 43–56 | 4 — RAG |
| 57–70 | 5 — Workflows & agents |
| 71–77 | 6 — Evals |
| 78–84 | 8 — Skills |
| 85–91 | 7 — Training (optional) |

---

## Copy-paste: today’s journal template

```markdown
# YYYY-MM-DD — Day N

- **Time boxed:** 30 min
- **Did:**
- **Stuck:**
- **Tomorrow:** Day N+1
```

Save as `docs/journal/YYYY-MM-DD.md`.
