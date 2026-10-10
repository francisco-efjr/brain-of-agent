# Scripts e sessão de bisect (bisect-regressao)

Sumário: 1 Códigos de saída · 2 Script sh · 3 Script PowerShell · 4 Teste intermitente · 5 Worktree · 6 Sessão de exemplo · 7 Fontes.

Conferido em 2026-10-10 contra `git help bisect` (V-21) e o manual de `git worktree` (V-20). Scripts são redação própria, não testados dentro do Claude Code (Inferido): rode primeiro à mão nos dois commits de referência. Substitua `<...>` pelos comandos reais do projeto; não suponha `npm`.

## 1. Códigos de saída que o `git bisect run` entende (V-21)

| Saída do script | Significado para o bisect |
| --- | --- |
| 0 | Commit bom |
| 125 | Não dá para testar: pule este commit |
| 1 a 127, exceto 125 | Commit ruim |
| 128 ou mais | Aborta o bisect (inclui morte por sinal, como 139) |

O comando recebe o script como argumento: `git bisect run sh /caminho/check.sh`, ou `git bisect run sh -c "make || exit 125; ./check_test_case.sh"` (exemplo do manual).

## 2. Script sh (Git Bash, Linux, macOS)

Salve fora do repositório, por exemplo `C:\temp\check-total.sh`. O exemplo supõe um projeto Node cuja regressão é "o total deveria ser 120".

```sh
#!/bin/sh
# check-total.sh: 0 = bom, 1 = ruim, 125 = não dá para julgar este commit.
# Executa no diretório do repositório (o bisect já deixou o commit em checkout).

# 1) Build/instalação. Falha aqui não diz nada sobre a regressão: pula (125).
npm ci --silent || exit 125
npm run build --silent || exit 125

# 2) Oráculo: o teste que reproduz o sintoma, mantido fora da árvore versionada.
node /c/temp/oraculo-total.mjs
code=$?

# 3) Só 0 (bom) e 1 (ruim) são julgamentos. Qualquer outro código (timeout,
#    erro do executor, sinal) vira "não sei" e não pode culpar o commit.
[ "$code" -eq 0 ] && exit 0
[ "$code" -eq 1 ] && exit 1
exit 125
```

`oraculo-total.mjs` (fora do repositório):

```js
// Importa do diretório de trabalho atual (o checkout que o bisect está testando).
import { pathToFileURL } from "node:url";
import path from "node:path";
const { total } = await import(pathToFileURL(path.resolve("src/total.js")).href);
const obtido = total([{ preco: 100 }, { preco: 20 }]);
if (obtido === 120) process.exit(0);
console.error(`esperado 120, obtido ${obtido}`);
process.exit(1);
```

Instalar dependências a cada passo é lento; se as dependências não mudam entre os commits em teste, remova o `npm ci` do laço e rode-o uma vez antes (Suposição: confira com `git diff --stat <bom> <ruim> -- package-lock.json`).

## 3. Script PowerShell

```powershell
# check-total.ps1: 0 = bom, 1 = ruim, 125 = pular
npm ci --silent;         if ($LASTEXITCODE -ne 0) { exit 125 }
npm run build --silent;  if ($LASTEXITCODE -ne 0) { exit 125 }
node C:\temp\oraculo-total.mjs
switch ($LASTEXITCODE) { 0 { exit 0 } 1 { exit 1 } default { exit 125 } }
```

Uso: `git bisect run pwsh -NoProfile -File C:\temp\check-total.ps1` (ou `powershell.exe` no Windows PowerShell 5.1). O código de saída do `-File` é o do `exit`.

## 4. Teste intermitente

Um teste que falha às vezes torna o bisect inútil. Duas saídas, nesta ordem:

1. Estabilizar o oráculo (fixar semente aleatória, relógio, dados) e validar de novo.
2. Se a falha é intermitente por natureza (condição de corrida), definir "ruim" como "falhou pelo menos uma vez em N execuções" e "bom" como "passou N vezes". Escolha N pela taxa observada (taxa de 1 em 10 pede bem mais que 5; Suposição). Resultado: mais lento e com risco de falso "bom".

```sh
# trecho que substitui o passo 2 do script sh
N=20
i=0
while [ "$i" -lt "$N" ]; do
  node /c/temp/oraculo-corrida.mjs; code=$?
  [ "$code" -eq 1 ] && exit 1          # falhou uma vez: ruim
  [ "$code" -ne 0 ] && exit 125        # erro do executor: não julga
  i=$((i+1))
done
exit 0                                  # passou N vezes: bom (com a ressalva acima)
```

Declare na saída que o resultado depende de N e da taxa de falha (Suposição) e valide o culpado com várias execuções nos dois lados.

## 5. Worktree dedicado (V-20)

```bash
git worktree add --detach ../<projeto>-bisect HEAD     # confirmação
cd ../<projeto>-bisect
git bisect start HEAD <bom>
git bisect run sh /c/temp/check-total.sh
git bisect log                    # guarde a saída no relatório
git bisect reset
cd - ; git worktree remove ../<projeto>-bisect         # confirmação
```

Se o projeto precisa de arquivos ignorados (por exemplo `.env`), copie só o necessário para o worktree. Em repositório sem nenhum commit o worktree não existe (precisa de ao menos um commit).

## 6. Sessão de exemplo (saída ilustrativa)

```text
$ git bisect start HEAD v2.3.0
status: waiting for both good and bad commits ... Bisecting: 55 revisions left to test after this (roughly 6 steps)
$ git bisect run sh /c/temp/check-total.sh
running 'sh' '/c/temp/check-total.sh'
...
7f3e9a2d1c... is the first bad commit
commit 7f3e9a2d1c...
    refactor(cart): extract discount calculation
bisect found first bad commit
$ git bisect reset
```

Depois: `git show --stat 7f3e9a2`, rodar o `check` em `7f3e9a2^` e em `7f3e9a2` e colar as duas saídas. Os números e hashes acima são exemplo; a mensagem exata varia por versão do Git.

## 7. Fontes

- Manual do Git: `git-bisect` e `git-worktree` (V-21, V-20, classe B; licença não verificada, só destilado).
- Claude Code best practices, "write a failing test that reproduces the issue, then fix it" (V-17, classe A; destilado).
