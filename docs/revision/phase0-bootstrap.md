# Phase 0 — Bootstrap (revision)

**Days 1–7** · Guide: [phase0.md](../guides/phase0.md)

---

## Big picture

You run **Ollama** locally with model **`lfm3`** and an **OpenAI-compatible** HTTP API on port **11434**. No training yet—only **inference** and understanding limits.

---

## Must remember

| Concept | Recall |
|---------|--------|
| **Token** | Text split into subword pieces; counts live in `usage` |
| **Context window** | Max tokens in one request (prompt + history + reply); ~4096 in this lab |
| **Reasoning** | LFM3 may fill `message.reasoning` / `delta.reasoning`; `content` is what you show the user |
| **Base URL** | `http://127.0.0.1:11434/v1` |
| **Inventory** | `GET /api/tags` — model name must match JSON `model` (`lfm3`) |
| **Chat** | `POST /v1/chat/completions` — `messages`, optional `stream: true` |
| **finish_reason** | `stop` = finished; `length` = hit a token cap |

---

## Response fields (chat)

- `choices[0].message.content` — assistant text the user sees
- `choices[0].message.reasoning` — hidden thinking on LFM3 (often most of the tokens)
- `choices[0].finish_reason` — `stop`, `length`, …
- `usage.prompt_tokens` / `completion_tokens` / `total_tokens`

Streaming: many `data:` JSON lines; read `choices[0].delta.content` until `data: [DONE]`.

---

## Common mistakes

- Server not running (connection refused on **11434**).
- Model string in JSON does not match `ollama list`.
- Assuming the server remembers the last curl — resend history in `messages`.
- Treating reasoning tokens as free — they count in `completion_tokens`.
- Pasting a whole document into one prompt (Day 5).

---

## Phase 0 exit check

Without the README: start the server, name the base URL and model id, define token and context, and run one batch chat plus one stream.
