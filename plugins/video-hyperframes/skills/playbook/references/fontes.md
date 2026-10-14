# Fontes: bibliografia validada do segmento Produção de vídeo com HyperFrames

Consulta e validação: 2026-10-13 · Rótulos: Verificado, Inferido, Suposição, Não verificável.
Classe A: contrato operacional ou código do próprio mantenedor, ou documentação oficial da tecnologia. Classe B: documentação pública do mantenedor. Classe C: apoio e contexto (arquivos do dono do plugin, práticas). "Destilar" = redação própria com atribuição e citação de arquivo e commit; é a decisão do projeto mesmo onde a licença permitiria copiar.
Origem: itens `V-nn` do relatório de validação da pesquisa do segmento (`VALIDATED.md`, que **não acompanha o plugin**), conferidos por um validador da família Claude (independência parcial) por **leitura de arquivo local** no commit abaixo; URLs não foram reabertas pelos pesquisadores, e estrelas, issues, releases e popularidade **não foram verificados**. Código vence documentação quando divergem (V-18, V-53). **Todo `V-nn` citado no plugin está resumido na seção 10**, com o tema e o arquivo do HyperFrames que o sustenta; as siglas internas (`D`, `C`, `L`, `VS`, `VP`, `TP`, `G` e as da fábrica) estão na seção 11.

## Sumário

1. Fonte única de versão
2. Ranking das fontes do HyperFrames
3. Outras fontes consultadas
4. Licenças e atribuições
5. Documentação defasada e itens rejeitados
6. Revalidação quando a versão subir
7. Lacunas
8. Política de uso
9. Gotchas
10. Índice dos itens V-nn
11. Siglas e referências internas

## 1. Fonte única de versão

Este arquivo e [toolchain-windows.md](toolchain-windows.md) guardam as constantes; em snippets, prompts e no invólucro elas são cópias literais que se atualizam juntas (`Grep` por `0.8.154`).

| Constante | Valor |
| --- | --- |
| Repositório | `heygen-com/hyperframes` (HeyGen, Inc.) |
| Commit validado | `bf4cf860fbd26a7d51938c5f11987c335d4e848a` (confirmado em `.git/refs/heads/main` e `packed-refs` do clone local) |
| CLI e plugin oficial | `0.8.154` (`plugin.json:5`, `.claude-plugin/plugin.json:4`, `packages/cli/package.json:3`) |
| Chrome gerenciado | `chrome-headless-shell 152.0.7977.30` |
| Licença | Apache-2.0, "Copyright 2026 HeyGen, Inc." (`LICENSE:1-4`); sem `NOTICE` na raiz |
| Data de conferência | 2026-10-13 |

Permalink de um arquivo: `https://github.com/heygen-com/hyperframes/blob/bf4cf860fbd26a7d51938c5f11987c335d4e848a/<arquivo>` (não aberto; sem rede nas conferências).

## 2. Ranking das fontes do HyperFrames

Caminhos relativos à raiz do clone, no commit acima. Quase todas são arquivos do próprio repositório. Nota = valor para o plugin e confiança na evidência (0 a 10).

| # | Fonte | Classe (nota) | V | Por que importa | Usada em |
| --- | --- | --- | --- | --- | --- |
| 1 | `packages/cli/src/utils/harnessUsage.ts`, `commands/usage.ts`; texto em `skills/hyperframes-cli/SKILL.md:193-199` e `skills/hyperframes/SKILL.md:19-21` | A (9) | V-01, V-11 | `usage` lê a credencial OAuth do Claude Code; o upstream manda rodá-lo; base da política mais importante | `seguranca-e-privacidade` |
| 2 | `packages/cli/src/browser/manager.ts`, `render/execute.ts`, `commands/validate.ts`, `windowsCrash.ts` | A (9) | V-14 | render e preview baixam Chrome gerenciado; ordem de resolução; crash 0xC0000409 | `toolchain-windows` |
| 3 | `skills/media-use/audio/scripts/lib/tts.mjs`, `lib/heygen.mjs`, `audio.mjs`; `skills/faceless-explainer/scripts/audio.mjs` | A (9) | V-05, V-06, V-24, V-29 | provedor de voz por credencial; `.env` subindo 5 pastas; wrapper sem `--lang` e `--provider` | `seguranca-e-privacidade`, `toolchain-windows` |
| 4 | `packages/cli/src/commands/init.ts`; `skills/hyperframes/scripts/plugin-cli.mjs`; `references/plugin-installation.md`, `skill-lifecycle.md` | A (9) | V-09, V-20 | `init` atualiza skills globais e recusa pasta não vazia; launcher exige `name: "hyperframes"`; pin do CLI | `toolchain-windows`, `decisoes-e-tradeoffs` |
| 5 | `skills/hyperframes/SKILL.md` e `references/routes/*.md` | A (9) | V-33, V-35, V-36 | roteador, 10 rotas, must-haves | `decisoes-e-tradeoffs` |
| 6 | `skills/faceless-explainer/SKILL.md`, `sub-agents/frame-worker.md`, `scripts/*` | A (10) | V-41, V-45 | pipeline completo com gates; scripts existem no disco | `checklist-completo` |
| 7 | `skills/hyperframes/references/intent-interview.md`, `brief-contract.md`, `brief-format.md`, `pitch-round.md`, `capability-menu.md`, `review-loop.md` | A (9 a 10) | V-34 a V-40, V-42 | camada de intenção, BRIEF, modos e gates, quatro pausas do usuário | `decisoes-e-tradeoffs` |
| 8 | `packages/parsers/src/ffBinaries.ts`; `packages/cli/src/utils/preflight.ts`, `commands/doctor.ts` | A (9) | V-13, V-15 | resolução de FFmpeg (cwd antes do PATH no Windows); checks do `doctor` | `toolchain-windows` |
| 9 | `skills/hyperframes-creative/references/` (`story-spine`, `story-design`, `motion-language`, `visual-design`, `typography`, `design-spec`, `video-composition`, `beat-direction`, `narration`) | A (9) | V-32, V-57, V-60 a V-67 | doutrina de história, motion, design e tipografia | `explicar-software`, `design-system-para-video` |
| 10 | `skills/hyperframes-core/references/` (`data-attributes`, `determinism-rules`, `sub-compositions`, `tracks-and-clips`, `minimal-composition`); `packages/lint/src/rules/composition.ts` | A (9) | V-49 a V-53, V-69 | contrato de composição e armadilhas silenciosas | `padroes-e-antipadroes` |
| 11 | `skills/hyperframes/references/frame-worker-core.md`, `subagent-dispatch.md` | A (9 e 7) | V-45, V-46 | contrato do worker; despacho com gate por artefato | `decisoes-e-tradeoffs` |
| 12 | `packages/cli/src/tts/*`, `whisper/*`, `utils/optionalPackages.ts` | A (8) | V-17, V-23, V-25 | Kokoro, Parakeet, pacotes opcionais, tamanhos | `toolchain-windows` |
| 13 | `packages/cli/src/telemetry/*`, `utils/updateCheck.ts`, `commands/feedback.ts`, `commands/publish.ts` | A (8 a 9) | V-02, V-03, V-04, V-07 | matriz de egresso, opt-out, o que `publish` e `feedback` enviam | `seguranca-e-privacidade` |
| 14 | `packages/producer/src/services/htmlCompiler.ts`, `core/src/gsapCdn.ts` | A (8) | V-19 | rede obrigatória na compilação (GSAP por CDN) | `toolchain-windows` |
| 15 | `docs/prompting/*.mdx` (`anatomy`, `specification-dial`, `iterating`, `capstone`, `storyboards`, `transitions`, `vocabulary`, `rendering-and-output`) | B (8 a 9) | V-54 a V-59, V-63, V-70 | anatomia de pedido, iteração, contrato cinematográfico; **partes defasadas** (qualidade padrão) | `explicar-software` |
| 16 | `LICENSE`, `CREDITS.md`, `SECURITY.md`, `skills/talking-head-recut/NOTICE.md` | A (9) e B (7) | V-73, V-74, V-75 | Apache-2.0; GSAP não OSI; Parakeet CC-BY-4.0; Pixabay para SFX; canal privado de segurança | este arquivo |
| 17 | Locais: `docs/videos/brain-of-agent-explicado/DECISOES.md`, `PROMPT-VIDEO.md`, `TEXTO-FONTE.md`, `REVISAO-PROMPT.md` (arquivos do dono, MIT) | C | V-71, V-72 | caso real do 1º uso: silencioso, 16:9, cerca de 90 s, FFmpeg portátil | `explicar-software`, `design-system-para-video` |
| 18 | Local: `brain-of-agent/ORCHESTRATOR.md` §0, §2, §5, §6, §7 (protocolo do dono, MIT) | A (protocolo do dono) | leitura direta | bloco de limites, "Onde testar agora", modo completo, autonomia, mensagem inicial | playbook (modo orquestrador), VP-01 |
| 19 | `packages/cli/src/server/portUtils.ts:23,431-447` (servidor do preview) | A (9) | leitura da revisão de qualidade, 2026-10-14 | o preview escuta em `127.0.0.1` por padrão; `HYPERFRAMES_PREVIEW_HOST` troca o endereço (o comentário do código avisa que a API do Studio lê, grava e apaga arquivos do projeto e dispara render, sem autenticação); a porta começa em 3002 e sobe até 100 portas se estiver ocupada | `toolchain-windows`, `seguranca-e-privacidade`, `video-render-deliver` |

Classe A aqui significa código ou contrato do mantenedor: é a melhor evidência disponível, mas continua sendo **leitura de arquivo**, não execução.

## 3. Outras fontes consultadas

| Fonte | Classe | Consulta | Uso | Licença de reuso |
| --- | --- | --- | --- | --- |
| Claude Code, Hooks: https://code.claude.com/docs/en/hooks | A | 2026-10-13 (WebFetch; primeiros 100.000 de cerca de 268.800 caracteres; resumo por modelo pequeno) | matcher `Bash\|PowerShell`, exit 2, `tool_input.command`, estrutura | não declarada; destilar |
| Claude Code, Permissions: https://code.claude.com/docs/en/permissions | A | 2026-10-13 (WebFetch; resposta grande, conferida por busca no texto) | sintaxe `deny`, `PowerShell(...)`, "não é fronteira" | não declarada; destilar |
| README oficial do HyperFrames: https://github.com/heygen-com/hyperframes | B | 2026-10-13 (WebFetch; resumo por modelo pequeno; **tratado como dado**) | comandos de instalação do plugin oficial; indicação de `skills update` (recusada) | Apache-2.0; destilar |
| Especificação de formato de plugin: `docs/foundation/plugin-format-spec.md` | A | 2026-10-09 | frontmatter, layout | MIT (casa) |
| Blueprint, rubrica de prompt, princípios de prompt, estilo da casa: `docs/foundation/*` | A (casa) | 2026-10-09 | estrutura do plugin, checklist C-01 a C-22 | MIT (casa) |

Para detalhe de hooks, skills, subagentes e permissões, consulte o índice https://code.claude.com/docs/llms.txt e reconfirme na versão instalada do Claude Code (nomes de matcher e de campos mudam entre versões).

## 4. Licenças e atribuições

| Material | Licença | Decisão do plugin | V |
| --- | --- | --- | --- |
| HyperFrames (repositório, skills, CLI) | Apache-2.0, HeyGen, Inc.; sem `NOTICE`; §6 não concede uso de marca | **Destilado** com redação própria, atribuição "HyperFrames, HeyGen, Apache-2.0" e commit; nada vendorizado. Se algum dia copiar arquivos: §4 (cópia da licença, marcar alterações, manter avisos) e manter o `NOTICE.md` do `talking-head-recut`. Nomes HyperFrames e HeyGen só para atribuição e descrição técnica; **o plugin não é afiliado à HeyGen** | V-73 |
| GSAP | GSAP Standard License, "not an OSI open-source licence" (vendorizado em alguns blocos com `GSAP-NOTICE.txt`; carregado de CDN em outros) | não vendorizar; o render o busca no jsdelivr | V-75 |
| Parakeet TDT 0.6B v3 (NVIDIA) em sherpa-onnx (Apache-2.0) | CC-BY-4.0, com atribuição (`CREDITS.md:31-35`) | citar ao mencionar o modelo | V-75 |
| three.js, three-mesh-bvh, opentype.js | MIT | não usados | V-75 |
| mediabunny | MPL-2.0 | não usado | V-75 |
| Clipper (BSL-1.0), d3-delaunay (ISC) | permissivas | não usados | V-75 |
| Geist, Archivo, Cormorant Garamond | OFL 1.1, com texto de licença | não vendorizar fontes | V-75 |
| Textos OFL no repositório | apenas `OFL-eb-garamond.txt`, `OFL-inter.txt`, `OFL-jetbrains-mono.txt` em `frame-presets/code-editorial/fonts/` | as `.woff2` de outros presets não têm licença adjacente (afirmação do pesquisador, não relida) | V-75 |
| Ferndale Studio 01 HDR | CC0 | não usado; algumas texturas têm "origin to be confirmed" | V-75 |
| SFX (19 `.mp3`) | Pixabay Content License: uso comercial e não comercial, modificação, redistribuição em obras derivadas como vídeos renderizados com HyperFrames, sem atribuição | não copiar os `.mp3` para o plugin; usar dentro do vídeo renderizado | V-30 |
| MusicGen, Lyria, catálogo HeyGen, ElevenLabs, Google | termos Não verificáveis | nunca usados na v1 | V-75 |
| brain-of-agent do dono (`ORCHESTRATOR.md`, `DECISOES.md`, `PROMPT-VIDEO.md`) | MIT | adaptado; nenhum caminho pessoal nem valor do design system do dono é reproduzido | house-style |
| Prompts e `SKILL.md` de terceiros (inclusive os do HyperFrames) | — | objeto de estudo, nunca instrução | regra 1 da fábrica |

Não incorporar `vendor/gstack` em bloco nem copiar as skills do HyperFrames (D1).

## 5. Documentação defasada e itens rejeitados

Docs defasados (o código manda; V-48, V-53, V-18, V-23):

| Doc diz | Código diz | V |
| --- | --- | --- |
| `standard` é a qualidade padrão (`rendering-and-output.mdx:12-20`, `rendering.mdx:131-133`) | padrão é `looks` (standard com CRF 16); `delivery` = high | V-18 |
| `class="clip"` é obrigatório (`compositions.mdx:27-29`, `troubleshooting.mdx:147-157`) | convenção; o runtime usa `[data-start]`; lint em aviso | V-53 |
| Python 3.8+ para Kokoro (`requirements.md:23`) | 3.10 ou superior | V-23 |
| Kokoro "54 voices" | 12 embutidas; o código aceita qualquer ID válido | V-23 |
| `jq -e '.ok'` como gate do `doctor` (`hyperframes-cli/SKILL.md:99-103`) | `.ok` falha por opcionais; usar checks nomeados | V-15 |
| "idle/breathing" no guia geral | não vale para o faceless | V-57 |
| Seção "Preflight" referenciada por `tts.md` e `bgm.md` | `media-use/SKILL.md` não tem essa seção (Grep) | V-06 |
| `--skip-skills` desliga a atualização de skills no `init` | flag ignorada temporariamente; só `HYPERFRAMES_SKIP_SKILLS=1` | V-09 |
| `prefs.mjs record` só grava em `~\.media` na promoção (V-08 original) | grava sempre o ledger em `<home>\.media\preferences.json` | leitura do crítico, `prefs-store.mjs:120-175` |

Rejeitados e rebaixados da pesquisa bruta (não servem de base): T-04 (Chrome sem download), T-05 (parte "Chrome ≤150"), T-08 (`doctor` como gate), T-11 (matriz de rede antiga), T-16 (Kokoro "padrão PT-BR"), T-21 (BGM com fallback), C-30 (prompt PT-BR original, nota 67; reescrito em V-72). Nenhum item foi rejeitado por injeção; nenhuma instrução dirigida a IA encontrada nas fontes foi obedecida.

Conflitos do upstream **não resolvidos** (não citar como fato): tipos de variável (5 na referência, 7 na documentação), `data-playback-start`, HeyGen `--oauth` contra CLI `heygen` "API-key-only", saída padrão do `render`.

## 6. Revalidação quando a versão subir

1. Anote a nova versão do plugin oficial e o commit; abra o `plugin.json` e `packages/cli/package.json`.
2. Releia, nos arquivos do novo commit, os itens sensíveis: `init.ts` (V-09), `manager.ts` (V-14), `doctor.ts` (V-15), `plan.ts` (V-18), `htmlCompiler.ts` (V-19), `plugin-cli.mjs` (V-20), `harnessUsage.ts` e `usage.ts` (V-01), `tts.mjs` e `heygen.mjs` (V-05, V-06), `faceless-explainer/SKILL.md` (V-41), `composition.ts` (V-53).
3. Compare o conjunto de verbos do CLI com a lista proibida e a de confirmação: verbo novo que envie dados entra em "proibido" até ser lido.
4. Atualize as constantes aqui e em [toolchain-windows.md](toolchain-windows.md); `Grep` por `0.8.154` e pelo commit antigo lista cada cópia literal (snippets, prompts, `hf.ps1`, regras `deny`).
5. Refaça o parse e o `-DryRun` do invólucro; registre a data.
6. Skills e registro mudam sem nova versão do CLI (V-48 #8, V-10): na dúvida, compare o commit.

## 7. Lacunas

Todas **Não verificado**; nenhuma deve ser citada como fato.

| # | Lacuna | Como o plugin lida |
| --- | --- | --- |
| L1 | PT-BR ponta a ponta nunca executado (voz `p*`, pronúncia de siglas e números, `kokoro-onnx` no Python 3.14) | padrão silencioso; narração opt-in com teste de uma frase |
| L2 | Arquitetura do áudio PT-BR (opções a, b, c) | recomendação provisória; decidir após o teste |
| L3 | espeak-ng no Windows | não instalar de início |
| L4 | Parakeet e sherpa-onnx no Windows 11 | nunca executado; sem eles, legendas desligadas |
| L5 | FFmpeg: origem, tamanho, integridade | o usuário confere o hash publicado |
| L6 | Render real (velocidade com Chrome comum, RAM, GPU, tamanho do MP4) | render de prova antes do definitivo |
| L7 | Render offline completo | aceitar a rede para o jsdelivr |
| L8 | `npx hyperframes` sem pin nos helpers do media-use | mitigação D4 (Suposição) |
| L9 | Pipeline com `words` vazio | `captions: skipped` é válido |
| L10 | Acentuação PT-BR nas fontes embutidas | `snapshot` de teste |
| L11 | Conteúdo mutável; estrelas, issues, releases | commit registrado |
| L12 | Itens só amostrais (`lambda.md`, `cloudrun.md`, `compare-and-batch.md`, `beats.md`, parte de `docs/prompting`, `hyperframes-audio`, `hyperframes-keyframes`, 21 de 22 blueprints, 12 de 13 presets) | o plugin aponta o arquivo oficial |
| L13 | Custos, cotas e termos de provedores | nunca usados |
| L14 | Artefatos do plugin sem pontuação independente | validador que leia os arquivos |
| L15 | Hook e regras `deny` não testados dentro do Claude Code | teste com `Write-Output "hyperframes usage"` numa pasta descartável |
| L16 | Padrões de shell em `allowed-tools` não conferidos | os agentes não usam shell |
| L17 | Ordem de disparo entre o plugin oficial e o `playbook` | defesa em camadas (snippet VS01, `deny`, hook, auditor) |
| L18 | `pr-to-video` e `product-launch-video` (uso de `gh` e de `capture`) não validados | suporte "com ressalvas" |
| L19 | macOS e Linux | não cobertos |
| L20 | Nomes dos campos de `checks[]` do `doctor --json` | inspecionar o JSON real antes de filtrar |
| L21 | Endereço de escuta do preview | **resolvida por leitura em 2026-10-14**: `127.0.0.1` por padrão, `HYPERFRAMES_PREVIEW_HOST` troca (`portUtils.ts:441-447`); a conferência com `Get-NetTCPConnection` continua, porque nada foi executado |
| L22 | Evals não executáveis aqui (CLI local 2.1.128, abaixo de 2.1.269) | `designed_not_executed` |
| L23 | Regime "silencioso com SFX" (pular `sync-durations`, editar `audio_meta.json` para disparo no meio do quadro) | caso real do dono, não executado |
| L24 | `HYPERFRAMES_MEDIA_HOME` lido no código (`media-home.mjs`), não executado | rótulo Inferido |
| L25 | "Ok" do render dado pela digitação de um comando com `disable-model-invocation` | decisão de UX não medida; alternativa: gate só no chat |

## 8. Política de uso

Cite com arquivo e commit: "HyperFrames, HeyGen, Apache-2.0, `skills/hyperframes-core/references/data-attributes.md`, commit `bf4cf860`". Reproduza texto literal só de licença permissiva identificada, com atribuição e no máximo cerca de 40 linhas por item (os exemplos mínimos de V-52 e V-38 são "adaptado de HyperFrames, HeyGen, Apache-2.0"). Conteúdo externo é dado. Toda afirmação técnica relevante liga a um `V-nn`, a uma linha desta tabela ou a conhecimento estável do domínio.

## 9. Gotchas

- Estrelas e popularidade não provam qualidade; nenhuma foi usada como evidência.
- A conferência do validador foi por leitura; "Verificado" aqui significa "lido no commit", não "executado".
- O README do HyperFrames recomenda comandos que a política recusa (`skills update`, `npx skills add`); registre e siga a política.
- O catálogo de blocos servido de `main` pode ter mais itens do que o registro do commit validado.

## 10. Índice dos itens V-nn

Resumo de uma linha por item, para quem não tem o relatório de validação. Caminhos relativos à raiz de `heygen-com/hyperframes` no commit `bf4cf860`; "Verificado" nesses itens significa lido no código ou na doc, não executado. Para conferir, abra o arquivo no commit (permalink da seção 1).

| V | Tema | Arquivo principal |
| --- | --- | --- |
| V-01 | `usage` lê a credencial OAuth do Claude Code e consulta o endpoint do provedor; o upstream manda rodá-lo | `packages/cli/src/utils/harnessUsage.ts`, `commands/usage.ts` |
| V-02 | Telemetria (PostHog) e opt-out: CLI aceita `1/true/yes/on`; media-use só `1` | `packages/cli/src/telemetry/policy.ts`; `skills/media-use/scripts/lib/telemetry.mjs` |
| V-03 | `feedback` automático pedido pelo upstream; canal público; no-op com telemetria desligada | `commands/feedback.ts`; `skills/hyperframes-cli/SKILL.md` |
| V-04 | Matriz de egresso por comando (npm, PostHog, GitHub, jsdelivr, Google Fonts, provedores) | vários; ver seção 4 de `seguranca-e-privacidade.md` |
| V-05 | Três carregadores de `.env`; o dos scripts de áudio examina até 5 pastas (a de partida e 4 acima) e carrega o primeiro `.env` inteiro | `skills/media-use/audio/scripts/lib/heygen.mjs`; `packages/cli/src/cli.ts` |
| V-06 | Provedor de voz escolhido pela credencial presente; o roteiro sai da máquina sem pedido | `skills/media-use/audio/scripts/lib/tts.mjs`; `skills/faceless-explainer/scripts/audio.mjs` |
| V-07 | `publish`, `cloud render`, `lambda`, `cloudrun` enviam o projeto ou geram custo | `commands/publish.ts`; `cloud.md` |
| V-08 | O que a toolchain grava fora do projeto (`~\.hyperframes`, `~\.cache\hyperframes`, `.media`) | `telemetry/config.ts`; `browser/manager.ts`; `prefs-store.mjs` |
| V-09 | `init` atualiza as skills globais; `--skip-skills` ignorado; só `HYPERFRAMES_SKIP_SKILLS=1`; recusa pasta não vazia | `packages/cli/src/commands/init.ts` |
| V-10 | `add <bloco>` baixa código de `main` sem pin | `packages/cli/src/registry/remote.ts` |
| V-11 | Diretivas do upstream que o plugin recusa (`usage`, `feedback`, `skills update`, login HeyGen) | `skills/hyperframes/SKILL.md`; `skills/hyperframes-cli/SKILL.md` |
| V-12 | Requisitos: Node 22 ou superior | `packages/cli/package.json` |
| V-13 | FFmpeg: variáveis `HYPERFRAMES_FFMPEG_PATH`/`FFPROBE_PATH`; no Windows o cwd vence o PATH | `packages/parsers/src/ffBinaries.ts` |
| V-14 | `render` e `preview` ignoram o Chrome do sistema e baixam `chrome-headless-shell` sem `HYPERFRAMES_BROWSER_PATH` existente | `packages/cli/src/browser/manager.ts`; `render/execute.ts` |
| V-15 | `doctor`: `.ok` falha por itens opcionais; usar checks nomeados | `commands/doctor.ts`; `utils/preflight.ts` |
| V-16 | Mapa de variáveis de ambiente | vários; tabela na seção 5 de `seguranca-e-privacidade.md` |
| V-17 | Sem `postinstall`; pacotes opcionais instalados sob demanda | `packages/cli/package.json`; `utils/optionalPackages.ts` |
| V-18 | Qualidades (`looks` é o padrão; `delivery` = high), `--output`, porta padrão 3002 | `render/plan.ts`; `commands/render.ts` |
| V-19 | Rede na compilação: GSAP 3.15.0 por `cdn.jsdelivr.net`; 18 fontes embutidas offline | `packages/producer/src/services/htmlCompiler.ts`; `packages/core/src/gsapCdn.ts` |
| V-20 | Launcher do plugin oficial; `npx` sem versão nos helpers do media-use | `skills/hyperframes/scripts/plugin-cli.mjs` |
| V-21 | Verbos do CLI com efeito, rede e postura L, C ou P | `skills/hyperframes-cli/SKILL.md` |
| V-22 | Onde renderizar: local, nuvem HeyGen, Lambda, Cloud Run | `skills/hyperframes-cli/SKILL.md`; `cloud.md` |
| V-23 | Kokoro local: Python 3.10+, vozes, espeak-ng, tamanhos | `packages/cli/src/tts/*` |
| V-24 | Wrapper de áudio do faceless: `provider: auto`, idioma inglês, sem `--voice` a voz é inglesa | `skills/faceless-explainer/scripts/audio.mjs` |
| V-25 | Transcrição: Parakeet (cerca de 670 MB) ou Whisper (compila com cmake no Windows) | `commands/transcribe.ts`; `whisper/*` |
| V-26 | TTS em nuvem (HeyGen, ElevenLabs, Gemini) | `skills/media-use/audio/references/tts.md` |
| V-27 | Login HeyGen e conflito OAuth × chave de API | `docs/guides/authentication.mdx` |
| V-28 | "Preflight" do upstream (`auth status` e parar) antes de voz ou música | `tts.md`; `bgm.md` |
| V-29 | Sem credencial HeyGen a música de fundo do faceless é pulada | `skills/media-use/audio/scripts/audio.mjs` |
| V-30 | 19 SFX da Pixabay embutidos e sua licença | `skills/media-use/audio/assets/sfx/` (`manifest.json`, `CREDITS.md`) |
| V-31 | Mixagem: descrever o sintoma, medir o nível antes | `docs/prompting/audio-effects.mdx` |
| V-32 | Ritmo de narração (cerca de 2,2 a 2,5 palavras/s) e escrita para TTS | `skills/hyperframes-creative/references/narration.md` |
| V-33 | Roteador: estado do projeto decide a rota | `skills/hyperframes/SKILL.md` |
| V-34 | Camada de intenção em 8 etapas | `skills/hyperframes/references/intent-interview.md` |
| V-35 | Perguntas oficiais do faceless (angle, length, destination, VO_MODE) | `references/routes/faceless-explainer.md`; `brief-contract.md` |
| V-36 | Must-haves por rota | `references/routes/*.md` |
| V-37 | Pitch round para pedido não formado | `references/pitch-round.md` |
| V-38 | `BRIEF.md`: campos e ciclo de vida | `references/brief-format.md`; `brief-contract.md` |
| V-39 | `flow` × `storyboard` → `mode`; render sempre gated pelo usuário | `references/brief-contract.md` |
| V-40 | Oferta de capacidades e pergunta de design em 3 estados | `references/capability-menu.md` |
| V-41 | Pipeline do faceless: passos, artefatos, pausas, contact sheet | `skills/faceless-explainer/SKILL.md` |
| V-42 | As quatro pausas do usuário no loop de revisão | `references/review-loop.md` |
| V-43 | Formato do `STORYBOARD.md` | `references/storyboard-format.md` |
| V-44 | Formato do `SCRIPT.md` (só o bloco recuado vai ao TTS) | `references/script-format.md` |
| V-45 | Contrato do worker de quadro: lê só o próprio pacote e o `frame.md`; zona da legenda | `references/frame-worker-core.md` |
| V-46 | Despacho de subagentes e gate por artefato | `references/subagent-dispatch.md` |
| V-47 | `lint` → `check` → `snapshot`; `browserSkipped`; gate não julga qualidade | `skills/hyperframes-cli/SKILL.md`; `lint-validate-inspect.md` |
| V-48 | Divergências entre docs e código, com resolução | vários |
| V-49 | Atributos `data-*` e armadilhas silenciosas | `skills/hyperframes-core/references/data-attributes.md` |
| V-50 | Determinismo e registro da timeline | `skills/hyperframes-core/references/determinism-rules.md` |
| V-51 | Sub-composições | `skills/hyperframes-core/references/sub-compositions.md` |
| V-52 | Exemplo mínimo de composição | `skills/hyperframes-core/references/minimal-composition.md` |
| V-53 | `class="clip"` é convenção (o lint só avisa) | `packages/lint/src/rules/composition.ts` |
| V-54 | Anatomia do pedido: rota, spec, beats, copy, técnica, negativos | `docs/prompting/anatomy.mdx` |
| V-55 | Vocabulário palavra → parâmetro de motion | `docs/prompting/vocabulary.mdx` |
| V-56 | "Prompt the plan" e direção fixa do vídeo | `skills/hyperframes-creative/references/story-spine.md` |
| V-57 | Doutrina de motion do faceless (power3, sem overshoot nem respiração) | `skills/faceless-explainer/references/motion-language.md` |
| V-58 | Contrato cinematográfico: um palco, fio persistente | `docs/prompting/capstone.mdx` |
| V-59 | Iteração com uma variável e alvos absolutos | `docs/prompting/iterating.mdx` |
| V-60 | Valor antes da evidência; não parafrasear o texto na ordem | `skills/faceless-explainer/references/story-design.md` |
| V-61 | Checklist final de 11 itens (compilado; não é lista oficial) | vários |
| V-62 | Estruturas de explainer, nove ganchos, seis técnicas, enum `type` | `skills/faceless-explainer/references/story-design.md` |
| V-63 | Verbos de beat e transições (uma primária) | `hyperframes-creative/references/beat-direction.md`; `docs/prompting/transitions.mdx` |
| V-64 | Blueprints de tomada | `skills/hyperframes-animation/blueprints-index.md` |
| V-65 | Diagramas, fluxos e números; não há bloco de arquitetura em camadas | `docs/guides/faceless-explainer.mdx`; `registry/blocks` |
| V-66 | `frame.md`, 13 presets, marca estrita e escala de vídeo | `hyperframes-creative/references/design-spec.md`, `video-composition.md` |
| V-67 | Tipografia: 18 famílias embutidas, lista "banida", pisos de legibilidade | `hyperframes-creative/references/typography.md` |
| V-68 | Blocos de código (`code-typing`, `code-diff`, `code-highlight`, `code-scroll` são os de explicação) e PRs | `docs/prompting/code-blocks.mdx`; `skills/pr-to-video/references/story-design.md` |
| V-69 | GSAP em seek frio (`fromTo`, `tl.set`) e determinismo | `docs/prompting/runtimes-and-3d.mdx`; `rules-and-anti-patterns.mdx` |
| V-70 | 4K, 60 fps, alpha: quando pedir | `docs/prompting/rendering-and-output.mdx` |
| V-71 | Método de conversão do design system de um usuário (caso do dono; valores não reproduzidos) | arquivos do dono (MIT) |
| V-72 | Esqueleto de pedido PT-BR reescrito (Inferido, não renderizado) | redação própria |
| V-73 | Licença Apache-2.0, sem `NOTICE` na raiz | `LICENSE` |
| V-74 | Canal privado de segurança do HyperFrames | `SECURITY.md` |
| V-75 | Licenças de terceiros (GSAP não OSI, Parakeet CC-BY-4.0) | `CREDITS.md` |
| V-76 | Windows: espaço e Unicode em caminhos, spawn sem shell | `runFfmpeg.ts`; `ffBinaries.ts`; `utils/preflight.ts` |

## 11. Siglas e referências internas

| Sigla | O que é | Onde está |
| --- | --- | --- |
| `G0` a `G11` | Gates do processo essencial | `SKILL.md` do playbook |
| `D1` a `D14` | Decisões de arquitetura do plugin (por exemplo D4 dependência local, D10 layout de pastas, D14 sem memória `.media`) | [decisoes-e-tradeoffs.md](decisoes-e-tradeoffs.md) |
| `C1` a `C18` (em decisões) | Conflitos entre fontes e como o plugin os resolve (por exemplo C2, plugin oficial disparando antes) | [decisoes-e-tradeoffs.md](decisoes-e-tradeoffs.md) |
| `C1` a `C14` (no `composition-reviewer`) | Itens do checklist de composição do agente; não confundir com os conflitos | `agents/composition-reviewer.md` |
| `L1` a `L25` | Lacunas Não verificadas | seção 7 deste arquivo |
| `VC-nn`, `PV-nn`, `AV-nn` | Itens do checklist completo, padrões e antipadrões | [checklist-completo.md](checklist-completo.md), [padroes-e-antipadroes.md](padroes-e-antipadroes.md) |
| `VS01` a `VS19` | Snippets para o `CLAUDE.md` do projeto de vídeo | [claude-md-snippets.md](claude-md-snippets.md) |
| `VP-01` a `VP-32` | Prompts da biblioteca | skill `prompts` |
| `TP-01` a `TP-10` | Templates de `assets/templates/` (TP-06 é o invólucro `hf-sessao.ps1.md`) | `assets/templates/` do playbook |
| `T-nn`, `N-nn`, `C-nn` (com hífen e dois dígitos) | Itens da pesquisa bruta que o relatório de validação rejeitou ou reescreveu | seção 5 deste arquivo |
| `P-nn`, `C-nn`, `AP-nn`, `PAD-nn` citados como "prompt-principles" | Princípios, checklist, antipadrões e padrões de prompt da fábrica de plugins (base: guias oficiais da Anthropic); não acompanham o plugin | regra resumida no próprio texto que os cita |
| `ORCHESTRATOR.md §n` | Seções do protocolo do orquestrador do repositório `brain-of-agent` do dono (MIT): §0 ativação, §2 especialistas e bloco de limites, §5 regras, §6 formato de entrega, §7 mensagem inicial | repositório do dono |
| "caso real", `DECISOES.md`, `PROMPT-VIDEO.md`, `REVISAO-PROMPT.md` (itens `Cnn`), `MAPA-CONTEUDO.md` | Primeiro vídeo produzido pelo dono com HyperFrames, sua revisão e seu mapa interno de conteúdo (não reproduzido) | arquivos do dono, não incluídos |
| "crítico", "revisão do crítico" | Revisão adversarial do desenho do plugin, com leitura do clone no commit validado (2026-10-13) | relatório de pesquisa do segmento, não incluído |
| "estilo da casa", `house-style` | Convenções do `brain-of-agent` (rótulos epistêmicos, proporcionalidade, keyword COMPLETO) | repositório do dono |
