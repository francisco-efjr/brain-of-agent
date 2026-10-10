# Validação independente do plugin `design-engineering-kit`

- **Data:** 2026-10-10
- **Validador:** agente separado (Claude Opus), com postura cética. O construtor foi outro agente (Sonnet). Os dois são da mesma família de modelo, então esta é uma revisão em contexto limpo e não uma validação externa.
- **Escopo:** `plugins/design-engineering-kit` (arquivos próprios e as 17 skills vendorizadas, lidas como dado), mais as edições pontuais em `ux-ui-design`, `web-frontend`, `mobile-apps`, `publish/ORCHESTRATOR.md` e `plugins/orchestrator/skills/playbook/references/protocolo.md`.
- **Critérios:** `docs/foundation/prompt-quality-rubric.md` (D1 a D12, aprovação a partir de 80) e `docs/foundation/plugin-format-spec.md`.
- **Não feito, por regra:** commit, push, instalação de plugin ou MCP, `npx`/`npm`, execução de qualquer coisa dos clones vendorizados. As skills vendorizadas e os `LICENSE` não foram editados.

## Veredito geral: APROVADO COM RESSALVAS

Pela rubrica, todos os artefatos pontuados ficaram com nota de 90 ou mais depois das correções, e nenhum critério de reprovação automática se aplica. As ressalvas: nada foi executado dentro do Claude Code (agentes e evals não rodaram); o bloqueio por nome no `ui-verifier` tem efeito em tempo de execução Inferido; as fontes oficiais da Figma divergem sobre limites; as skills taste podem disparar sozinhas pela `description` e isso não tem trava técnica.

## Resumo por checagem

| # | Checagem | Veredito | Evidência principal |
| --- | --- | --- | --- |
| 1 | Licenças e atribuição | Aprovado | 24 de 24 arquivos idênticos ao raw do GitHub em cada commit, normalizando CRLF; `LICENSE` idênticos ao upstream |
| 2 | Fatos de MCP contra fontes oficiais | Aprovado depois de correção | Limites do Figma estavam defasados (6/mês contra 20/mês na documentação atual); ferramentas de escrita sem nome; rótulos "informada" viraram Verificado com URL |
| 3 | Segurança | Aprovado depois de correção | Lacuna de `PowerShell` no `ui-verifier`; capturas gravadas na raiz do workspace; `disable-model-invocation` contornado; logos reais e dados com cara de reais vindos de `design-taste-frontend` |
| 4 | Precedência e conflitos | Aprovado | Conflitos conferidos nas linhas citadas; contraste recalculado; tokens do Mo baile e `dampingRatio` recalculados |
| 5 | Qualidade (D1 a D12) e formato | Aprovado | Todos de 90 a 98 depois; formato de evals bate com a documentação oficial; contagens do README batem |
| 6 | Verificação final | Aprovado | `RESULT: PASS` nos 5 plugins; `Validation passed` nos 3; `cmp` e `fc /b` sem diferença |

## 1. Licenças e atribuição

**Verificado.**

- **Clones de referência:** os refs lidos como arquivo (`.git/refs/heads/main`) estão em `e8a175de22ae1e49370fc144c1f3bb9aeedf988d` (emil) e `717446e07a78d4e6d7918b1fde1a263378eebac9` (taste). `diff -r` entre as 17 pastas e os clones não achou diferença; os dois `LICENSE` também são idênticos. Nada foi executado nos clones; nenhum comando `git` rodou dentro deles.
- **Upstream real, independente dos clones:** baixei de `https://raw.githubusercontent.com/<owner>/<repo>/<commit>/skills/<pasta>/<arquivo>` os 24 arquivos das 17 skills. Pelo hash bruto, todos diferem; normalizando CRLF (`tr -d '\r'`), **os 24 são idênticos**. A diferença é só de final de linha: as cópias locais têm CRLF (exemplo: `emil-design-eng/SKILL.md` com 674 CR, 27.797 bytes contra 27.123 no raw), herdadas do checkout no Windows. Não é alteração de conteúdo.
- **Completude:** a árvore da API do GitHub nos dois commits (`git/trees/<sha>?recursive=1`, `truncated: false`) tem exatamente esses 24 arquivos nas pastas incluídas. Nada ficou para trás.
- **LICENSE:** `third_party/emilkowalski-skills/LICENSE` e `third_party/taste-skill/LICENSE` têm o mesmo hash (normalizado) do upstream no commit e no `main`: MIT, "Copyright (c) 2026 Emil Kowalski" e "Copyright (c) 2026 Leonxlnx". Aviso de copyright e permissão presentes.
- **Atribuição:** `README.md` (tabela "Créditos e licenças") e `third_party/README.md` trazem autor, licença, repositório, commit completo, lista de skills e modificação ("pasta renomeada; conteúdo sem alteração"). A renomeação confere com o `name` do frontmatter no upstream: `taste-skill` para `design-taste-frontend`, `redesign-skill` para `redesign-existing-projects`, `minimalist-skill` para `minimalist-ui`, `soft-skill` para `high-end-visual-design`, `brutalist-skill` para `industrial-brutalist-ui`.
- **Correção:** a lista de excluídas do taste misturava pasta e `name` (`image-to-code` é o `name` da pasta `image-to-code-skill`). Corrigi em `third_party/README.md` e acrescentei a seção "Conferência de integridade" com a nota de CRLF.

## 2. Fatos de MCP contra fontes oficiais

Fontes baixadas como dado em 2026-10-10 (arquivos no scratchpad do validador):

| Fato | Estado antes | Estado agora | Fonte |
| --- | --- | --- | --- |
| URL do servidor Figma `https://mcp.figma.com/mcp` | Verificado | Verificado (também no `.mcp.json` do plugin oficial) | https://github.com/figma/mcp-server-guide (README) |
| `claude plugin install figma@claude-plugins-official` e `claude mcp add --transport http figma https://mcp.figma.com/mcp` | Verificado | Verificado | README do guia |
| `get_design_context`, `get_variable_defs`, `get_screenshot`, `get_metadata` | Verificado ou "citada" | Verificado | README do guia; https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/ |
| `search_design_system`, `get_code_connect_map` | "Informada pela pesquisa" | Verificado | tools-and-prompts |
| Ferramentas de escrita | "guia não nomeia" | Verificado por nome: `use_figma`, `generate_figma_design`, `create_new_file`, `upload_assets`, `generate_diagram`, `generate_image`, `add_code_connect_map`, `send_code_connect_mappings`, `create_*`/`update_*` de plugins e shaders; `weave_*` com créditos | tools-and-prompts |
| `use_figma` executa JavaScript no arquivo pela Plugin API; escrita exige assento Full | Ausente | Verificado | https://developers.figma.com/docs/figma-mcp-server/write-to-canvas/ |
| `generate_image` "consome créditos e escreve" | Impreciso | Corrigido: gasta créditos de IA da Figma, devolve URL temporária e não coloca no canvas | tools-and-prompts |
| Limite: 6 chamadas/mês para Starter e View/Collab | Apresentado como fato | **Divergência registrada**: o guia diz 6/mês; a documentação atual diz 20/mês, e Dev/Full 200/dia (Professional, Organization) ou 600/dia (Enterprise), com limite por minuto | README do guia; https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/ |
| Ferramentas isentas de limite | "as de escrita" | `add_code_connect_map`, `create_new_file`, `whoami`; `generate_figma_design` também | rate-limits-access; tools-and-prompts |
| Plugin oficial `figma`: versão e skills | "nomes informados" | Verificado: marketplace aponta para `figma/mcp-server-guide` no commit `f0493295acf5f7cbdebcbcc483c06de814420cb1`; `plugin.json` 2.2.127; 14 skills em `skills/` | https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/.claude-plugin/marketplace.json |
| Plugin oficial `playwright` usa `npx @playwright/mcp@latest` | Informado | Verificado no `.mcp.json` | https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright |
| `@playwright/mcp` 0.0.83, Apache-2.0 | Informado | Verificado | https://registry.npmjs.org/@playwright/mcp/latest |
| Flags `--allowed-origins`, `--blocked-origins`, `--isolated`, `--caps`, `--headless`, `--user-data-dir`, `--storage-state`, `--viewport-size`, `--allow-unrestricted-file-access`, `--no-sandbox` | Verificado | Verificado; acrescentei `--output-dir`, `--grant-permissions`, `--secrets` e as capacidades `config`, `network`, `storage`, `testing` | https://github.com/microsoft/playwright-mcp (README) |
| Aviso: origens e o próprio MCP "não são fronteira de segurança"; `browser_run_code_unsafe` "RCE-equivalent" | Verificado em parte | Verificado | README do Playwright MCP |
| Ferramentas `browser_*` citadas pelo kit | Verificado | Verificado (todas existem); `browser_emulate_media` tem `reducedMotion` | README do Playwright MCP |
| `browser_take_screenshot` grava em disco (diretório de saída ou, com nome relativo, raiz do workspace) | Ausente | Verificado e incorporado | README do Playwright MCP |
| `disallowedTools` é campo válido em agente de plugin | Suposto | Verificado: agentes de plugin ignoram só `hooks`, `mcpServers` e `permissionMode` (e `initialPrompt`) | https://code.claude.com/docs/en/sub-agents |
| Nomeação `mcp__plugin_<plugin>_<servidor>__<ferramenta>` | Informado (Playwright) e analogia (Figma) | Verificado pela regra documentada e pelos manifestos | https://code.claude.com/docs/en/mcp ; https://code.claude.com/docs/en/plugins/components |
| `disable-model-invocation: true` impede o modelo de disparar a skill | Verificado | Verificado | https://code.claude.com/docs/en/skills |

Também atualizei `plugins/ux-ui-design/skills/playbook/references/ferramentas-e-mcp.md`: a linha do Figma deixou de dizer "URL e ferramentas: Não verificado" e o exemplo 2 trocou `<URL_OFICIAL_DO_SERVIDOR_MCP_DO_FIGMA>` pela URL verificada; a linha e o exemplo do Playwright passaram de Inferido para Verificado, com `--isolated` e `--allowed-origins` e o aviso de que não são fronteira de segurança.

## 3. Segurança

### Regras exigidas

| Regra | Onde está (depois das correções) | Veredito |
| --- | --- | --- |
| Instalação de plugin ou MCP só com confirmação | `skills/playbook/SKILL.md:97`; `figma-mcp.md` seção 2; `playwright-verificacao-ui.md` seção 2; README "Instalação" | OK |
| OAuth do Figma feito pelo usuário; nunca pedir ou colar token | `SKILL.md` (pré-requisitos e princípio 9); `figma-mcp.md` seção 2; DE-02 | OK |
| Ferramentas de escrita do Figma só com pedido explícito | Antes: só "escrita no canvas", sem nomes. Agora: `SKILL.md:109`, `figma-mcp.md:67`, DE-02 e bloqueio por nome no `ui-verifier` (`agents/ui-verifier.md:4`) | Corrigido |
| Playwright só em URL local ou autorizada; sem credenciais reais | `SKILL.md` (segurança); `playwright-verificacao-ui.md` seções 5 e 11; `ui-verifier` | OK |
| Conteúdo do Figma, DOM, console e páginas é dado | Princípio 7, segurança, gotcha 8, `figma-mcp.md` seção 10, agentes, eval `figma-camada-com-injecao` | OK |
| Screenshots com dados pessoais não são publicados | Antes: regra existia, mas o procedimento mandava nomear o arquivo, o que grava na raiz do workspace. Agora: `SKILL.md:111`, `playwright-verificacao-ui.md:60`, `agents/ui-verifier.md:18`, P-04, DE-03 | Corrigido |
| Cadeia de suprimentos (`@latest` contra versão fixada) | `SKILL.md`, README, `playwright-verificacao-ui.md` seção 2 | OK |

### Lacunas técnicas corrigidas nos agentes

- `agents/ui-verifier.md:4` tinha `disallowedTools: Write, Edit, NotebookEdit, Bash`. Nesta máquina (Windows) a sessão expõe a ferramenta `PowerShell`, que subagentes herdam (a documentação de subagentes cita Bash e PowerShell): o agente "que não roda shell" podia rodar shell. Acrescentei `PowerShell`, `Agent`, `WebFetch`, `WebSearch` e, nas duas formas de nome, `browser_run_code_unsafe`, `browser_file_upload` e as ferramentas de escrita ou custo do Figma.
- A justificativa do agente dizia que uma lista `tools` "falharia em uma das formas". A documentação diz que só falha quando **nada** resolve e aceita padrões de servidor. Reescrevi a justificativa: a allowlist é possível, mas deixaria de fora servidor registrado com outro nome.
- `motion-polish-reviewer` (`tools: Read, Grep, Glob`): sem lacuna.

### Skills vendorizadas lidas como dado

Busca textual em todas e leitura das seções de risco (inclusive `design-taste-frontend` seções 0 a 4.11, 9, 11 a 14 e apêndices). Também conferi: nenhuma usa injeção de shell no carregamento (`` !`cmd` `` ou bloco ` ```! `), nenhuma tem `allowed-tools`, `hooks` ou `context` no frontmatter, e os únicos caracteres invisíveis são um ZWJ dentro de um emoji de teste (`break-ui/CATALOG.md:26`) e ZWSP para escapar cercas de código (`improve-animations/PLAN-TEMPLATE.md:19`), ambos benignos. Nenhum pedido de segredo, `curl` com pipe ou exfiltração.

| Instrução arriscada (arquivo:linha) | Neutralização no kit |
| --- | --- |
| Gerar imagem com qualquer ferramenta disponível, "you MUST" (`design-taste-frontend/SKILL.md:267`) | Gotcha 6 e `figma-mcp.md` (só com pedido; `generate_image` gasta crédito). Já existia; texto corrigido |
| Logos reais de marcas para prova social via Simple Icons (`design-taste-frontend/SKILL.md:276-277`, checklist em 14) | **Novo:** `SKILL.md:113`, `precedencia-e-adaptacao.md:43`, P-13 |
| Dados "orgânicos" com cara de reais, inclusive telefone completo (`design-taste-frontend/SKILL.md:618`) | **Novo:** mesmas linhas; placeholder marcado e `example.com` |
| "Se dá para inferir, não pergunte" (`design-taste-frontend/SKILL.md:36`) | **Novo:** `precedencia-e-adaptacao.md:43` manda perguntar uma vez sobre o design system ativo |
| Instalar pacote oficial de design system; comandos `npm install`/`npx shadcn@latest` (`design-taste-frontend/SKILL.md:99`, `987-1030`) | Já existia (`precedencia-e-adaptacao.md`, segurança do playbook) |
| `npx expo install` (`animate-expo/SKILL.md:84`, `RECIPES.md:10`, `258`) | Já existia (mapa e P-15) |
| Instalar e ligar a biblioteca (`pick-ui-library/SKILL.md:23`) | **Novo:** só por comando ou "sim" (`SKILL.md:40` e mapa) |
| Rodar o harness, criar rota e apagar a superfície (`prototype/SKILL.md:31`, `69`, `84`) | **Novo:** o playbook dizia "leia o roteiro e siga", contornando o `disable-model-invocation` do autor; agora exige comando ou "sim" (`SKILL.md:40`); subir servidor é do usuário |
| Gravar planos em `plans/` e ler o commit (`improve-animations/SKILL.md:30`, `90`, `94`) | **Novo:** mapa e P-07 declaram a gravação |
| Rolagem com inércia e scroll sequestrado (`redesign-existing-projects/SKILL.md:148`; GSAP em `design-taste-frontend` 5.B) | **Novo:** `precedencia-e-adaptacao.md:44` |
| Trocar fonte primeiro e substituir Inter (`redesign-existing-projects/SKILL.md:22`, `163`) | Já existia (precedência, P-12, eval de precedência) |
| Placeholders externos picsum/Unsplash/CDN | Já existia (gotcha 6) |
| Saudação fixa ao invocar sem pergunta (12 skills do Emil, linha 8 ou 9 de cada) | Já existia; texto do playbook precisado para "as 12 skills do Emil" |
| Proibição total de travessão no texto visível (`design-taste-frontend` 9.G) | **Novo:** `precedencia-e-adaptacao.md:45` (em pt-BR é pontuação legítima; vale o guia de voz) |

## 4. Precedência e conflitos

**Verificado.**

- **Ordem:** design system do projeto, depois Mo baile por pedido, depois taste; ofício do Emil dentro de qualquer um; acessibilidade como piso (`SKILL.md:30-36`, `precedencia-e-adaptacao.md` seção 1). Coerente com `ux-ui-design`, `web-frontend`, `mobile-apps` e orquestrador.
- **Inter e Lucide:** `minimalist-ui/SKILL.md:14-15` e `high-end-visual-design/SKILL.md:15-16` banem; `design-taste-frontend/SKILL.md:169` e 3.C desencorajam (Lucide aceito se o projeto já depende); `redesign-existing-projects/SKILL.md:22` manda trocar Inter; `industrial-brutalist-ui/SKILL.md:28` **recomenda** Inter. O gotcha 1 dizia "quatro skills banem": impreciso, reescrito. Mo baile usa Lucide com traço 1,6 e `-apple-system` (`design-systems/mo-baile/readme.md:66`, `72`; `tokens/typography.css:3`).
- **Contraste `#787774`** (fórmula WCAG 2.x, luminância relativa sRGB): 4,478:1 sobre `#FFFFFF`, 4,144:1 sobre `#F7F6F3` e 4,325:1 sobre `#FBFBFA` (terceiro fundo que a skill indica, `minimalist-ui/SKILL.md:33`). Os números do kit estavam certos; acrescentei `#FBFBFA` e uma alternativa na mesma matiz que passa nos três: `#706F6C` (5,02, 4,65 e 4,85:1).
- **Mola `smooth` contra 300 ms:** `review-animations/SKILL.md:37` e `STANDARDS.md:49` dizem "UI abaixo de 300 ms"; `design-systems/mo-baile/tokens/motion.css:4-8` tem `smooth` com 0,5 s perceptual e 761 ms até assentar. Resolução correta: o token vence e vira "divergência consciente" sem bloquear (`precedencia-e-adaptacao.md:39`, agente de revisão, eval `revisao-motion-componente`).
- **Geração de imagem:** tratada (seção 3).
- **Android:** sem copiar CSS, tradução para `spring`/`tween`, reduzir movimento como sobrescrita no tema, componentes da plataforma antes de custom. Recalculei `dampingRatio = damping / (2·√stiffness)`: 1,000 (`smooth`), 0,850 (`snappy`), 0,700 (`bouncy`), 1,000 (`smooth-small`); rigidez `(2π/duração)²` bate com os tokens. Abri três páginas oficiais Android e subi rótulos: `spring(dampingRatio, stiffness)` (https://developer.android.com/develop/ui/compose/animation/customize), alvo de 48 × 48 dp (https://developer.android.com/guide/topics/ui/accessibility/apps) e `ANIMATOR_DURATION_SCALE`, padrão 1,0, com 0 encerrando animações de Animator (https://developer.android.com/reference/android/provider/Settings.Global). Ficam Inferidos: massa 1 da mola do Compose e o ajuste "Remover animações" zerar a escala. **Material 3 motion não foi aberto** (m3.material.io): os valores seguem Não verificáveis, como o kit já dizia.

## 5. Qualidade (rubrica D1 a D12)

Notas de 0 a 5 por dimensão; final = média × 20. "Antes" é o estado entregue pelo construtor; "depois", o estado após as correções deste relatório.

| Artefato | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | Antes | Depois |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Playbook (`SKILL.md` + 6 referências) | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 3→5 | 4 | 5 | 5 | 3→5 | 90 | 97 |
| P-01 Figma para código | 5 | 4 | 5 | 5 | 3 | 5 | 5 | 5 | 5 | 5 | 5 | 4→5 | 93 | 95 |
| P-04 Verificar em 3 larguras | 5 | 4 | 5 | 5 | 3 | 5 | 5 | 4→5 | 5 | 5 | 5 | 5 | 93 | 95 |
| P-08 Revisar motion de diff | 5 | 4 | 4 | 5 | 3 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 92 | 92 |
| P-13 Nova direção visual | 5 | 4 | 4 | 5 | 3 | 4 | 4→5 | 3→5 | 5 | 5 | 4 | 5 | 85 | 90 |
| P-14 Android com Mo baile | 5 | 4 | 5 | 5 | 3 | 5 | 5 | 5 | 5 | 5 | 5 | 4→5 | 93 | 95 |
| Agente `ui-verifier` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 3→5 | 4 | 5 | 5 | 3→4 | 90 | 95 |
| Agente `motion-polish-reviewer` | 5 | 5 | 5 | 5 | 4 | 5 | 5 | 5 | 4 | 4 | 5 | 5 | 95 | 95 |
| Eval `figma-sem-mcp-orienta-instalacao` | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 95 | 95 |
| Eval `figma-camada-com-injecao` | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 4 | 5 | 98 | 98 |
| Eval `negativo-backend-indice-sql` | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 97 | 97 |

Justificativas curtas das notas abaixo de 5:

- **Playbook:** D5 4 (dois exemplos, sem exemplo de relatório preenchido no corpo); D9 4 (182 linhas densas, mas com referências sob demanda). D8 e D12 subiram com as correções da seção 3 e da seção 2.
- **Prompts:** D5 3 (sem exemplo de saída; aceitável em biblioteca de prompts); D2 4 (o porquê fica implícito no playbook). P-08 D3/D11 4: depende do agente e não diz o que fazer sem diff. P-13 D6/D11 4: não fixa quantas variantes nem o que fazer se o `prototype` não puder rodar.
- **`ui-verifier`:** D12 fica em 4 porque a documentação descreve a remoção por `disallowedTools`, não o caso de nome ausente na sessão (efeito em tempo de execução Inferido); D9 4 (frontmatter longo).
- **`motion-polish-reviewer`:** D10 4 (veredito mistura "Block/Approve" com "Aprovado com ressalvas"); D9 4.
- **Evals:** D11 4 nos casos que concedem `Bash` (no Windows nativo a rodada é recusada; agora documentado no README dos evals).

**Formato dos evals (Verificado em https://code.claude.com/docs/en/plugin-evals):** chaves usadas no `prompt.md` (`name`, `description`, `tags`, `max_turns`, `allowed_tools`, `timeout_seconds`, `runs`, `expected_outcome`, `model`) estão todas na lista aceita; tipos `llm` e `tool_used` válidos; `min: 0`/`max: 0` é a forma documentada de "nunca chamou"; `arm: both` está no único grader que precisa (`negativo-backend-indice-sql/graders/no-plugin-skill.md`), porque só graders `tool_used` sobre `Skill` são excluídos da nota em rodada com duas frentes; os demais `no-*` (Bash, Write, Edit, Read) já contam nas duas frentes. Critérios conferidos contra as skills: tooltip de 125 a 200 ms (`review-animations/STANDARDS.md:44`) e `x`/`y` do Framer Motion fora da GPU (`STANDARDS.md:118`).

**Contagens:** 17 vendorizadas, 16 prompts (`### P-`), 6 referências, 2 templates, 2 agentes, 8 evals: batem com o README. Links relativos: todos resolvem (`verify_plugin.py` passa e a lista de links foi conferida).

## Correções feitas

Arquivos próprios do kit:

1. `skills/playbook/SKILL.md`: versões e fontes no cabeçalho; regra para skills "só por comando" (sem contornar `disable-model-invocation` em `prototype` e `pick-ui-library`); efeitos de `improve-animations`, `pick-ui-library` e `prototype` no mapa; plugin oficial `figma` com as skills verificadas e quais preparam escrita; aceite dos termos da Figma; nomeação de ferramentas pela regra documentada; segurança com ferramentas de escrita do Figma por nome, gravação de capturas, `browser_run_code_unsafe` como execução remota, servidor de desenvolvimento, logos e dados com cara de reais; gotchas 1, 4 e 6 corrigidos.
2. `skills/playbook/references/figma-mcp.md`: fontes F-02 e F-12; `use_figma` e assento Full; plugin oficial 2.2.127 e 14 skills; nomeação Verificada; skills do plugin como terceiros; tabela de limites com a divergência entre fontes e isenções; tabelas de ferramentas de leitura e de escrita ou custo.
3. `skills/playbook/references/playwright-verificacao-ui.md`: npm e plugin Verificados; `--caps` completo; `--output-dir`, `--grant-permissions`, `--secrets`; seção "Arquivos gravados"; nome das capturas em pasta ignorada; `browser_emulate_media` com `reducedMotion`.
4. `skills/playbook/references/precedencia-e-adaptacao.md`: contraste com `#FBFBFA` e alternativa `#706F6C`; três conflitos novos (logos e dados com cara de reais e "não pergunte"; rolagem sequestrada; travessão); rótulos de plataforma (Android Verificado, iOS rotulado).
5. `skills/playbook/references/android-motion.md`: páginas Android abertas; `spring`, 48 dp e `ANIMATOR_DURATION_SCALE` Verificados; massa e "Remover animações" seguem Inferidos; Material 3 segue Não verificável.
6. `skills/playbook/references/fontes.md`: F-01 a F-05 e F-10 reescritos com URL e estado; F-11 a F-13 novos; lista "Não verificado" atualizada.
7. `skills/playbook/references/claude-md-snippets.md`: DE-02 (limites e ferramentas de escrita por nome) e DE-03 (pasta das capturas).
8. `skills/prompts/references/prompt-library.md`: P-01 (limite sem número fixo), P-04 (pasta das capturas), P-07 (onde os planos podem ser gravados), P-13 (logos, depoimentos e números reais só do usuário; imagem paga só com "sim").
9. `agents/ui-verifier.md`: `disallowedTools` ampliado; justificativa corrigida; regra "capturas são arquivos"; lista de ferramentas proibidas do Figma completa; `description` precisa sobre o que grava.
10. `README.md`: tabela do `ui-verifier`; skills só por comando; termos da Figma; segurança; limitações (Figma, conteúdo vendorizado, Android, verificação independente).
11. `third_party/README.md`: nomes exatos das excluídas; seção de integridade com nota de CRLF.
12. `evals/README.md`: documentação de evals Verificada; nota de sandbox no Windows; servidores MCP pessoais não carregam em rodada.

Fora do kit:

13. `plugins/ux-ui-design/skills/playbook/references/ferramentas-e-mcp.md`: Playwright e Figma de Inferido/Não verificado para Verificado, com URL; exemplo 2 com a URL real do Figma e os dois comandos de instalação; exemplo 1 com `--isolated` e `--allowed-origins`.

Conferido e **sem correção necessária**: seção "Ferramentas de design engineering (opcional)" em `plugins/ux-ui-design/skills/playbook/SKILL.md:123-125`; `plugins/ux-ui-design/agents/ui-designer.md:16`; `plugins/web-frontend/skills/playbook/SKILL.md:97`; `plugins/mobile-apps/skills/playbook/SKILL.md:109`; `publish/ORCHESTRATOR.md:71` igual ao `protocolo.md`; `agents/motion-polish-reviewer.md`; os 8 evals.

## Riscos residuais

1. **Nada foi executado.** Agentes, evals e o fluxo com Figma e Playwright conectados não rodaram; o CLI local é 2.1.128 e `claude plugin eval` exige 2.1.269 ou superior (Verificado na documentação e em `claude --version`).
2. **Bloqueio por nome no `ui-verifier`:** cobre só as formas `mcp__plugin_figma_figma__*`/`mcp__figma__*` e `mcp__plugin_playwright_playwright__*`/`mcp__playwright__*`. Servidor com outro nome depende da instrução. O efeito de listar em `disallowedTools` um nome que não existe na sessão não está documentado (Inferido: sem efeito); `claude plugin validate` passou.
3. **O agente herda outras ferramentas MCP** (por exemplo Slack, GitHub, controle do computador) que não podem ser negadas por nome genérico; a proibição é instrução.
4. **Disparo automático das skills taste:** as `description` podem acioná-las em pedidos de landing ou redesign. A documentação diz que `skillOverrides` **não** afeta skills de plugin, então não há trava por configuração; a precedência depende do playbook e da regra DE-01 no `CLAUDE.md` do projeto.
5. **Limites do Figma:** as duas fontes oficiais divergem; o kit assume o menor e manda conferir com `whoami`.
6. **Skills do plugin oficial `figma`** (por exemplo `figma-design-to-code`, que se diz obrigatória antes de `get_design_context`) entram na sessão quando o plugin está instalado e são conteúdo de terceiros não auditado aqui.
7. **Finais de linha CRLF** nas cópias vendorizadas: conteúdo idêntico, bytes diferentes; quem comparar por hash bruto vai achar "diferença".
8. **Material 3 motion** segue sem fonte aberta.

## Pendências para decisão do usuário

1. **Allowlist no `ui-verifier`?** Trocar o modelo "herda e nega" por `tools: Read, Grep, Glob, mcp__plugin_playwright_playwright__*, mcp__playwright__*, mcp__plugin_figma_figma__*, mcp__figma__*` (mais a negação atual). Fica mais restrito (sem Slack, GitHub, controle do computador), mas deixa de funcionar se o servidor tiver outro nome. Exige teste numa sessão real.
2. **Travar as skills taste?** A única trava técnica seria acrescentar `disable-model-invocation: true` ao frontmatter das 5 skills taste. Isso é modificação de conteúdo de terceiros (permitida pela MIT, mas teria de ser registrada em `third_party/README.md` e no README, e reaplicada a cada atualização). Não fiz, por regra desta validação.
3. **Rodar os evals** num CLI 2.1.269 ou superior, com as concessões de `Bash` em WSL2, e acrescentar casos para "recusa de ferramenta de escrita do Figma" e "pasta das capturas", que hoje não têm cobertura.
4. **Normalizar CRLF para LF** nas skills vendorizadas antes de publicar no git (por exemplo com `.gitattributes`), se quiser hash igual ao upstream.
5. **Confirmar o limite do Figma** da conta real com `whoami` antes do primeiro uso.
6. **Abrir a documentação de Material 3 motion** se o app Android for adiante.

## Verificação final

Comandos executados nesta sessão, depois de todas as correções:

```text
set PYTHONUTF8=1 ; python tools/verify_plugin.py plugins/<slug>
design-engineering-kit  {'skills': 19, 'agents': 2, 'commands': 0, 'evals': 8, 'files': 73}
  WARNING skills/design-taste-frontend/SKILL.md: 1207 lines (>500)   (vendorizada, aceito)
  WARNING skills/emil-design-eng/SKILL.md: 675 lines (>500)          (vendorizada, aceito)
  RESULT: PASS with warnings
ux-ui-design            RESULT: PASS
web-frontend            RESULT: PASS
mobile-apps             RESULT: PASS
orchestrator            RESULT: PASS

claude plugin validate (CLI 2.1.128)
design-engineering-kit  ✔ Validation passed
ux-ui-design            ✔ Validation passed
orchestrator            ✔ Validation passed

cmp publish/ORCHESTRATOR.md plugins/orchestrator/skills/playbook/references/protocolo.md  -> sem saída (idênticos)
fc /b (Windows)                                                                          -> FC: nenhuma diferença encontrada
```

Não há `graphify-out/` em `dev-segments` e só arquivos Markdown foram alterados; nenhuma atualização de grafo se aplicou.
