# Decisão, receitas e recuperação (rebase-seguro)

Sumário: 1 Tabela de decisão · 2 Receitas de limpeza · 3 Publicar histórico reescrito · 4 Revert por forma do merge · 5 Recuperação com reflog · 6 Fora de escopo · 7 Fontes.

Conferido em 2026-10-10 com o manual do Git (V-19, V-23, V-24) e as docs de proteção de branch do GitHub (V-27). Redação própria. Itens Inferido são conhecimento estável de Git não confirmado por teste dentro do Claude Code. Teste local: git 2.54.0, Windows.

## 1. Tabela de decisão

| Situação da branch | Quero | Faça | Não faça |
| --- | --- | --- | --- |
| Só local | Limpar commits | `fixup` + `rebase -i --autosquash`, ou `reset --soft` + novo commit | Nada especial; ainda assim crie `backup/<nome>` |
| Só local | Trazer a base nova | `git rebase origin/<principal>` | Merge da principal em branch curta gera ruído, mas é válido se a equipe prefere |
| Publicada só por mim | Limpar commits | Rebase + `push --force-with-lease --force-if-includes` após confirmação | `--force`; reescrever se há PR com reviews em andamento sem avisar |
| Publicada só por mim | Trazer a base nova | Rebase + lease, ou merge da base (sem reescrita) | |
| Compartilhada (time usa) | Qualquer limpeza | `git merge`; correções em novos commits | Rebase, amend, reset, force push (V-23: rebase de branch em que outros se baseiam é má ideia) |
| Principal ou protegida | Desfazer mudança publicada | `git revert` (PR de revert se a proteção exigir) | `reset --hard` + force push; GitHub bloqueia force push em protegidas por padrão (V-27) |
| Qualquer | Reaplicar o que foi revertido | Reverter o revert (V-24) | Mesclar de novo a mesma branch: o Git considera as mudanças já integradas e não as traz de volta |
| Qualquer | Recuperar commits sumidos | Seção 5 | `reset --hard` "para voltar" sem olhar o reflog |

Política de merge do repositório muda o raciocínio: com squash merge (padrão recomendado com release-please, V-33), a série de commits da branch é descartada na hora de mesclar, então limpar commits internos importa menos; o título do PR é o que fica. Com merge commit ou rebase-merge, cada commit entra no histórico principal e precisa estar bem escrito (e Conventional, se o repositório usa).

## 2. Receitas de limpeza (local ou publicada só por mim)

Rede de segurança, sempre antes:

```bash
git branch backup/<nome>              # ref nova; não altera nada
```

Juntar correções pequenas ao commit que elas consertam (V-23):

```bash
git commit --fixup=<sha-do-commit-alvo>            # cria "fixup! <assunto>"
GIT_SEQUENCE_EDITOR=true git rebase -i --autosquash <base>   # Inferido: aceita o roteiro gerado
# PowerShell: $env:GIT_SEQUENCE_EDITOR='true'; git rebase -i --autosquash <base>
```

Juntar tudo em um commit só (série bagunçada, tudo é um assunto):

```bash
git reset --soft $(git merge-base HEAD origin/<principal>)
git commit -m "tipo(escopo): descrição" -m "porquê"
```

Reescrever só a mensagem do último commit ainda não publicado: `git commit --amend` (com confirmação). Reescrever a mensagem de um commit mais antigo exige `reword` no rebase interativo: entregue o roteiro para a pessoa fazer no terminal, porque o editor não funciona aqui.

Mover uma branch para outra base (ex.: a feature nasceu de `develop` e deve nascer de `main`):

```bash
git rebase --onto origin/main origin/develop <branch>
```

Verificar a limpeza:

```bash
git diff backup/<nome> HEAD --stat     # vazio = mesma árvore (Inferido)
git log --oneline origin/<principal>..HEAD
```

Se a diferença não for vazia e você só reorganizou, algo foi perdido ou resolvido diferente: pare e investigue antes de publicar.

Cada commit continua compilando? (opcional, lento): `git rebase --exec '<comando de teste>' <base>`; se um commit falhar, o rebase para nele (Inferido; interativo em parte: entregue à pessoa se houver paradas).

## 3. Publicar histórico reescrito

```bash
git fetch origin <branch>                                   # atualiza a referência remota; pede permissão
git push --force-with-lease --force-if-includes origin <branch>
git ls-remote origin <branch>                               # compare com: git rev-parse HEAD
```

Por quê (V-19, manual do Git): `--force` desliga as checagens do lease e pode apagar commits de quem enviou depois de você; `--force-with-lease` sem valor esperado "interage muito mal" com fetch em segundo plano, porque a referência remota local pode já estar atualizada sem que você tenha integrado o conteúdo; `--force-if-includes` exige que o tip remoto tenha sido integrado localmente e não faz nada sem lease. Alternativa mais estrita: lease explícito `--force-with-lease=<branch>:<sha-esperado>`; confira a sintaxe em `git help push`.

Se o `fetch` trouxer commits de outra pessoa na branch, pare: ela é compartilhada e a regra muda para merge ou revert (seção 1). Antes de pedir confirmação, mostre: branch, quantos commits mudam, motivo, ponto de recuperação, e se há PR aberto (aprovações podem ser descartadas; conferir a regra "dismiss stale approvals" da proteção de branch, V-27). Nunca na principal; nunca `+refspec` nem `--force`.

## 4. Revert por forma do merge

Primeiro, descubra como o PR entrou na base. Não confie só no método pedido: olhe o commit real.

```bash
git show --no-patch --format='%H %P' <sha>   # um SHA = um pai; dois = merge commit
```

| Forma | Como reconhecer | Comando |
| --- | --- | --- |
| Merge commit | Dois pais; o pai 1 é a história da base | `git revert -m 1 <sha-do-merge>` |
| Squash | Um pai, mensagem do PR; um commit só | `git revert <sha>` |
| Rebase-merge | Vários commits novos na base, sem commit de merge | Reverter o intervalo exato do PR, do mais novo ao mais antigo (`git revert <primeiro>^..<último>`; o revert aplica na ordem inversa, Inferido: conferir com `git help revert`). O SHA de merge informado pelo GitHub sozinho é só o último commit, não o intervalo |
| Desconhecida (merge externo, fila de merge, força) | Não se encaixa nas anteriores | Pare e peça à pessoa o intervalo ou o PR |

Regras:
- Árvore limpa e base local atualizada por fast-forward (`git fetch`; se divergiu, pare). O revert acrescenta commits; nunca reescreve.
- Conflito no revert: pare, mostre `git status` e o comando; resolva com `resolver-conflitos` (revert tem a sua leitura de ours/theirs).
- Proteção da base rejeita push direto: crie `revert/<assunto>` com o commit de revert e abra PR (`criar-pr`); não o mescle sem aprovação separada.
- Reverter um merge faz o Git considerar aquelas mudanças como "nunca quero" em merges futuros da mesma branch; para trazê-las de volta, reverta o revert (V-24).
- Não reverta um rollback automaticamente (princípio do `land-and-deploy`, gstack, MIT): rollback que falhou é decisão humana.
- Depois do revert: rode os testes; se já havia release com a mudança, publique versão corretiva, não mova a tag (`release-cut`); estado externo (migração aplicada, e-mail enviado) não volta com o revert: registre em `rollback-plan.md`.

## 5. Recuperação com reflog

Situação típica: `git reset --hard` demais, rebase que perdeu commits, branch apagada.

```bash
git reflog -n 30            # somente leitura: lista movimentos de HEAD com SHAs
git log -g --oneline -20    # mesmo reflog em formato de log
```

Exemplo de saída (ilustrativa):

```text
4be2c1f HEAD@{0}: reset: moving to HEAD~3
9d0a7b3 HEAD@{1}: commit: fix(api): handle empty payload
c7e11aa HEAD@{2}: commit: feat(api): add rate limiting
```

O estado antes do `reset` é `HEAD@{1}` (9d0a7b3). Proponha (cria ref nova, não destrói nada):

```bash
git branch resgate/<nome> 9d0a7b3
git log resgate/<nome> -5          # confira que os commits estão lá
```

Só depois discuta como trazê-los de volta (merge, cherry-pick, ou apontar a branch original para o SHA com a confirmação da pessoa). Avisos: reflog é local e expira (padrão de 90 dias alcançáveis e 30 não alcançáveis; Inferido, `git help config`); mudanças que nunca foram commitadas não estão no reflog; `git stash drop`/`clear` são outra história (`git fsck --unreachable` pode ajudar, fora do escopo e Não verificado aqui).

## 6. Fora de escopo (lacunas declaradas)

- Backport para branch de manutenção com `git cherry-pick -x <sha>` e fluxos de release branches e hotfix: conhecimento estável, mas o plugin ainda não tem skill própria (lacuna G2).
- `git rerere`, `git filter-repo` e remoção de segredo do histórico: não lidos nem testados (G10); trate como incidente de segurança, não como rebase.
- Assinatura de commits e proveniência (G5).

## 7. Fontes

- Manual do Git: `git-rebase`, `git-push`, `git-revert` (V-23, V-19, V-24, classe B; licença não verificada, só destilado).
- Docs do GitHub: about protected branches e about pull request merges (V-27, classe B).
- gstack `land-and-deploy` Step 8, receita de revert por forma do merge (MIT, Garry Tan; destilado, sem o fluxo de deploy).
