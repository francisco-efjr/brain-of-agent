# História e git avançado

Push com lease, worktrees, bisect, conflitos, rebase, revert, tags e recuperação. Fontes por ID em [fontes.md](fontes.md). Confira flags no Git instalado (`git --version`; as verificações da pesquisa usaram 2.54.0 no Windows).

## Sumário

1. Regra de ouro e classificação da branch
2. Push e lease (V-19)
3. Worktree manual (V-20)
4. Bisect (V-21)
5. Conflitos (V-22)
6. Rebase, fixup e autosquash (V-23)
7. Desfazer: revert, inclusive de merge (V-24)
8. Revert por forma do merge (GS-land)
9. Tags (V-25)
10. Recuperação: reflog e backup (P-32)
11. Backport e hotfix (lacuna G2)
12. Tabela "o que fazer quando"

## 1. Regra de ouro e classificação da branch

"Rebasing... a branch that others have based work on is a bad idea" (V-23, citação curta). Classifique antes de escolher a operação:

| Classe | Como verificar | Pode reescrever? |
| --- | --- | --- |
| Só local | `git branch -r --contains HEAD` vazio | Sim, livremente |
| Publicada só por mim | Existe no remoto; ninguém mais baseou trabalho | Sim, com `--force-with-lease --force-if-includes` após confirmação |
| Compartilhada | Outros commits ou PRs apoiam-se nela | Não: `merge` ou `revert` |
| Protegida | Proteção de branch (`gh pr view`, configurações; V-27) | Não: o GitHub bloqueia force push por padrão |

## 2. Push e lease (V-19)

| Comando | Efeito | Uso |
| --- | --- | --- |
| `git push --force` | Sobrescreve o remoto; "can cause the remote repository to lose commits"; desliga as checagens do lease | Nunca |
| `git push --force-with-lease` | Só sobrescreve se o remoto ainda está como você viu | Com cautela: sem valor esperado "interacts very badly" com fetch em segundo plano |
| `--force-with-lease --force-if-includes` | Soma checagem de que o tip remoto está contido no seu histórico local; `--force-if-includes` sem lease é "no-op" | Forma recomendada para branch própria publicada, após confirmação |
| `--force-with-lease=<ref>:<esperado>` | Lease explícito | Quando há fetch automático |
| `+refspec` | Força só aquele ref | Trate como force |

Regra de CLAUDE.md pronta: S-07 em [claude-md-snippets.md](claude-md-snippets.md). Nunca na principal; mostre branch, motivo e comando antes de executar.

## 3. Worktree manual (V-20)

```bash
git worktree add ../projeto-tarefa -b tarefa   # cria pasta e branch nova
git worktree list
git worktree remove ../projeto-tarefa           # só se limpo; --force duas vezes se travado
git worktree prune -n                           # simulação, quando a pasta foi apagada à mão
git worktree prune
git worktree repair                             # reconecta worktrees movidos
```

`add` recusa uma branch já extraída em outro worktree (`--force` contorna; evite). Os worktrees do Claude Code têm regras próprias em [claude-code-no-fluxo-git.md](claude-code-no-fluxo-git.md).

## 4. Bisect (V-21)

Códigos de saída do script em `git bisect run`: **0** bom · **125** pular (não dá para testar, ex.: não compila) · **1 a 127 exceto 125** ruim · qualquer outro (inclusive 128 ou mais) **aborta** o bisect.

```text
1. Escreva e rode o teste que reproduz a falha (ver revisao-e-verificacao.md, seção 8). Saída 0 se bom, 1 se ruim, 125 se não compila.
2. Árvore limpa (commit ou stash) ou, melhor, um worktree separado. Leia o script: o bisect o executa em vários commits.
3. Valide o oráculo: rode o script no commit bom (passa) e no ruim (falha). Se o "bom" não é bom, pare.
4. git bisect start HEAD <commit-bom>      (--first-parent se houver merges quebrados)
5. git bisect run sh -c "make || exit 125; ./check_test.sh"
6. Anote o primeiro commit ruim (git show --stat) e rode git bisect reset.
7. Corrija em commit novo; não reescreva histórico publicado.
```

O exemplo do passo 5 segue a página oficial. Árvore suja não é advertida pela página: a recomendação de limpar é boa prática (Inferido). Teste intermitente dá resultado errado: rode o `check` várias vezes antes (Inferido). Em repositório de terceiros, executar o script é executar código não confiável.

## 5. Conflitos (V-22)

Marcadores: `<<<<<<<`, `=======`, `>>>>>>>`. Com `merge.conflictStyle` em `diff3` ou `zdiff3` a base aparece também.

```text
Antes: árvore limpa (commit ou stash). Considere `git config merge.conflictStyle zdiff3`.
1. `git status` e `git diff --name-only --diff-filter=U` listam os arquivos em conflito.
2. Por arquivo: leia a base e as duas versões (`git log --merge -p <arquivo>`; `git show :1:<arquivo>` base, `:2:` nosso, `:3:` deles); escreva em duas frases a intenção de cada lado.
3. Resolva combinando as intenções. Intenções incompatíveis (regra de negócio, contrato público, schema): pare e pergunte.
4. Remova todos os marcadores (`git grep -n '<<<<<<<\|>>>>>>>'` deve voltar vazio; `git diff --check`), depois `git add <arquivo>`.
5. Rode a verificação e só então `git merge --continue` (em rebase: `git rebase --continue`).
6. Se ficou confusa: `git merge --abort` (ou `git rebase --abort`) e recomece.
```

Cuidados:
- `git merge --abort` pode não restaurar alterações não commitadas anteriores: por isso comece com árvore limpa.
- Em **rebase**, "nosso" e "deles" se invertem em relação ao merge (conhecimento estável de Git, Inferido; confira no manual instalado). Por isso prefira ler as versões por `:2:` e `:3:` e decidir pelo conteúdo, não pelo rótulo.
- Lockfile e arquivo gerado: regenere com o comando do projeto, não edite à mão.
- Binário: pergunte qual versão.
- `git diff --check` e `git rerere` não foram lidos na fonte (G10); `--check` é Inferido.

## 6. Rebase, fixup e autosquash (V-23)

Ações do todo: `pick`, `reword`, `edit`, `squash`, `fixup`, `drop`. `--continue`, `--skip`, `--abort`, `--quit`. `--update-refs` atualiza branches empilhadas (exceto as extraídas em worktree). Rebase cria commits novos; o tip anterior fica acessível por `@{1}` no reflog.

```text
- Antes: git branch backup/<nome>   (rede de segurança)
- Corrigir um commit anterior: git commit --fixup=<sha>
- Limpar: git rebase -i --autosquash <base>
- Conflito: resolver (seção 5) e git rebase --continue; perdeu o fio: git rebase --abort
- Publicar depois de reescrever: git push --force-with-lease --force-if-includes (só com confirmação)
```

O editor interativo não funciona em ambiente de agente. Alternativa **Inferida e não testada**: `GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash <base>` aceita o todo gerado pelo autosquash; se falhar, entregue os comandos para a pessoa rodar no terminal. Depois de reordenar ou juntar commits sem mudar conteúdo, `git diff backup/<nome> HEAD --stat` deve vir vazio (Inferido).

## 7. Desfazer: revert, inclusive de merge (V-24)

`git revert` cria commits novos que desfazem outros; exige árvore limpa; merge exige `-m <n>` (pai principal); `--no-commit` agrupa vários reverts. Reverter um merge "declara que você nunca quer" aquelas mudanças: merges posteriores trazem só o que não é ancestral do merge revertido. Para reaplicar um merge revertido, **reverta o revert**. A página não compara revert com reset em histórico publicado: preferir revert é Inferido (revert acrescenta histórico, reset o remove).

## 8. Revert por forma do merge (GS-land Step 8, MIT, destilado)

Entre só depois da escolha explícita de rollback pela pessoa. Explique que isso adiciona commits inversos; produção não volta ao estado anterior até o rollback ser implantado e verificado (isso é de `devops-cloud-infra` e `sre-observability`).

1. Árvore limpa; `git fetch`; atualizar a base local só com fast-forward. Base suja, divergente ou ocupada: **parar** com "ROLLBACK PENDENTE"; nunca reset, force ou descarte.
2. Inspecionar o commit que de fato entrou: `git show --no-patch --format='%H %P' <sha-do-merge>`.

| Forma encontrada | Comando |
| --- | --- |
| Dois pais (merge commit) | Conferir que o pai 1 é o histórico da base; `git revert -m 1 <sha>` |
| Um pai, squash confirmado | `git revert <sha>` |
| Rebase merge | Estabeleça o intervalo exato de commits do PR e reverta do mais novo ao mais antigo. O `mergeCommit` sozinho é só o último commit, não o intervalo |
| Forma ou intervalo desconhecido (inclusive merge externo) | **Parar** com "ROLLBACK PENDENTE" e pedir rollback manual; não adivinhar |

3. Conflito no revert: parar, mostrar `git status` e o comando tentado; a resolução é da pessoa.
4. Publicar: a base protegida rejeita push direto. Mantenha o commit, crie `revert/pr-<número>-<data>`, empurre essa branch e abra um PR de revert contra a base. Informe a URL e "ROLLBACK PENDENTE"; não mescle sem aprovação separada. Outro erro de push: parar e informar, sem contornar proteção.
5. **Nunca reverter um rollback automaticamente.** Se já existe tag, publique versão corretiva `vX.Y.Z+1` contendo o revert (ver `releases-e-versionamento.md`).

Modelo preenchível: `assets/templates/rollback-plan.md`.

## 9. Tags (V-25)

Tags anotadas (`-a`, `-s`, `-u`) "are meant for release"; leves são rótulos privados. `git describe` ignora leves por padrão. `-s` assina; `git tag -v <tag>` verifica; `--sort=version:refname` ordena por versão. "Git does not change tags behind users back... use a different name": **nunca mova ou recrie tag publicada**; publique a versão seguinte.

```bash
git tag -a v1.4.0 -m "Release 1.4.0"      # anotada
git tag -v v1.4.0                          # verifica (tag assinada)
git ls-remote --tags origin v1.4.0         # confirma no remoto, depois do push
git push origin v1.4.0                     # só com confirmação; push de tag não consta em V-25 (conhecimento geral)
```

## 10. Recuperação: reflog e backup (P-32, Inferido)

Prompt/procedimento para "perdi meus commits" após reset, rebase ou branch apagada:

1. Entenda o que se perdeu e qual foi o último comando suspeito.
2. Somente leitura: `git reflog -n 30` e `git log -g --oneline`; identifique o SHA anterior (também `@{1}` para o tip anterior de uma branch rebaseada).
3. **Proponha** `git branch resgate/<nome> <sha>` (cria ref nova, não destrói nada) e confirme com `git log resgate/<nome> -5`.
4. Só depois discuta reset ou merge. Nunca `reset --hard` sem confirmação.
5. Avise: o reflog é local e expira; recupere cedo.

Rótulo: Inferido (V-23 cobre `@{1}`; o resto é conhecimento estável do Git, marcado como coberto só de passagem na pesquisa).

## 11. Backport e hotfix (lacuna G2: conhecimento estável, Inferido, não pesquisado)

A pesquisa não fechou release branches, backport nem rollback além do `revert`. O mínimo prático, a conferir no manual (`git cherry-pick --help`):

- Corrija na branch principal primeiro, com teste; só então leve a correção para a linha mantida.
- `git cherry-pick -x <sha>` em uma branch `release/x.y` acrescenta ao commit a referência do original (rastreabilidade).
- Cada backport é um PR para a branch de release, com tag de patch própria (`vX.Y.Z+1`).
- Conflitos de cherry-pick seguem a seção 5.
- Se isso for frequente no seu produto, trate como lacuna a pesquisar antes de automatizar.

## 12. Tabela "o que fazer quando"

| Situação | Ação | Confirmar? |
| --- | --- | --- |
| Commit ruim ainda local | `git commit --fixup` + autosquash, ou novo commit | Não (local) |
| Commit ruim já publicado em branch compartilhada | `git revert <sha>` | Push: sim |
| Branch própria publicada, limpar série | Backup + rebase + push com lease | Sim |
| Merge com problema na principal | Seção 8 | Sim, e PR de revert |
| Perdi commits | Seção 10 | Não (só cria ref) |
| Tag errada já publicada | Nova versão; não mover | Sim |
| Não sei em que commit quebrou | Seção 4 | Executar o script: sim, após ler |
