# Repositories and release order

| Repository | Responsibility | Contract/source note |
| --- | --- | --- |
| `lambda-api-decorators` | Runtime decorators, metadata, identity, permissions | Runtime behavior and tests are authoritative for unreleased changes. |
| `lambda-api-decorators-cdk` | CDK interpretation and infrastructure synthesis | Keep CDK discovery separate from runtime execution. |
| `lambda-api-decorators-examples` | Deployable consumers and examples | Examples consume released APIs and must not hide local/editable dependencies. |
| `docs` | Public guides and API documentation | Document released behavior; mark unreleased work explicitly. |

For coordinated work, release and validate runtime first, then CDK, then examples, then docs. A local checkout without a release tag is `unreleased`; never infer or invent a version.
