---
name: lambda-api-decorators-development
description: Implement, review, test, and document changes across the Infrastructure as Decorators runtime, CDK, examples, and docs repositories using their packaged public API contracts.
---

# Infrastructure as Decorators development

Use this skill when a task spans `lambda-api-decorators`, `lambda-api-decorators-cdk`, `lambda-api-decorators-examples`, or `docs`.

1. Read every applicable `AGENTS.md`, then classify the work as runtime library, CDK library, consumer/example, or documentation.
2. Load the packaged `_agent/api-contract.json` and `_agent/behavior.md` first with `scripts/load_api_contract.py`. The resolver reports `checkout`, `wheel`, or `installed`; it does not infer publication from installation and marks publication state as `unknown`. Use the contract as the public API boundary; obtain package versions from metadata, never from the contract.
3. Read only the needed reference: schema for contract work, repositories for cross-repo changes, anti-patterns for review, and validation for verification.
4. Inspect source and tests when changing a library, when a contract is absent or inconsistent, or when changes are unreleased. The branch's code and tests remain authoritative in those cases.
5. Prefer existing public APIs. Use `current_user` rather than parsing claims manually, and do not invent features absent from the contract and source.
6. Keep runtime metadata, CDK interpretation, registries, grants, authentication, and Lambda execution as separate concerns.
7. Preserve the release order: runtime, CDK, examples, then docs. Report unreleased checkouts explicitly.

See [contract-schema.md](references/contract-schema.md), [repositories.md](references/repositories.md), [anti-patterns.md](references/anti-patterns.md), and [validation.md](references/validation.md) only when relevant.
