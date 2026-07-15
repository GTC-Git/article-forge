# ADR 001 — Why a pipeline instead of the manual skill workflow

**Status:** Accepted
**Date:** 2026-07-16

## Context

Blog articles for UAV Drone Academy are currently produced manually in Claude chat using the `uav-blog-writer` skill. The skill works well, but every article requires a full interactive session: SEO conflict check, metadata, writing, QA and translations are all driven by hand. The skill is, in practice, a functional specification written as an operating manual.

This project also serves as a learning bridge: it trains the same Python muscles (CLI, config, chained stations, LLM API calls, validation, files on disk) needed for a future video pipeline, without the audiovisual complexity (rendering, TTS, FFmpeg).

## Decision

Build `article-forge`: a Python CLI pipeline that automates the skill's workflow station by station, calling the Anthropic API where the skill relies on Claude's judgment, and using pure Python where the work is deterministic.

## Consequences

- Each article costs API credits (a few dollars with translations) instead of running on the chat subscription.
- The fine-grained conversational iteration of the skill is lost; a feedback system is a possible future addition, not initial scope.
- The skill remains the functional specification: its blocks map 1:1 to pipeline stations.
- Every architectural lesson learned here feeds the sibling video pipeline project.