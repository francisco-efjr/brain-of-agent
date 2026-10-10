# Template: relatório de bisect

| Campo | Valor |
| --- | --- |
| Sintoma | |
| Commit bom (hash, tag ou data) | |
| Commit ruim | |
| Script `check` (caminho) | |
| Árvore usada | (worktree separado ou árvore limpa) |

## Oráculo

Códigos de saída do script: 0 bom · 1 ruim · 125 não dá para testar (ex.: não compila) · acima de 127 aborta o bisect.

- [ ] Script lido antes de rodar (executa código do repositório em vários commits)
- [ ] `check` passa no commit bom e falha no ruim (saídas coladas)
- [ ] Teste determinístico (rodado várias vezes; intermitência descartada)

## Resultado

Primeiro commit ruim: `<hash>` · assunto · data · arquivos (`git show --stat`). Sem atribuir culpa pessoal.

Passos do bisect: N. Comando: `git bisect start HEAD <bom>` e `git bisect run sh -c "make || exit 125; ./check_test.sh"`.

## Correção

- Causa raiz:
- Teste que falhava antes e passa depois (caminho):
- Commit de correção: `fix(escopo): ...` com o teste junto
- Suíte do módulo após a correção (comando, código de saída, hora):
- `git bisect reset` executado: sim/não

Rótulos: Verificado / Inferido / Suposição / Não verificável. Histórico publicado não é reescrito.
