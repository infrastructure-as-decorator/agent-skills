# Infrastructure as Decorators agent skills

Shared Codex skills for developing `lambda-api-decorators`, `lambda-api-decorators-cdk`, their examples, and documentation. The initial skill is `.agents/skills/lambda-api-decorators-development`.

## Use

Install it as a personal skill by copying or symlinking that directory into `${CODEX_HOME:-$HOME/.codex}/skills/`. To make it repository-local, copy it to a target repository's `.agents/skills/`. Invoke explicitly as `$lambda-api-decorators-development` or let Codex discover it from its description.

Run the tests with `../.venv/bin/pytest -q` (or `pytest -q` when available). Validate a skill with the Codex skill creator's `quick_validate.py`, compile with `python -m compileall`, and run `git diff --check`.

The resolver can be exercised without network access:

```bash
python .agents/skills/lambda-api-decorators-development/scripts/load_api_contract.py --checkout tests/fixtures/checkout_unreleased --json
python .agents/skills/lambda-api-decorators-development/scripts/load_api_contract.py --wheel path/to/package.whl --json
python .agents/skills/lambda-api-decorators-development/scripts/load_api_contract.py --distribution distribution-name --json
```

Resolver origins are `checkout`, `wheel`, and `installed`. Installation alone
does not prove publication; structured output reports `publication_state:
unknown` unless an external verification is explicitly added.

Future skills should live below `.agents/skills/<lowercase-hyphenated-name>/`, include only resources needed by their workflow, add focused tests, and update this README with their purpose. This repository intentionally has no plugin, release process, API snapshots, or changelog.
