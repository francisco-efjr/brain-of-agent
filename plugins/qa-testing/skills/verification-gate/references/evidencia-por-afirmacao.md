# Evidência por afirmação

Apoio da skill `verification-gate`. Leia quando precisar decidir qual comando prova qual frase, como ler a saída sem cair em falso verde ou como provar uma regressão sem destruir o trabalho em andamento.

## Sumário

- [Tabela afirmação -> prova mínima](#tabela-afirmação---prova-mínima)
- [Comandos por stack](#comandos-por-stack)
- [Leitura de saída: falsos verdes comuns](#leitura-de-saída-falsos-verdes-comuns)
- [Provar a regressão sem destruir o trabalho](#provar-a-regressão-sem-destruir-o-trabalho)
- [Saída de teste desenhada para agente](#saída-de-teste-desenhada-para-agente)
- [Quando não dá para executar](#quando-não-dá-para-executar)

## Tabela afirmação -> prova mínima

Base: V-01, V-28, V-32 (Verificado nas fontes); as linhas de migração, performance e segurança são Inferido (conhecimento estável do domínio).

| Afirmação | Prova mínima | O que não conta |
| --- | --- | --- |
| "Os testes passam" | comando de teste completo do escopo, contagem executada > 0, exit 0 | resultado de outro commit; execução com filtro que exclui o teste novo |
| "Bug corrigido" | sintoma original reproduzido antes; teste de regressão vermelho sem a correção e verde com ela | "o teste antigo passa" (ele já passava com o bug) |
| "Build/lint/tipos ok" | comando de build, lint e type-check, cada um com exit 0 | build de outro pacote do monorepo |
| "Requisito com várias partes cumprido" | uma linha de evidência por parte | uma linha geral "tudo ok" |
| "Refatoração sem mudar comportamento" | mesma suíte, mesmos números antes e depois (executados, passados, pulados) e diff sem alteração de asserção | suíte verde depois, sem número de antes |
| "Funciona na tela" | E2E ou navegador controlado com captura do estado final; sem navegador, declarar não verificado | print de um estado intermediário |
| "API responde certo" | `curl`/cliente com status, corpo e cabeçalhos relevantes contra ambiente de teste | só o status 200 |
| "Migração segura" | migração aplicada em cópia com volume realista; contagem antes/depois; rollback ensaiado | rodar em banco vazio |
| "Mais rápido" | mesma medição, mesmo ambiente, várias execuções, antes e depois | uma execução isolada |
| "Vulnerabilidade corrigida" | caso de ataque que antes passava agora recusado, mais teste de regressão | "usei biblioteca segura" |
| "Subagente terminou" | `git diff` lido e comandos reexecutados por você | o resumo do subagente |
| "CI está verde" | link ou saída do pipeline do commit exato, com os jobs relevantes | pipeline de um commit anterior |

## Comandos por stack

Exemplos de forma, não prescrição: use o comando que o projeto já define (CLAUDE.md, `package.json`, `Makefile`). Confirme flags com `--help` na versão instalada (Inferido, conhecimento estável).

| Stack | Escopo alterado | Um teste só | Suíte inteira |
| --- | --- | --- | --- |
| Python (pytest) | `pytest tests/test_pedido.py` | `pytest tests/test_pedido.py::test_cupom -x` | `pytest` |
| JS/TS (Vitest) | `npx vitest run src/cart` | `npx vitest run -t "cupom com frete grátis"` | `npx vitest run` |
| JS/TS (Jest) | `npx jest src/cart` | `npx jest -t "cupom com frete grátis"` | `npx jest` |
| Go | `go test ./cart/... -count=1` | `go test ./cart -run TestCupom -count=1` | `go test ./... -count=1` |
| Java (Maven) | `mvn -Dtest=CartTest test` | `mvn -Dtest=CartTest#cupom test` | `mvn test` |
| .NET | `dotnet test --filter FullyQualifiedName~Cart` | idem, filtro mais específico | `dotnet test` |
| Rust | `cargo test cart` | `cargo test cart::tests::cupom` | `cargo test` |
| Playwright | `npx playwright test tests/checkout.spec.ts` | `npx playwright test -g "cupom"` | `npx playwright test` |

Código de saída: Bash `echo $?` logo após o comando; PowerShell `$LASTEXITCODE`. Em pipeline (`cmd | tee log`), o exit do `tee` mascara o do `cmd`: use `set -o pipefail` no Bash ou rode sem pipe e grave com `> log 2>&1`.

## Leitura de saída: falsos verdes comuns

| Sinal | Leitura | Ação |
| --- | --- | --- |
| pytest `no tests ran`, exit 5 | nenhum teste coletado (padrão de nome, caminho errado) | corrigir caminho ou `-k`; não relatar como sucesso |
| Go `[no test files]` ou `ok ... (cached)` | pacote sem teste, ou resultado reaproveitado | reexecutar com `-count=1`; conferir o pacote certo |
| Jest/Vitest "No tests found" | filtro ou configuração errada | conferir `testMatch`/`include` |
| `skipped`, `xfail`, `todo`, `.only` | parte da suíte não rodou, ou só um teste rodou | listar os pulados; `.only` em commit é bloqueio |
| `cache hit`/replay (Nx, Turborepo), Gradle `UP-TO-DATE` | tarefa não executou de novo | usar a flag de bypass do orquestrador |
| Exit 0 com `Error` no log | o comando engoliu o erro (script que termina com `true`, `set +e`) | ler o script; testar o código de saída do runner direto |
| Teste verde que não tem asserção | passa sem verificar nada | chamar `test-reviewer`; ver `tdd-guard` (mutation check) |
| Retry verde (`flaky`, `passed on retry`) | primeira execução falhou | tratar como falha a investigar (`flaky-triage`) |
| Mesmo número de testes antes e depois da mudança | teste novo não foi coletado | conferir se o arquivo novo entrou na contagem |

## Provar a regressão sem destruir o trabalho

Objetivo: mostrar o teste novo vermelho contra o código sem a correção e verde com ela, sem perder alterações não commitadas.

Receita preferida (worktree; não toca o diretório de trabalho):

```bash
BASE=$(git merge-base HEAD origin/main)       # ou o commit pai do conserto
git worktree add "$TMPDIR/base-check" "$BASE"  # TMPDIR: pasta temporária da sessão
cp tests/test_pedido.py "$TMPDIR/base-check/tests/test_pedido.py"   # só o teste novo
(cd "$TMPDIR/base-check" && pytest tests/test_pedido.py::test_cupom_com_frete_gratis; echo "exit=$?")
git worktree remove --force "$TMPDIR/base-check"
```

Esperado: `exit=1` com a falha pelo motivo certo (valor errado, não ImportError). Depois rode o mesmo teste no diretório principal e cole o verde. Se o repositório não tem remoto, troque `origin/main` por um commit ou tag que você tenha conferido com `git log --oneline`.

Alternativas, em ordem de risco crescente:

1. Copiar o repositório inteiro para a pasta temporária (`cp -r`) e reverter ali.
2. `git stash push -- <arquivos de produção da correção>`, rodar o teste, `git stash pop`. Peça confirmação antes: a pilha de stash é fácil de perder.
3. `git reset --hard` ou `git checkout -- <arquivo>` em árvore com trabalho não commitado: só com pedido explícito do usuário.

Se o teste novo exige código de produção que só existe na correção (nova função), a prova de vermelho é o teste falhando por "função ausente" no worktree, aceitável desde que o motivo seja a ausência do comportamento, não do import do módulo de teste.

## Saída de teste desenhada para agente

Quando o projeto controla o script de teste (V-07, Verificado): console com poucas linhas; `ERROR <arquivo>:<teste> - <motivo curto>` numa linha só, para `grep`; sumário final de 3 linhas (total, falhas, caminho do log); log completo em arquivo; estatísticas pré-calculadas; progresso impresso raramente. Para suítes enormes, uma opção `--fast` que roda uma amostra determinística (por exemplo 1% ou 10%) acelera o ciclo, com a suíte inteira reservada ao gate final. O verificador de testes precisa ser quase perfeito: um verificador frouxo faz o agente resolver o problema errado.

Exemplo de sumário aceitável:

```text
ERROR tests/test_pedido.py::test_cupom_com_frete_gratis - esperado 225.00, obtido 250.00
SUMMARY total=212 failed=1 skipped=0
LOG logs/pytest-2026-10-10T1432.log
```

## Quando não dá para executar

Situações: sem ferramenta de shell, ambiente sem dependências, teste que exige serviço externo, tempo de suíte proibitivo.

1. Diga qual comando provaria a afirmação e por que não rodou.
2. Entregue o que é Inferido (análise do código) rotulado como tal.
3. Peça ao usuário para executar e colar a saída, ou proponha a menor verificação alternativa (um teste isolado, `curl` contra staging).
4. Nunca preencha o resultado esperado em uma tabela de evidência como se fosse o obtido.
