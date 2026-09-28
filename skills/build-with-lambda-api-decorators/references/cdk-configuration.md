# CDK configuration

Resolve the installed runtime and CDK contracts before configuring `LambdaApi`, `LambdaApiConfig`, registries, roles, environments, Layers, or grants. Register resources through the documented public builders, then add explicit grants for the handlers that need access. Registration alone does not grant permissions.

Follow the declared precedence and validation rules. If the installed public contracts do not expose a requested registry, grant, authorizer, or metadata capability, report the missing feature instead of reaching into private modules or adding a local bypass.
