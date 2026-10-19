# Phase 3 — Tools (function calling) & side effects

**Duration:** ~2 weeks (Days 29–42 in [DAILY_30MIN.md](./DAILY_30MIN.md))  
**Prerequisites:** [phase2.md](./phase2.md)  
**Next:** [phase4.md](./phase4.md) — RAG

---

## Purpose

Language models **propose** actions; **your code executes** them. Phase 3 teaches the tool loop: definitions, invocation, observations, logging, and sandboxing. This is the foundation for agents, MCP servers, and real product integrations (files, APIs, git).

---

## Core concepts

### Tool definition

Each tool has:

| Part | Purpose |
|------|---------|
| **Name** | Stable identifier (`read_file`) |
| **Description** | Tells the model when to use it |
| **Parameters** | JSON Schema (types, required fields) |

The model outputs a **tool call** (name + arguments). You run the function and return a **tool result** string (or structured JSON) back into the conversation.

### The loop

```text
messages + tools
    → model (tool_call or final answer)
    → if tool_call: execute → append tool result → repeat
    → else: return to user
```

Set **max steps** (e.g. 5–10) to prevent infinite loops.

### Safety

- **Allowlist** tools per app; do not expose `run_shell` by default.
- **Sandbox paths** — e.g. only read under `data/`; reject `..`.
- **Truncate** large tool outputs before feeding back to the model.
- **Never** `eval()` user or model-provided code.
- Log every call: name, args, duration, result size.

### Idempotency and permissions

Writes (delete, send email, post) need extra gates—Phase 5 adds human approval. Reads still need path and scope limits.

### MCP (Model Context Protocol)

A standard way to expose tools/resources to clients like Cursor. Optional stretch: same functions behind an MCP server as your Python registry uses.

---

## What you build

```text
tools/
  registry.py          # register(name, fn, schema), list_tools()
  builtins/
    files.py           # read_file, list_dir (sandboxed)
    git_readonly.py    # git_status
apps/
  tool_runner/
    repl.py            # chat + visible traces
logs/
  traces/              # jsonl per session
```

**Starter tools**

| Tool | Risk | Notes |
|------|------|--------|
| `add(a, b)` | None | Learn the loop |
| `read_file(path)` | Medium | Sandbox |
| `list_dir(path)` | Low | Sandbox |
| `git_status()` | Low | Read-only subprocess |

---

## Exercises

1. Registry + manual tool loop (you paste tool results).
2. Automated `run_tool_loop()` with jsonl trace.
3. Sandboxed file tools + path traversal test.
4. `git_status` summarization via model.
5. REPL with printed trace after each turn.
6. Deny unregistered tool names with a clear error observation.

---

## Done when

- [ ] Model successfully uses **≥2 tools** in one session.
- [ ] Full trace replayable from `logs/traces/`.
- [ ] Sandboxed `read_file` rejects escape paths.

---

## Tool loop vs RAG

| Tools | RAG |
|-------|-----|
| Live data, actions, APIs | Static corpus search |
| “Run git status” | “What does our doc say about X?” |

You will combine both in later phases.

---

## Related docs

- [phase4.md](./phase4.md) — retrieve documents before answering
- [phase5.md](./phase5.md) — agents run this loop autonomously
