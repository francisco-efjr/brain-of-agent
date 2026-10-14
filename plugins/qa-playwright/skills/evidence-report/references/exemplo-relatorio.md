# Exemplo de relatório da rodada: sistema-demo de tarefas

**Exemplo ilustrativo.** Os números, datas, ids de execução e caminhos são fictícios e servem só para mostrar o formato. Vêm de execução real apenas: as versões (Node v24.15.0, Playwright 1.64.0: X-01) e o defeito do contador (X-14, X-19, X-20). Não cite estes números como resultado de teste.

````markdown
# RELATORIO-FUNCIONAL: sistema-demo de tarefas · rodada 2026-10-13
Revisão e auditoria feitas pelo mesmo modelo que escreveu os specs: não são validação independente.

## 1. Veredito
Parcial. 3 de 6 funcionalidades do escopo passaram (2 com spec estável, 1 só por exploração); 1 falhou por bug de produto (BUG-01);
1 ficou Bloqueada por falta de conta de teste; 1 é N/A (UI nativa Android, executor equivalente indicado).
Nada foi executado contra produção.

## 2. Ambiente e versões
Node v24.15.0 · npm 11.12.1 · Playwright 1.64.0 (exata, sem ^) · Chrome <versão> · Windows 11
Exploração: `npx playwright cli` embutido · Instância de exploração: 127.0.0.1:4173 · Teste: 127.0.0.1:4174 (webServer)
Banco: compartilhado entre as instâncias; specs afirmam delta e usam dado único.

## 3. Números da matriz (antes → depois)
Inventariadas 6 · Passou 3 (spec estável 2, exploração 1) · Falhou 1 · Bloqueado 1 · N/A 1 · Não validado 0
Antes: Passou 0 (matriz criada nesta rodada). Regressões: 0.

## 4. Resultado por funcionalidade
| ID | Status | Prova | Spec | Execução | Evidência | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| F-01 | Passou | spec-estável | e2e/F-01-login-invalido.spec.ts | E2E_RUN=20261013T1530-evidencia, 2026-10-13 | C:\...\test-results\20261013T1530-evidencia\results.json | |
| F-06 | Passou | spec-estável | e2e/F-06-adicionar-tarefa.spec.ts | idem | idem | |
| F-07 | Falhou | spec (vermelho) | e2e/F-07-excluir-tarefa.spec.ts | idem | C:\...\test-results\20261013T1530-evidencia\<pasta do teste>\trace.zip | BUG-01 |
| F-08 | Passou | exploração | (sem spec) | exploração 2026-10-13 | C:\...\funcional\exploracao\F-08.md | |
| F-10 | Bloqueado | | | | | Sem conta de teste (seed, variável ou cadastro local): decisão pendente |
| F-15 | N/A | | | | | UI nativa Android: Compose UI test ou Espresso |

## 5. Antes × depois
Sem rodada anterior: sem regressão nem correção a registrar.

## 6. Bugs
BUG-01 · F-07 · contador de pendentes não diminui ao excluir · esperado `0 pendente(s)` (fonte: coerência da UI), observado `1 pendente(s)` ·
trace: C:\...\test-results\20261013T1530-evidencia\<pasta do teste>\trace.zip (`trace requests`: DELETE 200) ·
spec vermelho em commit próprio · severidade sugerida: média · decisão pendente: corrigir, ou `test.fail()` com `{ type: 'issue', description: 'BUG-01' }`.

## 7. Gate de estabilidade
| Spec | --repeat-each=5 --retries=0 | --shuffle --workers=2 --retries=0 | Revisão |
| --- | --- | --- | --- |
| F-01 | 5/5 passaram | passou | Aprovado (spec-reviewer) |
| F-06 | 5/5 passaram | passou | Aprovado (spec-reviewer) |
| F-07 | falha 5/5 (determinística: bug) | falhou | Aprovado (reproduz BUG-01) |

## 8. Evidência
Caminhos absolutos em `C:\...\e2e-playwright\`: `test-results\20261013T1530-evidencia\`, `playwright-report\20261013T1530-evidencia\index.html`, `funcional\exploracao\`.
Dado sensível: não commitada, não anexar a PR público ou artifact aberto. `playwright/.auth/` não foi lido.

## 9. N/A e equivalentes
F-15 · UI nativa Android: não aplicável ao Playwright (a documentação cobre web, Electron e Chrome/WebView Android, de forma experimental).
Executor equivalente: Compose UI test ou Espresso; exploração por `adb` no emulador existente (Inferido). A matriz é a mesma; só o executor muda.

## 10. Não validado e não verificado
Não validado nesta rodada: nenhuma funcionalidade do escopo.
Não verificado: teclado e leitor de tela; comportamento com mais de um item na lista; CI.
Risco residual: banco compartilhado entre exploração e teste.

## 11. Decisões pendentes
1. BUG-01: corrigir agora, ou `test.fail()` anotado? 2. F-10: fornecer conta de teste (variável de ambiente, fora do chat).

## 12. Como reproduzir
bash:
  E2E_RUN=reproducao npx playwright test --grep "F-07"
PowerShell:
  $env:E2E_RUN='reproducao'; npx playwright test --grep "F-07"; Remove-Item Env:E2E_RUN
Relatório HTML (pelo humano): npx playwright show-report playwright-report/20261013T1530-evidencia
Parar a instância de exploração: <PID e comando>
````

Linha de números para a mensagem final (mesmo exemplo):

```text
Funcionalidades: 6 inventariadas · Passou 3 (2 spec estável, 1 só exploração) · Falhou 1 (bug BUG-01) · Bloqueado 1 · N/A 1 · Não validado 0 · regressões 0
Matriz: C:\...\docs\testes\2026-10-13\funcional\FUNCIONALIDADES.md
```

## O que o exemplo mostra

- `Passou` aparece com a prova separada: spec estável e exploração têm totais distintos.
- O bug mantém o spec vermelho e não conta como regressão.
- Bloqueado e N/A têm motivo, e N/A tem executor equivalente.
- As seções 7 e 8 apontam para execuções com `E2E_RUN`, que não são apagadas pela execução seguinte.
- O relatório diz o que não foi verificado e que a revisão do mesmo modelo não é independente.
