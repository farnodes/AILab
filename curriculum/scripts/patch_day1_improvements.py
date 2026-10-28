#!/usr/bin/env python3
"""One-off patch for Day 1 content + submission fields. Safe to re-run."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CUR = REPO / "curriculum" / "curriculum.json"


def main() -> None:
    data = json.loads(CUR.read_text(encoding="utf-8"))
    day = next(d for d in data["days"] if d["id"] == "day-1")

    day["summary"] = (
        "Start the local model service, confirm the model id is lfm3, and define token "
        "and context in your own words. First run may take 45–60 min while lfm3 downloads; "
        "later sittings are ~30 min."
    )
    day["timeBoxMinutes"] = 30
    day["firstRunMinutes"] = 60

    steps = {str(s["id"]): s for s in day["steps"]}

    steps["1"]["durationMinutes"] = 4
    steps["1"]["body"] = (
        "Ollama is a program on your machine. It loads a model and answers HTTP calls. "
        "It is not the chat window and not the training step.\n\n"
        "Two URLs share port 11434:\n"
        "1) GET /api/tags — is the program up, and which model names exist?\n"
        "2) POST /v1/chat/completions — the chat call you start using on Day 2. "
        "The base for that family is http://127.0.0.1:11434/v1.\n\n"
        "The model id in every JSON body this week is lfm3. Read “The two URLs” and "
        "“How the seven days fit,” then run the exercises. By the end of today you should "
        "be able to say those two URLs, the model id, what a token is, and what has to fit in one call."
    )

    steps["2"]["durationMinutes"] = 10
    steps["2"]["body"] = (
        "Run this from the repo root (the folder that contains server.sh).\n\n"
        "./server.sh does three things: starts Ollama if port 11434 is closed, downloads lfm3 "
        "the first time (that can take several minutes), and sends one short request so the model is loaded.\n\n"
        "Ready looks like a banner with API base http://127.0.0.1:11434/v1 and model id lfm3. "
        "If it says ollama is not on PATH, install Ollama and run the command again. "
        "On Windows, use Git Bash or WSL so ./server.sh runs, or invoke bash scripts/server.sh from the repo root.\n\n"
        "Optional (not required today): after the banner, run ollama run lfm3 and ask one question "
        "so you have heard the model before Day 2’s curl.\n\n"
        "You do not type the model prompt in this step."
    )

    steps["3"]["durationMinutes"] = 3
    steps["3"]["figureAlt"] = (
        "Copy the NAME column into the model field. lfm3:latest is still requested as lfm3."
    )

    s4 = steps["4"]
    s4["durationMinutes"] = 5
    s4["figure"] = "docs/guides/images/tags-health.svg"
    s4["figureAlt"] = "Success is JSON with a models array; connection refused means Ollama is down."
    s4["submission"] = True
    s4["submissionRows"] = 4
    s4["submissionPlaceholder"] = (
        "Paste the models: [...] line from the second curl, or one sentence confirming JSON not connection refused."
    )

    s5 = steps["5"]
    s5["durationMinutes"] = 6
    s5.pop("journalGuide", None)
    s5["body"] = (
        "Read “A token” in the chapter, then write your answer in the box below (Save locally).\n\n"
        "A tokenizer cuts text into subword pieces. The model sees those pieces, not words or characters. "
        "“Hello” can be one piece or several. A space in front of a word is often its own piece. "
        "Character count on screen is a poor proxy — long JSON can cost more tokens than plain English.\n\n"
        "From Day 2 the counts arrive in usage.prompt_tokens (what you sent), "
        "usage.completion_tokens (what the model generated, including hidden reasoning on LFM3), "
        "and usage.total_tokens. Products bill and throttle on those numbers.\n\n"
        "Answer in 3–5 sentences:\n"
        "1) What is a token, in plain language?\n"
        "2) Why is “Hello” not guaranteed to be one token?\n"
        "3) Which JSON fields will hold the counts from Day 2 on?\n\n"
        "Strong entry: subword pieces plus those two usage field names. Do not paste the chapter."
    )
    s5["submission"] = True
    s5["submissionRows"] = 10
    s5["progressSection"] = "Day 1 — tokens"
    s5["submissionPlaceholder"] = "Your token definition (3–5 sentences)…"

    s6 = steps["6"]
    s6["durationMinutes"] = 6
    s6.pop("journalGuide", None)
    s6["body"] = (
        "Read “The context budget,” then write in the box below (Save locally).\n\n"
        "The budget is one number for a single HTTP call. It has to hold the messages you send "
        "and the reply the model writes back, including reasoning. Chat history you resend eats the same budget. "
        "About 4096 tokens is this lab’s working cap — a course limit so later days stay comparable, "
        "not a figure you measure today.\n\n"
        "If the text does not fit, the call can error, stop early (finish_reason length), or drop part of the prompt, "
        "often the middle. A PDF or a whole repo does not fit. Phase 2 retrieves small chunks instead.\n\n"
        "Answer in 3–5 sentences:\n"
        "1) What has to fit inside one chat/completions call?\n"
        "2) What can happen if someone pastes a whole PDF into one message?\n"
        "3) Why does this lab use about 4096 tokens as a working cap?\n\n"
        "The entry must say the prompt and the reply share one limit."
    )
    s6["submission"] = True
    s6["submissionRows"] = 10
    s6["progressSection"] = "Day 1 — context window"
    s6["submissionPlaceholder"] = "Your context window notes (3–5 sentences)…"

    s7 = steps["7"]
    s7["durationMinutes"] = 3
    s7["submission"] = True
    s7["submissionRows"] = 6
    s7["submissionPlaceholder"] = (
        "Your four close-out lines in your own words (base URL, model id, token, context)…"
    )

    day["steps"] = [steps[str(i)] for i in range(1, 8)]

    CUR.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("patched day-1")


if __name__ == "__main__":
    main()
