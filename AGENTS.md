# AGENTS.md

- Work only in this repository unless the task explicitly scopes another repository.
- Keep skills progressive: concise `SKILL.md`, focused references, deterministic scripts.
- Do not add package API snapshots, versions, changelogs, plugins, releases, or network-dependent tests.
- The publishable source of truth is `skills/<skill-name>/`; do not duplicate skills under tool-specific installation directories such as `.agents/skills`.
- The catalog is versioned by SemVer Git tags and GitHub Releases. Do not create tags or releases during ordinary changes or CI.
- Keep `build-with-lambda-api-decorators` consumer-focused and `maintain-lambda-api-decorators` maintainer-focused.
- Run the complete test and validation commands before committing.
