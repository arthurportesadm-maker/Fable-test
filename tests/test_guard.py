import threading

from tracerail import ToolDenied, guard_tool
from tracerail.state import APPROVED


def test_default_allow_and_explicit_deny(guard):
    assert guard.evaluate("unknown_tool", {}).allowed
    decision = guard.evaluate("db_query", {"env": "prod-eu"})
    assert not decision.allowed and decision.policy == "block-prod-db"


def test_amount_within_limit_allows(guard):
    assert guard.evaluate("issue_refund", {"amount": 50}).allowed


def test_call_cap_enforced(guard):
    assert guard.evaluate("web_search", {"q": "a"}).allowed
    assert guard.evaluate("web_search", {"q": "b"}).allowed
    third = guard.evaluate("web_search", {"q": "c"})
    assert not third.allowed and "cap exceeded" in third.reason


def test_over_limit_waits_for_approval_then_allows(guard):
    pending = {}

    def approve_when_visible():
        while True:
            approvals = guard.state.list_approvals()
            if approvals:
                pending["args"] = approvals[0].arguments
                guard.state.resolve_approval(approvals[0].id, APPROVED, resolved_by="tester")
                return

    approver = threading.Thread(target=approve_when_visible)
    approver.start()
    decision = guard.evaluate("issue_refund", {"amount": 5000, "password": "x"})
    approver.join()
    assert decision.allowed and decision.reason == "approved by human"
    assert pending["args"]["password"] == "[REDACTED]"  # redacted before humans see it


def test_approval_timeout_denies(guard):
    decision = guard.evaluate("issue_refund", {"amount": 5000})
    assert not decision.allowed and decision.reason == "approval timed out"
    # the timed-out approval is closed, not left dangling
    assert guard.state.list_approvals() == []


def test_every_call_is_audited(guard):
    guard.evaluate("unknown_tool", {})
    guard.evaluate("db_query", {"env": "prod"})
    records = list(guard.audit.iter_records())
    decisions = [r["decision"] for r in records]
    assert decisions == ["allow", "deny"]
    assert guard.audit.verify_chain().ok


def test_guard_tool_decorator(guard):
    @guard_tool(guard, name="db_query")
    def db_query(query, env):
        return "ran"

    assert db_query("SELECT 1", env="staging") == "ran"
    try:
        db_query("DROP TABLE x", env="prod")
        raised = False
    except ToolDenied as exc:
        raised = True
        assert exc.policy == "block-prod-db"
    assert raised
