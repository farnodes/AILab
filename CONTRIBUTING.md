# Contributing to AILab

AILab is a shared learning roadmap. The website is how people learn and track progress. The curriculum files are how contributors add use cases and techniques.

## What belongs here

- A phase, day, or step another learner can follow on a laptop with Ollama.
- A short guide that explains why the step exists.
- A fix to the website, the curriculum checker, or the docs.

Personal checkmarks and dated journal notes stay in `learner/` and are not part of the shared history. See [learner/README.md](learner/README.md).

## Add a day or use case

1. Pick the phase in [curriculum/SCHEMA.md](curriculum/SCHEMA.md). Add a phase only when the idea is a new stage, not a single exercise.
2. Append a day to `curriculum/curriculum.json`. Keep existing `id` values. New days use the next `day-N`. New steps use new string ids. Learners’ progress files key off those ids.
3. Write the chapter in `docs/guides/` if the day needs more than the step text (new phase guide, or a section in the current one). Link it from the step `links` with a repo-relative path such as `docs/guides/phase2.md`.
4. Point exercise commands at `examples/…`. Commit a sample only when it helps the next person see a good result. Generated runs stay untracked (see `.gitignore`).
5. Run `python3 scripts/check_curriculum.py`.
6. Open `./lab-ui.sh` and click through the new day.

Stable ids matter more than pretty numbers. Do not renumber days that are already in the file.

## Pull requests

- One track or one fix per pull request.
- Say which learner job the change serves (a new use case, a clearer step, a broken link).
- Do not commit `learner/progress.json`, `.env`, model weights, or private documents.

Issues: use the “New track” template for a use case you want in the roadmap, and the bug template for the website.

## Local check

```bash
python3 scripts/check_curriculum.py
./lab-ui.sh
```

The site binds to `127.0.0.1:8765` unless you set `LAB_UI_HOST` and `LAB_UI_PORT`.
