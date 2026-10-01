# Infrastructure as Decorators Agent Skills

This GitHub repository is a portable catalog of two independent Agent Skills:

- `build-with-lambda-api-decorators`: for developers building applications with the public APIs of `lambda-api-decorators` and `lambda-api-decorators-cdk`.
- `maintain-lambda-api-decorators`: for contributors and maintainers of the runtime, CDK, examples, documentation, contracts, tests, workflows, and releases.

You do not need to install both. Each skill can be installed and updated independently, although both are versioned under the same catalog tag. `lambda-api-decorators-development` was replaced by these two skills; there is no active third alias.

## Installation from GitHub

GitHub is the only distribution channel. `gh skill` is in public preview and requires GitHub CLI `2.90.0` or later. `gh skill` installs a skill in the location corresponding to the selected agent and scope.

For application developers:

```bash
gh skill install infrastructure-as-decorator/agent-skills \
  build-with-lambda-api-decorators
```

For contributors and maintainers:

```bash
gh skill install infrastructure-as-decorator/agent-skills \
  maintain-lambda-api-decorators
```

To pin an installation to a catalog version:

```bash
gh skill install infrastructure-as-decorator/agent-skills \
  build-with-lambda-api-decorators@v1.0.0
```

`v1.0.0` is only an example; this does not claim that the tag exists. Updates to an installed skill are managed with `gh skill update`. The catalog uses SemVer tags and GitHub Releases; no version is stored in `SKILL.md`, `agents/openai.yaml`, or the contracts.

## Publishing a version

Do not create the tag manually before publishing. Run the `Publish Agent Skills` workflow from `main` with `workflow_dispatch` and provide a stable version such as `v0.1.1`. The workflow validates the format, `main` ancestry, tests, and the dry-run; then `gh skill publish --tag` creates the tag and GitHub Release. If the tag already exists without a Release, the workflow stops to avoid publishing an ambiguous state.

## Contracts and development

The `_agent/api-contract.json` and `_agent/behavior.md` contracts are distributed inside the Python packages. They use `schema_version: "1.0"`; the JSON does not contain the package version. The version is obtained from distribution metadata. When there is insufficient evidence of publication, the resolver reports `publication_state: unknown`.

Packaged contracts are the authority for consumers. During library development, source and tests remain authoritative. Contract resolution and audit scripts are reserved for the maintainer skill and are not a normal requirement for application development.

## Catalog development

```bash
python -m pytest -q
python -m compileall -q skills tests
git diff --check
```

This repository does not maintain static API snapshots, a CHANGELOG, or copied contracts.
