# Tracerail — Guia de Produção de Vídeo (solo)

Guia prático para o fundador produzir os 3 vídeos sozinho, do zero ao publicado, sem equipe. Direto ao ponto. Use junto com [video-scripts.md](video-scripts.md).

Princípio que vale mais que qualquer ferramenta: **terminal real, comandos reais.** O público (engenheiros) detecta mock em segundos. A credibilidade é o produto.

---

## 1. Stack de ferramentas (grátis / barato)

### Gravação de terminal (o coração da demo)
- **VHS (Charm)** — recomendado. Você escreve um `.tape` (script de comandos + timing) e ele renderiza um GIF/MP4 perfeito, reproduzível. Ideal porque toda regravação fica idêntica. Grátis, open-source.
- **asciinema** — grava a sessão real do terminal como texto (leve, regravável). Bom para os trechos onde quer autenticidade pura. Exporte para vídeo com `agg` quando precisar de MP4.
- Dica: defina o tema do terminal nas cores da marca (fundo `#0B1220`, texto `#E6EDF7`, verde `#2EE6A6`). Fonte **JetBrains Mono**. Isso já dá identidade sem edição.

### Captura de tela (editor, navegador, diagrama)
- **OBS Studio** — grátis. Para gravar o editor abrindo o `policies.yaml`, o navegador, ou compor terminal + webcam. Grave em 1080p/60 ou superior; cena limpa, sem barra de tarefas.

### Edição
- **CapCut (desktop)** — rápido, grátis, ótimo para legendas automáticas e cortes. Suficiente para o Teaser e o Launch.
- **DaVinci Resolve** — grátis, mais controle (color, áudio, timeline). Use se quiser caprichar no Launch e no Demo de 3 min.

### Voz (VO)
- **ElevenLabs** — VO em EN com qualidade alta; escolha uma voz calma e sóbria (combina com o tom Guardião/Sábio). Evite vozes "vendedor animado".
- **Voz própria** — totalmente válido e mais autêntico para o Demo técnico. Grave com microfone decente, ambiente tratado, e limpe com o de-noise do Resolve/CapCut.
- Regra: VO nunca exagera. Lê a evidência, não vende o sonho.

### Música e SFX
- **Artlist** / **Epidemic Sound** — licença segura para YouTube e ads (pago, barato no plano anual).
- **YouTube Audio Library** / **Uppbeat** — opções grátis com atribuição.
- Estilo: ambiente eletrônico minimalista, baixo, sem drops de hype. SFX discretos (tick no deny, nota suave no approve, resolução no verify). Sem áudio de alarme.

---

## 2. Specs de export por plataforma

| Plataforma | Vídeo | Aspect | Resolução | Duração-alvo | FPS | Legendas | Observações |
|---|---|---|---|---|---|---|---|
| **X (feed)** | Teaser | 1:1 ou 9:16 | 1080×1080 / 1080×1920 | 30s (máx prático ~2:20) | 30 | **Queimadas (burned-in)** | Autoplay mudo: legenda obrigatória. MP4 H.264, ~< 512 MB |
| **LinkedIn (feed)** | Teaser / Launch | 1:1 (feed) ou 16:9 | 1080×1080 / 1920×1080 | 30–90s | 30 | **Queimadas** | Sobe `.srt` separado também. MP4 H.264 |
| **YouTube (landscape)** | Launch / Demo | 16:9 | 1920×1080 (ou 4K se gravou) | 90s / 3min | 30 ou 60 | `.srt` enviado + capítulos | Inclua chapters na descrição. H.264, áudio AAC 320 kbps |
| **YouTube Shorts** (opcional, recorte do Teaser) | Teaser | 9:16 | 1080×1920 | ≤ 60s | 30 | Queimadas | Bom para alcance extra |
| **Site (hero)** | Launch | 16:9 | 1920×1080 | 90s | 30 | Auto-mudo + toggle | Sirva também um poster `.jpg` e versão `.webm` leve |

Regras transversais:
- **Sempre** suba legendas EN (o conteúdo é global e muito assistido no mudo).
- Bitrate alvo: 1080p ≈ 8–12 Mbps; 4K ≈ 35–45 Mbps.
- Codec: H.264 (MP4) para máxima compatibilidade; `.webm`/VP9 para o site.
- Loudness: normalize a ~ -14 LUFS (web) para a VO não estourar nem sumir.

---

## 3. Identidade visual a respeitar (conforme BRAND.md)

**Cores** (fundo escuro é padrão; cor = estado, nunca decoração):

| Uso | Cor | Hex |
|---|---|---|
| Fundo principal | Slate Background | `#0B1220` |
| Cards / superfícies | Surface | `#131C2E` |
| Texto / wordmark | Text | `#E6EDF7` |
| Aprovação / verificação / OK | Signal Green | `#2EE6A6` |
| Pendente / aguardando humano | Amber | `#F5B83D` |
| Negado / bloqueado (discreto) | Red | `#E5484D` |
| Texto secundário, bordas, metadados | Neutral | `#8B98AC` |

- Verde é o **herói**: use com parcimônia, só no momento da prova (verify, approved). Se o verde aparece o tempo todo, perde o significado.
- Vermelho e âmbar comunicam **estado**, não pânico: sem flashes, sem alarme.

**Tipografia:**
- Títulos e texto on-screen: **Inter** (fallback `system-ui`), pesos 500–700 títulos, 400 corpo.
- Terminal, hashes, comandos, wordmark: **JetBrains Mono** (fallback `ui-monospace`).
- O contraste mono/sans é intencional: sans = calma institucional, mono = rigor do ledger.

**Logo:** wordmark `tracerail` minúsculo em mono, com o ícone-trilho (3 blocos encadeados em diagonal ascendente; último bloco verde com check). Respeite o espaço de proteção (margem = altura de 1 bloco) e o tamanho mínimo (120 px de largura em tela). Sobre `#0B1220` ou `#131C2E`.

**Voz/copy on-screen:** EN, declarativa, citável. Categoria + diferencial cedo. Verbos de evidência (prove, verify, enforce, deny, approve). **Don't:** "revolucionário", "mágico", promessa de segurança absoluta (é *tamper-evident*, não *tamper-proof*), antropomorfizar o produto, exclamações de alarme.

---

## 4. Checklist de publicação

Antes de exportar:
- [ ] Terminal real, comandos reais, todos batendo com o README (`pip install -e .`, `tracerail proxy …`, `approvals`, `approve … --by alice`, `log -v --tail`, `verify`).
- [ ] Nenhum segredo na tela (token, chave, e-mail real, path com nome de cliente). Os campos `redact` (`password`, `api_key`) não aparecem.
- [ ] Cores de estado corretas: deny vermelho discreto, pending âmbar, verify verde.
- [ ] Legendas EN sincronizadas e revisadas (sem erro de typo no terminal congelado).
- [ ] Claim da estatística com fonte na tela ("Menlo Ventures") e sem distorção.
- [ ] Tagline correta: "Every agent action, accounted for." / categoria "the open-source AI agent control plane".

Ao publicar:
- [ ] Export no aspect/resolução certos por plataforma (tabela acima).
- [ ] `.srt` enviado no YouTube/LinkedIn; legendas queimadas no X.
- [ ] Título e descrição com keywords: **AI agent governance, MCP proxy, AI audit trail, EU AI Act**.
- [ ] Capítulos na descrição (Launch e Demo).
- [ ] Thumbnail no padrão da marca (fundo escuro, verde só no verify, sem clickbait).
- [ ] Link do GitHub (Apache-2.0) e dos docs no primeiro parágrafo e no card final.
- [ ] Poster/`.webm` gerados para o embed do site.
- [ ] Pin de um comentário com o link do repo + "PRs welcome".

---

## 5. Cinco erros comuns em vídeos de dev tools (evite)

1. **Demo falsa ou acelerada demais.** Engenheiro percebe mock e edição que "pula" o comando que falha. Grave de verdade, deixe o comando rodar, mostre a saída real. Se algo é lento, corte limpo — não finja.
2. **Começar pela empresa, não pelo problema.** Ninguém liga para "fundada em…". Abra com a dor real (agentes agem; você consegue provar o quê?) nos primeiros 3 segundos.
3. **Texto ilegível no terminal.** Fonte pequena, baixo contraste, janela cheia de ruído. Aumente a fonte (JetBrains Mono grande), tema escuro da marca, foco só no que importa, zoom nos trechos-chave.
4. **Sem legendas / depender do áudio.** A maioria assiste no mudo (X/LinkedIn principalmente). Legenda EN sempre; no feed, queimada.
5. **Hype em vez de evidência.** "Revolucionário", "mágico", música épica com drop, promessa de segurança absoluta. Quebra o tom da marca e a confiança do público técnico. Mostre o mecanismo (deny → approve → verify) e deixe a prova falar.

---

Caminhos dos arquivos deste pacote:
- Roteiros: `/home/user/Fable-test/marketing/videos/video-scripts.md`
- Guia de produção: `/home/user/Fable-test/marketing/videos/production-guide.md`
