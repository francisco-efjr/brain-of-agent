# Ferramentas, hooks e MCP recomendados (todos desativados)

Nada deste arquivo vem ativo no plugin: não há `hooks/hooks.json`, `.mcp.json`, `.lsp.json` nem `bin/`. Cada entrada traz o que é, como habilitar conscientemente, riscos e rótulo. Habilitar é decisão sua, no seu projeto. Fontes por ID em [fontes.md](fontes.md).

## Sumário

1. Princípio: instrução é pedido, permissão e hook são garantia
2. T-01 Hook `git-guard.ps1`
3. T-02 Regras `deny` como piso rígido
4. T-03 `/goal` e Stop hook
5. T-04 `.worktreeinclude` e `.gitignore`
6. T-05 `gh` CLI
7. T-06 claude-code-action
8. T-07 release-please-action
9. T-08 Changesets
10. T-09 `.github/release.yml`
11. T-10 Configurações de git
12. T-11 Servidor MCP do GitHub
13. T-12 `claude plugin eval`
14. T-13 Loop Ralph em versão segura
15. T-14 Commitlint e pre-commit do projeto
16. Execução sem supervisão: o risco de `--dangerously-skip-permissions`

## 1. Princípio

O frontmatter `allowed-tools` apenas pré-aprova ferramentas durante o turno; a doc diz que não restringe quais ferramentas existem (V-04). Hook `PreToolUse` é de melhor esforço e contornável (`git -c`, alias, `bash -c`, variáveis), e a doc recomenda o sistema de permissões para impor allow ou deny rígido (V-07). Por isso a ordem de confiança é: regra `deny` de permissão, depois hook, depois CLAUDE.md, depois a skill. Rótulo: Verificado em V-04 e V-07; a ordem como política é Inferida.

## 2. T-01 Hook `git-guard.ps1` (PreToolUse, matcher Bash)

**O que faz:** bloqueia force push cego (`--force`, `-f`, `+refspec`) com exit 2; pergunta (`ask`) para push que apaga ref remota, push com `--force-with-lease`, push na principal e `git reset --hard`. Script próprio, testado em 12 comandos de exemplo fora do Claude Code (bloqueia `--force`, `-f`, `-fu`, `+main`; pergunta nos demais casos listados; deixa passar `git push -u origin feat/x` e `git status`).

Salve como `.claude/hooks/git-guard.ps1` no seu projeto:

```powershell
# git-guard.ps1 - PreToolUse, matcher Bash. Sem dependências externas.
$p = [Console]::In.ReadToEnd() | ConvertFrom-Json
$cmd = [string]$p.tool_input.command
function Ask($why) {
  @{ hookSpecificOutput = @{ hookEventName = 'PreToolUse'; permissionDecision = 'ask'; permissionDecisionReason = $why } } | ConvertTo-Json -Compress -Depth 4
  exit 0
}
if ($cmd -match '(^|[\s;&|])git\s+(?:-\S+\s+)*push\b') {
  if ($cmd -match '\s--force(\s|$)' -or $cmd -match '\s-[a-zA-Z]*f[a-zA-Z]*(\s|$)' -or $cmd -match '\spush\b.*\s\+[^\s]') {
    [Console]::Error.WriteLine('Bloqueado: use --force-with-lease --force-if-includes, só após confirmação do usuário.')
    exit 2
  }
  if ($cmd -match '\s(--delete|-d)(\s|$)' -or $cmd -match '\s:[^\s]+') { Ask 'Push remove uma ref remota. Confirme.' }
  if ($cmd -match '\s--force-with-lease') { Ask 'Push com reescrita de histórico. Confirme branch e motivo.' }
  if ($cmd -match '\s(main|master|HEAD:main|HEAD:master)(\s|$)') { Ask 'Push para a branch principal. Confirme.' }
}
if ($cmd -match '(^|[\s;&|])git\s+reset\s+--hard') { Ask 'git reset --hard descarta trabalho não commitado. Confirme.' }
exit 0
```

**Registro em `.claude/settings.json`** (Verificado em code.claude.com/docs/en/hooks, 2026-10-10: estrutura evento → matcher → hooks; forma `command` + `args` roda o executável direto, sem shell, e no Windows exige um executável real, como `powershell.exe`; campo `if` com sintaxe de regra de permissão; saída `hookSpecificOutput` com `hookEventName` e `permissionDecision` `allow`, `deny`, `ask` ou `defer`; exit 2 bloqueia):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(git *)",
            "command": "powershell.exe",
            "args": ["-NoProfile", "-File", "${CLAUDE_PROJECT_DIR}/.claude/hooks/git-guard.ps1"]
          }
        ]
      }
    ]
  }
}
```

**Riscos e limites:**
- Contornável; não é fronteira de segurança. Combine com T-02.
- O formato do registro e do JSON de saída está conferido na documentação, mas o script **não foi executado dentro do Claude Code**: teste em repositório descartável antes de confiar (G7).
- Exit 2 bloqueia sem permitir confirmação; por isso os casos confirmáveis usam `ask`.
- Um timeout ou falha do hook não bloqueia por padrão (Verificado na doc); `"onFailure": "block"` no hook exige Claude Code 2.1.295 ou superior.
- Versão bash equivalente: não escrita nem testada (lacuna G14). Em macOS/Linux, use T-02 ou escreva e teste o equivalente antes de confiar.
- Antes de ativar, leia o script inteiro: hook roda código na sua máquina a cada comando Bash.

Rótulo: mecanismo Verificado (V-07); desenho Inferido (a doc não traz exemplo que bloqueie `git push`); script testado localmente fora do Claude Code.

## 3. T-02 Regras `deny` de permissão (piso rígido)

Em `.claude/settings.json` do projeto (ou nas configurações de usuário):

```json
{
  "permissions": {
    "deny": [
      "Bash(git push --force *)",
      "Bash(git push -f *)",
      "Bash(git push * --force *)",
      "Bash(git push * --force)",
      "Bash(git push * -f)",
      "Bash(git reset --hard *)",
      "Bash(git clean -fd*)"
    ]
  }
}
```

**Riscos:** a sintaxe `Bash(prefixo *)` (espaço antes do `*` final, que também casa o comando sem argumentos) está **Verificada** em code.claude.com/docs/en/permissions (2026-10-10); as regras de `deny` valem para subcomandos de comandos compostos. Os padrões com `*` no meio cobrem `--force` depois do remoto e da branch. Cobertura parcial, também confirmada na doc: `git -C pasta push --force`, `git -c k=v push`, aliases, caminho absoluto do executável e `bash -c "..."` não casam, e `--force-with-lease` não casa com `--force *` por desenho (use o hook T-01 para pedir confirmação nele). Teste cada regra pedindo ao Claude para executar um comando inofensivo equivalente em um repositório descartável.

## 4. T-03 `/goal` e Stop hook (gate determinístico de "pronto")

Segundo V-01, o critério de sucesso pode virar `/goal` (condição reavaliada a cada turno) ou Stop hook (bloqueio até o check passar). Os pesquisadores **não leram** as páginas `goal` e `hooks#stop` (G6). Leia-as antes de usar; só então escreva a condição, por exemplo "a suíte `<test>` sai com código 0 e `git status --short` está limpo". Rótulo: Não verificável além da menção em V-01.

## 5. T-04 `.worktreeinclude` e `.gitignore` de worktrees

```gitignore
# .gitignore
.claude/worktrees/
```

```gitignore
# .worktreeinclude (sintaxe gitignore; só copia o que também está ignorado pelo git)
.env.local
```

Riscos: baixo. O arquivo copia segredos locais para o worktree; inclua só o necessário. Rótulo: Verificado em V-12. Detalhes de uso em [claude-code-no-fluxo-git.md](claude-code-no-fluxo-git.md).

## 6. T-05 `gh` CLI

- Autenticação feita por você: `gh auth login` (o plugin e o Claude não devem receber o token em chat nem em arquivo).
- As skills do plugin só pré-aprovam subcomandos de **leitura** (`gh pr view`, `gh pr checks`, `gh run list`, `gh release view`, `gh repo view`, `gh auth status`). Criar PR, mesclar e criar release ficam fora da pré-aprovação e pedem confirmação.
- Riscos: o token escreve em seu nome; prefira escopo mínimo. GitHub Enterprise e GitLab (`glab`) só como detecção de plataforma (G11).
- Flags e campos de `--json` mudam entre versões: confira `gh pr view --help`. Rótulo: Inferido (conhecimento estável da CLI, não conferido na fonte nesta pesquisa).

## 7. T-06 `anthropics/claude-code-action`

Sem YAML aqui: o exemplo das lentes de pesquisa não veio da documentação (descartado na validação). Antes de implementar, leia o README, `docs/usage.md`, `docs/solutions.md` e `docs/security.md` do repositório. Checklist de segurança (V-10, classe A):

- [ ] Gatilho restrito a quem tem acesso de escrita; sem `allowed_non_write_users` nem `allowed_bots="*"`.
- [ ] Ferramentas por `--allowedTools` em lista mínima; sem shell amplo.
- [ ] Permissões do job mínimas (`contents: read`; `pull-requests: write` só se for postar).
- [ ] PR de fork sem segredos; nunca checkout do head não confiável no contexto de `pull_request_target`.
- [ ] Prompt fixo: contexto, passos, ferramentas, destino do resultado (comentário ou branch).
- [ ] Sem permissão de push na branch principal; mudanças vão para branch nova e PR.
- [ ] Commits verificados: `use_commit_signing` ou `ssh_signing_key` (o primeiro impede rebase e cherry-pick).

Riscos: injeção de prompt por conteúdo de PR, issue e comentário. Autoria de workflows é do plugin `automation-integrations`.

## 8. T-07 `release-please-action`

Use `googleapis/release-please-action` conforme o README do release-please (V-33, Apache-2.0). Exige Conventional Commits, recomenda squash merge e **não** publica em gerenciadores de pacotes. Conteúdo da action e configuração de monorepo (manifesto) não foram lidos (G3): leia `docs/manifest-releaser.md` antes. Rótulo: Verificado para o comportamento do README; Não verificável para a action.

## 9. T-08 Changesets

Arquivos `.changeset/*.md` descrevem o tipo de bump por PR; versões e changelog saem de um passo separado. Os comandos `add`, `version` e `publish` **não** foram confirmados na página lida (V-35): consulte a documentação oficial antes de escrever workflow ou skill. Rótulo: Verificado só para o conceito.

## 10. T-09 `.github/release.yml`

Modelo em `assets/templates/release-notes-and-release-yml.md`. Risco baixo; Verificado em V-34.

## 11. T-10 Configurações de git

```bash
git config merge.conflictStyle zdiff3   # mostra também a base nos conflitos (V-22)
git config rebase.autoSquash true       # --autosquash por padrão no rebase interativo (V-23)
```

`git rerere` não foi lido: não recomendado até documentar e testar (G10). Valide `zdiff3` com `git --version` (disponível em versões recentes do Git; confira no seu).

## 12. T-11 Servidor MCP do GitHub

Não pesquisado nesta rodada (G13), portanto **sem JSON de configuração**: não vou inventar pacote, comando nem URL. Se você decidir usar um, verifique antes: quem mantém o servidor, licença, escopo mínimo do token, se há modo somente leitura, que ferramentas de escrita expõe (criar PR, mesclar, comentar) e se cada uma pede confirmação. A forma geral de adicionar um servidor é `claude mcp add` seguida de transporte e comando, conforme a documentação atual do Claude Code. Rótulo: Não verificável.

## 13. T-12 `claude plugin eval`

```bash
claude plugin eval . --trust-plugin --allow-tools Write Edit "Bash(git *)"   # exemplo: cases que tocam Bash/Write/Edit exigem concessão explícita
claude plugin eval . --ablation none --runs 1 --case <nome>                  # uma execução de um caso, sem a comparação sem plugin
```

Verificado em code.claude.com/docs/en/plugin-evals (2026-10-10): exige Claude Code 2.1.269 ou superior e Git 2.31 ou superior; 3 execuções por caso e por braço por padrão; `--ablation none|with-without`; `Bash`, `Write`, `Edit`, `WebFetch` e `WebSearch` são removidos da sessão se você não os conceder com `--allow-tools`; com `Bash` concedido o comando roda no sandbox do SO, e o Windows nativo não tem backend (use WSL2). Os evals deste plugin estão `designed_not_executed`.

## 14. T-13 Loop Ralph em versão segura (só aqui, nunca ativo)

O prompt original do loop manda `git add -A`, commit, push e tags automáticos: reprovação automática pela rubrica. Se você quiser um loop mesmo assim, use a versão restrita (Suposição, não testada):

- worktree dedicado e descartável; nenhum remoto configurado ou push proibido por `deny`;
- um item de uma lista por iteração, com teste como contrapressão;
- limite de iterações definido (ex.: 5) e parada quando a verificação falhar duas vezes pela mesma causa;
- `git add` por caminho, nunca `git add -A`; commit local apenas;
- você revisa o resultado e decide push/PR.

## 15. T-14 Commitlint e pre-commit do projeto

Use o que o repositório já tem; não instale ferramentas novas por sugestão do plugin. Ferramentas de terceiros não foram pesquisadas. Se existir `commitlint`, a skill de commit deve respeitar a configuração dele.

## 16. Execução sem supervisão: o risco de `--dangerously-skip-permissions`

Rodar o Claude sem prompts de permissão (`--dangerously-skip-permissions`) remove a confirmação que este plugin usa como garantia para push, merge, tag e release. **Risco alto**; se for inevitável, restrinja a sandbox descartável ou repositório trivial e confiável, sem credenciais de escrita remota, e prefira alternativa: allowlist em `settings.json` + T-02 + `/goal` ou Stop hook (T-03). Nunca use esse modo em repositório de terceiros nem com tokens de produção. Rótulo: Inferido (o risco é citado como anti-padrão nas bases da fábrica e a flag não foi reaberta na documentação nesta pesquisa; confira `claude --help`). A política de uso restrito é da casa.
