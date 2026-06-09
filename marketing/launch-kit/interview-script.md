# Roteiro de entrevista — Mom Test (H1 do GTM)

Objetivo: validar/invalidar **H1** — "≥40% dos times com agentes em prod citam auditoria/aprovação como bloqueador real de rollout". Meta: 20 entrevistas. Critério de invalidação: <8 de 20 citam o bloqueador **espontaneamente, sem indução**.

Princípio do Mom Test (Rob Fitzpatrick): fale sobre a vida e o passado *deles*, nunca sobre a sua ideia. Pergunte sobre comportamentos concretos e específicos que já aconteceram, nunca sobre o futuro ou hipóteses. Não venda. Não mencione Tracerail até o fim (e idealmente nem aí, na entrevista de problema).

---

## Critérios de qualificação do entrevistado

Antes de agendar, confirme que a pessoa:
1. Trabalha em um time que **já tem pelo menos um agente de IA executando ações em produção** (não POC, não chatbot read-only). Ações = escreve em sistema, move dinheiro, manda e-mail, faz deploy, altera dados.
2. Atua como **dono técnico ou de plataforma** desse agente (Platform/ML/Backend eng, Head of AI Platform, VP Eng) — alguém que sente a dor de operar, não só de demonstrar.
3. Bônus de alta prioridade: o agente **toca dinheiro ou dados sensíveis** (fintech, e-commerce, healthtech) — é o beachhead.

Desqualifica (registre, mas conte à parte): apenas POC interno sem ações reais; só usa agente para geração de texto sem efeito colateral; não tem visão do que acontece em prod.

---

## 10 perguntas (passado e comportamento — nunca futuro/hipotético)

Abertura (1 min): "Não estou aqui para mostrar nada nem vender — estou tentando entender como times de verdade operam agentes em produção. Pode me contar do seu, com exemplos concretos do que já aconteceu?"

1. Me conta sobre o último agente que vocês colocaram para tomar ações em produção. O que ele faz, exatamente, e desde quando está rodando?
2. Como foi o caminho do piloto até produção? O que travou ou atrasou esse rollout — me dá o exemplo concreto mais recente.
3. Da última vez que o agente fez algo que não devia (ou quase), como vocês descobriram? Me conta o episódio.
4. Quando isso aconteceu, o que você fez para entender o que tinha ocorrido? Que dados você foi olhar, e quanto tempo levou?
5. Hoje, se alguém — auditor, segurança, board, um cliente — pedisse para você provar exatamente o que o agente fez numa ação específica e quem autorizou, como você faria? Já te pediram isso?
6. Tem alguma ação que vocês *não* deixam o agente fazer sozinho hoje? Como vocês implementaram esse limite na prática — me mostra como funciona.
7. Como vocês decidem quando uma ação precisa de um humano no meio? Quem aprova, e por onde isso passa hoje?
8. Quanto de logging/auditoria de agentes vocês construíram internamente? Quem mantém isso e quanto tempo já consumiu?
9. Na última conversa com segurança/compliance/jurídico sobre esses agentes, o que eles pediram que vocês ainda não conseguem entregar?
10. De tudo que a gente falou, o que é a coisa mais dolorosa hoje em operar esses agentes? E o que você já tentou para resolver — funcionou?

Fechamento: "Isso foi muito útil. Tem mais alguém no seu time ou na sua rede que vive essa dor e com quem eu deveria falar?" (referral) + "Posso te procurar de novo se eu tiver mais perguntas?"

---

## Armadilhas a evitar

- **Não pergunte sobre o futuro/hipotético.** "Você usaria uma ferramenta que...?" / "Você pagaria por...?" — respostas inventadas, sem valor. Sempre puxe para o passado: "Da última vez que..."
- **Não mencione sua ideia/solução.** No instante em que você descreve Tracerail, o entrevistado vira gentil e enviesa tudo. Guarde para o final, fora do bloco de pesquisa.
- **Não aceite elogio como dado.** "Boa ideia", "legal isso" = ruído. Só conta comportamento concreto: o que já fizeram, gastaram, sofreram.
- **Não aceite generalidades.** "A gente geralmente loga tudo" → "Me mostra o último caso em que você precisou desse log. O que você fez?"
- **Não induza o bloqueador.** Se você perguntar "auditoria é um problema pra vocês?", a citação **não conta** para H1. Só vale o que surge espontaneamente.
- **Não fale mais que o entrevistado.** Meta: você fala <30% do tempo. Silêncio é ferramenta.
- **Não busque validação — busca verdade.** Uma entrevista que mata a hipótese mais barato é uma entrevista boa.
- **Não pule o compromisso/avanço.** Peça referral ou próximo passo; interesse real vira ação (apresentação, dado, tempo).

---

## Template de síntese pós-entrevista

Preencher em até 1h após cada entrevista, enquanto está fresco.

```
Entrevistado: __________   Cargo: __________   Empresa/Setor: __________
Data: __________   Entrevistador: __________   Duração: ___ min
Qualificado? (S/N): ___   Toca dinheiro/dados sensíveis? (S/N): ___

Agente em prod (o que faz, há quanto tempo):
__________________________________________________

H1 — Citou auditoria/aprovação como bloqueador ESPONTANEAMENTE (sem indução)? (S/N): ___
  Cite a frase exata do entrevistado:
  "__________________________________________________"

Dor #1 declarada (palavras dele):
__________________________________________________

O que JÁ tentou/construiu para resolver (comportamento concreto):
__________________________________________________

Episódio concreto mais revelador (incidente, pedido de auditor, etc.):
__________________________________________________

Sinais de compliance/segurança (EU AI Act, SOC2, pedido não atendido):
__________________________________________________

Surpresa / algo que contradiz nossa hipótese:
__________________________________________________

Citação memorável (verbatim):
__________________________________________________

Próximo passo / referral obtido:
__________________________________________________
```

---

## Planilha de tracking (uma linha por entrevista)

| # | Data | Entrevistado | Cargo | Setor | Qualif.? | $/dados sensíveis? | Citou bloqueador espontaneamente? | Dor #1 (resumo) | Já construiu solução caseira? | Sinal compliance? | Referral? | Link síntese |
|---|------|--------------|-------|-------|----------|--------------------|-----------------------------------|-----------------|-------------------------------|-------------------|-----------|--------------|
| 1 |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |  |  |  |  |
| ... |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 |  |  |  |  |  |  |  |  |  |  |  |  |

**Placar H1:** citações espontâneas = ___ / 20.
- **≥8/20** → H1 confirmada, seguir o plano de 90 dias.
- **<8/20** → H1 invalidada → avaliar pivô (auditoria de coding agents em CI, ver GTM §9).
