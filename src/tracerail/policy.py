"""Declarative policy engine for agent tool calls.

Policies are defined in YAML and evaluated in order; the first policy whose
``match`` block fits the tool call wins. Each policy yields one of three
effects: ``allow``, ``deny`` or ``require_approval``. Policies may also carry
``constraints`` (per-session call caps and numeric argument limits) that, when
violated, trigger the policy's ``on_violation`` effect instead.
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field
from typing import Any

import yaml

ALLOW = "allow"
DENY = "deny"
REQUIRE_APPROVAL = "require_approval"

_VALID_EFFECTS = {ALLOW, DENY, REQUIRE_APPROVAL}


class PolicyError(ValueError):
    """Raised when a policy file is malformed."""


def _dig(args: dict[str, Any], path: str) -> Any:
    """Resolve a dot path like ``payment.amount`` inside a nested dict."""
    current: Any = args
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


@dataclass
class Constraint:
    """Per-policy limits checked against session state."""

    max_calls: int | None = None
    amount_field: str | None = None
    amount_limit: float | None = None

    def amount_of(self, arguments: dict[str, Any]) -> float | None:
        if self.amount_field is None:
            return None
        value = _dig(arguments, self.amount_field)
        try:
            return float(value)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            return None


@dataclass
class Policy:
    name: str
    tool_pattern: str = "*"
    arg_matchers: dict[str, str] = field(default_factory=dict)
    effect: str = ALLOW
    on_violation: str = DENY
    constraint: Constraint | None = None
    reason: str = ""
    timeout_seconds: float | None = None
    on_timeout: str = DENY

    def matches(self, tool: str, arguments: dict[str, Any]) -> bool:
        if not fnmatch.fnmatchcase(tool, self.tool_pattern):
            return False
        for path, pattern in self.arg_matchers.items():
            value = _dig(arguments, path)
            if value is None or not fnmatch.fnmatchcase(str(value), str(pattern)):
                return False
        return True


@dataclass
class PolicySet:
    policies: list[Policy]
    default_effect: str = ALLOW
    redact_fields: list[str] = field(default_factory=list)

    def find(self, tool: str, arguments: dict[str, Any]) -> Policy | None:
        for policy in self.policies:
            if policy.matches(tool, arguments):
                return policy
        return None


def _parse_policy(raw: dict[str, Any], index: int) -> Policy:
    if not isinstance(raw, dict):
        raise PolicyError(f"policy #{index} must be a mapping")
    name = raw.get("name") or f"policy-{index}"
    match = raw.get("match") or {}
    if not isinstance(match, dict):
        raise PolicyError(f"policy {name!r}: 'match' must be a mapping")

    effect = raw.get("effect", ALLOW)
    on_violation = raw.get("on_violation", DENY)
    on_timeout = raw.get("on_timeout", DENY)
    for label, value in (("effect", effect), ("on_violation", on_violation), ("on_timeout", on_timeout)):
        if value not in _VALID_EFFECTS:
            raise PolicyError(f"policy {name!r}: invalid {label} {value!r}")
    if on_timeout == REQUIRE_APPROVAL:
        raise PolicyError(f"policy {name!r}: on_timeout cannot be require_approval")

    constraint = None
    raw_constraints = raw.get("constraints")
    if raw_constraints is not None:
        if not isinstance(raw_constraints, dict):
            raise PolicyError(f"policy {name!r}: 'constraints' must be a mapping")
        max_amount = raw_constraints.get("max_amount") or {}
        constraint = Constraint(
            max_calls=raw_constraints.get("max_calls"),
            amount_field=max_amount.get("field"),
            amount_limit=max_amount.get("limit"),
        )
        if (constraint.amount_field is None) != (constraint.amount_limit is None):
            raise PolicyError(f"policy {name!r}: max_amount needs both 'field' and 'limit'")

    arg_matchers = match.get("args") or {}
    if not isinstance(arg_matchers, dict):
        raise PolicyError(f"policy {name!r}: 'match.args' must be a mapping")

    return Policy(
        name=str(name),
        tool_pattern=str(match.get("tool", "*")),
        arg_matchers={str(k): str(v) for k, v in arg_matchers.items()},
        effect=effect,
        on_violation=on_violation,
        constraint=constraint,
        reason=str(raw.get("reason", "")),
        timeout_seconds=raw.get("timeout_seconds"),
        on_timeout=on_timeout,
    )


def load_policy_set(path: str) -> PolicySet:
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return parse_policy_set(data)


def parse_policy_set(data: dict[str, Any]) -> PolicySet:
    if not isinstance(data, dict):
        raise PolicyError("policy file must be a mapping")
    default_effect = data.get("default", ALLOW)
    if default_effect not in (ALLOW, DENY):
        raise PolicyError(f"invalid default effect {default_effect!r}")
    raw_policies = data.get("policies") or []
    if not isinstance(raw_policies, list):
        raise PolicyError("'policies' must be a list")
    policies = [_parse_policy(raw, i) for i, raw in enumerate(raw_policies)]
    redact = data.get("redact") or []
    if not isinstance(redact, list):
        raise PolicyError("'redact' must be a list of field names")
    return PolicySet(policies=policies, default_effect=default_effect, redact_fields=[str(r) for r in redact])
