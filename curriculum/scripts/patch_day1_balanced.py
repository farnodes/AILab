#!/usr/bin/env python3
"""Day 1 copy: direct by default; plain-language only where concepts need it."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CUR = REPO / "curriculum" / "curriculum.json"


def main() -> None:
    data = json.loads(CUR.read_text(encoding="utf-8"))
    day = next(d for d in data["days"] if d["id"] == "day-1")
    steps = {str(s["id"]): s for s in day["steps"]}

    day["summary"] = (
        "Start the local model service, confirm the model id is lfm3, and define token "
        "and context window in your own words. First run may take 45–60 min while lfm3 downloads; "
        "later sittings are ~30 min."
    )

    steps["1"]["body"] = (
        "Ollama is a program on your machine. It loads a model and answers HTTP calls. "
        "It is not the chat UI and not model training.\n\n"
        "Two URLs share port 11434:\n"
        "1) GET /api/tags — is the process up, and which model names are installed?\n"
        "2) POST /v1/chat/completions — the chat call you use from Day 2. "
        "Base URL for that family: http://127.0.0.1:11434/v1\n\n"
        "The model id in JSON this week is lfm3. Read “The two URLs” and “How the seven days fit,” "
        "then run the exercises.\n\n"
        "Useful distinction: connection refused means nothing is listening (run ./server.sh). "
        "model not found means the name in JSON does not match ollama list—not a bad prompt."
    )
    steps["1"]["why"] = (
        "When a later call fails, check port 11434 and the model string before editing prompts."
    )

    steps["2"]["body"] = (
        "Run from the repo root (folder that contains server.sh):\n\n"
        "./server.sh starts Ollama if port 11434 is closed, pulls lfm3 the first time "
        "(can take many minutes), and sends one short warm-up request.\n\n"
        "Success: a banner with API base http://127.0.0.1:11434/v1 and model id lfm3. "
        "If ollama is not on PATH, install from ollama.com. On Windows, use Git Bash/WSL "
        "or bash scripts/server.sh.\n\n"
        "Optional: ollama run lfm3 and ask one question before Day 2’s HTTP exercise."
    )

    steps["3"]["body"] = (
        "ollama list prints a table. For JSON, use the NAME column only.\n\n"
        "Example: a row lfm3:latest still maps to \"model\": \"lfm3\" in this lab unless your list shows a different name.\n\n"
        "Size and modified columns are not sent in requests. If lfm3 is missing, ./server.sh did not finish pulling—run it again.\n\n"
        "Tomorrow’s curls use \"model\": \"lfm3\". A mismatch returns model not found (name error, not content error)."
    )

    steps["4"]["body"] = (
        "This request does not call the model. It returns which models Ollama has installed.\n\n"
        "Success: JSON with a models array (each item has a name). "
        "Failure: connection refused with no JSON—port 11434 is down; run ./server.sh.\n\n"
        "First command pretty-prints the response; second prints only the first few names.\n\n"
        "Save locally: paste the models: [...] line or one sentence confirming you got JSON, not refused."
    )

    steps["5"]["body"] = (
        "Read “A token” in the chapter, then answer in Save locally (3–5 sentences, your words).\n\n"
        "A tokenizer splits text into subword pieces (tokens). The model sees tokens, not words. "
        "That is easy to misunderstand, so keep these examples in mind:\n"
        "- hello is often one token; a leading space before Hello is often an extra token.\n"
        "- JSON and code usually cost more tokens than the same idea in plain English.\n\n"
        "You do not count by hand. From Day 2, read usage.prompt_tokens (input), "
        "usage.completion_tokens (output, including hidden reasoning on LFM3), and usage.total_tokens.\n\n"
        "Answer:\n"
        "1) What is a token?\n"
        "2) Why is Hello not guaranteed to be one token?\n"
        "3) Which two usage fields will you track from Day 2 on?\n\n"
        "A strong answer names subword pieces and both usage fields."
    )
    steps["5"]["submissionPlaceholder"] = "Your token definition (3–5 sentences)…"

    steps["6"]["body"] = (
        "Read “The context budget,” then answer in Save locally (3–5 sentences).\n\n"
        "One chat/completions call has one token budget. It must fit everything you send "
        "(system, user, history you resend) and everything the model generates (including reasoning).\n\n"
        "If input is too large, you may get an error, finish_reason length, or silent truncation—"
        "often dropping the middle. A full PDF in one user message does not reliably fit; "
        "Phase 2 uses retrieval instead of stuffing whole documents.\n\n"
        "This lab uses about 4096 tokens as a working cap so later days stay comparable—not something you measure today.\n\n"
        "Answer:\n"
        "1) What must fit in one call?\n"
        "2) What happens if someone pastes a whole PDF in one message?\n"
        "3) Why ~4096 tokens here?\n\n"
        "Your answer must state that prompt and reply share one limit."
    )
    steps["6"]["submissionPlaceholder"] = "Your context window notes (3–5 sentences)…"

    steps["7"]["body"] = (
        "Close the chapter and record your close-out in Save locally or say it out loud:\n\n"
        "1) Chat base URL — http://127.0.0.1:11434/v1. /api/tags on the same port is inventory only.\n"
        "2) Model id — lfm3, from the NAME column.\n"
        "3) Token — subword piece; counts in usage.prompt_tokens and usage.completion_tokens.\n"
        "4) Context — one shared budget per call; this lab plans around ~4096 tokens.\n\n"
        "If any item is fuzzy, redo that step before marking the day done. Day 2 sends a real chat POST."
    )

    day["steps"] = [steps[str(i)] for i in range(1, 8)]
    CUR.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("patched day-1 balanced copy")


if __name__ == "__main__":
    main()
