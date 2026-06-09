"""The Guard ties together policies, state and the audit log.

``Guard.evaluate`` is the single enforcement point: every tool call goes in,
a ``Decision`` comes out, and an audit record is always written — including
for calls that were denied or are waiting on a human.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

from .audit import AuditLog, redact
from .policy import ALLOW, DENY, REQUIRE_APPROVAL, Policy, PolicySet, load_policy_set
from .state import APPROVED, PENDING, StateStore


@dataclass
class Decision:
    effect: str  # allow | deny
    policy: str
    reason: str = ""
    approval_id: str | None = None

    @property
    def allowed(self) -> bool:
        return self.effect == ALLOW


class Guard:
    def __init__(
        self,
        policy_set: PolicySet,
        audit: AuditLog,
        state: StateStore,
        session: str | None = None,
        approval_poll_interval: float = 0.5,
    ):
        self.policy_set = policy_set
        self.audit = audit
        self.state = state
        self.session = session or uuid.uuid4().hex[:12]
        self.approval_poll_interval = approval_poll_interval

    @classmethod
    def from_files(
        cls,
        policies_path: str,
        audit_path: str = "tracerail-audit.jsonl",
        state_path: str = "tracerail-state.db",
        session: str | None = None,
    ) -> "Guard":
        return cls(
            policy_set=load_policy_set(policies_path),
            audit=AuditLog(audit_path),
            state=StateStore(state_path),
            session=session,
        )

    def evaluate(self, tool: str, arguments: dict[str, Any] | None = None) -> Decision:
        arguments = arguments or {}
        policy = self.policy_set.find(tool, arguments)

        if policy is None:
            decision = Decision(effect=self.policy_set.default_effect, policy="default")
        else:
            decision = self._apply_policy(policy, tool, arguments)

        self._record(tool, arguments, decision)
        return decision

    def _apply_policy(self, policy: Policy, tool: str, arguments: dict[str, Any]) -> Decision:
        effect = policy.effect
        reason = policy.reason

        constraint = policy.constraint
        if constraint is not None:
            if constraint.max_calls is not None:
                calls = self.state.increment(self.session, f"calls:{policy.name}")
                if calls > constraint.max_calls:
                    effect = policy.on_violation
                    reason = f"call cap exceeded ({calls} > {constraint.max_calls})"
            if constraint.amount_limit is not None and effect == policy.effect:
                amount = constraint.amount_of(arguments)
                if amount is None or amount > constraint.amount_limit:
                    effect = policy.on_violation
                    reason = f"amount {amount} exceeds limit {constraint.amount_limit}"

        if effect == REQUIRE_APPROVAL:
            return self._escalate(policy, tool, arguments, reason)
        return Decision(effect=effect, policy=policy.name, reason=reason)

    def _escalate(self, policy: Policy, tool: str, arguments: dict[str, Any], reason: str) -> Decision:
        safe_args = redact(arguments, self.policy_set.redact_fields)
        approval = self.state.create_approval(
            session=self.session, tool=tool, arguments=safe_args, policy=policy.name, reason=reason
        )
        self.audit.append(
            session=self.session,
            tool=tool,
            arguments=safe_args,
            decision="approval_requested",
            policy=policy.name,
            reason=reason,
            kind="approval",
            extra={"approval_id": approval.id},
        )
        status = self.state.wait_for_resolution(
            approval.id, policy.timeout_seconds, self.approval_poll_interval
        )
        if status == APPROVED:
            return Decision(ALLOW, policy.name, "approved by human", approval_id=approval.id)
        if status == PENDING:  # timed out
            self.state.resolve_approval(approval.id, "denied", resolved_by="timeout")
            return Decision(
                policy.on_timeout, policy.name, "approval timed out", approval_id=approval.id
            )
        return Decision(DENY, policy.name, "denied by human", approval_id=approval.id)

    def _record(self, tool: str, arguments: dict[str, Any], decision: Decision) -> None:
        extra = {"approval_id": decision.approval_id} if decision.approval_id else None
        self.audit.append(
            session=self.session,
            tool=tool,
            arguments=redact(arguments, self.policy_set.redact_fields),
            decision=decision.effect,
            policy=decision.policy,
            reason=decision.reason,
            extra=extra,
        )
