# Phase 5 — Production (revision)

**Days 92–112** · Guide: [phase5.md](../guides/phase5.md)

---

## Big picture

**Measure** (eval CI), **observe** (traces), **constrain** (Outlines/Guidance/Pydantic), **defend** (injection, redaction), **isolate** (E2B/Modal), **deploy** (auth, Docker).

---

## Must remember

| Topic | Recall |
|-------|--------|
| **Evals** | Golden sets; `run_eval` fails on regression; `history.csv`. |
| **Tracing** | jsonl minimum; LangSmith / Phoenix / Helicone. |
| **Guardrails** | Untrusted RAG; no secrets in logs; tool allowlists. |
| **Sandbox** | Never run model code inline on host. |
| **LoRA** | Only with before/after metrics; facts stay in RAG. |

---

## Phase 5 exit check

[COVERAGE.md](../guides/COVERAGE.md) all ✅; capstone with eval gate.
