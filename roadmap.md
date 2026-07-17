# Article Forge — Roadmap

Documentation-first, then one station at a time. Each station is a GitHub issue, closed when delivered with its own commit.

## Phase A — Documentation (done)

- [x] Project readme, license and gitignore
- [x] Pipeline architecture (`docs/architecture.md`)
- [x] ADR 001 — why a pipeline instead of the manual workflow
- [x] ADR 002 — station architecture with file-based chaining
- [x] Roadmap and station issues

## Phase B — Skeleton (done)

- [x] Project structure (`src/`, `tests/`, `forge.yaml` example)
- [x] CLI entry point with `cmd_<name>` dispatch pattern
- [x] Provider abstraction (`base.py`, `mock.py`)

## Phase C — Stations, one at a time

- [ ] Station 1 — `intake`: receives and validates the topic request
- [ ] Station 2 — `scan`: inventories existing blog MDX files
- [ ] Station 3 — `conflict`: SEO conflict detection via LLM
- [ ] Station 4 — `plan`: full article plan + human checkpoint
- [ ] Station 5 — `write`: article body generation
- [ ] Station 6 — `qa`: deterministic lint + LLM editorial review
- [ ] Station 7 — `render`: validate and save final MDX
- [ ] Station 8 — `translate`: PT-BR / ES / UK translations

## Later (not initial scope)

- [ ] Anthropic provider (`anthropic.py`) wired to the real API
- [ ] Feedback loop for iterating on drafts
- [ ] OG/social image handling