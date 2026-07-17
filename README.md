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

## Status

Early stage. Documentation-first: architecture and ADRs came before any code (see `docs/` and `roadmap.md`). Current state: project skeleton, minimal CLI and provider abstraction with mock — phases A and B of the roadmap complete. Station development starts next.

## Development

Requires Python 3.10+. No external dependencies yet.

Run the CLI from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m forge.cli version
```

## Credits

Architecture inspired by [prajwal-y/video_explainer](https://github.com/prajwal-y/video_explainer) (MIT).

## License

MIT — see [LICENSE](LICENSE).