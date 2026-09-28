# Contract schema

The contract is JSON at `_agent/api-contract.json`; behavior that cannot be inferred from signatures is Markdown at `_agent/behavior.md`. The current format is `schema_version: "1.0"`; this identifies the format only, not a package release.

Required top-level fields are:

```json
{
  "schema_version": "1.0",
  "distribution": "distribution-name",
  "import_package": "import_name",
  "exports": ["public_name"],
  "functions": [{"name": "f", "signature": "f(x: str) -> str", "parameters": [{"name": "x", "type": "str", "required": true}], "returns": {"type": "str"}}],
  "decorators": [{"name": "route", "signature": "route(path: str)", "usage": "@route('/x')", "parameters": [], "behavior_ref": "routes"}],
  "classes": [{"name": "Config", "signature": "Config()", "methods": []}],
  "exceptions": ["PublicError"]
}
```

Functions, decorators, classes, methods, parameters, returns, and exceptions are intentionally generic so runtime and CDK contracts share the format. `behavior_ref` is optional and points to a heading or stable label in `behavior.md`; it is not a second signature catalog. The contract must not contain package version, tag, commit, release date, or history. `load_api_contract.py` validates the shape and requires both files without importing the package.

`behavior.md` should describe precedence, registry/grant relationships, `@public`, `read`/`write`, `current_user`, one-HTTP-route-per-callable constraints, errors, and important edge cases where applicable. Do not repeat every JSON signature.
