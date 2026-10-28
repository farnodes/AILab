"""Long-form journal teaching copy for Phase 0 reflect steps (merged into curriculum.json)."""

from __future__ import annotations

# Keys: (day_id, step_id) -> fields to merge into that step (journalGuide, body, links, …)
JOURNAL_STEP_PATCHES: dict[tuple[str, str], dict] = {
    ("day-1", "5"): {
        "journalGuide": (
            "Tokens are the unit everything else is built on. Models never see “words” directly—they see "
            "token IDs produced by a tokenizer. A tokenizer splits text into subword pieces: common English "
            "might be one token per word, but rare words, typos, emoji, and code often become several tokens. "
            "Spaces and punctuation can cost tokens too.\n\n"
            "That matters because three different systems all count tokens the same way: (1) how much text "
            "fits in one request (context window), (2) how long generation takes, and (3) how usage is reported "
            "in API JSON. Characters on screen are a poor proxy—10,000 characters of JSON can be far more "
            "tokens than 10,000 characters of plain English.\n\n"
            "Starting on Day 2 you will see usage.prompt_tokens (everything you sent), "
            "usage.completion_tokens (everything the model generated, including hidden reasoning on LFM3), "
            "and usage.total_tokens. Products bill and throttle on those numbers, not on “how long the reply looked.”"
        ),
        "body": (
            "Where to write: open learner/journal/PROGRESS.md or create learner/journal/YYYY-MM-DD.md for today. "
            "Use a heading like “Day 1 — tokens”.\n\n"
            "Your task (3–5 sentences in your own words):\n"
            "1) What is a token, in plain language?\n"
            "2) Why is “Hello” not guaranteed to be exactly one token?\n"
            "3) Where will you read token counts in API responses starting tomorrow?\n\n"
            "A strong entry names subword pieces and mentions usage.prompt_tokens / completion_tokens. "
            "A weak entry only says “pieces of text” with no link to the API."
        ),
        "links": [{"label": "Journal (PROGRESS.md)", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-1", "6"): {
        "journalGuide": (
            "The context window is a hard budget for one API call. Everything in messages[]—system, user, "
            "assistant history you resend, and the model’s new reply—must fit inside that budget, measured in "
            "tokens. If the budget is ~4096 tokens in this lab, you cannot reliably paste an entire PDF or "
            "repo into one user message and expect the model to “see” all of it.\n\n"
            "When input is too large, runtimes may truncate silently (often dropping the middle), return an "
            "error, or stop early with finish_reason length. That is not a bug in your curl—it is physics. "
            "Phase 2 (RAG) exists specifically because teams retrieve small relevant chunks instead of stuffing "
            "whole documents into one prompt.\n\n"
            "Context is shared: a long chat history you keep appending eats the same budget as the user’s latest "
            "question. Stateless APIs mean your app must decide what history to resend and what to drop."
        ),
        "body": (
            "Where to write: same journal file as the token entry; heading “Day 1 — context window”.\n\n"
            "Your task (3–5 sentences):\n"
            "1) What must fit inside a single chat/completions request?\n"
            "2) What happens if someone pastes a whole PDF into one message?\n"
            "3) Why does this lab use ~4096 as a working mental cap even if marketing sheets quote bigger numbers?\n\n"
            "Mention that prompt + completion share one limit and that overflow leads to truncation or errors."
        ),
        "links": [{"label": "Journal (PROGRESS.md)", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-2", "7"): {
        "journalGuide": (
            "The usage block is how backend jobs prove cost and health. prompt_tokens counts the input side "
            "(all roles in messages[]). completion_tokens counts generated tokens—including reasoning tokens on "
            "LFM3 even when the UI only shows message.content. total_tokens is the sum.\n\n"
            "finish_reason tells you why generation stopped: stop usually means the model ended naturally; "
            "length means it hit max_tokens or the context ceiling—your prompt or answer may be truncated. "
            "Dashboards alert on length spikes because they often mean bad UX or runaway spend.\n\n"
            "Journaling these fields now builds a habit: when something “looks wrong,” you check JSON metadata "
            "before rewriting the prompt."
        ),
        "body": (
            "Run the command above, then in your journal write a short bullet list:\n"
            "• prompt_tokens, completion_tokens, total_tokens (copy numbers from output)\n"
            "• finish_reason and what it implies for this Hello call\n"
            "• One sentence: why completion_tokens can exceed visible content length on LFM3"
        ),
        "links": [
            {"label": "Saved response", "path": "examples/day02-response.json"},
            {"label": "Journal", "path": "learner/journal/PROGRESS.md"},
        ],
    },
    ("day-2", "9"): {
        "journalGuide": (
            "Non-streaming (stream false or omitted) waits until the full JSON object is ready. That is ideal "
            "for batch jobs, tests, and pipelines that store one record per request—your Day 2 artifact is the "
            "pattern.\n\n"
            "Streaming (stream true) sends many SSE chunks so a UI can paint text incrementally. The same "
            "messages and model are used; only the transport changes. Choose stream for interactive products; "
            "choose batch when you need a single parsed object and do not care about time-to-first-token.\n\n"
            "Neither mode remembers prior curls—multi-turn only works if your app resends history in messages[]."
        ),
        "body": (
            "Confirm examples/day02-response.json exists. In your journal write 2–4 sentences:\n"
            "When would you pick non-streaming? When streaming? Name one example product surface for each "
            "(e.g. nightly ticket classifier vs in-app chat)."
        ),
        "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-3", "5"): {
        "journalGuide": (
            "Time to first token (TTFT) is the delay until the first data: chunk arrives over the wire. "
            "Users perceive “speed” from TTFT more than total time to finish a long answer. SLO dashboards often "
            "track TTFT separately from total latency.\n\n"
            "On LFM3 the first chunks may be delta.reasoning, not user-visible delta.content. That means TTFT "
            "can look “fast” while the user still waits for readable text—product teams need to decide whether "
            "to show reasoning, hide it, or show a spinner until content starts.\n\n"
            "Record TTFT in two places: a durable examples/day03-streaming.txt (artifact) and your journal "
            "(interpretation). Numbers without interpretation do not survive a week."
        ),
        "body": (
            "Run the timed curl. Fill TTFT into examples/day03-streaming.txt (next step) and in your journal "
            "add one paragraph: the TTFT number, whether the first chunk was reasoning or content, and why that "
            "matters for a chat UI."
        ),
        "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-3", "9"): {
        "journalGuide": (
            "Streaming is not “better”—it is appropriate when a human waits on the screen. Batch is appropriate "
            "when a worker processes a queue and writes to a database. Your capstone will likely use both: "
            "stream for demos and admin chat, batch for indexing, evals, and cron jobs.\n\n"
            "Tie the choice to failure modes: streams need parsers, reconnect logic, and partial UI state; "
            "batch needs timeouts and memory for large JSON bodies."
        ),
        "body": (
            "Journal 3–5 sentences: For the capstone track you are leaning toward (even if not chosen until Day 6), "
            "which flows would be streaming vs batch? Mention one risk for each choice."
        ),
        "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-4", "5"): {
        "journalGuide": (
            "Same model, same user question, different system prompt and temperature—two product surfaces. "
            "Temperature near 0 reduces randomness: good for support bots, extraction, and “same input → same "
            "shape output.” Temperature 1 allows more variation: better for brainstorming coaches, marketing "
            "drafts, and creative onboarding—at the cost of higher completion_tokens and less predictability.\n\n"
            "When you journal, combine numbers and taste: token counts explain cost; tone explains user trust. "
            "A terse bot that saves tokens but confuses users is not a win."
        ),
        "body": (
            "After running the compare command, add a small table in your journal:\n"
            "Columns: Profile (terse / verbose) | completion_tokens | tone (1 line) | good for (product surface)\n"
            "One closing sentence: which profile you would ship for an incident bot vs a learning coach."
        ),
        "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-4", "6"): {
        "journalGuide": (
            "Temperature and system prompts are the cheapest knobs before fine-tuning. temp 0 + strict system "
            "rules fit structured, high-stakes outputs (status, JSON, compliance). temp 1 + permissive system "
            "fit exploration and teaching.\n\n"
            "System rules you write now become templates in Phase 2 (“answer only from provided context”, "
            "“cite chunk ids”, “refuse if not in docs”). Pick one rule you expect to reuse so you are not "
            "inventing policy from scratch later."
        ),
        "body": (
            "Write three bullets in your journal:\n"
            "1) A feature that should use temperature 0 (name the user and failure if it drifts)\n"
            "2) A feature that benefits from temperature 1\n"
            "3) One system prompt rule you will reuse in Phase 2 (exact wording, ≤20 words)"
        ),
        "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-5", "4"): {
        "journalGuide": (
            "This step either succeeds with a large JSON response or fails with an HTTP/client error—both are "
            "valid learning outcomes. Production systems see both daily. Your journal must record which path "
            "happened so future-you knows which artifact to open.\n\n"
            "If saved: note finish_reason and whether the answer matched MAGICEND. If error: paste the error "
            "class/message and estimate whether the prompt was likely over the context budget."
        ),
        "body": (
            "In your journal, under “Day 5 — long prompt”, write:\n"
            "• Result: JSON saved OR error saved (filename)\n"
            "• One line on what you expect happened inside the model/runtime"
        ),
        "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-5", "5"): {
        "journalGuide": (
            "Long prompts test “lost in the middle”: instructions at the start and facts at the end may not "
            "both survive when filler consumes the budget. MAGICEND at the tail is deliberate—if the model "
            "answers something else, it likely never attended to the end.\n\n"
            "finish_reason length often means generation hit a cap—not necessarily that the input fit. "
            "Errors may mean the server refused oversize input. Relate what you saw to ~4096 tokens as a mental "
            "model, not magic."
        ),
        "body": (
            "Answer in plain language in your journal:\n"
            "1) Did the model return MAGICEND (or close)?\n"
            "2) What was finish_reason?\n"
            "3) If error, what did the message say?\n"
            "4) In one sentence, how does this connect to the context window you defined on Day 1?"
        ),
        "links": [
            {"label": "Response", "path": "examples/day05-long-response.json"},
            {"label": "Error", "path": "examples/day05-long-error.txt"},
            {"label": "Journal", "path": "learner/journal/PROGRESS.md"},
        ],
    },
    ("day-5", "6"): {
        "journalGuide": (
            "RAG is not a buzzword—it is an engineering response to context limits. Instead of one megabyte "
            "user message, you chunk documents, embed chunks, retrieve top-k relevant pieces, and inject only "
            "those into messages[]. The model then answers from a small evidence set.\n\n"
            "Chunking strategy (size, overlap), embedding model choice, and retrieval quality all matter as much "
            "as the LLM call. Phase 2 walks those pieces; today you journal the motivation so Phase 2 feels "
            "necessary, not optional."
        ),
        "body": (
            "Write one paragraph in your journal: How do chunking + retrieval fix “whole document in one prompt”? "
            "Name what still fits in the context window after retrieval (system + chunks + user question + answer)."
        ),
        "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-6", "2"): {
        "journalGuide": (
            "ROADMAP’s “Decide first” table is a prioritization guardrail. Teams often jump to fine-tuning or "
            "agents when retrieval or a simple workflow would ship faster. Reading the table with your capstone "
            "in mind forces a explicit bet: which column matches your first user value?\n\n"
            "Quote or paraphrase one row: need (facts, JSON, tools, process) → first technique to try. "
            "That sentence becomes your north star when Phase 1–2 offer many shiny options."
        ),
        "body": (
            "In your journal, write: “Decide first: for [your capstone need], I will try [column/technique] first because …” "
            "(2–3 sentences of reasoning)."
        ),
        "links": [
            {"label": "ROADMAP Decide first", "path": "docs/guides/ROADMAP.md"},
            {"label": "Journal", "path": "learner/journal/PROGRESS.md"},
        ],
    },
    ("day-6", "3"): {
        "journalGuide": (
            "A capstone track is a label for scope, not a contract. Dev platform = tools, IDE, codegen; "
            "Knowledge product = RAG, citations, search; Automation = workflows, cron, integrations; "
            "Learning lab = extend this repo and document experiments.\n\n"
            "Pick one for the next weeks—you can change it at Phase boundaries, but indecision wastes daily "
            "30-minute blocks. Write the track name where future-you will see it (journal header or PROGRESS table)."
        ),
        "body": (
            "Set your journal header (top of today’s entry) to: “Capstone track: [Dev platform | Knowledge product | Automation | Learning lab]”. "
            "Add one sentence why this track fits your real work or curiosity."
        ),
        "links": [{"label": "Journal", "path": "learner/journal/PROGRESS.md"}],
    },
    ("day-6", "4"): {
        "journalGuide": (
            "Four bullets connect Phase 0 skills to Phase 1–2 depth. Phase 1 (SLMs, quantization, clients) "
            "explains how lfm3 runs locally and how your code calls it. Phase 2 (RAG) explains how to give "
            "models facts without infinite context. Naming “biggest risk” early prevents fantasy architectures.\n\n"
            "This entry is what you reread on Day 8 when GGUF and memory math feel abstract—tie every Phase 1 "
            "topic back to the capstone sentence."
        ),
        "body": (
            "Journal exactly four bullets:\n"
            "1) Capstone in one sentence\n"
            "2) Phase 1 unlocks … (specific, not generic)\n"
            "3) Phase 2 unlocks …\n"
            "4) Biggest risk if you skip fundamentals"
        ),
        "links": [
            {"label": "COVERAGE", "path": "docs/guides/COVERAGE.md"},
            {"label": "Journal", "path": "learner/journal/PROGRESS.md"},
        ],
    },
    ("day-7", "4"): {
        "journalGuide": (
            "Phase 0 exit criteria are operational, not academic. You should be able to explain token, context "
            "window, stream vs batch, base URL, and model id without opening docs—because on-call and pairing "
            "sessions do not wait for grep.\n\n"
            "Self-grade honestly: “partial” means repeat the weak day before Phase 1. Journal yes/partial/no "
            "creates a checklist you can paste into PROGRESS.md when you mark Phase 0 complete."
        ),
        "body": (
            "Say each term aloud once, then in your journal create a table:\n"
            "Concept | yes / partial / no | one-line proof (what you would demo)\n"
            "Rows: token, context window, stream vs batch, base URL, model id.\n"
            "If any partial/no, note which day to redo."
        ),
        "links": [
            {"label": "phase0.md", "path": "docs/guides/phase0.md"},
            {"label": "Journal", "path": "learner/journal/PROGRESS.md"},
        ],
    },
    ("day-7", "5"): {
        "journalGuide": (
            "Artifacts beat memory. day02-response.json captured your first structured chat response; "
            "day03-streaming.txt captured how streaming felt on the wire. Re-reading them after seven days "
            "shows how much mental model you built beyond copy-paste.\n\n"
            "A good reflection names something you misunderstood on Day 1 that is obvious now—or something "
            "that is still fuzzy and needs Phase 1."
        ),
        "body": (
            "Open both artifacts. In your journal write one sentence: “Since Day 1, the biggest change in my "
            "understanding is …” Be specific (tokens, reasoning, streaming, context)—not “I learned a lot.”"
        ),
        "links": [
            {"label": "Day 2 JSON", "path": "examples/day02-response.json"},
            {"label": "Day 3 note", "path": "examples/day03-streaming.txt"},
            {"label": "Journal", "path": "learner/journal/PROGRESS.md"},
        ],
    },
}
