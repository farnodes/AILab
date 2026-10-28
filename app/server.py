#!/usr/bin/env python3
"""Local lab roadmap UI — serves static app, curriculum, repo docs; persists progress.json."""
from __future__ import annotations

import json
import mimetypes
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
APP = Path(__file__).resolve().parent
PUBLIC = APP / "public"
LEARNER = ROOT / "learner"
CURRICULUM = ROOT / "curriculum" / "curriculum.json"
PROGRESS = LEARNER / "progress.json"
SUBMISSIONS = LEARNER / "submissions"
PROGRESS_MD = LEARNER / "journal" / "PROGRESS.md"

HOST = os.environ.get("LAB_UI_HOST", "127.0.0.1")
PORT = int(os.environ.get("LAB_UI_PORT", "8765"))
HISTORY_MAX = 500

STATUS_VALUES = frozenset({"not_started", "in_progress", "done"})
BLOCKED_DIRS = frozenset({".git", ".llama", ".cursor", "__pycache__"})


def _blocked_repo_file(file_path: Path) -> bool:
    """Keep secrets and VCS metadata off the local reader."""
    try:
        rel = file_path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        return True
    if any(part in BLOCKED_DIRS or part == ".env" for part in rel.parts):
        return True
    name = rel.name
    if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
        return True
    if len(rel.parts) >= 2 and rel.parts[0] == "learner" and rel.parts[1] == "submissions":
        return True
    return False


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def default_progress() -> dict:
    return {
        "version": 1,
        "activeDayId": "day-1",
        "updatedAt": None,
        "days": {},
        "history": [],
    }


def load_progress_file() -> dict:
    if not PROGRESS.is_file():
        return default_progress()
    try:
        data = load_json(PROGRESS)
    except json.JSONDecodeError:
        print(f"[lab-ui] WARN: corrupt {PROGRESS}, resetting structure (backup manually if needed)")
        return default_progress()
    if not isinstance(data.get("history"), list):
        data["history"] = []
    return data


def save_progress(data: dict) -> None:
    """Write progress atomically so stopping the server mid-save cannot corrupt the file."""
    data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    LEARNER.mkdir(parents=True, exist_ok=True)
    tmp = PROGRESS.with_suffix(".json.tmp")
    payload = json.dumps(data, indent=2) + "\n"
    with tmp.open("w", encoding="utf-8") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(PROGRESS)


def merge_progress_with_curriculum(progress: dict, curriculum: dict) -> tuple[dict, bool]:
    """Ensure every day/step from curriculum exists in progress. Returns (progress, changed)."""
    changed = False
    days_out = dict(progress.get("days") or {})
    for day in curriculum.get("days", []):
        day_id = day["id"]
        if day_id not in days_out:
            days_out[day_id] = {"status": "not_started", "steps": {}}
            changed = True
        entry = days_out[day_id]
        steps = entry.setdefault("steps", {})
        for step in day.get("steps", []):
            sid = str(step["id"])
            if sid not in steps:
                steps[sid] = "not_started"
                changed = True
    progress["days"] = days_out
    if not progress.get("activeDayId") and curriculum.get("days"):
        progress["activeDayId"] = curriculum["days"][0]["id"]
        changed = True
    if progress.get("activeModulePhase") is None and progress.get("activeDayId"):
        for day in curriculum.get("days", []):
            if day["id"] == progress["activeDayId"]:
                progress["activeModulePhase"] = day.get("phase", 0)
                changed = True
                break
    if progress.get("activeModulePhase") is None and curriculum.get("days"):
        progress["activeModulePhase"] = curriculum["days"][0].get("phase", 0)
        changed = True
    if "history" not in progress or not isinstance(progress["history"], list):
        progress["history"] = []
        changed = True
    for day in curriculum.get("days", []):
        day_id = day["id"]
        if sync_day_status_from_steps(days_out[day_id], day.get("steps", [])):
            changed = True
    return progress, changed


def append_history(progress: dict, event: dict) -> None:
    hist = progress.setdefault("history", [])
    hist.append(event)
    if len(hist) > HISTORY_MAX:
        del hist[: len(hist) - HISTORY_MAX]


def curriculum_day(curriculum: dict, day_id: str) -> dict | None:
    for day in curriculum.get("days", []):
        if day["id"] == day_id:
            return day
    return None


def sync_day_status_from_steps(day_entry: dict, step_defs: list) -> bool:
    """Set day status from step statuses. Returns True if day status changed."""
    steps = day_entry.get("steps", {})
    ids = [str(s["id"]) for s in step_defs]
    values = [steps.get(i, "not_started") for i in ids]
    old = day_entry.get("status", "not_started")
    if all(v == "done" for v in values):
        new = "done"
    elif any(v in ("done", "in_progress") for v in values):
        new = "in_progress"
    else:
        new = "not_started"
    if old != new:
        day_entry["status"] = new
        return True
    return False


def curriculum_step(curriculum: dict, day_id: str, step_id: str) -> dict | None:
    day = curriculum_day(curriculum, day_id)
    if not day:
        return None
    sid = str(step_id)
    for step in day.get("steps") or []:
        if str(step.get("id")) == sid:
            return step
    return None


def submission_path(day_id: str, step_id: str) -> Path:
    return SUBMISSIONS / day_id / f"step-{step_id}.json"


def submission_questions(step: dict) -> list:
    qs = step.get("submissionQuestions")
    if not isinstance(qs, list) or not qs:
        return []
    return qs


def _mcq_option_ids(q: dict) -> set[str]:
    return {o["id"] for o in q.get("options") or [] if isinstance(o.get("id"), str)}


def _answer_display(q: dict, val: str) -> str:
    if q.get("input") == "mcq":
        for opt in q.get("options") or []:
            if opt.get("id") == val:
                return str(opt.get("label") or val)
    return val


def validate_submission_answers(step: dict, answers: dict) -> dict[str, str]:
    """Return field id -> error message."""
    field_errors: dict[str, str] = {}
    for q in submission_questions(step):
        qid = q["id"]
        raw = answers.get(qid, "")
        val = raw.strip() if isinstance(raw, str) else ""

        if q.get("input") == "mcq":
            valid = _mcq_option_ids(q)
            if q.get("required", True) and not val:
                field_errors[qid] = "Select one option."
                continue
            if val and val not in valid:
                field_errors[qid] = "Invalid choice."
                continue
            correct = q.get("correctOptionId")
            if val and correct and val != correct:
                field_errors[qid] = "Not quite—read the chapter and try another option."
            continue

        label = q.get("label") or qid

        if q.get("required", True) and not val:
            field_errors[qid] = "This answer is required."
            continue
        if not val:
            continue

        min_len = int(q.get("minLength") or 0)
        if min_len and len(val) < min_len:
            field_errors[qid] = f"At least {min_len} characters."

        max_len = int(q.get("maxLength") or 20_000)
        if len(val) > max_len:
            field_errors[qid] = f"At most {max_len} characters."

        for needle in q.get("mustContain") or []:
            if not isinstance(needle, str) or not needle.strip():
                continue
            if needle.lower() not in val.lower():
                hint = q.get("mustContainHint") or f"Include “{needle}”."
                field_errors[qid] = field_errors.get(qid, "")
                field_errors[qid] = (
                    f"{field_errors[qid]} {hint}".strip()
                    if qid in field_errors
                    else hint
                )
    return field_errors


def answers_to_progress_text(step: dict, answers: dict) -> str:
    parts: list[str] = []
    for q in submission_questions(step):
        val = answers.get(q["id"], "")
        if isinstance(val, str) and val.strip():
            shown = _answer_display(q, val.strip())
            parts.append(f"**{q.get('label', q['id'])}**\n\n{shown}")
    return "\n\n".join(parts)


def load_submission_file(day_id: str, step_id: str) -> dict:
    path = submission_path(day_id, step_id)
    if not path.is_file():
        return {}
    try:
        return load_json(path)
    except json.JSONDecodeError:
        return {}


def normalize_submission_response(step: dict | None, raw: dict) -> dict:
    updated = raw.get("updatedAt")
    qs = submission_questions(step) if step else []
    if qs:
        answers = {q["id"]: "" for q in qs}
        if isinstance(raw.get("answers"), dict):
            for q in qs:
                v = raw["answers"].get(q["id"])
                if isinstance(v, str):
                    answers[q["id"]] = v
        elif isinstance(raw.get("content"), str) and raw["content"].strip():
            answers[qs[0]["id"]] = raw["content"]
        return {"version": 1, "answers": answers, "updatedAt": updated}
    content = raw.get("content") if isinstance(raw.get("content"), str) else ""
    return {"content": content, "updatedAt": updated}


def save_submission_record(
    day_id: str,
    step_id: str,
    *,
    answers: dict | None = None,
    content: str | None = None,
) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    SUBMISSIONS.mkdir(parents=True, exist_ok=True)
    (SUBMISSIONS / day_id).mkdir(parents=True, exist_ok=True)
    path = submission_path(day_id, step_id)
    payload: dict = {"version": 1, "updatedAt": now}
    if answers is not None:
        payload["answers"] = answers
    if content is not None:
        payload["content"] = content
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(path)
    return payload


def load_submission(day_id: str, step_id: str) -> dict:
    """Legacy helper — prefer normalize_submission_response with step."""
    raw = load_submission_file(day_id, step_id)
    content = raw.get("content") if isinstance(raw.get("content"), str) else ""
    return {"content": content, "updatedAt": raw.get("updatedAt")}


def save_submission(day_id: str, step_id: str, content: str) -> dict:
    return save_submission_record(day_id, step_id, content=content)


def sync_progress_md_section(section_title: str, content: str) -> None:
    """Replace body under ## {section_title} in PROGRESS.md when the heading exists."""
    if not PROGRESS_MD.is_file():
        return
    text = PROGRESS_MD.read_text(encoding="utf-8")
    needle = f"## {section_title}"
    idx = text.find(needle)
    if idx == -1:
        return
    start = idx + len(needle)
    rest = text[start:]
    cut = len(rest)
    for marker in ("\n## ", "\n---"):
        pos = rest.find(marker)
        if pos != -1 and pos < cut:
            cut = pos
    block = content.strip()
    before = text[:idx]
    after = text[start + cut :]
    middle = f"{needle}\n\n{block}\n\n" if block else f"{needle}\n\n"
    PROGRESS_MD.write_text(before + middle + after.lstrip("\n"), encoding="utf-8")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        print(f"[lab-ui] {self.address_string()} - {fmt % args}")

    def _send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        if path == "/api/curriculum":
            self._send_json(200, load_json(CURRICULUM))
            return

        if path == "/api/progress":
            curriculum = load_json(CURRICULUM)
            progress, changed = merge_progress_with_curriculum(
                load_progress_file(), curriculum
            )
            if changed:
                save_progress(progress)
            self._send_json(200, progress)
            return

        if path == "/api/submissions":
            qs = parse_qs(parsed.query)
            day_id = (qs.get("dayId") or [None])[0]
            step_id = (qs.get("stepId") or [None])[0]
            if not day_id or step_id is None:
                self._send_json(400, {"error": "dayId and stepId required"})
                return
            curriculum = load_json(CURRICULUM)
            step = curriculum_step(curriculum, day_id, str(step_id))
            if not step or not step.get("submission"):
                self._send_json(404, {"error": "no submission for this step"})
                return
            raw = load_submission_file(day_id, str(step_id))
            data = normalize_submission_response(step, raw)
            self._send_json(200, data)
            return

        if path.startswith("/repo/"):
            rel = path[len("/repo/") :].lstrip("/")
            file_path = (ROOT / rel).resolve()
            if not str(file_path).startswith(str(ROOT.resolve())):
                self.send_error(403)
                return
            if _blocked_repo_file(file_path):
                self.send_error(403)
                return
            if not file_path.is_file():
                self.send_error(404)
                return
            self._send_file(file_path)
            return

        if path in ("", "/"):
            path = "/index.html"

        file_path = (PUBLIC / path.lstrip("/")).resolve()
        if not str(file_path).startswith(str(PUBLIC.resolve())):
            self.send_error(403)
            return
        if not file_path.is_file():
            self.send_error(404)
            return
        self._send_file(file_path)

    def do_PATCH(self) -> None:
        if urlparse(self.path).path != "/api/progress":
            self.send_error(404)
            return

        try:
            body = self._read_json_body()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid JSON"})
            return

        curriculum = load_json(CURRICULUM)
        valid_days = {d["id"] for d in curriculum.get("days", [])}
        progress, _ = merge_progress_with_curriculum(load_progress_file(), curriculum)

        now = datetime.now(timezone.utc).isoformat()
        day_id = body.get("dayId")

        if "activeDayId" in body:
            aid = body["activeDayId"]
            if aid not in valid_days:
                self._send_json(400, {"error": "unknown activeDayId"})
                return
            if progress.get("activeDayId") != aid:
                progress["activeDayId"] = aid
                append_history(
                    progress,
                    {"at": now, "type": "active_day", "dayId": aid},
                )
            day_def = curriculum_day(curriculum, aid)
            if day_def is not None:
                progress["activeModulePhase"] = day_def.get("phase", 0)

        if "activeModulePhase" in body:
            try:
                phase = int(body["activeModulePhase"])
            except (TypeError, ValueError):
                self._send_json(400, {"error": "invalid activeModulePhase"})
                return
            modules = curriculum.get("phases") or curriculum.get("modules") or []
            valid_phases = {m["phase"] for m in modules}
            if modules and phase not in valid_phases:
                self._send_json(400, {"error": "unknown activeModulePhase"})
                return
            progress["activeModulePhase"] = phase

        if day_id:
            if day_id not in valid_days:
                self._send_json(400, {"error": "unknown dayId"})
                return
            day_entry = progress["days"].setdefault(
                day_id, {"status": "not_started", "steps": {}}
            )

            if body.get("resetDay"):
                day_def = curriculum_day(curriculum, day_id)
                if not day_def:
                    self._send_json(400, {"error": "unknown dayId"})
                    return
                day_entry["status"] = "not_started"
                day_entry["steps"] = {
                    str(s["id"]): "not_started"
                    for s in day_def.get("steps", [])
                }
                day_entry.pop("currentStepId", None)
                append_history(
                    progress,
                    {"at": now, "type": "day_reset", "dayId": day_id},
                )
                save_progress(progress)
                self._send_json(200, progress)
                return

            if "dayStatus" in body:
                st = body["dayStatus"]
                if st not in STATUS_VALUES:
                    self._send_json(400, {"error": "invalid dayStatus"})
                    return
                if day_entry.get("status") != st:
                    day_entry["status"] = st
                    append_history(
                        progress,
                        {"at": now, "type": "day_status", "dayId": day_id, "status": st},
                    )

            step_id = body.get("stepId")
            if step_id is not None:
                step_status = body.get("stepStatus")
                if step_status not in STATUS_VALUES:
                    self._send_json(400, {"error": "invalid stepStatus"})
                    return
                sid = str(step_id)
                steps = day_entry.setdefault("steps", {})
                if steps.get(sid) != step_status:
                    steps[sid] = step_status
                    append_history(
                        progress,
                        {
                            "at": now,
                            "type": "step_status",
                            "dayId": day_id,
                            "stepId": sid,
                            "status": step_status,
                        },
                    )

            if "currentStepId" in body:
                day_entry["currentStepId"] = str(body["currentStepId"])

            day_def = curriculum_day(curriculum, day_id)
            if day_def and sync_day_status_from_steps(day_entry, day_def.get("steps", [])):
                append_history(
                    progress,
                    {
                        "at": now,
                        "type": "day_status",
                        "dayId": day_id,
                        "status": day_entry["status"],
                        "auto": True,
                    },
                )
        elif "activeDayId" not in body and "activeModulePhase" not in body:
            self._send_json(400, {"error": "dayId, activeDayId, or activeModulePhase required"})
            return

        if "activeModulePhase" in body and day_id is None:
            save_progress(progress)
            self._send_json(200, progress)
            return

        save_progress(progress)
        self._send_json(200, progress)

    def do_PUT(self) -> None:
        if urlparse(self.path).path != "/api/submissions":
            self.send_error(404)
            return
        try:
            body = self._read_json_body()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid JSON"})
            return
        day_id = body.get("dayId")
        step_id = body.get("stepId")
        if not day_id or step_id is None:
            self._send_json(400, {"error": "dayId and stepId required"})
            return
        curriculum = load_json(CURRICULUM)
        step = curriculum_step(curriculum, day_id, str(step_id))
        if not step or not step.get("submission"):
            self._send_json(404, {"error": "no submission for this step"})
            return

        qs = submission_questions(step)
        if qs:
            answers_in = body.get("answers")
            if not isinstance(answers_in, dict):
                self._send_json(400, {"error": "answers object required"})
                return
            answers = {
                q["id"]: str(answers_in.get(q["id"], ""))[:20_000] for q in qs
            }
            field_errors = validate_submission_answers(step, answers)
            if field_errors:
                self._send_json(
                    400,
                    {
                        "error": "validation failed",
                        "fieldErrors": field_errors,
                    },
                )
                return
            saved = save_submission_record(day_id, str(step_id), answers=answers)
            section = step.get("progressSection")
            if section:
                sync_progress_md_section(section, answers_to_progress_text(step, answers))
            self._send_json(200, saved)
            return

        content = body.get("content")
        if not isinstance(content, str):
            self._send_json(400, {"error": "content must be a string"})
            return
        if len(content) > 200_000:
            self._send_json(400, {"error": "content too large"})
            return
        saved = save_submission_record(day_id, str(step_id), content=content)
        section = step.get("progressSection")
        if section:
            sync_progress_md_section(section, content)
        self._send_json(200, saved)

    def _send_file(self, file_path: Path) -> None:
        mime, _ = mimetypes.guess_type(str(file_path))
        if file_path.suffix == ".md":
            mime = "text/markdown; charset=utf-8"
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    if not CURRICULUM.is_file():
        raise SystemExit(f"Missing {CURRICULUM}")
    LEARNER.mkdir(parents=True, exist_ok=True)
    if not PROGRESS.is_file():
        save_progress(default_progress())

    curriculum = load_json(CURRICULUM)
    progress, changed = merge_progress_with_curriculum(load_progress_file(), curriculum)
    if changed:
        save_progress(progress)

    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Lab roadmap UI → http://{HOST}:{PORT}")
    print(f"Progress persisted at → {PROGRESS}")
    print(f"Submissions (gitignored) → {SUBMISSIONS}")
    if progress.get("updatedAt"):
        print(f"Last saved → {progress['updatedAt']}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped. Progress remains on disk.")

if __name__ == "__main__":
    main()
