# Product Hunt launch

Tone: technical, honest, zero hype.

---

## Tagline (≤60 chars)

`Tamper-evident audit & approvals for AI agents` (47 chars)

Alt: `Audit, policy & human gates for AI agent actions` (48 chars)

---

## Description (≤260 chars)

Open-source control plane for AI agent actions. A drop-in MCP proxy that adds declarative policies, human approval gates, and a hash-chained, tamper-evident audit log to every tool call — no agent code changes. Apache-2.0. (236 chars)

---

## First comment from the maker (~200 words)

Hi PH — maker here. I build agent systems, and the wall I kept hitting wasn't model quality, it was governance. The moment an agent does something real — issue a refund, send a customer email, write to a prod DB — someone asks: what did it do, who allowed it, and can you prove the log wasn't edited? Framework traces are great for debugging but they're mutable, vendor-locked, and don't stop anything in the moment.

Tracerail is the boring layer I wanted. It's a drop-in MCP proxy: change one line in your client config and every tool call passes through a policy engine (allow/deny/spend caps as YAML), optional human approval gates, and a tamper-evident audit log. The log is a hash chain — `tracerail verify` proves it wasn't altered. Approvals are held synchronously until a human decides, with a timeout. No agent code changes.

Being honest about v0.1: stdio transport only, approvals are CLI (no dashboard yet), single-node, no replay. It's Apache-2.0 and runs on your infra today.

I'd genuinely rather hear "you're solving the wrong problem" than polite praise. If you run agents in prod, what's actually blocking your rollout? Repo and 2-minute quickstart in the links.

---

## Replies to 3 likely questions

### "How is this different from LangSmith / Langfuse / observability tools?"

Different job. Those are for debugging trace quality — the data lives in a vendor UI, it's mutable, and it doesn't gate actions. Tracerail is runtime control + provable integrity: it can *stop* a refund over a cap until a human approves, and its hash-chained log lets you hand an auditor a record you can prove wasn't altered. You'd run both — observability for debugging, Tracerail for control and evidence.

### "Does the proxy add latency to every call?"

For the normal path, negligible — a policy decision is a glob match plus an append to a local JSONL file, sub-millisecond next to network and model latency. The only call that gets slower is one you deliberately routed to a human for approval, which is the whole point. Everything else passes through untouched.

### "What's the business model — is it staying open source?"

The core is and stays Apache-2.0: proxy, policies, hash-chained log, approval CLI, SDK. The plan is open-core — paid additions later for teams that need a compliance dashboard, retention, and SOC2 / EU AI Act export packs. Nothing in the open core gets paywalled retroactively. You can run the whole thing self-hosted forever.
