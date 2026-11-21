# Business case and cost model

**Status: model structure with placeholder inputs. No figure here is a measurement or a forecast.** Replace `effort-inputs.example.yaml` with your own baseline, then run `python3 scripts/effort_model.py <file>`.

## Model
```
monthly manual cost    = requests x [ sum over clouds (mix x minutes) + rework rate x rework minutes ] / 60 x rate
monthly automated cost = requests x [ review minutes + failure rate x failure minutes ] / 60 x rate
monthly platform cost  = build cost / amortisation months + run cost
net monthly saving     = manual - automated - platform
break-even requests    = platform cost / saving per request
```

## What the structure implies (conditional on the inputs)
- The platform cost is fixed; the saving is per request. So there is a **break-even volume**. With the placeholder inputs it is roughly 40 requests a month; below it the automation costs more than it saves in effort.
- Therefore the case should be argued on **control, consistency and auditability** for low-volume estates, and on **effort** only for high-volume ones.
- Rework and failure rates matter: a manual process with high rework or an automated one with many manual interventions moves break-even materially. Measure them before arguing.

## Drivers and levers
| Driver | Lever |
|---|---|
| Build cost | Reuse Backstage and AFT; keep the engine small |
| Run cost | Fewer moving parts, shared runners |
| Manual effort per request | Measure honestly; include follow-ups and rework |
| Review time | Approval routing that asks only the relevant roles |
| Failure rate | Tests, sandbox rehearsals, clear runbooks |

## Benefits that the effort model does not count
Avoided incidents from unowned or unbudgeted containers, sandbox spend avoided by expiry, faster audits, consistent metadata for chargeback, and reduced key-person risk. These must be measured separately (for example sandbox spend before and after, number of orphaned containers found).

## Costs not in the model
Training, change management, ongoing governance meetings, and the time of approvers. Include them in a real business case.

## Showback and chargeback
Mandatory tags (`cost-center`, `owner`, `environment`, `data-classification`) are the allocation keys. Each cloud's billing export is joined on `cost-center`. How the platform's own cost is allocated is a decision for finance.

## Sensitivity
Run the model with the conservative and optimistic ends of each input. A decision that holds across the range is robust; one that flips needs better data.

See `evidence/effort-model-output.txt` for the output with placeholder inputs (labelled ILLUSTRATIVE by the tool).
