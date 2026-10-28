#!/usr/bin/env python3
"""Deprecated — use patch_day1_balanced.py instead."""
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
        "Turn on the local AI “engine,” check it is alive, and learn two ideas in plain English: "
        "tokens (how text is counted) and context (how much fits in one question). "
        "First download of lfm3 may take 45–60 minutes; after that, about 30 minutes per sitting."
    )

    steps["1"]["body"] = (
        "Think of **Ollama** as a small **restaurant kitchen on your laptop**. It does not train new models "
        "this week—it only **cooks answers** when your app sends an order.\n\n"
        "**Plain-English picture:** your code is the customer. Ollama is the kitchen on **port 11434** "
        "(like a local door number only your machine uses).\n\n"
        "Today you learn two “doors” on that same port:\n"
        "1) **GET /api/tags** — like asking *“Are you open, and what’s on the menu?”* "
        "You get a list of model names. No cooking yet.\n"
        "2) **POST /v1/chat/completions** — like placing a **real order** (Day 2). "
        "Base address for chat: http://127.0.0.1:11434/v1\n\n"
        "**Example:** If `/api/tags` fails with *connection refused*, the kitchen is closed—you run `./server.sh`. "
        "If chat says *model not found*, you used the wrong name from the menu—not a “bad question.”\n\n"
        "This week every order uses model id **lfm3**. Skim the chapter sections “The two URLs” and "
        "“How the seven days fit,” then do the steps. By tonight you should explain those two URLs, "
        "lfm3, what a token is, and what must fit in one call—in your own words."
    )
    steps["1"]["why"] = (
        "Most Day-2+ bugs are boring: service off, or wrong model name. Fix those before rewriting prompts."
    )

    steps["2"]["body"] = (
        "From the repo root (folder with `server.sh`), run one command.\n\n"
        "**What `./server.sh` does—in everyday terms:**\n"
        "1) **Opens the kitchen** if nothing is listening on port 11434.\n"
        "2) **Downloads the recipe book** (`lfm3`) the first time—like a big app install; can take many minutes.\n"
        "3) **Warms the stove** with one tiny request so the first real question is not painfully slow.\n\n"
        "**You’re done when** the terminal shows a banner with API base http://127.0.0.1:11434/v1 and model **lfm3**.\n\n"
        "**If it fails:** “ollama not on PATH” means install Ollama from ollama.com, then try again. "
        "On Windows, use Git Bash/WSL, or run `bash scripts/server.sh` from the repo root.\n\n"
        "**Optional comfort check:** `ollama run lfm3` and ask “What is 2+2?”—you’ll *hear* the model before Day 2’s HTTP curl. "
        "Not required today."
    )

    steps["3"]["body"] = (
        "`ollama list` is the **name tag list** for models on your machine.\n\n"
        "**Layman rule:** In tomorrow’s JSON you only copy the **NAME** column—like the exact spelling on a reservation.\n\n"
        "**Example row:** NAME shows `lfm3:latest` → you still usually send `\"model\": \"lfm3\"` in this lab "
        "(the short name the course standardized on).\n\n"
        "**Not used in JSON:** file size, “modified” date—those are for humans, not for the API.\n\n"
        "**If lfm3 is missing:** the download in step 2 did not finish—run `./server.sh` again and wait.\n\n"
        "**Wrong name feels like a smart question failed:** API says *model not found*—that’s a typo in the name, "
        "not proof the AI is “dumb.”"
    )

    steps["4"]["body"] = (
        "This curl is a **ping with a menu attached**. You are **not** asking the model a question yet.\n\n"
        "**Good result (plain English):** JSON with a `models` list—like `[{ \"name\": \"lfm3:latest\" }]`. "
        "That means “kitchen open, these brains are installed.”\n\n"
        "**Bad result:** `connection refused` and no JSON—nothing listening on 11434. "
        "Fix: run `./server.sh`, not “try a better prompt.”\n\n"
        "**The two commands:** first pretty-prints everything; second prints just `models: ['lfm3:latest', ...]` "
        "so you are not lost in braces.\n\n"
        "**Save locally:** paste the short `models:` line or write one sentence (“JSON with models array, not refused”)."
    )

    steps["5"]["body"] = (
        "Read “A token” in the chapter, then answer in **Save locally** (your words, 3–5 sentences).\n\n"
        "**Layman definition:** A **token** is a **small chunk of text** the model actually reads—not always a whole word. "
        "Think **Scrabble tiles** or **short text message pieces**: the model counts tiles, not “how long it looks on screen.”\n\n"
        "**Examples:**\n"
        "- “hello” might be **one** tile.\n"
        "- “Hello” with a leading space might be **two** (space + word).\n"
        "- Messy JSON with `{ \"foo\": ... }` can eat **more tiles** than the same idea in plain English.\n\n"
        "You never hand-count tiles. From Day 2 the receipt is in JSON:\n"
        "- `usage.prompt_tokens` — tiles in **your** message(s)\n"
        "- `usage.completion_tokens` — tiles in the **model’s** answer (including hidden “thinking” on LFM3)\n"
        "- `usage.total_tokens` — both added up (what bills and limits often use)\n\n"
        "**Answer these:**\n"
        "1) What is a token, in plain language?\n"
        "2) Why isn’t “Hello” always exactly one token?\n"
        "3) Which two usage fields will you watch from Day 2 on?\n\n"
        "**Example shape (don’t copy verbatim):** “A token is a subword piece; Hello can split; "
        "I’ll read prompt_tokens and completion_tokens in usage.”"
    )
    steps["5"]["submissionPlaceholder"] = (
        "Example starter: A token is like a small text chunk, not always one word…"
    )

    steps["6"]["body"] = (
        "Read “The context budget,” then answer in **Save locally** (3–5 sentences).\n\n"
        "**Layman definition:** The **context window** is **one shared backpack** for a single question-and-answer trip. "
        "Everything must fit: your instructions, any chat history you resend, **and** the model’s full reply "
        "(including hidden reasoning).\n\n"
        "**Example:** If the backpack holds about **4096 tokens** in this lab, you cannot shove a **whole PDF** in and "
        "expect the model to “have read every page.” Something gets dropped, cut off, or the request errors—"
        "like over-stuffing a suitcase.\n\n"
        "**Real-world analogy:** One text message thread has a max size; if you paste War and Peace, the phone truncates "
        "or refuses—not because your question was silly, but because the **container** is full.\n\n"
        "This course uses **~4096** as a **teaching ruler** so everyone’s exercises compare fairly—not something you measure on Day 1.\n\n"
        "**Answer these:**\n"
        "1) What must fit in one chat/completions call?\n"
        "2) What happens if someone pastes an entire PDF in one user message?\n"
        "3) Why does the lab use ~4096 as a working cap?\n\n"
        "Your answer must say **prompt + reply share one limit**."
    )
    steps["6"]["submissionPlaceholder"] = (
        "Example starter: One call shares one budget—for my message and the answer…"
    )

    steps["7"]["body"] = (
        "Close the chapter. Say these **four ideas out loud or in Save locally**—like explaining to a friend who never coded:\n\n"
        "1) **Where to chat:** http://127.0.0.1:11434/v1 — real questions go here (Day 2+). "
        "`/api/tags` on the same port is only “are you open + what’s installed?”\n"
        "2) **Which brain:** model id **lfm3** — spelled like the NAME column, not a marketing nickname.\n"
        "3) **Token:** a small text chunk; counts live in `usage.prompt_tokens` and `usage.completion_tokens`.\n"
        "4) **Context:** one backpack per call—your text + the answer share about **4096 tokens** in this lab.\n\n"
        "**Example one-liner tying it together:** “I ping `/api/tags`, then I’ll POST chat to /v1 with model lfm3; "
        "the reply and my prompt share a token budget counted in usage.”\n\n"
        "If any line feels fuzzy, redo that step before marking Day 1 done. Day 2 assumes this list is muscle memory."
    )

    day["steps"] = [steps[str(i)] for i in range(1, 8)]
    CUR.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("patched day-1 layman copy")


if __name__ == "__main__":
    main()
