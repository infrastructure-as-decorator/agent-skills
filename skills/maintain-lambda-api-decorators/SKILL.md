---
name: maintain-lambda-api-decorators
description: Develop and maintain the lambda-api-decorators runtime, CDK, official examples, and documentation repositories, including contracts, tests, wheels, release coordination, and CI.
---

# Maintain Lambda API Decorators

Use this skill for changes to the libraries or their official ecosystem repositories. It is not the application-consumer skill: a request to use an already published API in an unrelated application belongs to `build-with-lambda-api-decorators`.

1. Read the applicable `AGENTS.md` files and classify the change as runtime, CDK, examples, or docs. Keep those responsibility boundaries explicit.
2. For development, source and tests are authoritative. Search for an existing public API before adding one; write or update tests before implementation. A controlled red baseline is acceptable only when the failing test is understood and reported.
3. Use `scripts/load_api_contract.py` when a packaged contract is needed. Resolve installed distributions, wheels, or checkouts explicitly; versions come from distribution metadata, not JSON. A checkout is unreleased, and an installation or wheel alone does not establish publication (`publication_state: unknown`).
4. Read only the relevant reference: contract schema for contract changes, repositories for cross-repository work, validation for gates, and anti-patterns for review.
5. Release and consume in order: runtime, CDK, examples, then docs. Examples must use published PyPI versions; docs must be derived from code already integrated into examples. Never call a branch-only change published.
6. Run the relevant tests, wheel/sdist checks, synthesis, docs build, and workflows. Distinguish product failures, pre-existing failures, and environmental limitations. Report Docker skips instead of hiding them.
7. Use `scripts/audit_contract.py` for non-fatal checkout/example inventories and cross-repository anti-pattern checks. These scripts support maintainer work; application developers should not need them.

The references and scripts in this skill contain the detailed maintainer procedures. Do not copy contracts or static API/version snapshots into the skill.

See [contract-schema.md](references/contract-schema.md), [repositories.md](references/repositories.md), [validation.md](references/validation.md), and [anti-patterns.md](references/anti-patterns.md) when relevant.
