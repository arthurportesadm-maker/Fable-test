# Tracerail

**Control plane open-source para ações de agentes de IA.**
Auditoria à prova de adulteração, políticas declarativas e aprovação humana — sem mudar o código do seu agente.

---

## Problema

Empresas estão colocando agentes de IA em produção para executar ações reais: emitir reembolsos, enviar e-mails, mexer em infraestrutura, gastar dinheiro via APIs. Mas o "encanamento" de governança não existe. Hoje, quem é responsável por uma ação de agente não consegue responder três perguntas básicas:

- **O que o agente fez?** Não há trilha de auditoria confiável e à prova de adulteração.
- **O que o agente *pode* fazer?** Permissões, limites de gasto e rate limits ficam espalhados em prompts e código.
- **Quem autorizou?** Ações sensíveis disparam sem nenhum ponto de aprovação humana.

O resultado é que times travam o rollout por medo de compliance, ou avançam sem controle e assumem risco operacional e regulatório.

## Solução

Tracerail é um control plane que senta no caminho das ações do agente e impõe governança em tempo de execução. Ele intercepta cada chamada de ferramenta, avalia contra políticas declarativas, pausa o que exige aprovação humana e registra tudo em uma trilha imutável — tudo isso sem exigir mudança no código do agente, porque opera como um proxy drop-in no protocolo MCP. Cinco componentes:

- **Trilha de auditoria imutável** — registro com *hash-chaining* (tamper-evident); cada evento encadeia o hash do anterior. Exportável para evidência de SOC2 e EU AI Act.
- **Policy engine declarativo (YAML)** — regras `allow`/`deny`, *spend caps* por sessão, *rate limits* e redação de campos sensíveis, versionadas como código.
- **Approval gates** — ações sensíveis (reembolsos, e-mails, deploy) ficam pendentes até aprovação humana via CLI ou painel.
- **Proxy MCP drop-in** — senta entre qualquer cliente MCP (Claude, Cursor etc.) e qualquer servidor MCP, interceptando `tools/call` sem tocar no agente.
- **SDK Python (decorator)** — para governar ferramentas que vivem fora do MCP, com uma anotação.

## Por que agora

- **Demanda do mercado de risco.** A YC RFS (Fall 2025 / Summer 2026) pede explicitamente "governança operacional de agentes: permissões, *spend caps*, *audit logs*".
- **O gargalo virou supervisão humana.** a16z Big Ideas 2026 aponta que o limitante não é mais a capacidade do modelo, e sim humanos conseguirem supervisionar e aprovar dezenas de agentes rodando em paralelo — exatamente o que os *approval gates* resolvem.
- **Regulação obriga logging.** O EU AI Act exige registro e *logging* de sistemas de alto risco. Auditoria deixa de ser opcional.
- **Adoção enterprise ainda é cedo.** Menlo Ventures (2025): apenas 16% dos *deployments* enterprise são agentes de fato, e o "plumbing" representa só ~US$ 1,5 bi de um mercado de ~US$ 37 bi. Há *headroom* enorme para a camada de infraestrutura amadurecer.

## Mercado e concorrência

A categoria de **auditoria e compliance de agentes é fragmentada e não tem líder open-source**. Os concorrentes parciais ficam em outras camadas:

- **Tracing/observabilidade** — Galileo, LangSmith/Langfuse cobrem *tracing*, mas não são *compliance-grade*: sem trilha à prova de adulteração, sem políticas em runtime, sem aprovação humana.
- **AppSec incumbents** — Snyk/Invariant, SentinelOne/Prompt Security focam em segurança e detecção de ameaças, não em auditoria, política operacional e aprovação.

Tracerail ocupa o espaço entre observabilidade e segurança: **o control plane de governança e compliance**. Ser OSS e *drop-in* via MCP é o que cria a vantagem de distribuição que falta aos incumbentes.

## Modelo de negócio (open-core)

- **Núcleo OSS** — proxy MCP, policy engine, trilha de auditoria com *hash-chaining*, *approval gates* via CLI e SDK Python. Gratuito, adotado *bottom-up*.
- **Pago (enterprise)** — painel de compliance, retenção gerenciada da trilha, SSO/RBAC, *export* pronto para SOC2 e EU AI Act, e *replay* determinístico avançado.

A monetização segue o gancho de risco: quem precisa apresentar evidência a auditor ou regulador paga pela camada gerenciada e pelos controles de acesso.

## Go-to-market

**Bottom-up, dev-first, via MCP.** O desenvolvedor instala o proxy entre seu cliente e servidor MCP em minutos, sem reescrever o agente, e ganha auditoria e políticas de imediato. A adoção individual vira *pull* organizacional quando compliance, segurança e liderança precisam de evidência e aprovação — momento em que o plano enterprise entra.

## Roadmap

- **MVP (hoje)** — proxy MCP + policy engine + trilha de auditoria + *approval gates* via CLI.
- **v0.2** — dashboard web e *replay* de sessões.
- **v0.3** — cloud multi-tenant gerenciada.

## Métricas de sucesso iniciais

- **Adoção OSS** — *stars* no GitHub, instalações do proxy, servidores MCP sob governança.
- **Engajamento** — ações interceptadas e políticas ativas por *deployment*; *approval gates* acionados e resolvidos.
- **Sinal de monetização** — organizações com mais de um usuário ativo e conversão para o plano de compliance/enterprise.
