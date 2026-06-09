import pytest

from tracerail import AuditLog, Guard, StateStore, parse_policy_set

POLICIES = {
    "version": 1,
    "default": "allow",
    "redact": ["password"],
    "policies": [
        {
            "name": "block-prod-db",
            "match": {"tool": "db_*", "args": {"env": "prod*"}},
            "effect": "deny",
            "reason": "no prod access",
        },
        {
            "name": "refund-cap",
            "match": {"tool": "issue_refund"},
            "effect": "allow",
            "constraints": {"max_amount": {"field": "amount", "limit": 100}},
            "on_violation": "require_approval",
            "timeout_seconds": 1,
            "on_timeout": "deny",
        },
        {
            "name": "search-cap",
            "match": {"tool": "web_search"},
            "effect": "allow",
            "constraints": {"max_calls": 2},
            "on_violation": "deny",
        },
    ],
}


@pytest.fixture
def guard(tmp_path):
    return Guard(
        policy_set=parse_policy_set(POLICIES),
        audit=AuditLog(str(tmp_path / "audit.jsonl")),
        state=StateStore(str(tmp_path / "state.db")),
        session="test",
        approval_poll_interval=0.05,
    )
