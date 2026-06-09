# Tracerail

**Open-source control plane for AI agent actions.** A drop-in MCP proxy that gives every
tool call your agents make a tamper-evident audit trail, declarative policies, and human
approval gates — without changing a line of agent code.

```
MCP client (Claude, Cursor, ...) ──► tracerail proxy ──► any MCP server
                                          │
                                          ├─ policy engine   (allow / deny / spend caps / rate caps)
                                          ├─ approval gates  (sensitive actions wait for a human)
                                          └─ audit trail     (hash-chained, tamper-evident JSONL)
```

Agents are taking real actions now — refunds, emails, deploys, database writes. Frameworks
log *traces* for debugging, but nobody can answer the compliance question: *"prove what your
agent did, who allowed it, and that the record wasn't altered."* Tracerail is that layer.
See [docs/PITCH.md](docs/PITCH.md) for the business case (PT-BR).

## Quickstart

```bash
pip install -e .
```

Wrap any MCP server with the proxy. In your MCP client config, replace the server command:

```json
{
  "mcpServers": {
    "payments": {
      "command": "tracerail",
      "args": ["proxy", "--policies", "policies.yaml", "--",
               "npx", "-y", "@yourorg/payments-mcp-server"]
    }
  }
}
```

Everything passes through untouched **except** `tools/call`, which is gated. Try it end to
end with the bundled toy server:

```bash
tracerail proxy --policies examples/policies.yaml -- python examples/toy_mcp_server.py
```

## Policies

First match wins, top to bottom ([examples/policies.yaml](examples/policies.yaml)):

```yaml
default: allow
redact: [password, api_key]        # hidden from the audit trail and approvers

policies:
  - name: block-prod-db
    match: { tool: "db_*", args: { env: "prod*" } }   # glob on tool and args
    effect: deny
    reason: "Direct production database access is forbidden for agents."

  - name: refund-cap                # ≤ $100 auto-allowed, above goes to a human
    match: { tool: issue_refund }
    effect: allow
    constraints:
      max_amount: { field: amount, limit: 100 }
    on_violation: require_approval
    timeout_seconds: 3600
    on_timeout: deny

  - name: search-rate-cap           # at most 20 calls per session
    match: { tool: web_search }
    effect: allow
    constraints: { max_calls: 20 }
    on_violation: deny
```

Effects: `allow`, `deny`, `require_approval`. Constraints (`max_calls`, `max_amount`) trigger
`on_violation` when exceeded. `match.args` keys support dot paths (`payment.amount`).

## Approval gates

When a call requires approval, the agent's request is **held** (the MCP request simply doesn't
resolve yet) while a human decides:

```bash
$ tracerail approvals
588d3411cbbe  [pending ]  2026-06-09 18:32:58  issue_refund  policy=refund-cap
              args: {"amount": 9999}
              reason: amount 9999.0 exceeds limit 100

$ tracerail approve 588d3411cbbe --by alice     # or: tracerail deny ...
```

On approval the call proceeds; on denial or timeout the agent receives a structured tool
error explaining which policy blocked it, so the loop can adapt instead of crashing.

## Audit trail

Every decision — allowed, denied, escalated, resolved — is appended to a JSONL log where each
record embeds the SHA-256 hash of the previous one. Editing, deleting or reordering history
breaks the chain:

```bash
$ tracerail log -v --tail 20
$ tracerail verify
OK: audit chain intact (5 records)
```

The log is safe for concurrent writers (proxy + CLI + multiple agents) via file locking, and
fields listed under `redact` never reach disk.

## Python SDK (non-MCP tools)

```python
from tracerail import Guard, guard_tool, ToolDenied

guard = Guard.from_files("policies.yaml")

@guard_tool(guard)
def issue_refund(order_id: str, amount: float) -> str:
    ...

issue_refund("order-1", 42.0)     # allowed, audited
issue_refund("order-2", 2500.0)  # blocks until approved, or raises ToolDenied
```

See [examples/demo_agent.py](examples/demo_agent.py).

## Development

```bash
pip install -e ".[dev]"
python -m pytest
```

## Status & roadmap

v0.1 (this MVP): MCP stdio proxy, YAML policies, hash-chained audit log, approval CLI,
Python SDK. Next: web approval dashboard, deterministic replay of agent decisions,
SOC2/EU AI Act export packs, HTTP/SSE transports, managed multi-tenant cloud.

Apache-2.0.
