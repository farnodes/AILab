# Curriculum

Shared roadmap data. Learners do not edit this to track progress.

| File | Role |
|------|------|
| [curriculum.json](curriculum.json) | Phases, days, and steps the website serves |
| [SCHEMA.md](SCHEMA.md) | How to add a day or a use case |
| [days/](days/) | Short markdown mirrors of each day |
| [scripts/](scripts/) | Helpers that refresh Phase 0 step copy |

Check after an edit:

```bash
python3 scripts/check_curriculum.py
```

Progress for a person lives in [learner/progress.json](../learner/progress.json), created by [app/server.py](../app/server.py).
