"""Command line interface: vendingctl validate | compile | expire | input | gate."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

from . import approvals, compile as comp, expire as exp, rules
from .model import ROOT, Request, load_config, load_requests, load_yaml


def _load(args):
    cfg = load_config(Path(args.config) if args.config else None)
    reqs = load_requests(Path(args.requests))
    return cfg, reqs


def cmd_validate(args) -> int:
    cfg, reqs = _load(args)
    problems = rules.check_all(reqs, cfg)
    for path, vs in problems.items():
        print(f"FAIL {path}", file=sys.stderr)
        for v in vs:
            print(f"  - {v}", file=sys.stderr)
    if not problems:
        print(f"OK {len(reqs)} request(s) valid")
    return 1 if problems else 0


def cmd_compile(args) -> int:
    cfg, reqs = _load(args)
    problems = rules.check_all(reqs, cfg)
    if problems:
        print("refusing to compile invalid requests (run validate)", file=sys.stderr)
        return 1
    files = comp.compile_all(reqs, cfg)
    out = Path(args.out)
    if args.check:
        diff = comp.diff_outputs(out, files)
        for line in diff:
            print(line, file=sys.stderr)
        if diff:
            print("generated/ is out of date: run `vendingctl compile`", file=sys.stderr)
        return 1 if diff else 0
    removed = comp.write_outputs(out, files)
    print(f"wrote {len(files)} file(s), removed {len(removed)} stale file(s)")
    return 0


def cmd_expire(args) -> int:
    cfg, reqs = _load(args)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    hits = exp.expired(reqs, today)
    for r, when in hits:
        print(f"expired {r.key} (expired {when.isoformat()})")
        if args.apply:
            r.path.write_text(exp.mark_decommissioning(r, when), encoding="utf-8")
    if not hits:
        print("no expired sandboxes")
    return 0


def cmd_input(args) -> int:
    cfg = load_config(Path(args.config) if args.config else None)
    req = Request(Path(args.file), load_yaml(Path(args.file)))
    print(json.dumps(approvals.opa_input(req, cfg), indent=2, sort_keys=True))
    return 0


def cmd_gate(args) -> int:
    required = set(json.loads(Path(args.required).read_text()))
    given = json.loads(Path(args.approvals).read_text())
    team_for = json.loads(Path(args.teams).read_text())
    ok, missing = approvals.evaluate_gate(required, given, team_for)
    print("approvals satisfied" if ok else f"missing approvals: {', '.join(missing)}")
    return 0 if ok else 1


def cmd_reviewers(args) -> int:
    reviews = json.loads(Path(args.reviews).read_text())
    for user in approvals.approved_reviewers(reviews, args.author):
        print(user)
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="vendingctl")
    p.add_argument("--config", default=None)
    p.add_argument("--requests", default=str(ROOT / "requests"))
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    c = sub.add_parser("compile")
    c.add_argument("--out", default=str(ROOT / "generated"))
    c.add_argument("--check", action="store_true")
    c.set_defaults(fn=cmd_compile)
    e = sub.add_parser("expire")
    e.add_argument("--today", default=None)
    e.add_argument("--apply", action="store_true")
    e.set_defaults(fn=cmd_expire)
    i = sub.add_parser("input")
    i.add_argument("file")
    i.set_defaults(fn=cmd_input)
    g = sub.add_parser("gate")
    g.add_argument("--required", required=True)
    g.add_argument("--approvals", required=True)
    g.add_argument("--teams", required=True)
    g.set_defaults(fn=cmd_gate)
    r = sub.add_parser("reviewers")
    r.add_argument("--reviews", required=True)
    r.add_argument("--author", required=True)
    r.set_defaults(fn=cmd_reviewers)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
