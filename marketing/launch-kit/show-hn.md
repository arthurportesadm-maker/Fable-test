# Show HN post

**Title:** Show HN: Tracerail – tamper-evident audit and approvals for AI agents (MCP proxy)

**URL:** https://github.com/yourorg/tracerail

---

## Body (~350 words)

I build agent systems for a living, and the thing that kept stalling our rollouts wasn't model quality — it was that nobody could answer a simple question when an agent did something with real money: *prove what it did, who allowed it, and that the record wasn't edited afterward.* Our framework gave us nice traces for debugging, but traces aren't evidence. They live in a vendor's UI, they can be deleted, and they don't stop anything in the moment. So I built Tracerail to be the boring layer I wanted: a control plane that sits in front of tool calls.

Concretely, it's a drop-in MCP proxy. You change one line in your MCP client config — point it at `tracerail proxy -- <your real server>` — and every `tools/call` now passes through a policy engine (allow / deny / spend caps / rate caps as versioned YAML), optional human approval gates, and a tamper-evident audit log. No changes to agent code. There's also a Python decorator (`@guard_tool`) for non-MCP tools.

Two implementation details I found interesting:

- **The audit log is a hash chain in JSONL** — each record embeds the SHA-256 of the previous one, so editing, deleting, or reordering history breaks `tracerail verify`. It's safe for concurrent writers (proxy + CLI + multiple agents) via cross-process file locking, and `redact`-listed fields never touch disk.
- **Approval is synchronous at the protocol level.** When a call needs a human, the proxy simply *holds* the MCP request — it doesn't resolve until someone runs `tracerail approve <id>` (or it times out and the agent gets a structured tool error it can adapt to). No polling, no callback infra.

What it does **not** do yet: no web dashboard (approvals are CLI-only right now), stdio transport only (no HTTP/SSE), no deterministic replay, no managed/multi-tenant mode. Single-node. It's v0.1.

My question for HN: for those running agents that take real actions in prod — what's actually blocking you from going from pilot to production? Is it audit/approval, or is the real pain somewhere else entirely? I'd rather hear "you're solving the wrong problem" now than later.

Apache-2.0.

---

## Prepared replies to likely objections

### "Why not just use LangSmith / Langfuse traces for this?"

Because tracing and evidence are different jobs. LangSmith is excellent for debugging prompt/quality issues — but the trace lives in a vendor UI, it's mutable, and it doesn't *stop* an action mid-flight. Tracerail isn't trying to replace it; you'd run both. The difference is: can you hand a record to an auditor and prove it wasn't altered (`tracerail verify` over a hash chain), and can you require a human before a refund over $100 actually executes? That's runtime control + integrity, not post-hoc observability. If all you need is debugging, you don't need this.

### "Doesn't a proxy in front of every tool call add latency?"

For the common path, effectively no — a policy match is a glob comparison and an append to a local JSONL file (one fsync, one file lock). It's sub-millisecond relative to the network round-trip and the model latency that dominate any agent call. The only call that gets slower is one you *deliberately* sent to a human for approval, and that's the point — you opted into a human in the loop for that specific action. Everything else passes through untouched.

### "Synchronous approval just blocks the agent — doesn't that hang the loop?"

It blocks *that one tool call*, on purpose — the same way any external system that needs human confirmation would. Two things make it tolerable: (1) approvals are scoped narrowly by policy (e.g. only refunds above a cap), so the vast majority of calls never wait; (2) every gate has a `timeout_seconds` and an `on_timeout` effect (`deny` by default), so the call can't hang forever. On timeout or denial the agent receives a structured tool error explaining which policy blocked it, so a well-built loop adapts instead of crashing. If you want fully async/non-blocking approvals, that's a fair feature request — today it's intentionally simple and synchronous.
