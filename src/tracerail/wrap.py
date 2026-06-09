"""Python SDK: guard any callable tool with a decorator."""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable

from .guard import Guard


class ToolDenied(PermissionError):
    """Raised when a guarded tool call is denied by policy or by a human."""

    def __init__(self, tool: str, policy: str, reason: str):
        self.tool = tool
        self.policy = policy
        self.reason = reason
        super().__init__(f"tool {tool!r} denied by policy {policy!r}: {reason or 'no reason given'}")


def guard_tool(guard: Guard, name: str | None = None) -> Callable:
    """Decorate a function so every invocation passes through the Guard.

    Keyword and positional arguments are bound to parameter names so policies
    can match on them (e.g. ``match.args: {amount: "*"}``).
    """

    def decorator(func: Callable) -> Callable:
        tool_name = name or func.__name__
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            bound = signature.bind_partial(*args, **kwargs)
            decision = guard.evaluate(tool_name, dict(bound.arguments))
            if not decision.allowed:
                raise ToolDenied(tool_name, decision.policy, decision.reason)
            return func(*args, **kwargs)

        return wrapper

    return decorator
