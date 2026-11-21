# Developer tasks. Tools: python3, pytest, opa, tofu or terraform, node (optional).
TF ?= $(shell command -v tofu || command -v terraform)

.PHONY: help install test validate compile docs docs-check rego-test fmt-check backstage-check diagrams-check effort clean

help:
	@grep -E '^[a-z-]+:' Makefile | cut -d: -f1 | sort

install:
	pip install -e ".[dev]"

test: validate docs-check
	python3 -m pytest -q
	$(MAKE) rego-test fmt-check

validate:
	vendingctl validate
	vendingctl compile --check

compile:
	vendingctl compile

docs:
	python3 scripts/build_docs.py

docs-check:
	python3 scripts/build_docs.py --check

rego-test:
	opa check policies
	opa test policies/rego

fmt-check:
	$(TF) fmt -check -recursive infra generated

backstage-check:
	npm install --no-audit --no-fund
	node scripts/validate_backstage.mjs .

diagrams-check:
	npm install --no-audit --no-fund
	node scripts/check_mermaid.mjs .

effort:
	python3 scripts/effort_model.py

clean:
	rm -rf .pytest_cache node_modules .venv src/*.egg-info
