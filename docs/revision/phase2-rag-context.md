# Phase 2 — RAG & context (revision)

**Days 22–56** · Guide: [phase2.md](../guides/phase2.md)

---

## Big picture

First **shape** outputs (prompts, JSON, evals), then **retrieve** facts (embeddings, hybrid search, re-rank, optional graph)—never rely on weights for changing facts.

---

## Must remember

| Topic | Recall |
|-------|--------|
| **Context engineering** | Versioned prompts; Pydantic + retry; golden sets. |
| **Chunking** | Fixed, semantic, parent-doc, sliding window. |
| **Vector DBs** | Chroma (lab), Qdrant, pgvector, Pinecone. |
| **Hybrid** | BM25 + dense for exact tokens + meaning. |
| **Re-rank** | BGE / Cohere on top-k before LLM. |
| **RAG prompt** | Cite sources; say “I don’t know” if context weak. |
| **GraphRAG** | Entities/edges + vectors for multi-hop. |

---

## Phase 2 exit check

Classify + ask-docs with citations; hybrid or rerank decision documented.
