"""Intake station: validates the article request and starts the run chain.

First station of the pipeline. Receives the topic, applies validation
rules (ADR 003), and writes ``01-intake.json`` inside a new run
directory. No LLM calls happen here.
"""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

STATION_NAME = "intake"
MIN_TOPIC_WORDS = 3
MAX_TOPIC_CHARS = 200
FRAGMENT_MAX_WORDS = 4


def run(request: dict, runs_dir: str = "runs") -> dict:
    """Validate the request and write the first file of the run chain.

    Returns an inspection report: a dict with ``success``, ``error``,
    ``run_id`` and ``output_file``. Never raises for expected failures.
    """
    topic = (request.get("topic") or "").strip()

    error = _validate_topic(topic)
    if error:
        return _report(success=False, error=error)

    now = datetime.now()
    run_id = _build_run_id(topic, now)

    run_path = Path(runs_dir) / run_id
    run_path.mkdir(parents=True, exist_ok=False)

    payload = {
        "run_id": run_id,
        "created_at": now.isoformat(timespec="seconds"),
        "station": STATION_NAME,
        "status": "ok",
        "request": {"topic": topic},
    }

    output_file = run_path / "01-intake.json"
    output_file.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )

    return _report(success=True, run_id=run_id, output_file=str(output_file))


def _validate_topic(topic: str) -> str | None:
    """Return an error message, or None when the topic is valid."""
    if not topic:
        return "Topic is empty. Provide the article topic in quotes."
    if len(topic.split()) < MIN_TOPIC_WORDS:
        return (
            f"Topic too short (minimum {MIN_TOPIC_WORDS} words). "
            "A topic must define a search intent, not a bare keyword."
        )
    if len(topic) > MAX_TOPIC_CHARS:
        return (
            f"Topic too long (maximum {MAX_TOPIC_CHARS} characters). "
            "Provide a request, not a paragraph."
        )
    return None


def _build_run_id(topic: str, now: datetime) -> str:
    """Build ``YYYYMMDD-HHMMSS-topic-fragment`` for the run directory."""
    timestamp = now.strftime("%Y%m%d-%H%M%S")
    fragment = _slug_fragment(topic)
    return f"{timestamp}-{fragment}"


def _slug_fragment(topic: str) -> str:
    """Provisional slug from the first words of the topic (folder name only)."""
    ascii_text = (
        unicodedata.normalize("NFKD", topic)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    words = re.findall(r"[a-z0-9]+", ascii_text)[:FRAGMENT_MAX_WORDS]
    return "-".join(words) or "topic"


def _report(
    success: bool,
    error: str | None = None,
    run_id: str | None = None,
    output_file: str | None = None,
) -> dict:
    """Assemble the station inspection report."""
    return {
        "success": success,
        "station": STATION_NAME,
        "error": error,
        "run_id": run_id,
        "output_file": output_file,
    }