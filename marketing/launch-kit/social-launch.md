# Social launch copy

Tone: technical, honest, zero hype. Tracerail = open-source control plane for AI agent actions (drop-in MCP proxy: policies, human approval gates, tamper-evident hash-chained audit log).

---

## (a) X / Twitter thread — 6 tweets

**1/ (hook with a concrete fact)**
AI agents now issue refunds, send emails, write to prod DBs. But ask one question and most teams freeze: "prove what your agent did, who approved it, and that the log wasn't edited." Traces can't answer that. So we built the layer that can. 🧵

**2/ (problem)**
Agent frameworks log *traces* for debugging. Traces live in a vendor UI, they're mutable, and they don't stop anything in the moment. That's fine for fixing prompts. It's useless when an auditor — or your board — asks for evidence of an action.

**3/ (demo)**
Tracerail is a drop-in MCP proxy. One line in your client config:

`tracerail proxy --policies policies.yaml -- <your real mcp server>`

Every tools/call now passes through policy + approval + a tamper-evident audit log. Zero changes to agent code.

**4/ (differentiator)**
Two things make it real:
• Audit log is a hash chain — `tracerail verify` proves it wasn't altered.
• Approval is synchronous: a sensitive call is *held* until a human approves, or times out into a structured error the agent can adapt to.

**5/ (OSS)**
It's Apache-2.0. MCP stdio proxy, YAML policies, hash-chained log, approval CLI, Python SDK — all in the open. No signup to try it. Run it against the bundled toy server in 2 minutes.

**6/ (CTA)**
If you run agents that take real actions in prod, I want to know what's actually blocking your rollout — audit/approval, or something else. Repo + quickstart here, issues open: 👉 github.com/yourorg/tracerail

---

## (b) LinkedIn post (~150 words) — for VP Eng / CISO

Most AI agent pilots stall at the same wall: not model quality, but governance. The moment an agent touches money or sensitive data in production, someone — security, compliance, the board — asks: *what did it do, who authorized it, and can you prove the record wasn't altered?* Traces from your framework don't answer that.

The pressure is about to get concrete. The EU AI Act's logging obligations for high-risk systems take effect in August 2026, and "we have debug traces" won't satisfy an auditor.

We built Tracerail, an open-source control plane for agent actions: a drop-in MCP proxy that adds declarative policies, human approval gates on sensitive calls, and a tamper-evident, hash-chained audit trail you can verify — without rewriting your agents.

It's Apache-2.0 and runs on your infra today. If you're moving agents toward production, I'd value a candid conversation about what evidence you'll actually need. Link in comments.

---

## (c) Community post — Discord / r/mcp / r/LLMDevs

**Title:** Built a tamper-evident audit + approval proxy for MCP tool calls — feedback?

Hey all — I kept hitting the same problem putting agents into prod: once they take real actions (refunds, deploys, DB writes), I couldn't prove what happened or stop the risky stuff in the moment. Framework traces are great for debugging but they're mutable and don't gate anything.

So I built Tracerail. It's a drop-in MCP proxy — you wrap your existing server and every tools/call goes through:
- YAML policies (allow / deny / spend caps / rate caps, first match wins)
- human approval gates (the call is *held* at the protocol level until you approve/deny, with a timeout)
- a hash-chained JSONL audit log you can `verify` (editing/reordering breaks the chain)

No agent code changes. Apache-2.0. There's also a `@guard_tool` decorator for non-MCP Python tools.

It's v0.1 and honestly limited: stdio only, approvals are CLI (no dashboard yet), single-node, no replay. Not trying to oversell it.

Mostly posting because I want to know if the approach is even right. Is audit/approval the actual blocker for you, or am I solving a problem nobody has? Repo in comments — tear it apart.
