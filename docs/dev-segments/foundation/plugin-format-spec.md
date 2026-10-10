# Especificação do formato de plugin do Claude Code (verificada em 09/10/2026)

Fontes primárias consultadas: https://code.claude.com/docs/en/plugins-reference e https://code.claude.com/docs/en/plugin-marketplaces . CLI local: Claude Code 2.1.128 em `C:\Users\Francisco Edson\.local\bin\claude.exe` (`claude plugin validate <path>`). Docs gerais: https://code.claude.com/docs/llms.txt (índice) — consulte as páginas de skills (`/docs/en/skills`), subagents (`/docs/en/sub-agents`), slash commands, hooks e plugin evals quando precisar de detalhe adicional.

## Layout padrão

```text
<slug>/
├── .claude-plugin/
│   └── plugin.json          ← manifesto (só ele fica dentro de .claude-plugin/)
├── skills/<skill-name>/SKILL.md   ← uma pasta por skill; recursos auxiliares ao lado
│   └── references/*.md, assets/templates/*.md, examples/*.md
├── agents/<agent-name>.md   ← subagentes (arquivos .md planos)
├── commands/<cmd>.md        ← slash commands (legado; preferir skills, mas válidos)
├── evals/                   ← casos de avaliação (opcional)
└── README.md
```

- Componentes ficam na **raiz do plugin**, nunca dentro de `.claude-plugin/`.
- `CLAUDE.md` na raiz do plugin **não** é carregado (o validador avisa). Instruções que devem entrar no contexto vão em skills.
- Diretórios padrão são escaneados automaticamente; **não** declare `skills`, `commands`, `agents` no manifesto quando usar os diretórios padrão (declarar `commands`/`agents` substitui o scan padrão).
- Tudo é namespaced pelo `name` do plugin: skill `review` no plugin `web-frontend` → `/web-frontend:review`; agente `reviewer` → `web-frontend:reviewer`.

## plugin.json

`name` é o único campo obrigatório. Use:

```json
{
  "name": "web-frontend",
  "displayName": "Web Frontend",
  "version": "0.1.0",
  "description": "Uma frase clara do que o plugin entrega.",
  "author": { "name": "Francisco Edson", "url": "https://github.com/francisco-efjr" },
  "repository": "https://github.com/francisco-efjr/dev-segments",
  "license": "MIT",
  "keywords": ["react", "nextjs", "accessibility"]
}
```

- `name`: kebab-case, sem espaços, `@`, `:`, barras. **Proibido** começar com `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-`, ou conter `claude`/`anthropic` como palavra (aviso). Sem `official` junto de claude/anthropic.
- `homepage`, se usado, precisa ser URL válida (senão o plugin não carrega). Prefira omitir.
- Campos desconhecidos no topo são removidos com aviso — não invente campos.
- Caminhos no manifesto (se houver) começam com `./` e não podem conter `..`.

## Skills (`skills/<nome>/SKILL.md`)

Frontmatter YAML:

```yaml
---
name: component-review            # kebab-case, igual ao nome da pasta
description: O que faz e QUANDO usar. Inclua gatilhos em PT-BR e EN (palavras que o usuário diria). Máx. ~1024 caracteres.
---
```

Campos opcionais suportados por skills do Claude Code (use só quando agregarem): `argument-hint`, `allowed-tools` (lista de ferramentas pré-aprovadas), `model`, `disable-model-invocation: true` (skill só por /comando explícito — use para fluxos com efeitos colaterais), `user-invocable`. Não invente outros campos.

Boas práticas oficiais (Agent Skills):
- `description` é o que decide o acionamento automático: diga **o que** e **quando**, com gatilhos concretos; terceira pessoa ou imperativo; sem marketing.
- Corpo conciso (meta < 500 linhas). **Progressive disclosure:** detalhes em `references/*.md` ao lado, referenciados por link relativo e lidos sob demanda; um nível de profundidade.
- Instruções acionáveis (passos, checklists, critérios de saída), exemplos de entrada/saída, formato de entrega definido.
- Variáveis: `$ARGUMENTS` (argumentos do usuário), `${CLAUDE_PLUGIN_ROOT}` (caminho do plugin instalado) podem ser usados no corpo.

## Subagentes (`agents/<nome>.md`)

```yaml
---
name: security-reviewer
description: Quando delegar a este agente (gatilhos claros; "use proactively" quando couber).
tools: Read, Grep, Glob, Bash      # opcional; omitir = herda todas. Restrinja ao mínimo necessário
model: inherit                     # opcional: inherit | sonnet | opus | haiku | fable
---
<system prompt do agente: papel, escopo, processo, formato de saída, limites>
```

Agentes de revisão/auditoria devem ser somente leitura (`Read, Grep, Glob` e, se necessário, `Bash` para comandos de leitura/teste).

## Commands (`commands/<nome>.md`) — opcional

```yaml
---
description: Linha curta mostrada no menu /
argument-hint: "[arquivo ou escopo]"
allowed-tools: Read, Grep, Glob
---
Corpo do prompt; use $ARGUMENTS.
```

Preferir skills para novos fluxos; usar commands para atalhos finos que chamam uma skill/agente.

## Hooks, MCP, LSP, bin

Política deste projeto: **não ativar** (`hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `bin/` ausentes). Documente recomendações em `skills/<x>/references/tooling.md` ou no README, com o JSON pronto para o usuário copiar, explicando riscos.

## Marketplace (`.claude-plugin/marketplace.json` na raiz `dev-segments/`)

```json
{
  "name": "dev-segments",
  "description": "...",
  "owner": { "name": "Francisco Edson" },
  "plugins": [
    { "name": "web-frontend", "source": "./plugins/web-frontend", "description": "..." }
  ]
}
```

O `name` da entrada deve ser igual ao `name` do `plugin.json`. Instalação: `claude plugin marketplace add <caminho-ou-owner/repo>` e `claude plugin install <plugin>@brain-of-agent` (ou `/plugin marketplace add`, `/plugin install` dentro da sessão).

## Validação

- Determinística: `python "C:\Users\Francisco Edson\dev-segments\tools\verify_plugin.py" "C:\Users\Francisco Edson\dev-segments\plugins\<slug>"`.
- Oficial: `"/c/Users/Francisco Edson/.local/bin/claude.exe" plugin validate "C:\Users\Francisco Edson\dev-segments\plugins\<slug>"` (no Bash) — deve terminar em `Validation passed` (avisos devem ser corrigidos quando possível).
