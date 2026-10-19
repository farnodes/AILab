# Phase 2 — RAG & context engineering

**Days:** 22–56 (+ 107–109) · **Prerequisites:** [phase1.md](./phase1.md) · **Next:** [phase3.md](./phase3.md)

Read **§1 → §6** in order. Track every row in [COVERAGE.md](./COVERAGE.md).

| Block | Days |
|-------|------|
| 2A Context & evals | 22–35 |
| 2B RAG core | 36–49 |
| 2B Advanced retrieval | 50–56, 107–109 |

---

## 1. Context engineering (Days 22–28)

Versioned prompts, JSON, **Pydantic**, retry, classifier + extractor CLIs.

---

## 2. Golden sets & baseline eval (Days 29–35)

`intent_golden.jsonl`, accuracy, adversarial cases, `prompt_version`, capstone samples.

---

## 3. Embeddings & vector databases (Days 38, 107)

| Store | When |
|-------|------|
| **Chroma** | Local lab default |
| **Qdrant** | Filters, production |
| **pgvector** | Postgres already in stack |
| **Pinecone** | Managed cloud |

**Dense retrieval:** embed query + chunks, cosine similarity.

---

## 4. Chunking & RAG pipeline (Days 36–49, 108–109)

| Strategy | Notes |
|----------|--------|
| Fixed + overlap | Baseline (Day 37) |
| **Semantic** | Split on meaning boundaries |
| **Parent-document** | Small child chunks search; parent text to LLM |
| **Sliding window** | Long sequential text |
| **MMR** | Reduce redundant top-k (Day 109) |

Pipeline: ingest → chunk → embed → index → retrieve → (re-rank) → prompt → cite.

---

## 5. Hybrid search & re-ranking (Days 50–51)

**BM25 + dense** for SKUs, APIs, exact tokens.

**Re-rankers:** BGE-Reranker, Cohere Rerank — reorder top-k before LLM.

---

## 6. GraphRAG & knowledge graphs (Days 52–56)

Entities/relations from docs; **NetworkX** (lab) or **Neo4j** (prod); combine with vector hits for multi-hop questions.

---

## Done when

- [ ] [COVERAGE.md](./COVERAGE.md) Phase 2 rows ✅
- [ ] Classify + RAG demo with citations

---

## Related

[phase3.md](./phase3.md) · [phase5.md](./phase5.md)
