# Application patterns

Use the public route decorators and the documented `LambdaApi`/CDK entry points from the resolved contract. Keep one HTTP route decorator per callable unless the contract explicitly supports another composition.

Test handlers through their public inputs and outputs. Keep application code independent of library repository layout, private modules, release branches, and generated implementation details.
