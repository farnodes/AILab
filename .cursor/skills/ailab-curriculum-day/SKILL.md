---
name: ailab-curriculum-day
description: >-
  Authors and improves AILab curriculum days—chapter lesson, step exercises,
  submission Q&A, figures, and revision sync. Use when adding or editing days in
  curriculum/curriculum.json, docs/guides phase chapters, Day N content, exercises,
  Save locally submissionQuestions, infographics, or learner-facing explanations.
---

# AILab — curriculum day authoring

Maintain **one day** as three linked layers. The roadmap UI reads **`curriculum/curriculum.json` only** for steps; the chapter is the deep lesson.

| Layer | Path | Role |
|-------|------|------|
| **Chapter** | `docs/guides/phaseN.md` | Concepts, tables, samples, `![alt](images/foo.svg)` |
| **Day (canonical)** | `curriculum/curriculum.json` → `days[]` | Steps: explain → exercise → Q&A → close-out |
| **Day stub** | `curriculum/days/day-N.md` | GitHub-friendly summary; points at json + chapter |
| **Revision** | `docs/revision/` | Closed-book recall after the phase |
| **Daily plan row** | `docs/guides/DAILY_30MIN.md` | One-line hands-on + “done” artifact |

Schema reference: [curriculum/SCHEMA.md](../../../curriculum/SCHEMA.md).

---

## Non-negotiables

1. **Never rename or reuse** `day.id` or `step.id` inside a day — `learner/progress.json` keys off them.
2. **Repo-relative paths** in `links`, `figure`, `guide` — no `#` anchors (checker validates files only).
3. **Learner-private data** stays gitignored: `learner/progress.json`, `learner/submissions/**`, dated journals.
4. **Committed samples only** under `examples/` unless `.gitignore` says otherwise.
5. After curriculum edits: `python3 scripts/check_curriculum.py` must pass.
6. Bump `app/public/index.html` query strings (`app.js?v=`, `styles.css?v=`) only when changing `app/public/*.js` or CSS.

---

## Day arc (30-minute sitting)

Typical step sequence—adapt count, keep the **roles**:

| Order | Role | UI fields | Chapter |
|-------|------|-----------|---------|
| 1 | **Why today** | `body`, `why`, `links`, optional `figure`, `durationMinutes` | Matching section + “how days fit” |
| 2–n | **Hands-on** | `commands`, `outcome`, optional `figure`, optional `submission` | Procedure + failure table |
| n+1 | **Reflect / journal** | Short `body` + **`submissionQuestions`** + `progressSection` | Concept section only; Q&A in form |
| last | **Close-out** | `submissionQuestions` or recap `body` | Exit criteria |

**`summary`** on the day: outcomes + time honesty (e.g. first model pull 45–60 min).

**`reference`** (optional): `apiBase`, `model`, URLs shown on step 1.

**`guide`**: path to phase chapter (e.g. `docs/guides/phase0.md`).

---

## Writing style

- **Default:** direct, technical, short paragraphs; one concrete example where confusion is common (`connection refused` vs `model not found`).
- **Plain language:** only for non-obvious ideas (tokens, context window, streaming vs batch)—not for every step.
- **Avoid:** duplicate prose — do not repeat the same explanation in `body`, `journalGuide`, and chapter; prefer **one** place in the chapter + thin step `body` that points to it.
- **`journalGuide`:** use sparingly; label in UI is **Background**. Merge into `body` when possible.

---

## Step templates

Copy shapes from [templates.md](templates.md) and [Day 1 in curriculum.json](../../../curriculum/curriculum.json) (reference implementation).

### Command exercise

```json
{
  "id": "3",
  "title": "Exercise — …",
  "durationMinutes": 5,
  "body": "What to run and what success/failure looks like.",
  "why": "One line: why this belongs in the lab.",
  "commands": ["one line or grouped with \\"],
  "outcome": "Observable success check.",
  "figure": "docs/guides/images/….svg",
  "figureAlt": "One-line caption."
}
```

### Structured submission (preferred for journal / proof)

```json
{
  "submission": true,
  "progressSection": "Day N — topic",
  "submissionQuestions": [
    {
      "id": "stable-kebab-id",
      "label": "Question shown in UI",
      "hint": "Optional guidance; not the answer.",
      "input": "textarea",
      "rows": 3,
      "required": true,
      "minLength": 25,
      "mustContain": ["usage.prompt_tokens"],
      "mustContainHint": "Name both usage fields."
    }
  ]
}
```

- **`id`:** stable forever; used in `learner/submissions/day-N/step-M.json`.
- **`progressSection`:** must match `## …` in `learner/journal/PROGRESS.md` if sync desired.
- Validation runs **client + server**; **Mark step done** requires valid answers + **Save locally**.

Legacy single textarea: `submission: true` without `submissionQuestions` (avoid for new journal steps).

---

## Chapter (phase guide) updates

When a day teaches a new concept:

1. Add or extend a **## section** in `docs/guides/phaseN.md` (lesson depth).
2. Optional infographic: `docs/guides/images/*.svg` (valid UTF-8 XML), embed `![caption](images/file.svg)` in markdown.
3. Link from step `links` with label = section name; `path` = file only (`docs/guides/phase0.md`).
4. Update `docs/revision/phaseN-*.md` recall rows if it is exam-worthy.
5. Update `DAILY_30MIN.md` row for that day.

Keep **step ids** when rewriting copy in the chapter.

---

## Workflow: add or improve a day

```
- [ ] Read existing day in curriculum.json + chapter section + Day 1 as pattern
- [ ] Edit chapter first if concepts changed
- [ ] Edit curriculum steps (ids unchanged)
- [ ] Add submissionQuestions for every reflect/proof step
- [ ] Add PROGRESS.md ## heading if progressSection is new
- [ ] Update curriculum/days/day-N.md stub + DAILY_30MIN row
- [ ] python3 scripts/check_curriculum.py
- [ ] Spot-check UI: figures, Q&A validation, Save locally, mark done gate
```

### Bulk copy changes on one day

Prefer a **idempotent patch script** under `curriculum/scripts/patch_dayN_*.py` (see `patch_day1_submission_questions.py`) instead of hand-editing huge JSON strings in chat.

---

## Infographics

- Put SVGs in `docs/guides/images/`.
- Step card: `"figure": "docs/guides/images/foo.svg"` (repo root path).
- Chapter: relative `images/foo.svg` in markdown.
- Use for: architecture (two URLs), before/after, success vs error—not for glossary lists.

---

## UI / API (do not break)

| Feature | Location |
|---------|----------|
| Step render + Q&A | `app/public/app.js`, `app/public/submission.js` |
| Save answers | `PUT /api/submissions` → `learner/submissions/` |
| Progress checkmarks | `PATCH /api/progress` → `learner/progress.json` |
| Block submissions from git web | `/repo/` must not serve `learner/submissions/` |

---

## Quality bar (Day 1 level)

- Every **exercise** has `outcome` or submission proof.
- Every **journal step** uses `submissionQuestions` (not a blank textarea).
- **Close-out** checks recall of URLs, model id, and the day’s core terms.
- **Commands** grouped with trailing `\` in JSON; UI shows one copy icon per command.
- **No** capstone or future-phase requirements on Day 1 unless that day is capstone day.

---

## Additional resources

- Field-by-field templates and JSON examples: [templates.md](templates.md)
- Open-source layout: [CONTRIBUTING.md](../../../CONTRIBUTING.md), [OPEN.md](../../../OPEN.md)
