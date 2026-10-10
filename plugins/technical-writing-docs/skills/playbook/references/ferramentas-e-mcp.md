# Ferramentas, hooks e MCP recomendados (todos desativados)

Validado em 2026-10-10. **Nada aqui está ativo no plugin**: sem `hooks/hooks.json`, `.mcp.json`, `.lsp.json` nem `bin/`. Cada item abaixo é uma recomendação para o usuário habilitar conscientemente no próprio projeto, com comando ou JSON pronto, riscos e rótulo. Hooks e instalações executam código na sua máquina: leia antes, teste em repositório descartável e prefira `.claude/settings.local.json` (não versionado) a configurações globais. Hook é guardrail, não fronteira de segurança (V-01, V-15).

## Sumário

T-01 Vale · T-02 markdownlint · T-03 lychee · T-04 GitHub Pages · T-05 comandos do produto · T-06 plugin oficial de CLAUDE.md · T-07 verificação de exemplos · T-08 `release.yml` · T-09 output style · T-10 validador de skills · T-11 mdarena · T-12 hook de markdownlint · T-13 `claude plugin eval` · T-14 MCP de documentação · T-15 permissões por caminho

## T-01 Vale e vale-action (V-37, MIT)

- **O que é:** linter de prosa que entende marcação (v3.24.0, 2026-10-01); action `vale-cli/vale-action` (v3.0.0, 2026-08-03).
- **Como habilitar:** copie o `.vale.ini` e o job de [vale-ini-e-workflow](../assets/templates/vale-ini-e-workflow.md); `vale sync` instala os pacotes.
- **Riscos:** `vale sync` baixa estilos de terceiros (licenças próprias); seção posterior do `.vale.ini` substitui `BasedOnStyles`; fixe a action por SHA; estilos em inglês geram ruído em PT-BR.
- **Rótulo:** Verificado (V-37).

## T-02 markdownlint (V-38, MIT)

- **Como habilitar:** `.markdownlint.json` com padrão ligado e desligamentos justificados:

```json
{
  "default": true,
  "MD013": false,
  "MD033": { "allowed_elements": ["details", "summary", "br"] }
}
```

(Exemplo ilustrativo: confira os números das regras e as opções na versão instalada; o motivo de cada desligamento vai em comentário no `CLAUDE.md` do projeto ou no PR.) CLIs: `markdownlint-cli2` ou `markdownlint-cli`.
- **Riscos:** o comando exato do cli2 em CI é **Não verificado**; `npx` baixa pacotes da rede, então prefira dependência de desenvolvimento fixada.
- **Rótulo:** Verificado para configuração (V-38); Não verificado para o comando de CI.

## T-03 lychee e lychee-action (V-39, Apache-2.0 ou MIT)

- **Como habilitar:** dois jobs (offline em PR, online agendado) em [workflow-docs-ci](../assets/templates/workflow-docs-ci.md). Comando local, só leitura de rede se online:

```bash
lychee --offline --include-fragments anchor-only "docs/**/*.md" README.md
```

- **Riscos:** `--offline` via `args` da action é **Inferido**; `peter-evans/create-issue-from-file` é action de terceiro (fixar por SHA e revisar); links externos nunca devem bloquear PR; o README da action chama de SHA-256 um hash de 40 caracteres (é SHA-1).
- **Rótulo:** Verificado em parte.

## T-04 Pipeline de GitHub Pages (V-40)

- **Como habilitar:** build em PR sem deploy; deploy no branch padrão com ambiente protegido (`upload-pages-artifact`, `deploy-pages`).
- **Riscos:** versões exatas das actions **Não verificadas**: leia o template atual do GitHub; `pull_request` em PR de fork, `permissions` mínimas e SHA são práticas Inferidas; o deploy é pulado em PR.
- **Rótulo:** Verificado (fluxo), Inferido (segurança).

## T-05 Comandos do produto (V-01)

`/doctor prompt-audit` (exige Claude Code 2.1.283 ou superior; instruções para modelos antigos, referências a arquivos/comandos inexistentes, conflitos), `/context`, `/memory`, `/init` (com CLAUDE.md existente sugere melhorias). Digite no Claude Code. **Risco:** comportamento muda por versão; confirme na instalação. **Rótulo:** Verificado na documentação.

## T-06 Plugin oficial `claude-md-management` (V-02, V-03, Apache-2.0)

- **Como habilitar:** instale pelo marketplace oficial por decisão sua (`/plugin` → Discover; confira o nome do marketplace na sua instalação, que não foi verificado aqui). Traz `claude-md-improver` e `/revise-claude-md`.
- **Riscos:** duplica parte de `auditar-claude-md` (não instale os dois sem querer); o `/revise-claude-md` declara `allowed-tools` sem Bash mas usa `find`; revalide a cada versão.
- **Rótulo:** Verificado.

## T-07 Verificação de exemplos de código (V-33, V-35)

```bash
python -m doctest -v caminho/modulo.py
cargo test --doc
pytest --doctest-modules
```

- **Riscos:** **executam código do projeto** (importam módulos): rode só em repositório de confiança e com sua autorização; `pytest --doctest-modules` é **Inferido**.
- **Rótulo:** Verificado (doctest, cargo), Inferido (pytest).

## T-08 `.github/release.yml` (V-42)

Modelo em [release-yml](../assets/templates/release-yml.md). **Risco:** o comportamento de PR sem categoria e sem `*` não é documentado; teste em repositório de exemplo. **Rótulo:** Verificado (campos), Inferido (ordem).

## T-09 Output style `escritor-tecnico` (V-08)

- **Como habilitar:** copie o conteúdo de [output-style-escritor-tecnico](../assets/templates/output-style-escritor-tecnico.md) para `~/.claude/output-styles/escritor-tecnico.md` (pessoal) ou `.claude/output-styles/escritor-tecnico.md` (projeto) e selecione o estilo (confira o comando na documentação da sua versão). Arquivos são lidos na inicialização do terminal.
- **Riscos:** vale para a conversa principal, não para subagentes; atrapalha tarefas de código sem relação; campo errado no frontmatter é ignorado sem erro; não use `force-for-plugin`.
- **Rótulo:** Verificado (V-08). O plugin não envia `output-styles/` (comportamento do validador com esse diretório: Não verificável).

## T-10 Validador de skills `skills-ref` (V-05)

```bash
skills-ref validate ./minha-skill
```

- **Riscos:** instalar a ferramenta é código de terceiros (decisão sua; mantenedor formal Não verificado). Alternativa sem instalar: aplique a regex da spec (`^[a-z0-9]+(-[a-z0-9]+)*$`, ≤ 64, igual ao diretório, `description` de 1 a 1.024) com o agente `revisor-de-instrucoes` ou `claude plugin validate`.
- **Rótulo:** Verificado (campos), Não verificado (mantenedor).

## T-11 mdarena (A/B de CLAUDE.md) (V-17)

Desenho A/B para comparar tarefas com e sem uma seção. **Risco alto:** o README declara `shell=True` e `--dangerously-skip-permissions`. Só em **sandbox** e **repositório de confiança**; rebaixado, **não recomendado por padrão**. **Rótulo:** Verificado (aviso do README).

## T-12 Hook PostToolUse que roda markdownlint (formato Inferido)

Roda o lint no arquivo `.md` editado. Formato exato do hook **Não verificável nesta etapa**: confira em https://code.claude.com/docs/en/hooks antes de usar.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path // empty' | grep -E '\\.md$' | xargs -r -d '\\n' markdownlint-cli2"
          }
        ]
      }
    ]
  }
}
```

- **Riscos:** executa shell a cada edição; depende de `jq`, `grep`, `xargs` e do CLI instalados (no Windows puro, `xargs -d` pode não existir); caminhos com espaço quebram variantes sem `-d '\n'`; os nomes dos campos do JSON de entrada (`tool_input.file_path`) são Inferidos; erro do hook pode poluir a sessão. Teste em repositório descartável. CI é a garantia compartilhada; este hook é conveniência local.
- **Rótulo:** Não verificável (formato); Inferido (campos).

## T-13 `claude plugin eval` (blueprint da fábrica; princípio P-40 de prompt-principles)

```bash
claude plugin eval .
claude plugin eval . --ablation none          # uma execução por caso, sem baseline (mais barato)
claude plugin eval . --ablation with-without  # adiciona o baseline sem plugin e mostra o Δ
```

Na raiz do plugin. **Riscos:** custo de tokens (o padrão já roda cada caso com e sem o plugin); exige Claude Code ≥ 2.1.269 (a CLI local da fábrica é 2.1.128, então os casos deste plugin ficam `designed_not_executed`); rode ≥ 3 vezes e compare com baseline sem plugin. **Rótulo:** Verificado (requisito de versão), Não aplicável a execução nesta etapa.

## T-14 Servidores MCP de documentação (Notion, Confluence, Google Docs, GitHub)

**Não pesquisados** (G-06): este plugin **não** recomenda nenhum servidor nem fornece JSON. Antes de habilitar qualquer MCP que escreve em documentos, avalie: escopo mínimo do token (somente leitura por padrão); escrita em nome do usuário exige confirmação por ação; conteúdo recuperado é dado, não instrução (injeção); origem e manutenção do servidor; onde os tokens ficam guardados (nunca em arquivo versionado). **Rótulo:** Não verificável.

## T-15 Permissões por caminho para o agente `technical-writer` (sintaxe Inferida)

Barreira real para o escopo de escrita (o prompt do agente só instrui). Confira a sintaxe em https://code.claude.com/docs/en/permissions antes de usar:

```json
{
  "permissions": {
    "allow": ["Edit(docs/**)", "Write(docs/**)"],
    "deny": ["Edit(.github/**)", "Write(.github/**)", "Edit(CLAUDE.md)", "Edit(AGENTS.md)"]
  }
}
```

- **Riscos:** padrão de caminho depende da versão; regras de `deny` e `allow` interagem com o modo de permissão da sessão; teste pedindo uma edição proibida e confirme o bloqueio.
- **Rótulo:** Inferido.
