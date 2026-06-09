"""Shared runtime state: per-session counters and the approval queue.

SQLite is used so that the agent process (or MCP proxy) and the operator's
CLI can safely share state across processes.
"""

from __future__ import annotations

import json
import sqlite3
import time
import uuid
from dataclasses import dataclass
from typing import Any

PENDING = "pending"
APPROVED = "approved"
DENIED = "denied"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS counters (
    session TEXT NOT NULL,
    key     TEXT NOT NULL,
    count   INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (session, key)
);
CREATE TABLE IF NOT EXISTS approvals (
    id          TEXT PRIMARY KEY,
    created_ts  REAL NOT NULL,
    session     TEXT NOT NULL,
    tool        TEXT NOT NULL,
    arguments   TEXT NOT NULL,
    policy      TEXT NOT NULL,
    reason      TEXT NOT NULL DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'pending',
    resolved_ts REAL,
    resolved_by TEXT
);
"""


@dataclass
class Approval:
    id: str
    created_ts: float
    session: str
    tool: str
    arguments: dict[str, Any]
    policy: str
    reason: str
    status: str
    resolved_ts: float | None = None
    resolved_by: str | None = None


def _row_to_approval(row: sqlite3.Row) -> Approval:
    return Approval(
        id=row["id"],
        created_ts=row["created_ts"],
        session=row["session"],
        tool=row["tool"],
        arguments=json.loads(row["arguments"]),
        policy=row["policy"],
        reason=row["reason"],
        status=row["status"],
        resolved_ts=row["resolved_ts"],
        resolved_by=row["resolved_by"],
    )


class StateStore:
    def __init__(self, path: str):
        self.path = path
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    # -- counters ----------------------------------------------------------

    def increment(self, session: str, key: str) -> int:
        """Increment a per-session counter and return the new value."""
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO counters (session, key, count) VALUES (?, ?, 1) "
                "ON CONFLICT(session, key) DO UPDATE SET count = count + 1",
                (session, key),
            )
            row = conn.execute(
                "SELECT count FROM counters WHERE session = ? AND key = ?", (session, key)
            ).fetchone()
            return int(row["count"])

    # -- approvals ---------------------------------------------------------

    def create_approval(
        self, *, session: str, tool: str, arguments: dict[str, Any], policy: str, reason: str = ""
    ) -> Approval:
        approval_id = uuid.uuid4().hex[:12]
        now = time.time()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO approvals (id, created_ts, session, tool, arguments, policy, reason) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (approval_id, now, session, tool, json.dumps(arguments, ensure_ascii=False), policy, reason),
            )
        return Approval(
            id=approval_id,
            created_ts=now,
            session=session,
            tool=tool,
            arguments=arguments,
            policy=policy,
            reason=reason,
            status=PENDING,
        )

    def get_approval(self, approval_id: str) -> Approval | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM approvals WHERE id = ?", (approval_id,)).fetchone()
        return _row_to_approval(row) if row else None

    def list_approvals(self, status: str | None = PENDING) -> list[Approval]:
        query = "SELECT * FROM approvals"
        params: tuple[Any, ...] = ()
        if status:
            query += " WHERE status = ?"
            params = (status,)
        query += " ORDER BY created_ts"
        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [_row_to_approval(row) for row in rows]

    def resolve_approval(self, approval_id: str, status: str, resolved_by: str = "cli") -> Approval | None:
        if status not in (APPROVED, DENIED):
            raise ValueError(f"invalid resolution {status!r}")
        with self._connect() as conn:
            cursor = conn.execute(
                "UPDATE approvals SET status = ?, resolved_ts = ?, resolved_by = ? "
                "WHERE id = ? AND status = 'pending'",
                (status, time.time(), resolved_by, approval_id),
            )
            if cursor.rowcount == 0:
                return None
        return self.get_approval(approval_id)

    def wait_for_resolution(
        self, approval_id: str, timeout_seconds: float | None, poll_interval: float = 0.5
    ) -> str:
        """Block until an approval is resolved; returns final status (or 'pending' on timeout)."""
        deadline = None if timeout_seconds is None else time.time() + timeout_seconds
        while True:
            approval = self.get_approval(approval_id)
            if approval is None:
                return DENIED
            if approval.status != PENDING:
                return approval.status
            if deadline is not None and time.time() >= deadline:
                return PENDING
            time.sleep(poll_interval)
