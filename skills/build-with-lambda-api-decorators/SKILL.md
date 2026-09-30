---
name: build-with-lambda-api-decorators
description: Build, fix, test, or review an application that consumes the public lambda-api-decorators or lambda-api-decorators-cdk APIs, including routes, LambdaApi, Cognito, authorizers, registries, grants, roles, environments, Layers, and REST or HTTP APIs.
license: MIT
---

# Build with Lambda API Decorators

Use this skill for an application that consumes the published Python packages. It does not require or inspect library checkouts, Git history, release workflows, Docusaurus, or maintainer audits.

1. Detect the installed distribution versions from package metadata. Resolve `_agent/api-contract.json` and `_agent/behavior.md` from the installed distributions or supplied wheels. Consult those files only when the task needs their contract or behavior details. A contract has `schema_version: "1.0"`; its JSON has no package version, and local installation does not prove publication.
2. Prefer the highest-level public API already provided by the installed contract. Implement and test the application against that API. Do not invent decorators, metadata, permissions, or bypasses. If the public contract lacks a capability, report it as a missing feature instead of implementing an application workaround.
3. Keep HTTP authorizers, public routes, and any future API-key protection independent. A registered resource is metadata/discovery, not permission: add explicit grants and roles. Respect contract-declared precedence and validation.
4. For Cognito identity, use `current_user(event)` and handle `CurrentUserError` when appropriate. Do not parse Cognito claims manually when the helper exists.
5. Navigate only to the focused reference needed for the task:
   - [application-patterns.md](references/application-patterns.md) for handlers, decorators, and testing;
   - [authentication-and-user.md](references/authentication-and-user.md) for authorizers, Cognito, and `current_user`;
   - [cdk-configuration.md](references/cdk-configuration.md) for `LambdaApi`, `LambdaApiConfig`, registries, grants, roles, environments, and Layers;
   - [anti-patterns.md](references/anti-patterns.md) for review checks.

This skill works with PyPI-installed packages alone. It never requires a checkout of `lambda-api-decorators`, `lambda-api-decorators-cdk`, examples, or docs.
