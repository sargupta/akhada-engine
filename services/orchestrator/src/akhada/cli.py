"""`akhada` CLI entrypoint (V0 stub).

V1 commands per plan §16:
  akhada eval bench:diversity
  akhada eval bench:factual
  akhada eval bench:conformity
  akhada eval bench:bias-audit
  akhada debate run --topic "..." --agents 500 --rounds 3 --language hi-IN
"""
from __future__ import annotations

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(prog="akhada")
    sub = parser.add_subparsers(dest="cmd")

    debate = sub.add_parser("debate", help="run a debate")
    debate_sub = debate.add_subparsers(dest="debate_cmd")
    run = debate_sub.add_parser("run", help="run one debate")
    run.add_argument("--topic", required=True)
    run.add_argument("--agents", type=int, default=50)
    run.add_argument("--rounds", type=int, default=3)
    run.add_argument("--language", default="en-IN")

    evalp = sub.add_parser("eval", help="run benchmarks")
    evalp.add_argument("bench", choices=["bench:diversity", "bench:conformity",
                                          "bench:bias-audit", "bench:factual"])

    args = parser.parse_args()

    if args.cmd == "debate" and args.debate_cmd == "run":
        from akhada.flows.debate import run_debate
        from akhada.persona_registry.fixtures import get_panel

        panel = get_panel(args.agents)
        result = run_debate(args.topic, panel)
        print(result.article)
        print()
        print(result.conclusive_remark)
        return 0

    if args.cmd == "eval":
        print(f"V0 stub — {args.bench}: pending V1.")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
