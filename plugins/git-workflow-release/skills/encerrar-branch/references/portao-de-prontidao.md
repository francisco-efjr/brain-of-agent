# Portão de prontidão de merge (encerrar-branch)

Sumário: 1 Tabela do portão · 2 Como ler `mergeStateStatus` e `reviewDecision` · 3 Checks do SHA exato · 4 Deriva de versão · 5 Métodos de merge · 6 Limpeza segura · 7 Exemplo de relatório · 8 Fontes.

Conferido em 2026-10-10. Campos do `gh` e flags são conhecimento da CLI do GitHub: confirme com `gh pr view --help`, `gh pr checks --help` e `gh pr merge --help` na versão instalada (Inferido onde indicado). Redação própria; processo destilado do gstack `land-and-deploy` (MIT, Garry Tan) e das docs do GitHub (V-26, V-27, V-28).

## 1. Tabela do portão (todos somente leitura)

Preencha cada linha com o comando, o valor lido e o status (OK, PENDENTE, FALHOU, N/A, Não verificável). Qualquer FALHOU ou PENDENTE gera BLOQUEADO ou PENDENTE no veredito.

| # | Item | Comando | OK quando |
| --- | --- | --- | --- |
| 1 | `gh` autenticado | `gh auth status` | Logado no host do repositório |
| 2 | PR identificado pelo número | `gh pr view <n> --json number,state,isDraft,headRefOid,baseRefName,url` | `state` = `OPEN`, `isDraft` falso, base = a combinada |
| 3 | SHA do PR igual ao local | `git rev-parse HEAD` contra `headRefOid`; `git status --short` | Iguais e árvore limpa; se o local está atrás ou à frente, pare |
| 4 | Branch publicada | `git ls-remote --heads origin <branch>` | SHA remoto = `headRefOid` |
| 5 | Checks do SHA exato | `gh pr checks <n>` (e, se preciso, `gh run list --json headSha,conclusion,status,name` filtrando pelo SHA; `--commit` pode existir na sua versão, Inferido) | Todos os obrigatórios `pass` para esse SHA |
| 6 | Sem conflito | `gh pr view <n> --json mergeable,mergeStateStatus` | `mergeable` diferente de `CONFLICTING` |
| 7 | Revisão | `gh pr view <n> --json reviewDecision` | `APPROVED`, ou vazio quando o repositório não exige revisão |
| 8 | Donos de código | CODEOWNERS no repositório; "Require review from Code Owners" ligado na proteção (V-28) | Aprovação do dono incluída em `reviewDecision` |
| 9 | Deriva de versão | Seção 4 | Versão da branch maior ou igual à próxima da base, ou N/A |
| 10 | Política de merge | Método permitido pelo repositório (V-27) | O método escolhido é permitido |

Erro na consulta (rede, permissão) não é "sem checks": registre o erro e tente de novo. Zero checks após nova consulta é **Não verificável**: pergunte se o repositório realmente não tem CI e peça uma decisão por escrito antes de seguir.

## 2. Como ler `mergeStateStatus` e `reviewDecision`

Valores usuais do GitHub (conferir na versão da CLI; Inferido):

| `mergeStateStatus` | Significado prático | Ação |
| --- | --- | --- |
| `CLEAN` | Pode mesclar | Seguir |
| `BLOCKED` | Falta revisão, check obrigatório ou outra regra | Descobrir qual (itens 5, 7, 8) |
| `BEHIND` | A base avançou e a proteção exige branch atualizada | Atualizar a branch (merge da base ou `rebase-seguro`) e refazer o portão |
| `DIRTY` | Conflito com a base | `resolver-conflitos` |
| `UNSTABLE` | Falha em check não obrigatório | Listar a falha; decisão da pessoa |
| `HAS_HOOKS` | Há hooks de merge | Informar |
| `DRAFT` | PR em rascunho | Marcar como pronto antes |
| `UNKNOWN` | GitHub ainda calcula | Consultar de novo em instantes |

| `reviewDecision` | Significado |
| --- | --- |
| `APPROVED` | Aprovado conforme as regras |
| `CHANGES_REQUESTED` | Há pedido de mudança aberto |
| `REVIEW_REQUIRED` | Falta aprovação |
| vazio | Repositório não exige revisão |

## 3. Checks do SHA exato

Por quê: nome de workflow igual com outro SHA não é evidência, e um push novo invalida a aprovação de CI anterior. O portão compara sempre `headRefOid` do PR com o SHA dos checks.

- Check obrigatório pendente: PENDENTE. Reconsulte depois de alguns minutos; o limite de espera de 15 minutos é Suposição (gstack usa esse valor).
- Check opcional falhando: liste e deixe a pessoa decidir.
- Workflows que só rodam em `push` para a base não aparecem no PR: isso é N/A, não falha.
- PR vindo de fork pode ter checks que aguardam aprovação para rodar: PENDENTE, não verde.

## 4. Deriva de versão (só se o repositório tem `VERSION`, `package.json` com versão ou `CHANGELOG`)

Outra branch pode ter mesclado uma versão igual ou maior depois que a sua foi preparada. Compare números, nunca texto:

```bash
git show origin/<base>:VERSION        # versão atual da base
git show HEAD:VERSION                 # versão da branch
printf '%s\n%s\n' 1.9.0 1.10.0 | sort -V     # exemplo: 1.10.0 vem depois de 1.9.0 (Git Bash)
```

Texto compara `1.9.0` maior que `1.10.0`; número não. Versão da branch menor que a da base, ou igual à de outra release já mesclada: pare e peça atualização (duplicar versão sobrescreve notas de outra release). Versão ausente ou ilegível em só um dos lados: Não verificável, não verde. Arquivo `VERSION` inexistente: N/A.

## 5. Métodos de merge (V-27, V-33)

| Método | Efeito | Quando |
| --- | --- | --- |
| Squash | Um commit na base; título do PR vira o assunto; SHAs da branch somem | PR pequeno, histórico linear, release-please (recomendação do projeto) |
| Merge commit | Preserva commits e cria commit de merge | Série de commits atômicos que importa para bisect e para o histórico |
| Rebase-merge | Reaplica commits com SHAs novos, sem commit de merge; descarta vazios | Histórico linear com commits já bons; cada commit precisa ser Conventional se o repositório usa isso |

O método permitido vem da configuração do repositório. A pessoa confirma o método; a skill não troca por conta própria. Reverter depois depende da forma do merge (`rebase-seguro`).

## 6. Limpeza segura (V-12, V-20)

Antes de remover qualquer coisa, os três "não, não, sim":

1. Alterações não commitadas no worktree? `git -C <caminho> status --short`.
2. Commits sem push? `git -C <caminho> log @{u}.. --oneline` (sem upstream, trate como "há commits só aqui" até provar o contrário).
3. Branch mesclada? `gh pr view <n> --json state,mergeCommit` mostra `MERGED`.

Mesclado e limpo: `git worktree remove <caminho>` (confirmação). Não mesclado ou com pendência: manter e anotar `claude --worktree <nome> --resume` (V-12). Nunca `--force` sem confirmação: `remove` só aceita worktree limpo, e `--force` duas vezes é necessário se estiver travado (V-20).

Depois do squash, `git branch -d` recusa ("not fully merged") porque os commits da branch não existem na base. Procedimento: confirmar `MERGED` e que `headRefOid` do PR é o tip da branch (`git rev-parse <branch>`), registrar o SHA no relatório e então pedir confirmação para `git branch -D <branch>`. Recuperação: `git branch resgate/<nome> <sha>` com o SHA anotado.

## 7. Exemplo de relatório (ilustrativo)

```markdown
Veredito: MESCLADO (squash, merge SHA 5d2c7e1). Não implica deploy.

| # | Item | Valor lido | Status |
| 2 | PR #88 | OPEN, não rascunho, base main | OK |
| 3 | SHA | headRefOid = HEAD local = a1b2c3d; árvore limpa | OK |
| 5 | Checks | 3 de 3 obrigatórios pass para a1b2c3d | OK |
| 6 | Conflito | mergeable = MERGEABLE, CLEAN | OK |
| 7 | Revisão | APPROVED (1 dono de código) | OK |
| 9 | Versão | N/A (sem VERSION) | N/A |

Executado (com confirmação): gh pr merge 88 --squash --match-head-commit a1b2c3d
Limpeza: worktree ../app-export removido; branch local apagada com -D após conferir MERGED (SHA a1b2c3d anotado)
Pendente: apagar branch remota (pergunto); deploy e verificação em produção: fora desta skill
Próximo passo: release-cut se for cortar versão
```

## 8. Fontes

- gstack `land-and-deploy`, pré-voo, gate de CI por SHA e tabela de veredito (MIT, Garry Tan; processo destilado sem deploy).
- superpowers `finishing-a-development-branch` (MIT; V-16): menu sem padrão e palavra `discard`.
- Docs do GitHub: about protected branches, about pull request merges, about code owners (V-27, V-28, classe B; destilado).
- Claude Code worktrees (V-12, classe A; destilado) e manual de `git worktree` (V-20, classe B).
