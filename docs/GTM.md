# Go-to-Market — Tracerail

Plano de go-to-market *hypothesis-driven*. Tracerail é um control plane open-source para ações de agentes de IA: proxy MCP drop-in, policy engine YAML (`allow`/`deny`/*spend caps*), *approval gates* humanos e trilha de auditoria *hash-chained* (à prova de adulteração). Modelo *open-core*: núcleo OSS gratuito; pago = painel de compliance, retenção, *export* SOC2/EU AI Act e *replay*.

Este documento não é um roadmap de features nem um plano financeiro. É uma lista de apostas ordenadas por risco, com testes baratos para cada uma, no espírito do *build-measure-learn*.

---

## 1. Posicionamento (April Dunford, *Obviously Awesome*)

Dunford define posicionamento como o contexto que faz seu produto parecer obviamente valioso. São cinco componentes:

**Alternativas competitivas** — o que o cliente usaria se Tracerail não existisse:
- Planilhas e logs caseiros: cada time costura `print`/JSONL próprio, sem garantia de integridade nem aprovação.
- LangSmith / Langfuse: *tracing* para *debug* de qualidade de prompt — não são *compliance-grade*, não param ações, não provam não-adulteração.
- Guardrails de AppSec (Prompt Security, Invariant): detecção de ameaça e prompt injection — focam em segurança, não em política operacional, aprovação e evidência auditável.

**Atributos únicos** — o que só Tracerail tem na interseção dessas alternativas:
- Trilha *hash-chained* verificável (`tracerail verify`): a integridade é *provável*, não prometida.
- *Approval gates* no caminho da chamada: a ação fica retida no `tools/call` até decisão humana — controle em runtime, não relatório pós-fato.
- Proxy MCP drop-in: governança sem tocar no código do agente.

**Valor provado** — o que esses atributos permitem que o cliente faça: passar de piloto a produção respondendo, com evidência aceitável por auditor/regulador, "o que o agente fez, quem autorizou, e que o registro não foi alterado" — sem reescrever o agente.

**ICP (características que valorizam esse valor ao máximo)** — times com agentes que tocam dinheiro ou dados sensíveis em produção, sob pressão regulatória (EU AI Act) ou de auditoria (SOC2).

**Categoria de mercado** — Tracerail não é "mais um observability tool". A jogada é *category design* (Play Bigger): nomear e ancorar **AI Agent Control Plane** — a camada entre observabilidade e segurança que governa ações. A categoria enquadra a comparação a nosso favor: tracing não governa; AppSec não audita.

---

## 2. Jobs To Be Done (Christensen / Ulwick)

**Job principal:** *"Quando meu agente executa ações com dinheiro ou dados reais, preciso provar o que ele fez e impedir o que ele não pode fazer, para escalar de piloto a produção sem assumir risco regulatório ou reputacional."*

O cliente não "compra um proxy". Ele contrata Tracerail para remover o medo que trava o rollout.

**Jobs secundários:**
- *"Quando o regulador ou auditor pede evidência de uma ação de agente, preciso entregar um registro íntegro e legível em minutos, para não virar um projeto de semanas de garimpo em logs."*
- *"Quando defino que ações sensíveis (reembolso acima de X, deploy, e-mail a cliente) exigem um humano, preciso que essa regra seja imposta no caminho da execução, para não depender de o agente 'lembrar' de pedir permissão."*

---

## 3. Beachhead (Geoffrey Moore, *Crossing the Chasm*)

Moore: para cruzar o abismo, domine um único nicho onde a dor é aguda e a referência se propaga.

**Segmento-alvo inicial:** fintechs e e-commerce na UE e no Brasil com agentes tocando dinheiro (reembolsos, pagamentos, ajustes de saldo). É o ponto de maior dor: dinheiro real + obrigação de logging do EU AI Act para alto risco vigorando em agosto/2026 + cultura dev madura que adota OSS *bottom-up*. A urgência regulatória cria um *compelling reason to buy* com data.

**Bowling pins seguintes** (cada conquista financia e referencia a próxima):
1. **Healthtech** — dados sensíveis, mesma necessidade de trilha íntegra e aprovação.
2. **SaaS de suporte** com agentes que agem em conta de cliente (reembolso, cancelamento, mudança de plano).
3. **Agências e dev shops de agentes** — multiplicador: cada agência instala Tracerail em N clientes.

A sequência é deliberada: o que aprendemos sobre *export* de evidência em fintech reaproveita quase inteiro em healthtech.

---

## 4. ICP e personas

| Papel | Quem | Dor central | Gatilho de compra | Objeção principal | Mensagem-chave |
|---|---|---|---|---|---|
| **Comprador** | VP Eng / Head of AI Platform | Rollout de agentes travado por risco; pressão por colocar em prod sem virar passivo | Primeiro incidente ou primeira pergunta de auditor/board sem resposta | "Posso construir isso internamente" | Governança em runtime drop-in via MCP, sem reescrever o agente — você não constrói nem mantém o encanamento |
| **Influenciador** | CISO / Compliance / DPO | Precisa de evidência defensável para SOC2 e EU AI Act; hoje não consegue atestar integridade | Auditoria agendada ou enquadramento de alto risco do EU AI Act | "OSS é seguro/maduro o bastante?" | Trilha *hash-chained* verificável + redação de campos sensíveis; *export* pronto para auditor |
| **Usuário** | Platform / ML engineer | Costura logs e checagens caseiras; quebra a cada novo agente | Mais um pedido de "adiciona um log de auditoria aqui" | "Mais uma camada no caminho crítico" | Drop-in em minutos, políticas como YAML versionado, `tracerail verify` no CI |

---

## 5. Hipóteses e testes (Lean Startup / Ries + *The Mom Test* / Fitzpatrick)

Ordenadas do risco maior ao menor. Cada hipótese tem enunciado falseável, *Riskiest Assumption Test* (RAT), métrica e critério de invalidação. O Mom Test rege as entrevistas: perguntar sobre o passado e comportamentos concretos, nunca pedir opinião sobre a ideia.

| # | Hipótese (falseável) | Teste / RAT | Métrica | Critério de invalidação |
|---|---|---|---|---|
| **H1 — Problema** | ≥40% dos times com agentes em prod citam auditoria/aprovação como bloqueador real de rollout | 20 entrevistas Mom-Test com times com agentes em prod + survey em comunidades MCP / Discords | nº de entrevistados que citam o bloqueador *sem* induzirmos | Invalida se <8 de 20 citam espontaneamente |
| **H2 — Gatilho/mensagem** | "Drop-in sem mudar código" converte mais que "SDK/integração" | A/B do *hero* na landing + telemetria opt-in comparando adoção proxy vs SDK | taxa de instalação proxy vs SDK; CTR do hero A vs B | Invalida se proxy não supera SDK com significância, ou A ≈ B |
| **H3 — Canal** | OSS dev-first gera funil de aquisição viável | Show HN + listas *awesome-mcp* + MCP registries → medir stars e conversão | 500 GitHub stars em 90 dias; ≥10% star→install | Invalida se <500 stars em 90 dias *ou* conversão star→install <10% |
| **H4 — Monetização** | O *compliance dashboard*/export é o que as empresas pagam | 3 design partners com LOI em 60 dias; teste de preço van Westendorp | nº de LOIs; faixa de preço aceitável (PSM) | Invalida se <3 LOIs em 60 dias, ou disposição a pagar abaixo do custo de servir |
| **H5 — Descoberta por IA** | ≥20% do tráfego qualificado vem de assistentes de IA (AEO) | Tracking de referrer/UTM + páginas otimizadas para citação por LLM | % do tráfego qualificado com origem em assistentes de IA em 6 meses | Invalida se <20% em 6 meses |

H1 é a aposta-mãe: se o problema não dói o suficiente para ser citado sem indução, nada abaixo importa (ver kill criteria).

---

## 6. Canais (Bullseye, *Traction* / Weinberg & Mares)

Bullseye: faça *brainstorm* dos 19 canais, teste barato no anel do meio, e dobre na aposta do anel interno. Os três anéis para Tracerail:

- **Outer ring (descartar por ora):** paid ads, eventos presenciais, *outbound* sales tradicional, parcerias enterprise. Caros e prematuros para um motion *bottom-up* em estágio de validação.
- **Middle ring (testar barato):** publicações em engineering blogs, podcasts de dev/MLOps, parcerias com vendors de MCP server.
- **Inner ring (apostar):**
  1. **Comunidade OSS** — GitHub, Show HN, *awesome-mcp*, MCP registries.
  2. **SEO + AEO programático** — páginas "vs LangSmith", "EU AI Act agent logging", glossário de termos do control plane.
  3. **Conteúdo técnico de fundador** — *deep dives* sobre hash-chaining, approval gates, governança de agentes.

**Primeira ação concreta na semana 1, por canal do inner ring:**

| Canal | Ação na semana 1 |
|---|---|
| Comunidade OSS | Repositório público polido (README + quickstart de 2 min + GIF do `tracerail verify`) e submissão a 1 lista *awesome-mcp* via PR |
| SEO + AEO | Publicar a primeira página de comparação "Tracerail vs LangSmith" com schema/estrutura citável por LLM e UTM de tracking |
| Conteúdo de fundador | Escrever e publicar 1 post técnico: "Como provar o que um agente de IA fez: hash-chained audit logs na prática" |

---

## 7. Motion PLG open-core (Product-Led Growth / Bush)

Bush: o produto é o principal motor de aquisição, ativação e expansão. O núcleo OSS faz a aquisição; a dor de compliance puxa a conversão. Funil AARRR:

- **North Star Metric:** nº de *tool calls* auditadas por semana. Mede valor real entregue (governança em uso), não vaidade (stars).
- **Aha moment:** primeiro `tracerail verify` retornando OK **e** primeira aprovação humana resolvida — o instante em que o usuário *vê* a trilha íntegra e *sente* o controle no caminho da chamada.

**Funil:**

| Etapa AARRR | Evento | Sinal de saúde |
|---|---|---|
| Acquisition | `pip install` / star no GitHub | star→install ≥10% (H3) |
| Activation | Primeiro `tracerail verify` OK + primeira aprovação resolvida | % de instalações que chegam ao aha em 24h |
| Retention | Proxy rodando ≥7 dias com calls auditadas recorrentes | tool calls auditadas/semana por deployment (North Star) |
| Revenue | Conversa de compliance → LOI / plano pago | orgs com >1 usuário ativo que pedem export/dashboard |
| Referral | Indicação para outro time/agência | nº de instalações originadas de indicação |

**Instrumentação mínima, respeitando privacidade:** telemetria estritamente **opt-in**, anônima e agregada — contagem de tool calls auditadas, se `verify` rodou, proxy vs SDK, aha atingido. Nunca conteúdo de chamadas, argumentos ou campos sob `redact`. O default é não enviar nada; o pitch de privacidade é parte do produto e reforça a credibilidade de compliance.

---

## 8. Plano de 90 dias

Cada bloco testa explicitamente uma ou mais hipóteses. Não avançar de bloco sem o sinal mínimo do anterior.

| Bloco | Entregáveis | Hipótese testada |
|---|---|---|
| **S1–2** | Repo público polido (quickstart 2 min, GIF de `verify`); roteiro Mom-Test; iniciar 20 entrevistas; instrumentar telemetria opt-in | H1 (problema) |
| **S3–4** | Fechar 20 entrevistas + survey em Discords MCP; landing com A/B do hero (drop-in vs SDK); primeira página AEO "vs LangSmith" | H1, H2 |
| **S5–8** | Show HN + submissões awesome-mcp e MCP registries; 2 posts técnicos de fundador; medir star→install; iniciar conversas com design partners | H3, H2, H4 |
| **S9–12** | Buscar 3 LOIs; teste de preço van Westendorp; expandir páginas AEO (EU AI Act logging, glossário) e medir referrer de assistentes de IA | H4, H5 |

Gate de avanço: só investir pesado em H4/H5 (S9–12) se H1 confirmou (≥8/20) e H3 mostra tração de funil.

---

## 9. Riscos e kill criteria

| Risco | Sinal de falha | Decisão (pivô) |
|---|---|---|
| **Problema fraco (H1)** — auditoria/aprovação não é bloqueador agudo o suficiente | <8/20 entrevistados citam espontaneamente | Pivô para **auditoria de coding agents em CI**: mesma trilha hash-chained e gates aplicados a agentes que escrevem/deployam código, onde a dor de revisão é tangível e imediata |
| **Canal OSS não converte (H3)** — stars não viram instalações nem uso | <500 stars/90d ou star→install <10% | Reposicionar para **design-partner-led**: vender direto a 3–5 fintechs sob pressão do EU AI Act, validando valor antes de re-tentar o motion bottom-up |
| **Sem disposição a pagar (H4)** — OSS é adotado mas o open-core não monetiza | 0–1 LOI em 60d ou preço abaixo do custo de servir | Mover a linha do open-core: levar *export* SOC2/EU AI Act e retenção para o lado pago mais cedo, ou pivotar para **cloud gerenciada** como wedge de receita |

**Princípio de decisão:** cada kill criterion é numérico e datado de propósito. A meta dos 90 dias não é crescer — é descobrir, ao menor custo, se Tracerail tem um problema agudo, um canal que converte e alguém que paga. Crescer vem depois que as três respostas forem "sim".
