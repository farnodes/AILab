# Sync progress & guides to GitHub

This repo is meant to track **documentation, journal entries, and code you write**—not multi‑gigabyte models or `llama-server` binaries.

## What to commit

| Commit | Examples |
|--------|----------|
| **Yes** | `docs/**`, `README.md`, `experiments/*.json`, `tools/`, `apps/`, `evals/`, `skills/` |
| **Yes** | `docs/journal/*.md` — daily learning log |
| **No** | `.llama/` (see `.gitignore`) |
| **No** | `*.gguf`, `.env`, `data/index/`, large corpora under `data/` |

## Daily habit (after each 30 min session)

```bash
cd /Users/swetank/Farnodes/AI/Local

git status
git add docs/journal/YYYY-MM-DD.md experiments/   # whatever changed today
git commit -m "journal: day N — short description"
git push
```

Use a clear commit style:

- `journal: day 2 — chat completion curl + usage notes`
- `phase1: add llm_client with streaming`
- `docs: tweak phase4 RAG chunking notes`

## First-time setup

### 1. Initialize (already done if you cloned this repo)

```bash
cd /Users/swetank/Farnodes/AI/Local
git init   # skip if clone
```

### 2. Create GitHub repository

**Option A — GitHub CLI** (if `gh auth login` is done):

```bash
gh repo create local-ai-lab --private --source=. --remote=origin --push
```

Use a public repo instead: add `--public`.

**Option B — GitHub website**

1. [New repository](https://github.com/new) — name e.g. `local-ai-lab`, no README (you have one).
2. Then:

```bash
git remote add origin git@github.com:YOUR_USER/local-ai-lab.git
git branch -M main
git push -u origin main
```

### 3. Verify

Open the repo on GitHub; you should see `docs/DAILY_30MIN.md`, `docs/journal/`, and phase guides.

## Branching (optional)

- `main` — stable guides + your journal
- `feature/phase1-client` — bigger code changes, merge when tests pass

For solo learning, committing straight to `main` is fine.

## Milestones on GitHub

- Use [docs/journal/MILESTONES.md](./journal/MILESTONES.md) locally; tick phases in commits: `journal: complete phase 0 milestone`.
- Optional: [GitHub Issues](https://github.com/features/issues) per phase or capstone; close when eval passes.

## Security

- Never commit API keys, `.env`, or private documents in `data/corpus/`.
- Local `llama-server` has no API key by default—do not expose port 8080 to the internet without auth.
