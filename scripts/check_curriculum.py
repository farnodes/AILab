#!/usr/bin/env python3
"""Check curriculum.json shape and that guide links point at files in the repo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CURRICULUM = REPO / "curriculum" / "curriculum.json"
OPTIONAL_PREFIXES = ("examples/", "learner/journal/20")


def main() -> int:
    errors: list[str] = []
    data = json.loads(CURRICULUM.read_text(encoding="utf-8"))

    phases = data.get("phases") or []
    phase_ids = [p.get("phase") for p in phases]
    if len(phase_ids) != len(set(phase_ids)):
        errors.append("duplicate phase numbers")
    phase_set = set(phase_ids)

    day_ids: list[str] = []
    for day in data.get("days") or []:
        day_id = day.get("id")
        day_ids.append(day_id)
        if day.get("phase") not in phase_set:
            errors.append(f"{day_id}: phase {day.get('phase')} is not in phases")
        step_ids = [str(s.get("id")) for s in day.get("steps") or []]
        if len(step_ids) != len(set(step_ids)):
            errors.append(f"{day_id}: duplicate step ids")
        for step in day.get("steps") or []:
            for link in step.get("links") or []:
                _check_path(errors, f"{day_id} step {step.get('id')}", link.get("path"))
            if step.get("figure"):
                _check_path(errors, f"{day_id} step {step.get('id')} figure", step.get("figure"))
            _check_submission_questions(errors, day_id, step)
        for key in ("guide",):
            if day.get(key):
                _check_path(errors, day_id, day[key])

    if len(day_ids) != len(set(day_ids)):
        errors.append("duplicate day ids")

    for resource in data.get("resources") or []:
        _check_path(errors, f"resource {resource.get('id')}", resource.get("path"))

    if errors:
        print("curriculum check failed:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"curriculum ok — {len(day_ids)} days, {len(phase_ids)} phases")
    return 0


def _check_submission_questions(errors: list[str], day_id: str, step: dict) -> None:
    qs = step.get("submissionQuestions")
    if qs is None:
        return
    if not step.get("submission"):
        errors.append(f"{day_id} step {step.get('id')}: submissionQuestions without submission")
        return
    if not isinstance(qs, list) or not qs:
        errors.append(f"{day_id} step {step.get('id')}: submissionQuestions must be a non-empty list")
        return
    seen: set[str] = set()
    for q in qs:
        if not isinstance(q, dict):
            errors.append(f"{day_id} step {step.get('id')}: submissionQuestions entries must be objects")
            continue
        qid = q.get("id")
        if not qid or not isinstance(qid, str):
            errors.append(f"{day_id} step {step.get('id')}: each question needs string id")
            continue
        if qid in seen:
            errors.append(f"{day_id} step {step.get('id')}: duplicate question id {qid}")
        seen.add(qid)
        if not q.get("label"):
            errors.append(f"{day_id} step {step.get('id')}: question {qid} needs label")
        if q.get("input") == "mcq":
            opts = q.get("options")
            if not isinstance(opts, list) or len(opts) < 4:
                errors.append(
                    f"{day_id} step {step.get('id')}: MCQ {qid} needs at least 4 options"
                )
            else:
                oids: set[str] = set()
                for opt in opts:
                    if not isinstance(opt, dict) or not opt.get("id"):
                        errors.append(f"{day_id} step {step.get('id')}: MCQ option needs id")
                        continue
                    if opt["id"] in oids:
                        errors.append(f"{day_id} step {step.get('id')}: duplicate option id {opt['id']}")
                    oids.add(opt["id"])
                correct = q.get("correctOptionId")
                if correct and correct not in oids:
                    errors.append(f"{day_id} step {step.get('id')}: correctOptionId not in options")


def _check_path(errors: list[str], where: str, path: str | None) -> None:
    if not path or "://" in path:
        return
    if path.startswith(OPTIONAL_PREFIXES):
        return
    # Exercise artifacts are created by the learner; only committed samples must exist.
    if path.startswith("examples/") and not (REPO / path).is_file():
        return
    target = (REPO / path).resolve()
    if not str(target).startswith(str(REPO.resolve())):
        errors.append(f"{where}: path escapes repo ({path})")
        return
    if not target.is_file():
        errors.append(f"{where}: missing {path}")


if __name__ == "__main__":
    sys.exit(main())
