# Roadmap website

Local site for the AILab curriculum. Python standard library only.

```bash
./lab-ui.sh
```

Open http://127.0.0.1:8765

| Path | Role |
|------|------|
| `server.py` | Static files, `GET /api/curriculum`, `GET/PATCH /api/progress`, `GET /repo/<file>` |
| `public/` | Roadmap page and markdown reader |

The server reads [curriculum/curriculum.json](../curriculum/curriculum.json) and writes [learner/progress.json](../learner/progress.json).

`LAB_UI_HOST` defaults to `127.0.0.1`. `LAB_UI_PORT` defaults to `8765`.
