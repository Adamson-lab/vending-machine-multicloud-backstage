# Contributing

1. Branch from `main`; keep branches short-lived. Use Conventional Commits.
0. Set up: `python -m venv .venv`, activate it, then `pip install -e ".[dev]"`.
2. For a request change, edit `requests/<workload>-<environment>.yaml`, then run `vendingctl validate` and `vendingctl compile`; commit the generated files.
3. For engine, schema, policy or module changes, add or update tests, run `python -m pytest -q` and `opa test policies/rego`, and run `python scripts/build_docs.py`.
4. Changes to the schema, approval policy, credential model or a module interface need an ADR.
5. Never change the approval policy or team map in the same pull request as a request they would affect.
6. Never commit secrets or real tenant, account, billing, project or domain identifiers. Use placeholders.
