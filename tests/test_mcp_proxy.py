import asyncio
import json

import pytest

from tracerail.mcp_proxy import ProxyCore


class Recorder:
    def __init__(self):
        self.messages = []

    async def __call__(self, payload: bytes):
        self.messages.append(json.loads(payload))


def run(coro):
    return asyncio.get_event_loop_policy().new_event_loop().run_until_complete(coro)


@pytest.fixture
def wires(guard):
    to_server, to_client = Recorder(), Recorder()
    return ProxyCore(guard, to_server, to_client), to_server, to_client


def encode(message) -> bytes:
    return json.dumps(message).encode()


def test_non_tool_traffic_passes_through(wires):
    core, to_server, to_client = wires

    async def scenario():
        await core.on_client_line(encode({"jsonrpc": "2.0", "id": 1, "method": "initialize"}))
        await core.on_client_line(encode({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        await core.on_server_line(encode({"jsonrpc": "2.0", "id": 1, "result": {}}))
        await core.drain_gates()

    run(scenario())
    assert len(to_server.messages) == 2
    assert to_client.messages == [{"jsonrpc": "2.0", "id": 1, "result": {}}]


def test_allowed_tool_call_is_forwarded(wires):
    core, to_server, to_client = wires
    call = {"jsonrpc": "2.0", "id": 7, "method": "tools/call",
            "params": {"name": "issue_refund", "arguments": {"amount": 10}}}

    async def scenario():
        await core.on_client_line(encode(call))
        await core.drain_gates()

    run(scenario())
    assert to_server.messages == [call]
    assert to_client.messages == []


def test_denied_tool_call_short_circuits(wires):
    core, to_server, to_client = wires
    call = {"jsonrpc": "2.0", "id": 8, "method": "tools/call",
            "params": {"name": "db_query", "arguments": {"env": "prod"}}}

    async def scenario():
        await core.on_client_line(encode(call))
        await core.drain_gates()

    run(scenario())
    assert to_server.messages == []  # never reaches the server
    response = to_client.messages[0]
    assert response["id"] == 8
    assert response["result"]["isError"] is True
    assert "block-prod-db" in response["result"]["content"][0]["text"]


def test_denied_call_still_audited(wires, guard):
    core, _, _ = wires
    call = {"jsonrpc": "2.0", "id": 9, "method": "tools/call",
            "params": {"name": "db_query", "arguments": {"env": "prod"}}}

    async def scenario():
        await core.on_client_line(encode(call))
        await core.drain_gates()

    run(scenario())
    records = list(guard.audit.iter_records())
    assert records[-1]["decision"] == "deny"
    assert guard.audit.verify_chain().ok
