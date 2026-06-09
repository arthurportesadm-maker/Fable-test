"""Drop-in MCP stdio proxy.

Sits between any MCP client (Claude Desktop, Claude Code, Cursor, ...) and any
MCP server. All JSON-RPC traffic passes through untouched except ``tools/call``
requests, which are gated by the Guard: denied calls never reach the server and
the client receives a structured tool error instead; calls requiring approval
are held until a human resolves them via the CLI.

Usage:
    tracerail proxy --policies policies.yaml -- npx some-mcp-server --flag
"""

from __future__ import annotations

import asyncio
import json
import sys
from typing import Any, Awaitable, Callable

from .guard import Guard

Sender = Callable[[bytes], Awaitable[None]]


def deny_response(request_id: Any, policy: str, reason: str) -> dict[str, Any]:
    text = f"Tool call blocked by Tracerail policy {policy!r}."
    if reason:
        text += f" Reason: {reason}"
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {"content": [{"type": "text", "text": text}], "isError": True},
    }


class ProxyCore:
    """Transport-agnostic message router (kept separate for testability)."""

    def __init__(self, guard: Guard, send_to_server: Sender, send_to_client: Sender):
        self.guard = guard
        self.send_to_server = send_to_server
        self.send_to_client = send_to_client
        self._gates: set[asyncio.Task] = set()

    async def on_client_line(self, line: bytes) -> None:
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            await self.send_to_server(line)
            return
        if isinstance(message, dict) and message.get("method") == "tools/call" and "id" in message:
            # Gate in a separate task so a pending approval does not stall
            # unrelated traffic (pings, list requests, other tool calls).
            task = asyncio.create_task(self._gate(message))
            self._gates.add(task)
            task.add_done_callback(self._gates.discard)
        else:
            await self.send_to_server(line)

    async def _gate(self, message: dict[str, Any]) -> None:
        params = message.get("params") or {}
        tool = params.get("name", "<unknown>")
        arguments = params.get("arguments") or {}
        decision = await asyncio.to_thread(self.guard.evaluate, tool, arguments)
        if decision.allowed:
            await self.send_to_server(json.dumps(message, ensure_ascii=False).encode("utf-8"))
        else:
            response = deny_response(message["id"], decision.policy, decision.reason)
            await self.send_to_client(json.dumps(response, ensure_ascii=False).encode("utf-8"))

    async def on_server_line(self, line: bytes) -> None:
        await self.send_to_client(line)

    async def drain_gates(self) -> None:
        if self._gates:
            await asyncio.gather(*list(self._gates), return_exceptions=True)


async def _pump(reader: asyncio.StreamReader, handler: Callable[[bytes], Awaitable[None]]) -> None:
    while True:
        line = await reader.readline()
        if not line:
            break
        line = line.rstrip(b"\r\n")
        if line:
            await handler(line)


async def run_proxy(guard: Guard, server_command: list[str]) -> int:
    process = await asyncio.create_subprocess_exec(
        *server_command,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=sys.stderr,
    )
    assert process.stdin is not None and process.stdout is not None

    loop = asyncio.get_running_loop()
    stdin_reader = asyncio.StreamReader()
    await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(stdin_reader), sys.stdin)

    client_lock = asyncio.Lock()
    server_lock = asyncio.Lock()

    async def send_to_client(payload: bytes) -> None:
        async with client_lock:
            sys.stdout.buffer.write(payload + b"\n")
            sys.stdout.buffer.flush()

    async def send_to_server(payload: bytes) -> None:
        async with server_lock:
            process.stdin.write(payload + b"\n")
            await process.stdin.drain()

    core = ProxyCore(guard, send_to_server, send_to_client)
    client_pump = asyncio.create_task(_pump(stdin_reader, core.on_client_line))
    server_pump = asyncio.create_task(_pump(process.stdout, core.on_server_line))

    try:
        await asyncio.wait({client_pump, server_pump}, return_when=asyncio.FIRST_COMPLETED)
    finally:
        await core.drain_gates()
        for task in (client_pump, server_pump):
            task.cancel()
        if process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
    return process.returncode or 0
