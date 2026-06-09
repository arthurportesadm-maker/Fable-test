# Design partner outreach

Target: Head of AI Platform / VP Eng at fintech & e-commerce companies running agents that touch money. Tone: technical, honest, zero hype, no fake personalization. CTA on email 1 = 20-minute call.

---

## Email 1 — problem + technical proof (EN, ≤120 words)

**Subject:** proving what your agents did in prod

Hi {{first_name}},

You're running agents that take real actions — refunds, payments, account changes. The question that tends to stall production isn't model quality, it's: can you prove what an agent did, who approved it, and that the log wasn't altered? Framework traces don't answer that — they're mutable and don't gate anything.

We built Tracerail (open source, Apache-2.0): a drop-in MCP proxy that adds policies, human approval gates, and a hash-chained audit log you can verify — no agent code changes.

I'm picking a few design partners shaping the roadmap. Worth 20 minutes to see if it fits how {{company}} runs agents?

— {{your_name}}

---

## Email 2 — follow-up, compliance angle (EN)

**Subject:** re: proving what your agents did in prod

Hi {{first_name}},

Quick follow-up with the angle I should have led with.

The EU AI Act's logging obligations for high-risk systems take effect in August 2026. For agents touching money, "we have debug traces" won't satisfy an auditor — the bar is an integral, tamper-evident record of actions and who authorized them. That's exactly what Tracerail's hash-chained audit log and approval gates are built to produce, and it's the kind of thing that's far cheaper to design in now than to retrofit under audit pressure.

Still happy to walk through it in 20 minutes — even if you just want a second opinion on what evidence you'll need.

— {{your_name}}

---

## Email 3 — breakup (EN)

**Subject:** closing the loop

Hi {{first_name}},

I'll stop here so I'm not cluttering your inbox. I'm guessing audit/approval for agent actions isn't a priority for {{company}} right now — totally fair.

If that changes, Tracerail is open source and the quickstart runs in about two minutes: {{repo_url}}. And if I misjudged the problem entirely, I'd genuinely value a one-line reply telling me what the real blocker is — that's more useful to me than a meeting.

Thanks for the read.

— {{your_name}}

---

## Email 1 — PT-BR version (≤120 words)

**Assunto:** provando o que seus agentes fizeram em produção

Olá {{first_name}},

Vocês rodam agentes que executam ações reais — reembolsos, pagamentos, ajustes em conta. O que costuma travar o caminho até produção não é a qualidade do modelo, e sim: dá para provar o que o agente fez, quem autorizou, e que o registro não foi alterado? Os traces do framework não respondem isso — são mutáveis e não barram nada.

Construímos o Tracerail (open source, Apache-2.0): um proxy MCP drop-in que adiciona políticas, aprovação humana e uma trilha de auditoria hash-chained verificável — sem mexer no código do agente.

Estou selecionando alguns design partners para moldar o roadmap. Vale 20 minutos para ver se faz sentido para a {{company}}?

— {{your_name}}

---

## Design partnership offer

**What we give:**
- **Roadmap influence** — your use cases are prioritized; you have direct input on what we build next (dashboard, export packs, transports).
- **Direct support** — a private channel to the founder/eng team, not a ticket queue. Bugs and integration help handled directly.
- **Locked pricing** — when the paid tier (compliance dashboard, retention, SOC2 / EU AI Act export) ships, your price is locked at a permanent design-partner rate.

**What we ask:**
- **Weekly feedback** — ~30 minutes a week of candid input on what works, what's missing, what's broken.
- **Logo** — permission to list you as a design partner once you're comfortable.
- **Case study** — a written case study or reference call once you're getting real value (only with your sign-off, never before).
