#!/usr/bin/env python3
"""Day 1 structured submissionQuestions for the Q&A UI."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CUR = REPO / "curriculum" / "curriculum.json"


def main() -> None:
    data = json.loads(CUR.read_text(encoding="utf-8"))
    day = next(d for d in data["days"] if d["id"] == "day-1")
    steps = {str(s["id"]): s for s in day["steps"]}

    steps["4"]["submissionQuestions"] = [
        {
            "id": "tags-result",
            "label": "What did GET /api/tags return?",
            "hint": "Paste the models: [...] line or describe the JSON (not connection refused).",
            "input": "textarea",
            "rows": 3,
            "required": True,
            "minLength": 12,
            "mustContain": ["model"],
            "mustContainHint": "Mention that you saw model name(s) in the response.",
        }
    ]
    steps["4"].pop("submissionPlaceholder", None)
    steps["4"].pop("submissionRows", None)

    steps["5"]["body"] = (
        "Read “A token” in the chapter, then answer the questions below and **Save locally**.\n\n"
        "A tokenizer splits text into subword pieces (tokens). The model sees tokens, not words. "
        "hello is often one token; a leading space before Hello is often an extra token; "
        "JSON usually costs more tokens than plain English.\n\n"
        "From Day 2, read usage.prompt_tokens, usage.completion_tokens, and usage.total_tokens."
    )
    steps["5"]["submissionQuestions"] = [
        {
            "id": "token-define",
            "label": "What is a token, in your own words?",
            "hint": "3–5 sentences. Say subword pieces, not “letters” or “words” only.",
            "input": "textarea",
            "rows": 4,
            "required": True,
            "minLength": 40,
        },
        {
            "id": "hello-why",
            "label": "Why is “Hello” not guaranteed to be one token?",
            "hint": "Mention splitting or spaces/punctuation.",
            "input": "textarea",
            "rows": 3,
            "required": True,
            "minLength": 25,
        },
        {
            "id": "usage-fields",
            "label": "Which JSON fields hold token counts from Day 2 on?",
            "hint": "Name the two usage fields for input vs output.",
            "input": "text",
            "required": True,
            "minLength": 10,
            "mustContain": ["prompt_tokens", "completion_tokens"],
            "mustContainHint": "Include usage.prompt_tokens and usage.completion_tokens.",
        },
    ]
    steps["5"].pop("submissionPlaceholder", None)
    steps["5"].pop("submissionRows", None)

    steps["6"]["body"] = (
        "Read “The context budget,” then answer below and **Save locally**.\n\n"
        "One chat/completions call has one token budget for your messages and the model’s reply "
        "(including reasoning). This lab uses about 4096 tokens as a working cap."
    )
    steps["6"]["submissionQuestions"] = [
        {
            "id": "fits",
            "label": "What must fit inside one chat/completions call?",
            "input": "textarea",
            "rows": 3,
            "required": True,
            "minLength": 35,
        },
        {
            "id": "pdf",
            "label": "What happens if someone pastes a whole PDF into one user message?",
            "input": "textarea",
            "rows": 3,
            "required": True,
            "minLength": 30,
        },
        {
            "id": "cap4096",
            "label": "Why does this lab use about 4096 tokens as a working cap?",
            "input": "textarea",
            "rows": 2,
            "required": True,
            "minLength": 20,
        },
    ]
    steps["6"].pop("submissionPlaceholder", None)
    steps["6"].pop("submissionRows", None)

    steps["7"]["body"] = (
        "Close the chapter. Answer each item below in your own words, then **Save locally** "
        "before you mark the step done."
    )
    steps["7"]["submissionQuestions"] = [
        {
            "id": "base-url",
            "label": "Chat base URL and what /api/tags is for",
            "hint": "http://127.0.0.1:11434/v1 for chat; /api/tags is inventory only.",
            "input": "textarea",
            "rows": 2,
            "required": True,
            "minLength": 25,
            "mustContain": ["11434"],
        },
        {
            "id": "model-id",
            "label": "Model id for this lab",
            "input": "text",
            "required": True,
            "minLength": 3,
            "mustContain": ["lfm3"],
        },
        {
            "id": "token-recall",
            "label": "Token — definition and where counts appear in JSON",
            "input": "textarea",
            "rows": 2,
            "required": True,
            "minLength": 25,
            "mustContain": ["prompt_tokens"],
        },
        {
            "id": "context-recall",
            "label": "Context window — who shares the budget in one call?",
            "input": "textarea",
            "rows": 2,
            "required": True,
            "minLength": 25,
            "mustContain": ["4096"],
        },
    ]
    steps["7"].pop("submissionPlaceholder", None)
    steps["7"].pop("submissionRows", None)

    day["steps"] = [steps[str(i)] for i in range(1, 8)]
    CUR.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("patched day-1 submissionQuestions")


if __name__ == "__main__":
    main()
