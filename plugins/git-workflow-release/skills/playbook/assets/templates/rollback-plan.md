# Template: plano de rollback por revert

Adaptado do passo de revert do `land-and-deploy` do gstack (MIT, Copyright (c) 2026 Garry Tan), destilado. Só execute depois da escolha explícita de rollback pela pessoa. Revert **adiciona** commits inversos; produção só volta ao normal quando o rollback é implantado e verificado (`devops-cloud-infra`, `sre-observability`).

| Campo | Valor |
| --- | --- |
| PR / merge original | |
| SHA que entrou na base | |
| Pais do commit (`git show --no-patch --format='%H %P' <sha>`) | |
| Base protegida? | |
| Tag já publicada? | |

## 1. Pré-condições (se falhar, ROLLBACK PENDENTE; nunca reset ou force)

- [ ] Árvore limpa
- [ ] `git fetch` e base local só com fast-forward
- [ ] Base não está divergente nem ocupada em outro worktree

## 2. Forma do merge e comando

| Forma | Comando |
| --- | --- |
| Dois pais (merge commit) | `git revert -m 1 <sha>` (conferir que o pai 1 é a base) |
| Um pai, squash confirmado | `git revert <sha>` |
| Rebase merge | Estabelecer o intervalo exato de commits do PR e reverter do mais novo ao mais antigo (o `mergeCommit` sozinho é só o último) |
| Desconhecida ou merge externo | PARAR: ROLLBACK PENDENTE; pedir rollback manual; não adivinhar |

## 3. Publicação

- Base desprotegida: push só com confirmação (comando exato mostrado).
- Base protegida: manter o commit local, criar `revert/pr-<número>-<data>`, empurrar essa branch, abrir PR de revert; não mesclar sem aprovação separada.
- Conflito no revert: parar, mostrar `git status` e o comando; a resolução é da pessoa.
- **Nunca reverter um rollback automaticamente.**

## 4. Se há tag publicada

Não mover nem recriar. Publicar `vX.Y.Z+1` contendo o revert (ver `release-checklist.md`).

## 5. Efeitos irreversíveis a sinalizar

Migração de dados, e-mails enviados, cobranças, ativos já baixados. Reverter código não os desfaz; descreva a correção para frente:

## 6. Verificação pós-revert

- [ ] Suíte rodou na base após o revert (comando, código de saída, hora)
- [ ] `git log --oneline -5` mostra o revert
- [ ] Veredito: ROLLBACK PENDENTE ou REVERTIDO (só com evidência de que a base contém o revert e, se houver deploy, de que foi implantado e verificado)
