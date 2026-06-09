"""A minimal MCP-style stdio server used to demo the Tracerail proxy.

It speaks newline-delimited JSON-RPC and exposes three fake tools
(issue_refund, send_email, db_query) that just echo what they would do.
Not a full MCP implementation — just enough for an end-to-end demo:

    tracerail proxy --policies examples/policies.yaml -- python examples/toy_mcp_server.py
"""

import json
import sys

TOOLS = [
    {"name": "issue_refund", "description": "Refund an order", "inputSchema": {"type": "object"}},
    {"name": "send_email", "description": "Send an email", "inputSchema": {"type": "object"}},
    {"name": "db_query", "description": "Run a database query", "inputSchema": {"type": "object"}},
]


def reply(request_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": request_id, "result": result}) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        message = json.loads(line)
        method = message.get("method")
        request_id = message.get("id")
        if method == "initialize":
            reply(request_id, {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "toy-server", "version": "0.1.0"},
            })
        elif method == "tools/list":
            reply(request_id, {"tools": TOOLS})
        elif method == "tools/call":
            params = message.get("params") or {}
            text = f"executed {params.get('name')} with {json.dumps(params.get('arguments') or {})}"
            reply(request_id, {"content": [{"type": "text", "text": text}], "isError": False})
        elif request_id is not None:
            reply(request_id, {})


if __name__ == "__main__":
    main()
