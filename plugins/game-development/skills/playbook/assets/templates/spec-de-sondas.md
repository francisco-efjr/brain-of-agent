# Especificação de sondas de teste do jogo

Tarefa pequena, aprovada **antes** de mecânicas novas. Fonte do padrão: caso do port Amiga para Godot (blog, classe B) e check curto do compilador C (Anthropic Engineering). A transposição a jogo novo é Inferido.

| Flag | Efeito | Saída ou formato | Exemplo |
| --- | --- | --- | --- |
| `--level <id>` | carrega direto a cena de teste | log `level=<id> loaded` | `-- --level test_spawn` |
| `--drive <arquivo>` | injeta input por script (`quadro:ação`) | log `drive done frames=<N>` | `-- --drive tests/dash.drive` |
| `--probe` | imprime estado interno em texto | `probe t=<quadro> chave=valor ...` | `probe t=61 player.x=312.0 stamina=40` |
| `--screenshot <arquivo>` | salva captura e sai | caminho do arquivo | `-- --screenshot out/dash.png` |
| `--quick` e `--full` (no `check`) | amostra determinística ou tudo | resumo de até 20 linhas | `check --quick` |

## Regras

1. Saída do `check`: no máximo 20 linhas; erros como `ERROR[sistema] mensagem`; detalhe em `build/check.log`.
2. Sondas só leem estado (não o alteram) e não entram em build de release.
3. Dois checks headless de projeto: compilar todos os scripts; carregar todos os níveis relatando falhas.
4. Com referência (captura aprovada, build anterior), compare a saída de `--probe` linha a linha.
5. Godot: argumentos do jogo vêm depois de `--` e são lidos com `OS.get_cmdline_user_args()` [confirmar na versão].

## Formato do arquivo `--drive`

```text
# quadro:ação
0:press right
30:press jump
31:release jump
60:press dash
```
