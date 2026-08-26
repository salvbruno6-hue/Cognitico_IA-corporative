#!/usr/bin/env python3
"""CLI periférica do ELO; toda decisão passa pelo Control Plane."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.elo_control_plane import ELOControlPlane, PolicyError


def main() -> int:
    parser = argparse.ArgumentParser(prog="elo")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("query", "plan"):
        p = sub.add_parser(name)
        p.add_argument("text")
        p.add_argument("--operation", default="read")
    args = parser.parse_args()
    try:
        core = ELOControlPlane()
        result = core.plan(args.text, args.operation) if args.command == "plan" else core.handle(args.text, args.operation)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except PolicyError as exc:
        print(json.dumps({"decision": "denied", "reason": str(exc)}), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
