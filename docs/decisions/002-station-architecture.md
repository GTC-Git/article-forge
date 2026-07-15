# ADR 002 — Station architecture with file-based chaining

**Status:** Accepted
**Date:** 2026-07-16

## Context

The pipeline needs a structure that is easy to reason about, cheap to re-run after failures, and friendly to a mock provider for zero-cost validation. The reference project (`prajwal-y/video_explainer`, MIT) chains stations through files on disk with a state file per run.

## Decision

Eight stations chained by files on disk, one folder per article run under `runs/{slug}/`, with numbered artifacts (`01-intake.json` … `06-qa.json`) and a `state.json` tracking progress and approval.

Key choices:

1. **`intake` is station 1** — the topic request is the raw material entering the line; scanning existing articles is context preparation, not the start.
2. **Single human checkpoint after `plan`** — the last cheap moment. Everything before it costs cents; `write` and `translate` are where the dollars go.
3. **Two-layer QA** — deterministic lint (pure Python, free) runs before the LLM editorial review. If lint fails, no API call is made.
4. **`translate` is a separate command** — the EN article is published and validated first; translations are paid for on demand.
5. **Provider abstraction with mock** — `provider: mock` runs the full pipeline on recorded fixtures before spending any API credit.

## Alternatives considered

- **In-memory pipeline (no intermediate files):** simpler code, but a failure in any station loses all previous work and API spend. Rejected.
- **Automatic translation after render:** fewer commands, but removes cost control and publishes translations of an unvalidated article. Rejected.
- **Single-layer LLM QA:** simpler, but wastes credits reviewing drafts with mechanical errors a linter catches for free. Rejected.

## Consequences

- Any station can be re-run in isolation; earlier artifacts are preserved.
- `runs/` is a local work area, excluded from version control.
- The station list is stable enough to become the project roadmap (one GitHub issue per station).