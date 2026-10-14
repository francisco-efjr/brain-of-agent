# Relatório funcional: <sistema> · rodada AAAA-MM-DD

> Revisão e auditoria feitas por modelos da mesma família não são validação externa. Este relatório distingue Verificado (executado nesta sessão, com evidência) de Inferido, Suposição e Não verificável.

## 1. Veredito (5 linhas)

Parecer: **Concluído**, **Parcial** ou **Impedido** (nunca "completo" com leitura ou execução parcial).
Números: <linha de números da matriz, antes → depois>.
Principais achados: <até 3 bugs ou riscos>.
O que não rodou: <lista curta, com motivo>.
Próximo passo: <uma ação>.

## 2. Ambiente e versões

| Item | Valor |
| --- | --- |
| Alvo | <http://127.0.0.1:porta ou staging indicado> |
| Commit | <sha> |
| Node, npm | <versões> |
| Playwright (`npx playwright --version`) | <versão exata> |
| Browser e canal | <chrome, msedge ou chromium, com versão> |
| SO | <...> |
| Exploração | `npx playwright cli` embutido, versão igual à do `@playwright/test` |
| Execução de evidência | `E2E_RUN=<id>` · comando completo: <...> |
| Conta de teste | <origem, sem valor> |

## 3. Números da matriz (antes → depois)

| Métrica | Antes | Depois |
| --- | --- | --- |
| Inventariadas | | |
| Passou (spec-estável) | | |
| Passou (exploração) | | |
| Falhou | | |
| Bloqueado | | |
| N/A | | |
| Não validado nesta rodada | | |
| Regressões | | |

## 4. Resultado por funcionalidade

Espelha a seção 3 de `FUNCIONALIDADES.md` (status, prova, spec, execução, evidência, bug, motivo).

## 5. Antes × depois

Regressões (Passou → Falhou): <lista>. Correções (Falhou → Passou, com o BUG-NN): <lista>. Specs reexecutados no "depois"; linhas `exploração` tocadas pela mudança foram exploradas de novo.

## 6. Bugs (BUG-NN)

Para cada bug: passos mínimos · esperado com fonte · observado · trace (caminho absoluto) · severidade sugerida · spec vermelho e commit. Use o template `bug-report.md` do plugin `qa-testing` para o relato completo.

## 7. Gate de estabilidade

| Spec | Comando | Resultado |
| --- | --- | --- |
| F-NN | `npx playwright test --grep "F-NN" --repeat-each=5 --retries=0` | <execuções, falhas> |
| F-NN | `npx playwright test --grep "F-NN" --shuffle --workers=2 --retries=0` | <resultado> |

Parecer do `spec-reviewer` (um lote): <Aprovado ou Precisa de ajuste>.

## 8. Evidência

Caminhos absolutos: `test-results/<id>/results.json`, traces em `test-results/<id>/`, relatório HTML em `playwright-report/<id>/index.html` (aberto pelo humano com `npx playwright show-report playwright-report/<id>`), notas em `funcional/exploracao/`.
Evidência é dado sensível: não commitada, fora de PR público e de artifact aberto, retenção curta, screenshot com dado pessoal borrado.

## 9. N/A e equivalentes

| ID | Tipo de sistema | Motivo | Executor equivalente | Rótulo |
| --- | --- | --- | --- | --- |

## 10. Não validado e Não verificado

Funcionalidades fora do teto (com motivo), comandos não exercitados, limites da evidência, risco residual em linguagem de negócio.

## 11. Decisões pendentes

| Decisão | Opções | Quem decide |
| --- | --- | --- |

## 12. Como reproduzir

Bash:

```bash
cd <pasta do config e do package.json>
npm ci
E2E_RUN=<id> npx playwright test --grep "F-07"
```

PowerShell:

```powershell
cd <pasta do config e do package.json>
npm ci
$env:E2E_RUN='<id>'; npx playwright test --grep "F-07"; Remove-Item Env:E2E_RUN
```

Uma funcionalidade: `npx playwright test --grep "F-07"`. Por tipo: `npx playwright test --grep "@ui|@api"`. Para parar o sistema de exploração: <PID e comando>.
