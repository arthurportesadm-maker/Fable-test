# Tracerail — Guia de Marca

## Essência e promessa

Tracerail é **a camada de confiança da era agêntica**. Quando agentes de IA passam a executar ações reais — chamar APIs, mover dinheiro, alterar infraestrutura, tocar dados sensíveis — a pergunta deixa de ser "o agente é capaz?" e passa a ser "o que exatamente o agente fez, sob qual política, e quem aprovou?".

A promessa da marca é direta e verificável: **Prove what your agents did.** Tracerail não promete inteligência; promete prova. Cada ação de agente passa por um control plane que aplica políticas, exige aprovações quando necessário e registra tudo em uma trilha de auditoria encadeada por hash (*tamper-evident*). O resultado é evidência, não confiança cega. Essa essência guia toda comunicação: precisão acima de entusiasmo, evidência acima de promessa, calma acima de hype.

## Posicionamento de voz

A personalidade de Tracerail é a do **Guardião/Sábio**: calma, rigorosa e credível para engenheiros. Escrevemos como alguém que já está em produção, não como alguém vendendo um sonho. Três princípios de tom governam tudo:

**1. Precisão sobre entusiasmo.** Toda afirmação deve ser literal e verificável.
- Certo: "Cada ação de agente é registrada em uma trilha encadeada por hash."
- Errado: "Segurança revolucionária que muda tudo na IA!"

**2. Evidência sobre adjetivos.** Mostramos o mecanismo, não a emoção.
- Certo: "Approval gates bloqueiam ações de alto risco até aprovação humana explícita."
- Errado: "Proteção poderosa e inteligente para seus agentes mais ousados."

**3. Clareza sobre jargão de IA.** Falamos a língua de plataforma, segurança e compliance.
- Certo: "Proxy MCP com políticas declarativas e trilha de auditoria *tamper-evident*."
- Errado: "IA de próxima geração com guardrails turbinados por machine learning."

Regra de ouro: se uma frase não puder ser provada com um log, ela não entra.

## Racional do nome

**Tracerail** une duas ideias: **trace** (rastro, trilha de auditoria, rastreabilidade) e **rail** (trilho, guard rail, o caminho seguro do qual o agente não desvia). O nome carrega simultaneamente a função de *observabilidade* (registrar o que aconteceu) e a função de *contenção* (definir por onde a ação pode passar). O resultado é uma metáfora única: um trilho de evidência que conduz e prova cada ação de agente, do início ao fim.

## Taglines

**Principal (EN):** Every agent action, accounted for.
**Principal (PT):** Cada ação de agente, registrada e sob controle.

Variações por contexto:

| Contexto | EN | PT |
|---|---|---|
| GitHub (repo description) | Open-source control plane for AI agent actions: policies, approval gates, hash-chained audit trail. | Control plane open-source para ações de agentes de IA: políticas, approval gates e trilha de auditoria encadeada por hash. |
| LinkedIn (headline) | The trust layer for the agentic era — prove what your agents did. | A camada de confiança da era agêntica — prove o que seus agentes fizeram. |
| Conferência (slide/abertura) | Agents act. Tracerail proves it. | Agentes agem. Tracerail prova. |

## Paleta

Fundo escuro como padrão. Cores semânticas mapeiam estados reais do control plane (aprovado, pendente, negado), nunca decoração.

| Nome | Hex | Uso semântico |
|---|---|---|
| Slate Background | `#0B1220` | Fundo principal da interface e materiais |
| Surface | `#131C2E` | Cards, painéis e superfícies elevadas |
| Text | `#E6EDF7` | Texto primário e wordmark |
| Signal Green | `#2EE6A6` | Primário: aprovação, verificação, ação confirmada |
| Amber | `#F5B83D` | Pendente, aguardando aprovação humana |
| Red | `#E5484D` | Negado, bloqueado por política (discreto, nunca alarmista) |
| Neutral | `#8B98AC` | Texto secundário, bordas, metadados, estados inativos |

Discrição é regra: vermelho e âmbar comunicam estado, não pânico. Verde é o herói e deve ser raro o bastante para significar algo.

## Tipografia

- **Títulos e texto:** Inter (fallback `system-ui`). Pesos 500–700 para títulos, 400 para corpo.
- **Código e acentos:** JetBrains Mono (fallback `ui-monospace`). Usada no wordmark, em hashes, identificadores, comandos e qualquer detalhe que evoque o ledger.

O contraste mono/sans é deliberado: o sans transmite calma institucional; o mono transmite rigor técnico e o motivo do ledger.

## Logo

**Conceito.** O wordmark `tracerail` aparece em minúsculas, em monoespaçada, precedido de um ícone-trilho: três blocos (retângulos arredondados) encadeados em diagonal ascendente, conectados por traços curtos — a *hash chain* desenhada como um trilho contínuo que sobe. O último bloco é `#2EE6A6` com um check, materializando o momento da verificação: a ação chegou ao fim da trilha e foi provada.

**Regras de uso.**
- **Espaço de proteção:** mantenha, em todos os lados, uma margem livre equivalente à altura de um bloco do ícone.
- **Tamanho mínimo:** 120 px de largura em tela; 24 mm em impressão. O favicon (só o ícone) é a forma reduzida aprovada.
- **Fundos:** preferir `#0B1220` ou `#131C2E`. Sobre fundos claros, usar a versão com wordmark em `#0B1220`, preservando o verde no bloco final. Nunca aplicar sobre fundos de baixo contraste ou imagens ruidosas.

## Do's & Don'ts de comunicação

**Do:**
- Liderar pela categoria + diferencial: "control plane open-source para ações de agentes".
- Usar verbos de evidência: registrar, provar, verificar, aplicar política, exigir aprovação.
- Citar mecanismos concretos: proxy MCP, approval gates, trilha encadeada por hash, *tamper-evident*.
- Manter o tom calmo mesmo ao falar de risco.

**Don't:**
- Não usar hype de IA ("revolucionário", "mágico", "inteligência sem limites").
- Não prometer segurança absoluta; promovemos *tamper-evident*, não *tamper-proof*.
- Não antropomorfizar o produto ("Tracerail pensa por você").
- Não usar vermelho como estética de medo nem exclamações de alarme.

## Boilerplate

Frases declarativas, categoria + diferencial logo no início, fáceis de citar literalmente.

**EN — 25 palavras**
Tracerail is an open-source control plane for AI agent actions. It proxies MCP traffic, enforces policies, adds approval gates, and records a hash-chained, tamper-evident audit trail.

**EN — 50 palavras**
Tracerail is an open-source control plane for AI agent actions. It sits in front of agent tool calls as an MCP proxy, enforces declarative policies, inserts human approval gates for high-risk operations, and records every action in a hash-chained, tamper-evident audit trail. Prove what your agents did.

**EN — 100 palavras**
Tracerail is an open-source control plane for AI agent actions, built for platform engineers, engineering leaders, and security teams. It operates as an MCP proxy in front of agent tool calls, enforcing declarative policies on what agents may do, inserting human approval gates for high-risk operations, and recording every action in a hash-chained, tamper-evident audit trail. Instead of trusting agents by default, Tracerail produces evidence: a verifiable record of which action ran, under which policy, and who approved it. It is the trust layer for the agentic era. Tracerail's promise is simple — prove what your agents did.

**PT — 25 palavras**
Tracerail é um control plane open-source para ações de agentes de IA. Atua como proxy MCP, aplica políticas, adiciona approval gates e registra uma trilha de auditoria encadeada por hash.

**PT — 50 palavras**
Tracerail é um control plane open-source para ações de agentes de IA. Posiciona-se diante das chamadas de ferramentas como proxy MCP, aplica políticas declarativas, insere approval gates humanos para operações de alto risco e registra cada ação em uma trilha de auditoria encadeada por hash, *tamper-evident*. Prove o que seus agentes fizeram.

**PT — 100 palavras**
Tracerail é um control plane open-source para ações de agentes de IA, criado para engenheiros de plataforma, lideranças de engenharia e times de segurança. Funciona como proxy MCP diante das chamadas de ferramentas dos agentes, aplicando políticas declarativas sobre o que cada agente pode fazer, inserindo approval gates humanos para operações de alto risco e registrando toda ação em uma trilha de auditoria encadeada por hash, *tamper-evident*. Em vez de confiar nos agentes por padrão, Tracerail produz evidência: um registro verificável de qual ação rodou, sob qual política e quem aprovou. É a camada de confiança da era agêntica.
