# Anti-patterns

- Parsing `requestContext.authorizer.claims` in application code couples examples to an event shape. Use the public `current_user` abstraction.
- Applying multiple HTTP route decorators to one callable makes route ownership ambiguous. Keep one HTTP route per callable.
- Treating registry discovery as a grant or authorization decision mixes metadata with permissions. Keep registries, grants, authentication, and execution separate.
- Adding a feature because it is convenient when it is absent from the loaded contract is an API invention. Inspect source/tests and update the library contract through the library change.
- Adding Git, path, or editable requirements to published examples prevents reproducible consumer installs. Use released distributions.
