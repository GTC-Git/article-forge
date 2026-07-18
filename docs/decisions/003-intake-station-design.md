# ADR 003 — Intake Station Design

**Date:** 2026-07-18
**Status:** Accepted

## Context

The intake station is the entry point of the pipeline (issue #1). It receives
the article request, validates it, and writes the first file of the run chain
consumed by the next station (scan). No LLM calls happen here: validation is
pure Python, always at zero API cost.

The `uav-blog-writer` skill defines six task modes (Full Article, Plan,
Rewrite, Expand, SEO, QA). We had to decide how these modes map to the CLI,
what the intake accepts as input, and what it writes to disk.

## Decision

### Input: topic only

The `forge new` command receives a single argument, the article topic:

    forge new "How to choose FPV motors for a 5-inch quad"

No mode, language, category, or slug flags. Every other value is decided by
the station that has the right context for it:

- Language: always English for the original article (skill rule; translations
  are the translate station).
- Slug, title, category, tags, keywords: decided by the plan station, based
  on the inventory produced by the scan station.
- Category is restricted to the closed list extracted by the scan station.
  A new category requires human approval at the plan checkpoint.

### Modes are commands, not flags

Following the `cmd_<name>` dispatch pattern inherited from video_explainer,
each skill mode maps to its own CLI command:

| Skill mode   | Command                       | Status   |
|--------------|-------------------------------|----------|
| Full Article | `forge new "topic"`           | this ADR |
| Plan         | checkpoint inside `forge new` | this ADR |
| Rewrite      | `forge rewrite <file>`        | planned  |
| Expand       | `forge expand <file> "..."`   | planned  |
| SEO          | `forge seo <file>`            | planned  |
| QA           | `forge qa <file>`             | planned  |

Plan is not a separate command: the pipeline always stops at the plan
checkpoint and waits for human approval, so a "plan-only" run is simply a
full run not approved past the checkpoint.

Command discovery relies on argparse: `forge --help` lists all commands with
one-line descriptions, each command has its own `--help`, and an unknown
command prints the valid command list instead of a traceback.

### Pipeline flow

The full run follows the eight-station architecture defined in
`docs/architecture.md`:

    intake -> scan -> conflict -> plan -> [checkpoint: human approval]
      -> write -> qa -> render

The translate station runs as a separate command after publication.

Plan revision in v1 is manual: the user edits `04-plan.json` directly and
approves. An LLM-based `forge revise` command (parity with video_explainer's
`plan review`) is planned as a future issue.

### Validation rules

- Topic is required, non-empty, minimum 3 words (a topic must define a search
  intent, not a bare keyword).
- Topic maximum ~200 characters (a request, not a paragraph).

On failure the station returns an inspection report (`success=False`, clear
error message), writes nothing to disk, and the CLI exits with a non-zero
code.

### Output: first file of the run chain

The station creates the run directory and writes `01-intake.json`:

    runs/
      20260718-143502-fpv-motors/
        01-intake.json

    {
      "run_id": "20260718-143502-fpv-motors",
      "created_at": "2026-07-18T14:35:02",
      "station": "intake",
      "status": "ok",
      "request": {
        "topic": "How to choose FPV motors for a 5-inch quad"
      }
    }

- `run_id` = timestamp + provisional topic fragment. Human-readable and
  collision-safe. The fragment only names the folder; the editorial slug is
  decided later by the plan station.
- Numeric file prefixes (`01-`, `02-`, ...) keep the run folder readable as a
  timeline, as in video_explainer. Each station writes its own numbered file
  (`02-scan.json`, `03-conflict.json`, `04-plan.json`, ...).
- Station files use JSON (stdlib parsing, deterministic writes). YAML remains
  only for user-facing configuration.
- The runs directory is configurable in `forge.yaml` (`runs_dir`), default
  `runs/` at the repo root, and is git-ignored (execution artifact, not code).

### Code structure

- `src/forge/stations/__init__.py` — new `stations` package.
- `src/forge/stations/intake.py` — `run(request) -> report` with validation
  and file writing. All business rules live here.
- `cli.py` — `cmd_new` only translates CLI arguments into a request and calls
  the station, so the station is testable without simulating a terminal.
- `tests/test_intake.py` — valid topic, empty topic, short topic, long topic,
  written JSON contents.

## Consequences

- The intake stays minimal and free: no API cost, trivial to test.
- Mode selection is explicit through command choice, faithful to the
  inherited CLI pattern.
- Deferred decisions (slug, category, metadata) each land in the station with
  the best context, keeping stations single-purpose.
- Two future issues derive from this ADR: `forge revise` (LLM plan revision)
  and the commands operating on existing articles (rewrite, expand, seo, qa).