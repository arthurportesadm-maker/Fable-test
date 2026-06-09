"""Demo: guarding plain Python tools with the Tracerail SDK.

Run from the repo root:
    python examples/demo_agent.py

Then inspect what happened:
    tracerail log -v --audit demo-audit.jsonl
    tracerail verify --audit demo-audit.jsonl
"""

from tracerail import Guard, ToolDenied, guard_tool

guard = Guard.from_files(
    "examples/policies.yaml",
    audit_path="demo-audit.jsonl",
    state_path="demo-state.db",
    session="demo",
)


@guard_tool(guard)
def issue_refund(order_id: str, amount: float) -> str:
    return f"refunded ${amount:.2f} for order {order_id}"


@guard_tool(guard, name="db_query")
def db_query(query: str, env: str) -> str:
    return f"ran {query!r} on {env}"


def attempt(label, fn, *args, **kwargs):
    try:
        print(f"  OK   {label}: {fn(*args, **kwargs)}")
    except ToolDenied as exc:
        print(f"  DENY {label}: {exc}")


if __name__ == "__main__":
    print("Tracerail demo (session 'demo')")
    attempt("small refund", issue_refund, "order-1", 42.0)
    attempt("prod db query", db_query, "DELETE FROM users", env="prod-us-1")
    attempt("staging db query", db_query, "SELECT 1", env="staging")
    print("\nNow try a refund above the $100 cap — it will wait for a human.")
    print("In another terminal: tracerail approvals --state demo-state.db")
    print("then: tracerail approve <id> --state demo-state.db --audit demo-audit.jsonl")
    attempt("big refund", issue_refund, "order-2", 2500.0)
