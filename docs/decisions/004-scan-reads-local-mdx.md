# ADR 004: Scan reads local MDX files, not the published site

**Date:** 2026-07-21
**Status:** Accepted

## Context

Station 2 (scan) must inventory the existing blog articles so that station 3
(conflict) can detect SEO cannibalization, and so that station 4 (plan) can pick
a category from a closed list, as decided in ADR 003.

Two sources were possible: the local MDX files of the blog repository, or the
published website at uavdroneacademy.com.

The blog stores each article as an `.mdx` file with a YAML frontmatter block.
Articles are translated into four locales (`en`, `pt`, `es`, `uk`) under
`src/content/blog/{locale}/`, with the English file as the original.

## Decision

Scan reads local MDX files only. It performs no network access and makes no LLM
calls. It is deterministic local I/O.

1. **Source of truth:** the `en/` folder of the local blog repository. Other
   locales are translations of the same articles and would produce duplicated
   inventory entries and phantom conflicts.

2. **Configuration:** the blog path and the internal URL pattern are read from
   `forge.yaml` at the repository root. This file is machine-specific and is
   git-ignored. A committed `forge.example.yaml` documents the format.

```yaml
   blog:
     content_path: "C:/path/to/blog/src/content/blog"
     url_pattern: "/{locale}/blog/{slug}"
```

   The URL pattern was confirmed against a real published article and is stored
   in config so that later stations build internal links without guessing.

3. **Extracted fields:** `title`, `slug`, `focusKeyphrase`, `excerpt`,
   `metaDescription`, `tags`, `category`, `date`, `updated`, plus the source
   filename. The article body is not indexed; frontmatter is sufficient for
   conflict detection and keeps the inventory small.

4. **Dependency:** PyYAML (MIT) parses the frontmatter block. It is the first
   external dependency of the project.

5. **Output:** `02-scan.json` inside the current run folder, containing
   `articles`, `categories` (the closed, deduplicated, sorted category list
   consumed by plan), `stats`, and `skipped`.

6. **Chaining:** `forge new` runs intake, then scan. Scan locates the run by
   reading `01-intake.json`, following the file-based chaining pattern inherited
   from video_explainer.

7. **Failure policy:** scan returns an inspection report, never an unhandled
   exception. A missing config or an invalid path fails the run with an
   actionable message. An empty blog is a valid outcome: empty inventory,
   `success: true`. A malformed or missing frontmatter sends that single file to
   `skipped` with a reason, and the scan continues.

## Alternatives considered

**Scraping the published website.** Rejected for now. The rendered HTML does not
expose the editorial frontmatter: `focusKeyphrase` is an authoring annotation
that never reaches the page, and `category` has no guaranteed machine-readable
form. Those are exactly the two fields that ADR 003 depends on for keyphrase
overlap detection and for the closed category list. Scraping would also add a
network dependency, break whenever the site theme changes, and stop scan from
being pure local reading.

**Scanning all locales.** Rejected. Translations share slug and topic with the
English original, so each article would be counted four times and would appear
to conflict with itself.

## Consequences

- Scan requires a local clone of the blog repository. Users without one cannot
  run the conflict check until they provide a content path.
- Blogs published on a different stack or CMS are out of scope for v1. Support
  would arrive as a pluggable source adapter behind the same station interface,
  since the station contract is "produce the inventory", not "read MDX".
- Zero API cost for this station.