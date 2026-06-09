# Tracerail — Roteiros de Vídeos Promocionais

Roteiros de produção para 3 vídeos do Tracerail. Texto on-screen e narração (VO) em **EN** (mercado global); instruções e contexto em **PT**.

Convenções:
- **Tempo**: marcação relativa do início do vídeo (mm:ss).
- **Visual**: o que aparece na tela.
- **Texto na tela**: legendas e lower-thirds (sempre em EN; obrigatório quando o áudio é opcional).
- **VO**: narração em EN. Em vídeos sem áudio obrigatório, vira legenda.
- **Áudio**: música, SFX, silêncio.

Marca a respeitar em todos: fundo `#0B1220`, texto `#E6EDF7`, verde `#2EE6A6` só para aprovação/verificação, âmbar `#F5B83D` para pendente, vermelho `#E5484D` discreto para deny. Tom calmo, evidência sobre hype. Wordmark `tracerail` em minúsculas, JetBrains Mono. Nunca exclamação de alarme.

---

## Vídeo 1 — Teaser 30s

**Plataformas:** X / LinkedIn (feed, autoplay mudo — legendas obrigatórias).

**Objetivo:** parar o scroll e fixar a categoria ("control plane para ações de agentes") + gerar clique no GitHub.
**Métrica de sucesso:** ≥ 25% de view-through a 3s; CTR para o repo ≥ 1,5%; ≥ 30 stars atribuíveis ao post na primeira semana.

### Roteiro cena a cena

| Tempo | Visual | Texto na tela (EN) | VO / legenda (EN) | Áudio |
|---|---|---|---|---|
| 00:00–00:03 | Fundo `#0B1220`. Cursor digita numa linha de terminal mono. | **Your AI agents take real actions.** | "Your AI agents take real actions." | Beat eletrônico minimalista entra, baixo |
| 00:03–00:07 | Lista rápida de ações deslizando: `issue_refund`, `send_email`, `deploy`, `db_write`. Ícones neutros. | Refunds. Emails. Deploys. DB writes. | "Refunds. Emails. Deploys. Database writes." | Pulso rítmico sobe levemente |
| 00:07–00:12 | Corte para pergunta no centro, texto `#E6EDF7`. | **Can you prove what they did?** | "Can you prove what they did?" | Música segura 1 beat, leve pausa |
| 00:12–00:16 | **Beat 1 — Deny.** Terminal: `tools/call db_write {env: prod}` → resposta `DENY` em vermelho discreto `#E5484D`, com `policy=block-prod-db`. | DENY · policy=block-prod-db | "Block what shouldn't happen." | Tick seco de SFX no DENY |
| 00:16–00:21 | **Beat 2 — Approval.** Terminal: `issue_refund {amount: 9999}` → estado `PENDING` âmbar `#F5B83D`; linha `tracerail approve … --by alice`. | PENDING → approved by alice | "Hold high-risk actions for a human." | SFX suave de confirmação |
| 00:21–00:25 | **Beat 3 — Verify.** Terminal: `tracerail verify` → `OK: audit chain intact` em verde `#2EE6A6`. Blocos de hash encadeados aparecem ao lado. | tracerail verify → OK: chain intact | "Verify the record wasn't altered." | Nota verde de resolução |
| 00:25–00:28 | Logo `tracerail` (ícone-trilho de 3 blocos, último verde com check) centralizado. | **Every agent action, accounted for.** | "Every agent action, accounted for." | Música assenta na tagline |
| 00:28–00:30 | CTA. Fundo escuro, mono. | **github.com/…/tracerail** · Open-source · Apache-2.0 | "Open source on GitHub." | Outro curto, fade |

**Thumbnail sugerida (para versão LinkedIn/preview):** terminal escuro `#0B1220` com três linhas empilhadas — `DENY` (vermelho discreto), `PENDING` (âmbar), `OK: chain intact` (verde) — e o wordmark `tracerail` no rodapé. Sem rostos, sem setas berrantes.

### SEO / publicação

- **Título (X/LinkedIn):** Your AI agents take real actions. Can you prove what they did?
- **Descrição/legenda do post:**
  > Tracerail is the open-source control plane for AI agent actions. An MCP proxy that enforces policies, adds human approval gates, and records a hash-chained, tamper-evident audit trail — no agent code changes.
  >
  > Deny what shouldn't run. Hold high-risk actions for a human. Verify the record. ⛓️
  >
  > Apache-2.0 on GitHub 👇
  > #AIagentgovernance #MCP #MCPproxy #AIauditTrail #EUAIAct #AIsecurity #LLMOps
- **Keywords-alvo:** AI agent governance, MCP proxy, AI audit trail, EU AI Act.

---

## Vídeo 2 — Launch 90s

**Plataformas:** YouTube + site (hero / above the fold).

**Objetivo:** apresentar a categoria e converter engenheiro/líder técnico cético em visitante do repo, via estrutura problema → agitação → solução com prova na tela.
**Métrica de sucesso:** retenção média ≥ 50%; ≥ 40% assistem além de 00:60 (a demo); CTR do card/descrição para GitHub ≥ 4%.

### Roteiro cena a cena

| Tempo | Visual | Texto na tela (EN) | VO (EN) | Áudio |
|---|---|---|---|---|
| 00:00–00:08 | **Problema.** Montagem rápida de agentes agindo: um chat dispara `issue_refund`, outro `deploy`. Tom calmo, sem caos. | Agents don't just answer anymore. They act. | "AI agents don't just answer questions anymore. They take actions — refunds, emails, deploys, database writes." | Pad ambiente sóbrio |
| 00:08–00:20 | **Agitação.** Split: à esquerda, um "trace" de debug rolando; à direita, um auditor com uma pergunta. | Traces are for debugging. Not for proof. | "Frameworks log traces for debugging. But nobody can answer the compliance question: prove what your agent did, who allowed it, and that the record wasn't altered." | Tensão sutil, sem alarme |
| 00:20–00:30 | **Estatística citável.** Card limpo, número grande em `#E6EDF7`, fonte creditada embaixo. | **Only 16%** of enterprise AI deployments are real agents. Governance is the blocker. — Menlo Ventures | "According to Menlo Ventures, only sixteen percent of enterprise AI deployments are actually agents. The blocker isn't capability. It's governance." | Beat marca o número |
| 00:30–00:38 | **Solução / categoria.** Diagrama do README anima: `MCP client → tracerail proxy → MCP server`, com os 3 ramos (policy, approval, audit). | tracerail: the control plane for agent actions | "Tracerail sits in front of your agents as an MCP proxy. Every tool call passes through — untouched, except the ones that matter." | Música vira para resolução |
| 00:38–00:50 | **Demo real 1 — policy + deny.** Tela real: `policies.yaml` com `block-prod-db`; agente tenta `db_write env=prod` → `DENY` vermelho discreto, com `reason`. | Declarative policies. First match wins. | "You write policies in YAML. First match wins. A production database write from an agent? Denied — with a reason the agent can adapt to." | SFX deny seco |
| 00:50–01:02 | **Demo real 2 — approval gate.** `issue_refund {amount: 9999}` fica `PENDING` âmbar; `tracerail approvals` lista; `tracerail approve … --by alice`; call prossegue. | High-risk actions wait for a human. | "High-risk actions don't just run. They wait. A human approves — by name — and only then the call proceeds." | Confirmação suave |
| 01:02–01:14 | **Demo real 3 — audit + verify.** `tracerail log -v --tail`; blocos JSONL com hash do anterior; `tracerail verify → OK: audit chain intact`. Verde `#2EE6A6`. | Hash-chained. Tamper-evident. Verifiable. | "Every decision is appended to a hash-chained log. Each record carries the hash of the last. Edit one line, and verify catches it." | Nota verde de prova |
| 01:14–01:24 | **Fechamento de categoria.** Logo `tracerail`. Boilerplate curto. | **the open-source AI agent control plane** | "Tracerail. The open-source AI agent control plane. Not trust — evidence." | Música assenta |
| 01:24–01:30 | CTA. | github.com/…/tracerail · `pip install -e .` · Apache-2.0 | "Open source. Start in one command." | Outro, fade |

**Thumbnail sugerida:** fundo `#0B1220`. À esquerda, texto grande em Inter: "Prove what your agents did." À direita, o terminal com `tracerail verify → OK` em verde. Selo discreto "Open Source · MCP". Alto contraste, zero clickbait.

### SEO / publicação (YouTube)

- **Título:** Tracerail: The Open-Source Control Plane for AI Agent Actions (MCP Proxy + Audit Trail)
- **Descrição:**
  > AI agents now take real actions — refunds, deploys, database writes. Tracerail is the open-source AI agent governance layer: a drop-in MCP proxy that enforces declarative policies, adds human approval gates, and records a hash-chained, tamper-evident AI audit trail. No agent code changes.
  >
  > Menlo Ventures reports only 16% of enterprise AI deployments are real agents — governance is the blocker. Tracerail is built for that gap, with EU AI Act-ready evidence in mind.
  >
  > In this video:
  > 00:20 Why governance blocks agent deployments
  > 00:38 How the MCP proxy works
  > 00:38 Deny a policy-violating action
  > 00:50 Human approval gates
  > 01:02 Hash-chained audit trail + tracerail verify
  >
  > ⭐ GitHub (Apache-2.0): github.com/…/tracerail
  > 📄 Docs: …
  >
  > #AIagentgovernance #MCPproxy #AIauditTrail #EUAIAct #LLMOps #AIsecurity #opensource
- **Tags:** AI agent governance, MCP proxy, AI audit trail, EU AI Act, AI agents, agent control plane, LLM security, MCP server, tamper-evident log.

---

## Vídeo 3 — Demo Técnico 3min

**Plataformas:** YouTube + docs (embed na página de quickstart).

**Objetivo:** mostrar, com comandos reais, que dá para instalar e governar um agente em minutos — converter o engenheiro avaliador em quem roda `pip install` e abre o `policies.yaml`.
**Métrica de sucesso:** retenção ≥ 45% até o `tracerail verify` (≈ 02:30); ≥ 8% de cliques em "instalar/docs"; comentários técnicos > superficiais.

> Gravar tudo em terminal real (asciinema/VHS) para legitimidade. Nada de mock. Usar o servidor de exemplo do repo.

### Roteiro cena a cena

| Tempo | Visual | Texto na tela (EN) | VO (EN) | Áudio |
|---|---|---|---|---|
| 00:00–00:12 | Intro curta. Logo `tracerail` + uma linha do que será feito. | Install → write policies → deny → approve → verify | "In three minutes: install Tracerail, write a policy, watch it deny a bad call, approve a refund from the CLI, and verify the audit chain. Real terminal, no edits." | Pad calmo, baixo |
| 00:12–00:28 | **1. Install.** Terminal real:<br>`pip install -e .` | `$ pip install -e .` | "First, install. Tracerail is a Python package — clone the repo and install it editable." | Teclado sutil |
| 00:28–00:52 | **2. Policies.** Abrir `policies.yaml` no editor; destacar `default: allow`, `redact`, e as 3 regras (`block-prod-db`, `refund-cap`, `search-rate-cap`). | policies.yaml — first match wins | "Policies are declarative YAML. Default allow. Redact secrets so they never hit disk. Then rules, top to bottom, first match wins: block production DB access, cap refunds at 100 dollars with approval above that, and rate-limit search to 20 calls." | Música leve sob a explicação |
| 00:52–01:10 | **3. Run the proxy.** Terminal:<br>`tracerail proxy --policies examples/policies.yaml -- python examples/toy_mcp_server.py` | Wrap any MCP server. Agent code unchanged. | "Run the proxy in front of any MCP server. Here, the bundled toy server. Everything passes through untouched — except tools/call, which is gated." | SFX start curto |
| 01:10–01:32 | **4. See a DENY.** Agente (ou cliente) chama `db_write {env: prod}`. Resposta `DENY` vermelho discreto `#E5484D` + `reason: Direct production database access is forbidden`. | DENY · policy=block-prod-db | "A production database write. Denied — by policy block-prod-db, with a structured reason. The agent gets the error and can adapt instead of crashing." | Tick deny |
| 01:32–02:00 | **5. Trigger approval.** Agente chama `issue_refund {amount: 9999}`. Fica `PENDING` âmbar. Em outra aba:<br>`tracerail approvals`<br>mostra `588d3411cbbe [pending] issue_refund policy=refund-cap` + `reason: amount 9999.0 exceeds limit 100`. | PENDING — waiting for a human | "A 9,999-dollar refund exceeds the 100-dollar cap, so it escalates. The agent's call is held — the MCP request simply doesn't resolve yet. List pending approvals with tracerail approvals." | Âmbar musical sutil |
| 02:00–02:18 | **6. Approve from CLI.** Terminal:<br>`tracerail approve 588d3411cbbe --by alice`<br>→ call prossegue; agente recebe sucesso. | $ tracerail approve <id> --by alice | "Approve by name from the CLI. The held call proceeds — and who approved it is now part of the record." | Confirmação suave |
| 02:18–02:40 | **7. Verify.** Terminal:<br>`tracerail log -v --tail 20`<br>`tracerail verify`<br>→ `OK: audit chain intact (5 records)` verde `#2EE6A6`. | tracerail verify → OK: audit chain intact | "Every decision was appended to the log. Verify the whole chain in one command. OK — audit chain intact." | Nota verde de prova |
| 02:40–02:56 | **8. Show the JSONL.** Abrir o arquivo de log: cada registro JSONL com campo de hash do anterior; apontar que editar uma linha quebra o `verify`. Mostrar que `password`/`api_key` não aparecem (redacted). | Each record embeds the hash of the previous one. | "Here's the raw log. Each record embeds the SHA-256 hash of the one before it. Change a line, reorder, delete — verify breaks. And redacted fields never reached disk." | Música segura |
| 02:56–03:00 | Outro. Logo + CTA. | github.com/…/tracerail · Apache-2.0 · docs link | "That's Tracerail. Star it on GitHub and read the docs to wrap your own MCP server." | Outro, fade |

### Comandos exatos usados (do README)

```bash
pip install -e .
tracerail proxy --policies examples/policies.yaml -- python examples/toy_mcp_server.py
tracerail approvals
tracerail approve 588d3411cbbe --by alice
tracerail log -v --tail 20
tracerail verify
```

(Para a versão SDK / não-MCP, opcional como B-roll: `Guard.from_files("policies.yaml")` + `@guard_tool(guard)` de `examples/demo_agent.py`.)

**Thumbnail sugerida:** terminal real em destaque mostrando a sequência `DENY` → `approve --by alice` → `OK: audit chain intact`, com um título mono no topo: "Govern an AI agent in 3 min". Verde só na linha do verify.

### SEO / publicação (YouTube)

- **Título:** Tracerail Demo: Govern AI Agent Actions with an MCP Proxy (Policies, Approvals, Audit Trail)
- **Descrição:**
  > A real, no-edits walkthrough of Tracerail — the open-source AI agent governance control plane. Install it, write a policies.yaml, run the MCP proxy in front of an MCP server, watch a policy deny a production DB write, approve a refund from the CLI, and verify the hash-chained, tamper-evident AI audit trail.
  >
  > Built for platform, security, and compliance teams preparing for the EU AI Act.
  >
  > Chapters:
  > 00:12 Install (pip install -e .)
  > 00:28 Write policies.yaml
  > 00:52 Run the MCP proxy
  > 01:10 See a DENY
  > 01:32 Trigger an approval gate
  > 02:00 Approve a refund from the CLI
  > 02:18 tracerail verify
  > 02:40 Inspect the hash-chained JSONL log
  >
  > ⭐ GitHub (Apache-2.0): github.com/…/tracerail
  >
  > #AIagentgovernance #MCPproxy #AIauditTrail #EUAIAct #MCP #LLMOps #opensource
- **Tags:** AI agent governance, MCP proxy, AI audit trail, EU AI Act, MCP server tutorial, agent approval gates, hash-chained log, tamper-evident, LLM security demo.
