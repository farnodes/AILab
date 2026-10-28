#!/usr/bin/env bash
# Start Ollama (if needed), ensure lfm3 is pulled, warm the model — ready for API + ollama run.
# Usage: ./scripts/server.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck source=/dev/null
  source "$ROOT/.env"
  set +a
fi

HOST="${OLLAMA_HOST:-http://127.0.0.1:11434}"
MODEL="${LLM_MODEL:-lfm3}"
MAX_WAIT="${OLLAMA_STARTUP_SEC:-60}"

log() { printf '→ %s\n' "$*"; }

if ! command -v ollama >/dev/null 2>&1; then
  echo "ERROR: ollama not on PATH. Install from https://ollama.com/download"
  exit 1
fi

ollama_reachable() {
  curl -sf "${HOST}/api/tags" >/dev/null 2>&1
}

if ! ollama_reachable; then
  log "Ollama API not up — starting ollama serve (background)…"
  mkdir -p "$ROOT/logs"
  nohup ollama serve >>"$ROOT/logs/ollama-serve.log" 2>&1 &
  disown 2>/dev/null || true
  for ((i = 1; i <= MAX_WAIT; i++)); do
    if ollama_reachable; then
      log "Ollama API ready (${i}s)"
      break
    fi
    if (( i == MAX_WAIT )); then
      echo "ERROR: Ollama did not start in ${MAX_WAIT}s."
      echo "Open the Ollama app from Applications, then run this script again."
      echo "Log: $ROOT/logs/ollama-serve.log"
      exit 1
    fi
    sleep 1
  done
else
  log "Ollama API already running"
fi

if ! ollama list 2>/dev/null | awk 'NR>1 {print $1}' | grep -qx "$MODEL"; then
  log "Pulling model: $MODEL (first time may take a few minutes)…"
  ollama pull "$MODEL"
else
  log "Model '$MODEL' already installed"
fi

log "Loading model into memory (warm-up)…"
curl -sf "${HOST}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"${MODEL}\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"stream\":false}" \
  >/dev/null

echo ""
echo "══════════════════════════════════════════"
echo "  Ready — $MODEL on Ollama"
echo "══════════════════════════════════════════"
echo "  Interactive:  ollama run $MODEL"
echo "  API base:     ${HOST}/v1"
echo "  Model id:     $MODEL"
echo ""
echo "  Test:"
echo "  curl -s ${HOST}/v1/chat/completions -H 'Content-Type: application/json' \\"
echo "    -d '{\"model\":\"${MODEL}\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'"
echo "══════════════════════════════════════════"
