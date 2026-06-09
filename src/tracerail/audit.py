"""Tamper-evident audit log.

Records are appended to a JSONL file where each record embeds the SHA-256
hash of the previous record, forming a hash chain. Any retroactive edit,
deletion or reordering breaks the chain and is detected by ``verify_chain``.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from dataclasses import dataclass
from typing import Any, BinaryIO, Iterator

try:
    import fcntl
except ImportError:  # Windows: no cross-process lock, thread lock still applies
    fcntl = None  # type: ignore[assignment]

GENESIS = "0" * 64


def _canonical(record: dict[str, Any]) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def record_hash(record: dict[str, Any]) -> str:
    body = {k: v for k, v in record.items() if k != "hash"}
    return hashlib.sha256(_canonical(body)).hexdigest()


def redact(arguments: Any, fields: list[str]) -> Any:
    """Recursively replace values of sensitive keys before they are persisted."""
    if isinstance(arguments, dict):
        return {
            key: "[REDACTED]" if key in fields else redact(value, fields)
            for key, value in arguments.items()
        }
    if isinstance(arguments, list):
        return [redact(item, fields) for item in arguments]
    return arguments


@dataclass
class ChainStatus:
    ok: bool
    records: int
    error: str = ""


def _tail_hash(fh: BinaryIO) -> str:
    """Hash of the last record in an open log file (GENESIS when empty)."""
    fh.seek(0, os.SEEK_END)
    size = fh.tell()
    if size == 0:
        return GENESIS
    # Read backwards in growing chunks until the final line is complete.
    chunk = 65536
    while True:
        start = max(0, size - chunk)
        fh.seek(start)
        data = fh.read(size - start)
        lines = data.strip().splitlines()
        if start == 0 or len(lines) > 1:
            return json.loads(lines[-1]).get("hash", GENESIS) if lines else GENESIS
        chunk *= 4


class AuditLog:
    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        parent = os.path.dirname(os.path.abspath(path))
        os.makedirs(parent, exist_ok=True)

    def iter_records(self) -> Iterator[dict[str, Any]]:
        if not os.path.exists(self.path):
            return
        with open(self.path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def append(
        self,
        *,
        session: str,
        tool: str,
        arguments: Any,
        decision: str,
        policy: str,
        reason: str = "",
        kind: str = "tool_call",
        extra: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        with self._lock:
            # The previous hash is re-read under an exclusive file lock so
            # several processes (proxy, CLI, multiple agents) can share one
            # log without breaking the chain.
            with open(self.path, "a+b") as fh:
                if fcntl is not None:
                    fcntl.flock(fh, fcntl.LOCK_EX)
                record: dict[str, Any] = {
                    "ts": time.time(),
                    "kind": kind,
                    "session": session,
                    "tool": tool,
                    "arguments": arguments,
                    "decision": decision,
                    "policy": policy,
                    "reason": reason,
                    "prev_hash": _tail_hash(fh),
                }
                if extra:
                    record["extra"] = extra
                record["hash"] = record_hash(record)
                fh.seek(0, os.SEEK_END)
                fh.write((json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8"))
            return record

    def verify_chain(self) -> ChainStatus:
        prev = GENESIS
        count = 0
        for index, record in enumerate(self.iter_records()):
            if record.get("prev_hash") != prev:
                return ChainStatus(False, count, f"record {index}: broken link to previous record")
            if record_hash(record) != record.get("hash"):
                return ChainStatus(False, count, f"record {index}: contents do not match hash")
            prev = record["hash"]
            count += 1
        return ChainStatus(True, count)
