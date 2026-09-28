# Validation matrix

| Area | Minimum checks |
| --- | --- |
| Runtime | Load contract, run unit/public API/identity/permission tests, verify metadata and `current_user` behavior. |
| CDK | Load runtime and CDK contracts, run synthesis and resource/authorization tests, inspect generated graph. |
| Packaging | Inspect both wheel and sdist contents, validate `_agent/api-contract.json` plus `behavior.md`, and obtain version from package metadata. |
| Examples | Install released dependencies, run handler and stack tests, audit for manual claims and multiple routes. |
| Docs | Build docs, verify links and examples against released contracts, avoid documenting unreleased API as current. |

Use `scripts/load_api_contract.py --distribution NAME`, `--wheel FILE`, or `--checkout DIR`. The resolver classifies these as `installed`, `wheel`, and `checkout` respectively; installation does not establish publication, so `publication_state` is `unknown`. For sdists, inspect the tar archive with the same schema checks and its `PKG-INFO` metadata. Use `scripts/audit_contract.py --root DIR` for a non-fatal repository inventory; warnings require review, while a missing repository is reported as absent.
