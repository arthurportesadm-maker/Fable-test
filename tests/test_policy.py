import pytest

from tracerail.policy import PolicyError, parse_policy_set


def test_first_match_wins():
    ps = parse_policy_set({
        "policies": [
            {"name": "a", "match": {"tool": "x"}, "effect": "deny"},
            {"name": "b", "match": {"tool": "*"}, "effect": "allow"},
        ]
    })
    assert ps.find("x", {}).name == "a"
    assert ps.find("y", {}).name == "b"


def test_glob_matching_on_tool_and_args():
    ps = parse_policy_set({
        "policies": [{"name": "p", "match": {"tool": "db_*", "args": {"env": "prod*"}}, "effect": "deny"}]
    })
    assert ps.find("db_query", {"env": "prod-us"}) is not None
    assert ps.find("db_query", {"env": "staging"}) is None
    assert ps.find("db_query", {}) is None  # missing arg never matches
    assert ps.find("http_get", {"env": "prod"}) is None


def test_dot_path_args():
    ps = parse_policy_set({
        "policies": [{"name": "p", "match": {"args": {"payment.currency": "USD"}}, "effect": "deny"}]
    })
    assert ps.find("t", {"payment": {"currency": "USD"}}) is not None
    assert ps.find("t", {"payment": {"currency": "BRL"}}) is None


def test_no_match_falls_back_to_default():
    ps = parse_policy_set({"default": "deny", "policies": []})
    assert ps.find("anything", {}) is None
    assert ps.default_effect == "deny"


@pytest.mark.parametrize("bad", [
    {"policies": [{"name": "p", "effect": "explode"}]},
    {"policies": [{"name": "p", "constraints": {"max_amount": {"field": "x"}}}]},
    {"default": "require_approval"},
    {"policies": [{"name": "p", "on_timeout": "require_approval"}]},
])
def test_malformed_policies_rejected(bad):
    with pytest.raises(PolicyError):
        parse_policy_set(bad)
