import sys
from pathlib import Path

import yaml

from vendingctl.model import ROOT

sys.path.insert(0, str(ROOT / "scripts"))
import effort_model as em  # noqa: E402

INP = {
    "loaded_rate_per_hour": 60,
    "manual": {"minutes_per_request_by_cloud": {"aws": 60, "azure": 30}, "rework_rate": 0.5, "rework_minutes": 20},
    "automated": {"minutes_per_request_review": 10, "failure_rate": 0.1, "failure_minutes": 30},
    "mix_of_clouds_per_request": {"aws": 1.0, "azure": 0.5},
    "platform": {"build_cost_one_off": 2400, "amortisation_months": 24, "run_cost_per_month": 100},
}


def test_minutes_hand_computed():
    assert em.per_request_minutes_manual(INP) == 60 * 1.0 + 30 * 0.5 + 0.5 * 20   # 85
    assert em.per_request_minutes_automated(INP) == 10 + 0.1 * 30                  # 13


def test_scenario_hand_computed():
    s = em.scenario(INP, 10)
    assert s["manual"] == 10 * 85 * 1.0 and s["automated"] == 10 * 13 * 1.0
    assert s["platform"] == 2400 / 24 + 100 == 200
    assert s["net"] == 850 - 130 - 200


def test_break_even_is_where_net_crosses_zero():
    be = em.break_even_requests(INP)
    assert abs(em.scenario(INP, be)["net"]) < 1e-6
    assert em.scenario(INP, be * 2)["net"] > 0 > em.scenario(INP, be / 2)["net"]


def test_no_saving_means_no_break_even():
    worse = {**INP, "automated": {"minutes_per_request_review": 500, "failure_rate": 0, "failure_minutes": 0}}
    assert em.break_even_requests(worse) is None
    assert "never" in em.report({**worse, "requests_per_month_scenarios": [5]})


def test_example_inputs_are_flagged_illustrative():
    inp = yaml.safe_load((ROOT / "docs/08-cost-and-finance/effort-inputs.example.yaml").read_text())
    assert inp["illustrative"] is True and "ILLUSTRATIVE" in em.report(inp)
