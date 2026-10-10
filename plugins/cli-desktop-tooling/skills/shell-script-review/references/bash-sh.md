# bash e sh: checklist SHL, antes/depois e portabilidade

Verificado em 2026-10-10 contra V-61 (wiki do ShellCheck: SC2086, SC2155, SC2164), V-62 (Google Shell Style Guide, repositório sob CC BY 3.0; aqui só destilado) e V-63 (POSIX.1-2017, lido até 160.000 de 189.000 caracteres). Ambiente do usuário: Git Bash no Windows (bash, não `sh` puro). Itens Inferido são conhecimento estável. Trechos ilustrativos, **não executados**.

Sumário: [Checklist](#checklist-shl) · [Antes/depois](#antesdepois) · [`set -e`](#set--e-o-que-as-fontes-dizem) · [POSIX sh](#portabilidade-para-sh-puro-v-63) · [Windows](#git-bash-no-windows-inferido) · [Comandos](#comandos-para-o-usuário-executar)

## Checklist SHL

IDs SHL-01 a SHL-10 e severidades padrão: os do `checklist-completo.md` do playbook. SHL-11 a SHL-13 são extensões desta skill (Inferido quanto à numeração e à severidade).

| ID | Sev. | Verificar | Detectar | Fonte |
| --- | --- | --- | --- | --- |
| SHL-01 | Média | Dialeto declarado no shebang (`bash` ou `sh`) para o ShellCheck e para quem executa | primeira linha ausente, ou `#!/bin/sh` com recursos de bash | V-61, V-62, V-63 |
| SHL-02 | Alta | SC2086: expansão sem aspas sofre divisão de palavras e globbing (`"$1"`, `"$@"`). SC2164: `cd dir` sem tratamento de falha continua no diretório errado (crítica antes de `rm`) | `$var` fora de aspas em argumentos; `cd` sem tratamento de falha depois dele (`exit` ou, em função, `return`) | V-61 |
| SHL-03 | Média | SC2155: `local`, `export` ou `readonly` com substituição de comando na mesma linha mascara o código de saída | `local x=$(...)` | V-61 |
| SHL-04 | Média | `"$@"` no lugar de `$*` | `$*` | V-62 |
| SHL-05 | Média | Em `sh` puro, nada de `[[`, arrays, `local` ou `function` | recursos de bash em `#!/bin/sh` | V-63 |
| SHL-06 | Baixa | Erros em STDERR por função `err()` | `echo "erro"` sem `>&2` | V-62 |
| SHL-07 | Média | `set -euo pipefail` é decisão própria, com as exceções conhecidas; não é regra do Google; prefira checagem explícita e ShellCheck | `set -e` apresentado como garantia | V-62, V-63 |
| SHL-08 | Baixa | Script com mais de 100 linhas ou fluxo não trivial: considere linguagem mais estruturada | contagem de linhas | V-62 |
| SHL-09 | Baixa | ShellCheck no CI com SC2086, SC2155 e SC2164 como erro; supressões com comentário de justificativa | ausência de etapa | V-61 |
| SHL-10 | Baixa | `(( i++ ))` solto pode encerrar o script com `set -e` quando a expressão vale zero | `(( ... ))` como comando isolado | V-62 |
| SHL-11 | Média | `local` para variáveis de função (extensão) | variáveis de função sem `local` | V-62 |
| SHL-12 | Baixa | Nomes de função e variável em minúsculas com sublinhado; constantes e variáveis de ambiente em maiúsculas (extensão) | convenções | V-62 |
| SHL-13 | Crítica | `rm -rf "$dir/"*` ou similar com variável possivelmente vazia (extensão; relacionado a SC2164) | `rm -rf` com variável | Inferido |

Notas: SC2046, SC2034, SC1008 e SC3001 a SC3067 vêm do índice lido pelo pesquisador e não foram reconferidos (V-61). Exceções de SC2086 conforme a página: arrays no bash/ksh/zsh para divisão intencional, `set -f` ou `IFS=''`, e `${debug:+"-x"}` para argumento opcional. Supressões só com justificativa.

## Antes/depois

Antes (SHL-02, 03, 13):

```bash
#!/bin/sh
deploy() {
  cd $1
  local out=$(make build)
  rm -rf $1/dist/*
  echo "erro: build falhou"
}
```

Depois (modelo; não executado):

```bash
#!/usr/bin/env bash
set -euo pipefail   # decisão própria do projeto; ver a seção sobre set -e

err() { printf '%s\n' "$*" >&2; }

deploy() {
  local dir=${1:-}
  local out

  [[ -n "$dir" ]] || { err "uso: deploy <diretorio>"; return 2; }
  cd "$dir" || return 1
  out=$(make build) || { err "erro: build falhou"; return 1; }
  rm -rf "${dir:?}/dist/"*
  printf '%s\n' "$out"
}
```

Por quê: aspas evitam divisão de palavras e globbing (SC2086); declarar `out` e atribuir em linhas separadas preserva o código de saída de `make` (SC2155); `cd ... || return` evita seguir no diretório errado (SC2164); `${dir:?}` aborta se `dir` estiver vazio, para o `rm` nunca expandir para a raiz; o erro vai para STDERR (V-61, V-62). O shebang passou a `bash` porque o trecho usa `[[`.

## `set -e`: o que as fontes dizem

- O guia do Google **não** recomenda `set -e` nem `pipefail`; usa `PIPESTATUS` para checar pipes (V-62). Portanto `set -euo pipefail` é convenção **própria** do projeto, não "do Google".
- POSIX (V-63): com `set -e`, a falha de comando individual dentro de pipeline de vários comandos não faz o shell sair (só a do pipeline inteiro conta); a lista composta depois de `while`, `until`, `if`, `elif`, pipeline iniciado por `!` e qualquer comando de lista AND-OR que não seja o último são ignorados.
- Conclusão prática: trate `set -e` como rede parcial, não como garantia. Checagens explícitas (`|| return`, `|| exit`) nos pontos críticos e ShellCheck cobrem o que ele deixa passar. `pipefail` é recurso do bash (não está na lista POSIX lida): não o use em `sh` puro.

## Portabilidade para sh puro (V-63)

Se o script deve rodar em `sh` puro: sem `[[`, arrays, `local` nem `function`; declare o dialeto no shebang. Palavras reservadas da gramática lidas: `if`, `then`, `else`, `elif`, `fi`, `do`, `done`, `case`, `esac`, `while`, `until`, `for`, `{`, `}`, `!`, `in`. `local` só aparece em uma tabela de utilitários de comportamento não especificado. Não reconfirmados (V-63): "`#!`: resultado não especificado" e "`[[`, `function` e `select` possivelmente reservadas".

## Git Bash no Windows (Inferido)

- É bash (MSYS), não `sh` puro; scripts devem declarar `bash` no shebang.
- Terminações de linha CRLF quebram o shebang (`bad interpreter`) e comparações de string: verifique `.gitattributes` e o editor.
- Caminhos: `C:\x` em um comando nativo do Windows versus `/c/x` no Git Bash; conversão automática de argumentos pode surpreender. Teste com um caminho real do usuário antes de afirmar.
- Variáveis e comandos do PowerShell não existem aqui; para comandos específicos do Windows, prefira um `.ps1` revisado pela outra metade desta skill.

## Comandos para o usuário executar

Nenhum foi rodado pela skill. ShellCheck é GPL-3.0 (ferramenta de terceiros): instalar é decisão do usuário.

```bash
shellcheck --version
shellcheck -s bash -S warning scripts/*.sh     # -s dialeto, -S severidade mínima
shellcheck -s sh scripts/portavel.sh           # confere portabilidade para sh
```

Supressão justificada:

```bash
# shellcheck disable=SC2086  # divisão intencional: $FLAGS contém várias opções simples
cmd $FLAGS
```
