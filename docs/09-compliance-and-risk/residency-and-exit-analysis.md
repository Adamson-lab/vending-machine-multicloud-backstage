# Data residency and exit analysis

## Residency
| Question | Answer |
|---|---|
| Where is jurisdiction captured? | Mandatory `jurisdiction` field, validated against the configuration |
| What does it drive today? | Recorded in custom fields and catalog descriptions; approval routing can use it (extension point) |
| What enforces region limits? | Landing zone guardrails (project 1); this project does not place workloads, only containers |
| Where are request and state data stored? | In the organization's repository and state backends; place those in approved regions |

## Vendor concentration and exit
| Element | Portable? | Notes |
|---|---|---|
| Request format and schema | Yes | Cloud-neutral |
| Approval policy (Rego) | Yes | Independent of any cloud |
| Engine and compiler | Yes | Python; targets per cloud are modules |
| Terraform stacks | Partly | Per-cloud resources must be recreated for another cloud |
| AFT delivery | No | AWS and Control Tower specific |
| Backstage template | Yes | Replaceable front end (ADR 0002) |
| GitHub as platform | Partly | Workflows and OIDC trust are GitHub specific; request files are plain YAML |

## Exit scenarios
1. **Drop a cloud:** remove it from schema enums, configuration and compile; existing containers remain until decommissioned.
2. **Add a cloud:** add config placements, a compile target and a module; the request format does not change.
3. **Replace GitHub:** keep the engine and policies; replace workflows and the approval gate.

## Concentration indicators
Share of the pipeline depending on one CI provider; share of approvals depending on one team; single points of failure in view D10.
