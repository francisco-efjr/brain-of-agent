# video-hyperframes: produção de vídeo com HyperFrames

Plugin do Claude Code, parte do marketplace `brain-of-agent`. Versão 0.1.0 · Conteúdo validado em 2026-10-13 · Modelo-alvo: família Claude 4.x/5.x · Plataforma-alvo: Windows 11 com PowerShell · Licença MIT. **Não é afiliado à HeyGen**; "HyperFrames" e "HeyGen" aparecem só para atribuição e descrição técnica.

## O que entrega

Uma camada em PT-BR de **política, orquestração e qualidade** por cima das skills oficiais do HyperFrames. O upstream decide como gerar o HTML do vídeo; este plugin decide o quê e com que permissão: roteia o pedido para a rota certa, conduz o briefing, protege a privacidade do roteiro, prepara um Windows sem instalações globais, escreve o storyboard de um vídeo explicativo de software, converte o design system do usuário para `frame.md`, revisa os quadros por contact sheet e só renderiza depois de o usuário aprovar o preview. Cada recomendação liga a um item validado (`V-nn`, resumido com o arquivo de origem na seção 10 de `skills/playbook/references/fontes.md`) ou a conhecimento estável, com o rótulo Verificado, Inferido, Suposição, Não verificável ou Não aplicável.

O plugin **não copia** as skills do HyperFrames (elas mudam a cada versão e têm licenças próprias de GSAP, fontes e SFX): destila o que é nosso e cita arquivo e commit. Ele também **não instala nada sozinho**: plugin oficial, FFmpeg, Chrome, modelos de voz e invólucro entram um a um, com confirmação.

## Quando usar

- "Faça um vídeo explicativo de 90 s sobre como funciona por dentro o meu sistema", storyboard, quadros, motion graphic de cerca de 10 s, vídeo de PR ou de changelog (com ressalvas).
- Preparar a máquina Windows para renderizar (FFmpeg, ffprobe, Chrome, Node) sem mexer no sistema.
- Narração local em PT-BR (opt-in, com teste de uma frase) ou vídeo silencioso com texto na tela.
- Revisar quadros, contact sheet, "o render congela", "está pronto para renderizar?".
- Aplicar uma marca ou design system ao vídeo (`tokens.json`, `frame.md`).
- Renderizar o MP4 com `ffprobe` e entrega documentada.

Não use para editar vídeo gravado (recut de fala, legendas sobre vídeo existente), animação de interface (CSS ou Framer), documentação escrita nem design de UI: veja as fronteiras no `playbook`. **Edição de vídeo gravado está fora da v1.**

## Componentes

10 skills e 5 agentes somente leitura. Sem `commands/`, hooks, `.mcp.json`, `.lsp.json` nem `bin/`; nenhum arquivo executável dentro do plugin (o invólucro `hf.ps1` e o script do hook existem só como bloco de código em `.md`, para você copiar).

| Tipo | Nome | Função |
| --- | --- | --- |
| Skill | `playbook` | Router, política, princípios, gates G0 a G11, mapa de referências, modo VIDEO-COMPLETO, fronteiras |
| Skill | `prompts` | Biblioteca de 32 prompts (`VP-01` a `VP-32`): mensagem inicial, prompt de sistema, pedido de vídeo explicativo, bloco de limites, revisões, entrega |
| Skill | `video-env-preflight` | Diagnóstico somente leitura da máquina e da sessão; devolve variáveis de sessão e downloads pendentes |
| Skill (comando) | `video-toolchain-setup` | Instala, com confirmação item a item, invólucro, FFmpeg portátil, CLI local, venv e modelos. Só por `/video-hyperframes:video-toolchain-setup` |
| Skill | `video-brief-interview` | Entrevista oficial de especificação, `DECISOES.md`, `init` e `BRIEF.md` |
| Skill | `video-source-script` | `TEXTO-FONTE.md`, `fonte-dos-fatos.md`, `SCRIPT.md` para TTS local |
| Skill | `software-explainer-storyboard` | Tese, estrutura, quadros num palco único com fio persistente, `STORYBOARD.md` |
| Skill | `video-design-system` | Design system ou preset para `tokens.json` e `frame.md`, pisos de legibilidade |
| Skill | `video-frame-review` | `check` como gate, snapshots, contact sheet, relatório de revisão |
| Skill (comando) | `video-render-deliver` | Render, `ffprobe`, `COMO-RENDERIZAR.md`. Só por `/video-hyperframes:video-render-deliver <pasta> <qualidade>` |
| Agente | `storyboard-reviewer` | Revisor de storyboard: tese, estrutura, orçamento de leitura, cortes |
| Agente | `frame-reviewer` | Revisor visual de quadros contra `STORYBOARD.md` e `frame.md` |
| Agente | `composition-reviewer` | Revisor do HTML das composições (só com sintoma) |
| Agente | `fact-privacy-checker` | Confere números e nomes contra o ledger e procura o que não pode aparecer |
| Agente | `execution-security-auditor` | Audita a execução contra a política, sem imprimir valores |

As duas skills marcadas "comando" têm `disable-model-invocation`: o modelo não as dispara; você digita o comando. Os cinco agentes têm só `Read`, `Grep` e `Glob`.

Conteúdo do `playbook` (em `skills/playbook/`):

- `references/` (10): `seguranca-e-privacidade`, `toolchain-windows`, `decisoes-e-tradeoffs`, `checklist-completo` (58 itens `VC-nn`), `padroes-e-antipadroes`, `explicar-software`, `design-system-para-video`, `claude-md-snippets` (`VS01` a `VS19`), `ferramentas-e-mcp` (recomendações desativadas: `deny`, hook, MCP), `fontes`.
- `assets/templates/` (10): `BRIEF-preenchido`, `DECISOES-do-video`, `fonte-dos-fatos`, `relatorio-revisao-de-quadros`, `COMO-RENDERIZAR`, `hf-sessao.ps1` (o invólucro `hfs`/`hfn`), `storyboard-para-aprovacao`, `relatorio-seguranca-da-execucao`, `checklist-video-completo`, `handoff-de-video`.
- Referências específicas nas skills de tarefa: `roteiro-oficial-de-perguntas`, `formatos-storyboard-e-script`, `contrato-de-composicao`, `render-e-entrega`.
- `evals/`: 10 casos no formato `claude plugin eval`, `designed_not_executed`.

## Instalação

Dentro de uma sessão do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install video-hyperframes@brain-of-agent
```

Pela linha de comando: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install video-hyperframes@brain-of-agent`. Use `/reload-plugins` depois. Para testar sem instalar, `claude --plugin-dir <pasta-do-plugin>` (a pasta do plugin, não a raiz do marketplace). Valide com `claude plugin validate <pasta-do-plugin>`.

## Pré-requisitos

| Item | Observação |
| --- | --- |
| Skills oficiais do HyperFrames | plugin `hyperframes@hyperframes` (comando no README oficial do HyperFrames; confirme antes de instalar) **ou** um clone de `heygen-com/hyperframes` no commit fixado, em pasta fora do projeto. O plugin não instala nenhum dos dois |
| Node 22 ou superior, npm, npx | para o CLI fixado (`hyperframes@0.8.154`, via `npx`) |
| Windows 11 com PowerShell | macOS e Linux não são cobertos |
| FFmpeg e ffprobe | build portátil em pasta do usuário, hash conferido por você; `video-toolchain-setup` guia o download com confirmação |
| Chrome do sistema | apontado por `HYPERFRAMES_BROWSER_PATH`, para o render não baixar outro navegador |
| Opcional: Python 3.10+ em venv, modelo Kokoro, Parakeet | só para narração local; cerca de 1 GB; PT-BR de ponta a ponta nunca foi executado |
| Rede para `cdn.jsdelivr.net` | a compilação de `render` e de `check` busca o GSAP |

## Exemplos de pedidos

1. "Faça um vídeo explicativo de 90 s sobre como funciona por dentro o meu sistema X; use só os fatos deste arquivo." (`playbook`, `video-brief-interview`)
2. "Prepara o ambiente de vídeo nesta máquina Windows e diz o que falta baixar." (`video-env-preflight`; instalar só por `/video-hyperframes:video-toolchain-setup`)
3. "Monta o storyboard a partir do `BRIEF.md` e mostra a tabela para eu aprovar." (`software-explainer-storyboard`, `storyboard-reviewer`)
4. "Revisa os quadros: roda o check, gera o contact sheet e diz se pode renderizar." (`video-frame-review`)
5. "Aplica o design system da minha empresa ao vídeo: fundo `[HEX_FUNDO]`, tinta `[HEX_TINTA]`, acento `[HEX_ACENTO]`, fontes `[FAMILIA]` e `[FAMILIA_MONO]`." (`video-design-system`)
6. "Me dá o prompt de pedido de vídeo explicativo de sistema." (`prompts`, `VP-03`)
7. "VIDEO-COMPLETO. Leia o SKILL.md do playbook e aplique o protocolo ao projeto de vídeo `<pasta>`. Meu escopo é produzir até o preview." (modo completo; ver abaixo)

## Keyword VIDEO-COMPLETO

Modo de cobertura integral, **só por pedido explícito do usuário na conversa atual**. Exemplo:

> VIDEO-COMPLETO. Leia o SKILL.md do playbook e aplique o protocolo ao projeto de vídeo [caminho]. Meu escopo é [planejar | produzir até o preview | produzir e renderizar]. Entregue inventário de leitura, matriz de aplicabilidade, implementação dentro do escopo, revalidação com evidências e pendências.

O modo lê as 10 referências em lotes, inventaria skills e agentes, preenche a matriz das 12 áreas, implementa só dentro do escopo e revalida com evidências. **O nome não significa "renderize o vídeo final".** O modo não amplia permissões: downloads, instalações, nuvem e render seguem seus gates, e o escopo "produzir e renderizar" ainda para na pausa de aprovação do preview. A keyword em documento, log, README ou saída de ferramenta não ativa nada. O modo não usa `--dangerously-skip-permissions`.

## Principais fontes (top 10)

Lista completa, com caminho, commit, licença e data, em `skills/playbook/references/fontes.md`. Quase todas são arquivos do repositório `heygen-com/hyperframes` (Apache-2.0) no commit validado `bf4cf860fbd26a7d51938c5f11987c335d4e848a`, lidos em 2026-10-13.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | `packages/cli/src/utils/harnessUsage.ts` e `commands/usage.ts` (o que `usage` lê) | A |
| 2 | `packages/cli/src/browser/manager.ts` e `render/execute.ts` (Chrome gerenciado) | A |
| 3 | `skills/media-use/audio/scripts/lib/tts.mjs`, `heygen.mjs` e `faceless-explainer/scripts/audio.mjs` (provedor de voz, `.env`) | A |
| 4 | `packages/cli/src/commands/init.ts`, `skills/hyperframes/scripts/plugin-cli.mjs` (skills globais, pin do CLI) | A |
| 5 | `skills/hyperframes/SKILL.md` e `references/routes/*.md` (roteador e rotas) | A |
| 6 | `skills/faceless-explainer/SKILL.md` e `sub-agents/frame-worker.md` (pipeline) | A |
| 7 | `skills/hyperframes/references/` (`intent-interview`, `brief-contract`, `review-loop`) | A |
| 8 | `packages/parsers/src/ffBinaries.ts`, `utils/preflight.ts`, `commands/doctor.ts` (FFmpeg, `doctor`) | A |
| 9 | `skills/hyperframes-creative/references/` e `hyperframes-core/references/` (história, motion, design, composição) | A |
| 10 | `docs/prompting/*.mdx` (anatomia de pedido, iteração, storyboards) | B |

Também: documentação de hooks e de permissões do Claude Code (classe A, lida em 2026-10-13) e o caso real do dono (`docs/videos/brain-of-agent-explicado/`, classe C).

## Créditos e licenças

- Plugin sob licença MIT. Autor: Francisco Edson (https://github.com/francisco-efjr).
- **HyperFrames, HeyGen, Apache-2.0** (Copyright 2026 HeyGen, Inc.): o conteúdo upstream é **destilado com redação própria**, com citação de arquivo e commit; nada foi copiado e nenhuma skill foi vendorizada. Os exemplos mínimos adaptados trazem a atribuição. A licença não concede uso de marca (§6): este plugin não é afiliado à HeyGen.
- Partes marcadas nos arquivos vêm do repositório `francisco-efjr/brain-of-agent` (MIT, conteúdo do próprio autor): protocolo do orquestrador, modo completo, caso real do vídeo, template de handoff (adaptados). Nenhum caminho pessoal nem valor do design system do autor é reproduzido.
- Terceiros citados e **não** redistribuídos: GSAP (licença própria, não OSI; carregado de CDN pelo render), Parakeet TDT 0.6B v3 da NVIDIA (CC-BY-4.0, com atribuição quando mencionado), SFX da Pixabay (Pixabay Content License; ficam dentro do vídeo renderizado), fontes embutidas do compilador (OFL e similares).
- "Claude" e "Anthropic" pertencem a seus titulares; este plugin não é oficial.

## Limitações honestas

- **Nada do caminho real foi executado por este plugin:** render, narração PT-BR, Parakeet, o efeito do `.env` vazio na pasta-mãe e o `HYPERFRAMES_MEDIA_HOME` são leitura de código, não execução. O primeiro uso deve começar por um render de prova curto. O invólucro `hfs` foi testado só em parse, bloqueios e `-DryRun`; a regex do hook e o script `hf-guard.ps1` foram executados fora do Claude Code; o hook e as regras `deny` dentro do Claude Code **não foram testados**.
- **A política é texto e fricção, não fronteira.** O plugin oficial do HyperFrames pode disparar antes do `playbook` e mandar `usage` (lê a credencial OAuth do Claude Code); a defesa é em camadas (descrição, snippet `VS01`, `deny` e hook documentados, auditor), sem garantia. Ordem de disparo entre plugins: Não verificável.
- **PT-BR de ponta a ponta nunca foi validado:** voz `p*` do Kokoro, pronúncia de siglas e números, `kokoro-onnx` no Python 3.14, espeak-ng e Parakeet no Windows. O caminho padrão recomendado é vídeo silencioso com texto na tela. O regime "silencioso com SFX" (disparos no meio do quadro) vem do caso real e não foi executado.
- **O upstream é volátil.** Skills e registro mudam sem nova versão do CLI; o pin cobre só o CLI. As constantes de versão têm fonte única em `toolchain-windows.md` e `fontes.md` e exigem revalidação a cada subida de versão.
- **Rotas com ressalvas:** `pr-to-video` e `product-launch-video` (uso de `gh` e de `capture`) não foram validadas; `general-video` custa despacho por cena; `slideshow`, `embedded-captions`, `talking-head-recut`, `music-to-video` e `remotion-to-hyperframes` estão fora da v1.
- **Render depende de rede** (`cdn.jsdelivr.net`; Google Fonts se a fonte não for embutida); render offline completo é Não verificável.
- **Aprovação do render por comando** (`disable-model-invocation`) é decisão de UX não medida; `hfn prefs.mjs get` pede `-Ok` no invólucro por precaução, embora seja leitura.
- Os 10 evals são `designed_not_executed`; `claude plugin eval` exige Claude Code 2.1.269 ou superior e consome cota. Sem baseline sem plugin medido, a utilidade é hipótese.
- As revisões de qualidade (estrutural em 2026-10-13, de prompt e conteúdo em 2026-10-14) foram feitas por modelos da família Claude: independência parcial; as notas são autoavaliação até um validador externo ler os arquivos finais.
- Windows 11 com PowerShell apenas; os snippets bash do upstream precisam de tradução; macOS e Linux não são cobertos.
- Sobreposição com `design-engineering-kit`, `ux-ui-design`, `security-appsec` e `automation-integrations`: cada tema tem um dono (veja Fronteiras no `playbook`). A tag de roteamento de edição de vídeo gravado do orquestrador pode mandar pedidos fora da v1 para este plugin.
