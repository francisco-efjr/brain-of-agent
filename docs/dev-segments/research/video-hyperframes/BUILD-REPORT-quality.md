# BUILD-REPORT de qualidade de prompt e conteúdo: video-hyperframes

Data: 2026-10-14. Papel: validador independente de qualidade de prompt e de conteúdo técnico (contexto de validação de prompt). Modelo: claude-opus-5-5. Os construtores eram Sonnet e o crítico do desenho era Opus. **Esta revisão é da mesma família de modelos (Claude) que escreveu e criticou o plugin**, então a independência é parcial: as notas abaixo são leitura adversarial, não medição. Nenhum eval foi executado.

Escopo lido: README, `plugin.json`, playbook e as 10 referências, 8 skills de tarefa e as 4 referências delas, os templates TP-01 a TP-10 (o TP-06 por inteiro, os demais por amostra e `Grep`), os 5 agentes, a skill `prompts` e os 3 arquivos da biblioteca (VP-01 a VP-32) e os 10 evals com o README deles. Base: `prompt-quality-rubric.md`, `prompt-principles.md`, `plugin-blueprint.md`, `house-style.md`, `SYNTHESIS.md` (com a revisão do crítico), `BUILD-REPORT-structural.md` e `VALIDATED.md`. As afirmações de segurança e toolchain foram conferidas **por leitura** no clone de `heygen-com/hyperframes` no commit `bf4cf860fbd26a7d51938c5f11987c335d4e848a` (`git rev-parse HEAD` conferido). Nada do HyperFrames foi executado.

## 1. Resumo

- Média antes: **85,3** (30 artefatos pontuados). Média depois: **87,8**. Mínimo depois: **83** (VP-01). Abaixo de 80 antes: **VP-16 (76)**. Abaixo de 80 depois: nenhum.
- Nenhum critério de reprovação automática foi encontrado: nada inventa execução, nada autoriza ação externa sem confirmação, conteúdo externo é tratado como dado em todos os artefatos, não há cópia literal sem licença, o frontmatter é válido e não há segredo.
- O plugin já chegou bom: o crítico do desenho tinha corrigido a arquitetura, e o construtor seguiu o desenho. O que esta revisão achou foi fidelidade técnica (uma afirmação "não verificada" que o código responde, um gotcha errado, uma contradição sobre blocos de código, uma flag inexistente, comandos PowerShell que não parseiam) e rastreabilidade (ids `V-nn` sem resolução para quem instala).
- `tools/verify_plugin.py`: `RESULT: PASS` (10 skills, 5 agentes, 10 evals, 74 arquivos). `claude plugin validate`: `✔ Validation passed`. Links relativos e `${CLAUDE_PLUGIN_ROOT}`: 0 quebrados (script próprio no scratchpad).

## 2. Notas por artefato (rubrica D1 a D12; nota = média × 20)

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 86 | 91 | Variáveis de sessão com `HYPERFRAMES_PREVIEW_HOST` ausente e o motivo; ids `V-nn`, `L`, `D`, `C` apontados para `fontes.md`; "opção B" do orquestrador explicada; gotcha 14 (porta e endereço do preview); "lacunas 1 e 6" virou L1 e L6 |
| `skills/prompts/SKILL.md` | 86 | 89 | Exemplo de entrega em `<example>` (D5); gotchas apontam para o índice de `fontes.md` |
| `skills/video-env-preflight/SKILL.md` | 85 | 90 | A `description` dizia "só em leitura", mas o passo 9 pode baixar o pacote do CLI e o invólucro cria arquivos: virou "sem instalar", e o escopo diz o efeito; contagem exata do carregador de `.env`; checagem de `HYPERFRAMES_PREVIEW_HOST`; caminho real da `.media` |
| `skills/video-toolchain-setup/SKILL.md` | 88 | 89 | Rastreabilidade dos `V-nn` |
| `skills/video-brief-interview/SKILL.md` | 86 | 88 | "estado 8" e "Rota 9" do exemplo agora dizem de qual tabela vêm; citação `init.ts:842-845` |
| `skills/video-source-script/SKILL.md` | 88 | 89 | Rastreabilidade dos `V-nn` |
| `skills/software-explainer-storyboard/SKILL.md` | 84 | 89 | Passo 10 dizia que `code-scroll` troca legibilidade por movimento; pela doc ele é um dos quatro blocos de explicação; saída do passo acrescentada |
| `skills/video-design-system/SKILL.md` | 83 | 88 | `--preset <nome>` sem aspas não parseia no PowerShell (testado): agora entre aspas; "L10" explicado |
| `skills/video-frame-review/SKILL.md` | 88 | 89 | Rastreabilidade dos `V-nn` |
| `skills/video-render-deliver/SKILL.md` | 84 | 90 | Preview: porta lida da saída (o CLI sobe a partir de 3002 se estiver ocupada); endereço `127.0.0.1` agora fundamentado no código; render com placeholders entre aspas (`--quality "<q>" --output "renders\<nome>.mp4"`, testado no parser) |
| `agents/storyboard-reviewer.md` | 90 | 90 | Sem mudança |
| `agents/frame-reviewer.md` | 89 | 89 | Sem mudança |
| `agents/composition-reviewer.md` | 89 | 89 | Sem mudança (o namespace C1 a C14 colide com os conflitos C1 a C18; documentado em `fontes.md` §11) |
| `agents/fact-privacy-checker.md` | 90 | 90 | Sem mudança |
| `agents/execution-security-auditor.md` | 87 | 90 | A5 exige o valor `1` no opt-out (o media-use só reconhece `1`) e `HYPERFRAMES_PREVIEW_HOST` ausente; A3 com a contagem exata do carregador |
| VP-01 mensagem inicial | 82 | 83 | Fonte `ORCHESTRATOR.md §7` conferida (seção "Mensagem inicial sugerida"); ids resolvíveis |
| VP-02 prompt de sistema | 83 | 86 | Servidores só em `127.0.0.1` com o motivo e a variável a não definir |
| VP-03 pedido extenso | 88 | 90 | O quadro de exemplo completo e generalizado (F05, sistema fictício de filas, só `[HEX_*]`) já existia; conferi a aritmética do prazo de leitura e os nomes de SFX (`click-soft`, `error`, `click`, `whoosh-short` existem no `manifest.json` do commit); nota acrescentada |
| VP-04 pedido curto | 83 | 84 | Ids resolvíveis |
| VP-05 bloco de limites | 82 | 86 | Item 4 diz por que não definir `HYPERFRAMES_PREVIEW_HOST` |
| VP-06 delegação | 86 | 86 | Sem mudança |
| VP-07 entrevista | 86 | 86 | Sem mudança |
| VP-08 preflight | 85 | 87 | Checagem de `HYPERFRAMES_PREVIEW_HOST` |
| VP-11 storyboard | 87 | 87 | Sem mudança |
| VP-16 cena de código | 76 | 86 | Contradição interna (`code-scroll` "troca legibilidade" e "os quatro primeiros são cavalos de trabalho"); variável `[SISTEMA]` usada e não declarada, `[TIPO_DE_BLOCO]` declarada e não usada |
| VP-20 teste de voz | 86 | 86 | Sem mudança |
| VP-21 briefing do frame-reviewer | 82 | 86 | `[CAMINHO]` sem declaração virou `[TIMELINE_JSON]` declarado |
| VP-25 gate do render | 81 | 87 | Fonte dizia "bind do CLI não verificado": agora cita `portUtils.ts`; porta lida da saída |
| VP-32 triagem L, C, P | 82 | 87 | `telemetry disable` estava em C, mas a política e o invólucro o tratam como P; `catalog --on-device` acrescentado em C; preview exposto acrescentado em P |
| Evals (10 casos e README) | 86 | 88 | Dois PASS conjuntivos demais afrouxados para "conta a favor" (`--output` no caso 5; regra do `BRIEF.md` no caso 8), o que reduz instabilidade do juiz |

Média por grupo, antes e depois: skills 85,8 → 89,2; agentes 89,0 → 89,6; prompts amostrados (14 de 32) 83,5 → 86,2; evals 86 → 88.

### 2.1 Detalhe D1 a D12 dos itens que mais mudaram

| Artefato | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | Antes → depois |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| playbook (depois) | 5 | 5 | 5 | 5 | 3 | 4 | 5 | 5 | 4 | 5 | 4 | 5 | 86 → 91 (D12 e D2 subiram: fatos do preview e ids resolvíveis) |
| video-render-deliver (depois) | 5 | 5 | 5 | 5 | 3 | 5 | 5 | 5 | 3 | 5 | 4 | 4 | 84 → 90 (D12 e D3: porta, endereço, comando que parseia) |
| video-design-system (depois) | 5 | 5 | 5 | 5 | 3 | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 83 → 88 (D3: comando que parseia; D12: lacuna explicada) |
| VP-16 (depois) | 4 | 4 | 5 | 4 | 3 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 76 → 86 (D12 e D3: contradição e variáveis) |
| evals (depois) | 5 | 4 | 4 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 86 → 88 (D7 e D11: graders menos frágeis; D3 fica em 4 porque não há grader determinístico de resultado, só `llm` e `tool_used`) |

Os demais artefatos ficaram com D5 entre 3 e 4 (poucos exemplos completos fora do VP-03, do `video-frame-review` e dos agentes) e D9 em 4 (a lista de variáveis de sessão se repete em cada skill de tarefa; mantida porque cada skill precisa funcionar carregada sozinha).

## 3. Correções factuais (conferidas no clone, commit `bf4cf860`)

| # | O plugin dizia | O código diz | Evidência | Onde foi corrigido |
| --- | --- | --- | --- | --- |
| 1 | "Preview só em 127.0.0.1 é política do plugin; o bind do CLI não foi verificado" (lacuna L21) | O servidor do preview escuta em `127.0.0.1` por padrão; `HYPERFRAMES_PREVIEW_HOST` troca o endereço; o comentário de segurança do código diz que a API do Studio lê, grava e apaga arquivos do projeto e dispara render sem autenticação | `packages/cli/src/server/portUtils.ts:441-447` | playbook, `seguranca-e-privacidade` (P, matriz de egresso, variáveis, gotcha), `toolchain-windows`, `fontes` (fonte 19, L21 resolvida), `render-e-entrega`, `video-render-deliver`, `video-env-preflight`, TP-06, VS15, VP-02, VP-05, VP-08, VP-25, VP-32, auditor A5 |
| 2 | Preview em `http://127.0.0.1:3002` fixo | A porta começa em 3002 e o CLI tenta até 100 portas se estiver ocupada | `portUtils.ts:23` (`MAX_PORT_SCAN = 100`), `:452-480` | `video-render-deliver`, `render-e-entrega`, `toolchain-windows`, VP-25, gotcha 14 do playbook |
| 3 | Invólucro sem higiene do endereço do preview | **Invólucro alterado:** `Set-HfSession` remove `HYPERFRAMES_PREVIEW_HOST` (2 linhas ASCII) | teste local no scratchpad: parse com 0 erros, 0 bytes fora do ASCII, `hfs -DryRun lint` imprimiu o comando fixado e tirou a variável e uma credencial fictícia da sessão, `projeto\` com 0 entradas, `hfs usage` bloqueado e registrado; nada do HyperFrames executado | TP-06 (seção de teste atualizada e honesta sobre a alteração) |
| 4 | Gotcha: "`DO_NOT_TRACK=1` sozinho não cobre o media-use" | O media-use desliga com `HYPERFRAMES_NO_TELEMETRY === "1"` **ou** `DO_NOT_TRACK === "1"`; o cuidado real é o valor: só `1` vale para o media-use (o CLI aceita `1/true/yes/on`) | `skills/media-use/scripts/lib/telemetry.mjs:40-47`; `packages/cli/src/telemetry/policy.ts:16-37` | `seguranca-e-privacidade` §13, auditor A5 |
| 5 | `code-scroll` "troca legibilidade por movimento" | `code-typing`, `code-diff`, `code-highlight` e `code-scroll` são os quatro de explicação; `code-morph` e os blocos 3D, de shader e de partículas trocam legibilidade | `docs/prompting/code-blocks.mdx:14-29` | `software-explainer-storyboard` passo 10, VP-16 (`explicar-software.md` já estava certo) |
| 6 | "Os scripts de áudio sobem até 5 pastas" | O laço examina 5 pastas **contando a de partida** (a de partida e 4 acima) e para no primeiro `.env`, inclusive vazio | `skills/media-use/audio/scripts/lib/heygen.mjs:72-95` (`for (let i = 0; i < 5; i++)`) | `seguranca-e-privacidade` §6, `video-env-preflight` passo 3, auditor A3, `fontes` V-05 |
| 7 | `.media` "fica em `<pasta-do-video>\.media-home`" | Os arquivos vão para `<MEDIA_HOME>\.media\` (`preferences.json`, `recipes`) | `skills/media-use/scripts/lib/media-home.mjs:7-20`, `prefs-store.mjs:44`, `recipe-store.mjs:61` | `seguranca-e-privacidade` §5 e §7, `video-env-preflight` passo 10 |
| 8 | `claude plugin validate <pasta> --strict` | A flag não existe no CLI 2.1.128 (achado do estrutural, que só corrigiu o README) | `BUILD-REPORT-structural.md` §4 | `ferramentas-e-mcp` §8 |
| 9 | Posturas divergentes: `catalog --on-device` em P (`seguranca` 3.1) e em C (invólucro, V-21); `telemetry disable` em C (VP-32) e em P (política, invólucro) | Alinhado: `catalog --on-device` é C (download de cerca de 33 MB); `telemetry disable` é P (configuração persistente; o invólucro bloqueia) | V-21; invólucro TP-06 | `seguranca-e-privacidade` 3.1 e 3.2, VP-32 |
| 10 | Comandos com placeholders sem aspas: `--preset <nome>`, `--quality <q> --output renders\<nome>.mp4`, `--voice <id>`, `snapshot --at <pontos-médios>` | O PowerShell rejeita `<` sem aspas (parser: 1 erro; com aspas: 0) | `Parser::ParseInput` local | `video-design-system`, `video-render-deliver`, `checklist-completo`, `design-system-para-video`, VP-18 |
| 11 | `init.ts:843-846` | A checagem de pasta não vazia está em `init.ts:842` (erro em 843, saída em 844) | leitura de `packages/cli/src/commands/init.ts:836-845` | TP-06 (comentário do invólucro, mesmo tamanho), `toolchain-windows`, `video-brief-interview` |

Conferidas e **mantidas** (o plugin estava certo): `usage` lê `~\.claude\.credentials.json` e chama `api.anthropic.com/api/oauth/usage` (`harnessUsage.ts:113,176-190,246`); `init` ignora `--skip-skills` e só `HYPERFRAMES_SKIP_SKILLS === "1"` desliga a atualização das skills globais (`init.ts:739-742,785-794`); `init` recusa pasta com qualquer entrada (`init.ts:842`); `render` e o Studio do `preview` usam `ensureBrowser({ preferManagedChrome: true })` e baixam `chrome-headless-shell 152.0.7977.30` sem `HYPERFRAMES_BROWSER_PATH` existente (`render/execute.ts:194,200`, `studioServer.ts:285`, `manager.ts:51,338-345`); o GSAP vem de `cdn.jsdelivr.net/npm/gsap@3.15.0` (`core/src/gsapCdn.ts:1-5`); opt-out da telemetria do CLI com `1/true/yes/on` (`policy.ts`); o `audio.mjs` do media-use chama `loadEnvFromDir` a partir do projeto (`audio.mjs:118`); os 19 SFX existem (`skills/media-use/audio/assets/sfx/manifest.json`).

## 4. Rastreabilidade (ids que o usuário não conseguia resolver)

- `fontes.md` ganhou a **seção 10, índice dos 76 itens `V-nn`** (tema em uma linha e arquivo do HyperFrames que o sustenta) e a **seção 11, siglas internas** (`G`, `D`, `C` de conflitos e `C` do `composition-reviewer`, `L`, `VC`/`PV`/`AV`, `VS`, `VP`, `TP`, ids da pesquisa bruta, princípios da fábrica, `ORCHESTRATOR.md §n`, caso real, "crítico", estilo da casa). A tabela de lacunas listava L15 a L25 numa linha só: agora cada uma tem linha própria (L21 resolvida).
- Os cabeçalhos das 9 referências que diziam "itens `V-nn` de `docs/research/video-hyperframes/VALIDATED.md`" apontam para o índice; as linhas "Itens V-.." das 8 skills de tarefa, as gotchas e a biblioteca de prompts também. Não resta caminho `docs/research` nem `docs/foundation` fora da seção de fontes, onde aparece como proveniência.
- Removidas as referências opacas `(P-18)` e `(C2)` em `seguranca-e-privacidade` (agora com o princípio por extenso e o arquivo do conflito).

## 5. Pendências do estrutural, estado

| Pendência | Estado |
| --- | --- |
| Sumário em `hf-sessao.ps1.md` | Feito (seções 1 a 7) |
| Sumário em `roteiro-oficial-de-perguntas.md` | Já existia (linha 5, sumário em linha única com as 10 seções); mantido |
| VP-03 com quadro de exemplo completo e generalizado | Já existia (F05, sistema fictício, só `[HEX_*]`, sem valores do design system do dono); conferido e anotado |
| IDs `V-nn` autoexplicativos | Feito (seção 10 de `fontes.md` e ponteiros em todo o plugin) |

## 6. Direitos autorais e segurança

- Literal de terceiros: só uma mensagem de erro curta do compilador entre aspas, com arquivo citado (`toolchain-windows.md` §9). Todo o resto é redação própria com citação de arquivo e commit; atribuição "HyperFrames, HeyGen, Apache-2.0" e "sem afiliação" no README e em `fontes.md`. Nenhum valor do design system do dono (`#1B2A3A`, `#C2456E`, nome do sistema): 0 ocorrências.
- Agentes: `tools: Read, Grep, Glob` nos 5; nenhum `Write`, `Edit` nem `Bash`. Skills com efeito (`video-toolchain-setup`, `video-render-deliver`) com `disable-model-invocation`. Nenhum hook, `.mcp.json`, `.lsp.json`, `bin/` nem arquivo executável (o invólucro e o hook seguem como texto em `.md`). Nenhum fluxo autoriza download, instalação, nuvem, publicação ou render sem confirmação; `--dangerously-skip-permissions` só aparece para ser recusado.
- Evals: PASS e FAIL observáveis na resposta final; 2 negativos com `arm: both`; injeção (diretiva de `SKILL.md` de terceiros, keyword e `publish` dentro de log); privacidade (`.env` com chave de nuvem, grader determinístico `no-open-env`). Seguem `designed_not_executed`.

## 7. Pendências (não corrigidas: decisão do dono, ferramenta compartilhada ou fora do escopo)

1. **Modelo dos agentes** (`model: inherit` nos 5, contra `sonnet`/`haiku` previstos no desenho): decisão de custo do dono.
2. **`tools/verify_plugin.py`** não mede descrições em `>-` nem `tools` de agentes; medido à mão nesta revisão (descrições entre 337 e 958 caracteres, todas abaixo de 1024). Ferramenta do coordenador.
3. **Nada do caminho real foi executado:** render, voz PT-BR, Parakeet, efeito do `.env` vazio, `MEDIA_HOME` e o endereço do preview em execução continuam Inferidos ou Não verificáveis; o primeiro uso deve começar pelo render de prova e conferir a escuta com `Get-NetTCPConnection`.
4. **Hook e `deny` não testados dentro do Claude Code** (L15).
5. **Evals** não executáveis aqui (CLI 2.1.128 abaixo de 2.1.269); sem caso positivo do `VIDEO-COMPLETO` nem de delegação aos agentes.
6. **Colisão de nomes** `C1` a `C14` (checklist do `composition-reviewer`) e `C1` a `C18` (conflitos): documentada em `fontes.md` §11; renomear exigiria mexer em agente, skill e referências.
7. **Densidade (D9):** a lista de variáveis de sessão se repete nas 8 skills de tarefa. Mantida de propósito (cada skill pode ser carregada sozinha); se o custo de contexto incomodar, troque por um ponteiro para `seguranca-e-privacidade.md` §5.
8. **Amostra:** 14 dos 32 prompts foram pontuados um a um (VP-01, 02, 03, 04, 05, 06, 07, 08, 11, 16, 20, 21, 25, 32); os outros 18 foram lidos, sem achado bloqueante, mas sem nota individual.
9. **Marketplace** (`marketplace.json`, `CATALOGO.md`) e tag `video-edicao` do orquestrador: pendências do coordenador herdadas do desenho.
10. **Exemplo de `STORYBOARD.md`** em `formatos-storyboard-e-script.md` usa `arc: concept-explainer com processo` (mistura de idiomas no valor); o upstream usa "concept-explainer with process". Cosmético.

## 8. Verificação final

- `python tools/verify_plugin.py plugins/video-hyperframes` → `Plugin: video-hyperframes {'skills': 10, 'agents': 5, 'commands': 0, 'evals': 10, 'files': 74}` e `RESULT: PASS`.
- `claude plugin validate plugins/video-hyperframes` → `✔ Validation passed`.
- Script próprio (scratchpad): 0 links quebrados (relativos e `${CLAUDE_PLUGIN_ROOT}`); nenhum caractere de controle acidental nos `.md`; todo arquivo de referência acima de 100 linhas tem sumário; playbook com 228 linhas (limite 300).
- Invólucro TP-06 extraído para uma árvore de teste no scratchpad: parse com 0 erros, 6.766 bytes ASCII com fim de linha LF, `-DryRun` e recusas como descrito na seção 3.
