"""Tracerail CLI: run the MCP proxy and operate the control plane."""

from __future__ import annotations

import argparse
import asyncio
import datetime
import json
import sys

from .audit import AuditLog
from .guard import Guard
from .state import APPROVED, DENIED, PENDING, StateStore

DEFAULT_AUDIT = "tracerail-audit.jsonl"
DEFAULT_STATE = "tracerail-state.db"


def _fmt_ts(ts: float | None) -> str:
    if ts is None:
        return "-"
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--audit", default=DEFAULT_AUDIT, help="audit log path (JSONL)")
    parser.add_argument("--state", default=DEFAULT_STATE, help="state database path (SQLite)")


def cmd_proxy(args: argparse.Namespace) -> int:
    if not args.server_command:
        print("error: missing MCP server command after '--'", file=sys.stderr)
        return 2
    guard = Guard.from_files(args.policies, args.audit, args.state, session=args.session)
    print(f"[tracerail] session {guard.session} guarding: {' '.join(args.server_command)}", file=sys.stderr)
    return asyncio.run(asyncio.wait_for(run_proxy_entry(guard, args.server_command), timeout=None))


async def run_proxy_entry(guard: Guard, command: list[str]) -> int:
    from .mcp_proxy import run_proxy

    return await run_proxy(guard, command)


def cmd_approvals(args: argparse.Namespace) -> int:
    store = StateStore(args.state)
    status = None if args.all else PENDING
    approvals = store.list_approvals(status)
    if not approvals:
        print("no approvals" if args.all else "no pending approvals")
        return 0
    for a in approvals:
        print(f"{a.id}  [{a.status:8}]  {_fmt_ts(a.created_ts)}  {a.tool}  policy={a.policy}")
        print(f"              args: {json.dumps(a.arguments, ensure_ascii=False)}")
        if a.reason:
            print(f"              reason: {a.reason}")
    return 0


def _resolve(args: argparse.Namespace, status: str) -> int:
    store = StateStore(args.state)
    approval = store.resolve_approval(args.id, status, resolved_by=args.by)
    if approval is None:
        print(f"error: approval {args.id!r} not found or already resolved", file=sys.stderr)
        return 1
    AuditLog(args.audit).append(
        session=approval.session,
        tool=approval.tool,
        arguments=approval.arguments,
        decision=f"approval_{status}",
        policy=approval.policy,
        reason=f"resolved by {args.by}",
        kind="approval",
        extra={"approval_id": approval.id},
    )
    print(f"{approval.id} {status}: {approval.tool}")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    log = AuditLog(args.audit)
    records = list(log.iter_records())
    for record in records[-args.tail:] if args.tail else records:
        when = _fmt_ts(record.get("ts"))
        print(
            f"{when}  {record.get('decision', '?'):20}  {record.get('tool', '?'):24}  "
            f"policy={record.get('policy', '?')}  session={record.get('session', '?')}"
        )
        if args.verbose:
            print(f"  args: {json.dumps(record.get('arguments'), ensure_ascii=False)}")
            if record.get("reason"):
                print(f"  reason: {record['reason']}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    status = AuditLog(args.audit).verify_chain()
    if status.ok:
        print(f"OK: audit chain intact ({status.records} records)")
        return 0
    print(f"TAMPERED: {status.error} (verified {status.records} records before failure)")
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracerail",
        description="Control plane for AI agent actions: audit, policies and approval gates.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_proxy = sub.add_parser("proxy", help="run a guarded MCP stdio proxy in front of a server")
    p_proxy.add_argument("--policies", required=True, help="policy YAML file")
    p_proxy.add_argument("--session", default=None, help="session id (default: random)")
    _add_common(p_proxy)
    p_proxy.add_argument("server_command", nargs=argparse.REMAINDER, metavar="-- server command",
                         help="MCP server command, after '--'")
    p_proxy.set_defaults(func=cmd_proxy)

    p_list = sub.add_parser("approvals", help="list approval requests")
    p_list.add_argument("--all", action="store_true", help="include resolved approvals")
    _add_common(p_list)
    p_list.set_defaults(func=cmd_approvals)

    for name, status in (("approve", APPROVED), ("deny", DENIED)):
        p = sub.add_parser(name, help=f"{name} a pending action")
        p.add_argument("id", help="approval id")
        p.add_argument("--by", default="cli", help="who resolved it (for the audit trail)")
        _add_common(p)
        p.set_defaults(func=lambda a, s=status: _resolve(a, s))

    p_log = sub.add_parser("log", help="show the audit trail")
    p_log.add_argument("--tail", type=int, default=0, help="show only the last N records")
    p_log.add_argument("-v", "--verbose", action="store_true", help="include arguments and reasons")
    _add_common(p_log)
    p_log.set_defaults(func=cmd_log)

    p_verify = sub.add_parser("verify", help="verify the audit chain integrity")
    _add_common(p_verify)
    p_verify.set_defaults(func=cmd_verify)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if getattr(args, "server_command", None) and args.server_command[0] == "--":
        args.server_command = args.server_command[1:]
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
