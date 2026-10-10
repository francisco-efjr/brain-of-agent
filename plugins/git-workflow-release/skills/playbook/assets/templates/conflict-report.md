# Template: relatório de resolução de conflitos

Operação em curso (merge / rebase / cherry-pick / revert):
Branch atual e branch de origem:
`merge.conflictStyle`: (`zdiff3` recomendado para mostrar a base)
Árvore estava limpa antes? (sim/não; em caso negativo, o `--abort` pode não restaurar)

| Arquivo | Intenção do lado A (nosso) | Intenção do lado B (deles) | Resolução | Risco | Teste que cobre |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Em rebase "nosso" e "deles" se invertem em relação ao merge: confirme pelo conteúdo das versões `:2:` e `:3:` (`git show :2:<arquivo>`), não pelo rótulo.

## Verificação

- [ ] `git grep -n '<<<<<<<\|>>>>>>>'` sem resultados
- [ ] `git diff --check` sem avisos
- [ ] `git status`: nenhum arquivo `UU`
- [ ] Lockfile e arquivos gerados regenerados com o comando do projeto
- [ ] Verificação do projeto (`<lint>`, `<test>`) rodou agora: saída e código de saída
- [ ] Conflitos de regra de negócio ou contrato resolvidos com resposta do dono (pergunta feita e respondida)

## Próximo passo (confirmação necessária)

`git add <arquivos>` e `git merge --continue` (ou `git rebase --continue`). Se a resolução ficou confusa: `git merge --abort` / `git rebase --abort` e recomeçar.

Rótulos: Verificado / Inferido / Suposição / Não verificável para cada decisão.
