#!/usr/bin/env python3
"""Local lab roadmap UI — serves static app, curriculum, repo docs; persists progress.json."""
from __future__ import annotations

import json
import mimetypes
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
APP = Path(__file__).resolve().parent
PUBLIC = APP / "public"
LEARNER = ROOT / "learner"
CURRICULUM = ROOT / "curriculum" / "curriculum.json"
PROGRESS = LEARNER / "progress.json"

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
    if progress.get("updatedAt"):
        print(f"Last saved → {progress['updatedAt']}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped. Progress remains on disk.")

if __name__ == "__main__":
    main()
