#!/usr/bin/env python3
"""Day 1 submission steps → MCQ (4–5 options each). Idempotent."""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CUR = REPO / "curriculum" / "curriculum.json"


def main() -> None:
    data = json.loads(CUR.read_text(encoding="utf-8"))
    day = next(d for d in data["days"] if d["id"] == "day-1")
    steps = {str(s["id"]): s for s in day["steps"]}

    steps["4"]["body"] = (
        "Run the curls below, then pick the answer that matches what you saw.\n\n"
        "This request does not call the model—it lists installed models."
    )
    steps["4"]["submissionQuestions"] = [
        {
            "id": "tags-result",
            "label": "After GET /api/tags, which outcome did you get?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "json-models",
            "options": [
                {
                    "id": "json-models",
                    "label": "JSON with a models array (each item has a name)",
                },
                {
                    "id": "refused",
                    "label": "curl: connection refused — no JSON body",
                },
                {
                    "id": "chat-reply",
                    "label": "A chat completion with message.content from the model",
                },
                {
                    "id": "html-404",
                    "label": "An HTML 404 page from a web browser",
                },
                {
                    "id": "empty-200",
                    "label": "HTTP 200 with an empty body and no JSON",
                },
            ],
        }
    ]

    steps["5"]["body"] = (
        "Read “A token” in the chapter, then answer each multiple-choice question and **Save locally**."
    )
    steps["5"]["submissionQuestions"] = [
        {
            "id": "token-define",
            "label": "What is a token?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "subword",
            "options": [
                {
                    "id": "subword",
                    "label": "A subword piece the tokenizer passes to the model—not always one English word",
                },
                {"id": "char", "label": "Always exactly one keyboard character"},
                {"id": "word", "label": "Always one dictionary word"},
                {"id": "byte", "label": "One raw byte from the UTF-8 file on disk"},
                {"id": "pixel", "label": "One pixel in a rendered screenshot of the prompt"},
            ],
        },
        {
            "id": "hello-why",
            "label": "Why can “Hello” be more than one token?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "split-space",
            "options": [
                {
                    "id": "split-space",
                    "label": "Tokenizers can split subwords; a leading space is often its own token",
                },
                {"id": "always-one", "label": "It cannot—Hello is always exactly one token"},
                {"id": "model-random", "label": "The model randomly decides how many tokens to use"},
                {"id": "curl-bug", "label": "curl merges multiple words into one token automatically"},
                {"id": "gpu", "label": "GPU drivers combine letters into one token for speed"},
            ],
        },
        {
            "id": "usage-fields",
            "label": "Which fields report token counts in the chat JSON (from Day 2)?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "usage-pc",
            "options": [
                {
                    "id": "usage-pc",
                    "label": "usage.prompt_tokens and usage.completion_tokens (plus usage.total_tokens)",
                },
                {"id": "choices-len", "label": "choices[0].length and choices[0].width"},
                {"id": "model-size", "label": "model.size and model.modified from ollama list",
                },
                {"id": "headers", "label": "HTTP Content-Length headers only"},
                {"id": "finish-only", "label": "finish_reason only—no token counts exist"},
            ],
        },
    ]

    steps["6"]["body"] = (
        "Read “The context budget,” then answer the multiple-choice questions and **Save locally**."
    )
    steps["6"]["submissionQuestions"] = [
        {
            "id": "fits",
            "label": "What must fit inside one chat/completions call?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "both",
            "options": [
                {
                    "id": "both",
                    "label": "Your messages (system/user/history you send) and the model’s new reply—including reasoning",
                },
                {"id": "user-only", "label": "Only the latest user message—replies are unlimited"},
                {"id": "reply-only", "label": "Only the model reply—prompts do not count"},
                {"id": "disk", "label": "The entire model weights file on disk"},
                {"id": "unlimited", "label": "Nothing—context is unlimited on localhost"},
            ],
        },
        {
            "id": "pdf",
            "label": "Someone pastes a whole PDF into one user message. What is realistic?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "overflow",
            "options": [
                {
                    "id": "overflow",
                    "label": "Often truncate, error, or cut off—the model may not see all pages",
                },
                {"id": "all-seen", "label": "The model always reads every page with no limit"},
                {"id": "auto-rag", "label": "Ollama automatically enables RAG and indexes the PDF"},
                {"id": "split-api", "label": "The API splits the PDF across unlimited free calls automatically"},
                {"id": "ignore", "label": "PDF text is ignored; only the filename is used"},
            ],
        },
        {
            "id": "cap4096",
            "label": "Why ~4096 tokens as a working cap in this lab?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "teaching",
            "options": [
                {
                    "id": "teaching",
                    "label": "A shared teaching ruler so everyone’s exercises stay comparable",
                },
                {"id": "hardware", "label": "It is the exact hardware RAM size of your GPU in bytes"},
                {"id": "law", "label": "It is a legal maximum enforced by OpenAI globally"},
                {"id": "measure-today", "label": "You must measure it with curl on Day 1 before continuing"},
                {"id": "pdf-size", "label": "It equals the maximum PDF page count Ollama supports"},
            ],
        },
    ]

    steps["7"]["body"] = (
        "Close-out check: pick the best answer for each item, **Save locally**, then mark the step done."
    )
    steps["7"]["submissionQuestions"] = [
        {
            "id": "base-url",
            "label": "Where do chat requests go in this lab?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "v1",
            "options": [
                {
                    "id": "v1",
                    "label": "POST http://127.0.0.1:11434/v1/chat/completions (base http://127.0.0.1:11434/v1)",
                },
                {"id": "tags-chat", "label": "POST http://127.0.0.1:11434/api/tags with a user message",
                },
                {"id": "openai-cloud", "label": "https://api.openai.com only—local Ollama has no chat URL"},
                {"id": "github", "label": "POST requests to github.com/farnodes/AILab"},
                {"id": "ollama-com", "label": "https://ollama.com/chat for all local models"},
            ],
        },
        {
            "id": "model-id",
            "label": "Which model id do you send in JSON this week?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "lfm3",
            "options": [
                {"id": "lfm3", "label": "lfm3 (from ollama list NAME column in this lab)"},
                {"id": "latest-only", "label": "lfm3:latest including the tag every time"},
                {"id": "any", "label": "Any display name you remember—no need to match the list"},
                {"id": "gpt4", "label": "gpt-4o"},
                {"id": "size-col", "label": "The SIZE column from ollama list"},
            ],
        },
        {
            "id": "token-recall",
            "label": "Tokens and usage fields—best statement?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "usage",
            "options": [
                {
                    "id": "usage",
                    "label": "Subword pieces; counts in usage.prompt_tokens and usage.completion_tokens",
                },
                {"id": "words", "label": "Always one token per English word; no usage block exists"},
                {"id": "chars", "label": "Character count in message.content only"},
                {"id": "free", "label": "Reasoning tokens are free and not in usage"},
                {"id": "tags", "label": "Token counts come from GET /api/tags"},
            ],
        },
        {
            "id": "context-recall",
            "label": "Context window in one call?",
            "input": "mcq",
            "required": True,
            "correctOptionId": "shared",
            "options": [
                {
                    "id": "shared",
                    "label": "One shared budget (~4096 here) for prompt + reply in that call",
                },
                {"id": "reply-free", "label": "Prompt unlimited; only replies are capped"},
                {"id": "two-windows", "label": "Separate windows—4096 for you and 4096 for the model",
                },
                {"id": "permanent", "label": "The server remembers all past curls without resending history"},
                {"id": "pdf-ok", "label": "A full PDF in one message always fits if you use lfm3"},
            ],
        },
    ]

    day["steps"] = [steps[str(i)] for i in range(1, 8)]
    CUR.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("patched day-1 MCQ submissions")


if __name__ == "__main__":
    main()
