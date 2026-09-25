# Validation matrix

| Area | Minimum checks |
| --- | --- |
| Runtime | Load contract, run unit/public API/identity/permission tests, verify metadata and `current_user` behavior. |
| CDK | Load runtime and CDK contracts, run synthesis and resource/authorization tests, inspect generated graph. |
| Examples | Install released dependencies, run handler and stack tests, audit for manual claims and multiple routes. |
| Docs | Build docs, verify links and examples against released contracts, avoid documenting unreleased API as current. |

Use `scripts/load_api_contract.py --distribution NAME`, `--wheel FILE`, or `--checkout DIR`. Use `scripts/audit_contract.py --root DIR` for a non-fatal repository inventory; warnings require review, while a missing repository is reported as absent.
