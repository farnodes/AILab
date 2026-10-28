# Day 1 — Ollama & API

> **Use the web UI:** `./lab-ui.sh` → http://127.0.0.1:8765  
> Progress is stored in [learner/progress.json](../../learner/progress.json), not in this file.  
> Exercise answers: **Save locally** on the step → [learner/submissions/](../../learner/submissions/) (gitignored, never pushed).

**Phase:** 0 Bootstrap · **Time box:** ~30 minutes (first `lfm3` pull may take 45–60 min)

**No chat curl today** — Day 2 sends `POST /v1/chat/completions`.

## Steps (canonical list in [curriculum.json](../curriculum.json))

1. Why Day 1 — two URLs on port 11434, model id `lfm3`
2. Exercise — `./server.sh` (Ollama up, pull, warm)
3. Exercise — `ollama list` (NAME column → JSON `"model"`)
4. Exercise — `GET /api/tags` + save proof locally
5. Reflect — tokens (Save locally → syncs **Day 1 — tokens** in PROGRESS.md)
6. Reflect — context window (Save locally)
7. Close out — four lines in your own words (Save locally)

**Lesson:** [Phase 0 chapter](../../docs/guides/phase0.md) — “The two URLs”, “A token”, “The context budget”.
