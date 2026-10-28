# AILab

Open roadmap for learning AI on your own machine. You follow phases in a local website, mark steps as you go, and keep that progress on your computer. Other people extend the same roadmap when a new use case or technique is worth teaching.

**Repository:** [github.com/farnodes/AILab](https://github.com/farnodes/AILab)

## Start learning

```bash
./server.sh     # Ollama + lfm3  →  http://127.0.0.1:11434/v1
./lab-ui.sh     # roadmap site   →  http://127.0.0.1:8765
```

Then open [OPEN.md](OPEN.md). The daily plan is [docs/guides/DAILY_30MIN.md](docs/guides/DAILY_30MIN.md). Phase map: [docs/guides/phases.md](docs/guides/phases.md).

You need [Ollama](https://ollama.com/download) and Python 3. The website uses the Python standard library only.

## How progress works

The shared curriculum is [curriculum/curriculum.json](curriculum/curriculum.json). Your checkmarks are [learner/progress.json](learner/progress.json). That file is created on first run and is not part of the shared repo, so your place in the roadmap stays on your machine when you pull other people’s tracks.

## Add a track or use case

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [curriculum/SCHEMA.md](curriculum/SCHEMA.md). A new day is a block in `curriculum.json` plus a guide under `docs/guides/` when the idea needs a written chapter.

```bash
python3 scripts/check_curriculum.py
```

## Layout

| Path | Who edits it | What it is |
|------|----------------|------------|
| `app/` | website changes | Local roadmap UI and API |
| `curriculum/` | anyone adding a day or phase | Steps learners see in the UI |
| `docs/guides/` | anyone adding a chapter | Phase guides, daily plan, coverage |
| `docs/revision/` | chapter authors | Short recap after a phase |
| `docs/README.md` | runtime changes | How to start Ollama |
| `examples/` | exercise output | Sample responses; your other runs stay local |
| `learner/` | you, on your machine | Progress JSON and journal |
| `scripts/` | tooling | Model startup, UI, curriculum check |

## License

[MIT](LICENSE)
