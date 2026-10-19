# Phase 4 — RAG (retrieval-augmented generation)

**Duration:** ~2 weeks (Days 43–56 in [DAILY_30MIN.md](./DAILY_30MIN.md))  
**Prerequisites:** [phase1.md](./phase1.md) (client), [phase2.md](./phase2.md) (prompt assembly)  
**Next:** [phase5.md](./phase5.md) — Agents & workflows

---

## Purpose

Answer questions using **your documents**, with **citations** and honest **“I don’t know”** when retrieval misses. RAG keeps facts in files and indexes—not in model weights (see [phase7.md](./phase7.md) for when training is appropriate).

---

## Core concepts

### Pipeline overview

```text
Documents → chunk → embed → index
                ↓
User query → embed → retrieve top-k chunks → prompt with context → LLM → answer + cites
```

### Chunking

Split long docs into overlapping segments (e.g. 500 characters, overlap 50).

| Too small | Too large |
|-----------|-----------|
| Loses context | Dilutes relevance; wastes context window |

Store metadata: `source` path, `chunk_id`, optional page/section.

### Embeddings

Map text to vectors so **similar meaning** is near in space.

| Approach | Tradeoff |
|----------|----------|
| Local embedding model | Offline, one more artifact to manage |
| API embeddings | Simple, sends text out |

Start simple (small local model or a single API) before optimizing.

### Vector store

Options: in-memory numpy, sqlite-vss, Chroma, LanceDB. Phase 4 goal is **understanding**, not picking the best database—pick the smallest thing that persists an index on disk.

### Retrieval

- **Top-k** — highest cosine similarity.
- **MMR** — diversify chunks (less redundancy).
- **Hybrid** — keyword (BM25) + vector when exact terms matter (SKUs, function names).

### Prompt assembly

```text
System: Answer only from context. Cite source paths. If insufficient, say you don't know.

Context:
[source: docs/README.md]
...chunk text...

User: {question}
```

### Failure modes (learn on purpose)

- Stale index after doc edits → re-run ingest.
- Wrong chunk size → irrelevant context.
- **Lost in the middle** — important info buried in long context; try reranking or fewer chunks.

---

## What you build

```text
data/
  corpus/              # md, notes, exports
  index/               # persisted vectors + metadata
tools/
  ingest/
    chunk.py
    embed.py
    build_index.py
  rag/
    retrieve.py
    answer.py          # answer_with_citations()
apps/
  ask_my_docs/
    cli.py             # ingest + ask
```

---

## Exercises

1. Chunk all files in `docs/` + personal notes.
2. Build and persist index; `ingest` CLI rebuilds it.
3. `retrieve(query)` returns top 5 with scores.
4. Answers include correct source paths on 3 known questions.
5. One unanswerable question → model refuses without hallucinating.
6. Compare same question with RAG off vs on.
7. Five-question manual eval with citation check.

---

## Done when

- [ ] `ask_my_docs` (or equivalent) CLI: ingest + one-shot question.
- [ ] Citations verified on a 5-question set you wrote.
- [ ] You can explain ingest vs query and when to re-index.

---

## RAG vs tools

Use **RAG** for static knowledge in documents. Use **tools** for live systems (git, APIs, calculators). Production apps often use both.

---

## Related docs

- [phase5.md](./phase5.md) — wire RAG into workflow steps
- [phase6.md](./phase6.md) — RAG regression evals
- [ROADMAP.md](./ROADMAP.md) — “Decide first” ladder
