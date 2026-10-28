# Phase 5 — Production MLOps, guardrails & observability

**Days:** 92–112 · **After** [phase4.md](./phase4.md)

Complete all Phase 5 rows in [COVERAGE.md](./COVERAGE.md).

---

## 1. Observability & tracing (Day 97)

Log: execution graph, tokens/cost, tool latency, `prompt_version`, `run_id`.

| Tool | Role |
|------|------|
| **LangSmith** | LangGraph/LangChain traces |
| **Arize Phoenix** | OSS LLM observability |
| **Helicone** | Proxy analytics |

Lab minimum: `logs/traces/*.jsonl` + `evals/history.csv`.

---

## 2. Structured output (Days 25, 92, 96)

**Pydantic** (throughout pipeline), **Outlines**, **Guidance**, JSON schema in API when available.

---

## 3. Guardrails & security (Day 95)

- Prompt injection: untrusted RAG, delimiters, no obeying doc instructions
- **Secret redaction** in logs and traces
- Output validation, PII scan, tool allowlists

---

## 4. Sandboxing (Day 98)

**E2B**, **Modal** vs local deny-shell; untrusted model code never runs inline.

---

## 5. Evals & regression (Days 92–94, 111)

`run_eval`, `run_all`, `history.csv`, optional **LLM-as-judge** with bias documentation.

---

## 6. Deployment (Day 112)

Auth in front of `llama-server`, Docker, rate limits, queues for agent jobs, secrets in env.

---

## 7. Model adaptation (Day 105–106)

LoRA/SFT + eval compare; **distillation** survey — [phase1 §6](./phase1.md).

---

## Done when

- [ ] [COVERAGE.md](./COVERAGE.md) fully ✅ for Phases 0–5

---

## Related

[ROADMAP.md](./ROADMAP.md) · [journal/MILESTONES.md](../../learner/journal/MILESTONES.md)
