#!/usr/bin/env bash
# Evaluate a module's pure logic (variables.tf + locals.tf) WITHOUT providers or credentials.
# Usage: eval_tf_logic.sh <module-dir> <var-file.json> <local-name> [<local-name> ...]
# Prints a JSON object {local-name: value}. Exit code 1 on Terraform errors (validation, type, logic).
set -euo pipefail

TF="${TF:-$(command -v tofu || command -v terraform)}"
MODULE="$(cd "$1" && pwd)"; VARS="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; shift 2
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

cp "$MODULE/variables.tf" "$MODULE/locals.tf" "$WORK/"
for name in "$@"; do
  printf 'output "%s" {\n  value = local.%s\n}\n' "$name" "$name" >> "$WORK/outputs.tf"
done
cp "$VARS" "$WORK/inputs.auto.tfvars.json"

cd "$WORK"
"$TF" init -backend=false -input=false >/dev/null
"$TF" apply -auto-approve -input=false -no-color >"$WORK/apply.log" 2>&1 || { cat "$WORK/apply.log" >&2; exit 1; }
"$TF" output -json
