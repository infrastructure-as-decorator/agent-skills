# Consumer anti-patterns

- Do not parse Cognito claims manually when `current_user(event)` exists.
- Do not invent a decorator, route metadata, or configuration key absent from the public contract.
- Do not treat registry discovery as authorization or assume registration grants access; use explicit grants and roles.
- Do not combine authorizers, public routes, and future API-key protection into one implicit mechanism.
- Do not infer that a locally installed distribution is published.
