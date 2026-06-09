# Tracerail — Manual de Operação do Fundador

Guia único para **entender, gerenciar e escalar** a startup. Tudo o que existe, onde está, e o ritual para operar sozinho com alavancagem de agentes.

## 1. Entenda o negócio em 60 segundos

- **Tese**: agentes de IA estão executando ações reais (refunds, e-mails, deploys), mas ninguém consegue *provar* o que eles fizeram nem aprovar o que importa. Observabilidade (LangSmith/Langfuse) serve para debug; AppSec serve para ataques. O espaço de **auditoria + aprovação compliance-grade** está fragmentado e sem líder open-source.
- **Produto**: proxy MCP drop-in + políticas YAML + approval gates humanos + trilha de auditoria hash-chained (tamper-evident). Funciona com qualquer cliente/servidor MCP sem mudar código do agente.
- **Categoria que estamos criando**: *AI Agent Control Plane*.
- **Beachhead**: fintech/e-commerce na UE e Brasil (EU AI Act alto risco vigora ago/2026).
- **Modelo**: open-core. Grátis: proxy, SDK, CLI. Pago (futuro): painel de compliance, retenção gerenciada, export SOC2/EU AI Act, replay.
- **North Star**: tool calls auditadas/semana. **Aha moment**: primeiro `tracerail verify` OK + primeira aprovação humana.

## 2. Mapa de ativos (o que existe e onde)

| Ativo | Caminho | Uso |
|---|---|---|
| Produto v0.1 (código + 25 testes) | `src/tracerail/`, `tests/` | `pip install -e ".[dev]"` e `python -m pytest` |
| Pitch de negócio | `docs/PITCH.md` | Base para conversas com investidores |
| Plano GTM com hipóteses H1–H5 | `docs/GTM.md` | **Seu painel de controle** — toda decisão volta aqui |
| Marca (voz, paleta, taglines, boilerplates) | `docs/BRAND.md` + `site/assets/logo.svg`, `favicon.svg` | Consistência em tudo que publica |
| Landing page SEO+AEO | `site/` | Publicar via GitHub Pages (gratuito) |
| Kit de lançamento | `marketing/launch-kit/` | Show HN, social, Product Hunt, cold emails, roteiro Mom Test |
| Vídeos | `marketing/videos/` | Teaser 30s pronto (`teaser-30s.mp4`, regenerável via `render_teaser.py`) + roteiros de 90s e 3min + guia de produção |
| Agentes de gestão | `.claude/agents/` | Ver §3 |
| Guia do repositório p/ IA | `CLAUDE.md` | Sessões futuras de Claude Code operam o repo sozinhas |

## 3. Como gerenciar: seus 5 agentes

Em qualquer sessão de Claude Code neste repo, invoque pelo nome:

| Agente | Quando usar | Exemplo de pedido |
|---|---|---|
| `startup-coo` | **Toda segunda-feira** | "Faça a weekly review" → status H1–H5, funil, 3 prioridades da semana, red flags |
| `customer-research` | Antes/depois de cada entrevista | "Sintetize estas notas de entrevista e atualize o status da H1" |
| `growth-marketer` | Qualquer conteúdo | "Escreva o post de blog 'EU AI Act logging for AI agents' seguindo BRAND.md" |
| `release-manager` | A cada versão | "Prepare o release v0.2: changelog, bump, checagem de consistência" |
| `compliance-analyst` | Vendas a CISO / roadmap regulatório | "Responda este questionário de segurança" / "Mapeie a feature X ao Art. 12" |

**Seu ritual mínimo (≈5h/semana de gestão):** segunda: weekly review com `startup-coo` (30min) → semana: executar as 3 prioridades (entrevistas você mesmo faz — fundador não delega discovery) → sexta: registrar evidências novas no GTM.md (commit).

## 4. Lançamento: checklist sequenciado

Pré-lançamento (1 semana):
1. Registrar domínio (`tracerail.dev` ou alternativa) e criar org GitHub dedicada; mover o repo; trocar os placeholders (`github.com/yourorg/...`, `hello@tracerail.dev`) em `site/` e `marketing/`.
2. Publicar `site/` no GitHub Pages (Settings → Pages → branch). Verificar Search Console + Bing Webmaster.
3. Gravar o demo de 3min seguindo `marketing/videos/video-scripts.md` + `production-guide.md` (terminal com VHS/asciinema). O teaser 30s já está pronto.
4. Começar as 20 entrevistas Mom Test (roteiro em `marketing/launch-kit/interview-script.md`) — **antes** do lançamento público, para H1 ter dados.

Lançamento:
5. Show HN (terça–quinta, ~9h ET) com `show-hn.md`; responder TUDO nas primeiras 4h (respostas a objeções já preparadas).
6. Mesma semana: thread X + LinkedIn + r/mcp e r/LLMDevs (`social-launch.md`); submeter às listas awesome-mcp e registries MCP.
7. Product Hunt 1–2 semanas depois (`product-hunt.md`), com o teaser como mídia.
8. Iniciar sequência de design partners (`design-partner-outreach.md`) com quem demonstrar interesse + alvos do beachhead.

## 5. Como escalar: estágios e gatilhos

| Estágio | Critério de entrada | Foco | O que mudar |
|---|---|---|---|
| **0 → Validação** (agora, S1–12) | — | H1–H5, 20 entrevistas, lançamento OSS | Nada de feature nova fora do plano 90 dias (GTM §8) |
| **1 → Tração** | H1+H3 confirmadas (500 stars/90d, ≥10% install) | v0.2: dashboard web de aprovações + replay; conteúdo SEO/AEO programático | Considerar aplicação YC/aceleradora com tração OSS |
| **2 → Receita** | 3 design partners ativos (H4) | Compliance packs (SOC2/EU AI Act export) pagos; pricing van Westendorp | Primeira contratação: founding engineer OSS-facing |
| **3 → Escala** | ≥US$10k MRR ou 5 logos enterprise | Cloud multi-tenant (v0.3), SSO/RBAC, SLA | Seed round: PITCH.md + métricas North Star + casos |

Regras de escala que não mudam: (a) o formato do audit log é contrato de compliance — retrocompatibilidade de `verify` sempre; (b) categoria antes de feature — todo conteúdo reforça "AI agent control plane"; (c) cortar > atrasar.

## 6. Kill criteria (honestidade com você mesmo)

Do GTM §9 — verifique mensalmente com o `startup-coo`:
- **H1 falha** (<8/20 entrevistas citam o problema) → pivô: auditoria de coding agents em CI/CD (mesma tecnologia, dor mais imediata).
- **H3 falha** (OSS não gera funil) → pivô de canal: vendas diretas compliance-led no beachhead.
- **H4 falha** (ninguém paga por compliance) → pivô de monetização: cobrar pelo painel de operações/aprovação (workflow), não pelo compliance.

## 7. Referência rápida de comandos

```bash
python -m pytest -q                          # saúde do produto
tracerail proxy --policies examples/policies.yaml -- python examples/toy_mcp_server.py
tracerail approvals && tracerail approve <id> --by você
tracerail verify                             # a demo que vende
python marketing/videos/render_teaser.py     # regenerar o teaser após mudanças de marca
```
