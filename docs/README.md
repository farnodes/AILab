# Local runtime — Ollama + LFM3

Learning guides live in [guides/](./guides/phases.md). This page is only how to start the model.

One command to get the model **up and ready**:

```bash
./server.sh
```

Same as `./scripts/server.sh` — starts Ollama if needed, pulls **`lfm3`**, warms the model, prints API details.

**API:** `http://127.0.0.1:11434/v1` · **model:** `lfm3`

**Learning path:** [ROADMAP.md](./guides/ROADMAP.md) · [DAILY_30MIN.md](./guides/DAILY_30MIN.md)

---

## Requirements

- [Ollama](https://ollama.com/download) installed (`ollama` on PATH)

---

## After `server.sh`

```bash
# Chat in terminal
ollama run lfm3

# Or HTTP (Day 2 lab)
curl -s http://127.0.0.1:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"lfm3","messages":[{"role":"user","content":"Hello"}]}'
```

Env for Phase 1 client: [.env.example](../.env.example)

---

## Security

Keep Ollama on localhost (port **11434**). Do not expose publicly without auth.
