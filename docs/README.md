# Local Qwen3 llama-server

Run [llama.cpp](https://github.com/ggml-org/llama.cpp) `llama-server` with **Qwen3 1.7B** (Q4_K_M GGUF) from Hugging Face.

**Learning path:** [phases.md](./phases.md) (Phase 0–7 guides) · [ROADMAP.md](./ROADMAP.md) · [DAILY_30MIN.md](./DAILY_30MIN.md) (30 min/day). **GitHub:** [GITHUB.md](./GITHUB.md).

## Requirements

- macOS **Apple Silicon** (arm64) for the bundled binary below, or your own `llama-server` build
- Network on first run (downloads the model from Hugging Face)
- ~1.3 GB disk for the GGUF; model cache: `~/.cache/huggingface/hub/`

## One-time setup (binary)

If `llama-server` is not on your `PATH`, use the copy in this repo:

```bash
cd /Users/swetank/Farnodes/AI/Local/.llama

# Only if .llama/llama-b11724/ does not exist yet:
curl -fL -o llama-macos-arm64.tar.gz \
  https://github.com/ggml-org/llama.cpp/releases/download/b11724/llama-b11724-bin-macos-arm64.tar.gz
tar -xzf llama-macos-arm64.tar.gz
```

Binary path:

```text
.llama/llama-b11724/llama-server
```

Alternatively install via Homebrew when available: `brew install llama.cpp`.

## Start the server

From the project root:

```bash
cd /Users/swetank/Farnodes/AI/Local/.llama

./llama-b11724/llama-server \
  --hf-repo enacimie/Qwen3-1.7B-Q4_K_M-GGUF \
  --hf-file qwen3-1.7b-q4_k_m.gguf \
  -c 4096 \
  --port 8080
```

If `llama-server` is on your `PATH`, you can run the same flags without the `./llama-b11724/` prefix.

| Flag | Meaning |
|------|---------|
| `--hf-repo` / `--hf-file` | Hugging Face model repo and GGUF filename |
| `-c 4096` | Context length (tokens) |
| `--port 8080` | HTTP listen port |

Default bind address is **127.0.0.1** (localhost only).

First startup downloads the weights, then loads the model. When ready you should see:

```text
llama_server: listening on http://127.0.0.1:8080
```

## Verify

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/v1/models
```

Expected health response: `{"status":"ok"}`.

## OpenAI-compatible API

Base URL for clients that support a local OpenAI API:

```text
http://127.0.0.1:8080/v1
```

Example completion:

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "enacimie/Qwen3-1.7B-Q4_K_M-GGUF",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Stop the server

Press `Ctrl+C` in the terminal where it is running, or:

```bash
lsof -nP -iTCP:8080 -sTCP:LISTEN
kill <PID>
```

## Security note

With default settings, no API key is required and CORS may allow all origins. Do not expose this port on a public network without adding authentication and tightening CORS. See [llama.cpp server security](https://github.com/ggml-org/llama.cpp/pull/25655).
