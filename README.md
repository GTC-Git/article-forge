# Article Forge

AI-powered pipeline that turns a topic into a publish-ready MDX blog article — SEO check, metadata, writing, QA and translations.

Built for the [UAV Drone Academy](https://uavdroneacademy.com) blog (EN original, with PT-BR, ES and UK translations).

## What it does

Article Forge is a Python CLI that runs an article through a chain of stations, like an assembly line. Each station reads the output of the previous one from disk and writes its own:

| # | Station | Purpose |
|---|---------|---------|
| 1 | `intake` | Receives the topic request |
| 2 | `scan` | Inventories existing blog articles |
| 3 | `conflict` | Detects SEO conflicts against existing content |
| 4 | `plan` | Generates the full article plan |
| — | **checkpoint** | Human approves the plan |
| 5 | `write` | Writes the article body in MDX |
| 6 | `qa` | Audits the draft (deterministic lint + LLM editorial review) |
| 7 | `render` | Validates and saves the final MDX |
| 8 | `translate` | Translates the published article (separate command) |

The pipeline stops after `plan` and waits for explicit human approval before spending API credits on writing.

## Usage

Each task mode is its own command (ADR 003):

| Command | Purpose | Status |
|---------|---------|--------|
| `forge new "topic"` | Create a full article from a topic | available |
| `forge version` | Show the forge version | available |
| `forge rewrite <file>` | Rewrite or improve an existing article | planned |
| `forge expand <file> "..."` | Add depth or sections to an existing article | planned |
| `forge seo <file>` | Improve metadata and search positioning | planned |
| `forge qa <file>` | Audit an article for publishing issues | planned |

Run `forge --help` for the full command list, or `forge <command> --help` for details.

### Runs

Every `forge new` execution creates a run: a timestamped folder under `runs/`
holding one numbered file per station (`01-intake.json`, `02-scan.json`, ...).
The run folder tells the story of the pipeline in order and is the handoff
mechanism between stations. `runs/` is a local work area and is never
committed.

## Status

Early stage. Documentation-first: architecture and ADRs came before any code (see `docs/` and `roadmap.md`). Phases A and B of the roadmap are complete (project skeleton, minimal CLI, provider abstraction with mock). Phase C in progress: station 1 (`intake`) is implemented and tested — `forge new` validates the topic and starts the run chain.

## Development

Requires Python 3.10+. Runtime has no external dependencies; tests use [pytest](https://pytest.org).

Run the CLI from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m forge.cli version
```

Run the tests:

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests/ -v
```

## Credits

Architecture inspired by [prajwal-y/video_explainer](https://github.com/prajwal-y/video_explainer) (MIT).

## License

MIT — see [LICENSE](LICENSE).