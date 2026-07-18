"""Tests for the intake station (ADR 003)."""

import json

from forge.stations import intake


def test_valid_topic_creates_run(tmp_path):
    report = intake.run(
        {"topic": "How to choose FPV motors for a 5-inch quad"},
        runs_dir=str(tmp_path),
    )

    assert report["success"] is True
    assert report["error"] is None
    assert report["run_id"] is not None
    assert report["output_file"] is not None


def test_intake_file_contents(tmp_path):
    topic = "How to choose FPV motors for a 5-inch quad"
    report = intake.run({"topic": topic}, runs_dir=str(tmp_path))

    data = json.loads(
        (tmp_path / report["run_id"] / "01-intake.json").read_text(encoding="utf-8")
    )

    assert data["run_id"] == report["run_id"]
    assert data["station"] == "intake"
    assert data["status"] == "ok"
    assert data["request"] == {"topic": topic}


def test_run_id_format(tmp_path):
    report = intake.run(
        {"topic": "How to choose FPV motors for a 5-inch quad"},
        runs_dir=str(tmp_path),
    )

    # YYYYMMDD-HHMMSS-fragment: two numeric blocks, then the topic fragment
    parts = report["run_id"].split("-")
    assert len(parts[0]) == 8 and parts[0].isdigit()
    assert len(parts[1]) == 6 and parts[1].isdigit()
    assert "-".join(parts[2:]) == "how-to-choose-fpv"


def test_empty_topic_fails(tmp_path):
    report = intake.run({"topic": "   "}, runs_dir=str(tmp_path))

    assert report["success"] is False
    assert "empty" in report["error"].lower()
    assert list(tmp_path.iterdir()) == []


def test_missing_topic_fails(tmp_path):
    report = intake.run({}, runs_dir=str(tmp_path))

    assert report["success"] is False
    assert "empty" in report["error"].lower()


def test_short_topic_fails(tmp_path):
    report = intake.run({"topic": "drones"}, runs_dir=str(tmp_path))

    assert report["success"] is False
    assert "short" in report["error"].lower()
    assert list(tmp_path.iterdir()) == []


def test_long_topic_fails(tmp_path):
    long_topic = "drone motor selection " * 20  # ~440 characters
    report = intake.run({"topic": long_topic}, runs_dir=str(tmp_path))

    assert report["success"] is False
    assert "long" in report["error"].lower()
    assert list(tmp_path.iterdir()) == []


def test_accented_topic_produces_ascii_fragment(tmp_path):
    report = intake.run(
        {"topic": "Como escolher motores de drone eficientes"},
        runs_dir=str(tmp_path),
    )

    assert report["success"] is True
    assert report["run_id"].endswith("-como-escolher-motores-de")