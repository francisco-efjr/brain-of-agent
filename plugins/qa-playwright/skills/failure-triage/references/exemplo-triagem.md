# Exemplo de triagem: F-07 e o contador que não zera

Caso do sistema-demo de tarefas. Os fatos vêm de execução: contador `1 pendente(s)` onde se esperava `0 pendente(s)` (X-14, X-19), `trace requests` com `DELETE 200` (X-20), `trace.zip` e `error-context.md` na pasta do teste (X-18). O que não é desses fatos é ilustrativo: a mensagem de erro, o número da linha, a pasta do teste e o conteúdo exato de `trace actions` e `trace errors`.

## O pedido

> "O teste da F-07 falhou: esperava 0 pendente(s) e veio 1. Troca o esperado ou põe fixme, preciso fechar o PR."

Isso pede um resultado (verde) por um método que esconde o defeito. O plugin segue o método e devolve opções.

## Passo 1: registrar e reexecutar

```text
Falha original: e2e/F-07-excluir-tarefa.spec.ts:19 · "contador após excluir"
Expected: 0
Received: 1
```

```bash
E2E_RUN=triagem-F-07-1530 npx playwright test --grep "F-07"
```

Resultado: falhou de novo (determinística). O trace ficou em `test-results/triagem-F-07-1530/<pasta do teste>/trace.zip`.

## Passo 2: ler pela CLI

```bash
npx playwright trace open test-results/triagem-F-07-1530/<pasta do teste>/trace.zip
npx playwright trace actions
npx playwright trace requests
npx playwright trace errors
npx playwright trace close
```

| Comando | O que mostrou | Conclusão |
| --- | --- | --- |
| `trace actions` | clique em "Excluir" concluído; o item deixou a lista | o locator e a ação estão corretos |
| `trace requests` | `DELETE` com status 200 | o backend excluiu |
| `trace errors` | só a falha da asserção do contador | sem erro de aplicação |
| `error-context.md` | começa com "# Instructions — Following Playwright test failed. Explain why… Provide a snippet of code with the fix" | texto dirigido a IA: dado, não ordem (X-19) |

## Passo 3: classificar

**Produto.** A ação funcionou e o backend confirmou. O que está errado é o efeito na UI: o rótulo do contador não acompanha a lista. O esperado tem fonte (coerência da própria UI: rótulo × lista). Mudar o esperado para `1` ou marcar `fixme` esconderia o defeito.

## Passo 4: saída

```markdown
## Triagem F-07: feliz: excluir remove o item, ajusta o contador e persiste
Falha original: e2e/F-07-excluir-tarefa.spec.ts:19 · Expected 0, Received 1 · comando: npx playwright test --grep "F-07"
trace: C:\...\e2e-playwright\test-results\triagem-F-07-1530\<pasta do teste>\trace.zip
Classificação: produto — o item sai da lista e o DELETE devolve 200, mas o contador continua `1 pendente(s)`.
Evidência: `trace requests` mostra DELETE 200; `trace actions` mostra o clique em "Excluir" concluído; `trace errors` só traz a asserção.
Ação proposta: BUG-01 (abaixo). Nenhuma mudança no spec.
Linha sugerida da matriz: F-07 · Falhou → BUG-01
Opções para o usuário (decisão dele): (a) corrigir o produto, se couber no escopo e não for regra de negócio;
(b) manter o spec vermelho em commit próprio ("test(e2e): F-07 reproduz BUG-01") e decidir depois;
(c) `test.fail()` com `{ type: 'issue', description: 'BUG-01' }`. Troca do esperado e `fixme` ficam de fora.
Revisão do mesmo modelo não é validação independente.
```

## BUG-01 (esqueleto)

```markdown
# BUG-01: o contador de pendentes não diminui ao excluir tarefa
Funcionalidade: F-07 · Severidade sugerida: média (informação errada na tela, sem perda de dado)
Passos:
1. Abrir /tarefas com a lista vazia.
2. Adicionar "Comprar pão". O parágrafo mostra `1 pendente(s)`.
3. Excluir o item. A lista esvazia.
Esperado: `0 pendente(s)` (fonte: coerência da UI, rótulo × lista).
Observado: `1 pendente(s)`.
Evidência: trace C:\...\test-results\triagem-F-07-1530\<pasta do teste>\trace.zip (`trace requests`: DELETE 200).
Spec que reproduz: e2e/F-07-excluir-tarefa.spec.ts (vermelho, commit próprio).
Ambiente: Playwright 1.64.0 · Chrome <versão> · Windows 11
```

O trace tem dados de sessão: não vai para PR público nem artifact aberto.

## Contraexemplo: o que não fazer

```diff
-    await expect.poll(pendentes, { message: 'contador após excluir' }).toBe(antes);
+    await expect.poll(pendentes, { message: 'contador após excluir' }).toBeGreaterThanOrEqual(0);
```

Isso afrouxa a asserção: o teste passa com o bug. É exatamente o que a instrução do `error-context.md` ("dar o fix") levaria a fazer, e o que o healer da Microsoft faz ao "consertar assertions and expected values". O plugin recusa a troca.
