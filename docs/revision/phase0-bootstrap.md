# Phase 0 — Bootstrap (revision)

**Days 1–7** · Lesson: [phase0.md](../guides/phase0.md)

Read this after the week, with the chapter closed. If a row is fuzzy, open that section and redo that day.

---

## Big picture

Ollama on your machine serves **`lfm3`** at port **11434**. You practiced **inference** (a request and a reply), not training.

Two URLs: `GET /api/tags` (is it up, which names exist) and `POST /v1/chat/completions` (the chat you will keep using).

---

## Must remember

| Concept | Recall |
|---------|--------|
| **Token** | Subword piece, not a word. `"Hello"` may be more than one |
| **Where counts live** | `usage.prompt_tokens`, `completion_tokens`, `total_tokens` |
| **Context window** | One shared budget for messages you send and the new reply. Working cap here ~4096 |
| **Reasoning** | LFM3 fills `message.reasoning` / `delta.reasoning`. It spends completion tokens. `content` is what you show |
| **Base URL** | `http://127.0.0.1:11434/v1` |
| **Model id** | `lfm3`, exactly as `ollama list` |
| **Batch** | Omit `stream`. One JSON object |
| **Stream** | `"stream": true`, `curl -N`, join `delta.content` until `data: [DONE]` |
| **finish_reason** | `stop` finished; `length` hit a cap |
| **Memory** | None, unless you resend history in `messages` |
| **Steering** | `system` is policy, `user` is the task. Temperature 0 is steadier than 1 |

---

## A response you should recognize

```json
{
  "choices": [{
    "message": {"content": "…user-visible…", "reasoning": "…often longer…"},
    "finish_reason": "stop"
  }],
  "usage": {"prompt_tokens": 11, "completion_tokens": 135, "total_tokens": 146}
}
```

Streaming is the same ideas in slices: `delta` instead of a full `message`, then `data: [DONE]`.

---

## Common mistakes

- Connection refused: the server is down, the prompt is not wrong.
- Model string does not match `ollama list`.
- Treating reasoning tokens as free.
- Assuming the last curl is still in memory.
- Pasting a whole document into one call (Day 5, `MAGICEND` at the tail).

---

## Exit check

Without the chapter: start the server, name the base URL and model id, define token and context, run one batch chat and one stream.
