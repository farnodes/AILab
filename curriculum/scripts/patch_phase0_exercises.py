#!/usr/bin/env python3
"""One-off helper to refresh Phase 0 step copy in curriculum.json (safe to re-run)."""
from __future__ import annotations

import json
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
CUR = SCRIPTS.parent / "curriculum.json"

import sys

sys.path.insert(0, str(SCRIPTS))
from journal_guides import JOURNAL_STEP_PATCHES  # noqa: E402

# Enhanced steps keyed by day id — same step ids as before (progress.json compatible)
ENHANCED: dict[str, list[dict]] = {
    "day-1": [
        {
            "id": "1",
            "title": "Why Day 1 — bootstrap the runtime",
            "durationMinutes": 5,
            "body": "Scenario: You join a team that runs AI features behind an HTTP API—not a chat website. Before prompts or RAG, you must know the service is up, which model name to pass, and what limits apply.\n\nToday you treat Ollama like a microservice: start it, list models, read /api/tags, then define token and context in your journal so later numbers make sense.\n\nSkim Runtime README + Daily progress, then continue.",
            "why": "On-call debugging starts with “is the server running?” not “is the prompt wrong?”",
            "links": [
                {"label": "Runtime README", "path": "docs/README.md"},
                {"label": "Daily progress", "path": "docs/guides/DAILY_30MIN.md"},
            ],
        },
        {
            "id": "2",
            "title": "Exercise — start the LLM service",
            "body": "Scenario: First minute of a lab session—bring the stack up the same way every time.",
            "why": "One command beats remembering five manual steps.",
            "commands": ["./server.sh"],
            "outcome": "Terminal shows API ready on 11434 and model lfm3 (or pull completes).",
        },
        {
            "id": "3",
            "title": "Exercise — verify model name",
            "body": "Scenario: Your curl fails with “model not found” if the name here does not match every JSON body you send later.",
            "why": "The string lfm3 must match exactly in all API calls.",
            "commands": ["ollama list"],
            "outcome": "You see lfm3 in the list and know the name to copy into Day 2 curl.",
        },
        {
            "id": "4",
            "title": "Exercise — health via /api/tags",
            "body": "Scenario: A monitoring check pings inventory—not chat—to see if Ollama is alive.",
            "why": "/api/tags is Ollama-native; /v1/* is the OpenAI-compatible layer on the same port.",
            "commands": [
                "curl -s http://127.0.0.1:11434/api/tags | python3 -m json.tool",
                "curl -s http://127.0.0.1:11434/api/tags | python3 -c \"import json,sys; d=json.load(sys.stdin); print('models:', [m.get('name') for m in d.get('models',[])][:5])\""
            ],
            "outcome": "JSON prints without “connection refused”; you can name one model from the list.",
        },
        {
            "id": "5",
            "title": "Reflect — define token (journal)",
            "body": "Write 3–5 sentences: What is a token? Why is “Hello” not one token? Where will counts appear in API responses starting Day 2?",
            "why": "Tokens drive billing, speed, and context limits in every product.",
            "outcome": "Journal answers: subword pieces; usage.prompt_tokens / completion_tokens.",
            "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
        },
        {
            "id": "6",
            "title": "Reflect — define context window (journal)",
            "body": "Write 3–5 sentences: What must fit in one request? What happens if a user pastes a whole PDF? Use ~4096 as this lab’s working cap.",
            "why": "Phase 2 RAG exists because you cannot stuff everything into one call.",
            "outcome": "Journal mentions prompt + reply share one limit; overflow truncates or errors.",
        },
        {
            "id": "7",
            "title": "Close out",
            "body": "Mark all steps done. You can explain: base URL, model id, token, context—in one breath.",
            "why": "Day 2 assumes this foundation.",
            "outcome": "Day 1 shows Done in the sidebar and Daily progress.",
        },
    ],
    "day-2": [
        {
            "id": "1",
            "title": "Why Day 2 — one-shot chat JSON",
            "durationMinutes": 5,
            "body": "Scenario: A nightly batch job sends support tickets to the model and stores JSON—not a chat UI. That integration uses non-streaming POST /v1/chat/completions.\n\nToday you run a realistic one-liner prompt, save the full response, and read content, reasoning, usage, and finish_reason. That file is your baseline for Days 3–4.\n\nRun ./server.sh first.",
            "why": "Batch + tests use one JSON body; streaming comes later for interactive UX.",
            "commands": ["./server.sh"],
            "links": [{"label": "Phase 0 API", "path": "docs/guides/phase0.md"}],
        },
        {
            "id": "2",
            "title": "Learn — request contract",
            "body": "Open phase0.md mentally: POST /v1/chat/completions with model, messages[{role, content}], stream omitted or false.",
            "why": "Every SDK ultimately sends this shape.",
            "links": [{"label": "Phase 0 guide", "path": "docs/guides/phase0.md"}],
            "outcome": "You can sketch the JSON on paper without curl.",
        },
        {
            "id": "3",
            "title": "Exercise — realistic one-shot prompt",
            "body": "Scenario: Classify urgency of a user message (practice for later agent routing).",
            "why": "More memorable than Hello—and still one user message.",
            "commands": [
                "curl -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"User message: \\\"Server down since 9am.\\\" Reply with one word: urgent or normal.\"}]}' | python3 -m json.tool"
            ],
            "outcome": "Single JSON object; choices[0].message.content is non-empty.",
        },
        {
            "id": "4",
            "title": "Exercise — save artifact",
            "body": "Save the Hello response (simpler baseline) for diffing in later days.",
            "why": "Files beat terminal scrollback for learning and git.",
            "commands": [
                "mkdir -p experiments",
                "curl -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}' \\",
                "  | python3 -m json.tool > examples/day02-response.json"
            ],
            "outcome": "examples/day02-response.json exists and is valid JSON.",
        },
        {
            "id": "5",
            "title": "Exercise — extract user-visible answer",
            "body": "Scenario: Your app only displays message.content to the user.",
            "why": "Other fields are metadata or hidden reasoning.",
            "commands": [
                "python3 -c \"import json; d=json.load(open('examples/day02-response.json')); print(d['choices'][0]['message']['content'])\""
            ],
            "outcome": "You see the assistant greeting without reading raw JSON by hand.",
        },
        {
            "id": "6",
            "title": "Exercise — LFM3 reasoning cost",
            "body": "Scenario: Latency and token bills include reasoning tokens even if the UI hides them.",
            "why": "Short content + long reasoning is normal on LFM3.",
            "commands": [
                "python3 -c \"import json; d=json.load(open('examples/day02-response.json')); m=d['choices'][0]['message']; r=m.get('reasoning',''); print('content chars', len(m.get('content',''))); print('reasoning chars', len(r)); print('reasoning preview:', r[:120])\""
            ],
            "outcome": "You notice reasoning often dominates completion_tokens.",
        },
        {
            "id": "7",
            "title": "Exercise — usage & finish_reason",
            "body": "Scenario: Dashboards track tokens; alerts fire on finish_reason length (hit max tokens).",
            "why": "stop = OK; length = need shorter prompt or higher max_tokens.",
            "commands": [
                "python3 -c \"import json; d=json.load(open('examples/day02-response.json')); c=d['choices'][0]; u=d.get('usage',{}); print('finish_reason:', c.get('finish_reason')); print('usage:', u)\""
            ],
            "outcome": "Journal lists prompt/completion/total tokens and finish_reason stop.",
            "links": [{"label": "Saved response", "path": "examples/day02-response.json"}],
        },
        {
            "id": "8",
            "title": "Exercise — stateless multi-turn",
            "body": "Scenario: Chat history must be sent by your app—send two user messages in one request and see both in context.",
            "why": "The server does not remember yesterday’s curl.",
            "commands": [
                "curl -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"My name is Sam.\"},{\"role\":\"assistant\",\"content\":\"Hi Sam.\"},{\"role\":\"user\",\"content\":\"What name did I give? One word.\"}]}' \\",
                "  | python3 -c \"import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'])\""
            ],
            "outcome": "Model answers Sam (proves history is only what you send).",
        },
        {
            "id": "9",
            "title": "Close out",
            "body": "Confirm day02-response.json exists. Journal one sentence: when you would use non-streaming vs streaming.",
            "why": "Day 3 is streaming on the same endpoint.",
            "outcome": "Day 2 complete in sidebar.",
        },
    ],
    "day-3": [
        {
            "id": "1",
            "title": "Why Day 3 — streaming for interactive UX",
            "durationMinutes": 5,
            "body": "Scenario: A chat product shows tokens as they arrive so users know the model is working. Same endpoint as Day 2, but stream:true and SSE chunks.\n\nToday you measure TTFT, parse delta.reasoning vs delta.content on LFM3, and save examples/day03-streaming.txt for Day 7.\n\nRun ./server.sh.",
            "why": "Perceived speed = time to first token, not time to full JSON.",
            "commands": ["./server.sh"],
            "links": [
                {"label": "Day 2 baseline", "path": "examples/day02-response.json"},
                {"label": "Daily progress", "path": "docs/guides/DAILY_30MIN.md"},
            ],
        },
        {
            "id": "2",
            "title": "Learn — batch vs stream",
            "body": "Same URL and messages; add \"stream\": true. Response is many data: lines ending with [DONE], not one object.",
            "why": "Choose stream for UI; batch for tests and ETL.",
            "outcome": "You can name one field that differs in the HTTP response shape.",
        },
        {
            "id": "3",
            "title": "Exercise — live stream (product-style prompt)",
            "body": "Scenario: User asks for a short list—watch tokens appear incrementally.",
            "why": "curl -N disables buffering so you feel TTFT.",
            "commands": [
                "curl -N http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"List three tips for learning APIs. Number them.\"}],\"stream\":true}'"
            ],
            "outcome": "You see multiple data: lines before [DONE].",
        },
        {
            "id": "4",
            "title": "Learn — wire format",
            "body": "Pick one chunk: note object, choices[0].delta, and whether content or reasoning updated.",
            "why": "Your Phase 1 client will concatenate delta fields.",
            "links": [{"label": "Phase 0 API", "path": "docs/guides/phase0.md"}],
            "outcome": "You can point to delta.content vs delta.reasoning in a chunk.",
        },
        {
            "id": "5",
            "title": "Exercise — measure TTFT",
            "body": "Scenario: SLO dashboard tracks seconds until first byte.",
            "why": "First chunk may be reasoning-only on LFM3—note that in your metric.",
            "commands": [
                "time ( curl -N -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"Say OK.\"}],\"stream\":true}' \\",
                "  | head -1 > /dev/null )"
            ],
            "outcome": "You record one TTFT number in journal and in day03 file.",
        },
        {
            "id": "6",
            "title": "Exercise — rebuild answer from chunks",
            "body": "Scenario: Your CLI must print only user-visible text from a stream.",
            "why": "Teaches parsing without a framework.",
            "commands": [
                "curl -N -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"Count from 1 to 5.\"}],\"stream\":true}' \\",
                "  | python3 -c \"import sys,json; out=[]\\nfor line in sys.stdin:\\n  line=line.strip()\\n  if not line.startswith('data:') or line=='data: [DONE]': continue\\n  d=json.loads(line[6:])\\n  c=d['choices'][0].get('delta',{}).get('content') or ''\\n  out.append(c)\\n  sys.stdout.write(c)\\nprint(); print('--- joined:', ''.join(out))\""
            ],
            "outcome": "Joined text matches what you saw stream (e.g. 1…5).",
        },
        {
            "id": "7",
            "title": "Exercise — save learning note",
            "body": "Capture TTFT, model, and whether reasoning preceded content.",
            "why": "Day 7 review uses this artifact.",
            "commands": [
                "mkdir -p experiments",
                "printf 'Day 3\\nTTFT seconds: (fill in)\\nModel: lfm3\\nNote: reasoning chunks before content? yes/no\\n' > examples/day03-streaming.txt",
                "cat examples/day03-streaming.txt"
            ],
            "outcome": "File exists with your TTFT filled in.",
        },
        {
            "id": "8",
            "title": "Exercise — final chunk",
            "body": "Scenario: Client must detect normal completion vs truncation.",
            "why": "finish_reason on last chunk matches Day 2 semantics.",
            "commands": [
                "curl -N -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"Say hi in five words.\"}],\"stream\":true}' | tail -3"
            ],
            "outcome": "You see finish_reason stop (or length) before [DONE].",
        },
        {
            "id": "9",
            "title": "Close out",
            "body": "Journal: when your capstone would use streaming vs batch.",
            "why": "Day 4 tunes prompts, not transport.",
            "outcome": "Day 3 complete.",
        },
    ],
    "day-4": [
        {
            "id": "1",
            "title": "Why Day 4 — steer behavior without changing models",
            "durationMinutes": 5,
            "body": "Scenario: Same lfm3 powers a terse status bot and a friendly onboarding coach—system prompt + temperature do the work.\n\nToday you run the same user question under two profiles, save JSON, compare tokens and tone.\n\nRun ./server.sh.",
            "why": "Cheaper than fine-tuning for style and format constraints.",
            "commands": ["./server.sh"],
        },
        {
            "id": "2",
            "title": "Learn — system + user roles",
            "body": "System sets policy; user carries the task. Both live in messages[].",
            "why": "Misplacing instructions in user text weakens control.",
            "links": [{"label": "Phase 0 API", "path": "docs/guides/phase0.md"}],
            "outcome": "You can write a one-line system rule for “JSON only” or “max 15 words”.",
        },
        {
            "id": "3",
            "title": "Exercise — support bot (temp 0)",
            "body": "Scenario: Incident bot must be short and deterministic.",
            "why": "temperature 0 + strict system reduces variance.",
            "commands": [
                "mkdir -p experiments",
                "curl -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"temperature\":0,\"messages\":[{\"role\":\"system\",\"content\":\"Reply in at most 15 words. No preamble.\"},{\"role\":\"user\",\"content\":\"Explain what a token is in one sentence.\"}]}' \\",
                "  | python3 -m json.tool > examples/day04-terse.json"
            ],
            "outcome": "day04-terse.json saved; content is noticeably short.",
        },
        {
            "id": "4",
            "title": "Exercise — onboarding coach (temp 1)",
            "body": "Scenario: Teaching mode allows warmth and extra context.",
            "why": "Higher temperature adds variation run-to-run.",
            "commands": [
                "curl -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"temperature\":1,\"messages\":[{\"role\":\"system\",\"content\":\"Be friendly and thorough; use two short paragraphs.\"},{\"role\":\"user\",\"content\":\"Explain what a token is in one sentence.\"}]}' \\",
                "  | python3 -m json.tool > examples/day04-verbose.json"
            ],
            "outcome": "day04-verbose.json saved; completion_tokens usually higher.",
        },
        {
            "id": "5",
            "title": "Exercise — compare outputs",
            "body": "Side-by-side content and completion_tokens from usage.",
            "why": "Quantitative + qualitative beats gut feel.",
            "commands": [
                "python3 -c \"import json; t=json.load(open('examples/day04-terse.json')); v=json.load(open('examples/day04-verbose.json')); print('TERSE tokens', t['usage'].get('completion_tokens')); print('VERBOSE tokens', v['usage'].get('completion_tokens')); print('---'); print('TERSE:', t['choices'][0]['message']['content']); print('VERBOSE:', v['choices'][0]['message']['content'][:300])\""
            ],
            "outcome": "Journal table: tokens, tone, which profile for which product surface.",
        },
        {
            "id": "6",
            "title": "Reflect — when to use which",
            "body": "Write three bullets: (1) feature that needs temp 0 (2) feature that needs temp 1 (3) one system rule you will reuse in Phase 2.",
            "why": "Phase 1 covers Top-P and LFM3-specific tuning.",
            "outcome": "Concrete examples tied to your capstone track.",
        },
        {
            "id": "7",
            "title": "Close out",
            "body": "Both JSON files exist. Mark day done.",
            "why": "Day 5 explores limits of stuffing text into one call.",
            "outcome": "Day 4 complete.",
        },
    ],
    "day-5": [
        {
            "id": "1",
            "title": "Why Day 5 — context is a hard budget",
            "durationMinutes": 5,
            "body": "Scenario: A user attaches a “whole repo” paste; the model silently drops the middle or errors. Context is finite—measured in tokens.\n\nToday you baseline a small prompt, then stress-test a large one and record behavior.\n\nRun ./server.sh.",
            "why": "Phase 2 RAG sends chunks instead of megabytes in one shot.",
            "commands": ["./server.sh"],
        },
        {
            "id": "2",
            "title": "Exercise — baseline small request",
            "body": "Confirm normal stop + usage on a tiny prompt before stress test.",
            "why": "You need a control to compare against failure.",
            "commands": [
                "curl -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with exactly: OK\"}]}' \\",
                "  | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['choices'][0]['finish_reason'], d.get('usage'))\""
            ],
            "outcome": "finish_reason stop with modest token counts.",
        },
        {
            "id": "3",
            "title": "Exercise — build oversized prompt",
            "body": "Generate ~12k characters of filler plus a question at the start: “What is the magic word at the end?” (word only at end).",
            "why": "Tests whether early instructions survive (often they do not).",
            "commands": [
                "mkdir -p experiments",
                "python3 -c \"prefix='What is the magic word at the end of this text? Reply one word. '; filler='word '*3000; suffix=' MAGICEND'; open('examples/day05-long-prompt.txt','w').write(prefix+filler+suffix)\"",
                "wc -c examples/day05-long-prompt.txt"
            ],
            "outcome": "File size printed; you know MAGICEND is the correct answer if model reads the tail.",
        },
        {
            "id": "4",
            "title": "Exercise — send long prompt",
            "body": "POST entire file as user message; save response or error.",
            "why": "Real systems hit this in production with big PDF pastes.",
            "commands": [
                "python3 << 'PY'\nimport json, urllib.request\nfrom pathlib import Path\ntext = Path('examples/day05-long-prompt.txt').read_text()\nbody = json.dumps({'model': 'lfm3', 'messages': [{'role': 'user', 'content': text}]}).encode()\nreq = urllib.request.Request('http://127.0.0.1:11434/v1/chat/completions', data=body, headers={'Content-Type': 'application/json'})\ntry:\n    r = urllib.request.urlopen(req, timeout=120)\n    Path('examples/day05-long-response.json').write_bytes(r.read())\n    print('saved examples/day05-long-response.json')\nexcept Exception as e:\n    Path('examples/day05-long-error.txt').write_text(str(e))\n    print('error saved to examples/day05-long-error.txt')\nPY"
            ],
            "outcome": "You have either JSON or error file—journal which.",
        },
        {
            "id": "5",
            "title": "Reflect — what happened?",
            "body": "Did the model say MAGICEND? finish_reason length vs stop? Error message? Relate to ~4096 token cap.",
            "why": "Your capstone RAG design should avoid this failure mode.",
            "links": [
                {"label": "Response", "path": "examples/day05-long-response.json"},
                {"label": "Error", "path": "examples/day05-long-error.txt"},
            ],
            "outcome": "Journal answers all four questions in plain language.",
        },
        {
            "id": "6",
            "title": "Reflect — mitigation",
            "body": "One paragraph: how chunking + retrieval (Phase 2) fixes “whole document in one prompt”.",
            "why": "Connects bootstrap pain to curriculum arc.",
            "outcome": "You can explain RAG’s purpose without buzzwords.",
        },
        {
            "id": "7",
            "title": "Close out",
            "body": "Mark done. You have felt context limits, not just read about them.",
            "why": "Day 6 picks direction for the rest of the lab.",
            "outcome": "Day 5 complete.",
        },
    ],
    "day-6": [
        {
            "id": "1",
            "title": "Why Day 6 — connect skills to a capstone",
            "durationMinutes": 5,
            "body": "Scenario: Phase 0 taught the wire protocol; Phase 1–5 teach depth. Without a chosen outcome, daily exercises feel random.\n\nToday you pick a capstone track and map Phase 1–2 skills to it using ROADMAP’s Decide first table.",
            "why": "Purpose improves retention more than extra curl.",
            "links": [{"label": "ROADMAP", "path": "docs/guides/ROADMAP.md"}],
        },
        {
            "id": "2",
            "title": "Exercise — Decide first table",
            "body": "For your capstone need (facts, JSON, tools, process): mark which column you will try first.",
            "why": "Teams retrieve before fine-tune; workflows before full autonomy.",
            "links": [{"label": "Decide first", "path": "docs/guides/ROADMAP.md"}],
            "outcome": "Journal cites one row from the table with your project in mind.",
        },
        {
            "id": "3",
            "title": "Exercise — pick capstone track",
            "body": "Choose: Dev platform · Knowledge product · Automation · Learning lab (extend this repo).",
            "why": "Default choice beats endless debate.",
            "outcome": "One track name written in journal header.",
        },
        {
            "id": "4",
            "title": "Exercise — three bullets + phase map",
            "body": "(1) Capstone in one sentence (2) Phase 1 unlocks … (3) Phase 2 unlocks … (4) Biggest risk.",
            "why": "Four bullets still fit 30 minutes if you stay terse.",
            "links": [{"label": "COVERAGE", "path": "docs/guides/COVERAGE.md"}],
            "outcome": "Journal entry you can reread before Day 8.",
        },
        {
            "id": "5",
            "title": "Learn — what Day 8 starts",
            "body": "Phase 1 Day 8: GGUF & quantization—how lfm3 fits in memory and on disk.",
            "why": "Sets expectation after bootstrap.",
            "links": [{"label": "Daily progress", "path": "docs/guides/DAILY_30MIN.md"}],
            "outcome": "You know the next technical topic after Phase 0.",
        },
        {
            "id": "6",
            "title": "Close out",
            "body": "Mark done. Day 7 is timed review of Days 2–3.",
            "why": "Muscle memory before quantization math.",
            "outcome": "Day 6 complete.",
        },
    ],
    "day-7": [
        {
            "id": "1",
            "title": "Why Day 7 — prove bootstrap skills",
            "durationMinutes": 3,
            "body": "Scenario: You join a pairing session and must demo local inference in five minutes without docs.\n\nToday you time yourself on batch + stream flows and self-score Phase 0 exit criteria.",
            "why": "If this is hard, repeat weak days before Phase 1.",
            "commands": ["./server.sh"],
        },
        {
            "id": "2",
            "title": "Timed demo — batch chat (< 5 min)",
            "body": "From memory: POST Hello, print content only.",
            "why": "Mirrors Day 2 integration path.",
            "commands": [
                "curl -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}' \\",
                "  | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'])\""
            ],
            "outcome": "Completed under 5 minutes including server check.",
        },
        {
            "id": "3",
            "title": "Timed demo — stream (< 5 min)",
            "body": "stream:true, -N, show last lines include [DONE].",
            "why": "Mirrors Day 3 product path.",
            "commands": [
                "curl -N -s http://127.0.0.1:11434/v1/chat/completions \\",
                "  -H \"Content-Type: application/json\" \\",
                "  -d '{\"model\":\"lfm3\",\"messages\":[{\"role\":\"user\",\"content\":\"Count 1 to 3.\"}],\"stream\":true}' | tail -2"
            ],
            "outcome": "You see data: lines and [DONE].",
        },
        {
            "id": "4",
            "title": "Self-check — exit rubric",
            "body": "Without notes, explain aloud: token, context window, stream vs batch, base URL, model id. Journal yes/partial/no for each.",
            "why": "Matches phase0 exit criteria.",
            "links": [{"label": "phase0.md", "path": "docs/guides/phase0.md"}],
            "outcome": "At least four yes; re-study any partial.",
        },
        {
            "id": "5",
            "title": "Reflect — artifacts",
            "body": "Open day02-response.json and day03-streaming.txt; one sentence on what changed in your understanding since Day 1.",
            "why": "Closure before Phase 1.",
            "links": [
                {"label": "Day 2 JSON", "path": "examples/day02-response.json"},
                {"label": "Day 3 note", "path": "examples/day03-streaming.txt"},
            ],
            "outcome": "Journal sentence saved.",
        },
        {
            "id": "6",
            "title": "Close Phase 0",
            "body": "Mark Day 7 done. Celebrate bootstrap complete—Phase 1 adds SLM depth and a Python client.",
            "why": "You can operate local lfm3 like a microservice.",
            "links": [{"label": "Daily progress", "path": "docs/guides/DAILY_30MIN.md"}],
            "outcome": "Phase 0 days show done in Daily progress when all steps complete.",
        },
    ],
}

def main() -> None:
    data = json.loads(CUR.read_text(encoding="utf-8"))
    summaries = {
        "day-1": "Operate Ollama as a local LLM service: verify model + API, define token & context for everything after.",
        "day-2": "Integrate like a backend job: one-shot JSON, usage, reasoning, and stateless message history.",
        "day-3": "Build interactive UX: stream parsing, TTFT, and visible vs reasoning tokens on LFM3.",
        "day-4": "Steer the same model with system prompts and temperature—support bot vs coach.",
        "day-5": "Feel context limits: baseline vs oversized prompt and why RAG exists.",
        "day-6": "Pick a capstone and map Phase 1–2 skills using ROADMAP Decide first.",
        "day-7": "Timed demo of batch + stream; self-score Phase 0 exit rubric.",
    }
    for day in data["days"]:
        if day["id"] in ENHANCED:
            day["steps"] = ENHANCED[day["id"]]
            if day["id"] in summaries:
                day["summary"] = summaries[day["id"]]
        for step in day.get("steps", []):
            patch = JOURNAL_STEP_PATCHES.get((day["id"], step["id"]))
            if patch:
                step.update(patch)
    CUR.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Patched:", ", ".join(sorted(ENHANCED.keys())))


if __name__ == "__main__":
    main()
