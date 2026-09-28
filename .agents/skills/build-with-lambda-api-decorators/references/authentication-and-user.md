# Authentication and current user

Keep public routes and Cognito-protected routes separate, and configure authorizers through the public API. In a protected handler, prefer `current_user(event)` and handle the public `CurrentUserError` contract when identity is absent or invalid. Do not read `requestContext.authorizer.claims` manually when the helper is available; the event shape is an implementation boundary.

Do not couple authentication to registries, grants, or future API-key protection. Those concerns have separate contracts and configuration.
