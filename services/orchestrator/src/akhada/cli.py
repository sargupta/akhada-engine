"""`akhada` CLI entrypoint."""
from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path


def _cmd_library_generate(args: argparse.Namespace) -> int:
    """V0.8 — generate a persona library by Pro-tier biography generation."""
    from akhada.persona_registry.biography.generator import generate_library
    from akhada.persona_registry.biography.seeds import SEEDS
    from akhada.persona_registry.loader import write_jsonl
    from akhada.telemetry.otel import init_logging

    log = init_logging()

    if args.n is not None:
        seeds = SEEDS[: args.n]
    else:
        seeds = SEEDS

    log.info("library generate: %d seeds → %s", len(seeds), args.output)
    results = asyncio.run(generate_library(seeds))

    ok = [r.persona for r in results if r.persona is not None]
    failed = [(r.seed_id, r.error) for r in results if r.persona is None]

    out = Path(args.output)
    write_jsonl(ok, out)

    log.info("wrote %d personas to %s", len(ok), out)
    for sid, err in failed:
        log.warning("FAILED %s :: %s", sid, (err or "")[:200])

    print(f"\nDone. {len(ok)} ok, {len(failed)} failed → {out}")
    return 0 if not failed else 1


def _cmd_library_show(args: argparse.Namespace) -> int:
    from akhada.persona_registry.loader import read_jsonl

    personas = read_jsonl(Path(args.path))
    print(f"loaded {len(personas)} personas from {args.path}\n")
    for p in personas:
        d = p.demographic
        print(f"- {p.id} | {d.age_band} {d.gender} | {d.religion}/{d.caste_cat} | "
              f"{d.education} | {d.occupation} | {d.urban_rural} {d.state}")
    return 0


def _cmd_debate_run(args: argparse.Namespace) -> int:
    from akhada.flows.debate import run_debate
    from akhada.persona_registry.fixtures import get_panel

    panel = get_panel(args.agents)
    result = run_debate(args.topic, panel)
    print(result.article)
    print()
    print(result.conclusive_remark)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="akhada")
    sub = parser.add_subparsers(dest="cmd")

    # debate run ----------------------------------------------------------
    debate = sub.add_parser("debate", help="run a debate (offline stub)")
    debate_sub = debate.add_subparsers(dest="debate_cmd")
    run = debate_sub.add_parser("run", help="run one debate")
    run.add_argument("--topic", required=True)
    run.add_argument("--agents", type=int, default=50)
    run.add_argument("--rounds", type=int, default=3)
    run.add_argument("--language", default="en-IN")

    # library --------------------------------------------------------------
    lib = sub.add_parser("library", help="manage the persona library")
    lib_sub = lib.add_subparsers(dest="library_cmd")
    gen = lib_sub.add_parser("generate", help="Pro-tier biography generation")
    gen.add_argument("--n", type=int, default=None,
                     help="number of seeds (default: all SEEDS)")
    gen.add_argument(
        "--output", required=True,
        help="output JSONL path, e.g. data/personas/personas-2026.Q2.1.jsonl",
    )
    show = lib_sub.add_parser("show", help="list personas in a JSONL file")
    show.add_argument("path")

    # eval -----------------------------------------------------------------
    evalp = sub.add_parser("eval", help="run benchmarks")
    evalp.add_argument(
        "bench",
        choices=["bench:diversity", "bench:conformity", "bench:bias-audit", "bench:factual"],
    )

    args = parser.parse_args()

    if args.cmd == "debate" and args.debate_cmd == "run":
        return _cmd_debate_run(args)
    if args.cmd == "library" and args.library_cmd == "generate":
        return _cmd_library_generate(args)
    if args.cmd == "library" and args.library_cmd == "show":
        return _cmd_library_show(args)
    if args.cmd == "eval":
        print(f"V0 stub — {args.bench}: pending V1.")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
