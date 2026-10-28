# Curriculum schema

Source of truth: [curriculum.json](curriculum.json). The website reads this file only. Markdown under `curriculum/days/` is a short mirror for people who want a file per day; the UI does not read those files.

## Top level

| Field | Meaning |
|-------|---------|
| `version` | Schema version. Stay on `1` until a breaking change is agreed. |
| `title`, `subtitle` | Shown in the roadmap header. |
| `phases` | Ordered stages. `phase` is an integer, `name` is the short label. |
| `resources` | Sidebar links. `id`, `label`, `path` (repo-relative file). |
| `days` | The learning sequence. |

## A day

| Field | Meaning |
|-------|---------|
| `id` | Stable key, `day-1`, `day-2`, … Never reuse or rename. |
| `number` | Display order. |
| `title`, `summary` | What this sitting is for. |
| `phase` | Must match a `phases[].phase`. |
| `phaseLabel` | Same name as that phase, for the sidebar. |
| `timeBoxMinutes` | Default 30. |
| `resources` | Ids from the top-level `resources` list. |
| `guide` | Optional path to the chapter, for example `docs/guides/phase0.md`. |
| `steps` | Ordered work for that sitting. |

## A step

| Field | Meaning |
|-------|---------|
| `id` | Stable string, unique inside the day (`"1"`, `"2"`, …). |
| `title` | One line in the UI. |
| `durationMinutes` | Part of the time box. |
| `body` | What to do, in plain language. Commands the learner runs. |
| `why` | Why this step exists. |
| `links` | `{ "label", "path" }` repo-relative files the reader can open. |
| `outcome` | Optional. How you know the step worked. |
| `figure`, `figureAlt` | Optional infographic under the step title. Repo-relative path. |
| `submission` | If `true`, the UI shows a **Save locally** form → `learner/submissions/<day>/step-<id>.json` (gitignored). |
| `submissionQuestions` | List of `{ id, label, hint?, input?: textarea\|text\|mcq, rows?, required?, minLength?, maxLength?, mustContain?, mustContainHint?, options?, correctOptionId? }`. MCQ: **4+** `options` with `{ id, label }`; optional `correctOptionId` for validation. |
| `submissionPlaceholder`, `submissionRows` | Legacy single textarea when `submissionQuestions` is omitted. |
| `progressSection` | Optional heading in `learner/journal/PROGRESS.md` updated when the learner saves. |
| `journalGuide` | Optional extra background (shown as **Background**). Prefer merging into `body` to avoid duplication. |

## Paths

`path` is relative to the repository root, using forward slashes. The site opens it at `/repo/<path>`.

Good: `docs/guides/phase1.md`, `learner/journal/PROGRESS.md`, `examples/day02-response.json`.

External URLs do not belong in `path`. Put them in the guide markdown.

## Where new material goes

| You are adding | Edit |
|----------------|------|
| Another sitting in the current arc | a `days` entry and, if needed, a section of the phase guide |
| A new stage (for example evals, or a product use case) | a `phases` entry, a `docs/guides/phaseN.md`, a row in `docs/guides/phases.md` |
| A recap after the chapter exists | `docs/revision/` |
| A sample command output | `examples/` |
| Your own checkmarks | nowhere in git — `learner/progress.json` |
| Your exercise answers | nowhere in git — `learner/submissions/` (from **Save locally** in the UI) |
