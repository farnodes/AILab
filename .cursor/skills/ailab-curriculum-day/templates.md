# AILab day templates

Use with [SKILL.md](SKILL.md). Replace placeholders; **do not change** existing `id` values when improving copy.

## New day block (curriculum.json)

```json
{
  "id": "day-8",
  "number": 8,
  "title": "Short title",
  "phase": 1,
  "phaseLabel": "SLMs & client",
  "timeBoxMinutes": 30,
  "summary": "One sentence outcome. Note if first-time setup exceeds 30 min.",
  "resources": ["phase1", "runtime"],
  "guide": "docs/guides/phase1.md",
  "reference": {
    "apiBase": "http://127.0.0.1:11434/v1",
    "model": "lfm3"
  },
  "steps": []
}
```

## Step 1 — framing

```json
{
  "id": "1",
  "title": "Why Day N — …",
  "durationMinutes": 4,
  "body": "What the learner will be able to do after today.\n\nPoint to chapter sections by name.",
  "why": "Why order matters in the roadmap.",
  "links": [
    { "label": "Chapter: section name", "path": "docs/guides/phase1.md" }
  ]
}
```

## MCQ submission (4–5 options)

```json
{
  "submission": true,
  "submissionQuestions": [
    {
      "id": "check",
      "label": "Question stem?",
      "input": "mcq",
      "required": true,
      "correctOptionId": "right",
      "options": [
        { "id": "right", "label": "Correct answer" },
        { "id": "d1", "label": "Plausible wrong answer" },
        { "id": "d2", "label": "Plausible wrong answer" },
        { "id": "d3", "label": "Plausible wrong answer" }
      ]
    }
  ]
}
```

Minimum **4** options; set `correctOptionId`. Learner must select the correct option to **Save locally**.

## Proof-of-work submission (curl / artifact)

```json
{
  "submission": true,
  "submissionQuestions": [
    {
      "id": "proof",
      "label": "What output did you get?",
      "hint": "Paste one line or describe success vs error.",
      "input": "textarea",
      "rows": 3,
      "required": true,
      "minLength": 12
    }
  ]
}
```

## Journal step with PROGRESS sync

1. Add to `learner/journal/PROGRESS.md`:

```markdown
## Day N — topic name

*(Save locally on Day N step M.)*
```

2. Step fields:

```json
{
  "title": "Reflect — …",
  "submission": true,
  "progressSection": "Day N — topic name",
  "submissionQuestions": [
    {
      "id": "q1",
      "label": "First question?",
      "input": "textarea",
      "rows": 4,
      "required": true,
      "minLength": 40
    }
  ]
}
```

## Chapter section skeleton

```markdown
## Section title

![Short caption](images/section-slug.svg)

One paragraph definition.

| Term | Meaning |
|------|---------|
| … | … |

**Example:** concrete success vs failure symptom.

```json
{ "minimal": "sample" }
```
```

## DAILY_30MIN row

```markdown
| **N** | Topic | Hands-on one line; mention Save locally if journal | Done artifact |
```

## Patch script skeleton

```python
#!/usr/bin/env python3
"""Idempotent patch for day-N …"""
from pathlib import Path
import json

REPO = Path(__file__).resolve().parents[2]
CUR = REPO / "curriculum" / "curriculum.json"

def main() -> None:
    data = json.loads(CUR.read_text(encoding="utf-8"))
    day = next(d for d in data["days"] if d["id"] == "day-N")
    steps = {str(s["id"]): s for s in day["steps"]}
    # mutate steps["5"] …
    day["steps"] = [steps[str(i)] for i in range(1, len(steps) + 1)]
    CUR.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
```

Run: `python3 curriculum/scripts/patch_dayN_….py && python3 scripts/check_curriculum.py`
