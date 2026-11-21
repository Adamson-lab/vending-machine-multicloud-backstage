# Request contract standard

The authoritative definition is `schema/request.schema.json` plus the rules in `src/vendingctl/rules.py`.

## Identity
File `requests/<workload_name>-<environment>.yaml`; the name must match the content (rule R10).

## Field conventions
| Field | Rule |
|---|---|
| `workload_name` | `^[a-z][a-z0-9-]{2,23}$` |
| `owner_email`, `gcp_viewer_group` | Strict email pattern; characters that can alter generated code are rejected |
| `owner_first_name`, `owner_last_name` | No quotes, backslashes or newlines |
| `cost_center` | `cc-` plus 3 to 6 digits |
| `environment` | `prod`, `nonprod`, `dev`, `sandbox` |
| `data_classification` | `public`, `internal`, `confidential`, `restricted` |
| `requested_on` | `YYYY-MM-DD`, a real calendar date |
| `exception_ref` | `EXC-` plus 3 to 5 digits |

## Tags and labels produced
`cost-center`, `data-classification`, `environment`, `lifecycle`, `managed-by`, `owner`. Values contain only characters every cloud accepts (the strictest rules are GCP label rules). `owner` is a label-safe alias of the email local part; the full email stays in the request record.

## Change rules
A change to the schema needs an ADR, an update to the Backstage template (a test fails otherwise), and a regeneration of outputs.

## Compatibility
Adding an optional field is backwards compatible. Adding a required field or tightening a pattern is a breaking change and needs a migration of existing requests.
