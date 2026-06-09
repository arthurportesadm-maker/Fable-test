# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Tracerail: an open-source control plane for AI agent actions — a drop-in MCP stdio proxy plus Python SDK that enforces declarative policies, holds sensitive tool calls for human approval, and writes a tamper-evident (hash-chained) audit trail. The repo also contains the startup's strategy/marketing assets, not just code.

## Commands

```bash
pip install -e ".[dev]"        # install package + pytest
python -m pytest -q            # run the full test suite
python -m pytest tests/test_guard.py -k approval   # run a single test / pattern
python examples/demo_agent.py  # SDK demo (writes demo-audit.jsonl / demo-state.db)
tracerail proxy --policies examples/policies.yaml -- python examples/toy_mcp_server.py  # e2e proxy
tracerail approvals / approve <id> / log -v / verify   # operator CLI (share --state/--audit paths)
python marketing/videos/render_teaser.py   # regenerate the teaser video (needs pillow, imageio, imageio-ffmpeg)
```

No linter is configured. Tests use real files via pytest `tmp_path` fixtures (see `tests/conftest.py` for the canonical policy fixture and `Guard` wiring).

## Architecture

Everything funnels through one enforcement point: `Guard.evaluate(tool, arguments)` in `src/tracerail/guard.py` returns a `Decision` and **always** writes an audit record, including for denied and escalated calls. The two integration surfaces — `wrap.guard_tool` (Python decorator) and `mcp_proxy.ProxyCore` (intercepts only `tools/call` JSON-RPC messages; everything else passes through) — are thin adapters over `Guard`.

Supporting pieces and their contracts:

- `policy.py` — YAML policies, first-match-wins, glob matching on tool name and argument dot-paths. Effects: `allow` / `deny` / `require_approval`; constraints (`max_calls`, `max_amount`) trigger `on_violation` instead of the base effect.
- `audit.py` — append-only JSONL where each record embeds the previous record's SHA-256. The previous hash is re-read under `fcntl.flock` on every append so multiple processes (proxy + CLI + agents) can share one log without breaking the chain. **The log format is a compliance contract**: changes must keep `verify_chain` working on logs written by older versions, or constitute a major version bump.
- `state.py` — SQLite shared between the agent process and the operator CLI: per-session counters and the approval queue. `Guard._escalate` blocks (polling) on `wait_for_resolution`; in the proxy this runs inside `asyncio.to_thread` per request, so a pending approval never stalls unrelated traffic.
- Redaction (`redact:` list in the policy file) is applied before anything is persisted or shown to approvers — the tool still receives real values.

Version lives in **two places** that must stay in sync: `pyproject.toml` and `src/tracerail/__init__.py`.

## Non-code assets

- `docs/` — PITCH.md (business one-pager), GTM.md (hypotheses H1–H5, 90-day plan, kill criteria), BRAND.md (voice, palette, taglines), OPERATING-MANUAL.md (founder's operating guide). Marketing copy must stay consistent with actual product capabilities in README.md.
- `site/` — static landing page (single-file `index.html`, no external deps) with JSON-LD that mirrors the visible FAQ exactly; `llms.txt`, `robots.txt`, `sitemap.xml`.
- `marketing/` — launch kit (Show HN, social, Product Hunt, outreach, Mom Test interview script) and video scripts.
- `.claude/agents/` — five management agents (growth-marketer, customer-research, release-manager, compliance-analyst, startup-coo); they treat docs/GTM.md and docs/BRAND.md as sources of truth.

Brand language rule used across all assets: "tamper-evident", never "tamper-proof"; no AI hype; category term is "AI agent control plane".
