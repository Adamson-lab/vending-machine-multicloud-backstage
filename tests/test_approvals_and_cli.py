import json

from conftest import make
from vendingctl import approvals, cli


def test_gate_requires_each_role_team():
    team_for = {"security": "sec-arch", "finance": "finops"}
    ok, missing = approvals.evaluate_gate({"security", "finance"}, [{"reviewer": "a", "teams": ["sec-arch"]}], team_for)
    assert not ok and missing == ["finance"]
    ok, missing = approvals.evaluate_gate({"security", "finance"},
                                          [{"reviewer": "a", "teams": ["sec-arch"]}, {"reviewer": "b", "teams": ["finops"]}], team_for)
    assert ok and missing == []


def test_gate_unknown_role_fails_closed():
    ok, missing = approvals.evaluate_gate({"compliance"}, [{"reviewer": "a", "teams": ["x"]}], {})
    assert not ok and missing == ["compliance"]


def test_gate_with_nothing_required_passes():
    assert approvals.evaluate_gate(set(), [], {}) == (True, [])


def test_opa_input_has_computed_fields(prod, config):
    inp = approvals.opa_input(prod, config)
    assert inp["request"]["key"] == "payments-api-prod" and inp["request"]["owner_alias"] == "ada-owner"
    assert inp["request"]["lifecycle"] == "active"
    assert inp["config"]["approvals"]["finance_budget_threshold_usd"] == 10000


def test_cli_validate_ok_and_compile_check(tmp_path, capsys):
    assert cli.main(["validate"]) == 0
    assert cli.main(["compile", "--check"]) == 0


def test_cli_validate_fails_on_bad_request(tmp_path, capsys):
    (tmp_path / "bad-name-prod.yaml").write_text("workload_name: x\n")
    assert cli.main(["--requests", str(tmp_path), "validate"]) == 1
    assert "FAIL" in capsys.readouterr().err


def test_cli_compile_refuses_invalid(tmp_path, capsys):
    (tmp_path / "bad.yaml").write_text("workload_name: x\n")
    assert cli.main(["--requests", str(tmp_path), "compile", "--out", str(tmp_path / "out")]) == 1


def test_cli_gate(tmp_path, capsys):
    (tmp_path / "r.json").write_text(json.dumps(["security"]))
    (tmp_path / "a.json").write_text(json.dumps([{"reviewer": "x", "teams": ["sec"]}]))
    (tmp_path / "t.json").write_text(json.dumps({"security": "sec"}))
    args = ["gate", "--required", str(tmp_path / "r.json"), "--approvals", str(tmp_path / "a.json"), "--teams", str(tmp_path / "t.json")]
    assert cli.main(args) == 0


def rv(user, state):
    return {"user": {"login": user}, "state": state}


def test_latest_review_per_user_wins():
    reviews = [rv("bob", "APPROVED"), rv("bob", "CHANGES_REQUESTED"), rv("cat", "CHANGES_REQUESTED"), rv("cat", "APPROVED")]
    assert approvals.approved_reviewers(reviews, "alice") == ["cat"]


def test_author_cannot_approve_own_request_case_insensitive():
    assert approvals.approved_reviewers([rv("Alice", "APPROVED"), rv("bob", "APPROVED")], "alice") == ["bob"]


def test_comments_do_not_cancel_or_grant_approval():
    assert approvals.approved_reviewers([rv("bob", "APPROVED"), rv("bob", "COMMENTED")], "x") == ["bob"]
    assert approvals.approved_reviewers([rv("bob", "COMMENTED")], "x") == []


def test_dismissed_approval_is_removed():
    assert approvals.approved_reviewers([rv("bob", "APPROVED"), rv("bob", "DISMISSED")], "x") == []


def test_reviews_with_missing_user_are_ignored():
    assert approvals.approved_reviewers([{"state": "APPROVED", "user": None}, {"state": "APPROVED"}], "x") == []


def test_cli_reviewers(tmp_path, capsys):
    (tmp_path / "r.json").write_text(json.dumps([rv("bob", "APPROVED"), rv("alice", "APPROVED")]))
    assert cli.main(["reviewers", "--reviews", str(tmp_path / "r.json"), "--author", "alice"]) == 0
    assert capsys.readouterr().out.split() == ["bob"]
