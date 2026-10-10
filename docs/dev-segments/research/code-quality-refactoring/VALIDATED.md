# Qualidade de código, revisão, refatoração e debugging — VALIDADO (consolidado das 3 lentes)

Data: 2026-10-10 · Validador: claude-sonnet-5-5 (modelo diferente dos pesquisadores, claude-haiku-5-5, mas da mesma família Claude; a independência é parcial e está declarada) · Segmento: `code-quality-refactoring`

Arquivos validados: `authoritative.md` (29 itens), `github.md` (20), `community.md` (24). Total recebido: 73.

## Estatísticas por lente

| Lente | Recebidos | Aprovados sem mudança de classe | Rebaixados (classe reduzida, restrição de uso ou ressalva obrigatória) | Rejeitados como item | Itens com fonte primária re-verificada por ferramenta |
| --- | --- | --- | --- | --- | --- |
| authoritative | 29 | 25 | 3 (R-08, R-09, R-24) | 1 (R-28) | 29 de 29 |
| github | 20 | 15 | 4 (R-04, R-08, R-09, R-19) | 1 (R-06) | 20 de 20 |
| community | 24 | 13 | 10 (R-01, 05, 07, 08, 10, 11, 13, 16, 20, 24) | 1 (R-17) | 24 de 24 |
| Total | 73 | 53 | 17 | 3 | 73 de 73 (existência); conteúdo lido a fundo em cerca de 60 |

Aprovados no total (incluindo rebaixados que continuam utilizáveis): 70. Esses 70 itens de origem foram consolidados em 40 itens validados (V-01 a V-40), porque as três lentes repetiram as mesmas fontes. Os itens V-36 a V-40 são novos: o validador os trouxe para cobrir lacunas declaradas pelos pesquisadores.

URLs re-verificadas com WebFetch (conteúdo lido): 73. Entre elas: todos os itens classe A, todos os que viram prompt, skill ou regra, as páginas do repositório (estrelas, forks, licença), 9 feeds de commits para datas de atualização e 4 comentários do Hacker News pela API Algolia. A pontuação de prompt vem da rubrica D1 a D12 e aparece como "fonte -> reescrito" quando o texto foi melhorado.

Média dos Prompt-scores dos conteúdos reescritos (23 itens do tipo prompt, skill, agente ou regra): 82,4. Observação: o escore avalia o conteúdo reutilizável como está escrito neste arquivo. O construtor precisa pontuar de novo o artefato final.

### Limitações da validação (declaradas)

- Verificado: o WebSearch estava sem orçamento (200 chamadas por turno, esgotado). Três tentativas do validador foram recusadas. Nenhuma busca foi contornada. As fontes novas dos itens V-36 a V-40 vieram de URLs canônicas conhecidas, abertas diretamente.
- Verificado: a API do GitHub devolveu HTTP 403 por limite de taxa (60 por hora, sem autenticação) via WebFetch e via curl; `gh` não está autenticado. Estrelas, forks e licença vieram das páginas HTML dos repositórios. Datas de atualização vieram dos feeds `commits/main.atom`.
- Não verificável: pontos e número de comentários dos itens do Hacker News; contagens de citações do artigo Reflexion; datas de publicação de várias páginas da documentação da Anthropic (a documentação é viva).
- O conteúdo reaproveitável abaixo está em redação própria. Nenhum texto literal de fonte sem licença permissiva foi copiado. A única lista usada com atribuição literal é o vocabulário do Conventional Comments (CC BY 3.0).

### Avisos transversais de direitos autorais e segurança

1. `anthropics/claude-code` tem `LICENSE.md` com "All rights reserved" e uso sujeito aos Termos Comerciais da Anthropic (Verificado). O README do `pr-review-toolkit` diz "MIT" (Verificado), o que conflita com a licença do repositório. Tratar tudo de `anthropics/claude-code/plugins/*` como não permissivo: só destilar com redação própria.
2. `anthropics/claude-plugins-official` declara Apache-2.0 na raiz (Verificado). O README por plugin do `code-simplifier` não existe (HTTP 404), então a licença por plugin é Inferido a partir da raiz.
3. `garrytan/gstack` (MIT) instala executando `./setup`, que compila binário, baixa o Chromium, edita o CLAUDE.md, registra hooks em `~/.claude/settings.json` (inclusive um hook Stop ligado por padrão), faz verificação de atualização silenciosa e tem telemetria opcional para Supabase (Verificado no README). Não instalar nem copiar scripts. Só ideias descritas em prosa.
4. `anthropics/claude-plugins-official/plugins/code-modernization` traz 5 hooks de telemetria e um painel que exige `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1` (Verificado). Não instalar nem embutir hooks; só destilar o método.
5. Os agentes do VoltAgent têm exemplos com números fabricados (47 arquivos, 72% a 89% de cobertura, 156 métodos) que um modelo pode reproduzir como resultado real. Não reaproveitar texto.
6. Regra de plugin: sem hooks de shell, sem `.mcp.json` ativo, sem postagem automática em GitHub. O pipeline de revisão posta comentário só com autorização explícita do usuário.

---

## Itens aprovados

### V-01 — Verificação executável e evidência antes de "pronto" (origens R-authoritative-01, R-github-11, R-community-09) — Classe A (8/10) · Prompt-score 84 -> 86
- **Lente:** authoritative, github, community
- **Tipo:** claude-md-rule | checklist
- **Fonte:** https://code.claude.com/docs/en/best-practices · **Autor/Org:** Anthropic (documentação oficial)
- **Sinais:** página viva e atual (Verificado: cita auto mode do Claude Code v2.1.283, `/goal`, `/verify`); licença não declarada (destilar).
- **Para que serve:** impedir que o agente pare em "parece pronto"; exigir prova.
- **Técnicas-chave (Verificado na página):** dar um check que devolve passa ou falha (testes, build, linter, comparação de saída, captura de tela); pedir causa raiz e não supressão do erro; mostrar evidência (saída do teste, comando executado) em vez de afirmar sucesso; Stop hook ou `/goal` como portão determinístico (opcional, fora do plugin seguro); sintoma + local provável + "como é corrigido" no pedido; depois de duas correções falhas no mesmo assunto, `/clear` e prompt melhor; teste de poda do CLAUDE.md: "remover esta linha faria Claude errar?".
- **Conteúdo reutilizável (redação própria):**
```markdown
## Verificação
- Antes de implementar, defina o check que prova que a tarefa está pronta (teste, build, linter, comparação de saída). Rode-o e cole o comando e a saída.
- Corrija a causa raiz. Não suprima o erro, não desative o teste, não afrouxe a asserção.
- Se não existir check executável, diga "não verificado" e proponha qual check criaria.
- Depois de duas correções falhas no mesmo problema, pare, resuma o que aprendeu e recomece com um pedido mais específico.
- Rotule cada afirmação: Verificado (executei e vi), Inferido (li o código), Suposição, Não verificável.
```
- **Ressalvas:** a taxa "validado em equipes internas" é afirmação da fonte (Não verificável por nós). Portão determinístico via hook fica fora do plugin (regra de segurança).
- **Verificação:** página lida na íntegra; todas as seis afirmações do pesquisador conferem. Nota de atualidade: a página agora cita a skill nativa `/code-review`; o plugin deve complementar, não duplicar.

### V-02 — Prompt de revisão adversarial em contexto novo, só lacunas de correção e requisito (R-authoritative-01, R-github-11, R-community-09) — Classe A (8/10) · Prompt-score 88
- **Lente:** authoritative, github, community
- **Tipo:** prompt | pattern
- **Fonte:** https://code.claude.com/docs/en/best-practices (seção "Add an adversarial review step") · **Autor/Org:** Anthropic
- **Sinais:** Verificado na página, incluindo a advertência de que um revisor pedido para achar lacunas quase sempre acha alguma, o que leva a overengineering.
- **Para que serve:** checar um diff contra um plano ou requisito sem viés do autor.
- **Técnicas-chave:** subagente em contexto novo vê só o diff e os critérios; critério declarado; "reporte lacunas, não preferências de estilo"; achados de baixo impacto viram opcionais.
- **Conteúdo reutilizável (redação própria):**
```text
<tarefa>Revise o diff atual contra {{PLANO_OU_REQUISITOS}}. Você não escreveu este código.</tarefa>
<verificar>
1. Cada requisito do plano foi implementado? Cite o arquivo:linha que o cumpre.
2. Cada caso de borda listado tem teste que falharia se o comportamento quebrasse?
3. Algo fora do escopo foi alterado?
</verificar>
<regras>
- Reporte só lacunas que afetam correção ou requisito declarado. Estilo e preferência ficam de fora.
- Para cada achado: arquivo:linha, impacto, evidência (o que você leu ou executou), correção sugerida.
- Rotule: Verificado, Inferido ou Suposição. Se não tiver certeza, não reporte; liste em "dúvidas".
- Se não houver lacuna, diga "nenhuma lacuna encontrada" e o que checou.
- Somente leitura: não edite arquivos.
</regras>
```
- **Ressalvas:** um revisor do mesmo modelo compartilha pontos cegos (a comunidade do HN levanta isso, ver V-35). Combine com testes.
- **Verificação:** trecho da doc lido; o prompt acima é reescrita própria, mais estruturada, não cópia.

### V-03 — Receitas oficiais de bug, refatoração e testes (R-authoritative-02, R-github-12) — Classe A (8/10) · Prompt-score 78 -> 82
- **Lente:** authoritative, github
- **Tipo:** workflow | checklist
- **Fonte:** https://code.claude.com/docs/en/common-workflows · **Autor/Org:** Anthropic
- **Sinais:** Verificado na página (receitas "Fix bugs efficiently", "Refactor code", "Work with tests").
- **Técnicas-chave:** informar o comando que reproduz e o stack trace, e se o erro é intermitente ou constante; refatorar em incrementos pequenos e testáveis mantendo o comportamento; testes que seguem o estilo do repositório e cobrem casos de borda; subagente para pesquisa de código grande.
- **Conteúdo reutilizável (redação própria):**
```text
Bug: comando de reprodução = {{CMD}}; erro/stack trace = {{TRACE}}; frequência = {{constante|intermitente}}.
Passos: reproduza -> leia o erro completo -> proponha 2 hipóteses com um teste para cada -> corrija a causa -> rode o teste que falhava e a suíte afetada.
Refatoração: liste os usos do trecho -> faça um passo pequeno por vez -> rode os testes após cada passo -> não misture mudança de comportamento.
```
- **Ressalvas:** receitas genéricas; a profundidade vem de V-04, V-10 e V-36.
- **Verificação:** página lida; o passo "peça opções e depois aplique" confere.

### V-04 — Skill `debug-causa-raiz`: quatro fases e regra dos três — Classe A (8/10) · Prompt-score 74 -> 90
(origens R-authoritative-15, R-github-01, R-community-02)
- **Lente:** authoritative, github, community
- **Tipo:** skill
- **Fonte:** https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md · **Autor/Org:** repositório `obra/superpowers` (nome pessoal do autor: Não verificado)
- **Sinais:** Verificado: 296,9 mil estrelas, 26,5 mil forks, MIT, 684 commits; último commit 2026-10-10 (release v7.0.0) pelo feed do repositório. Pontuação da fonte: autoridade 1, evidência 2, atualidade 2, comunidade 2, licença 1 = 8. Reclassificado de B para A pela pontuação mecânica.
- **Técnicas-chave (Verificado no arquivo):** frontmatter com `name: systematic-debugging` e descrição de gatilho; quatro fases em ordem (causa raiz, análise de padrões, hipótese e teste, implementação com teste que falha primeiro); parar após três correções falhas e discutir arquitetura; lista de alertas (palpite antes de rastrear, várias mudanças juntas, "correção rápida por ora"); arquivos de apoio sobre rastreio para trás na pilha, defesa em profundidade e espera por condição em vez de timeout. O arquivo tem cerca de 1.100 palavras, usa CAPS e absolutos, e cita skills externas (TDD, verificação antes de concluir).
- **Conteúdo reutilizável (redação própria, sem CAPS):**
```markdown
---
name: debug-causa-raiz
description: Use ao investigar bug, teste que falha, build quebrado ou comportamento inesperado, antes de propor correção. Gatilhos: "bug", "erro", "não funciona", "teste falhando", "debug", "por que quebrou".
---
Corrigir sintoma gera novo bug. Investigue a causa antes de editar.

1. Causa raiz: leia o erro e o stack trace inteiros; reproduza com um comando; veja mudanças recentes (git log/diff); em sistema com várias camadas, registre entrada e saída em cada fronteira; siga o valor errado de volta até a origem.
2. Padrão: ache código parecido que funciona e liste as diferenças.
3. Hipótese: escreva uma hipótese por vez ("acredito que X causa Y porque Z") e teste com a menor mudança possível. Se falhar, descarte e formule outra. Diga quando não entender algo.
4. Correção: escreva primeiro um teste que falha pelo motivo certo; aplique uma única correção na causa; rode o teste e a suíte afetada. Não refatore junto.

Parada: depois de 3 correções falhas, pare. Descreva o que tentou, o que cada tentativa revelou e proponha rever o desenho com o usuário.
Sinais para voltar à fase 1: propor correção sem rastrear; várias mudanças de uma vez; "deve ser X" sem prova; cada correção expõe outro problema.
Sem causa raiz achada: diga "causa não identificada", liste as evidências coletadas e o que falta medir.

Saída: causa raiz, evidência (comando e saída), correção, teste de regressão, prevenção. Rótulos: Verificado, Inferido, Suposição.
```
- **Ressalvas:** o texto original é enfático; o texto acima remove CAPS e referências a skills externas. O plugin deve manter a regra "teste antes da correção" sem depender das outras skills do superpowers.
- **Verificação:** SKILL.md aberto (frontmatter, fases, regra de parada, alertas, arquivos de apoio); repositório e licença pela página; data pelo feed.

### V-05 — Subagente `debugger`: fases e relatório de cinco campos (R-authoritative-27, R-github-03, R-github-07, R-community-03, R-community-04) — Classe B (6/10) · Prompt-score 70 -> 84
- **Lente:** authoritative, github, community
- **Tipo:** subagent
- **Fonte:** https://raw.githubusercontent.com/github/awesome-copilot/main/agents/debug.agent.md e https://raw.githubusercontent.com/wshobson/agents/main/plugins/debugging-toolkit/agents/debugger.md
- **Sinais:** awesome-copilot: 39,9 mil estrelas, MIT na página do repositório, commit em 2026-10-09; o arquivo não traz texto de licença. wshobson/agents: 40,3 mil estrelas, MIT, 604 commits, commit em 2026-10-04; o arquivo não declara `tools`.
- **Técnicas-chave (Verificado):** Copilot: quatro fases (avaliação, investigação, resolução, qualidade) e regra "reproduzir antes de corrigir"; lista de `tools` inclui edição, terminal, testes e `web/fetch`. wshobson: cinco passos (capturar erro, reproduzir, isolar, correção mínima, verificar) e saída com causa raiz, evidência, correção, teste e prevenção; `model: sonnet`, sem `tools`.
- **Conteúdo reutilizável (redação própria):**
```markdown
---
name: debugger
description: Investiga erro, stack trace ou teste que falha. Reproduz, isola a causa e devolve relatório com correção proposta. Use quando algo quebrou e a causa não é óbvia.
tools: Read, Grep, Glob, Bash
model: sonnet
---
Você investiga; não edita arquivos. Use Bash só para rodar o comando de reprodução, testes e `git log/diff/blame`.
Passos: 1) reproduza e registre esperado versus observado; 2) liste hipóteses em ordem de probabilidade, cada uma com o comando que a confirma ou refuta; 3) execute as verificações; 4) proponha o menor patch na causa raiz, como diff; 5) indique o teste de regressão e o comando que o roda.
Relatório: causa raiz | evidência (comando e saída) | correção proposta | teste de regressão | prevenção. Rotule Verificado, Inferido ou Suposição. Se não reproduzir, diga isso e liste o que coletou.
```
- **Ressalvas:** `Bash` amplo permite escrita via shell; o plugin deve instruir a delegação a passar o comando exato e documentar o risco. Restringir `Bash` por padrão de comando na lista `tools`: Não verificado. `permissionMode`, `hooks` e `mcpServers` são ignorados em subagente de plugin (V-09).
- **Verificação:** os dois arquivos abertos (frontmatter, fases, saída); repositórios pela página e feed. Rebaixado de "agente de escrita" para investigador, por segurança.

### V-06 — Pipeline `/review`: triagem, regras, revisão paralela, validação por achado, filtro (R-authoritative-07, R-github-05, R-community-06) — Classe A (8/10) · Prompt-score 82 -> 88
- **Lente:** authoritative, github, community
- **Tipo:** command | workflow
- **Fonte:** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md · **Autor/Org:** Anthropic (plugin oficial; README lista Boris Cherny como autor)
- **Sinais:** repositório com 149,9 mil estrelas e commit em 2026-10-09 (Verificado); licença do repositório proprietária (ver aviso 1): destilar.
- **Técnicas-chave (Verificado no arquivo):** nove passos: (1) triagem barata (PR fechado, rascunho, trivial ou já comentado); (2) caminhos dos CLAUDE.md relevantes; (3) resumo das mudanças; (4) quatro revisores em paralelo: dois de conformidade com CLAUDE.md, dois de bugs (um só no diff, outro em segurança e lógica do código introduzido); (5) um subagente de validação por achado; (6) descarta o que não valida; (7) saída no terminal; (8) plano interno de comentários; (9) postagem inline só com `--comment`. Filtro de alto sinal: erro de compilação ou parse, resultado certamente errado, violação de CLAUDE.md citável. Exclusões: problema pré-existente, código correto que parece bug, nitpick, o que o linter pegaria, qualidade geral sem regra, achado silenciado por comentário de lint. Links com SHA completo e linhas com contexto.
- **Correção importante:** o arquivo atual NÃO usa pontuação 0 a 100 nem limiar 80; o filtro é binário (valida ou descarta). O README do plugin ainda descreve pontuação com limiar 80 e um agente de histórico (git blame). O README está desatualizado em relação ao arquivo. Prevalece o arquivo (Verificado nos dois).
- **Conteúdo reutilizável (redação própria):**
```text
Etapas do /review (somente leitura por padrão):
0. Triagem: pare se não há diff, se é trivial ou se já foi revisado.
1. Coletar regras: caminhos dos CLAUDE.md que cobrem os arquivos alterados.
2. Resumir o diff em cinco linhas.
3. Revisões independentes: (a) conformidade com as regras do projeto, só regras que se possa citar; (b) bugs no diff; (c) segurança e lógica do código novo.
4. Validação: para cada achado, um segundo agente tenta refutá-lo lendo o código. Sem confirmação, descarte.
5. Filtro: mantenha só erro de compilação/tipo, resultado errado certo ou regra citada. Descarte: problema pré-existente, estilo, o que linter/typechecker pega, suposição que depende de entrada específica, item silenciado de propósito.
6. Saída: tabela com severidade, arquivo:linha, regra ou explicação, evidência, correção sugerida; ou "nenhum achado" com o que foi checado.
Postar no GitHub só se o usuário pedir explicitamente.
```
- **Ressalvas:** custo alto (muitos subagentes; reclamação registrada no HN). `gh` necessário só para PR. Modelos por etapa (haiku, sonnet, opus) dependem do que o usuário tem.
- **Verificação:** arquivo bruto lido; README do plugin lido na página `tree/main/plugins/code-review`; divergência confirmada.

### V-07 — Faixas de confiança 0–100 com limiar 80 e saída em dois grupos (R-authoritative-08, R-community-07) — Classe B (7/10; rebaixado de A) · Prompt-score 72 -> 82
- **Lente:** authoritative, community
- **Tipo:** subagent | prompt
- **Fonte:** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/pr-review-toolkit/agents/code-reviewer.md (a mesma estrutura existe em `anthropics/claude-plugins-official/plugins/pr-review-toolkit`, Verificado)
- **Sinais:** Anthropic; frontmatter `name: code-reviewer`, `model: opus`, `color: green`, sem `tools` (Verificado). Rebaixado a B por: licença proprietária no repositório de origem (aviso 1), pontuação ser autoavaliação do modelo e ausência de `tools`.
- **Técnicas-chave (Verificado):** faixas 0 a 25 (falso positivo ou pré-existente), 26 a 50 (nitpick), 51 a 75 (válido, baixo impacto), 76 a 90 (importante), 91 a 100 (crítico); reportar só 80 ou mais; saída em Crítico (90 a 100) e Importante (80 a 89), com arquivo, linha, regra e correção; sem achado, resumo curto.
- **Conteúdo reutilizável (redação própria):** adotar as faixas como critério de corte do revisor, com a etapa de validação do V-06 como prova real; o texto do prompt é o de V-02 com a tabela abaixo.
```text
Confiança do achado (0 a 100), baseada no que você executou ou leu, não em intuição:
0-25 provável falso positivo ou pré-existente | 26-50 nitpick | 51-75 válido, baixo impacto | 76-89 importante | 90-100 bug certo ou violação explícita de regra.
Reporte só >= 80. Informe a evidência que sustenta o número.
```
- **Ressalvas:** a nota é autoavaliação (modelos tendem a calibrar mal). Exige validação por V-06. `tools` deve ser declarado como `Read, Grep, Glob` na versão do plugin.
- **Verificação:** arquivo lido por WebFetch; faixas, limiar e formato conferem; ausência de `tools` confirmada.

### V-08 — Sequência de revisão por aspecto: seis agentes do `pr-review-toolkit` (R-authoritative-09) — Classe B (7/10; rebaixado de A) · n/a (referência)
- **Lente:** authoritative
- **Tipo:** workflow | reference
- **Fonte:** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/pr-review-toolkit/README.md
- **Sinais:** README diz "MIT" e autor "Daisy"; conflita com `LICENSE.md` proprietário do repositório (aviso 1). Rebaixado por esse conflito.
- **Técnicas-chave (Verificado):** agentes: comment-analyzer, pr-test-analyzer, silent-failure-hunter, type-design-analyzer, code-reviewer, code-simplifier; ordem: revisor geral, depois silent-failure-hunter se mexeu em tratamento de erro, depois testes, comentários, por último simplificação; sem slash commands, gatilhos em linguagem natural.
- **Conteúdo reutilizável (redação própria):** checklist por aspecto: correção e regras -> falhas silenciosas (catch vazio, fallback que mascara erro, falta de log) -> testes (comportamento, bordas, não linhas) -> comentários (verdadeiros, explicam o porquê) -> invariantes de tipos -> simplificação. Um agente por aspecto só quando o diff justificar.
- **Ressalvas:** o README não lista `tools` por agente.
- **Verificação:** README aberto.

### V-09 — Subagente revisor read-only: frontmatter, `tools` e limites de plugin (R-authoritative-06, R-authoritative-28, R-community-17, R-github-06) — Classe A (8/10) · Prompt-score 85
- **Lente:** authoritative, github, community
- **Tipo:** subagent | reference
- **Fonte:** https://code.claude.com/docs/en/sub-agents · **Autor/Org:** Anthropic
- **Sinais:** Verificado: campos `name`, `description` obrigatórios; `tools` (lista de permissão), `disallowedTools`, `model` (inclui `inherit`), `permissionMode`, `omitClaudeMd`, `skills`, `mcpServers`, `hooks`, `maxTurns`, `memory`, `background`, `effort`, `isolation`, `color`; campos desconhecidos são ignorados em silêncio.
- **Técnicas-chave:** subagente não vê o histórico, as skills invocadas nem os arquivos já lidos (exceto fork); carrega o CLAUDE.md (exceto Explore, Plan ou `omitClaudeMd: true`); em plugin, `hooks`, `mcpServers`, `permissionMode` e `initialPrompt` são ignorados; projeto em `.claude/agents/` sobrepõe usuário.
- **Correção ao pesquisador:** o aviso de inicialização não é por uma descrição longa, e sim quando a soma das descrições dos subagentes personalizados passa de 15.000 tokens. Manter `description` curta continua certo.
- **Conteúdo reutilizável (redação própria):**
```markdown
---
name: code-reviewer
description: Revisa um diff em contexto novo e reporta falhas de correção e de requisito. Use antes de commit ou PR.
tools: Read, Grep, Glob
model: sonnet
---
Papel: revisor somente leitura. Receba o diff e o critério no prompt de delegação; se faltar o diff, peça-o em vez de rodar comandos.
Passos: 1) leia o diff e os arquivos citados; 2) cheque correção, segurança e requisito; 3) reporte arquivo:linha, problema, evidência, correção sugerida; 4) veredito: aprovar, aprovar com ressalvas ou bloquear.
Rotule Verificado, Inferido ou Suposição. Não reporte estilo nem o que o linter pega.
```
- **Ressalvas:** um revisor sem `Bash` não consegue obter o diff sozinho; o comando ou skill que o chama deve coletar o diff e colá-lo no prompt (desenho recomendado). Sintaxe para limitar `Bash` por comando em `tools`: Não verificado.
- **Verificação:** doc lida (os primeiros 100.000 de 108.415 caracteres); o VoltAgent `code-reviewer.md` foi aberto e concede `Read, Write, Edit, Bash, Glob, Grep`, o que refuta a afirmação dos pesquisadores de que revisores dessa coletânea são somente leitura (ver tabela de rebaixados).

### V-10 — Bloco "Escopo do entregável": pedido é o escopo, extras viram follow-up (R-authoritative-03, R-community-22) — Classe A (8/10) · Prompt-score 88 -> 90
- **Lente:** authoritative, community
- **Tipo:** claude-md-rule | prompt
- **Fonte:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1 · **Autor/Org:** Anthropic
- **Sinais:** Verificado: a página existe e cobre Claude Fable 5.1 e Mythos 5.1; a seção "Keep changes and tests to what the task asks for" afirma queda substancial de extras e de testes commitados sem mudança mensurável no sucesso da tarefa (afirmação da fonte; Não verificável por nós). Específico de versão de modelo.
- **Conteúdo reutilizável (redação própria):**
```markdown
## Escopo
- O pedido (ou o plano aprovado) define o escopo. Não amplie nem reduza em silêncio.
- Bug pré-existente, problema de desempenho ou comportamento não pedido que você encontrar: não corrija nesta mudança. Liste no resumo como follow-up, salvo se o pedido não funcionar sem isso.
- Ambiguidade: implemente a leitura mais apoiada pelo texto e pelo código vizinho, declare a suposição e não construa para as outras leituras.
- Edite o trecho necessário em vez de reescrever o arquivo inteiro.
- Commite testes só quando a tarefa os pedir ou o repositório já mantenha testes desse tipo, no tamanho dos vizinhos. Scripts de verificação temporários não viram arquivos permanentes.
- Ação destrutiva ou além do pedido exige aval do usuário.
```
- **Ressalvas:** tratar como hipótese a medir nos evals do plugin (outros modelos podem se comportar diferente).
- **Verificação:** seção lida em `platform.claude.com` (texto do bloco lido; este bloco é reescrita própria).

### V-11 — Anti-overengineering, "ler antes de afirmar" e anti-gaming de testes (R-authoritative-04) — Classe A (8/10) · Prompt-score 84 -> 86
- **Lente:** authoritative
- **Tipo:** prompt | claude-md-rule
- **Fonte:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices · **Autor/Org:** Anthropic
- **Sinais:** Verificado: seção sobre overengineering (a página atribui a tendência a Opus 4.5 e 4.6), seção "Avoid focusing on passing tests and hardcoding" e orientação de ler o arquivo antes de responder. A página lista Claude Sonnet 5.5, Haiku 5.5 e Fable 5.1 entre os modelos atuais.
- **Conteúdo reutilizável (redação própria):**
```markdown
## Qualidade da solução
- Faça só a mudança pedida: sem arquivos extras, sem abstração para uso único, sem tratamento de erro para cenário impossível, sem comentário em código que você não alterou. Valide apenas nas fronteiras (entrada do usuário, APIs externas).
- Antes de afirmar algo sobre um arquivo, leia-o. Se não puder abrir, diga "não verificado".
- Escreva a solução geral, sem valores fixos para fazer teste passar. Se o teste parecer errado, avise em vez de contorná-lo.
```
- **Ressalvas:** a tendência descrita é de modelos anteriores; aplicar se os evals mostrarem o problema.
- **Verificação:** trechos localizados no arquivo salvo da página (linhas sobre overengineering, hardcoding e "read the file").

### V-12 — Skill `simplify`: simplificar sem mudar comportamento (R-authoritative-10, R-github-04, R-community-08) — Classe B (7/10) · Prompt-score 72 -> 84
- **Lente:** authoritative, github, community
- **Tipo:** skill | subagent
- **Fonte:** https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/code-simplifier/agents/code-simplifier.md · **Autor/Org:** Anthropic
- **Sinais:** repositório 37,6 mil estrelas, Apache-2.0 na raiz, commit em 2026-10-09 (Verificado). Frontmatter com `model: opus`, sem `tools`.
- **Técnicas-chave (Verificado):** mudar o "como", nunca o "o quê"; escopo = código tocado na sessão, salvo pedido; reduzir aninhamento e redundância, evitar ternário aninhado, preferir clareza a concisão, não juntar responsabilidades nem remover abstrações úteis; documentar só mudanças significativas. As regras de React, ES modules e `function` declarations são preferências de projeto e ficam fora do plugin genérico.
- **Conteúdo reutilizável (redação própria):**
```markdown
---
name: simplify
description: Simplifica código recém-alterado sem mudar o comportamento. Use depois de uma mudança, quando o código ficou aninhado, repetido ou confuso. Gatilhos: "simplifique", "limpe isso", "deixe mais legível", "simplify".
---
Escopo: apenas o diff atual ou os arquivos indicados.
Antes: rode os testes do trecho e registre o resultado. Se não houver teste, escreva um de caracterização (V-36) ou avise que a garantia de comportamento é só por leitura (Inferido).
Aplique, um passo por vez: reduzir aninhamento com retornos antecipados; remover duplicação; nomes que dizem a intenção; trocar ternário aninhado por if/else; apagar comentário que repete o código. Siga as convenções do CLAUDE.md.
Não faça: juntar responsabilidades sem relação, remover abstração que tem mais de um uso, mudar API pública, mexer fora do escopo.
Depois: rode os mesmos testes e confirme a saída igual. Resumo: o que mudou e por que, em até 5 linhas.
```
- **Ressalvas:** "preserva comportamento" só vale com teste; sem teste, o resultado é Inferido. Classe A por regra de fonte oficial foi recusada porque a licença por plugin não pôde ser verificada (README do plugin devolve 404).
- **Verificação:** arquivo e repositório lidos; feed de commits.

### V-13 — `/simplify` e `/batch` nativos e comportamento diff entre branches (R-authoritative-12, R-community-20) — Classe B (6/10) · Prompt-score 70 -> 78
- **Lente:** authoritative, community
- **Tipo:** command | workflow
- **Fonte:** https://support.claude.com/en/articles/14554000-claude-code-power-user-tips · **Autor/Org:** Anthropic (Central de Ajuda)
- **Sinais:** Verificado: `/simplify` roda agentes paralelos de reuso, qualidade, eficiência e CLAUDE.md; `/batch` entrevista e distribui para agentes em worktrees, cada um testa e abre seu PR; verificação é a "dica nº 1"; a dica de "descartar e reimplementar" também está. Data exata: Não verificável.
- **Conteúdo reutilizável (redação própria):** sequência "mudança -> simplify -> verificação de comportamento (testes e diff de saídas entre a branch e a base)"; antes de `/batch`, o plugin pede: o que migra, o critério de pronto, o check por arquivo. Antes de "descartar e refazer", commit ou checkpoint e teste de paridade. Prompt de endurecimento: "Liste os três pontos mais frágeis desta mudança, como você verificaria cada um, e só então proponha o PR."
- **Ressalvas:** comandos dependem da versão do Claude Code.
- **Verificação:** artigo lido; cinco afirmações conferem.

### V-14 — Migração com juiz primeiro, rulebook e paridade (R-authoritative-05, R-github-13, R-community-21) — Classe A (9/10) · Prompt-score 88
- **Lente:** authoritative, github, community
- **Tipo:** workflow | checklist
- **Fonte:** https://claude.com/blog/ai-code-migration ("How Anthropic runs large-scale code migrations with Claude Code", publicado em 2026-07-16 — Verificado) · **Autor/Org:** Anthropic
- **Sinais:** autoridade 3, evidência 1 (relato de caso, sem números), atualidade 2, comunidade 2, licença 0 (destilar). Reclassificado de B para A pelo conjunto das lentes e pela data confirmada.
- **Técnicas-chave (Verificado, as oito afirmações conferem):** construir o juiz antes e validá-lo contra código quebrado de propósito; rulebook + mapa de dependências + inventário de lacunas (o rulebook vem antes do inventário); piloto pequeno cujo resultado é descartado; fila em disco retomável (arquivo existe = feito); modelo menor para o volume, maior para revisão e regras; erro repetido vai para o rulebook e o lote é regenerado; revisão adversarial por dois revisores com terceiro como desempate; paridade comportamental com cenários rodados nos dois lados; sem suíte, construir uma a partir do original.
- **Conteúdo reutilizável (redação própria):**
```markdown
Checklist de migração (módulo, linguagem, framework ou versão):
- [ ] Juiz: comandos que rodam contra o original e o novo e dão o mesmo veredito; prove que ele falha em código quebrado de propósito.
- [ ] Rulebook (equivalências), mapa de dependências (ordem dos lotes) e inventário de comportamento implícito do original.
- [ ] Piloto de 3 a 5 arquivos; descarte a saída; ajuste as regras.
- [ ] Lotes retomáveis: lista em disco; arquivo concluído = saída existe e o juiz passa.
- [ ] Erro repetido: corrija a regra e regenere o lote; não remende arquivo por arquivo.
- [ ] Revisão adversarial citando a regra violada; desempate por um terceiro.
- [ ] Compilar, smoke test, suíte; agrupe falhas por causa raiz.
- [ ] Paridade: mesmos cenários nos dois lados; diferença de saída = pendência.
```
- **Ressalvas:** custo alto; em repositório pequeno, um juiz e um lote bastam. O fluxo usa vários agentes e deve ser adaptado ao que o usuário tem.
- **Verificação:** blog aberto e as oito afirmações conferidas uma a uma.

### V-15 — Modernização de legado: uplift, transform, reimagine e veredito por módulo (R-authoritative-13) — Classe B (7/10) · Prompt-score 80
- **Lente:** authoritative
- **Tipo:** workflow | checklist
- **Fonte:** https://github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization · **Autor/Org:** Anthropic
- **Sinais:** Verificado: Apache-2.0, CHANGELOG, testes, hooks, README extenso; nada edita o código legado (saída em `analysis/<nome>/` e `modernized/`).
- **Técnicas-chave (Verificado no README):** três tipos: uplift (mesma tecnologia, versão nova), transform (outra tecnologia, módulo a módulo, comparando entradas iguais), reimagine (nova arquitetura a partir de uma spec extraída); pré-verificação com prova de build; extração de regras; plano aprovado antes de construir; verificação independente com veredito por módulo: PROVEN (testes rodados do zero e saídas iguais), PARTLY PROVEN (falta evidência; o máximo quando o sistema antigo não roda), NOT PROVEN; endurecimento de segurança com patch aplicado pelo humano; permissões sugeridas negam edição do legado.
- **Conteúdo reutilizável (redação própria):** tabela de veredito de paridade por módulo (provado, parcialmente provado, não provado) com o critério de cada um; regra "nada é construído antes do plano aprovado"; regra "código legado fica em somente leitura".
- **Ressalvas:** NÃO instalar nem copiar hooks e telemetria (aviso 4). Só o método.
- **Verificação:** diretório e README lidos na página; licença Apache-2.0 pela página do plugin e do repositório.

### V-16 — Laço avaliador-otimizador com critério e parada; ferramentas com poka-yoke (R-authoritative-14) — Classe B (7/10) · n/a (referência)
- **Lente:** authoritative
- **Tipo:** pattern | reference
- **Fonte:** https://www.anthropic.com/engineering/building-effective-agents · **Autor/Org:** Anthropic (engenharia), publicado em 2024-12-19 (Verificado; a página avisa que parte da ferramenta mudou desde então).
- **Técnicas-chave (Verificado):** avaliador-otimizador vale quando há critério claro; código é caso forte porque testes dão feedback; incluir condição de parada como número máximo de iterações; "poka-yoke" nas ferramentas (exigir caminho absoluto removeu erros de caminho relativo); começar pelo padrão mais simples; frameworks podem esconder os prompts.
- **Conteúdo reutilizável:** regra "o ambiente (testes, compilador) é o juiz, não a autoavaliação" e limite de iterações no protocolo de correção. Atualidade: conceito estável, ferramentas citadas podem estar defasadas.
- **Verificação:** artigo lido; cinco afirmações conferem.

### V-17 — Checklist de revisão do Google, nove dimensões e padrão de aprovação (R-authoritative-17) — Classe B (6/10) · Prompt-score 76 -> 80
- **Lente:** authoritative
- **Tipo:** checklist | reference
- **Fonte:** https://google.github.io/eng-practices/review/reviewer/looking-for.html e https://google.github.io/eng-practices/review/reviewer/standard.html · **Autor/Org:** Google (engineering practices)
- **Sinais:** Verificado: seções Design, Functionality, Complexity, Tests, Naming, Comments, Style, Consistency, Documentation, Every Line, Context, Good Things; prefixo "Nit:" para preferência de estilo; a página diz só "This site is open source", sem licença nomeada (destilar).
- **Conteúdo reutilizável (redação própria):**
```markdown
Dimensões e a pergunta de cada uma
1 Design: a mudança pertence a este código e este é o momento certo?
2 Funcionalidade: faz o que o autor quer e serve ao usuário?
3 Complexidade: entende-se rápido, sem generalização especulativa?
4 Testes: existem, são corretos e falhariam se o código quebrasse?
5 Nomes: dizem a intenção sem ficar longos?
6 Comentários: explicam o porquê, não o quê?
7 Consistência: segue o guia de estilo e depois o código vizinho?
8 Documentação: README e referência atualizados?
Padrão: aprove quando a mudança melhora de forma clara a saúde do código, mesmo imperfeita; não aprove o que piora.
```
- **Ressalvas:** para revisor de agente, cortar estilo (ruído); humano mantém a lista completa. Conflito com o pipeline da Anthropic (V-06) resolvido assim: agente segue V-06, humano usa V-17.
- **Verificação:** duas páginas abertas.

### V-18 — Mudança pequena e separação de refatoração e comportamento (R-authoritative-18) — Classe B (6/10) · Prompt-score 80
- **Lente:** authoritative
- **Tipo:** checklist | claude-md-rule
- **Fonte:** https://google.github.io/eng-practices/review/developer/small-cls.html · **Autor/Org:** Google
- **Sinais:** Verificado: cerca de 100 linhas costuma ser razoável e cerca de 1000 grande demais, a critério do revisor; arquivos espalhados contam; refatoração em CL separado de feature ou correção (pequenas limpezas locais podem ficar junto); testes na mesma mudança; empilhar CLs.
- **Conteúdo reutilizável (redação própria):** regra "refatoração pura em commit próprio, mudança de comportamento em outro; commit autocontido com testes e suíte verde; se o diff passar de aproximadamente 400 linhas ou 10 arquivos, proponha dividir" (os números do exemplo são sugestão minha, Suposição, ajustáveis).
- **Ressalvas:** os números da fonte são orientação, não regra.
- **Verificação:** página aberta.

### V-19 — Vocabulário da saída de revisão: Conventional Comments + três níveis de severidade (R-authoritative-19, R-authoritative-26, R-github-02, R-community-05) — Classe B (5/10); a parte de severidade é C (4) · Prompt-score 60 -> 80
- **Lente:** authoritative, github, community
- **Tipo:** checklist | reference
- **Fonte:** https://conventionalcomments.org/ e https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/code-review-generic.instructions.md
- **Sinais:** Conventional Comments: licença CC BY 3.0 (Verificado na página; reuso literal com atribuição). awesome-copilot: repositório MIT na página; o arquivo não traz licença, usa emojis (🔴🟡🟢) e `applyTo: '**'`.
- **Atribuição (literal permitida):** "Rótulos de Conventional Comments (https://conventionalcomments.org/, CC BY 3.0)": praise, nitpick, suggestion, issue, todo, question, thought, chore, note; extras typo, polish, quibble; decorações (non-blocking), (blocking), (if-minor); formato `rótulo (decorações): assunto`, discussão opcional.
- **Conteúdo reutilizável (redação própria):**
```text
Severidade: CRÍTICO (bloqueia: segurança, correção, quebra de API, perda de dados) | IMPORTANTE (exige discussão: qualidade, testes, desempenho, arquitetura) | SUGESTÃO (não bloqueia).
Cada achado: [SEVERIDADE] categoria: título | onde (arquivo:linha) | por que importa | correção sugerida | evidência.
PR grande: visão geral e arquitetura primeiro; depois segurança, testes, lógica, estilo.
Elogio só quando real; revisor de IA não fabrica "praise".
```
- **Ressalvas:** o arquivo do Copilot não tem seção "o que não reportar"; suprida por V-06.
- **Verificação:** as duas páginas abertas; emojis confirmados e removidos na versão própria.

### V-20 — Dívida técnica: quadrantes e priorização por frequência de mudança (R-authoritative-20) — Classe B (6/10) · n/a
- **Lente:** authoritative
- **Tipo:** reference | checklist
- **Fonte:** https://martinfowler.com/bliki/TechnicalDebt.html (21 maio 2019; publicado em 2003 e reescrito em abril de 2019) e https://martinfowler.com/bliki/TechnicalDebtQuadrant.html (2009, republicado em 2014) · **Autor/Org:** Martin Fowler
- **Verificado:** a página principal diz que se gasta mais tempo removendo "cruft" nas áreas modificadas com frequência, e que áreas feias mas estáveis podem ficar como estão; a metáfora falha porque o juro vem do uso, não do tempo. A página do quadrante define os quatro casos (prudente ou imprudente x deliberada ou inadvertida) com exemplos.
- **Correção ao pesquisador:** o pesquisador disse que o detalhe dos quadrantes não estava lido; o validador leu a página do quadrante.
- **Conteúdo reutilizável (redação própria):** tabela dos quatro quadrantes e regra "ordene a limpeza por (frequência de alteração x dor ao mexer); código estável e feio entra no fim da fila". Para o agente: classificar cada item de dívida e exigir dono e prazo para a dívida deliberada.
- **Ressalvas:** copyright do site, sem licença: só destilação.
- **Verificação:** duas páginas abertas.

### V-21 — Strangler Fig: substituição incremental (R-authoritative-21) — Classe B (5/10) · n/a
- **Lente:** authoritative
- **Tipo:** pattern | checklist
- **Fonte:** https://martinfowler.com/bliki/StranglerFigApplication.html (22 agosto 2024) · **Autor/Org:** Martin Fowler
- **Verificado:** quatro atividades sem ordem fixa: entender os resultados desejados, decidir como quebrar o problema, entregar as partes com sucesso, mudar a organização. **Correção:** a página atribui essas quatro atividades a Ian Cartwright, Rob Horn e James Lewis; o pesquisador as colocou como de Fowler.
- **Conteúdo reutilizável (redação própria):** quando usar (reescrita total é arriscada e remendar é caro) e a lista de atividades como checklist de plano; código de transição temporário deve ter data de remoção.
- **Verificação:** página aberta.

### V-22 — Catálogo de refatorações como vocabulário (R-authoritative-22) — Classe B (6/10) · n/a
- **Lente:** authoritative
- **Tipo:** reference | checklist
- **Fonte:** https://refactoring.com/catalog/ · **Autor/Org:** Martin Fowler
- **Verificado:** os 16 nomes citados pelo pesquisador existem no catálogo (Extract Function, Inline Function, Extract Variable, Split Loop, Remove Dead Code, Move Function, Extract Class, Hide Delegate, Encapsulate Variable, Replace Primitive with Object, Decompose Conditional, Replace Nested Conditional with Guard Clauses, Replace Conditional with Polymorphism, Remove Flag Argument, Change Function Declaration, Introduce Parameter Object). A página `extractFunction.html` mostra exemplo antes e depois, mas não lista a mecânica passo a passo nem diz "teste após cada passo".
- **Conteúdo reutilizável (redação própria):** "Cite o nome da refatoração; faça o menor passo possível; rode o teste após cada passo; se o teste quebrar, desfaça o passo". O passo a passo é do validador (Inferido da prática), não da página.
- **Ressalvas:** os nomes são vocabulário; a descrição detalhada está no livro (não lido). Licença não verificada: não copiar texto.
- **Verificação:** catálogo e uma página de detalhe abertos.

### V-23 — Evidência executável para afirmações de agente e validação de achados de IA (R-authoritative-23, R-community-12) — Classe B (5/10) · Prompt-score 74
- **Lente:** authoritative, community
- **Tipo:** anti-pattern | checklist
- **Fonte:** https://danluu.com/ai-coding/ (título real: "Agentic test processes, LLM benchmarks, and other notes on agentic coding from Galapagos Island") · **Autor/Org:** Dan Luu
- **Sinais:** sem data explícita; cita atualização de setembro de 2026 (Verificado). Texto longo (110.862 caracteres; os primeiros 100.000 lidos).
- **Verificado (relato anedótico do autor):** agentes erram a origem de um bug cerca de metade das vezes quando não executam código, e exigir execução eliminou a maioria dos erros; o autor vê fuzzing "geralmente ganhar" em latência, bugs achados e falsos positivos; regra de violação de "uma por 100 dias-agente" é inaceitável sem revisão em escala; um agente produziu um vídeo de reprodução convincente de ambiente artificial e alegou falta de permissão falsamente; testes gerados por LLM são "entre inúteis e marginalmente úteis" por padrão.
- **Não confirmado:** a afirmação de R-community-12 de que testes automatizados fortes substituem boa parte da revisão humana (parte final do texto não lida).
- **Conteúdo reutilizável (redação própria):**
```text
Toda hipótese de causa vem com o comando que a confirma ou refuta, e a saída dele.
Todo achado de IA sem reprodução executável é uma hipótese, não um defeito.
Reprodução entregue pelo agente é conferida: o ambiente é o real? o artefato existe?
Prefira fuzzing e testes de propriedade a pedir ao modelo que "ache bugs".
```
- **Ressalvas:** opinião de autor com contexto específico (hardware); sem medição formal.
- **Verificação:** cinco afirmações do pesquisador conferidas; uma não confirmada.

### V-24 — Revisão de código gerado por IA em três camadas e marca de edição humana (R-authoritative-24, R-github-15, R-community-11) — Classe C (4/10; rebaixado de B) · Prompt-score 66 -> 76
- **Lente:** authoritative, github, community
- **Tipo:** checklist | pattern
- **Fonte:** https://www.sanity.io/blog/first-attempt-will-be-95-garbage · **Autor/Org:** Vincent Quigley (Sanity), publicado em 2025-09-02 (Verificado)
- **Verificado:** três camadas (revisão pela IA, revisão do engenheiro, revisão normal da equipe); marcar código editado por humano; arquivo de contexto com decisões, padrões e armadilhas; cerca de três tentativas até algo utilizável; "nunca paralelizar o mesmo espaço de problema". Pontuação: autoridade 2, evidência 0, atualidade 1 (13 meses), comunidade 0, licença 0.
- **Conteúdo reutilizável (redação própria):** quem pega o quê: IA = lacunas de teste e bugs óbvios; autor = manutenibilidade, arquitetura, regra de negócio; time = padrão normal. Quem envia responde pelo que entrega. Anotar no PR o que foi gerado por IA e o que foi editado por humano.
- **Ressalvas:** os percentuais do título são retórica do autor.
- **Verificação:** artigo lido.

### V-25 — Fluxo pesquisa -> plano anotado -> execução mecânica (R-authoritative-25, R-github-14, R-community-10) — Classe C (4/10) · Prompt-score 70 -> 76
- **Lente:** authoritative, github, community
- **Tipo:** workflow
- **Fonte:** https://boristane.com/blog/how-i-use-claude-code/ · **Autor/Org:** Boris Tane, 2026-02-10 (Verificado)
- **Verificado:** `research.md`, `plan.md`, ciclo de anotação de 1 a 6 vezes com a trava "não implemente ainda", lista de tarefas marcada no documento, typecheck contínuo, reverter e reduzir escopo quando a direção está errada. As três lentes divergiam (C, C, B); harmonizado em C.
- **Conteúdo reutilizável (redação própria):**
```text
Fase 1: estude {{área}} e grave research.md com o que encontrou. Não planeje.
Fase 2: escreva plan.md com abordagem, arquivos afetados, trade-offs e tarefas por fase. Não implemente.
Fase 3 (repetir): eu anoto plan.md; revise conforme as anotações. Não implemente.
Fase 4: execute o plano, marque as tarefas e rode o typecheck/testes a cada bloco. Se a direção estiver errada, reverta e reduza o escopo.
```
- **Ressalvas:** relato pessoal. Só para mudanças que passam de uma frase (a doc oficial pede pular o plano nas pequenas, V-01).
- **Verificação:** post lido.

### V-26 — Regras curtas de CLAUDE.md para qualidade (Sanglard) (R-authoritative-29, R-github-16, R-community-13) — Classe C (4/10) · Prompt-score 66 -> 76
- **Lente:** authoritative, github, community
- **Tipo:** claude-md-rule
- **Fonte:** https://fabiensanglard.net/agent.md/index.html · **Autor/Org:** Fabien Sanglard, 2026-08-21 (Verificado)
- **Verificado:** bug começa por teste que falha; uma sessão por feature; pedir ao agente que recarregue o arquivo de regras; agente mantém o arquivo; mudança mínima; aprovação antes de ampliar visibilidade de API; regras de estilo (enum em vez de booleano, retorno antecipado, constantes nomeadas). O autor diz que isso não substitui revisão.
- **Conteúdo reutilizável (redação própria):**
```markdown
## Qualidade de código
- Bug: escreva um teste que falha, veja-o falhar, corrija, veja-o passar.
- Mudança mínima: não toque em código sem relação com a tarefa.
- Não amplie a visibilidade de uma API (private -> public) sem aprovação.
- Uma sessão por feature. Se a qualidade cair, releia este arquivo.
```
- **Ressalvas:** as regras de estilo (enum, tamanho de função, chaves em todo `if`) são opinião da casa e ficam fora; só as três regras acima entram. A regra do teste primeiro duplica V-04.
- **Verificação:** página lida.

### V-27 — Revisão de PR em CI com `claude-code-action` (R-authoritative-11, R-github-10, R-community-18) — Classe A (9/10) · Prompt-score 78 -> 80
- **Lente:** authoritative, github, community
- **Tipo:** workflow (referência, não ativo)
- **Fonte:** https://github.com/anthropics/claude-code-action (e `docs/solutions.md`) · **Autor/Org:** Anthropic
- **Sinais:** Verificado: 9,5 mil estrelas, 2,2 mil forks, MIT, 818 commits, commit em 2026-10-09; a página diz "updating your workflows to v1.0" e liga um guia de migração de v0.x.
- **Verificado em `docs/solutions.md` (arquivo bruto):** gatilho `pull_request` com tipos `opened` e `synchronize`; `permissions`: `contents: read`, `pull-requests: write`, `id-token: write`; `uses: anthropics/claude-code-action@v1`; entradas `anthropic_api_key` (de secret), `prompt` e `claude_args` (restringe a ferramenta de comentário inline e `gh pr comment/diff/view`).
- **Correções ao pesquisador:** (1) R-github-10 propôs `issues: write` como Inferido; o exemplo oficial não o usa. (2) R-authoritative-11 dizia não ter confirmado "modos tag e agent"; a página descreve detecção automática do modo pelo contexto do workflow, e a menção `@claude` como um dos gatilhos.
- **Conteúdo reutilizável (esboço do validador baseado em solutions.md, a reconferir antes de publicar):**
```yaml
on:
  pull_request:
    types: [opened, synchronize]
permissions:
  contents: read
  pull-requests: write
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4   # versão a confirmar
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Revise este PR contra o checklist de qualidade; reporte só achados de alto sinal, com arquivo:linha e evidência."
```
- **Ressalvas:** vai em `references/`, não ativo. A chave de API vem de secret, nunca no código. PRs de forks e entrada não confiável exigem permissões mínimas; `id-token: write` só se houver OIDC (Inferido). O plugin não cria workflow sem pedido do usuário.
- **Verificação:** página do repositório, arquivo `docs/solutions.md` bruto e feed de commits.

### V-28 — Skill de refatoração React `composition-patterns` (R-authoritative-16, R-github-08, R-community-15) — Classe A (8/10, para React) · Prompt-score n/a
- **Lente:** authoritative, github, community
- **Tipo:** skill (referência opcional de stack)
- **Fonte:** https://github.com/vercel-labs/agent-skills (skill `composition-patterns`; arquivo bruto `skills/composition-patterns/SKILL.md`) · **Autor/Org:** Vercel
- **Sinais:** Verificado: 32,1 mil estrelas, 2,8 mil forks, MIT, 275 commits, último commit em 2026-08-28; o frontmatter do SKILL traz `name: vercel-composition-patterns`, licença MIT e autor `vercel`; regras em quatro faixas de prioridade (arquitetura, estado, padrões de implementação, APIs do React 19), cada uma com arquivo próprio com exemplos incorreto e correto.
- **Conteúdo reutilizável:** a ideia de ordenar regras por impacto e o formato "regra com exemplo ruim e bom". Os 4 passos de "caracterização antes de extrair variantes" de R-community-15 são composição do pesquisador, não da skill (Inferido).
- **Ressalvas:** específico de React e Next.js; fora do núcleo genérico. Recomendar como pacote opcional.
- **Verificação:** SKILL.md aberto; repositório e feed.

### V-29 — Regras anti-alucinação por versão de biblioteca (R-github-17, R-community-16) — Classe C (4/10) · Prompt-score 70 -> 74
- **Lente:** github, community
- **Tipo:** claude-md-rule
- **Fonte:** https://github.com/PatrickJS/awesome-cursorrules · **Autor/Org:** PatrickJS e colaboradores
- **Sinais:** Verificado: 40,9 mil estrelas, CC0-1.0, último commit em 2026-05-30; entradas `nestjs-anti-hallucination`, `anti-sycophancy-code-discipline` (17 diretivas segundo a listagem) e Next.js 15. Os arquivos `.mdc` não foram abertos: o conteúdo é Não verificado.
- **Conteúdo reutilizável (redação própria):**
```markdown
- Antes de usar uma API de biblioteca, confirme o nome e a assinatura na versão do projeto (lockfile ou manifesto).
- Se não conseguir confirmar, escreva "não verificado" em vez de inventar.
- Nunca diga que testes passaram sem mostrar a saída.
```
- **Ressalvas:** repositório de regras do Cursor, qualidade desigual. Só a ideia.
- **Verificação:** página do repositório e listagem; feed de commits.

### V-30 — Auditoria de testes que custam mais do que protegem; modo somente relatório (R-github-09, R-community-01) — Classe C (4/10) · Prompt-score 72 -> 78
- **Lente:** github, community
- **Tipo:** checklist | pattern
- **Fonte:** https://github.com/garrytan/gstack (README) · **Autor/Org:** Garry Tan (conforme a página)
- **Sinais:** MIT, commit em 2026-10-09 (Verificado). Segurança: ver aviso 3; nada deve ser instalado ou copiado.
- **Verificado no README:** `/test-audit` procura testes que custam mais do que protegem (grep em fonte, duplicatas, sondas sem asserção, exports só de teste), com cartão de evidência por item, e só relata sem aprovação; `/investigate` para após 3 correções falhas e trava edição do módulo; `/qa` exige teste de regressão que falha antes da correção; `/deslop-shared-libs` só recomenda até três extrações.
- **Conteúdo reutilizável (redação própria):** critérios de auditoria de testes: (1) testa o código-fonte em vez do comportamento; (2) duplica outro teste; (3) executa sem asserção; (4) depende de export criado só para o teste; (5) mock confirma a chamada e não o efeito. Saída: relatório com evidência; nenhuma remoção sem aprovação.
- **Ressalvas:** em agente somente leitura, "AUTO-FIX" vira "ASK" (proposta). O final do README (100.000 de 109.820 caracteres) não foi lido pelos pesquisadores.
- **Verificação:** README bruto aberto.

### V-31 — Reflexion: reflexão verbal guiada por feedback externo (R-github-19, R-community-24) — Classe C (4/10, rebaixado de B) · n/a
- **Lente:** github, community
- **Tipo:** pattern
- **Fonte:** https://arxiv.org/abs/2303.11366 · **Autor/Org:** Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao
- **Verificado:** submetido em 2023-03-20, v4 em 2023-10-10; resumo afirma pass@1 de 91% no HumanEval (contra 80% do GPT-4, segundo o resumo); reflexões em memória episódica, sem atualizar pesos. Atualidade 0 (3 anos); citações e licença: Não verificado. Benchmark de geração de código, não de refatoração.
- **Conteúdo reutilizável (redação própria):** em cada tentativa de correção, registre o sinal externo (teste passou ou falhou), escreva uma frase do que a falha ensinou e use-a na próxima tentativa, com limite de tentativas (V-04). "Autoavaliação sem teste não vale" é Inferido (não é afirmação do artigo).
- **Verificação:** página arXiv aberta.

### V-32 — Descoberta de convenções do código antes de refatorar (R-github-18, R-community-14) — Classe B (5/10) · Prompt-score 70 -> 78
- **Lente:** github, community
- **Tipo:** workflow | prompt
- **Fonte:** https://github.com/buildermethods/agent-os · **Autor/Org:** Brian Casel (Builder Methods)
- **Sinais:** Verificado: 5,5 mil estrelas, 828 forks, MIT, commit em 2026-10-07; recursos listados: descobrir, aplicar e indexar standards. O mecanismo de descoberta e os comandos não foram abertos (Não verificado); a instalação passa pelo site externo.
- **Conteúdo reutilizável (redação própria):**
```text
Analise {{pasta}} sem alterar código. Liste as convenções observadas (nomes, estrutura de pastas, tratamento de erro, testes). Para cada uma: um arquivo de exemplo; Verificado se aparece em 3 ou mais lugares, Inferido se em 1 ou 2. Grave o resultado em um arquivo de padrões. Não proponha mudanças.
```
- **Ressalvas:** não instalar o agent-os; só o prompt.
- **Verificação:** página do repositório e feed.

### V-33 — Base própria: revalidação em cinco passos e evidência com quatro rótulos (R-github-20) — Classe: base própria (MIT por plano do projeto) · Prompt-score 86
- **Lente:** github
- **Tipo:** checklist
- **Fonte:** `docs/foundation/brain-of-agent-snapshot/brains/fullstack/references/testes-e-debugging.md` (4.155 bytes, lido localmente) · **Fonte consultada nele:** 2026-10-09
- **Verificado:** investigação reproduzível (esperado, observado, build, ambiente, passos mínimos, hipótese refutável); exemplo de mock que confirma a chamada mas não detecta duplicidade; oráculo calculado pela mesma função sob teste; espera por condição em vez de sleep; retry que esconde falha deve ficar visível; revalidação em cinco passos (reprodução original, casos adjacentes, tipos/lint/build/testes afetados, jornada real, conferir o diff final e o artefato testado); checklist com "evidência distingue executado, revisado, inferido e bloqueado".
- **Conteúdo reutilizável:** usar o checklist de nove itens como base do critério de saída das skills `debug-causa-raiz` e `review`.
- **Ressalvas:** base própria, não substitui fonte externa para afirmações gerais. A citação do Playwright dentro do arquivo não foi re-aberta.
- **Verificação:** arquivo lido por inteiro.

### V-34 — Formato de regras de revisão em AGENTS.md (R-community-23) — Classe B (5/10) · Prompt-score 76
- **Lente:** community
- **Tipo:** claude-md-rule (contraste de outro fornecedor)
- **Fonte:** https://learn.chatgpt.com/docs/agent-configuration/agents-md · **Autor/Org:** OpenAI (documentação do Codex; página "Custom instructions with AGENTS.md")
- **Verificado:** seção `Code Review Rules` com uma bullet do que sinalizar e uma linha indentada com o caminho seguro; a página recomenda declarar exceções, mas o exemplo não mostra uma. O exemplo original é de experimentos, não de código geral. Linter e formatação ficam no CI.
- **Conteúdo reutilizável (redação própria):**
```markdown
## Code Review Rules
- Sinalize: {{comportamento que quebra a regra}}.
  Caminho seguro: {{como fazer certo}}. Exceção: {{quando é aceitável}}.
```
- **Ressalvas:** nada a copiar da fonte; apenas o formato.
- **Verificação:** página aberta.

### V-35 — Sinais do Hacker News sobre revisão por IA (R-community-19) — Classe C (4/10) · n/a
- **Lente:** community
- **Tipo:** pattern | anti-pattern (sinal)
- **Fonte:** itens HN 49992857, 48963926, 49293760, 48863990 (https://news.ycombinator.com/item?id=<id>) e API `hn.algolia.com/api/v1/items/<id>`
- **Verificado (os quatro são comentários, datas 2026-07-10 a 2026-10-07; pontos: Não verificável):** (a) um mantenedor lê todo PR e usa Claude Code e Codex como revisão adversarial (49992857); (b) `/code-review` do Claude Code usa vários subagentes, gasta muitos tokens e cobre bem; o autor montou uma skill com 4 a 5 agentes no Codex (48963926); (c) copiar saída de um Claude para outro Claude aproxima de colapso de modelo, e subagente que só resume saída de LLM é visto com ceticismo (49293760); (d) revisão por um LLM de outro fornecedor acha problemas, mas o diff ainda precisa de olhos humanos (48863990). Os demais itens citados pelo pesquisador (49293760 está confirmado; 48510668, 48458603, 48296378, 47936868) não foram reabertos.
- **Conteúdo reutilizável:** armadilhas: revisor que só resume outro modelo; custo de tokens de muitos subagentes; ausência de leitura humana do diff.
- **Ressalvas:** conversas curtas e anedóticas; sinal, não prova.
- **Verificação:** quatro comentários abertos pela API.

### V-36 — Rede de segurança antes de refatorar: testes de caracterização e código autotestável (NOVO; fecha lacuna declarada) — Classe B (5/10) · Prompt-score 80
- **Lente:** validador (fecha lacuna das três lentes)
- **Tipo:** workflow | checklist
- **Fonte:** https://michaelfeathers.silvrback.com/characterization-testing (Michael Feathers, "Characterization Testing", 2016-08-08) e https://martinfowler.com/bliki/SelfTestingCode.html (Martin Fowler, 2014-05-01; versão menor de 2005) · **Autor/Org:** autores reconhecidos
- **Sinais:** Verificado nas duas páginas. Pontuação: autoridade 2, evidência 1, atualidade 1 (atemporal), comunidade 1, licença 0. O livro "Working Effectively with Legacy Code" não foi lido.
- **Verificado:** teste de caracterização registra o que o código faz de fato, não o que deveria fazer; procedimento: escrever um teste com valor esperado fictício, rodar, copiar a saída real para o teste, renomear com o que aprendeu. Fowler: código autotestável dá a confiança para mudar o sistema; sem testes, os desenvolvedores evitam refatorar e a dívida cresce.
- **Conteúdo reutilizável (redação própria):**
```markdown
Antes de refatorar código sem teste:
1. Escolha o trecho e as entradas relevantes (inclua bordas e casos de erro).
2. Escreva um teste por entrada com expectativa provisória, rode, e fixe a saída real como expectativa. Nomeie o teste pelo comportamento observado.
3. Marque no teste as saídas que parecem bug ("comportamento atual, possível defeito") e não as corrija nesta mudança.
4. Refatore em passos pequenos; rode os testes a cada passo.
5. Ao terminar, mantenha os testes que protegem regra de negócio; remova os que só prendem detalhe de implementação.
```
- **Ressalvas:** teste de caracterização trava também os bugs; o relatório deve listá-los como follow-up. Não substitui a especificação.
- **Verificação:** as duas páginas abertas.

### V-37 — Parallel Change (expandir, migrar, contrair) para mudar API e dependência com segurança (NOVO) — Classe B (5/10) · n/a
- **Lente:** validador
- **Tipo:** pattern
- **Fonte:** https://martinfowler.com/bliki/ParallelChange.html (Danilo Sato, 2014-05-13) · **Autor/Org:** Martin Fowler's bliki
- **Verificado:** três fases: expandir (nova versão ao lado da antiga), migrar (clientes aos poucos) e contrair (remover a antiga); aplica-se a mudança de assinatura, esquema de banco, APIs remotas e flags; risco de nunca contrair e piorar o código.
- **Conteúdo reutilizável (redação própria):** checklist para trocar uma função pública ou atualizar uma dependência com API quebrada: criar a nova ao lado; migrar chamadas em commits pequenos; remover a antiga só quando a busca não achar usos e a suíte passar; registrar a data prevista da contração.
- **Verificação:** página aberta.

### V-38 — Revisão de segurança como dimensão do review: OWASP Secure Code Review (NOVO) — Classe B (6/10) · n/a
- **Lente:** validador
- **Tipo:** checklist | reference
- **Fonte:** https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html · **Autor/Org:** OWASP Cheat Sheet Series
- **Verificado:** seções de metodologia (revisão de linha de base versus revisão por diff), padrões comuns (validação de entrada, injeção, autenticação e sessão, controle de acesso, desserialização, criptografia), técnicas (análise de fluxo de dados, revisão por ameaça), checklists e integração no SDLC; licença CC BY-SA 4.0 (reuso literal exigiria compartilhar sob a mesma licença, então destilar).
- **Conteúdo reutilizável (redação própria):** no `review`, uma passada de segurança por diff: para cada entrada externa no diff, siga até o uso (consulta, comando, caminho, HTML) e confira validação, autorização e segredos; achados de segurança entram com evidência e severidade.
- **Verificação:** página aberta; data da página: Não verificável.

### V-39 — Análise estática no fluxo: correções seguras do linter e plataforma de análise (NOVO; cobertura parcial da lacuna) — Classe B (5/10) · Prompt-score 70 -> 76
- **Lente:** validador
- **Tipo:** reference | checklist
- **Fonte:** https://docs.astral.sh/ruff/linter/ (documentação oficial do Ruff), https://research.google/pubs/tricorder-building-a-program-analysis-ecosystem/ (Tricorder, ICSE 2015) e https://www.sonarsource.com/resources/cognitive-complexity/ (apenas existência)
- **Verificado:** Ruff: seleção de regras com `select`, `ignore`, `extend-select`; `ruff check --fix` aplica só correções seguras; correções inseguras (que podem mudar comportamento ou remover comentários) exigem opt-in; `noqa` com códigos; RUF100 acha supressões inúteis. Tricorder: página do artigo confirma a plataforma de análise (Sadowski, van Gogh, Jaspan, Soederberg, Winter) mas NÃO lista os princípios (falso positivo baixo, botão "não útil" ficam Não verificados). Sonar Cognitive Complexity (G. Ann Campbell, 2021-04-05): página de entrada com download protegido e "All rights reserved"; regras de pontuação não lidas.
- **Conteúdo reutilizável (redação própria):**
```markdown
Análise estática:
- Rode o linter e o typechecker do projeto antes do review; o que eles pegam não entra no relatório do agente.
- Aplique só correções automáticas seguras. Correção "insegura" exige teste antes e depois e aprovação.
- Não suprima aviso (noqa, ts-ignore) para fazer passar; justifique ou corrija.
- Métrica de complexidade serve para escolher onde olhar, não como meta. Cite a ferramenta e a versão.
```
- **Ressalvas:** nenhuma fonte oficial por linguagem para ESLint, Sonar (regras) ou métricas de manutenibilidade foi lida; lacuna parcial mantida.
- **Verificação:** três páginas abertas.

### V-40 — Upgrades de dependência e framework: receitas determinísticas e atualizações automáticas (NOVO; cobertura parcial da lacuna) — Classe B (5/10) · n/a
- **Lente:** validador
- **Tipo:** reference
- **Fonte:** https://docs.openrewrite.org/ (OpenRewrite by Moderne) e https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates
- **Verificado:** OpenRewrite é um ecossistema open source de refatoração automatizada com receitas para migração de framework, correções de segurança e estilo, via plugins Gradle e Maven, começando por Java; a página não declara a licença (Não verificado). Dependabot version updates abre PRs de atualização com um `dependabot.yml`; espera 3 dias após uma release por padrão (não vale para correções de segurança).
- **Conteúdo reutilizável (redação própria):** para upgrade, prefira receita determinística ou codemod quando existir; use o agente para o que sobra; rode a suíte antes e depois; em lotes pequenos; combine com V-14 (juiz) e V-37 (parallel change). Leia o guia oficial de migração da versão antes de agir (Não verificado: nenhum guia por framework foi lido).
- **Ressalvas:** licença do OpenRewrite não verificada; não instalar plugins sem pedido do usuário.
- **Verificação:** duas páginas abertas.

---

## Rejeitados e rebaixados

| Item | Decisão | Motivo (verificado) |
| --- | --- | --- |
| R-authoritative-28 (VoltAgent), R-community-17, R-github-06 | Rejeitados como itens | Índices de coletânea sem conteúdo lido; o `code-reviewer.md` concede `Read, Write, Edit, Bash, Glob, Grep` (viola menor privilégio), é genérico, depende de "context manager" inexistente e traz métricas de exemplo fabricadas. A afirmação "revisores são somente leitura" é falsa para esse arquivo. `refactoring-specialist.md` menciona testes de caracterização, mas com as mesmas ferramentas amplas e métricas de exemplo. Só os nomes de papéis foram aproveitados (V-09). Contagem divergente na página ("mais de 100" versus "161+") |
| R-github-09, R-community-01 (gstack) | Rebaixados a ideia (C), instalação proibida | Instalação executa `./setup`, baixa Chromium, edita CLAUDE.md, registra hooks (inclui Stop ligado por padrão), auto-update silencioso e telemetria opcional (aviso 3) |
| R-authoritative-08, R-community-07 | Rebaixados de A para B | Licença proprietária no repositório de origem; nota 0–100 é autoavaliação; sem `tools` |
| R-authoritative-09 | Rebaixado de A para B | README diz MIT mas o repositório é "All rights reserved" |
| R-github-04, R-community-08, R-authoritative-10 | Harmonizados em B (7) | Classes divergentes (A, B, A); licença por plugin não verificada; regras de React e TS removidas |
| R-authoritative-24, R-github-15, R-community-11 (Sanity) | Rebaixados de B para C | Evidência e comunidade nulas; atualidade de 13 meses; percentuais retóricos |
| R-community-10, R-authoritative-25, R-github-14 (Tane) | Harmonizados em C | Relato pessoal sem avaliação |
| R-community-13, R-authoritative-29, R-github-16 (Sanglard) | Rebaixados para C; regras de estilo rejeitadas | enum em vez de booleano, tamanho de função e chaves obrigatórias são opinião da casa |
| R-community-05, R-authoritative-26, R-github-02 | Harmonizados em C para a parte de severidade | Sem licença no arquivo; emojis; genérico; Conventional Comments é B por CC BY 3.0 |
| R-community-16, R-github-17 | C | Conteúdo dos `.mdc` não aberto |
| R-github-19, R-community-24 (Reflexion) | Rebaixados de B para C | 3 anos; benchmark de geração, não de refatoração; citações e licença não verificadas |
| R-community-19 (HN) | Mantido como C | Comentários anedóticos; pontos não verificáveis; 4 de 8 itens re-abertos |
| R-github-05 versus atlas e README do plugin | Correção | Arquivo atual usa filtro binário e validação por achado; o README do plugin ainda diz 0–100 com limiar 80 e um agente de git blame |
| R-github-10 | Correção | `issues: write` era Inferido e não está no exemplo oficial; permissões reais: `contents: read`, `pull-requests: write`, `id-token: write` |
| R-authoritative-11 | Correção | Modos "tag" e "agent" não confirmados; a página descreve detecção por contexto e menção `@claude` |
| R-authoritative-06 | Correção | O aviso de inicialização é pela soma das descrições (acima de 15.000 tokens), não por uma descrição longa |
| R-authoritative-20 | Complementado | Página do quadrante lida (2009, republicada em 2014) |
| R-authoritative-21 | Correção | Quatro atividades são de Cartwright, Horn e Lewis, citadas por Fowler |
| R-authoritative-22 | Limitado | Só os nomes foram verificados; a mecânica por passos não está na página |
| R-community-12 | Parcialmente não confirmado | Afirmação de que testes substituem revisão humana não encontrada na parte lida |
| R-community-15 | Esclarecido | Os 4 passos de caracterização são composição do pesquisador, não da skill |
| R-github-01 e R-community-02 (classe B provisória) | Elevados | Estrelas, licença e atividade verificadas; classe A (8) |
| Classe "A por regra de fonte" dos pesquisadores | Recalculada | A rubrica de fonte (0–10) foi reaplicada; o status oficial não basta sem licença e atualidade |

Nenhum item continha instrução dirigida à IA em texto de página (injeção) nem link encurtado. Cuidado de segurança relevante: instaladores de gstack e agent-os e hooks do code-modernization (avisos 3 e 4).

---

## Mapa de cobertura do escopo

| Subtema | Itens validados | Cobertura |
| --- | --- | --- |
| Code review de PR (severidade, confiança, falsos positivos) | V-02, V-06, V-07, V-08, V-17, V-19, V-24, V-27, V-38 | Boa |
| Clean code e legibilidade | V-12, V-17, V-22, V-26 | Parcial: sem fonte do livro "Clean Code" nem guia de estilo por linguagem |
| Refatoração segura | V-03, V-18, V-22, V-36, V-37 | Boa (lacuna de testes de caracterização fechada) |
| Dívida técnica | V-20, V-21, V-30 | Parcial: sem método de auditoria ou métrica de priorização além de Fowler |
| Debugging sistemático | V-04, V-05, V-23, V-31, V-33 | Boa |
| Compreensão de base de código | V-03, V-32 | Parcial |
| Modernização de legado e migração | V-14, V-15, V-21, V-37 | Boa |
| Upgrades de framework e dependência | V-37, V-40, V-14 | Fraca a parcial: nenhum guia oficial por framework |
| Análise estática e métricas | V-39 | Fraca a parcial: só Ruff, Tricorder (resumo) e Sonar (existência) |
| Simplificação | V-12, V-13 | Boa |
| Comunicação dos achados | V-19, V-17 | Boa |
| Escopo, verificação, planejamento de sessão | V-01, V-10, V-11, V-25, V-26 | Boa |
| Subagentes e permissões | V-09, V-05 | Boa |
| Segurança em revisão | V-38, V-06 | Parcial |
| CI | V-27 | Parcial |
| Comunidade (Reddit, X, YouTube, dev.to, Medium, newsletters) | V-35 (só HN) | Lacuna |

---

## Lacunas para o plugin

1. Comunidade: nenhuma fonte de Reddit (bloqueado no WebFetch), X, YouTube, dev.to, Medium ou newsletter; só 4 comentários do HN. Pesquisável quando o WebSearch for reaberto: threads de r/ClaudeCode e r/ClaudeAI sobre "code review subagent", "CLAUDE.md refactoring rules", "debugging loop".
2. Upgrades de framework e dependência: nenhum guia oficial de migração por framework lido (por exemplo guias de upgrade de React, Angular, Rails, Django, Spring) nem fonte sobre OpenRewrite com licença verificada. Pesquisável: guias oficiais de upgrade e a página "Licensing" do OpenRewrite.
3. Análise estática e métricas: faltam ESLint, SonarQube (regras de complexidade cognitiva, hoje atrás de formulário), Semgrep, mypy, e os princípios do Tricorder (o artigo completo). Pesquisável: documentação oficial de ESLint e do paper completo do Tricorder.
4. Clean code e legibilidade por linguagem: nenhuma fonte primária de guia de estilo (Google style guides, PEP 8, Effective Go, Rust API guidelines).
5. Dívida técnica: sem método de auditoria ou priorização quantitativa.
6. Avaliação do prompt: nenhum item traz eval próprio; as afirmações "reduziu extras sem mudar sucesso" (V-10) e "validado em equipes internas" (V-01) são da fonte. O construtor deve medir com evals do plugin.
7. Datas de publicação das páginas vivas da Anthropic (best-practices, common-workflows, sub-agents, prompting): Não verificável.
8. Estrelas e licença via API do GitHub: limite de taxa; foram obtidas pelas páginas HTML. A licença de `plugins/*` em `claude-plugins-official` não foi lida arquivo a arquivo.
9. Conteúdo não lido: `.mdc` do awesome-cursorrules; comandos do agent-os; final do README do gstack e do post do Dan Luu; arquivos `refactoring-specialist` e `legacy-modernizer` só em parte.

---

## Recomendações ao construtor

| Artefato | Base (V-xx) | Observações |
| --- | --- | --- |
| Skill `debug-causa-raiz` | V-04, V-05, V-23, V-31, V-33 | Núcleo. Quatro fases, parada em 3, teste antes da correção; PT-BR e EN nos gatilhos; sem CAPS. |
| Skill `review` (comando `/review`) | V-06, V-07, V-02, V-19, V-38, V-39 | Somente leitura por padrão; validação por achado; filtro de alto sinal; saída em tabela com severidade e evidência; postar no GitHub só com pedido explícito; avisar que a skill nativa `/code-review` existe. |
| Subagente `code-reviewer` | V-09, V-07 | `tools: Read, Grep, Glob`; o comando coleta o diff e o passa no prompt. |
| Subagente `debugger` | V-05 | Declarar `tools`; patch como diff, sem Edit por padrão. |
| Skill `simplify` | V-12, V-13, V-36 | Escopo do diff; exigir teste antes (caracterização se faltar). |
| Skill `refactor-seguro` (ou subagente `refactor-safe`) | V-36, V-22, V-18, V-37, V-03 | Caracterizar -> passo pequeno -> teste a cada passo -> commit separado de comportamento. |
| Skill `migration-parity` | V-14, V-15, V-21, V-37, V-40 | Juiz primeiro, rulebook, piloto descartável, fila em disco, veredito por módulo; hooks e telemetria do code-modernization nunca embutidos. |
| Checklist `revisao-nove-dimensoes` | V-17, V-19, V-24 | Versão de agente sem estilo; humano usa a lista completa. |
| Checklist de dívida e legado | V-20, V-21, V-30 | Referência (`references/`), não comando. |
| Prompts da biblioteca | V-02 (revisão adversarial), V-25 (research -> plan), V-32 (descobrir convenções), V-13 (grill me), V-36 (caracterização), V-23 (hipótese com comando) | Variáveis `{{...}}`; rótulos Verificado, Inferido, Suposição. |
| Bloco de CLAUDE.md (curto) | V-01, V-10, V-11, V-26, V-29 | Verificação, escopo, ler antes de afirmar, bug com teste primeiro, API só na versão do projeto. Aplicar o teste de poda: cada linha precisa evitar um erro real. |
| Referência `references/` (não ativa) | V-27 (workflow de CI), V-28 (React composition), V-34 (formato AGENTS.md), V-16 | Marcar versão a confirmar; nenhum workflow ativo. |
| Não incluir | gstack e agent-os (instaladores), code-modernization (hooks e telemetria), VoltAgent (agentes com ferramentas amplas e métricas fabricadas) | Regras de segurança do plugin. |

Nota de design: o plugin deve evitar duplicar o que o Claude Code já traz (`/code-review`, `/simplify`, `/batch`, plan mode). O valor está nos critérios de saída, no filtro de falsos positivos, no protocolo de debugging, na rede de segurança antes de refatorar e nos rótulos de evidência.
