# CLI, desktop e ferramentas de desenvolvedor — VALIDADO (consolidado das 3 lentes)

Data: 2026-10-10 · Validador: claude-sonnet-5-5 (modelo diferente dos pesquisadores, claude-haiku-5-5; a independência é de modelo e de sessão, não de ferramenta: usei as mesmas ferramentas WebFetch/API que eles) · Escopo: segmento `cli-desktop-tooling`

## Estatísticas

| Lente | Recebidos | Aprovados (A/B, fundidos em V-xx) | Rebaixados (C ou redundante) | Rejeitados |
| --- | --- | --- | --- | --- |
| authoritative | 25 | 24 | 0 | 1 |
| github | 20 | 17 | 1 | 2 |
| community | 24 | 16 | 7 | 1 |
| **Total** | **69** | **57** | **8** | **4** |

**Rodada de complemento (gapfill, validada em 2026-10-10 por claude-sonnet-5-5, sessão independente do pesquisador claude-haiku-5-5):**

| Lente | Recebidos | Aprovados (A/B, fundidos em V-xx) | Rebaixados | Rejeitados | Itens novos do validador |
| --- | --- | --- | --- | --- | --- |
| gapfill (43 itens R-gap-01 a R-gap-43 mais 5 linhas de rejeitados) | 48 | 42 itens R-gap em 35 itens V | 1 (R-gap-40, ver "Rejeitados") | 5 (steipete e 4 linhas do HN, já rejeitados pelo pesquisador e mantidos) | 3 (V-42 WiX, V-64 guidelines do Azure CLI, V-65 DoltHub/HN) |

- **Total acumulado: 67 itens V** (V-01 a V-67): **39 de classe A e 28 de classe B**. A rodada de complemento acrescentou **38 itens V** (V-30 a V-67): 23 A e 15 B.
- Re-verificação do complemento: **todos os 43 itens R-gap foram reabertos com ferramenta** (100% contra a meta de 40%; todos os classe A e todo conteúdo reaproveitável como regra ou prompt incluídos), com cerca de **100 URLs/páginas distintas** abertas (páginas oficiais, arquivos brutos, metadados de repositórios pela API de busca do GitHub, itens do HN, arquivos de licença). Pontuação média de prompt dos 37 itens V reutilizáveis do complemento (conteúdo já reescrito): **82,2** (faixa 70–88). Pontuação dos **prompts-fonte** efetivamente lidos (agentes e skills): média 66,9 (faixa ≤40 a 85): `plugin-validator` 75, `skill-reviewer` 73, `claude-automation-recommender` 70, `build-mcp-server` 85 (provisório), `skill-based-architecture` 72, `powershell-5.1-expert` 53, `cli-developer` ≤40 (reprovação automática por métricas inventadas).
- **Correções materiais feitas ao pesquisador** (detalhe nos itens): `OnlyLoadAppFromAsar` deve ficar **ligado** (V-48); os papéis de D8 e D10 estavam trocados (V-56); `plugin-dev` tem README dizendo MIT mas `LICENSE` Apache-2.0 (V-54); MAUI não é "excluído" do MVVM Toolkit (V-34); `set -euo pipefail` não é do guia do Google (V-62); `set -e` aparece no POSIX (V-63); licenças verificadas: Ratatui MIT, Sparkle MIT, Pester Apache-2.0, MVVM Toolkit MIT (V-31, V-49, V-58, V-34); 14 módulos Qt só-GPL, não 6 (V-39); `__TAURI_ISOLATION_HOOK__` só em exemplo (V-47); `-ErrorAction Stop` escalando para o `catch` agora Verificado (V-59).
- **Conflito EV versus OV resolvido** com a documentação da Microsoft (V-44): "EV obrigatório desde 2023" está **refutado**; V-17 e V-21 receberam nota de correção.
- Itens aprovados consolidados e deduplicados entre lentes (primeira rodada): **29 itens V** (V-01 a V-29). Muitos itens das três lentes cobriam a mesma fonte (por exemplo, a página de segurança do Electron aparece nas três); foram fundidos.
- Fontes re-verificadas nesta rodada: **49** fontes distintas (páginas oficiais, repositórios, blogs, itens do HN e o arquivo local do gstack), mais metadados de 12 repositórios pela API de busca do GitHub. Isso cobre cerca de 90% das fontes distintas das três lentes e todos os itens classe A (meta: 40%).
- Pontuação média de prompt (D1–D12, conteúdo reutilizável já reescrito): **82,2**. Faixa 76–88. Nenhum critério de reprovação automática disparou no conteúdo reescrito.
- Veredito da primeira rodada: **needs_more** (quatro subtemas sem cobertura). **Veredito da rodada final (complemento): `pass_with_gaps`.** Os quatro subtemas sem cobertura (TUI, .NET desktop, Qt, empacotamento e instaladores Windows) agora têm itens A ou B, e assinatura, PowerShell avançado, shell POSIX/bash, segurança de desktop e as páginas do Claude Code foram fechadas. Restam lacunas objetivas que dependem de ferramentas que não estiveram disponíveis (**WebSearch bloqueado de novo pelo limite de 200 chamadas por turno, o que impede a comunidade em Reddit, X e YouTube**) ou de páginas que não retornaram corpo: ver "Lacunas (objetivas e pesquisáveis)".

### Método e limites desta validação

- Re-verifiquei com ferramentas: existência da URL, conteúdo contra a afirmação, estrelas/licença/data de push (API de busca do GitHub: a API `repos/` deu rate limit para este IP, mas `search/repositories?q=repo:<owner>/<repo>` respondeu), versões e campos técnicos.
- Rótulos: **Verificado** = conferi nesta rodada com ferramenta. **Inferido** = conclusão minha a partir de fontes. **Não verificado** = não consegui conferir. Onde o pesquisador afirmou algo que não bate, o item traz **Correção**.
- Não verifiquei: scripts de hook do Trail of Bits, conteúdo do centminmod, `plan-devex-review` do gstack, `electron-pro.md` do VoltAgent, o comportamento prático de qualquer comando (nenhum comando de CLI foi executado, apenas leitura de documentação). Na rodada de complemento: os corpos de agentes e skills foram lidos por **resumo estruturado** da ferramenta de leitura (WebFetch), não por texto integral; as pontuações desses prompts-fonte são provisórias (±5). Páginas longas foram lidas por trecho ou busca de termos no texto salvo, e cada item diz o que ficou de fora. A API `repos/` e `git/trees` do GitHub deram 403 e o `gh` não está autenticado; usei `search/repositories?q=repo:...`.
- Direitos autorais: todo conteúdo reutilizável abaixo é destilação com redação própria. Nenhum trecho literal de fonte sem licença permissiva foi mantido. Onde a fonte é permissiva (MIT/Apache), ainda assim não copiei texto literal; só o template de 6 linhas de `anthropics/skills` foi descrito, não reproduzido.
- Segurança: nenhum código de terceiros foi baixado ou executado. Os exemplos de script abaixo são de minha autoria e **não foram executados**.

---

## Itens aprovados

### V-01 — Estrutura de plugin do Claude Code e layout de marketplace (origem R-authoritative-01, R-authoritative-20, R-github-17, R-community-21) — Classe A (9) · Prompt-score 86
- **Lente:** authoritative + github + community (fundido)
- **Tipo:** reference + checklist
- **Fonte:** https://code.claude.com/docs/en/plugins · https://code.claude.com/docs/en/plugins-reference · https://github.com/anthropics/claude-plugins-official · **Autor/Org:** Anthropic
- **Sinais:** repositório `anthropics/claude-plugins-official`: 37.606★, Apache-2.0, `pushed_at` 2026-10-09 (Verificado pela API de busca). Documentação atual, com versões mínimas citadas no texto (v2.1.2xx). Licença do texto das docs não declarada (destilar).
- **Para que serve no segmento:** montar `plugins/<slug>/` da fábrica dev-segments, decidir plugin versus skill avulsa e nomear com segurança.
- **Técnicas-chave (Verificado):**
  - O manifesto `.claude-plugin/plugin.json` é **opcional** segundo a referência: sem ele o Claude Code carrega os componentes do layout padrão e o nome vem do marketplace ou da pasta. Só `name` é obrigatório quando o manifesto existe.
  - Layout padrão: `skills/<nome>/SKILL.md`, `commands/` (a doc recomenda `skills/` para plugins novos), `agents/`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `bin/`, `monitors/`, `settings.json`.
  - `claude plugin validate ./meu-plugin` é a checagem oficial do manifesto; `--strict` transforma avisos em falha (útil em CI).
  - Caminhos no manifesto começam com `./`, devem existir e ficar dentro da raiz do plugin.
  - Um `CLAUDE.md` na raiz do plugin **não é carregado** como contexto (o validador avisa). Instruções que devem entrar no contexto vão em skill.
  - `${CLAUDE_PLUGIN_ROOT}` muda a cada atualização (não gravar estado ali); `${CLAUDE_PLUGIN_DATA}` aponta para `~/.claude/plugins/data/<id>/`, persiste entre atualizações e, por padrão, é apagado quando o plugin é desinstalado do último escopo.
  - Nome de plugin: kebab-case; `claude plugin validate` dá **erro** para nomes que começam com `claude-`, `anthropic-`, `anthropics-` ou `cc-plugin-`, e para `claude`, `anthropic`, `claude-code` etc.
  - Skills do plugin ganham o prefixo `<plugin>:<skill>`. `version` no manifesto fixa o plugin naquela versão até mudar.
  - Escopos de instalação: usuário, projeto (via `.claude/settings.json` versionado) e local. Para desenvolver sem marketplace: `--plugin-dir`.
  - Nome e descrição de cada skill/agente invocável entram no contexto em todo turno (custo mesmo sem uso).
  - Repositório oficial: o nome de marketplace é permanente (usar `displayName` para rótulo, `renames` se for inevitável) e existe o aviso de que a Anthropic não controla plugins de terceiros (declarado pelos pesquisadores; o aviso literal de confiança está na página de segurança, Verificado).
- **Conteúdo reutilizável (destilação própria):**
  - Checklist de estrutura: (1) nome kebab-case sem prefixos reservados; (2) `plugin.json` presente mesmo sendo opcional, com `description`, `version`, `author`; (3) uma pasta por componente; (4) `claude plugin validate --strict` limpo; (5) descrições curtas (custo de contexto por turno); (6) estado em `${CLAUDE_PLUGIN_DATA}`, nunca na pasta do plugin; (7) sem `hooks/`, `.mcp.json` ou `bin/` ativos na base dev-segments sem revisão (ver V-02); (8) nenhum `CLAUDE.md` na raiz esperando ser lido.
  - Regra de decisão: plugin só quando houver mais de uma peça a distribuir (skills, agentes, hooks, MCP); uma peça só vira skill ou agente avulso.
- **Ressalvas:** **Correção:** os pesquisadores diziam que o repositório oficial trata `plugin.json` como obrigatório. A referência oficial atual diz que é opcional. Esse ponto do README do repositório **não** foi reverificado por mim; adote sempre o manifesto por prudência. As pastas `plugin-dev`, `claude-code-setup`, `mcp-server-dev` e `skill-creator`, que estavam como "não confirmadas", **existem** (Verificado na listagem de `plugins/`, 40 pastas, possivelmente incompleta). O conteúdo foi lido na rodada de complemento (V-54, V-55). A licença do repositório é Apache-2.0 (confirmada no arquivo `LICENSE`, inclusive na pasta `plugin-dev`, apesar de o README dessa pasta dizer MIT). Campos de manifesto mudam com a versão: conferir `claude --version` e a página.
- **Verificação:** WebFetch das páginas `plugins`, `plugins-reference` e `plugins/security`; API de busca do GitHub para estrelas/licença/push; WebFetch da listagem `plugins/` do repositório.

### V-02 — Revisão de segurança antes de habilitar um plugin (origem R-authoritative-02) — Classe A (9) · Prompt-score 88
- **Lente:** authoritative
- **Tipo:** checklist
- **Fonte:** https://code.claude.com/docs/en/plugins/security · **Autor/Org:** Anthropic
- **Sinais:** página oficial existente e atual (Verificado). Licença do texto não declarada (destilar).
- **Para que serve no segmento:** revisar qualquer plugin (inclusive os gerados pela fábrica) antes de publicar ou habilitar; fundamenta a regra "sem hooks que executem shell, sem `.mcp.json` ativo e sem `bin/`" da base.
- **Técnicas-chave (Verificado):**
  - Um plugin instalado pode executar código com os privilégios do usuário. Hooks e monitores rodam como comandos de shell; servidores MCP/LSP são processos locais; `bin/` entra no `PATH` da ferramenta Bash; skills, comandos e agentes entram no contexto como instruções.
  - Permissões e sandbox do Claude Code cobrem as chamadas feitas por Claude, **não** o que hooks, monitores, servidores MCP/LSP e mods executam por conta própria (rodam fora do sandbox).
  - Atualização automática pode mudar arquivos já revisados.
  - Nomes de marketplace "oficiais" e "community" só são aceitos se a origem for `github.com/anthropics/`; qualquer outro marketplace é de terceiros.
  - Comandos: `claude plugin marketplace list` (origem), painel `/plugin` (seção "Will install"), `claude --plugin-dir <pasta> plugin details <nome>` (inventário sem abrir sessão), `claude plugin details <nome>` (cópia instalada, em `~/.claude/plugins/cache/<marketplace>/<plugin>/<versão>/`), `claude plugin uninstall <plugin> --scope ...`.
- **Conteúdo reutilizável (destilação própria):**
  - Checklist de revisão: (a) origem do marketplace; (b) ler `hooks/hooks.json` e o script de cada hook (o painel só mostra que existe hook, não o que roda); (c) ler `.mcp.json` e a origem de cada servidor; (d) listar tudo em `bin/`; (e) listar também monitores e mods; (f) rodar o inventário `plugin details`; (g) decidir se a atualização automática fica ligada.
  - Checklist de remoção: desinstalar no escopo certo; lembrar que o diretório de dados persistente some por padrão (usar a opção de manter dados se precisar); o cache fica 14 dias em `~/.claude/plugins/cache/` e pode ser apagado à mão; remover o marketplace se não confia no dono.
  - Skill sugerida: `plugin-security-review`, somente leitura, com `disable-model-invocation: true` e `allowed-tools` restrito a leitura.
- **Ressalvas:** os comandos acima não foram executados por mim (só lidos). A lista de "o que um plugin pode fazer" cresce (monitores e mods não estavam no resumo dos pesquisadores).
- **Verificação:** WebFetch completo da página; confrontei cada afirmação do item com o texto. Tudo confere; acrescentei monitores, mods, 14 dias de cache e a exclusão dos dados persistentes.

### V-03 — Formato de SKILL.md e skills de referência da Anthropic (origem R-authoritative-03, R-authoritative-21) — Classe A (9) · Prompt-score 87
- **Lente:** authoritative
- **Tipo:** skill-template + checklist + reference
- **Fonte:** https://code.claude.com/docs/en/skills · https://github.com/anthropics/skills · **Autor/Org:** Anthropic
- **Sinais:** `anthropics/skills`: 180.248★, `pushed_at` 2026-10-09, sem licença raiz detectada pela API; a README declara muitas skills como Apache-2.0 e `docx/pdf/pptx/xlsx` como "source-available, not open source" (Verificado).
- **Para que serve no segmento:** criar as skills da fábrica (revisão de CLI, auditoria Electron/Tauri, checklist de release) com frontmatter correto.
- **Técnicas-chave (Verificado):**
  - Campos de frontmatter existentes na documentação atual: `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility`. Todos opcionais; `description` recomendado.
  - `shell` aceita `bash` (padrão) ou `powershell` (relevante no Windows). `when_to_use` é anexado a `description` e o conjunto é truncado em 1.536 caracteres.
  - `SKILL.md` com menos de 500 linhas; material longo em arquivos de apoio.
  - Portabilidade: ao subir a skill para claude.ai ou para a Skills API, só `name`, `description`, `license`, `compatibility`, `metadata` e `allowed-tools` são aceitos e qualquer outra chave causa erro. Skills de plugin para Claude Code podem usar o conjunto completo.
  - `anthropics/skills` tem `skills/` (19 pastas, incluindo `skill-creator`, `mcp-builder`, `webapp-testing`), `spec/`, `template/` (um `SKILL.md` de poucas linhas, só nome e descrição de exemplo) e `.claude-plugin/`.
- **Conteúdo reutilizável (destilação própria) — template de skill da fábrica:**
  ```
  ---
  name: <verbo-objeto-kebab>
  description: <caso principal primeiro; "Use quando ..." com gatilhos em PT-BR e EN>
  allowed-tools: <o mínimo, ex.: Read Grep Glob>
  disable-model-invocation: true   # só se houver efeito colateral
  shell: powershell                # só se a skill injeta comandos de shell no Windows
  ---
  Objetivo e por quê (1-2 frases).
  Entradas: $ARGUMENTS (o que falta, perguntar).
  Passos: 1) ... 2) ... 3) verificação com saída observável.
  Formato de saída: ...
  Se faltar acesso ou o dado for ambíguo: ...
  Armadilhas (lista viva, só falhas reais).
  Referências: references/<arquivo>.md — ler quando <condição>.
  ```
  - Checklist (minha, baseada na página; **Correção:** o item original dizia "checklist de 9 itens do próprio doc", mas a página não traz checklist formal, apenas os passos de criação e teste): nome kebab-case e igual à pasta; `description` com caso principal no início; frontmatter na linha 1; nomes de campo exatos (grafia errada é ignorada em silêncio); efeito colateral ⇒ `disable-model-invocation: true`; `allowed-tools` mínimo; menos de 500 linhas; cada referência com condição de leitura; testar disparo automático e chamada direta `/nome`, com e sem a skill.
- **Ressalvas:** não copiar as skills `docx/pdf/pptx/xlsx` (source-available). A lista de pastas de `skills/` pode estar truncada. Confirmar a existência do campo na versão instalada (`claude --version`).
- **Verificação:** WebFetch das 100 mil primeiras posições da página `skills` (restaram ~6,6 mil caracteres não lidos); WebFetch do repositório, da pasta `skills/` e do `template/SKILL.md`; API de busca para metadados.

### V-04 — Princípios de skills (Anthropic Engineering) (origem R-authoritative-04) — Classe A (9) · Prompt-score 84
- **Lente:** authoritative
- **Tipo:** checklist
- **Fonte:** https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills · **Autor/Org:** Barry Zhang, Keith Lazuka, Mahesh Murag (Anthropic)
- **Sinais:** publicado em 2025-10-16, com nota de atualização de 2025-12-18 (Skills como padrão aberto) (Verificado). Autoria que os pesquisadores não identificaram.
- **Para que serve no segmento:** decidir o que fica em `SKILL.md`, em `references/` e em scripts.
- **Técnicas-chave (Verificado):** carregamento em três níveis (nome e descrição no prompt do sistema; corpo ao parecer relevante; arquivos ligados sob demanda); scripts como ferramentas determinísticas; deixar claro se um arquivo é para executar ou para ler; avaliar em tarefas representativas e iterar vendo como o agente usa a skill; pedir ao agente que registre acertos e erros; auditar skills de terceiros (arquivos, dependências, instruções que chamam a rede).
- **Conteúdo reutilizável (destilação própria):** roteiro de criação: (1) registrar a tarefa real que falhou sem skill; (2) escrever a skill mínima; (3) mover detalhe para arquivos referenciados; (4) transformar lógica repetível em script e documentar que é "executar, não ler"; (5) observar o disparo e ajustar nome e descrição; (6) registrar armadilhas depois de cada falha real.
- **Ressalvas:** texto de princípios, sem skill completa de exemplo.
- **Verificação:** WebFetch confirmou data, autores e cada ponto.

### V-05 — Lições de Thariq sobre skills (origem R-authoritative-05, R-github-16, R-community-12) — Classe B (7) · Prompt-score 82
- **Lente:** authoritative + github + community (fundido). **Reclassificado:** github tinha C(4); authoritative, B(7); community, B(6). Fico com B(7) pelos motivos abaixo.
- **Tipo:** checklist (dicas)
- **Fonte:** https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/main/tips/claude-thariq-tips-17-mar-26.md · **Autor/Org:** Thariq (@trq212), título "Lessons from Building Claude Code: How We Use Skills", data 2026-03-17 (Verificado no arquivo); repositório espelho de terceiro
- **Sinais:** espelho `shanraisshan/claude-code-best-practice`: 67.329★, MIT, `pushed_at` 2026-10-10 (Verificado pela API). A autoria vem do próprio arquivo; vínculo do autor com a Anthropic **Inferido** pelo título.
- **Para que serve no segmento:** melhorar skills de plugin com padrões de uso real.
- **Técnicas-chave (Verificado no arquivo):** tipos de skill (referência de biblioteca, verificação de produto, dados, automação, scaffolding, qualidade/revisão, CI/CD, runbooks, infraestrutura); "não dizer o óbvio"; seção de armadilhas (gotchas); sistema de arquivos e divulgação progressiva; evitar engessar o modelo; pensar na configuração (arquivo `config.json`); descrição escrita para o modelo; memória e dados em pasta estável; scripts empacotados; hooks sob demanda.
- **Conteúdo reutilizável (destilação própria):** toda skill da fábrica ganha seção "Armadilhas" começando vazia e crescendo com falhas observadas; estado do plugin em `${CLAUDE_PLUGIN_DATA}`; descrição sempre em forma de gatilho; preferir objetivos e restrições a passos rígidos quando o modelo já sabe o caminho.
- **Ressalvas:** dica de praticante em espelho, mas agora **a variável `${CLAUDE_PLUGIN_DATA}` está confirmada na referência oficial de manifesto** (ver V-01), então a ressalva dos pesquisadores caiu. O espelho tem licença MIT, mas o texto de origem é do autor; seguimos destilando.
- **Verificação:** WebFetch do arquivo bruto (título, data, lista de títulos e dicas); API de busca para o espelho; cruzei `${CLAUDE_PLUGIN_DATA}` com a página `plugins-reference`.

### V-06 — CLAUDE.md, memória automática, regras por caminho e AGENTS.md (origem R-authoritative-06, R-community-01) — Classe A (9) · Prompt-score 87
- **Lente:** authoritative + community (corroboração do blog arps18)
- **Tipo:** claude-md-rule + checklist
- **Fonte:** https://code.claude.com/docs/en/memory · https://code.claude.com/docs/en/best-practices (seção CLAUDE.md) · **Autor/Org:** Anthropic
- **Sinais:** página oficial atual (Verificado, via arquivo salvo e busca por termos). Blog de corroboração: arps18 (Arpan Patel, 2026-05-26), HN 451 pontos e 254 comentários (Verificado pela API Algolia).
- **Para que serve no segmento:** escrever o CLAUDE.md do repositório dev-segments e de projetos de CLI/desktop.
- **Técnicas-chave (Verificado):**
  - Alvo: menos de 200 linhas por CLAUDE.md; mais longo reduz a aderência. A memória automática carrega as primeiras 200 linhas ou 25 KB.
  - Imports `@caminho` são expandidos no início da sessão e **não reduzem** o custo de contexto (apenas organizam).
  - `.claude/rules/*.md` (sem `paths`: carrega no início; com `paths`: só quando Claude usa arquivo que casa). Procedimento de várias etapas vai para skill.
  - CLAUDE.md é contexto, não garantia; para bloquear uma ação sempre, usar hook PreToolUse.
  - Instruções contraditórias: o modelo pode escolher uma ao acaso; revisar periodicamente. `/doctor` propõe cortes de conteúdo dedutível do código.
  - Ênfase ("IMPORTANT") em uma ou duas linhas apenas; ênfase em tudo anula o efeito.
  - `AGENTS.md`: Claude Code lê quando não há CLAUDE.md (exige Claude Code v2.1.277 ou superior); para convivência, um `CLAUDE.md` que importa `AGENTS.md`.
  - Link simbólico de regra ou CLAUDE.md para caminho de rede UNC (`\\servidor\pasta`) **não carrega** (caminhos `\\wsl$` não contam como rede).
- **Conteúdo reutilizável (destilação própria):**
  - Esqueleto: (1) comandos exatos de build/teste/lint com filtro para um teste; (2) convenções que diferem do padrão; (3) fluxo (branch, commit, PR); (4) ambiente (Windows, PowerShell 5.1 ou 7, variáveis obrigatórias); (5) armadilhas conhecidas; (6) ponteiros para docs em vez de cópia.
  - Teste de corte por linha: "remover esta linha faria o modelo errar?". Se não, apagar.
  - Cada comportamento indesejado que se repete vira uma regra curta e imperativa; mover para hook se precisa ser garantido.
- **Ressalvas:** limites numéricos mudam com versões. Os blogs de praticante só repetem a convenção oficial.
- **Verificação:** busca por termos no texto completo salvo da página (linhas sobre 200 linhas/25 KB, UNC, AGENTS.md, imports, rules); WebFetch da página best-practices; API Algolia para os pontos do HN; WebFetch do blog arps18.

### V-07 — Fluxo explorar-planejar-implementar-verificar e revisão adversarial (origem R-authoritative-07, R-github-01) — Classe A (9) · Prompt-score 88
- **Lente:** authoritative + github
- **Tipo:** workflow + checklist + prompt
- **Fonte:** https://code.claude.com/docs/en/best-practices · **Autor/Org:** Anthropic
- **Sinais:** página oficial atual (Verificado, lida por inteiro).
- **Para que serve no segmento:** rotina padrão de qualquer tarefa de CLI ou desktop e base do subagente `diff-gap-reviewer`.
- **Técnicas-chave (Verificado):** dar ao modelo uma verificação executável (teste, build com código de saída, linter, screenshot); evidência em vez de "pronto" (saída do teste, comando e resultado); quatro fases com modo de plano; pular o plano quando a diff cabe em uma frase; depois de duas correções fracassadas, `/clear` e reescrever o prompt; subagentes para investigação; hook para o que deve acontecer sempre; Stop hook como portão determinístico; `/goal` para condição de término na sessão; revisor em contexto novo com a diff e o critério.
- **Conteúdo reutilizável (destilação própria):**
  - Prompt de revisão adversarial: "Revise a diff abaixo contra PLANO.md em um subagente com contexto novo. Confira: (1) cada requisito foi implementado; (2) cada caso de borda listado tem teste; (3) nada fora do escopo mudou. Relate só lacunas que afetam correção ou requisito, cada uma com arquivo:linha, severidade e confiança. Não relate preferências de estilo. Se não houver lacuna, diga isso."
  - Motivo a incluir no prompt: o próprio documento adverte que um revisor pedido para achar lacunas tende a reportar algumas mesmo quando o trabalho está correto, o que leva a excesso de abstração e testes de casos impossíveis. Por isso o filtro "correção ou requisito" é obrigatório.
  - Checklist de fechamento: saída de teste/build anexada; comando executado com seu resultado; screenshot se houver UI; diff revisada por subagente; o que **não** foi verificado declarado.
- **Ressalvas:** **Correção menor:** os comandos `/goal`, `/verify`, `/batch`, `/rewind` existem na versão atual da página (Verificado), mas a lista muda; conferir na versão instalada antes de citar no plugin.
- **Verificação:** WebFetch integral e conferência frase a frase.

### V-08 — Hooks como guardrail: exit 2 e decisão em JSON (origem R-authoritative-08, R-community-11, parte de R-github-10) — Classe A (9) · Prompt-score 85
- **Lente:** authoritative + community + github
- **Tipo:** pattern + reference
- **Fonte:** https://code.claude.com/docs/en/hooks-guide · referência completa em https://code.claude.com/docs/en/hooks · **Autor/Org:** Anthropic
- **Sinais:** guia oficial atual (Verificado por busca de termos no texto completo salvo).
- **Para que serve no segmento:** bloquear comandos perigosos, auditar comandos, portão de testes.
- **Técnicas-chave (Verificado):**
  - Hook `PreToolUse` com matcher `Bash` recebe o evento em JSON no stdin (`tool_input.command`); exit 0 não decide; exit 2 bloqueia e devolve o stderr ao modelo (o destino do stderr varia por evento).
  - Alternativa em JSON: `hookSpecificOutput.permissionDecision` com `allow`, `ask`, `deny` ou `defer`. O campo **precisa estar dentro de `hookSpecificOutput`**; no nível errado o JSON é aceito e o campo é ignorado sem erro. `claude --debug` mostra "unrecognized keys". `defer` só existe no modo `-p`.
  - Vários hooks em paralelo: a decisão mais restritiva vence (`deny`, `defer`, `ask`, `allow`).
  - `PreToolUse` dispara antes de qualquer checagem de modo de permissão, mesmo em `bypassPermissions`: um `deny` bloqueia.
  - Em plugin, hook em forma shell deve citar `${CLAUDE_PLUGIN_ROOT}` entre aspas; existe forma "exec" com `args` e o campo `shell: powershell` para Windows.
- **Conteúdo reutilizável (destilação própria):**
  - Template de guardrail: "PreToolUse, matcher Bash: ler o JSON do stdin; se o comando casar com a lista de proibidos, escrever no stderr o motivo **e a alternativa** e sair com 2; caso contrário, sair com 0."
  - Exemplo próprio em PowerShell (não executado; testar antes de usar):
    ```
    $evento = [Console]::In.ReadToEnd() | ConvertFrom-Json
    $cmd = $evento.tool_input.command
    if ($cmd -match '(?i)Remove-Item\b.*-Recurse.*-Force|\brm\s+-rf\b') {
      [Console]::Error.WriteLine('Bloqueado: remoção recursiva forçada. Use Move-Item para uma pasta .trash/ ou peça confirmação ao usuário.')
      exit 2
    }
    exit 0
    ```
  - Hook de auditoria: gravar `tool_input.command` em um arquivo de log. **Correção:** o guia oficial usa `PostToolUse` para esse registro (o pesquisador de community escreveu PreToolUse). Trocar `jq` por `ConvertFrom-Json` onde `jq` não existir.
  - Regra: guardrail não é fronteira de segurança. A fronteira real é sandbox, deny rules de permissão e ambiente isolado.
- **Ressalvas:** hooks executam com os privilégios do usuário; em plugin só depois da revisão de V-02. Regex de bloqueio sempre tem contornos.
- **Verificação:** busca por `exit 2`, `permissionDecision`, `most restrictive`, `command-log` e `bypassPermissions` no texto completo salvo; WebFetch de `plugins-reference` para as regras de plugin e `shell: powershell`.

### V-09 — `claude -p` em scripts e CI (origem R-authoritative-09) — Classe A (9) · Prompt-score 84
- **Lente:** authoritative
- **Tipo:** workflow + checklist
- **Fonte:** https://code.claude.com/docs/en/headless · **Autor/Org:** Anthropic
- **Sinais:** página oficial atual, com notas de versão (Verificado).
- **Para que serve no segmento:** revisão de diff, migrações em lote e relatórios; ponte entre CLI e Claude.
- **Técnicas-chave (Verificado):** `-p`; exit 0 em sucesso e não zero em falha (erro de flag no stderr; falha dentro da execução vira resultado no stdout); `--output-format json|stream-json` e `--json-schema` (resultado estruturado em `structured_output`); `--allowedTools` com prefixo (`Bash(git diff *)`; o espaço antes do `*` importa); `--permission-mode dontAsk|auto|acceptEdits`; `--permission-prompts none` (exige v2.1.259+); `--bare` ignora hooks, skills, plugins, MCP, memória e CLAUDE.md do host e "será o padrão no futuro"; sem `--bare`, `-p` roda os hooks de `.claude/settings.json` e os servidores de `.mcp.json` do projeto mesmo em pasta não confiável; SIGTERM sai com 143 sem resultado do turno; stdin limitado a 10 MB; `system/init` traz `plugins`, `plugin_errors`, `mcp_servers` e `mcp_server_errors` para falhar cedo em CI.
- **Conteúdo reutilizável (destilação própria):**
  - Checklist de CI: usar `--bare`; passar o contexto necessário por flags; ferramentas mínimas; saída JSON e registro de custo (`total_cost_usd`, estimativa do cliente); falhar o job se `plugin_errors` ou `mcp_server_errors` vier não vazio; tratar 143 como cancelamento.
  - Exemplo: revisar a diff contra `main` canalizando-a por stdin (assim a ferramenta não precisa de permissão de Bash) com `--bare -p "<instrução de revisão enxuta>" --allowedTools "Read" --output-format json`.
- **Ressalvas:** **Omissão corrigida:** em modo `--bare` o Claude Code **não usa o login da assinatura**; é preciso `ANTHROPIC_API_KEY` (ou provedor de nuvem), o que gera cobrança de API. Isso faltava no item original. O exemplo é derivado da doc e não foi executado.
- **Verificação:** WebFetch integral; conferi cada flag e cada limite citado.

### V-10 — AGENTS.md (formato aberto) (origem R-authoritative-10, R-github-08, parte de R-community-22) — Classe B (7) · Prompt-score 80
- **Lente:** authoritative + github + community
- **Tipo:** claude-md-rule (esqueleto portátil)
- **Fonte:** https://agents.md/ · **Autor/Org:** projeto AGENTS.md, descrito como sob a Agentic AI Foundation/Linux Foundation
- **Sinais:** a página declara uso por mais de 60 mil projetos (alegação não confirmada de forma independente); rodapé de copyright "a Series of LF Projects, LLC"; licença do conteúdo não declarada (Verificado). **Reclassificado:** github dava A(8); mantenho B(7) porque a licença não está declarada e o número de uso é autodeclarado.
- **Para que serve no segmento:** gerar um AGENTS.md portátil junto com o CLAUDE.md.
- **Técnicas-chave (Verificado):** Markdown livre; seções sugeridas (visão geral, comandos de build e teste, estilo, testes, segurança; opcionais: commits/PR, armadilhas, deploy); em monorepo, um arquivo por subprojeto e o mais próximo do arquivo editado vence; instrução explícita no chat sobrepõe o arquivo; comandos de teste listados são executados antes de concluir.
- **Conteúdo reutilizável (destilação própria):** esqueleto em PT-BR: Visão geral · Setup (Windows/PowerShell) · Comandos exatos (build, teste completo, teste único, lint) · Estilo · Testes · Segurança (segredos, pastas que não se editam) · PR. Regra: lint e testes antes de commitar, corrigir até passar.
- **Ressalvas:** a relação com o CLAUDE.md está em V-06 (leitura direta exige v2.1.277+). Os exemplos da página são de monorepo pnpm/turbo; adaptar.
- **Verificação:** WebFetch de `agents.md` (mantenedor, contagem alegada, precedência, sobreposição pelo usuário, seções); cruzei com a página de memória do Claude Code.

### V-11 — Escrever ferramentas para agentes e aplicá-las a CLI (origem R-authoritative-11, R-github-02, R-community-14) — Classe A (9) · Prompt-score 86
- **Lente:** authoritative + github + community
- **Tipo:** checklist
- **Fonte:** https://www.anthropic.com/engineering/writing-tools-for-agents · **Autor/Org:** Ken Aizawa com colegas da Anthropic, publicado em 2025-09-11 (Verificado)
- **Sinais:** post oficial de engenharia (Verificado: existência, data, autor).
- **Para que serve no segmento:** desenhar subcomandos, flags, `--help` e erros de CLIs usadas por agentes.
- **Técnicas-chave (Verificado):** poucas ferramentas de alto impacto; nome com prefixo de serviço/recurso, escolhido por avaliação com o modelo-alvo (prefixo versus sufixo muda por modelo); parâmetros sem ambiguidade (`user_id`, não `user`); `response_format` com `concise` e `detailed`; paginação, filtro, intervalo e truncamento com padrões razoáveis; erros acionáveis (problema, correção, exemplo); avaliação com tarefas realistas de vários passos e leitura de transcrições, com conjunto separado para não superajustar. O único padrão numérico citado: o Claude Code limita respostas de ferramenta a 25.000 tokens.
- **Conteúdo reutilizável (destilação própria) — checklist de CLI para agente:**
  - [ ] cada subcomando faz uma coisa, com nome inequívoco
  - [ ] saída padrão curta; `--json` estável; modo `concise`/`detailed`
  - [ ] listas limitadas ou paginadas, com dica de como filtrar
  - [ ] erro diz o que faltou e mostra o uso correto
  - [ ] ação destrutiva exige flag explícita (`--yes`)
  - [ ] testado com uma tarefa real de vários passos, lendo a transcrição
- **Ressalvas:** o texto trata de ferramentas MCP e de funções; aplicar a CLI é **Inferido** (os três pesquisadores marcaram isso). **Correção:** a frase "anotações para ação destrutiva" do item authoritative não foi confirmada na página; não usar como citação.
- **Verificação:** WebFetch com checagem item a item (cinco pontos confirmados, um parcial: truncamento).

### V-12 — CLI pronta para agente (Armin Ronacher) (origem R-authoritative-12, R-github-04, R-community-07) — Classe B (6) · Prompt-score 80
- **Lente:** authoritative + github + community
- **Tipo:** checklist (padrões de prática)
- **Fonte:** https://lucumr.pocoo.org/2025/6/12/agentic-coding/ · **Autor/Org:** Armin Ronacher, 2025-06-12 (Verificado)
- **Sinais:** blog de praticante conhecido; sem licença (destilar); mais de 12 meses (atualidade 0), por isso B(6) e não 7.
- **Para que serve no segmento:** tornar CLIs utilizáveis por agentes.
- **Técnicas-chave (Verificado):** ferramentas rápidas (travar é pior que quebrar); logs informativos e concisos para poupar tokens; erros claros em uso incorreto; pidfile que impede um segundo `make dev` e responde "serviços já rodando"; serviços escrevem log em arquivo que o agente lê (`make tail-log`); críticos em `Makefile`; prefere `psql` a um servidor MCP de banco; MCP só onde as alternativas são pouco confiáveis.
- **Conteúdo reutilizável (destilação própria):** sem prompt interativo quando não há TTY; saída curta com botão de verbosidade; bloqueio de execução duplicada (pidfile ou lock); log em caminho fixo e documentado no CLAUDE.md; erro com a correção; CLI simples antes de MCP.
- **Ressalvas:** **Correção:** o post **não** trata de timeouts e **não** diz onde fica o arquivo de log nem que o caminho deve ser documentado (Verificado: negado). "Timeout padrão" e "log em `./logs/<comando>.log`" do item original são **Inferido**/sugestão da fábrica, não do autor.
- **Verificação:** WebFetch com oito afirmações conferidas (cinco confirmadas, uma parcial, duas negadas).

### V-13 — Command Line Interface Guidelines (clig.dev) (origem R-authoritative-13, R-github-03) — Classe B (7) · Prompt-score 82
- **Lente:** authoritative + github
- **Tipo:** checklist + reference
- **Fonte:** https://clig.dev/ · **Autor/Org:** Aanand Prasad, Ben Firshman, Carl Tashian, Eva Parish; design de Mark Hurrell (Verificado na página; os pesquisadores marcaram autoria como "não verificável")
- **Sinais:** página sem data e sem licença declarada, descrita como projeto aberto com repositório (Verificado). Referência amplamente citada; popularidade do repositório **não verificada** por mim.
- **Para que serve no segmento:** referência de design para toda CLI e para os scripts da fábrica.
- **Técnicas-chave (Verificado):** stdout para saída principal, stderr para logs e erros; exit 0 em sucesso e não zero em falha; `--json` e `--plain`; `NO_COLOR`; `--no-input`; não ler segredos de variáveis de ambiente; seguir XDG; precedência de configuração: flags, variáveis de ambiente, configuração do projeto, do usuário, do sistema; primeira resposta em menos de 100 ms; desinstalação fácil, com instruções ao fim das de instalação.
- **Conteúdo reutilizável (destilação própria):**
  - [ ] exit codes distintos e documentados · [ ] stdout/stderr separados · [ ] `--help` com exemplos primeiro · [ ] `--json` estável e `--plain` · [ ] sem cor sem TTY ou com `NO_COLOR` · [ ] `--no-input` falha dizendo quais flags passar · [ ] confirmação proporcional ao risco, com `--yes`/`--force` · [ ] segredo nunca por flag nem por variável de ambiente · [ ] desinstalação documentada.
- **Ressalvas:** não cobre TUI, desktop, auto-update, assinatura nem instaladores Windows. Sem licença: só destilar.
- **Verificação:** WebFetch com onze itens conferidos; autores confirmados; licença e data não encontradas.

### V-14 — Verbos aprovados e nomes Verbo-Substantivo (PowerShell) (origem R-authoritative-14) — Classe A (8) · Prompt-score 83
- **Lente:** authoritative
- **Tipo:** checklist (convenção de nome)
- **Fonte:** https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands · **Autor/Org:** Microsoft Learn (autor listado: sdwheeler)
- **Sinais:** `ms.date` 2026-03-30 e `updated_at` 2026-03-31 (Verificado nos metadados); aplica-se de Windows PowerShell 5.1 a 7.x.
- **Para que serve no segmento:** nomear funções e scripts PowerShell (build, instalador, release).
- **Técnicas-chave (Verificado):** usar a forma exata do verbo aprovado (`Get`, não `Gets`); nada de sinônimo (`Remove`, nunca `Delete`); verbos reservados: `ForEach`, `Ping`, `Sort`, `Tee`, `Where`; `New` cria, `Add` acrescenta a algo existente, `Set` modifica (ou cria com dados); `Invoke` é síncrono, `Start` é assíncrono; `Test` no lugar de `Ping`; `Get` obtém o objeto, `Read` extrai o conteúdo; `Get-Verb` lista todos.
- **Conteúdo reutilizável (destilação própria) — tabela de escolha:** instalar → `Install`; desinstalar → `Uninstall`; validar/diagnosticar → `Test`; publicar → `Publish`; implantar em destino remoto → `Deploy`; executar e esperar → `Invoke`; iniciar sem esperar → `Start`; medir → `Measure`; comparar → `Compare`.
- **Ressalvas:** **Correção importante para este ambiente:** `Build` (e `Deploy`) foram adicionados no PowerShell 6; **não existem no Windows PowerShell 5.1**, que é o shell principal desta máquina. O item original sugeria `Build` sem essa nota. Em scripts que rodam em 5.1, usar `Invoke-<Algo>Build` ou `New-<Artefato>`. A própria tabela da página lista `Build` como sinônimo a evitar de `New`; conferir com `Get-Verb` na versão instalada.
- **Verificação:** WebFetch da página inteira (com metadados); conferi cada verbo citado e a data.

### V-15 — Diretrizes de design de cmdlets e scripts PowerShell (origem R-community-09; substitui R-github-19) — Classe B (7) · Prompt-score 80
- **Lente:** community (item substituto da R-github-19, que veio vazia)
- **Tipo:** checklist + reference
- **Fonte:** https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/strongly-encouraged-development-guidelines · **Autor/Org:** Microsoft Learn
- **Sinais:** `ms.date` 2021-10-05, `updated_at` 2026-04-08 (Verificado). Classe rebaixada de A(8) para B(7): atualização de conteúdo antiga, texto escrito para cmdlets compilados em .NET.
- **Para que serve no segmento:** revisar scripts e módulos PowerShell antes de publicar.
- **Técnicas-chave (Verificado):** substantivos específicos e no singular; PascalCase em cmdlets e parâmetros; nomes de parâmetro padrão; tipos fortes (`ValidateSet` ou enum para listas de opções); `[switch]` em vez de booleano; suporte a `PassThru` em `Add/Set/New`; suporte a arrays e a conjuntos de parâmetros; entrada por pipeline; escrever objetos no pipeline à medida que são gerados; mensagens por `Write-Warning`/`Write-Verbose`/`Write-Debug` (equivalentes de script dos métodos citados); sem a API `System.Console` dentro de cmdlets; arquivo de ajuda.
- **Conteúdo reutilizável (destilação própria) — checklist de script (10 itens):** verbo aprovado; substantivo singular; PascalCase; `[switch]` para flags; `ValidateSet` para opções; aceitar pipeline quando fizer sentido; objetos (não texto) na saída; `Write-Verbose/Warning/Debug` para mensagens; ajuda com exemplos (`.SYNOPSIS`, `.EXAMPLE`); parâmetro `Path` com `-LiteralPath` quando lidar com arquivos.
- **Ressalvas:** **Correção:** o título do item de origem prometia `ShouldProcess`, mas **a página não trata de `ShouldProcess`, `-WhatIf` nem `-Confirm`** (Verificado); também não menciona `Write-Host`. A regra "preferir `Write-Verbose` a `Write-Host`" é **Inferido** da orientação sobre feedback ao usuário. A lacuna de `ShouldProcess`/`-WhatIf` segue aberta (ver Lacunas). R-github-19 (`cmdlet-development-guidelines`) foi **rejeitada** por não ter conteúdo extraído.
- **Verificação:** WebFetch da página (metadados e texto); conferi cada técnica listada e anotei as ausentes.

### V-16 — Checklist de segurança do Electron (origem R-authoritative-15, R-github-05, R-community-15) — Classe A (8) · Prompt-score 85
- **Lente:** authoritative + github + community
- **Tipo:** checklist
- **Fonte:** https://www.electronjs.org/docs/latest/tutorial/security · **Autor/Org:** projeto Electron
- **Sinais:** documentação oficial `latest` (Verificado: 20 recomendações numeradas). Sem data de página e sem licença declarada; **reclassificado** de B(6) (github) e A(9) (community) para A(8).
- **Para que serve no segmento:** revisão de um app Electron antes do release.
- **Técnicas-chave (Verificado, com a numeração da página):** 1 só conteúdo seguro (HTTPS/WSS); 2 sem `nodeIntegration` com conteúdo remoto; 3 `contextIsolation`; 4 `sandbox` (desligar o isolamento de contexto, por exemplo com `nodeIntegration: true`, desliga também o sandbox daquele processo); 5 tratar pedidos de permissão (`setPermissionRequestHandler`); 6 não desligar `webSecurity`; 7 CSP; 8 sem `allowRunningInsecureContent`; 9 sem recursos experimentais; 10 sem `enableBlinkFeatures`; 11 sem `allowpopups` em webview; 12 validar opções do webview (`will-attach-webview`); 13 limitar navegação (`will-navigate`); 14 limitar novas janelas (`setWindowOpenHandler`); 15 `shell.openExternal` nunca com conteúdo não confiável; 16 Electron atualizado; 17 validar o `sender` de toda mensagem IPC; 18 evitar `file://` e preferir protocolo customizado (`protocol.handle`); 19 revisar fuses (`@electron/fuses`: `runAsNode`, `nodeCliInspect`); 20 não expor APIs do Electron a conteúdo não confiável.
- **Conteúdo reutilizável (destilação própria) — checklist com coluna de verificação:**
  - [ ] `contextIsolation`/`sandbox` ligados e `nodeIntegration` desligado em toda janela (verificar: buscar por `nodeIntegration: true` e `contextIsolation: false` na configuração das janelas)
  - [ ] CSP definida · [ ] handler de permissões · [ ] navegação e novas janelas com negação por padrão
  - [ ] cada `ipcMain.handle`/`on` valida o remetente · [ ] preload expõe funções específicas, nunca `ipcRenderer` cru
  - [ ] `openExternal` só com URL fixa ou validada · [ ] fuses revistos · [ ] versão do Electron atual
  - Skill sugerida: `electron-security-audit`, que lê arquivos e **não** executa o app.
- **Ressalvas:** a lista não tem prioridade; o item de IPC exige ler código real. As sugestões de `grep` são da fábrica (**Inferido**).
- **Verificação:** WebFetch listou as 20 recomendações e confirmou cada uma citada pelos três pesquisadores.

### V-17 — Assinatura de código e notarização para Electron (origem R-authoritative-16) — Classe A (8) · Prompt-score 82
- **Lente:** authoritative
- **Tipo:** checklist (distribuição)
- **Fonte:** https://www.electronjs.org/docs/latest/tutorial/code-signing · **Autor/Org:** projeto Electron
- **Sinais:** documentação oficial (Verificado). Sem data nem licença declarada.
- **Para que serve no segmento:** planejar entrega Windows/macOS sem alertas.
- **Técnicas-chave (Verificado):** desde junho de 2023 a Microsoft exige certificados de validação estendida (EV) para reduzir alertas, segundo a página; assinatura em nuvem facilita CI (a página cita o DigiCert KeyLocker para os apps do próprio Electron); "Azure Artifact Signing" (antigo Azure Trusted Signing) é descrito como a opção mais barata, limitada a desenvolvedores de certos países (a lista está na documentação da Microsoft); no macOS, assinar e depois notarizar exige conta no Apple Developer Program e Xcode; o Electron Forge é a ferramenta recomendada para Windows (inclusive instaladores Squirrel.Windows e WiX MSI); app sem assinatura ou com assinatura ad hoc pode se comportar de forma inconsistente (por exemplo, `safeStorage` volta a pedir permissão no Keychain depois de cada atualização); o Squirrel.Mac exige app assinado para atualizar.
- **Conteúdo reutilizável (destilação própria) — checklist de release:** certificado escolhido (EV ou serviço de assinatura em nuvem para CI); chave privada fora do repositório; notarização no macOS; atualização testada com build assinado; primeira execução testada em máquina limpa; desinstalação testada.
- **Ressalvas:** **Conflito entre fontes — RESOLVIDO na rodada de complemento (ver V-44):** a página do Electron diz que EV é exigido desde 2023 e que a assinatura em nuvem elimina os avisos do SmartScreen; as páginas da Microsoft (2026) dizem que o requisito de junho de 2023 foi de HSM para OV, que o bypass do SmartScreen do EV acabou em 2024 e que o Azure Artifact Signing não dá confiança instantânea. **"EV obrigatório" está refutado**; use V-44 para a decisão de certificado. (A afirmação sobre a página de assinatura do Tauri estava imprecisa: ela diz apenas que seu guia vale para OV obtidos antes de 1/6/2023.) Preços e países de serviços de assinatura mudam; conferir antes de usar.
- **Verificação:** WebFetch com sete pontos conferidos.

### V-18 — Auto-update do Electron (Squirrel, RELEASES, HTTP 204) (origem R-community-17) — Classe A (8) · Prompt-score 80
- **Lente:** community
- **Tipo:** checklist
- **Fonte:** https://www.electronjs.org/docs/latest/tutorial/updates · **Autor/Org:** projeto Electron
- **Sinais:** documentação oficial (Verificado).
- **Técnicas-chave (Verificado):** `autoUpdater` com Squirrel é o caminho "oficialmente suportado"; Squirrel.Windows serve `RELEASES` em `/RELEASES` mesmo sem atualização; Squirrel.Mac responde JSON com `url` obrigatória ou 204 sem atualização; usar `app.isPackaged` para só ativar o código de update no app empacotado; tratar o evento `error`; servidores alternativos listados: Hazel, Nuts, electron-release-server, Nucleus.
- **Conteúdo reutilizável (destilação própria):** checklist de 7 itens: escolher o servidor; testar o caminho "sem atualização" (RELEASES, 204); só em app empacotado; tratar `error` e logar; avisar o usuário quando o download termina; testar atualização de versão anterior para a nova com build assinado; plano de rollback.
- **Ressalvas:** **Correção:** `update.electronjs.org` exige repositório GitHub **público** com builds publicados em GitHub Releases (e builds assinados no macOS), não "open source" como estava no item. As alternativas privadas não foram avaliadas.
- **Verificação:** WebFetch com sete pontos conferidos, um corrigido.

### V-19 — Segurança e capabilities do Tauri v2 (origem R-authoritative-17, R-authoritative-18, R-github-06, R-community-18) — Classe A (8) · Prompt-score 84
- **Lente:** authoritative + github + community
- **Tipo:** checklist + config-template
- **Fonte:** https://v2.tauri.app/security/ · https://v2.tauri.app/security/capabilities/ · **Autor/Org:** projeto Tauri
- **Sinais:** a página de segurança exibe "Last updated: Jul 22, 2026" (Verificado). Sem licença declarada. **Reclassificado** de B(6) (github) para A(8) pela autoridade e pela data.
- **Técnicas-chave (Verificado):** fronteira entre o núcleo Rust (acesso irrestrito) e o frontend/WebView (só vê o que o IPC expõe); capabilities restringem comandos; "inspecionar e definir fortemente todos os dados que cruzam a fronteira" para evitar violações de confiança (a página não usa a palavra "validar"); CSP e padrão de isolamento só aparecem como links; WebView do sistema (atualizações de segurança mais rápidas); reporte de vulnerabilidade em privado (GitHub ou `security@tauri.app`). Capabilities: arquivos em `src-tauri/capabilities` (JSON ou TOML), campos `identifier`, `description`, `windows`, `platforms`, `permissions`, `remote.urls`; se `tauri.conf.json` listar capabilities, só elas entram no build; a fronteira segue o **rótulo** da janela, não o título; em Linux e Android o Tauri não distingue iframe da janela; por padrão todos os comandos registrados em `invoke_handler` são chamáveis por todas as janelas, a menos que `AppManifest::commands` em `build.rs` restrinja.
- **Conteúdo reutilizável (destilação própria):**
  - Checklist: [ ] lista mínima de comandos expostos e `AppManifest::commands` restringindo o padrão "todos chamam todos" · [ ] uma capability por janela, com `windows` explícito · [ ] nenhum `remote` sem justificativa escrita · [ ] entrada validada e tipada em cada comando Rust · [ ] CSP · [ ] quem pode criar janelas controlado (rótulo é a fronteira) · [ ] WebView do sistema atualizado · [ ] política de reporte no README.
  - Modelo de capability: `identifier: janela-principal`, `windows: ["main"]`, `permissions`: o padrão do core mais só o que for necessário.
- **Ressalvas:** isolation pattern e CSP **foram lidos na rodada de complemento (V-47)**; a URL correta é `/concept/inter-process-communication/isolation/`. Nomes de permissão variam por plugin.
- **Verificação:** WebFetch das duas páginas, com cada campo e cada comportamento conferido.

### V-20 — Updater do Tauri v2: assinatura e manifesto (origem R-authoritative-19) — Classe A (8) · Prompt-score 83
- **Lente:** authoritative
- **Tipo:** checklist (auto-update)
- **Fonte:** https://v2.tauri.app/plugin/updater/ · **Autor/Org:** projeto Tauri
- **Sinais:** documentação oficial (Verificado). Sem data.
- **Técnicas-chave (Verificado):** assinatura obrigatória e impossível de desligar; `pubkey` em `plugins.updater` recebe o **conteúdo** da chave; a chave privada vai por `TAURI_SIGNING_PRIVATE_KEY` (caminho ou conteúdo) e `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` (opcional); arquivos `.env` não funcionam para isso; manifesto estático exige `version` e, por plataforma, `url` e `signature` (conteúdo do `.sig`, não caminho); servidor dinâmico responde 204 sem atualização e 200 com `url`, `version` e `signature`; TLS obrigatório em produção (`dangerousInsecureTransportProtocol` existe para exceções); no Windows `installMode` pode ser `passive` (padrão), `basicUi` ou `quiet` (desencorajado).
- **Conteúdo reutilizável (destilação própria):** checklist: chave gerada e guardada fora do repositório (perdê-la impede publicar atualizações para instalações existentes, afirmado pelos pesquisadores e coerente com o modelo de assinatura; **não** reconferi esta frase); chave pública no config; manifesto completo validado antes de publicar; endpoint HTTPS; estado salvo antes do fechamento no Windows; testar versão anterior para a nova.
- **Ressalvas:** comparar com o updater do Electron (V-18) fica como lacuna de documentação própria; a ordem de assinatura com Authenticode está em V-21.
- **Verificação:** WebFetch com cada variável e campo conferidos.

### V-21 — Assinatura Windows no Tauri e ordem Authenticode versus assinatura do updater (origem R-community-16) — Classe B (7) · Prompt-score 78
- **Lente:** community
- **Tipo:** workflow + checklist
- **Fonte:** https://v2.tauri.app/distribute/sign/windows/ (oficial) e https://www.fluxzy.io/resources/blogs/electron-to-tauri-migration-fluxzy-desktop (relato, 2026-05-09)
- **Sinais:** guia oficial lido; relato de praticante com HN de poucos pontos (autor único).
- **Técnicas-chave (Verificado):** é preciso um certificado de **code signing** (certificado SSL não serve); `Import-PfxCertificate` para o repositório do usuário; `certificateThumbprint`, `digestAlgorithm`, `timestampUrl` em `bundle.windows`; segredos de CI para o `.pfx` em base64 e a senha; `signCommand` (relic/Azure Key Vault) para assinar em outra plataforma. O relato afirma que o Authenticode reescreve o binário e invalida a assinatura minisign do updater, então é preciso assinar com Authenticode primeiro e regenerar os `.sig`.
- **Conteúdo reutilizável (destilação própria):** roteiro de 6 passos: obter certificado de code signing; importar; preencher `bundle.windows`; configurar segredos; **assinar com Authenticode antes de gerar as assinaturas do updater**; testar a atualização de uma versão de teste.
- **Nota da rodada de complemento:** a página oficial do updater (V-20) e a de assinatura Windows (V-46) foram relidas e **nenhuma trata da ordem** entre Authenticode e assinatura do updater; a ordem segue como hipótese de relato único, a confirmar em teste. A parte sobre certificado EV/OV deve seguir V-44.
- **Ressalvas:** **Atenção:** a página oficial só cobre certificados OV obtidos antes de 1/6/2023 e remete ao emissor para EV; seu exemplo de workflow usa ferramentas antigas (Node 12, `actions-rs/toolchain`, `webkit2gtk-4.0`, `tauri-action@v0`); valores como thumbprint e URL de timestamp são exemplos a substituir. A **ordem de assinatura** é relato único e a página oficial **não** a cobre (Verificado): tratar como hipótese a confirmar em teste.
- **Verificação:** WebFetch da página oficial (EV, exemplos, ausência do tema da ordem) e do post da Fluxzy (confirma a ordem, data e a ponte entre updaters).

### V-22 — Rubrica de auditoria de DX (gstack `devex-review`) (origem R-authoritative-24, R-github-07, R-community-20) — Classe B (7) · Prompt-score 79
- **Lente:** authoritative + github + community. **Reclassificado:** github tinha A(8), authoritative B(6), community B(6). Fico com B(7): autoria individual, evidência de validação baixa, skill acoplada a um runtime.
- **Tipo:** rubric + workflow
- **Fonte:** https://github.com/garrytan/gstack (arquivo local `docs/foundation/brain-of-agent-snapshot/vendor/gstack/devex-review/SKILL.md`, 1.094 linhas) · **Autor/Org:** `garrytan/gstack`
- **Sinais:** MIT, 135.781★, `pushed_at` 2026-10-09 (Verificado pela API de busca). Skills `devex-review` e `plan-devex-review` existem na árvore (Verificado na página).
- **Técnicas-chave (Verificado no arquivo local):** oito leis de DX; sete características (usável, confiável, encontrável, útil, valioso, acessível, desejável); escala 0–10 com o "método do gap" (descrever o que seria 10 para este produto); faixas de TTHW (campeão, competitivo 2–5 min, precisa melhorar 5–10 min, alerta vermelho acima de 10 min); "boomerang" (estimativa do plano contra tempo medido).
- **Conteúdo reutilizável (destilação própria):** roteiro: (1) instalar só pelo README, sem atalho; (2) cronometrar até o primeiro resultado útil; (3) anotar cada atrito com passo e mensagem exata; (4) provocar erros de propósito (argumento faltando, flag inválida) e avaliar se dizem o que fazer; (5) testar a desinstalação limpa; (6) comparar com a expectativa do plano; (7) para cada nota, descrever o que seria 10.
- **Ressalvas (segurança):** o `SKILL.md` do gstack manda executar binários `bin/gstack-*`, registrar telemetria, gravar estado e fazer perguntas de consentimento; o instalador do repositório roda `./setup`. **Nada disso é incorporado ou executado**; só a rubrica tem valor. A afirmação do arquivo de que ">10 min" implica "50–70% abandonam" **não tem evidência** no texto; **não usar** esse número. Regra da base: instalar ferramenta de terceiros só com autorização explícita.
- **Verificação:** leitura do arquivo local (cabeçalho, leis, características, TTHW, método do gap, telemetria e binários); WebFetch do repositório; API de busca para metadados.

### V-23 — Subagentes: formato oficial e coleção de referência (origem R-community-13, R-github-12; template A-04) — Classe A (8) para o formato; B (7) para a coleção · Prompt-score 84
- **Lente:** community + github
- **Tipo:** subagent (formato) + reference
- **Fonte:** https://code.claude.com/docs/en/sub-agents · https://github.com/VoltAgent/awesome-claude-code-subagents
- **Sinais:** doc oficial (Verificado). VoltAgent: MIT, 25.618★, `pushed_at` 2026-10-05 (API de busca); a página declara uso "como está", sem garantia, e que os mantenedores não auditam os subagentes.
- **Técnicas-chave (Verificado na doc):** obrigatórios `name` e `description`; opcionais `tools` (lista permitida), `disallowedTools`, `model` (`sonnet`, `opus`, `haiku`, ID completo ou `inherit`), `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `omitClaudeMd`, `effort`, `isolation` (`worktree`), `color`; campos com nome errado são ignorados em silêncio e a grafia é camelCase; **subagentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`** (por segurança); acima de 15.000 tokens somados nas descrições, o Claude Code mostra um aviso na inicialização.
- **Conteúdo reutilizável (destilação própria) — template de subagente revisor:**
  ```
  ---
  name: diff-gap-reviewer
  description: Use quando uma implementação terminou e precisa de revisão independente contra o plano. Revisa a diff e relata lacunas de correção ou requisito.
  tools: Read, Grep, Glob
  model: sonnet
  ---
  Papel: revisor adversarial em contexto novo. Objetivo: achar lacunas de correção e de requisito.
  Escopo: ler a diff e o PLANO; não editar arquivos.
  Processo: 1) listar requisitos; 2) cruzar com a diff e com os testes; 3) procurar mudanças fora do escopo.
  Saída: achados com arquivo:linha, severidade e confiança; "sem lacunas" quando for o caso. Não relatar estilo.
  ```
- **Ressalvas:** **Correção (segurança):** `Read, Grep, Glob` é somente leitura; incluir `Bash` (como no blog arps18 e em exemplos da própria doc) **não** é somente leitura. Os arquivos individuais do VoltAgent não foram abertos por mim; o formato de quatro campos foi visto no índice. Categoria `04-quality-security` lista `code-reviewer` e `security-auditor`, conteúdo não lido.
- **Verificação:** WebFetch da doc (tabela de campos, aviso de plugin, 15 mil tokens); WebFetch do repositório VoltAgent (categorias, quatro campos, avisos, instalador por `curl -s ... -o`, sem pipe para shell); API de busca.

### V-24 — Validação de plugin em camadas (wshobson/agents) (origem R-github-13) — Classe B (7) · Prompt-score 76
- **Lente:** github
- **Tipo:** pattern + workflow
- **Fonte:** https://github.com/wshobson/agents
- **Sinais:** MIT, 40.318★, `pushed_at` 2026-10-05 (API de busca). A página mostra 94 plugins, 202 agentes, 184 skills e 105 comandos (Verificado).
- **Técnicas-chave (Verificado):** validação estrutural em modo estrito (`make validate STRICT=1`, `make generate-all`, `make garden`); `plugin-eval` com análise estática de skills sem chamada a modelo; camadas de juiz LLM e Monte Carlo declaradas "experimentais, não validadas contra rótulos humanos"; chamadas de modelo usam `ANTHROPIC_API_KEY` quando definida (cobrança de API); instalação via marketplace, `gh skill install` ou `npx skills add` (executam código de terceiros).
- **Conteúdo reutilizável (destilação própria):** pirâmide de validação da fábrica: (1) estrutura determinística (`claude plugin validate --strict`, frontmatter, nomes, links); (2) análise estática de skills sem modelo; (3) avaliação por modelo só como sinal, declarando que não foi validada por humanos e informando o custo antes de rodar.
- **Ressalvas:** escala grande demais para absorver; usar o padrão, não o conteúdo. Não executei nenhum alvo do `Makefile`.
- **Verificação:** WebFetch (contagens, comandos, aviso de LLM, uso de chave); API de busca.

### V-25 — Fases de desenvolvimento orientado a especificação (cc-sdd) (origem R-github-15) — Classe B (7) · Prompt-score 77
- **Lente:** github
- **Tipo:** workflow
- **Fonte:** https://github.com/gotalab/cc-sdd
- **Sinais:** MIT, 3.709★, `pushed_at` 2026-09-23 (API de busca). Claude Code e Codex estáveis; os demais agentes em beta (Verificado).
- **Técnicas-chave (Verificado):** brief → requisitos em EARS com critérios de aceitação → design (plano de estrutura de arquivos e diagrama) → tarefas (com anotações de fronteira e dependência) → implementação com RED→GREEN e revisor independente por tarefa quando há subagentes; humanos aprovam nas portas entre fases.
- **Conteúdo reutilizável (destilação própria):** fases com arquivo versionado por fase e aprovação do usuário antes da seguinte; no plugin, expor como skill de planejamento (não de execução autônoma).
- **Ressalvas:** **Correção:** os pesquisadores diziam que o comando de implementação "roda tarefas sem supervisão e exige revisão"; a página descreve a implementação como "autônoma de longa duração" e **não traz aviso explícito** sobre supervisão. A recomendação de revisar cada tarefa é da fábrica. A instalação é `npx cc-sdd@latest` (executa código de terceiros): não executar sem autorização do usuário; existe `--dry-run`.
- **Verificação:** WebFetch da página; API de busca.

### V-26 — Anti-padrões de instalação de conjuntos grandes de agentes (ECC) (origem R-github-18) — Classe B (6) · Prompt-score 80
- **Lente:** github
- **Tipo:** anti-pattern + checklist
- **Fonte:** https://github.com/affaan-m/ECC
- **Sinais:** MIT, 276.210★, `pushed_at` 2026-10-10; release 2.2.3 em 2026-10-01 (Verificado). Popularidade não eleva a classe (contagens internas divergentes: 302 versus 293 skills, 95 versus 94 comandos).
- **Técnicas-chave (Verificado):** não empilhar métodos de instalação para o mesmo harness; não copiar o `hooks.json` bruto para o `settings.json` (execução duplicada); exigir escolha explícita entre `--enable-hooks` e `--no-hooks`; versão fixada não é auditoria; Windows nativo é "suportado com limitações" (recursos de shell exigem Git Bash ou WSL).
- **Conteúdo reutilizável (destilação própria) — checklist de instalação de plugin de terceiros:** revisar o código antes; um único método de instalação por harness; não copiar `hooks.json` para o `settings.json`; escolher explicitamente se hooks ficam ligados; versão fixada não substitui revisão; conferir compatibilidade com Windows; desinstalação limpa documentada; não executar instalador de fonte não oficial.
- **Ressalvas:** o instalador executa código (`npx`, `install.sh`, `install.ps1`); **não executar**. Só a parte final do texto da página não foi lida.
- **Verificação:** WebFetch (as cem mil primeiras posições); API de busca.

### V-27 — Guardrails de configuração do Claude Code (Trail of Bits) (origem R-authoritative-22, R-github-10, R-github-11, R-community-03) — Classe B (6) · Prompt-score 78
- **Lente:** authoritative + github + community. **Reclassificado:** authoritative B(6), github C(4), community B(6). Fico com B(6): a data de push (2026-08-24) e a ausência de licença agora estão verificadas.
- **Tipo:** checklist + config-template (somente destilação)
- **Fonte:** https://github.com/trailofbits/claude-code-config (e `claude-md-template.md` na raiz) · **Autor/Org:** Trail of Bits
- **Sinais:** 2.129★, `pushed_at` 2026-08-24, **sem licença** (a API retorna `None` e a página não mostra arquivo LICENSE) (Verificado). Sem licença, **só destilar**; a suposta CC-BY-SA-4.0 das skills não foi confirmada.
- **Técnicas-chave (Verificado no README):** dois hooks PreToolUse em Bash que bloqueiam `rm -rf` (sugerindo `trash`) e push direto para main/master (exigindo branch de feature); deny rules de Read e Edit para chaves SSH/GPG, credenciais de nuvem, tokens de registro de pacotes, credenciais do git, configuração de shell (edição negada para evitar plantar backdoor), chaveiro do macOS e carteiras de criptomoeda; `enableAllProjectMcpServers: false` explícito, porque um repositório comprometido pode trazer servidores MCP; a própria documentação diz que hooks são guardrail e não fronteira.
- **Conteúdo reutilizável (destilação própria):**
  - Template de política: deny para caminhos de chaves e credenciais (`~/.ssh`, `~/.gnupg`, nuvem, contêiner), tokens de pacotes (`.npmrc`, `.pypirc`), arquivos de configuração do shell; `enableAllProjectMcpServers: false`; hooks de bloqueio com mensagem de alternativa (ver V-08); sandbox como fronteira real.
  - Do `claude-md-template.md` (Verificado: seções de escopo, comunicação, qualidade, testes, revisão, ferramentas, fluxo): resultado primeiro; relatar progresso só com evidência de ferramenta e declarar o que não foi verificado; achados de revisão com arquivo, linha, severidade e confiança; pedir antes de aplicar correção; subagentes só para trabalho grande e independente.
- **Ressalvas:** o template tem preferências pessoais de ferramenta (por exemplo, preferir Exa a WebSearch, `trash` do macOS); remover o que não for genérico. Os caminhos exatos da lista de deny e os scripts de hook não foram abertos linha a linha. Hooks em bash precisam de tradução para PowerShell no Windows.
- **Verificação:** WebFetch do README e do `claude-md-template.md`; API de busca para estrelas, push e licença.

### V-28 — Fonte única de regras para vários agentes (Ruler) (origem R-authoritative-23, R-github-09, parte de R-community-22) — Classe B (6) · Prompt-score 76
- **Lente:** authoritative + github + community
- **Tipo:** pattern
- **Fonte:** https://github.com/intellectronica/ruler
- **Sinais:** MIT, 2.941★, `pushed_at` 2026-09-30 (API de busca). A README se rotula "Beta Research Preview"; nenhuma release publicada (Verificado).
- **Técnicas-chave (Verificado):** fonte em `.ruler/`; `ruler apply` gera arquivos por agente; backup `.bak` por padrão; `ruler revert`; `--dry-run` em `apply` e `revert`; modo aninhado experimental; skills experimentais (**habilitadas por padrão**, segundo a página) e subagentes experimentais (desligados por padrão).
- **Conteúdo reutilizável (destilação própria):** usar como referência de padrão (fonte única + geração + backup + dry-run); se adotado, rodar `--dry-run` antes e revisar os arquivos gerados; conferir o `CLAUDE.md` gerado contra V-06/V-10 (precedência).
- **Ressalvas:** estado "beta"; instalar a ferramenta exige autorização do usuário (não instalei). Windows e links simbólicos não verificados.
- **Verificação:** WebFetch da README; API de busca.

### V-29 — Subagente de revisão de PR com veredito (origem R-community-06) — Classe B (6) · Prompt-score 79
- **Lente:** community
- **Tipo:** subagent (padrão)
- **Fonte:** https://arps18.github.io/posts/claude-code-mastery/ (Arpan Patel, 2026-05-26) · HN 48289950: 451 pontos, 254 comentários, 2026-05-27 (Verificado pela API Algolia)
- **Técnicas-chave (Verificado):** revisor com seção "NÃO sinalizar" para cortar ruído de estilo; saída com veredito `SHIP`, `FIX FIRST` ou `REWORK`; modelo mais capaz justificado pelo custo de deixar passar falha de segurança.
- **Conteúdo reutilizável (destilação própria):** estender V-23: acrescentar ao revisor uma seção "Não sinalizar" (estilo, preferências, casos impossíveis), agrupar achados por severidade e fechar com um de três vereditos.
- **Ressalvas:** **Correção:** o blog chama as ferramentas `Read, Grep, Glob, Bash` de "deliberadamente somente leitura", mas `Bash` pode modificar arquivos; é somente leitura **por intenção**, não por permissão. O prompt completo do blog não é publicado; o texto acima é composição própria.
- **Verificação:** WebFetch do blog (frontmatter, seção "Do NOT flag", vereditos, modelo); API Algolia.

---

## Itens aprovados do complemento (rodada gapfill, V-30 a V-67)

Origem: `gapfill.md` (pesquisador claude-haiku-5-5, sem WebSearch) revalidado em 2026-10-10 pelo validador claude-sonnet-5-5 em sessão independente. Escala de rótulos: **Verificado** = conferi nesta rodada com ferramenta; **Inferido**; **Suposição**; **Não verificado**. Onde o resumo da ferramenta de leitura (WebFetch) foi a única evidência de um corpo de arquivo, o item diz "pontuado sobre resumo estruturado". Todo conteúdo reutilizável é destilação com redação própria; nenhum trecho literal de fonte foi mantido.

### V-30 — Textual (TUI em Python): teclado, foco, testes headless e snapshots (origem R-gap-01) — Classe A (8) · Prompt-score 84
- **Lente:** gapfill (authoritative)
- **Tipo:** reference + checklist
- **Fonte:** https://textual.textualize.io/guide/input/ · https://textual.textualize.io/guide/testing/ · repositório https://github.com/Textualize/textual · **Autor/Org:** Textualize
- **Sinais:** `Textualize/textual` 37.422★, MIT, push 2026-10-09, não arquivado (Verificado pela API de busca do GitHub). Páginas de guia sem data.
- **Para que serve no segmento:** escolher e testar TUI em Python (ferramentas de terminal interativas).
- **Técnicas-chave (Verificado):** `BINDINGS` são tuplas (tecla, ação, descrição) ou instâncias `Binding`; `priority=True` é checado antes dos bindings do widget focado e o widget não consegue desativá-lo (o App usa em Ctrl+Q); `show=False` esconde do rodapé; Tab e Shift+Tab movem o foco; `can_focus` é booleano, mas widget desabilitado não recebe foco. Testes: `app.run_test()` roda em modo headless (não atualiza o terminal) e devolve um `Pilot`; `pilot.press(...)` aceita várias teclas; `pilot.click(seletor, offset=, times=, modificadores)`; tamanho simulado padrão (80, 24), alterável com `size=(l, a)`; snapshots com `pytest-textual-snapshot` (fixture `snap_compare`, `terminal_size=(l, a)`); cada teste async precisa de `@pytest.mark.asyncio`, salvo `asyncio_mode = auto`.
- **Conteúdo reutilizável (destilação própria) — checklist de TUI Textual:** (1) toda ação tem binding com descrição visível no rodapé; `priority=True` só para sair e ajuda; (2) ordem de foco testada com Tab e Shift+Tab; (3) um teste headless por fluxo, com `press` e `click`; (4) snapshot em pelo menos dois tamanhos (por exemplo 80x24 e 120x40) para pegar quebra no resize; (5) configurar o modo asyncio do pytest uma vez; (6) acessibilidade: **sem fonte oficial lida**, registrar como risco (contraste, sem depender só de cor, alternativa em texto).
- **Ressalvas:** a página de input não menciona acessibilidade nem leitor de tela (Verificado); modo não interativo além do headless de teste não foi confirmado. Versão do Textual não aparece nas páginas: conferir `pip show textual`.
- **Verificação:** WebFetch das duas páginas (cada ponto acima conferido) e API de busca do GitHub.

### V-31 — Ratatui (TUI em Rust): modo imediato, layout adaptativo e testes por snapshot (origem R-gap-02) — Classe B (7) · Prompt-score 80
- **Lente:** gapfill
- **Tipo:** reference + pattern
- **Fonte:** https://ratatui.rs/concepts/rendering/ · https://ratatui.rs/concepts/layout/ · https://ratatui.rs/recipes/testing/snapshots/ · repositório https://github.com/ratatui/ratatui · **Autor/Org:** projeto Ratatui
- **Sinais:** `ratatui/ratatui` 22.926★, MIT, push 2026-10-10 (Verificado). **Correção:** o pesquisador registrou a licença como "não verificável"; é MIT. Subpágina de snapshots, que ele só viu como índice, foi lida por mim.
- **Técnicas-chave (Verificado):** a UI é reconstruída a cada quadro dentro de `terminal.draw(|f| ...)` a partir do estado; o crate só desenha em um backend (ex.: `CrosstermBackend`), e a lib de eventos é escolha do app; thread bloqueada trava a UI; pouca ajuda embutida para organizar apps grandes. Layout divide `Frame::area()` com restrições `Length` (fixo), `Percentage`/`Ratio` (proporcional; cuidado ao misturar com fixos), `Min`/`Max` e `Fill`; o solver pode devolver resultado próximo e não determinístico quando as restrições não cabem. Testes: `TestBackend::new(80, 20)`, `terminal.draw(...)`, `assert_snapshot!(terminal.backend())` com `insta`, revisão por `cargo insta review`; a página recomenda tamanho fixo para reprodutibilidade.
- **Conteúdo reutilizável (destilação própria):** (1) estado separado da renderização; a função de draw não muda estado; (2) snapshot com `TestBackend` em dois tamanhos; (3) `TestBackend` **não** cobre loop de eventos, teclado nem setup do terminal (a própria página): usar teste de ponta a ponta com PTY para isso; (4) cor não é suportada nos snapshots atuais; (5) tratar resize como novo `Frame::area()` no próximo draw.
- **Ressalvas:** as páginas de rendering e layout **não** descrevem eventos de resize (Verificado), então "resize" fica como regra de projeto, não como fato do framework. Acessibilidade não encontrada. Instalar `cargo-insta` altera o ambiente: só recomendar.
- **Verificação:** WebFetch de rendering, layout e snapshots; API do GitHub.

### V-32 — Bubble Tea (TUI em Go): Init/Update/View, resize, execução sem renderer e teatest (origem R-gap-03) — Classe B (7) · Prompt-score 80
- **Lente:** gapfill
- **Tipo:** reference + pattern
- **Fonte:** https://github.com/charmbracelet/bubbletea · https://pkg.go.dev/github.com/charmbracelet/bubbletea · https://pkg.go.dev/github.com/charmbracelet/x/exp/teatest · **Autor/Org:** Charm
- **Sinais:** `charmbracelet/bubbletea` 45.411★, MIT, push 2026-10-08 (Verificado). `teatest` está sob `x/exp` (caminho experimental), MIT; a página avisa que a versão vista não é a mais recente do módulo.
- **Técnicas-chave (Verificado):** modelo com `Init`, `Update`, `View`; `tea.KeyPressMsg` chega ao `Update` (README); `WindowSizeMsg` (largura e altura) é enviado ao `Update` uma vez no início e a cada resize, e `WindowSize()` consulta sob demanda; opções `WithoutRenderer()` (saída simples para fora de TTY ou modo daemon), `WithInput`, `WithOutput`, `WithoutSignalHandler`. `teatest`: `NewTestModel`, `WaitFor` (padrão 1 s, verificação a cada 50 ms), `RequireEqualOutput` com arquivos golden atualizáveis por `-update`.
- **Conteúdo reutilizável (destilação própria):** (1) tratar `WindowSizeMsg` guardando largura e altura no modelo e recalculando o layout na `View`; (2) testar o `Update` com mensagens sintéticas, sem terminal; (3) fluxo completo com `teatest` e golden files, sabendo que o pacote é experimental e fixar a versão; (4) para uso em CI ou pipe, `WithoutRenderer()`.
- **Ressalvas:** o README **não** menciona `WindowSizeMsg` nem teste (Verificado); essas informações vêm do pkg.go.dev. A frase de que o Windows não reporta resize (sem SIGWINCH) veio do texto resumido do pkg.go.dev e **não foi reverificada** para a versão v2 atual: testar no Windows antes de afirmar. "Update é função pura" é **Inferido** da assinatura. Acessibilidade não encontrada.
- **Verificação:** WebFetch do README (Init/Update/View, KeyPressMsg, licença), do pkg.go.dev de Bubble Tea e de `teatest`; API do GitHub.

### V-33 — WPF (visão geral oficial) (origem R-gap-04) — Classe A (8) · Prompt-score 80
- **Lente:** gapfill (authoritative)
- **Tipo:** reference
- **Fonte:** https://learn.microsoft.com/en-us/dotnet/desktop/wpf/overview/ · **Autor/Org:** Microsoft Learn
- **Sinais:** `ms.date` 2026-03-23, `updated_at` 2026-03-30 (Verificado nos metadados).
- **Técnicas-chave (Verificado):** WPF é só Windows, mesmo sobre .NET moderno (duas implementações: .NET de código aberto em dotnet/wpf e .NET Framework 4, componente do sistema); markup XAML para aparência e code-behind para comportamento, unidos por `x:Class` e `InitializeComponent`; motor de data binding (`Binding`, `DataContext`) com validação, ordenação, filtro e agrupamento; sistema de comandos separa a ação do usuário da lógica; layout em duas etapas (filho pede, pai concede); `ControlTemplate` troca a aparência sem mudar comportamento; a página recomenda migrar de .NET Framework para .NET (cita acessibilidade e confiabilidade melhores).
- **Conteúdo reutilizável (destilação própria):** comandos em vez de handlers de clique para ações reutilizáveis; templates para aparência; binding para dados; migrar de .NET Framework quando possível.
- **Ressalvas:** a página **não** cita MVVM (Verificado); para MVVM ver V-34. Página de acessibilidade do WPF não localizada (a URL testada pelo pesquisador deu 404; não retestei). Segurança e empacotamento do WPF não lidos.
- **Verificação:** WebFetch da página inteira, com metadados.

### V-34 — MVVM Toolkit (`CommunityToolkit.Mvvm`) (origem R-gap-07) — Classe A (8) · Prompt-score 82
- **Lente:** gapfill (authoritative)
- **Tipo:** reference + pattern
- **Fonte:** https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/ · repositório https://github.com/CommunityToolkit/dotnet · **Autor/Org:** Microsoft / .NET Foundation
- **Sinais:** página com `ms.date` 2024-11-07 (mais de 18 meses: atualidade tratada como atemporal); repositório 3.762★, push 2026-03-25; **licença MIT** confirmada no arquivo `License.md` (a API do GitHub mostra "NOASSERTION" por causa do nome do arquivo: **Correção** do "licença não visível").
- **Técnicas-chave (Verificado):** tipos `ObservableObject`, `ObservableRecipient`, `ObservableValidator`; `RelayCommand` e `AsyncRelayCommand` (e versões genéricas e interfaces); `IMessenger` com `WeakReferenceMessenger` e `StrongReferenceMessenger`; `Ioc` para injeção de dependência; alvos .NET Standard 2.0, 2.1 e .NET 6; "à la carte", sem estrutura de app obrigatória.
- **Conteúdo reutilizável (destilação própria):** ViewModel sem referência a controles; comandos com `RelayCommand`/`AsyncRelayCommand`; comunicação entre ViewModels por messenger; validação em `ObservableValidator`.
- **Ressalvas:** **Correção ao pesquisador:** ele concluiu que o MAUI "não aparece" e deu a entender incompatibilidade; a página diz que o pacote mira .NET Standard e funciona "em qualquer plataforma de app", com a lista "WinUI 3, UWP, WinForms, WPF, Xamarin, Uno e mais". Ausência na lista não é incompatibilidade, mas também não é suporte confirmado para MAUI. Geradores de código (atributos de propriedade observável) **não** são tratados na página: não afirmar.
- **Verificação:** WebFetch da página e do arquivo de licença; API do GitHub.

### V-35 — WinUI 3 e acessibilidade em apps Windows (origem R-gap-05) — Classe A (8) · Prompt-score 86
- **Lente:** gapfill (authoritative)
- **Tipo:** checklist + reference
- **Fonte:** https://learn.microsoft.com/en-us/windows/apps/winui/winui3/ (a URL `/winui/` redireciona para ela) · https://learn.microsoft.com/en-us/windows/apps/design/accessibility/accessibility-overview · **Autor/Org:** Microsoft Learn
- **Sinais:** WinUI `ms.date` 2026-10-02; acessibilidade `ms.date` 2026-08-21 (Verificado).
- **Técnicas-chave (Verificado):** WinUI 3 é descrito como o framework nativo recomendado para novos apps desktop, parte do Windows App SDK, C# ou C++, Windows 10 1809 (build 17763) ou posterior. Acessibilidade vem de UI Automation (peers e patterns); o dado mais importante é o **nome acessível** de cada elemento; navegação por teclado embutida (Tab segue o layout; setas em `ListView`/`GridView`; Espaço/Enter em botão); alto contraste funciona se não houver cores fixas nem estilos que bloqueiem a busca de recursos de tema; tamanho e escala do sistema; sinal combinado (ícone com cor, alerta visual com som); controle customizado precisa de `AutomationPeer`; conteúdo DirectX em `SwapChainPanel` ou `SurfaceImageSource` **não** é acessível por padrão; verificação contínua (checagens automáticas a cada build mais teste manual com Narrator nos fluxos críticos).
- **Conteúdo reutilizável (destilação própria) — checklist de acessibilidade WinUI:** (1) nome acessível em todo controle interativo; (2) ordem de Tab revisada; (3) tema de alto contraste testado, sem cor fixa; (4) texto escala com o sistema sem cortar; (5) controles customizados com `AutomationPeer`; (6) fluxo crítico com Narrator; (7) checagem automática no CI.
- **Ressalvas:** empacotamento e segurança do WinUI vão em V-36; para WPF não há página equivalente lida.
- **Verificação:** WebFetch das duas páginas com metadados.

### V-36 — Windows App SDK: empacotamento e implantação (origem R-gap-08) — Classe A (8) · Prompt-score 84
- **Lente:** gapfill (authoritative)
- **Tipo:** decision guide + checklist
- **Fonte:** https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/deploy-overview · **Autor/Org:** Microsoft Learn
- **Sinais:** `ms.date` 2026-10-02 (Verificado). A página-índice `package-and-deploy/` não foi relida por mim.
- **Técnicas-chave (Verificado):** dois modos: framework-dependent (padrão: pequeno e atualizável pelo sistema, mas depende de instalar o runtime e há risco de componente compartilhado ser removido ou de regressão) e self-contained (controle da versão, isolamento, implantação xcopy, mas maior e, no não empacotado, mais lento e sem servicing); `PublishSingleFile` só para app **não empacotado e self-contained** (Windows App SDK 1.5 ou posterior); inicialização: empacotado framework-dependent usa a Deployment API, não empacotado usa a bootstrapper API, self-contained empacotado não precisa de inicialização; publicar por RID (`win-x64`, `win-arm64`); bundle MSIX com x64 e ARM64; Arm64EC para bases C/C++ grandes; emulação Prism roda x64 só no Windows 11 ARM64 (x86 em Windows 10 e 11 ARM64).
- **Conteúdo reutilizável (destilação própria):** árvore de decisão: (1) Store ou assinatura própria? (V-44); (2) precisa de identidade de pacote (V-40)? (3) runtime compartilhado ou embutido? (4) arquiteturas-alvo; (5) um build por RID ou um bundle.
- **Ressalvas:** páginas de deploy de apps empacotados e não empacotados só tiveram os links conferidos pelo pesquisador; eu também não as li.
- **Verificação:** WebFetch da página inteira.

### V-37 — .NET MAUI (visão geral) (origem R-gap-06) — Classe B (7) · Prompt-score 78
- **Lente:** gapfill (authoritative)
- **Tipo:** reference
- **Fonte:** https://learn.microsoft.com/en-us/dotnet/maui/what-is-maui · **Autor/Org:** Microsoft Learn
- **Sinais:** `ms.date` 2024-06-21, `updated_at` 2025-02-04 (Verificado); rebaixada de A(8) para B(7) por atualidade (8 meses desde a última atualização, texto-base de 2024).
- **Técnicas-chave (Verificado):** projeto único com multi-targeting para Android, iOS, macOS e Windows; no Windows usa WinUI 3, no macOS usa Mac Catalyst; APIs de sensores, rede, clipboard, arquivos, armazenamento seguro, TTS, fluxo de autenticação por callback; hot reload de C# e XAML; evolução do Xamarin.Forms; iOS e macOS exigem um Mac para compilar; suporte a data binding citado, sem detalhar MVVM.
- **Conteúdo reutilizável (destilação própria):** só escolher MAUI quando houver alvo mobile ou macOS além do Windows; caso contrário WinUI 3 (V-35) ou WPF (V-33).
- **Ressalvas:** a página de MVVM do MAUI deu 404 para o pesquisador e eu não a procurei; empacotamento e acessibilidade de desktop não estão na página.
- **Verificação:** WebFetch da página inteira com metadados.

### V-38 — Qt 6: implantação com `windeployqt` e `macdeployqt` (origem R-gap-09; macOS acrescentado pelo validador) — Classe B (7) · Prompt-score 82
- **Lente:** gapfill (authoritative)
- **Tipo:** checklist
- **Fonte:** https://doc.qt.io/qt-6/windows-deployment.html · https://doc.qt.io/qt-6/macos-deployment.html · **Autor/Org:** The Qt Company
- **Sinais:** documentação oficial Qt 6 sem data; documentação sob GFDL 1.3 (a página de licenciamento diz; destilar, não copiar). A lacuna do pesquisador ("`macdeployqt` não lido") foi fechada por mim.
- **Técnicas-chave (Verificado):** `windeployqt`: `--release`, `--no-translations`, `--qmldir <dir>` (varre importações QML), `--libdir`, `--no-compiler-runtime`; copia DLLs e plugins por tipo (`qwindows.dll` fica em `platforms`); em release o instalador deve incluir o Visual C++ Redistributable oficial e não DLLs soltas do compilador; bibliotecas de terceiros (banco de dados, por exemplo) entram à mão; build não relocável pede `qt.conf`; build estático não implanta plugins. `macdeployqt`: `-dmg`, `-qmldir=`, `-always-overwrite`, `-verbose=0..3`; a assinatura padrão é **ad hoc**: usar `-codesign=<identidade>`; `-sign-for-notarization=<identidade>` liga `-hardened-runtime`, `-timestamp` e o `-codesign` (exigem internet); usa o primeiro `.entitlements` achado em `Contents/Resources/` (manter no máximo um); `-appstore-compliant` pula componentes com API privada.
- **Conteúdo reutilizável (destilação própria):** (1) build release; (2) `windeployqt` com `--qmldir` se houver QML; (3) VC++ Redistributable no instalador (V-41/V-40); (4) dependências extras copiadas à mão; (5) macOS: `macdeployqt` com identidade real e preparo para notarização (V-45); (6) testar em máquina limpa; (7) para obrigações de licença ver V-39.
- **Ressalvas:** segurança do Qt continua sem fonte (a URL testada pelo pesquisador deu 404; não achei alternativa sem busca).
- **Verificação:** WebFetch das duas páginas (cada opção e aviso conferido).

### V-39 — Qt: licenciamento (comercial versus LGPLv3/GPLv3) (origem R-gap-10) — Classe B (7) · Prompt-score 80
- **Lente:** gapfill (authoritative)
- **Tipo:** decision guide (não é aconselhamento jurídico)
- **Fonte:** https://doc.qt.io/qt-6/licensing.html · **Autor/Org:** The Qt Company
- **Técnicas-chave (Verificado):** licença comercial para quem não quer compartilhar código com terceiros ou não pode cumprir a LGPLv3; LGPLv3 (ou GPLv3) para quem cumpre os termos; **14 módulos** não estão disponíveis sob LGPLv3 (Canvas Painter, CoAP, Graphs, GRPC, HTTP Server, Lottie Animation, MQTT, Network Authorization, Qml Compiler, Quick 3D, Quick 3D Physics, Quick Timeline, Virtual Keyboard, Wayland Compositor): **Correção:** o pesquisador listou 6 como exemplo; a página tem a lista completa. Ferramentas: comercial ou GPLv3 com "Qt GPL exception 1.0". Exemplos: comercial ou BSD-3-Clause. Documentação: comercial ou GFDL 1.3.
- **Conteúdo reutilizável (destilação própria) — matriz:** app fechado que usa módulo só-GPL → licença comercial; app fechado só com módulos LGPL → possível se cumprir a LGPLv3, e o usuário deve conferir as obrigações com assessoria jurídica; app aberto compatível → LGPLv3/GPLv3; antes de escolher, listar todos os módulos Qt usados e cruzar com a lista de 14.
- **Ressalvas:** as obrigações detalhadas da LGPLv3 (linkagem dinâmica, direito de substituir a biblioteca, avisos) **não foram obtidas** (a URL do pesquisador deu 404). Lacuna aberta.
- **Verificação:** WebFetch da página (cada afirmação conferida).

### V-40 — MSIX e App Installer (origem R-gap-11, R-gap-12) — Classe A (8) · Prompt-score 82
- **Lente:** gapfill (authoritative)
- **Tipo:** reference + checklist
- **Fonte:** https://learn.microsoft.com/en-us/windows/msix/overview · https://learn.microsoft.com/en-us/windows/msix/app-installer/app-installer-root · **Autor/Org:** Microsoft Learn
- **Sinais:** ambas `ms.date` 2026-04-15 (Verificado).
- **Técnicas-chave (Verificado):** MSIX dá identidade de pacote (publisher, nome e versão), exigida por notificações push, tarefas em segundo plano, tiles, APIs de IA do Windows, distribuição na Store e gestão por Intune; atualização diferencial por blocos de 64 KB; desinstalação sem resíduos; execução em contêiner leve com sistema de arquivos e registro virtualizados; conteúdo do pacote: payload, `AppxBlockMap.xml` (hashes por bloco de 64 KB), `AppxManifest.xml`, `AppxSignature.p7x`; todo pacote precisa estar assinado antes da instalação; ferramentas: WinApp CLI (certificados, build e assinatura), MSIX Packaging Tool (converte instalador), Package Support Framework, MSIX SDK. App Installer: instala por duplo clique e da web, pacotes opcionais e related sets; vem no Windows 10 1803 ou posterior e no 11; o arquivo `.appinstaller` descreve pacote e configuração de atualização; tutoriais de hospedagem em Azure Web App, IIS e AWS S3; páginas separadas de segurança, solução de problemas e referência do esquema.
- **Conteúdo reutilizável (destilação própria):** (1) pacote assinado (V-44); (2) identidade estável (mesmo publisher); (3) teste de instalar, atualizar e desinstalar em máquina limpa; (4) `.appinstaller` servido por HTTPS; (5) teste de atualização da versão anterior; (6) frameworks sem suporte a MSIX (o relato V-65 aponta Tauri) pedem outro instalador.
- **Ressalvas:** a taxa de "99,96% de sucesso de instalação" é alegação do fornecedor, **não** verificada de forma independente. A página não dá o passo a passo do manifesto; opções específicas de atualização do `.appinstaller` (`update-settings`) não foram lidas.
- **Verificação:** WebFetch das duas páginas com metadados.

### V-41 — Inno Setup (construtor de instaladores) (origem R-gap-13) — Classe B (7) · Prompt-score 78
- **Lente:** gapfill (authoritative)
- **Tipo:** reference
- **Fonte:** https://jrsoftware.org/ishelp/topic_whatisinnosetup.htm · https://jrsoftware.org/ishelp/topic_setup_signtool.htm · **Autor/Org:** Jordan Russell e Martijn Laan
- **Sinais:** ajuda versão 7.1.0 no cabeçalho (Verificado). Licença: arquivo de licença do projeto lido por mim; é uma licença própria e permissiva (uso comercial permitido; manter avisos de copyright em código e binários; não afirmar autoria do original; versões modificadas devem ser marcadas), **não** uma licença OSI padrão. A página "o que é" pede que usuários comerciais comprem uma licença comercial (pedido, não condição da licença).
- **Técnicas-chave (Verificado):** instaladores com scripts em seções (Languages, Files, Icons, Registry, Ini, Run, Types), script Pascal opcional, instalação com e sem administrador, desinstalação completa; diretiva `SignTool` define a ferramenta de assinatura para o instalador, o desinstalador (com `SignedUninstaller`) e os arquivos de origem; o marcador `$f` (nome do arquivo entre aspas) é obrigatório no comando; várias entradas `SignTool` rodam em ordem (assinatura dupla). Chaves silenciosas de Inno para o winget: `/SILENT` ou `/VERYSILENT` (V-43).
- **Conteúdo reutilizável (destilação própria):** checklist: (1) modo por usuário ou administrador definido; (2) desinstalação testada; (3) assinatura pelo `SignTool` com o comando vindo de variável de ambiente ou do store do sistema, sem senha literal (V-44); (4) switches silenciosos documentados; (5) instalador não assinado só em teste.
- **Ressalvas:** a sintaxe de cada seção não foi lida; a versão 7.1.0 vem do cabeçalho da ajuda e não foi cruzada com a página de downloads.
- **Verificação:** WebFetch das duas páginas e do texto da licença.

### V-42 — WiX Toolset: assinatura de MSI e bundles, taxa de manutenção e EULA (item do validador, fecha a lacuna 1 do complemento) — Classe B (7) · Prompt-score 78
- **Lente:** validador (lacuna que o pesquisador não conseguiu ler: só havia menu)
- **Tipo:** reference + checklist
- **Fonte:** https://docs.firegiant.com/wix/tools/signing/ · https://docs.firegiant.com/wix/osmf/ · **Autor/Org:** FireGiant (mantenedor do WiX)
- **Sinais:** documentação oficial atual; o corpo das duas páginas vem depois dos primeiros 100 mil caracteres de menu (li com `offset`). Sem data de página.
- **Técnicas-chave (Verificado):** MSI: assinar o `.msi` com `signtool` ou assinar gabinetes (cabs) externos e gravar as assinaturas no MSI; cabs embutidos não precisam de assinatura própria; `wix msi inscribe` registra as assinaturas dos cabs no MSI; com MSBuild, `SignOutput=true` e alvos `SignCabs` e `SignMsi`. Bundles: assinatura em duas partes: o motor Burn (`wix burn detach`, assinar, `wix burn reattach`) e depois o `.exe` inteiro; alvos `SignBundleEngine` e `SignBundle`. Taxa de manutenção (OSMF, introduzida no WiX v6): organizações com receita anual acima de US$ 10 mil devem patrocinar a organização do WiX no GitHub; o código-fonte segue livre sob o `LICENSE.TXT` do repositório. A partir do **WiX v7**, usar exige **aceitar o EULA** (`AcceptEula`, `-acceptEula` ou `wix eula accept wix7`).
- **Conteúdo reutilizável (destilação própria):** (1) decidir se o projeto cabe no OSMF e no EULA antes de adotar o WiX; (2) **a fábrica nunca aceita EULA nem termos em nome do usuário**: deixar o comando de aceite para ele; (3) assinar na ordem: cabs/MSI, depois o bundle; (4) verificar com `signtool verify /pa` (V-44).
- **Ressalvas:** a página de assinatura não trata de `insignia`, de timestamp nem de `wix build` (Verificado); cobertura de WiX v3/v4 não verificada; texto jurídico do EULA e do OSMF não lido além do resumo.
- **Verificação:** WebFetch das duas páginas com `offset: 100000`.

### V-43 — winget: manifesto, validação e submissão ao repositório comunitário (origem R-gap-14) — Classe A (9) · Prompt-score 86
- **Lente:** gapfill (authoritative)
- **Tipo:** checklist + workflow
- **Fonte:** https://learn.microsoft.com/en-us/windows/package-manager/package/manifest · https://learn.microsoft.com/en-us/windows/package-manager/package/repository · repositório https://github.com/microsoft/winget-pkgs · **Autor/Org:** Microsoft
- **Sinais:** manifesto `ms.date` 2026-09-14; repositório (página) `ms.date` 2024-11-21, `updated_at` 2026-07-14; `microsoft/winget-pkgs` 11.152★, MIT, push 2026-10-10 (Verificado).
- **Técnicas-chave (Verificado):** `ManifestVersion` 1.12.0; formato singleton (um instalador e uma localidade) ou múltiplo (mínimo 3 arquivos: version, defaultLocale, installer); campos mínimos: `PackageIdentifier` (Publisher.Package), `PackageVersion`, `PackageLocale`, `Publisher`, `PackageName`, `License`, `ShortDescription`, `Installers` (`Architecture`, `InstallerType`, `InstallerUrl`, `InstallerSha256`), `ManifestType`, `ManifestVersion`; ferramentas de criação: `wingetcreate` e `YAMLCreate.ps1` (ambas oferecem enviar o PR sozinhas); fluxo: `winget validate`, teste no Windows Sandbox com `Tools\SandboxTest.ps1`, fork, sparse checkout, branch, PR; um manifesto por submissão; pasta `manifests/<letra>/<publisher>/<app>/<versão>`; expectativas: URL vinda direto do publicador (sem redirecionador), HTTPS, instalação silenciosa, instalar e desinstalar como administrador e não administrador, hash correto; rótulos de erro: `Error-Hash-Mismatch`, `Validation-Indirect-URL`, `Validation-HTTP-Error`, `Validation-Domain`, `Validation-Unattended-Failed`, `Validation-Uninstall-Error`, `URL-Validation-Error`, `Binary-Validation-Error`; `Needs-Author-Feedback` fecha o PR após 10 dias sem resposta; "a Microsoft pode recusar qualquer submissão". Chaves silenciosas listadas: MSI `/q`, Inno `/SILENT` ou `/VERYSILENT`, Nullsoft `/S`.
- **Conteúdo reutilizável (destilação própria) — checklist de submissão:** (1) URL estável do fabricante em HTTPS; (2) SHA256 recalculado a cada release; (3) instalador silencioso testado; (4) desinstalação limpa; (5) `winget validate` antes do PR; (6) **o PR é ação externa pública: só com autorização explícita do usuário**.
- **Ressalvas:** a lista de tipos de instalador na página é um comentário de exemplo (exe, msi, msix, inno, wix, nullsoft, appx, font); a enumeração do esquema pode ter outros valores (não verificado). Políticas completas de conteúdo (`Policy-Test-2.x`) não lidas.
- **Verificação:** WebFetch das duas páginas e API do GitHub.

### V-44 — Assinatura no Windows: escolha de certificado, SmartScreen e SignTool; resolve o conflito EV (origem R-gap-15, R-gap-16; corrige V-17 e V-21) — Classe A (9) · Prompt-score 88
- **Lente:** gapfill (authoritative)
- **Tipo:** decision guide + checklist
- **Fonte:** https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options · https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation · https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool · **Autor/Org:** Microsoft Learn
- **Sinais:** `ms.date` 2026-08-29 (opções), 2026-05-04 (SmartScreen), 2024-11-21 com `updated_at` 2026-10-05 (SignTool) (Verificado).
- **Técnicas-chave (Verificado):** MSIX na Store: a Microsoft reassina, sem custo e sem aviso do SmartScreen; MSI ou EXE na Store: o publicador assina com certificado de uma CA do Programa de Raiz Confiável. Azure Artifact Signing (antigo Trusted Signing): cerca de US$ 9,99 por mês; organizações nos EUA, Canadá, UE e Reino Unido; indivíduos só nos EUA e Canadá; sem token físico; integra com CI; **não dá confiança instantânea no SmartScreen**. OV: US$ 150–300 por ano; desde junho de 2023 o CA/Browser Forum exige chave privada em HSM ou token. **EV: o bypass do SmartScreen foi removido em 2024; EV e OV constroem reputação do mesmo jeito; pagar a mais por EV só para evitar aviso "não se justifica mais"**. Reputação tem dois sinais: certificado do editor e hash do arquivo; arquivo sem assinatura recomeça do zero a cada versão; usar a mesma identidade de assinatura; não modificar o arquivo depois de assinar; não assinar programa potencialmente indesejado. Não há mecanismo de envio manual de reputação para o consumidor. Smart App Control no Windows 11 pode bloquear arquivos sem assinatura e sem reputação positiva. Auto-assinado: só desenvolvimento ou empresa com confiança distribuída por política. SignPath Foundation oferece assinatura gratuita para projetos de código aberto qualificados. SignTool: `sign` exige `/fd` (SHA256 recomendado) e, com `/tr`, também `/td`; `timestamp` sem `/td` só avisa; `verify /pa` usa a política de autenticação padrão e `/tw` avisa sem timestamp; códigos de saída 0, 1 e 2 (avisos). Os exemplos oficiais usam `/p` com senha literal.
- **Conflito resolvido (V-17 versus V-21 versus Electron):** a página do Electron (lida de novo agora) ainda diz que "desde junho de 2023 a Microsoft exige certificado EV" e que a assinatura em nuvem "elimina os avisos do SmartScreen". As duas páginas da Microsoft de 2026 dizem o contrário (HSM para OV; EV sem bypass; Artifact Signing sem confiança instantânea). **Decisão:** a Microsoft é fonte primária e prevalece; "EV obrigatório" fica **refutado**; o Tauri só diz que seu guia vale para OV obtidos antes de 1/6/2023.
- **Conteúdo reutilizável (destilação própria) — decisão para o plugin:** (1) MSIX na Store se possível; (2) senão Azure Artifact Signing quando a região permitir; (3) senão OV com HSM ou assinatura em nuvem; (4) não exigir EV por causa do SmartScreen; (5) mesma identidade em toda release; (6) `signtool sign /fd SHA256 /tr <url> /td SHA256 ...` e depois `signtool verify /pa`; (7) senha nunca em argumento: usar store do sistema, KSP/nuvem ou variável de ambiente do CI; (8) avisar o usuário de que a primeira release pode mostrar aviso do SmartScreen.
- **Ressalvas:** preços e regiões mudam e foram lidos como estão na página; não são verificados em site de preços.
- **Verificação:** WebFetch das três páginas e da página de assinatura do Electron; comparação linha a linha das afirmações em conflito.

### V-45 — Notarização no macOS: requisitos da Apple, Tauri e `macdeployqt` (origem R-gap-18; Apple lida pelo validador) — Classe B (7) · Prompt-score 82
- **Lente:** gapfill (authoritative)
- **Tipo:** checklist
- **Fonte:** https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution (corpo obtido pelo endpoint de dados `https://developer.apple.com/tutorials/data/documentation/security/notarizing-macos-software-before-distribution.json`, porque a página HTML só devolve o título) · https://v2.tauri.app/distribute/sign/macos/ · https://doc.qt.io/qt-6/macos-deployment.html · **Autor/Org:** Apple; projeto Tauri; Qt
- **Técnicas-chave (Verificado):** a notarização é verificação automatizada (não é App Review) que gera um ticket para grampear (staple) no software; software assinado com novo certificado Developer ID precisa ser notarizado a partir do macOS 10.14.5 e o distribuído com Developer ID e compilado depois de 1/6/2019, a partir do macOS 10.15. Requisitos: assinatura válida em todos os executáveis; certificado **Developer ID** (não Mac Distribution, ad hoc, Apple Developer nem local); Hardened Runtime em apps e alvos de linha de comando; timestamp seguro; **sem** a entitlement `com.apple.security.get-task-allow` verdadeira; entitlements em XML ASCII; plugins herdam as entitlements do host. Ferramentas citadas pela Apple: `notarytool` e `stapler`, incluídas no Xcode; fluxo alternativo pelo Organizer; a Apple recomenda revisar o log do serviço. Tauri: certificado "Developer ID Application" (só o Account Holder o cria); duas vias de notarização por variáveis de ambiente: chave de API do App Store Connect (`APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH`) ou Apple ID (`APPLE_ID`, `APPLE_PASSWORD`, `APPLE_TEAM_ID`); em CI o `.p12` em base64 (`APPLE_CERTIFICATE`, `APPLE_CERTIFICATE_PASSWORD`); assinatura ad hoc (`"-"`) não evita a aprovação do usuário em Privacidade e Segurança. Qt: ver V-38.
- **Conteúdo reutilizável (destilação própria):** (1) Developer ID + Hardened Runtime + timestamp; (2) conferir entitlements; (3) submeter ao serviço de notarização com a ferramenta oficial, ler o log, grampear o ticket; (4) testar em máquina limpa; (5) credenciais só por variáveis de ambiente do CI ou chaveiro, nunca no repositório nem em argumento de linha de comando; (6) **submeter, aceitar termos de conta ou criar certificado é ação do usuário**, não da fábrica.
- **Ressalvas:** a página da Apple não traz sintaxe de comando (só os nomes das ferramentas). A sintaxe `notarytool submit --wait`, `store-credentials` e `stapler staple` que circula nas respostas de ferramentas veio de conhecimento geral do modelo da ferramenta de leitura, **não** da Apple: **Não verificado**, conferir `xcrun notarytool --help` na versão instalada. A página da Tauri não trata de Hardened Runtime nem de entitlements (Verificado).
- **Verificação:** WebFetch do endpoint de dados da Apple (texto completo), da página da Tauri e da Qt; as duas outras páginas da Apple do pesquisador seguem sem corpo em HTML.

### V-46 — Tauri v2: assinatura no Windows e no macOS, e Store (origem R-gap-17; corrige partes de V-21) — Classe A (8) · Prompt-score 80
- **Lente:** gapfill (authoritative)
- **Tipo:** checklist + config-template
- **Fonte:** https://v2.tauri.app/distribute/sign/windows/ · https://v2.tauri.app/distribute/windows-installer/ · https://v2.tauri.app/distribute/microsoft-store/ · **Autor/Org:** projeto Tauri
- **Sinais:** `tauri-apps/tauri` 111.721★, Apache-2.0, push 2026-10-10 (Verificado). Páginas sem data.
- **Técnicas-chave (Verificado):** `tauri.conf.json` > `bundle` > `windows`: `certificateThumbprint`, `digestAlgorithm`, `timestampUrl`; `signCommand` para assinar a partir de outro sistema (Azure Key Vault com `relic`, Artifact Signing com `artifact-signing-cli`); em CI, `.pfx` em base64 em segredo, com senha em outro segredo; a página diz que o guia **só vale para certificados OV obtidos antes de 1/6/2023**. Formatos de instalador no Windows: MSI (pelo WiX v3, segundo a página) e NSIS (`-setup.exe`); a página de instaladores não menciona MSIX. Guia da Store: Tauri só gera EXE e MSI; no Partner Center o app entra como "EXE ou MSI"; instalador offline, assinado, silencioso (`/S` no NSIS, `/quiet` no MSI), com WebView2 em modo offline.
- **Conteúdo reutilizável (destilação própria):** etapa de CI para Windows: importar certificado de segredo; `signCommand` com timestamp; verificar com `signtool verify /pa` (V-44); tratar EV/OV posteriores a junho de 2023 como assunto da CA (V-44).
- **Ressalvas:** **a ordem Authenticode versus assinatura do updater continua sem fonte oficial**: a página do updater (V-20) não cita Authenticode e a de assinatura não cita o updater (Verificado). Fica como hipótese a testar (V-21). Cópia de exemplo com `Import-PfxCertificate` exige senha: usar segredo de CI.
- **Verificação:** WebFetch das quatro páginas Tauri (assinatura Windows, macOS, instaladores, Store) e da página do updater.

### V-47 — Tauri v2: isolation pattern e Content Security Policy (origem R-gap-20, R-gap-21; complementa V-19) — Classe A (8) · Prompt-score 84
- **Lente:** gapfill (authoritative)
- **Tipo:** pattern + config-template
- **Fonte:** https://v2.tauri.app/concept/inter-process-communication/isolation/ · https://v2.tauri.app/security/csp/ · **Autor/Org:** projeto Tauri
- **Técnicas-chave (Verificado):** isolation: um `<iframe>` em sandbox roda a "Isolation application" que intercepta a mensagem IPC antes do core Rust; a mensagem é cifrada com AES-GCM com chave gerada em tempo de execução; `app.security.pattern` com `"use": "isolation"` e `options.dir` apontando para o diretório da isolation app; manter a isolation app mínima; no Windows arquivos externos não carregam no iframe (o build injeta scripts inline) e módulos ES não funcionam. CSP: só é ativada se estiver na configuração do Tauri; `default-src` restrito (exemplo da página: `'self' customprotocol: asset:`); `connect-src` com `ipc: http://ipc.localhost`; hashes para scripts locais e nonces para estilos e scripts externos são acrescentados no build; `'wasm-unsafe-eval'` em `script-src` para WebAssembly; evitar conteúdo remoto como CDN.
- **Conteúdo reutilizável (destilação própria) — checklist:** (1) isolation ligada quando o frontend usa dependências de terceiros; (2) no hook, validar caminhos de arquivo (dentro de pastas esperadas) e a origem das requisições; (3) CSP definida, `default-src` restrito, sem CDN; (4) `connect-src` mínimo; (5) toda exceção justificada por escrito; (6) isolation + CSP não substituem capabilities (V-19).
- **Ressalvas:** **Correção:** `window.__TAURI_ISOLATION_HOOK__` aparece só no código de exemplo da página, não em texto formal; tratar como detalhe de implementação a conferir na versão usada. O overhead de criptografia "pequeno" não é medido. A URL `/security/isolation/` do pesquisador deu 404; a página certa é a acima.
- **Verificação:** WebFetch das duas páginas (cada ponto conferido).

### V-48 — Electron Fuses (`@electron/fuses`) (origem R-gap-19) — Classe B (7) · Prompt-score 80
- **Lente:** gapfill (github)
- **Tipo:** checklist + config-template (somente leitura e recomendação)
- **Fonte:** https://github.com/electron/fuses · **Autor/Org:** projeto Electron
- **Sinais:** `electron/fuses` 54★, MIT, push 2026-10-10 (Verificado); organização oficial do Electron.
- **Técnicas-chave (Verificado):** nove fuses no README: `RunAsNode`, `EnableCookieEncryption`, `EnableNodeOptionsEnvironmentVariable`, `EnableNodeCliInspectArguments`, `EnableEmbeddedAsarIntegrityValidation`, `OnlyLoadAppFromAsar`, `LoadBrowserProcessSpecificV8Snapshot`, `GrantFileProtocolExtraPrivileges`, `WasmTrapHandlers`. A página não declara padrões. Aplicar com `flipFuses` **depois** de empacotar e **antes** de assinar (gancho `afterPack` do electron-builder, `postPackage` ou `packageAfterCopy` do Forge); `strictlyRequireAllFuses` falha o build se faltar fuse; macOS arm64 sem assinatura logo em seguida exige `resetAdHocDarwinSignature: true`, senão o app falha a validação de assinatura.
- **Conteúdo reutilizável (destilação própria) — valores a recomendar (Inferido pelo significado de cada fuse; conferir o README da versão usada):** `RunAsNode` desligado; `EnableNodeOptionsEnvironmentVariable` desligado; `EnableNodeCliInspectArguments` desligado; `GrantFileProtocolExtraPrivileges` desligado; `EnableCookieEncryption`, `OnlyLoadAppFromAsar` e `EnableEmbeddedAsarIntegrityValidation` **ligados** (a integridade exige configuração de asar; o texto lido a descreve para macOS). `LoadBrowserProcessSpecificV8Snapshot` e `WasmTrapHandlers` conforme a necessidade.
- **Correção importante:** o pesquisador escreveu que `OnlyLoadAppFromAsar` deve ficar "desligado". O fuse **restringe o carregamento ao `app.asar`**; o valor seguro é **ligado**. Também citou só 5 dos 9 fuses.
- **Ressalvas:** a fábrica **não executa** `npx @electron/fuses` (código de terceiros baixado); só lê e recomenda. Item 19 da checklist V-16 remete a este.
- **Verificação:** WebFetch do README (lista de fuses, ganchos, opções, licença) e API do GitHub.

### V-49 — Sparkle (auto-update no macOS) (origem R-gap-22) — Classe A (8) · Prompt-score 80
- **Lente:** gapfill (authoritative)
- **Tipo:** reference + checklist
- **Fonte:** https://sparkle-project.org/documentation/ · repositório https://github.com/sparkle-project/Sparkle · **Autor/Org:** projeto Sparkle
- **Sinais:** 9.823★, push 2026-10-04 (Verificado). **Licença: MIT** no arquivo `LICENSE` (Verificado), com componentes incluídos sob BSD e zlib (bsdiff/bspatch, SUSignatureVerifier, Ed25519); a API do GitHub devolve "NOASSERTION" (**Correção:** o pesquisador não tinha a licença).
- **Técnicas-chave (Verificado):** feed (appcast) em XML na URL de `SUFeedURL` no `Info.plist`; chaves EdDSA geradas com `generate_keys` (privada no chaveiro do login; pública em `SUPublicEDKey`); `generate_appcast` gera o appcast e arquivos `.delta`; `SURequireSignedFeed` assina feed e notas e exige `SUVerifyUpdateBeforeExtraction` (feed assinado é validado a partir do Sparkle 2.9); notas de lançamento em `.md` a partir do 2.9 e macOS 12; HTTPS e notarização com Developer ID são **recomendações**, não exigências; atualização delta é ignorada se o app não bater o checksum.
- **Conteúdo reutilizável (destilação própria):** (1) EdDSA e chave privada fora do repositório; (2) appcast por HTTPS; (3) app assinado e notarizado (V-45); (4) feed assinado; (5) testar atualização da versão anterior; (6) comparar com os updaters do Electron (V-18) e do Tauri (V-20).
- **Ressalvas:** versões citadas (2.9) mudam; conferir a versão instalada. A fábrica não instala o Sparkle nem roda `generate_keys` (gera segredo).
- **Verificação:** WebFetch da documentação (nove pontos) e do arquivo `LICENSE`.

### V-50 — Claude Code: testar plugins com evals e medir custo e uso (origem R-gap-27, R-gap-28) — Classe A (9) · Prompt-score 88
- **Lente:** gapfill (authoritative)
- **Tipo:** workflow + checklist + metric guide
- **Fonte:** https://code.claude.com/docs/en/plugin-evals · https://code.claude.com/docs/en/plugins/measure · **Autor/Org:** Anthropic
- **Sinais:** páginas oficiais atuais (Verificado). Evals exigem Claude Code v2.1.269 ou posterior.
- **Técnicas-chave (Verificado) — evals:** `claude plugin eval` (no shell, não no prompt); `claude plugin eval init` propõe casos e graders; caso = prompt realista + graders; seis tipos de grader: `regex`, `tool_used`, `tool_order`, `file_exists` (calculados, sem custo) e `llm` e `baseline` (juiz de modelo, com custo); cada caso roda 3 vezes por padrão (1 a 50 com `--runs`), score = fração de graders aprovados, ponderável; caso passa se o score atinge `--threshold` (padrão 1.0) e qualquer caso abaixo faz o comando sair com código 1; baseline sem o plugin (`--ablation`) mostra o ganho `Δ`; diagnóstico típico: `Δ` perto de zero com `tool_used: Skill` reprovando = descrição que não casa com a fala natural; relatório `report.html` autocontido; o formato de `skill-creator` (`evals/evals.json`) não é compatível. Boas práticas da página: um grader sobre o resultado e outro sobre o caminho (`tool_used`, `tool_order`); `regex` sobre o conteúdo de arquivos longos; `llm` só para saídas curtas, com rubrica de condições PASS e FAIL concretas; suspeitar do juiz antes do plugin quando `Δ` for negativo com `tool_used` passando. **Custo/uso:** `claude plugin details <nome>` (no shell) mostra inventário e custo estimado "always-on" (nome + `description` + `when_to_use` de skills, agentes e comandos) e "on-invoke" (corpo carregado ao disparar); hooks e MCP não têm estimativa (MCP: `/context`); a linha "Every turn" fica destacada a partir de 2.000 tokens no `/plugin` do marketplace oficial; `/plugin` move para "Not used recently" após 14 dias **e** 10 sessões sem uso; `/skill-doctor`, `/doctor`, `/usage`; eventos OTEL `plugin_installed`, `plugin_loaded`, `skill_activated`; nomes de plugins de terceiros são redigidos, salvo `OTEL_LOG_TOOL_DETAILS=1`.
- **Conteúdo reutilizável (destilação própria) — etapa de teste da fábrica:** (1) um caso por skill com `tool_used: Skill` e um `regex` sobre a saída; (2) `file_exists` para artefatos; (3) `--threshold` em CI (por exemplo 0,8); (4) rodar `claude plugin details` antes de publicar e encurtar descrições se o always-on passar de 2.000 tokens; (5) depois de encurtar descrição, repetir os graders `tool_used` (descrição menor pode parar de disparar); (6) **evals gastam tokens** (casos × runs × 2 braços): o usuário autoriza a execução.
- **Ressalvas:** custos são estimativas ("podem diferir do uso real"). Os eventos de telemetria interessam a administradores, não ao autor individual.
- **Verificação:** WebFetch das duas páginas; `measure` lida por inteiro; `plugin-evals` conferida por busca de termos no arquivo salvo.

### V-51 — Claude Code: sandbox, permissões e página de segurança (origem R-gap-24, R-gap-25, R-gap-26) — Classe A (9) · Prompt-score 88
- **Lente:** gapfill (authoritative)
- **Tipo:** reference + checklist
- **Fonte:** https://code.claude.com/docs/en/sandboxing · https://code.claude.com/docs/en/permissions · https://code.claude.com/docs/en/security · **Autor/Org:** Anthropic
- **Técnicas-chave (Verificado) — sandbox:** roda em macOS, Linux e WSL2; **no Windows nativo os comandos rodam sem sandbox**; cobre Bash, PowerShell e Monitor e seus processos filhos; **fora do sandbox**: Read, Edit, Write, WebFetch, WebSearch, hooks de comando, servidores MCP locais, monitores de plugin, servidores LSP, status line e `apiKeyHelper` (rodam com acesso total do usuário); `denyRead` não bloqueia a ferramenta Read e `allowedDomains` não limita o WebFetch; rede passa por proxy com `network.allowedDomains` (começa vazio); `excludedCommands` roda **fora** do sandbox e um padrão largo (`docker *`) deixa Claude escrever um arquivo e executá-lo fora; repetição sem sandbox é desligada por `"allowUnsandboxedCommands": false`, e `failIfUnavailable` impede rodar sem sandbox quando ele não sobe; `sandbox.filesystem.disabled: true` (v2.1.216+) mantém só a rede e afrouxa a proteção. **Permissões:** ordem de avaliação deny, depois ask, depois allow (o primeiro que casar decide; allow específico não abre exceção em deny); `bypassPermissions` pula prompts, inclusive em caminhos protegidos como `.git` e `.claude`, e só deve ser usado em contêiner ou VM; `permissions.disableBypassPermissionsMode` e `disableAutoMode`; `Bash(command:rm *)` é ignorado com aviso (contornável por comando composto); regra de Bash casa o texto escrito e **não é fronteira de segurança**; PowerShell: aliases são canonizados (`gci`, `ls`, `dir` casam com `Get-ChildItem`), sem diferença de caixa; caminho UNC (`\\servidor\pasta`) pede aprovação porque pode vazar credencial; no Windows os caminhos são normalizados para POSIX (`//c/**/.env`); a decisão `allow` de um hook `PreToolUse` **não** vence deny nem ask; um hook que sai com código 2 bloqueia mesmo com regra allow. **Segurança:** modo automático usa um classificador separado e respeita regras explícitas; modo manual começa só com leitura; `curl` e `wget` não são aprovados automaticamente; falha fechada; detecção de injeção em comando que não pode ser analisado; diálogo de confiança de pasta e aprovação própria de `.mcp.json` (sessão `-p` não mostra nenhum dos dois); aviso de WebDAV e `\\*` no Windows; a Anthropic revisa conectores para o diretório, mas **não audita nem gerencia servidores MCP**; plugins também podem adicionar servidores MCP.
- **Conteúdo reutilizável (destilação própria) — nota de segurança do plugin e bloco de permissões:** (1) "o sandbox não cobre hooks nem MCP; no Windows nativo use WSL2 para isolar Bash"; (2) `deny` para `Read(./.env)`, `Read(./secrets/**)`, `Bash(rm -rf *)`, `Bash(git push --force *)`; `ask` para `Bash(git push *)`; regras de rede com deny ou ask mais allowlist do sandbox; (3) plugin da fábrica sem hooks de comando ativos, sem `.mcp.json` e sem `bin/` (V-01, V-02); (4) conteúdo não confiável não vai direto ao prompt.
- **Ressalvas:** versões mínimas variam por recurso; conferir `claude --version`. A página de permissões é longa; li por busca de termos e pelo texto salvo, não palavra por palavra.
- **Verificação:** WebFetch das três páginas; afirmações conferidas contra o texto salvo.

### V-52 — Claude Code: referência de hooks (origem R-gap-23; complementa V-08) — Classe A (9) · Prompt-score 86
- **Lente:** gapfill (authoritative)
- **Tipo:** reference
- **Fonte:** https://code.claude.com/docs/en/hooks · **Autor/Org:** Anthropic
- **Sinais:** página oficial atual, 262.610 caracteres; li os primeiros 100.000 (restam 162.610, entre eles a seção de privilégios).
- **Técnicas-chave (Verificado):** cinco tipos de handler: `command`, `http`, `mcp_tool`, `prompt` e `agent` (este marcado como experimental); código de saída 2 bloqueia nos eventos que podem bloquear (`PreToolUse`, `UserPromptSubmit`, `Stop`, `PreCompact`) e o stderr vira o motivo; em `PostToolUse` só mostra o stderr ao Claude; **exit 2 vence até `permissionDecision: "allow"` no JSON**; qualquer outro código (como 1), sem JSON válido, **não bloqueia**; se houver JSON válido no stdout, os campos decidem; `onFailure: "block"` em hooks `command` ou `http` (v2.1.295+) transforma falha (não inicia, código diferente de 0 e 2, rede, timeout, saída inválida) em bloqueio; timeout vencido em `PreToolUse` **não** bloqueia sem `onFailure: "block"`; `PermissionRequest` não honra exit 2 (negar com `hookSpecificOutput.decision.behavior: "deny"`); timeouts padrão: `command`, `http` e `mcp_tool` 600 s (30 s em `UserPromptSubmit` e nos eventos de troca de modelo; 10 s em `MessageDisplay`), `prompt` 30 s, `agent` 60 s; matcher: `*`, vazio ou omitido casa tudo; só letras, dígitos, `_`, `-`, espaço, `,` e `|` dão nome exato ou lista; qualquer outro caractere vira regex JavaScript **sem âncora** (`Edit.*` também casa `NotebookEdit`; usar `^Edit$`); `PreToolUse` decide com `hookSpecificOutput.permissionDecision` em `allow`, `deny`, `ask` ou `defer`; silêncio (exit 0 sem JSON) não aprova: segue o fluxo normal de permissão.
- **Conteúdo reutilizável (destilação própria) — template de guardrail:** `PreToolUse`, matcher exato `Bash`, política em código que sai com 2 e escreve o motivo no stderr; `onFailure: "block"` para falha fechada; testar com `claude --debug`; lembrar que hook não é fronteira de segurança (V-51, V-27).
- **Ressalvas:** a seção de privilégios dos hooks (final da página) **continua não lida**. A semântica de `defer` não foi confirmada além da tabela de decisão. **Correção sutil a V-08:** a compreensão de "exit 1 não bloqueia" está certa e agora tem a citação do exemplo oficial da página.
- **Verificação:** WebFetch com oito pontos confirmados.

### V-53 — Claude Code: criar plugin, componentes e depuração (origem R-gap-29; complementa V-01) — Classe A (9) · Prompt-score 86
- **Lente:** gapfill (authoritative)
- **Tipo:** workflow + checklist
- **Fonte:** https://code.claude.com/docs/en/plugins/create · https://code.claude.com/docs/en/plugins/components · **Autor/Org:** Anthropic
- **Técnicas-chave (Verificado):** só `plugin.json` fica em `.claude-plugin/`; `skills/`, `agents/`, `hooks/hooks.json` e `.mcp.json` ficam na raiz; sem manifesto, o plugin carregado por `--plugin-dir` recebe o nome da pasta; skills de plugin ganham o prefixo `/plugin:skill`; `claude plugin validate <caminho>` checa o manifesto e o frontmatter (`--strict` falha em aviso); teste local: `claude --plugin-dir ./meu-plugin` (também aceita `.zip` e, com v2.1.265+, uma pasta de plugins); `/reload-plugins` aplica edições; aba **Errors** de `/plugin` e `claude plugin list` mostram falhas de carga; `claude plugin init <nome>` cria o plugin em `~/.claude/skills/<nome>/` e ele carrega em toda sessão; `--plugin-url` baixa um `.zip` ("apontar só para arquivos que você controla ou confia"); `CLAUDE_CODE_PLUGIN_DIRS` exige v2.1.280+ e a configuração gerenciada pode desligar essas flags; hooks migrados sem apagar o original rodam duas vezes; monitores de plugin não iniciam em modo `-p`. **Agentes de plugin:** campos aceitos `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, `omitClaudeMd`, `isolation` (só `"worktree"`), `color`; **campos ignorados** `permissionMode`, `hooks`, `mcpServers` e `initialPrompt`; frontmatter que não analisa faz o agente carregar com todos os campos ignorados. O plugin oficial `plugin-dev` é apontado como ajuda para criar e validar (V-54).
- **Conteúdo reutilizável (destilação própria) — checklist de scaffold:** (1) manifesto; (2) componentes na raiz; (3) `validate --strict`; (4) `--plugin-dir` e `/reload-plugins`; (5) aba Errors limpa; (6) gatilho de `claude plugin eval` (V-50); (7) agentes sem campos ignorados.
- **Ressalvas:** os campos completos de cada componente (hooks, LSP, `userConfig`) não foram lidos linha a linha por mim.
- **Verificação:** WebFetch de `create` (por inteiro) e `components` (busca de termos no texto salvo).

### V-54 — `plugin-dev` (Anthropic): agentes `plugin-validator` e `skill-reviewer` (origem R-gap-42) — Classe A (8) · Prompt-score 75 (fonte `plugin-validator`) / 73 (fonte `skill-reviewer`) / 84 (checklist reescrita)
- **Lente:** gapfill (github)
- **Tipo:** subagent (estudo e reescrita)
- **Fonte:** https://github.com/anthropics/claude-plugins-official/tree/main/plugins/plugin-dev · arquivos `agents/plugin-validator.md` e `agents/skill-reviewer.md` · **Autor/Org:** Anthropic
- **Sinais:** repositório 37.607★, Apache-2.0, push 2026-10-09 (Verificado). **Conflito de licença resolvido:** o README da pasta diz "MIT License", mas o arquivo `LICENSE` da pasta (e o da raiz) é **Apache-2.0** (Verificado nos arquivos). O arquivo de licença prevalece; V-01 estava certo. A pasta tem 7 skills (`hook-development`, `mcp-integration`, `plugin-structure`, `plugin-settings`, `command-development`, `agent-development`, `skill-development`), 3 agentes (`agent-creator`, `plugin-validator`, `skill-reviewer`) e o comando `/plugin-dev:create-plugin` (8 fases).
- **Pontuação dos prompts-fonte (D1–D12, resumo estruturado):** `plugin-validator` 75: D3 5, D6 5, D7 4, D11 4, D8 3 (Bash para rodar scripts de validação cujo conteúdo não vi; sem cláusula de tratar conteúdo externo como dado), D12 3 (foco em `commands`, convenções da versão antiga). `skill-reviewer` 73: D8 5 (só Read, Grep, Glob), D6 5, D12 2 (**afirma que `when_to_use` está obsoleto, mas a página oficial `plugins/measure` conta `when_to_use` no custo always-on**: está em uso; faixas de tamanho inconsistentes: "1.000 a 3.000 palavras" e "menos de 3.000 idealmente"; limites de 50 a 500 caracteres na descrição não conferidos com a doc atual). Nenhum dispara critério de reprovação.
- **Conteúdo reutilizável (destilação própria) — checklist de validação de plugin (10 passos, somente leitura):** (1) achar a raiz (`.claude-plugin/plugin.json`); (2) manifesto: `name` kebab-case sem prefixos reservados, `version` semver, campos opcionais coerentes; (3) estrutura e descoberta automática; (4) skills: `SKILL.md`, frontmatter, arquivos referenciados existem; (5) agentes: campos aceitos e **nenhum** dos ignorados (V-53); (6) hooks: JSON válido, evento, matcher, caminho do script; (7) MCP: transporte e uso de `${CLAUDE_PLUGIN_ROOT}`; (8) organização: README, LICENSE, sem `node_modules` nem `.DS_Store`; (9) segurança: segredos no código, HTTP em vez de HTTPS, hooks de risco (V-02); (10) saída com severidades, arquivo e linha, correção sugerida, achados positivos e veredito PASS/FAIL. Para skills: avaliar gatilhos da descrição, corpo enxuto, divulgação progressiva e referências que existem, e medir o custo com `claude plugin details` (V-50).
- **Ressalvas:** só li um resumo estruturado dos dois agentes, não o texto integral; os scripts `validate-agent.sh` e `validate-hook-schema.sh` não foram vistos e a fábrica não os executa sem revisão.
- **Verificação:** WebFetch da pasta, da lista de agentes e dos dois arquivos; arquivos `LICENSE` lidos.

### V-55 — `claude-code-setup`, `mcp-server-dev` e `skill-creator` (Anthropic) (origem R-gap-43 e lacuna 14) — Classe A (8) · Prompt-score 70 (`claude-automation-recommender`) / 85 (`build-mcp-server`, provisório) / 80 (nota reescrita)
- **Lente:** gapfill (github)
- **Tipo:** skill (estudo)
- **Fonte:** https://github.com/anthropics/claude-plugins-official/tree/main/plugins/claude-code-setup · `.../mcp-server-dev` · `.../skill-creator` · **Autor/Org:** Anthropic
- **Sinais:** licença Apache-2.0 verificada para o `LICENSE` da raiz e o de `skill-creator`; os `LICENSE` de `claude-code-setup` e `mcp-server-dev` **não foram lidos** (existem).
- **O que cada um faz (Verificado):** `claude-code-setup` traz a skill `claude-automation-recommender`: lê o projeto e recomenda 1–2 automações por categoria (servidores MCP, skills, hooks, subagentes, comandos); declara-se **somente leitura**; fases de análise, recomendação e relatório. `mcp-server-dev` traz `build-mcp-server` (porta de entrada: descoberta em 5 perguntas, escolha de implantação e de padrão de tool, encaminha a `build-mcp-app` ou `build-mcpb`), com referências para autenticação (DCR/CIMD), descrição de tools, widgets, esquemas e endurecimento de segurança. `skill-creator` cria, melhora e mede skills com evals e análise de variância (só o README foi lido).
- **Pontuação:** `claude-automation-recommender` 70: D4 5, D6 4, D8 4 (declara somente leitura), D7 2 (nada pede verificar as recomendações), D12 3, **inconsistência:** manda usar busca na web, mas as `tools` não incluem a ferramenta de busca (e inclui Bash). `build-mcp-server` 85 (provisório; resumo): D1 5, D3 5, D9 5 (divulgação progressiva em referências), D10 5, D8 4 (cobre injeção e anotações de leitura e escrita nos critérios de revisão).
- **Conteúdo reutilizável (destilação própria):** (1) **padrão de recomendador**: perfil do projeto, 1–2 recomendações por categoria com justificativa e local de instalação, tudo só leitura, o usuário aplica; (2) **decisão de servidor MCP**: serviço em nuvem → HTTP remoto (padrão); precisa tocar a máquina do usuário → pacote MCPB; stdio local só para protótipo pessoal; poucas ações (menos de uns 15) → uma tool por ação; API grande → busca mais execução; OAuth exige servidor remoto com DCR ou CIMD; conferir se o host suporta elicitation e ter alternativa.
- **Ressalvas:** a fábrica não instala nem ativa esses plugins; só estuda. Para nós, qualquer MCP continua desligado na base (V-02).
- **Verificação:** WebFetch das três pastas, do `SKILL.md` do recomendador e do `build-mcp-server`; licenças.

### V-56 — Guia de prompting da plataforma Claude: calibração das dimensões D2, D4, D8 e D10 (origem R-gap-30) — Classe A (9) · Prompt-score 88
- **Lente:** gapfill (authoritative)
- **Tipo:** reference + calibração da rubrica
- **Fonte:** https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices · **Autor/Org:** Anthropic
- **Sinais:** guia oficial atual; abre listando os modelos atuais (Fable 5.1, Mythos 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5, entre outros). Li por busca de termos no texto salvo (66 KB), não por inteiro.
- **Técnicas-chave (Verificado):** dar o motivo da instrução ajuda o modelo a entender o objetivo (apoia **D2**); etiquetas XML separam instruções, contexto, exemplos e entradas (apoia **D4**); modelos recentes respondem mais ao system prompt: onde antes se escrevia "CRITICAL: You MUST use this tool when…", basta "Use this tool when…", e a correção do excesso de gatilho é **reduzir a linguagem agressiva** (apoia **D10**); e há um texto sugerido de **reversibilidade**: ações locais e reversíveis (editar arquivos, rodar testes) podem seguir; ações difíceis de reverter, que afetam sistemas compartilhados ou destrutivas (apagar arquivos ou branches, `rm -rf`, `git push --force`, `git reset --hard`, amendar commits publicados) pedem confirmação; não usar ação destrutiva como atalho, não contornar verificações (por exemplo `--no-verify`) e não descartar arquivos desconhecidos (apoia **D8**).
- **Correção importante à rubrica sugerida pelo pesquisador:** ele escreveu "ênfase (D8)" e "ação irreversível (D10)". Na rubrica da casa é o contrário: **D10 = calibração de linguagem (ênfase, CAPS, "CRITICAL")** e **D8 = escopo, autonomia e segurança (confirmação antes de ação irreversível)**.
- **Conteúdo reutilizável (destilação própria) — calibração:** D10: penalizar CAPS e "MUST/CRITICAL/NEVER" usados para forçar disparo, preferir "faça X quando Y"; remover "na dúvida, use a ferramenta"; D8: exigir a cláusula de confirmação com lista de exemplos de ação irreversível e a regra de não contornar verificações; D2: exigir o porquê das regras; D4: exigir separação entre instrução, dado e exemplo.
- **Ressalvas:** os comportamentos de excesso de gatilho são descritos para modelos específicos (Opus 4.5 e 4.6 em destaque); modelos novos podem reagir diferente. Seção de exemplos (few-shot) não lida por inteiro.
- **Verificação:** WebFetch do guia; busca de termos nas linhas 63, 95–97, 491, 882–894 do texto salvo.

### V-57 — PowerShell: `ShouldProcess`, `-WhatIf`, `-Confirm` e `-Force` (origem R-gap-31) — Classe A (8) · Prompt-score 88
- **Lente:** gapfill (authoritative)
- **Tipo:** pattern + checklist
- **Fonte:** https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess · **Autor/Org:** Microsoft Learn (texto original de Kevin Marquette, creditado)
- **Sinais:** `ms.date` 2024-09-24, `updated_at` 2026-05-27; vale de Windows PowerShell 5.1 a 7.x (monikers da página) (Verificado).
- **Técnicas-chave (Verificado):** `[CmdletBinding(SupportsShouldProcess)]` cria `-WhatIf` e `-Confirm` (não criar parâmetro manual nem checar `$WhatIf`); `$PSCmdlet.ShouldProcess('alvo', 'operação')` o mais perto possível da mudança e dentro do laço, para executar o máximo de código no modo simulação; com `-WhatIf` devolve falso e imprime "What if:"; `ConfirmImpact` (High, Medium, Low, None) é comparado com `$ConfirmPreference` (padrão **High**) e o padrão de `ConfirmImpact` é **Medium**, então só `High` pede confirmação sem `-Confirm`; `-Confirm` coloca `$ConfirmPreference` em `Low` no escopo; `ShouldContinue` ignora `-WhatIf`, `-Confirm` e as preferências e sempre pergunta; `-Force` próprio: `if ($Force -and -not $PSBoundParameters.ContainsKey('Confirm')) { $ConfirmPreference = 'None' }`, mantendo `-WhatIf` prioritário e **nunca** pondo `$Force` dentro do `if` do `ShouldProcess`; chamadas internas: `-Confirm:$false` depois do prompt tratado e `-WhatIf:$WhatIfPreference` explícito; limite conhecido: `-WhatIf` e `-Confirm` **não atravessam** um módulo de script que chama outro módulo de script.
- **Conteúdo reutilizável (destilação própria) — checklist de script da fábrica:** `[CmdletBinding(SupportsShouldProcess, ConfirmImpact='High')]` em qualquer função que apague, mova, publique ou instale; chamadas a `Remove-Item` e semelhantes com `-WhatIf:$WhatIfPreference`; teste Pester que roda a função com `-WhatIf` e prova que nada mudou; nada de `ShouldContinue` em script que outros scripts chamam.
- **Ressalvas:** não cobre `ShouldProcess` em cmdlet compilado (só script). Corrige a lacuna de V-15.
- **Verificação:** WebFetch da página inteira.

### V-58 — PSScriptAnalyzer e Pester (origem R-gap-32, R-gap-33) — Classe A (8) · Prompt-score 82
- **Lente:** gapfill (authoritative)
- **Tipo:** tool reference + checklist
- **Fonte:** https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/overview · https://pester.dev/docs/quick-start · https://pester.dev/docs/introduction/installation · **Autor/Org:** Microsoft (PSScriptAnalyzer); projeto Pester
- **Sinais:** `PowerShell/PSScriptAnalyzer` 2.169★, MIT, push 2026-09-22; `pester/Pester` 3.356★, **Apache-2.0** (arquivo `LICENSE` lido; a API mostra "NOASSERTION"), push 2026-10-01; página do analisador `ms.date` 2026-03-20 (Verificado).
- **Técnicas-chave (Verificado):** PSScriptAnalyzer: verificador estático com regras embutidas (variáveis não inicializadas, uso do tipo `PSCredential`, `Invoke-Expression` e outras), inclusão e exclusão de regras, formatação de código; suporta Windows PowerShell 5.1 ou posterior e PowerShell 7.2.11 ou posterior; instalação por `Install-PSResource` ou `Install-Module`. Pester (documentação da versão 6, exemplo 6.1.0): arquivos `*.Tests.ps1`; `Describe`/`Context`, `It`, `Should`; `Invoke-Pester -Output Detailed`; `BeforeAll` para carregar o arquivo de função por `$PSScriptRoot`; compatível com Windows PowerShell 5.1 e PowerShell 7.4 ou posterior; o Windows traz o Pester 3.4.0 embutido, que não atualiza com `Update-Module`: instalar a versão atual lado a lado com `Install-Module -Name Pester -Force -SkipPublisherCheck`.
- **Conteúdo reutilizável (destilação própria):** gate de qualidade: (1) PSScriptAnalyzer com regras padrão e falha em erro, mais exclusão justificada por escrito; (2) testes Pester por função, incluindo o teste `-WhatIf` (V-57); (3) **cuidado com a versão**: a documentação nova usa asserções do estilo `Should-Be`, enquanto o Pester 5 usa `Should -Be`; conferir `Get-Module Pester -ListAvailable` antes de escrever testes; (4) instalar módulos altera o ambiente: a fábrica só recomenda.
- **Ressalvas:** o quick-start não trata de código de saída para CI, de `-CI` nem de `-PassThru` (Verificado); a diferença Discovery versus Run do Pester 5 também não está nessa página. Parâmetros `-Settings` do analisador não lidos.
- **Verificação:** WebFetch das três páginas, API do GitHub e arquivo de licença do Pester.

### V-59 — PowerShell: tratamento de erro (`try/catch/finally`, `$ErrorActionPreference`, comandos nativos) (origem R-gap-34) — Classe A (8) · Prompt-score 86
- **Lente:** gapfill (authoritative)
- **Tipo:** pattern + checklist
- **Fonte:** https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_try_catch_finally · https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling · https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_preference_variables · **Autor/Org:** Microsoft Learn
- **Sinais:** `about_try_catch_finally` `ms.date` 2026-04-02; `about_error_handling` `ms.date` 2026-07-02 (acrescentada por mim); `about_preference_variables` `ms.date` 2026-06-29 (Verificado, páginas do PowerShell 7.6 com versões 5.1 e 7.x ligadas).
- **Técnicas-chave (Verificado):** três categorias de erro: **não terminante** (não aciona `catch`, a menos que escalado), terminante de instrução e terminante de script (`throw`); `try/catch` pega as duas terminantes; `catch` filtra por tipo, do mais específico ao mais geral; `$_`/`$PSItem` é um `ErrorRecord`; `finally` roda sempre, inclusive com Ctrl+C e com `exit` no `catch`; **`-ErrorAction Stop` ou `$ErrorActionPreference = 'Stop'` escalam erro não terminante para terminante** e então o `catch` o pega (**Inferido** pelo pesquisador, agora **Verificado**); em função avançada (`[CmdletBinding()]`) o erro escalado vira terminante de instrução (o script continua na próxima linha), em bloco não avançado vira terminante de script; `$ErrorActionPreference = 'SilentlyContinue'` ou `Ignore` pode suprimir até um `throw`, e `-ErrorAction` não suprime erro vindo de `ThrowTerminatingError()`; **comando nativo** com código diferente de zero não gera `ErrorRecord` nem aciona `catch` por padrão: testar `$LASTEXITCODE`; `$PSNativeCommandUseErrorActionPreference` (experimental no PowerShell 7.3, estável no 7.4, padrão `$false`) faz o código de saída virar erro regido por `$ErrorActionPreference`; padrões: `$ErrorActionPreference` = `Continue`, `$ConfirmPreference` = `High`, `$WhatIfPreference` = `$false`.
- **Conteúdo reutilizável (destilação própria) — padrão de script:** `$ErrorActionPreference = 'Stop'` no topo; `try { ... } catch { Write-Error ...; exit 1 } finally { limpeza }`; para `git`, `signtool`, `msbuild` e outros nativos, checar `$LASTEXITCODE` depois de cada chamada (no 5.1, que não tem `$PSNativeCommandUseErrorActionPreference`); em funções avançadas, `ThrowTerminatingError()` quando não dá para continuar e `WriteError()` quando dá.
- **Ressalvas:** a disponibilidade de `$PSNativeCommandUseErrorActionPreference` no Windows PowerShell 5.1 não foi lida na versão 5.1 da página (**Inferido**: a página diz que foi adicionada na 7.3). O valor `Suspend` de `$ErrorActionPreference`, citado pelo pesquisador, não aparece na tabela de `-ErrorAction` lida.
- **Verificação:** WebFetch de três páginas; textos salvos conferidos com busca de termos.

### V-60 — PowerShell 5.1 versus PowerShell 7: diferenças e verbos (origem R-gap-35; reforça V-14) — Classe A (8) · Prompt-score 84
- **Lente:** gapfill (authoritative)
- **Tipo:** compatibility checklist
- **Fonte:** https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell · https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/approved-verbs-for-windows-powershell-commands · **Autor/Org:** Microsoft Learn
- **Sinais:** diferenças `ms.date` 2026-02-04, `updated_at` 2026-06-16; verbos `ms.date` 2026-03-30 (Verificado).
- **Técnicas-chave (Verificado):** o Windows PowerShell 5.1 roda sobre o .NET Framework 4.5; o PowerShell 6 em diante é de código aberto e multiplataforma; PowerShell Workflow foi removido (sem Windows Workflow Foundation no .NET moderno); `Out-GridView` e cmdlets dependentes de WPF voltaram no 7.0; `$OutputEncoding` passou a UTF-8 sem BOM no lugar de ASCII; operadores `??` e `??=` são do PowerShell 7; `ForEach-Object -Parallel` é do 7; **`Build` e `Deploy` foram adicionados no PowerShell 6** (a coluna "verbos a evitar" lista `Build` como sinônimo de `New` e `Deploy` como sinônimo de `Publish`).
- **Conteúdo reutilizável (destilação própria) — tabela de compatibilidade:** scripts da fábrica miram o 5.1 por padrão; recursos do 7 (`??`, `-Parallel`, `Build-`, `Deploy-`) exigem `#requires -Version 7` e aviso ao usuário; nomes com `Publish-`, `Install-`, `Test-`, `Invoke-`, `New-`; conferir sempre com `Get-Verb` na versão instalada.
- **Ressalvas:** operador ternário e encadeamento de pipeline (`&&`, `||`) não foram conferidos no texto lido: não afirmar. Pacotes só de Windows no 7 e o modo de compatibilidade não foram lidos.
- **Verificação:** WebFetch das duas páginas; tabela de verbos lida por inteiro; busca de termos no texto das diferenças.

### V-61 — ShellCheck (wiki de códigos SC) (origem R-gap-36) — Classe A (8) · Prompt-score 82
- **Lente:** gapfill (authoritative)
- **Tipo:** checklist + reference
- **Fonte:** https://www.shellcheck.net/wiki/ · páginas `SC2086`, `SC2155`, `SC2164` · repositório https://github.com/koalaman/shellcheck · **Autor/Org:** projeto ShellCheck
- **Sinais:** `koalaman/shellcheck` 40.153★, push 2026-10-09; **licença GPL-3.0** da ferramenta (API do GitHub); a wiki não declara licença (Verificado) → só destilar.
- **Técnicas-chave (Verificado nas três páginas lidas):** SC2086: expansão sem aspas sofre divisão de palavras e globbing; usar `"$1"`, `"$@"`; exceções: arrays no bash/ksh/zsh para divisão intencional, `set -f` ou `IFS=''`, e `${debug:+"-x"}` para argumento opcional. SC2155: `local`/`export`/`readonly` com substituição de comando na mesma linha mascara o código de saída do comando; declarar e atribuir em linhas separadas. SC2164: `cd` sem tratamento de falha continua no diretório errado, o que é perigoso antes de `rm`; usar `cd dir || exit` (em função, `|| return`). SC2046, SC2034, SC1008 e SC3001–SC3067 vêm do índice lido pelo pesquisador e **não** foram reconferidos por mim.
- **Conteúdo reutilizável (destilação própria):** rodar ShellCheck em todo `.sh` e tratar SC2086, SC2155 e SC2164 como erro; declarar o dialeto no shebang (`sh` ou `bash`) para o ShellCheck avisar recursos não portáveis; supressões só com comentário de justificativa.
- **Ressalvas:** instalar o ShellCheck é decisão do usuário (binário de terceiros). Em Windows o ambiente é Git Bash (bash, não `sh` puro).
- **Verificação:** WebFetch de três páginas da wiki e API do GitHub.

### V-62 — Google Shell Style Guide (origem R-gap-38) — Classe B (7) · Prompt-score 80
- **Lente:** gapfill (authoritative)
- **Tipo:** style guide + checklist
- **Fonte:** https://google.github.io/styleguide/shellguide.html · **Autor/Org:** Google
- **Sinais:** guia sem data na página. O repositório `google/styleguide` tem `LICENSE` **Creative Commons Attribution 3.0 Unported** (Verificado), ou seja, texto literal é possível com atribuição, mas aqui só destilei. A página em si só diz "open source".
- **Técnicas-chave (Verificado):** bash é a única linguagem de shell permitida para executáveis (exceção para ambientes sem bash); script com mais de 100 linhas ou fluxo não trivial deve ir para linguagem mais estruturada; usar `set` para opções do shell, para o script funcionar quando chamado como `bash nome.sh`; mensagens de erro vão para STDERR por uma função `err()`; aspas em variáveis, `"$@"` no lugar de `$*`; `local` para variáveis de função; nomes de função e variável em minúsculas com sublinhado e constantes e variáveis de ambiente em maiúsculas; `(( i++ ))` solto pode encerrar o script com `set -e` quando a expressão vale zero.
- **Conteúdo reutilizável (destilação própria):** convenções para `.sh` da fábrica: bash declarado, erros em STDERR, aspas, `local`, ShellCheck no CI (V-61), script curto.
- **Correção:** o pesquisador listou `set -euo pipefail` como convenção do guia; o guia **não recomenda** `set -e` nem `pipefail` (usa `PIPESTATUS` para checar pipes). Se a fábrica adotar `set -euo pipefail`, é decisão **própria**, com o aviso do guia sobre `set -e`.
- **Ressalvas:** cobre bash e não POSIX `sh` (ver V-63).
- **Verificação:** WebFetch do guia (nove pontos) e do arquivo `LICENSE` do repositório.

### V-63 — POSIX.1-2017: Shell Command Language (origem R-gap-37) — Classe B (6) · Prompt-score 76
- **Lente:** gapfill (authoritative)
- **Tipo:** reference
- **Fonte:** https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html · **Autor/Org:** The Open Group / IEEE Std 1003.1-2017
- **Sinais:** especificação (edição 2018; a página avisa que há mais recente); página de 189 mil caracteres, li de 60.000 a 160.000.
- **Técnicas-chave (Verificado nas partes lidas):** `set -e` (errexit): o shell sai quando um comando falha; **exceções**: falha de comando individual dentro de pipeline de vários comandos não faz sair (só a do pipeline inteiro conta); ignora a lista composta depois de `while`, `until`, `if`, `elif`, pipeline iniciado por `!` e qualquer comando de lista AND-OR que não seja o último; palavras reservadas da gramática (`if`, `then`, `else`, `elif`, `fi`, `do`, `done`, `case`, `esac`, `while`, `until`, `for`, `{`, `}`, `!`, `in`); `local` aparece só em uma tabela de utilitários de comportamento não especificado.
- **Conteúdo reutilizável (destilação própria) — regra de portabilidade:** se o script deve rodar em `sh` puro, não usar `[[`, arrays, `local` nem `function`; declarar o dialeto no shebang; tratar `set -e` como rede de proteção parcial (as exceções acima), não como garantia.
- **Ressalvas:** **Correção:** o pesquisador disse que `set -e` "não aparece no trecho lido"; aparece na entrada `set`. Já "`#!`: resultado não especificado" e "`[[`, `function` e `select` possivelmente reservadas" **não** foram reconfirmados por mim nas partes lidas (Não verificado). Uma terceira parte (160.000 em diante) não foi lida.
- **Verificação:** WebFetch com `offset: 60000`.

### V-64 — Segunda fonte para design de CLI e DX: guidelines do Azure CLI (com Heroku e Atlassian como sinal) (item do validador; fecha em parte a lacuna 12 de DX) — Classe B (7) · Prompt-score 80
- **Lente:** validador
- **Tipo:** checklist + reference
- **Fonte:** https://github.com/Azure/azure-cli/blob/dev/doc/command_guidelines.md (lido pelo caminho bruto) · https://devcenter.heroku.com/articles/cli-style-guide · https://www.atlassian.com/blog/it-teams/10-design-principles-for-delightful-clis · **Autor/Org:** Microsoft (Azure CLI); Heroku; Atlassian
- **Sinais:** `Azure/azure-cli` 4.649★, MIT, push 2026-10-09 (Verificado); data do arquivo de guidelines **não obtida** (a API de commits deu 403). Heroku: "Last updated: January 31, 2025" (14 meses). Atlassian: 23/07/2020.
- **Notas de fonte:** Azure B(7): autoridade 2 (empresa de engenharia), evidência 2, atualidade 1, comunidade 1, licença 1. Heroku C(4): autoridade 2, atualidade 1, restante 0–1. Atlassian C(3): post de 2020 sem evidência. Heroku e Atlassian servem de **sinal**, não de base.
- **Técnicas-chave (Verificado):** Azure: nomes `[substantivo] [substantivo] [verbo]`, verbo em todo comando, subgrupos hifenizados, evitar subgrupos só de subgrupos; verbos padrão com semântica (`create` idempotente e devolve o recurso, `update` tipo PATCH, `set` substitui tudo, `show` com 404 → código de saída 3, `list` um comando só, `delete` não devolve nada, `wait` quando existe `--no-wait`); unidades fora do nome do argumento (aceitar sufixos como `1h`); JSON bruto como parâmetro é **proibido** (expor propriedades como parâmetros); saída em JSON, TSV e tabela, retornando objeto e nunca string ou booleano; dados em `stdout` e tudo mais (logs, status, erros) em `stderr`; operações longas com `--no-wait`; testes obrigatórios. Heroku: CLI "para humanos antes das máquinas"; `topic:command`; descrição para todo comando e flag (minúscula, até 80 colunas, sem ponto final); flags em vez de argumentos; prompt sempre contornável por flag; avisos e progresso em `stderr`; `--json` e `--terse` onde valer; cores com `--no-color` e desligadas fora de TTY; não quebrar entradas e saídas depois de GA; tabelas amigáveis ao `grep`. Atlassian: `--help`, progresso visível, erros legíveis com correção, sugerir o próximo passo, prompt para entrada faltante, "saída fácil", flags em vez de argumentos.
- **Conteúdo reutilizável (destilação própria) — acréscimo ao checklist de V-11/V-13:** (1) verbos com semântica fixa e documentada; (2) idempotência declarada em `create`; (3) `--no-wait` e `wait` em operações longas; (4) sem blob JSON como parâmetro; (5) estabilidade de entradas e saídas após GA; (6) código de saída distinto para "não encontrado"; (7) toda flag com descrição.
- **Ressalvas:** isto é **design de CLI**, não a rubrica de auditoria de DX de V-22 (a lacuna de uma segunda fonte para a auditoria de onboarding e tempo até o "hello world" segue **aberta**). O guia do Azure não trata de prompts nem de `--yes` (Verificado). O guia do Heroku não trata de códigos de saída nem de tratamento de erro (Verificado).
- **Verificação:** WebFetch das três páginas e API de busca do GitHub.

### V-65 — Electron versus Tauri na prática: DoltHub e discussão no HN (origem: busca do validador; fecha em parte o item de comunidade) — Classe B (6) · Prompt-score 74
- **Lente:** community (HN pela API Algolia; Reddit e YouTube continuam inacessíveis)
- **Tipo:** pattern (matriz qualitativa de decisão)
- **Fonte:** https://www.dolthub.com/blog/2025-11-13-electron-vs-tauri/ · discussão do HN `item 46082291` (https://news.ycombinator.com/item?id=46082291) · **Autor/Org:** DoltHub (Eric Richardson)
- **Sinais:** post de 13/11/2025 (11 meses); HN: 133 pontos e 81 comentários (Verificado pela API Algolia); **N=1** (um app, o Dolt Workbench). Nota de fonte: autoridade 2, evidência 1, atualidade 1, comunidade 1, licença 0 = 5, **B(6)** com o cruzamento abaixo.
- **Técnicas-chave (Verificado no post):** Electron: renderização consistente (Chromium) com pegada grande; Tauri: webview do sistema pela biblioteca WRY, mais leve, sem garantia de compatibilidade (o autor diz que inconsistências foram "raríssimas"); suporte a Next.js: Electron depende do Nextron (aparentemente sem manutenção), Tauri funciona com export estático; Tauri exige compilar o servidor Node como binário *sidecar*; **bloqueios para migrar: falta de suporte a `.appx`/`.msix` no Windows (afeta a Store) e problemas com binários universais e assinatura no macOS (assinar duas vezes)**. O post não trata de auto-update nem de autenticação. No HN (os primeiros ~12 comentários que li): WebKitGTK no Linux como principal dor; AppImage gerado no Ubuntu falha em outras distribuições por glibc; Tauri "mais leve, mas não leve"; build do Rust lento e pesado em disco; maturidade de plugins do Electron.
- **Cruzamento com fonte A (Verificado):** a documentação do Tauri lida agora diz que ele só gera MSI e NSIS e que a Store aceita só EXE ou MSI (V-46), compatível com o relato do MSIX. A parte de Linux do HN **não** foi cruzada com fonte oficial: Não verificado.
- **Conteúdo reutilizável (destilação própria):** matriz qualitativa para a decisão do usuário: (1) precisa de MSIX/identidade de pacote → Electron (ou outro empacotamento) hoje; (2) quer pegada pequena e aceita webview do sistema → Tauri; (3) alvo Linux sério → testar WebKitGTK cedo; (4) precisa de Node completo no processo principal → Electron. Nunca citar números do post como benchmark.
- **Ressalvas:** relato de uma equipe; pode ter mudado desde novembro de 2025. Complementa o rebaixado R-community-19 (V-matrix anterior, N=1).
- **Verificação:** WebFetch do post, do item do HN (API de itens) e da API de busca do HN.

### V-66 — Meta-skill `skill-based-architecture` (WoJiSama): arquitetura de skills por roteamento (origem R-gap-39) — Classe B (6) · Prompt-score 72 (fonte) / 76 (destilação)
- **Lente:** gapfill (github)
- **Tipo:** pattern + reference (**não instalar nem executar**)
- **Fonte:** https://github.com/WoJiSama/skill-based-architecture (README e `SKILL.md`) · **Autor/Org:** WoJiSama
- **Sinais:** 610★, MIT, push 2026-09-20, não arquivado (Verificado). Nota de fonte: autoridade 1, evidência 1, atualidade 2, comunidade 1, licença 1 = 6.
- **Técnicas-chave (Verificado no README e no `SKILL.md`, via resumo):** `SKILL.md` como roteador (descrição até 25 linhas e corpo até uns 90, segundo os princípios), `rules/`, `workflows/`, `references/`, `scripts/`; "rigor progressivo" (um arquivo, pasta leve ou completo, escolhido por evidência); carregar um arquivo só quando ele muda a próxima ação; descrições grosseiras sem passos de workflow; provas em camadas (estrutural, migração, comportamental) e relatar "sem veredito" quando falta evidência ao vivo; o README admite que as verificações estruturais "não provam" que toda instrução antiga sobreviveu. Instalação pelo marketplace do Claude Code ou `git clone`; scripts de scaffold com prévia somente leitura e `--apply` que escreve no projeto, com reversão se falhar.
- **Pontuação da fonte:** 72: D9 5, D7 4, D10 4, D4 4, D5 2 (poucos exemplos), D8 3 (escreve arquivos, mas com prévia primeiro), D12 3.
- **Conteúdo reutilizável (destilação própria):** princípios: dono único para cada regra; roteamento por descrição curta mais referências com condição de leitura (já em V-03); nada de mecanismo sem cenário concreto; provas separadas por camada.
- **Ressalvas:** riscos listados: `--apply` escreve no repositório; atualização sem versão fixa pelo marketplace executa código de terceiros; o README não alerta para execução de scripts. A fábrica não executa nem instala.
- **Verificação:** WebFetch do README e do `SKILL.md`; API do GitHub.

### V-67 — VoltAgent `awesome-claude-code-subagents`: catálogo e dois agentes lidos (origem R-gap-41) — Classe B (7) para o catálogo; agentes individuais rebaixados · Prompt-score 53 (`powershell-5.1-expert`) / 40 (`cli-developer`)
- **Lente:** gapfill (github)
- **Tipo:** referência de catálogo (estudo)
- **Fonte:** https://github.com/VoltAgent/awesome-claude-code-subagents · `.../categories/02-language-specialists/powershell-5.1-expert.md` · `.../categories/06-developer-experience/cli-developer.md` · **Autor/Org:** VoltAgent
- **Sinais:** 25.619★, MIT, push 2026-10-05 (Verificado). O README avisa que a equipe **não audita** a segurança nem a correção de nenhum subagente e manda revisar cada um. Instalação inclui `install-agents.sh` (script de terceiros): a fábrica não o executa.
- **Catálogo (Verificado):** agentes relevantes: `powershell-5.1-expert`, `powershell-7-expert`, `powershell-module-architect`, `powershell-ui-architect`, `powershell-security-hardening`, `windows-infra-admin`, `ad-security-reviewer`, `csharp-developer`, `dotnet-core-expert`, `dotnet-framework-4.8-expert`, `electron-pro`, `cli-developer`, `build-engineer`, `tooling-engineer`, `dx-optimizer`, `dependency-manager`. **Não há agente de Tauri, nem de shell (bash/zsh), nem de emulador de terminal.**
- **Pontuação dos agentes lidos (resumo estruturado):** `powershell-5.1-expert` **53** (revisar/rebaixado): D6 1 (sem formato de saída), D8 2 (`Write`, `Edit` e `Bash` para mudar AD, DNS e GPO em lote sem portão de aprovação), D11 2, D5 2; tem checklist de `-WhatIf/-Confirm`, mas não nomeia `ShouldProcess`, Pester nem PSScriptAnalyzer. `cli-developer` **≤ 40** (reprovação automática): o modelo de mensagem de entrega traz métricas inventadas ("70% mais rápido", "4,8/5") e exemplos numéricos sem fonte; não define códigos de saída, não menciona `--json` nem modo não interativo; acessibilidade ausente.
- **Conteúdo reutilizável:** apenas a lista de lacunas do catálogo e o esqueleto de frontmatter (`name`, `description`, `tools`, `model`). Nenhum corpo de agente é reaproveitado. Para a fábrica: agente de auditoria só com `Read, Grep, Glob` (V-23).
- **Ressalvas:** `electron-pro.md` foi lido pelo pesquisador, mas **não reaberto** por mim; os outros agentes do catálogo não foram abertos.
- **Verificação:** WebFetch do README e dos dois arquivos; API de busca do GitHub.

---

## Rejeitados e rebaixados

| Item (origem) | Decisão | Motivo |
| --- | --- | --- |
| R-authoritative-25 (HN 46470017, "setup do criador do Claude Code") | Rejeitado | Classe C(4) sem conteúdo reaproveitável: o texto do post original é um tweet que o HN apenas aponta. Verifiquei por Algolia (568 pontos, 53 comentários diretos, 2026-01-02): a thread não contém "allowlist" nem "settings.json". As afirmações do atlas sobre allowlist e skill versionada não se sustentam. As ideias úteis (planejar antes, registrar decisões) já estão em V-07. |
| R-github-20 (mesmo HN) | Rejeitado | Duplicata de R-authoritative-25; mesma conclusão. |
| R-github-19 (`cmdlet-development-guidelines`) | Rejeitado | Nenhuma regra extraída (só 85 palavras de introdução). Substituído por V-15 (`strongly-encouraged-development-guidelines`). |
| R-community-24 (busca no HN "claude code powershell windows") | Rejeitado | Itens não lidos, engajamento 1–11 pontos; só sinal de demanda, sem conteúdo. O único item aproveitável (blog harishgarg) está em R-community-10 (rebaixado). |
| R-github-14 (centminmod/my-claude-code-setup) | Rebaixado (redundante) | Metadados verificados (MIT, 2.659★, push 2026-10-08), mas o valor (divulgação progressiva de CLAUDE.md) já está em V-06 com fonte oficial; contém comandos pessoais (fuso, `ccusage`, `brew`). Não li o repositório além do que o pesquisador relatou. |
| R-community-02 (antjanus, CLAUDE.md como onboarding) | Rebaixado para C(3) e fundido em V-06 | Nota recalculada: autoridade 1 + evidência 1 + atualidade 1 (janeiro de 2026) + comunidade 0 (6 pontos no HN) + licença 0 = 3. Conteúdo confere (seções, lista "não faça", PLAN.md para mais de 3 arquivos) e é redundante com a doc oficial. |
| R-community-04 (CreatmanCEO, portão de testes no commit) | Rebaixado para C(4) | Repositório com 12★, MIT, push 2026-04-30 (Verificado); alegação de top-5 do Habr é do próprio autor. Padrão válido (PreToolUse em `git commit` com timeout), mas o README admite limites (bloqueia commit e não push; suíte lenta estoura 120 s; PowerShell nativo exige adaptação). Reaproveitar só a ideia, via V-08. |
| R-community-05 (planner, tester, code-reviewer do CreatmanCEO) | Rebaixado para C(4) | Arquivos existem (planner: Read, Grep, Glob, LS; code-reviewer: Read, Grep, Glob; tester com Write e Bash, Verificado no README), mas não li os corpos dos prompts. V-23 e V-29 cobrem o padrão com fonte melhor. |
| R-community-08 (Bitcraze, daemon + comandos one-shot) | Rebaixado para C(4) | Post confere (Arnaud, 2026-04-13, "Fun Friday project", CLI em Rust, daemon, skill), mas é experimento não oficial sem testes formais. A ideia "separar capacidade (CLI) e fluxo (skill); daemon para estado" fica como **sinal** na seção de recomendações. |
| R-community-10 (harishgarg, ambiente Windows no CLAUDE.md) | Rebaixado para C(4) | Conteúdo confere só em parte: é uma **lista** (não tabela) de equivalentes, sem data, sem hooks ou permissões. O bloco útil (declarar PowerShell como shell e listar equivalentes `Get-ChildItem`, `Get-Content`, `Get-Command`, `ConvertFrom-Json`) é fato elementar do PowerShell e entra como regra própria em "Recomendações". |
| R-community-19 (Hopp e Fluxzy, Electron versus Tauri) | Rebaixado para C(4) | Números conferem (172 versus 409 MB com 6 janelas; 8,6 versus 244 MiB; build 1:21 versus 16 s), mas o autor mesmo diz "com um grão de sal", N=1, hardware não especificado, post de 2025-04-09 (mais de 12 meses). Usar só como matriz de decisão qualitativa (updaters incompatíveis, ordem de assinatura, WebKitGTK/Wayland), nunca como benchmark. |
| R-community-23 (Build This Now, dados de adoção) | Rebaixado para C(4) | Números conferem (2.500 repositórios de 8.298; CLAUDE.md 84,9%; hooks 13,3%; subagentes 24,6%; skills 28,1%; mediana 6,2 KB; 2026-06-19), mas a fonte vende um kit de US$ 29, amostra só de repositórios públicos e metodologia não auditada. Citar, se for o caso, como "segundo levantamento de fornecedor", nunca como fato de mercado. |
| R-gap-40 (`ciembor/agent-rules-books`, 2.945★, MIT, push 2026-09-10; metadados Verificados) | Rebaixado para C(5) | O conteúdo é destilado de livros de terceiros (o README diz "inspirado em", sem reproduzir texto, mas também sem autorização dos autores); a única evidência é um experimento inicial do próprio autor (80 tarefas, 74/100 contra 46/100 em avaliação por ChatGPT; ele diz que não é benchmark). Nota: autoridade 1 + evidência 1 + atualidade 2 + comunidade 1 + licença 1 = 6, mas o risco de direitos autorais e a falta de validação independente rebaixam. Só a **estrutura** (versões completa, mini e nano por tamanho de contexto) vale como ideia; nenhuma regra é reaproveitada e `npx skills add` não é executado. |
| R-gap-41, agente `powershell-5.1-expert` (VoltAgent) | Rebaixado (prompt-score 53) | Sem formato de saída, sem portão de aprovação para mudanças em AD, DNS e GPO, com `Write`, `Edit` e `Bash`; não nomeia `ShouldProcess`, Pester nem PSScriptAnalyzer. Ver V-67. |
| R-gap-41, agente `cli-developer` (VoltAgent) | Rejeitado (prompt-score ≤ 40) | Reprovação automática: o modelo de mensagem de entrega contém métricas inventadas ("70% mais rápido", "4,8/5") e metas numéricas sem fonte; sem códigos de saída definidos, sem `--json`, sem acessibilidade. Ver V-67. |
| R-gap-39/R-gap-42, scripts de instalação e de validação (`scaffold-downstream.sh --apply`, `validate-agent.sh`, `validate-hook-schema.sh`, `install-agents.sh`) | Não aprovados para execução | Código de terceiros que escreve no repositório ou cujo conteúdo não foi visto; a fábrica só estuda a estrutura. |
| `steipete/agent-rules` (5.680★, MIT, **arquivado em 2026-05-03**) | Rejeitado (mantido) | Reconferido: o dono arquivou o repositório em 2026-05-03 (somente leitura); o README diz que o conteúdo é de meados de 2025, para Cursor; dois scripts de shell (`install-project-rules.sh`, `tweak-claude.sh`) não descritos. |
| 4 linhas do HN do pesquisador (Revdiff 17 pts, Hopp 42 pts, harishgarg 5 pts, elevator-music 56 pts) | Rejeitadas (mantidas) | Engajamento baixo ou fora do escopo, sem conteúdo reaproveitável. O thread do HN do DoltHub (133 pts, 81 comentários) entrou como V-65 (B(6)) depois de cruzado com a documentação do Tauri. |
| Afirmação "Electron: EV obrigatório desde 2023" (V-17) | **Refutada** | Páginas da Microsoft de 2026 (V-44): a mudança de 2023 foi HSM para OV; o bypass do SmartScreen pelo EV foi removido em 2024. |
| Afirmação "OnlyLoadAppFromAsar deve ficar desligado" (R-gap-19) | **Refutada** | O fuse restringe o carregamento ao `app.asar`: o valor seguro é ligado (V-48). |
| Afirmação "`set -euo pipefail` é convenção do Google Shell Style Guide" (R-gap-38) | **Refutada** | O guia não recomenda `set -e` nem `pipefail` (V-62). |

## Deduplicação entre lentes (resumo)

- Segurança do Electron: R-authoritative-15 + R-github-05 + R-community-15 → V-16.
- Segurança e capabilities do Tauri: R-authoritative-17/18 + R-github-06 + R-community-18 → V-19.
- Hooks: R-authoritative-08 + R-community-11 + R-github-10 (parte) → V-08; guardrails de Trail of Bits em V-27.
- Boas práticas oficiais: R-authoritative-07 + R-github-01 → V-07.
- Ferramentas para agente: R-authoritative-11 + R-github-02 + R-community-14 → V-11.
- CLI de Ronacher: R-authoritative-12 + R-github-04 + R-community-07 → V-12.
- clig.dev: R-authoritative-13 + R-github-03 → V-13.
- Plugin/marketplace: R-authoritative-01/20 + R-github-17 + R-community-21 → V-01.
- AGENTS.md e Ruler: R-authoritative-10/23 + R-github-08/09 + R-community-22 → V-10 e V-28.
- gstack: R-authoritative-24 + R-github-07 + R-community-20 → V-22.
- Dicas de Thariq: R-authoritative-05 + R-github-16 + R-community-12 → V-05.
- Reclassificações de classe: R-github-10/11 (C→B), R-github-16 (C→B), R-github-07 (A→B), R-github-08 (A→B), R-community-15 (A(9)→A(8)), R-github-05/06 (B→A), R-community-09 (A→B), R-github-12/13/15 (A→B), R-github-18 (B, nota 7→6).
- **Complemento (gapfill):** Tauri assinatura Windows e macOS: R-gap-17 + parte oficial de R-community-16 → V-46 (V-21 mantém só o relato da ordem); Tauri isolation e CSP: R-gap-20 + R-gap-21 → V-47 (complementa V-19); updaters: V-18 (Electron), V-20 (Tauri) e V-49 (Sparkle) são complementares, não duplicados; hooks: R-gap-23 → V-52 (complementa V-08); estrutura de plugin: R-gap-29 → V-53 (complementa V-01); sandbox, permissões e segurança do Claude Code: R-gap-24 + 25 + 26 → V-51; evals e custo: R-gap-27 + 28 → V-50; PSScriptAnalyzer e Pester: R-gap-32 + 33 → V-58; MSIX e App Installer: R-gap-11 + 12 → V-40; certificado, SmartScreen e SignTool: R-gap-15 + 16 → V-44 (resolve o conflito de V-17 e V-21); Qt `windeployqt` + `macdeployqt` → V-38; R-gap-41 (VoltAgent) e o catálogo de V-23 tratam do mesmo repositório: V-23 fica com o formato de subagente e V-67 com os dois agentes lidos.
- **Reclassificações do complemento:** R-gap-04 A(9)→A(8) (sem citação de MVVM); R-gap-05 A(9)→A(8); R-gap-06 A(8)→B(7) (atualidade); R-gap-07 A(8) mantida com licença corrigida; R-gap-09 A(8)→B(7) e R-gap-10 A(8)→B(7) (documentação sem data, licença GFDL); R-gap-11 e 12 A(8) mantidas; R-gap-13 B(7) mantida; R-gap-18 A(8)→B(7) (Apple lida só por endpoint de dados, sem sintaxe de comando); R-gap-19 B(7) mantida; R-gap-22 B(7)→A(8) (licença MIT, 9.8k★); R-gap-33 B(7)→A(8) (licença Apache-2.0, agrupada em V-58); R-gap-36 A(7)→A(8); R-gap-37 A(9)→B(6) (parte da norma lida); R-gap-39 B(7)→B(6); R-gap-40 B(6)→C(5); R-gap-41 B(6)→B(7) só para o catálogo; R-gap-42 A(8) mantida; R-gap-43 A(8) mantida (README apenas).

## Mapa de cobertura do escopo (após validação, incluindo o complemento)

| Subtema | Itens V | Cobertura |
| --- | --- | --- |
| Design de CLI para humanos e máquinas | V-11, V-12, V-13, V-64 | Boa (V-64 acrescenta uma segunda fonte B: Azure CLI) |
| CLI pronta para agente | V-11, V-12 | Boa (fonte de praticante única para idempotência e logs) |
| TUI | V-30, V-31, V-32 | **Parcial**: Textual bem coberto (teclado, foco, headless, snapshot); Ratatui e Bubble Tea com teste e resize; **acessibilidade em TUI sem fonte nas três**; resize do Ratatui é regra de projeto, não fato do framework |
| Electron: segurança | V-16, V-48 | Boa (fuses com valores corrigidos) |
| Electron: assinatura e distribuição | V-17 (corrigido), V-44, V-40, V-41, V-42, V-43 | Boa |
| Electron: auto-update | V-18 | Boa |
| Tauri: segurança e capabilities | V-19, V-47 | Boa (isolation e CSP lidos) |
| Tauri: updater e assinatura | V-20, V-21, V-46 | Boa; a **ordem Authenticode versus assinatura do updater continua sem fonte oficial** |
| Auto-update macOS | V-49 (Sparkle), V-18, V-20 | Boa (Sparkle fecha a lacuna; App Installer em V-40) |
| .NET, WPF, WinUI, MAUI | V-33, V-34, V-35, V-36, V-37 | **Boa**, com lacunas: segurança .NET não lida; página de acessibilidade do WPF não localizada; MVVM do MAUI (404 para o pesquisador, não procurei alternativa); geradores de código do MVVM Toolkit não lidos |
| Qt | V-38, V-39 | **Parcial**: implantação e licenciamento lidos; obrigações da LGPLv3 e segurança do Qt sem fonte |
| Empacotamento e instaladores Windows | V-40 (MSIX + App Installer), V-41 (Inno Setup), V-42 (WiX), V-43 (winget), V-36 | **Boa** (um item por tecnologia); sintaxe de scripts do Inno e de `.wxs` não lida |
| Assinatura de código (fornecedor) | V-44 (Microsoft), V-45 (Apple), V-46 (Tauri) | **Boa**; sintaxe de `notarytool`/`stapler` **não verificada** (a Apple só nomeia as ferramentas) |
| Multiplataforma Windows/macOS/Linux | V-17, V-21, V-46, V-65 | Parcial (Linux só por relato de HN) |
| PowerShell | V-14, V-15, V-57, V-58, V-59, V-60 | **Boa**; falta ler Pester por inteiro (Discovery versus Run, mocks, `-CI`) |
| Shell POSIX/bash | V-61 (ShellCheck), V-62 (Google), V-63 (POSIX) | Boa para os três; POSIX lido de 60.000 a 160.000 caracteres de 189.000 |
| Ferramentas de DX | V-22, V-64 | **Parcial**: V-64 é design de CLI; a rubrica de auditoria de onboarding (tempo até o primeiro sucesso) continua com fonte única (gstack, B) |
| Plugins, skills, hooks do Claude Code | V-01 a V-09, V-23, V-50 a V-55 | **Excelente** |
| CLAUDE.md, AGENTS.md e regras portáteis | V-06, V-10, V-28, V-66 | Boa |
| Guardrails e permissões | V-08, V-27, V-26, V-51, V-52 | **Excelente** |
| Validação e avaliação de plugins | V-24, V-25, V-50, V-54 | **Boa** (evals e `plugin details` lidos; `plugin-dev` estudado) |
| Calibração de prompts (rubrica) | V-56 | Boa (D2, D4, D8 e D10 calibradas; mapeamento corrigido) |
| Comunidade (Reddit, X, YouTube, newsletters, dev.to) | V-65 (HN + blog DoltHub) | **Fraca**: WebSearch indisponível de novo (limite de 200 buscas por turno, compartilhado); Reddit, X e YouTube não acessados; 1 item B(6) |

## Lacunas (objetivas e pesquisáveis)

Estado após a rodada final. As lacunas da primeira rodada foram **fechadas ou reduzidas** como indicam os itens V-30 a V-67; restam estas:

1. **Comunidade real (Reddit r/ClaudeCode, r/ClaudeAI, r/PowerShell, r/electronjs, r/rust; YouTube; X; newsletters):** `WebSearch` recusou toda chamada ("orçamento de 200 buscas por turno usado") em três tentativas minhas. Não contornei por curl, proxy ou leitor de terceiros. Só HN pela API Algolia (permitida) e um blog de empresa (V-65). **Meta de 8 itens B ou superiores: não atingida (1 item).** Pendente de um turno novo ou de `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` maior, com pelo menos 15 buscas em modo standard.
2. **Acessibilidade em TUI:** nenhuma fonte oficial lida para Textual, Ratatui ou Bubble Tea. Pesquisar guias de acessibilidade de terminal (leitores de tela, `NO_COLOR`, contraste).
3. **Sintaxe de `notarytool`/`stapler`:** a página da Apple (corpo obtido por endpoint de dados) só nomeia as ferramentas; ler "Customizing the notarization workflow" por endpoint de dados equivalente ou conferir `xcrun notarytool --help`. Hardened Runtime e entitlements da Apple estão em V-45; o guia do Tauri não os trata.
4. **Ordem Authenticode versus assinatura do updater do Tauri:** nenhuma fonte oficial; só relato único (V-21). Testar em ambiente de teste com um build descartável.
5. **Qt:** obrigações detalhadas da LGPLv3 e página de segurança do Qt (URLs do pesquisador deram 404); procurar o caminho correto no menu de `doc.qt.io/qt-6/`.
6. **.NET desktop:** página de acessibilidade do WPF, MVVM do MAUI e segurança do .NET desktop; geradores de código do MVVM Toolkit.
7. **Inno Setup e WiX:** sintaxe das seções de script (`[Setup]`, `[Files]`, `[Run]`) e do `.wxs`; páginas de WiX v3/v4 (a lida cobre v6/v7); `insignia` e timestamp no WiX.
8. **Claude Code:** seção de privilégios dos hooks (final da página, 162.610 caracteres não lidos) e semântica de `defer`; campos completos de `components` (LSP, `userConfig`); a página de permissões foi lida por busca de termos.
9. **DX:** segunda fonte para a **auditoria de onboarding e tempo até o primeiro sucesso** (V-64 cobre design de CLI, não esta rubrica).
10. **Pester:** `Invoke-Pester` com `-CI`, `-PassThru`, mocks e Discovery versus Run do Pester 5; diferença `Should -Be` versus `Should-Be`.
11. **POSIX:** parte final da página (160.000 em diante) e reconfirmação de `#!` não especificado e das palavras reservadas opcionais.
12. **Agentes e skills lidos só por resumo estruturado:** `plugin-validator`, `skill-reviewer`, `claude-automation-recommender`, `build-mcp-server`, `skill-creator` (só README), `electron-pro` e `skill-based-architecture`; ler o texto integral antes de reaproveitar qualquer trecho.
13. **Páginas sem metadado de data** (Qt, Textual, Tauri, Apple, ShellCheck, Google): atualidade tratada como atemporal.

## Recomendações ao construtor

**Skills (cada uma com a seção "Armadilhas" vazia no início, descrição-gatilho PT-BR e EN, `allowed-tools` mínimo):**
- `plugin-security-review` (V-02, V-08, V-26, V-27): somente leitura, `disable-model-invocation: true`.
- `plugin-structure-check` (V-01, V-03, V-24): roda `claude plugin validate --strict` apenas se o usuário autorizar a execução; senão, checklist manual.
- `cli-agent-review` (V-11, V-12, V-13): checklist de CLI para humanos e agentes, com exit codes, stdout/stderr, `--json`, `--no-input`, erros acionáveis e desinstalação.
- `electron-security-audit` (V-16) e `tauri-security-audit` (V-19): leem arquivos de configuração e código; nunca executam o app.
- `desktop-release-checklist` (V-17, V-18, V-20, V-21): assinatura, notarização, updater, teste em máquina limpa; registrar o conflito EV versus OV como decisão do usuário.
- `powershell-naming-and-style` (V-14, V-15): usar `Get-Verb` na versão instalada como fonte; avisar sobre `Build`/`Deploy` no 5.1.
- `dx-audit` (V-22): só a rubrica; sem telemetria, sem binários, sem instalar nada do gstack.
- `spec-driven-planning` (V-25): somente as fases e as portas de aprovação; sem execução autônoma.

**Agentes (frontmatter conforme V-23; plugins ignoram `hooks`, `mcpServers` e `permissionMode`):**
- `diff-gap-reviewer` (V-07, V-23, V-29): `Read, Grep, Glob`, saída por severidade e confiança, seção "não sinalizar".
- `planner` somente leitura (sinal de R-community-05, após o corpo ser revisado ou reescrito).

**Checklists/referências (arquivos em `references/`, com condição de leitura):**
- Estrutura de plugin e nomes reservados (V-01); revisão de segurança de plugin (V-02); fluxo de verificação e prompt de revisão (V-07); checklist de CLI (V-11/V-13); checklists Electron/Tauri (V-16, V-19); updater Electron/Tauri (V-18, V-20); matriz de decisão Electron versus Tauri como sinal qualitativo, com a ressalva de N=1 (R-community-19, rebaixado).

**Hooks (somente documentados em `references/`, nunca ativos no plugin):**
- Guardrail Bash em PowerShell (exemplo de V-08, a testar antes de recomendar) e hook de auditoria (`PostToolUse`, V-08). Regra: hook não é fronteira de segurança; apontar sandbox e deny rules (V-27).

**Regras para CLAUDE.md do repositório e dos projetos gerados:**
- Menos de 200 linhas; teste de corte por linha; comandos exatos; ênfase em no máximo uma ou duas linhas (V-06).
- Bloco "Ambiente Windows": shell principal é Windows PowerShell 5.1 (ou 7, se instalado); usar cmdlets em vez de comandos Linux (`Get-ChildItem`, `Get-Content`, `Get-Command`, `ConvertFrom-Json`); `Build` e `Deploy` não existem como verbos no 5.1; quando for necessário bash, usar a ferramenta Bash/Git Bash conscientemente. (Regra própria, baseada em V-14 e no sinal R-community-10.)
- Ações irreversíveis, publicação e instalação de terceiros só com confirmação do usuário.
- Estado de plugin em `${CLAUDE_PLUGIN_DATA}`; nome de plugin sem prefixos reservados (V-01).

**Prompts da biblioteca (candidatos):**
- Revisão adversarial de diff (V-07), auditoria de DX por roteiro (V-22), planejamento por fases com aprovação (V-25), revisão de segurança de plugin (V-02), checklist de release de app desktop (V-17/V-18/V-20/V-21).

**Não virar regra sem novo cruzamento:** a ordem Authenticode versus assinatura do updater (relato único, V-21); qualquer número de benchmark Electron/Tauri; contagens de adoção do vendedor de kit; a afirmação ">10 min de TTHW = 50–70% de abandono" do gstack; a lista de países do Azure Artifact Signing; e as sugestões de timeout e de caminho de log atribuídas a Ronacher (são da fábrica, não dele).

### Acréscimos da rodada de complemento (construtor)

**Skills novas ou ampliadas (sempre com `allowed-tools` mínimo, descrição-gatilho PT-BR e EN, seção "Armadilhas" inicial vazia; nenhuma executa instalador, assina, notariza ou publica sem autorização do usuário):**
- `windows-release-checklist` (V-40, V-41, V-42, V-43, V-44, V-36): árvore de decisão MSIX/Store, Artifact Signing, OV com HSM; **sem EV obrigatório**; senha nunca em argumento; winget só com PR autorizado; WiX só após o usuário decidir sobre OSMF e EULA.
- `macos-release-checklist` (V-45, V-49, V-38): Developer ID, Hardened Runtime, timestamp, entitlements, Sparkle com EdDSA; sintaxe de `notarytool` conferida com `--help` da versão instalada (V-45 não a verificou).
- `desktop-security-audit` (V-16, V-19, V-47, V-48): somente leitura; Electron fuses com `OnlyLoadAppFromAsar` **ligado**; Tauri com capabilities, isolation e CSP.
- `tui-review` (V-30, V-31, V-32): checklist de binding visível, foco, teste headless, snapshot em dois tamanhos e resize; acessibilidade como risco aberto.
- `dotnet-desktop-review` (V-33 a V-37): comandos e binding em WPF, MVVM Toolkit, checklist de acessibilidade WinUI, árvore de empacotamento do Windows App SDK.
- `powershell-quality` (V-57, V-58, V-59, V-60, V-14, V-15): `SupportsShouldProcess` com `ConfirmImpact='High'`, teste `-WhatIf`, PSScriptAnalyzer, Pester (conferir versão), `$ErrorActionPreference = 'Stop'` com `$LASTEXITCODE` para nativos, tabela 5.1 versus 7 (`Build` e `Deploy` só no 6+).
- `shell-script-review` (V-61, V-62, V-63): ShellCheck (SC2086, SC2155, SC2164), convenções do Google (bash, STDERR, aspas, `local`) e portabilidade POSIX; `set -euo pipefail` como convenção **própria** documentada.
- `claude-plugin-test-and-cost` (V-50, V-53, V-54): `claude plugin validate --strict`, casos de eval com `tool_used: Skill`, `claude plugin details` e orçamento de 2.000 tokens; gasto de tokens com autorização.
- `claude-permissions-hardening` (V-51, V-52): ordem deny, ask, allow; sandbox não cobre hooks nem MCP; Windows nativo sem sandbox; hooks com `onFailure: "block"` e matcher ancorado.

**Agentes:** `plugin-reviewer` somente leitura (checklist de V-54 reescrita, `Read, Grep, Glob`, sem executar scripts de terceiros); **não** copiar `cli-developer` nem `powershell-5.1-expert` do VoltAgent (V-67).

**Rubrica de prompts da casa (V-56):** D10 penaliza CAPS e "MUST/CRITICAL/NEVER" usados para forçar disparo e exige instrução positiva; D8 exige a cláusula de confirmação com lista de ações irreversíveis e a regra de não contornar verificações; D2 e D4 apoiados por motivação e etiquetas XML.

**Não virar regra sem novo cruzamento (complemento):** a ordem Authenticode versus assinatura do updater (relato único); "Windows não reporta resize no Bubble Tea" (texto do pkg.go.dev, não reverificado na v2); qualquer sintaxe de `notarytool`/`stapler`; valores recomendados dos fuses `EnableEmbeddedAsarIntegrityValidation` e `WasmTrapHandlers` (Inferido); números do post do DoltHub e comentários de Linux no HN; a taxa de 99,96% de instalação do MSIX (vendedor).

## Confiabilidade dos pesquisadores (para o orquestrador)

- Acertos: URLs reais, metadados do GitHub (estrelas, licença e push batem com a API), conteúdo técnico central de Electron, Tauri, docs do Claude Code e Microsoft. A honestidade sobre o que não foi lido (marcações "Não verificado") foi alta.
- Erros encontrados: 12 itens com correção de conteúdo (ver "Correção" nos itens V-03, V-07, V-08, V-09, V-11, V-12, V-14, V-15, V-18, V-23, V-25, V-29) — nenhuma fabricação de fonte; sobretudo extrapolações (timeouts em Ronacher; ShouldProcess na página errada; "checklist de 9 itens"; "somente leitura" com Bash; `Build` no 5.1; `--bare` sem mencionar a chave de API; hook de log em evento errado). Classes inconsistentes entre lentes para as mesmas fontes (por exemplo, a mesma página do Electron saiu A(9), A(8) e B(6)), corrigidas aqui pela fórmula da rubrica.
- **Rodada de complemento (gapfill, claude-haiku-5-5):** acertos: todas as 43 URLs principais existem e o conteúdo técnico central confere (assinatura Windows, winget, MSIX, Claude Code, ShouldProcess, ShellCheck, Qt); a conclusão que resolve o conflito EV versus OV estava **certa** e foi confirmada com a página mais nova da Microsoft; nenhuma fonte inventada; a marcação de "não lido" e "404" foi honesta (WiX e Apple realmente só traziam menu ou título). Erros corrigidos por mim: (1) **fuse `OnlyLoadAppFromAsar` descrito como "desligado" em vez de ligado** (risco de segurança); (2) papéis de **D8 e D10 trocados** na calibração da rubrica; (3) licença do `plugin-dev` registrada como "MIT na pasta" (o arquivo é Apache-2.0); (4) licenças "não verificadas" de Ratatui, Sparkle, Pester e MVVM Toolkit (todas permissivas); (5) lista de 6 em vez de 14 módulos Qt só-GPL; (6) `set -euo pipefail` atribuído ao guia do Google; (7) `set -e` "não aparece" no POSIX (aparece); (8) MAUI tratado como ausente do MVVM Toolkit; (9) `__TAURI_ISOLATION_HOOK__` como documentado (só em exemplo); (10) inferência sobre `-ErrorAction Stop` e `catch` (agora verificada). Limites do pesquisador: nenhum WebSearch (orçamento esgotado), Apple e WiX sem corpo, vários arquivos de agentes não abertos. **Independência:** sou um modelo diferente (claude-sonnet-5-5) e usei a mesma família de ferramentas (WebFetch e API de busca do GitHub), mais o endpoint de dados da Apple e arquivos brutos que ele não tentou; isso reduz, mas não elimina, vieses comuns de leitura por resumo.
