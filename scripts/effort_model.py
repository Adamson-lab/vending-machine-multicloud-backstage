#!/usr/bin/env python3
"""Business case for automated vending: effort saved versus cost to build and run.

monthly manual cost    = requests x [ sum_cloud(mix_c x minutes_c) + rework_rate x rework_minutes ] / 60 x rate
monthly automated cost = requests x [ review_minutes + failure_rate x failure_minutes ] / 60 x rate
monthly platform cost  = build_cost / amortisation_months + run_cost
net monthly saving     = manual - automated - platform
break-even requests/mo = platform / (saving per request)    (None if the automation saves nothing)

The shipped inputs are ILLUSTRATIVE and the tool says so. The point of the model is the shape of the
curve (fixed platform cost against a per-request saving), not the numbers.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def per_request_minutes_manual(inp: dict) -> float:
    m = inp["manual"]
    base = sum(inp["mix_of_clouds_per_request"][c] * mins for c, mins in m["minutes_per_request_by_cloud"].items())
    return base + m["rework_rate"] * m["rework_minutes"]


def per_request_minutes_automated(inp: dict) -> float:
    a = inp["automated"]
    return a["minutes_per_request_review"] + a["failure_rate"] * a["failure_minutes"]


def scenario(inp: dict, requests: int) -> dict:
    rate = inp["loaded_rate_per_hour"] / 60
    manual = requests * per_request_minutes_manual(inp) * rate
    auto = requests * per_request_minutes_automated(inp) * rate
    p = inp["platform"]
    platform = p["build_cost_one_off"] / p["amortisation_months"] + p["run_cost_per_month"]
    return {"requests": requests, "manual": manual, "automated": auto, "platform": platform, "net": manual - auto - platform}


def break_even_requests(inp: dict):
    saving = (per_request_minutes_manual(inp) - per_request_minutes_automated(inp)) * inp["loaded_rate_per_hour"] / 60
    p = inp["platform"]
    platform = p["build_cost_one_off"] / p["amortisation_months"] + p["run_cost_per_month"]
    return None if saving <= 0 else platform / saving


def report(inp: dict) -> str:
    lines = []
    if inp.get("illustrative"):
        lines += ["WARNING: inputs are ILLUSTRATIVE PLACEHOLDERS, not measurements.", ""]
    lines += [f"Manual minutes per request:    {per_request_minutes_manual(inp):.1f}",
              f"Automated minutes per request: {per_request_minutes_automated(inp):.1f}"]
    be = break_even_requests(inp)
    lines += [f"Break-even requests per month: {be:.1f}" if be is not None else "Break-even: never (automation saves no time)", "",
              "| Requests/month | Manual | Automated | Platform | Net saving/month |", "|---|---|---|---|---|"]
    for n in inp["requests_per_month_scenarios"]:
        s = scenario(inp, n)
        lines.append(f"| {n} | {s['manual']:,.0f} | {s['automated']:,.0f} | {s['platform']:,.0f} | {s['net']:,.0f} |")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="?", default=str(Path(__file__).resolve().parent.parent / "docs/08-cost-and-finance/effort-inputs.example.yaml"))
    print(report(yaml.safe_load(Path(ap.parse_args(argv).inputs).read_text(encoding="utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
