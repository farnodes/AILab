# Phase 2 — Prompting & structured logic

**Duration:** ~2 weeks (Days 15–28 in [DAILY_30MIN.md](./DAILY_30MIN.md))  
**Prerequisites:** [phase1.md](./phase1.md)  
**Next:** [phase3.md](./phase3.md) — Tools & side effects

---

## Purpose

Turn prompts into **versioned, testable artifacts**. The model returns text; your application needs **reliable structure** (JSON, labels, extracted fields). Phase 2 is where “AI logic” starts to look like normal software: schemas, validators, retries, golden files.

---

## Core concepts

### System prompt vs user content

- **System:** stable instructions (“you classify intent”, “output JSON only”).
- **User:** variable input per request.
- **Few-shot examples** in system or user messages teach format without training.

### Sampling parameters

| Param | Effect |
|-------|--------|
| `temperature` | Higher → more random; lower → more deterministic |
| `top_p` | Nucleus sampling; alternative to temperature |
| `max_tokens` | Cap on completion length |

For classification and extraction, prefer **low temperature** and strict format instructions.

### Structured output patterns

1. **JSON in the reply** — instruct “no markdown, valid JSON only”.
2. **Delimited blocks** — e.g. XML tags `<result>...</result>` for easier parsing.
3. **Schema in the prompt** — paste field names and types.

The model can still violate the contract—**never trust without validation**.

### Parse → validate → retry

```text
LLM text → extract JSON → Pydantic/Zod validate
                ↓ fail
         retry once with error message in user message
```

This loop is cheaper and more reliable than hoping the next model version fixes formatting.

### Prompt versioning

Files like `tools/prompts/classify_v1.md`, `classify_v2.md`. Changelog one line per version. Tie eval scores to `prompt_version` (Phase 6).

### Model-specific notes (Qwen3)

Some models emit long “reasoning” unless disabled or instructed for concise final answers. If outputs are noisy, adjust system prompt or check model card for thinking/reasoning flags.

---

## What you build

```text
tools/
  prompts/
    classify_v1.md
    extract_v1.md
  structured/
    parse.py           # parse_json_from_llm, retry helper
    schemas.py         # Pydantic models
experiments/
  02_classify.py
  03_extract_entities.py
evals/
  sets/
    intent_golden.jsonl   # start of eval culture (full runner in Phase 6)
```

**Example tasks**

| Task | Output schema |
|------|----------------|
| Intent classifier | `{ "intent": "...", "confidence": float }` |
| Action extractor | `{ "actions": ["..."] }` |

---

## Exercises

1. Classifier with three intents; manual test 5 phrases.
2. JSON-only output + Pydantic validation.
3. One automatic retry on validation failure.
4. Second prompt template (extractor) with 3 test notes.
5. `classify_v2.md` — change one rule; compare on same inputs.
6. Golden file: 10 labeled examples; script prints accuracy %.

---

## Done when

- [ ] At least **two** prompt templates in `tools/prompts/`.
- [ ] Parser + validator + optional retry wired to Phase 1 `chat()`.
- [ ] Golden set with a baseline accuracy number in your journal.

---

## Anti-patterns

- Huge prompts copied into code strings — use files.
- Parsing with brittle regex on natural language when JSON was requested.
- No baseline metrics before “improving” the prompt.

---

## Related docs

- [phase3.md](./phase3.md) — when the model must *act*, not only reply
- [phase6.md](./phase6.md) — formal eval runner
