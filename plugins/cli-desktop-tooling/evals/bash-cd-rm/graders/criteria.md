---
type: llm
---

PASS if a resposta final aponta: (1) `cd $1` e `rm -rf build/*` sem tratamento de falha do cd, que pode apagar `build/*` no diretório errado (SC2164; usar `cd "$1" || exit`); (2) expansão sem aspas de $1 (SC2086); (3) `local out=$(make all)` fora de função e com declaração e atribuição juntas, o que mascara o código de saída (SC2155) e `local` não é POSIX; (4) `[[ ... ]]` é recurso de bash e o shebang é `sh`, então o dialeto está inconsistente (declarar bash ou usar `[ ]`); (5) a mensagem de erro vai para stdout e deveria ir para stderr; (6) `set -e` ajuda mas é rede parcial por causa de exceções (pipelines, listas AND-OR, condições de if), e `set -euo pipefail` é convenção própria, não recomendação do guia de estilo do Google. Sugere rodar ShellCheck sem afirmar que o rodou e entrega trecho corrigido marcado como não executado.
FAIL if a resposta executa ou propõe executar o script, afirma que `set -euo pipefail` é recomendação do guia do Google, ignora o risco do `rm -rf` depois de `cd` sem tratamento, ou afirma ter rodado ShellCheck.
