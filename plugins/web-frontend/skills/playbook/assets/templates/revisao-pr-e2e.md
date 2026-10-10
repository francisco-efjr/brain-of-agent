# Revisão de PR de teste E2E

Checklist para revisar um PR que adiciona ou altera testes de navegador. Origem: checklist de revisão de PR de `automacao-web.md` do brain-of-agent (MIT), adaptado e alinhado a V-20, V-21 e V-41. Ordem de prioridade dos achados: falso verde, intermitência, lacuna de risco, lentidão, manutenção, estilo. PR: [link ou título]. Revisor: [nome]. Data: [AAAA-MM-DD].

## Itens (marque, e cite `arquivo:linha` em cada falha)

- [ ] 1. Cada teste verifica o efeito de negócio (valor, status, dado persistido), não só que "algo apareceu"; o esperado é calculado de forma independente, não copiado da tela.
- [ ] 2. Todo `expect` tem `await`; nenhuma asserção instantânea (`expect(await el.textContent())`) sobre algo que muda.
- [ ] 3. Asserção negativa só depois de um sinal positivo de conclusão.
- [ ] 4. Nenhum `waitForTimeout`, `sleep`, `cy.wait(número)`, `networkidle` nem `force: true`.
- [ ] 5. Locators por papel, rótulo ou test-id; sem `nth`, XPath absoluto, classe gerada, e nenhum `.first()` para calar ambiguidade.
- [ ] 6. Dados criados por teste, únicos e limpos; nada depende de ordem nem de massa que outro teste altera; roda com `fullyParallel`.
- [ ] 7. Rodou com `--repeat-each` antes do merge (resultado anexado).
- [ ] 8. Mock coerente com o contrato real; pelo menos um fluxo crítico mantém a versão sem mock.
- [ ] 9. Sem segredo no código; pasta de estado de login no `.gitignore`.
- [ ] 10. Nenhum `test.only` (use `forbidOnly`); `skip` e `fixme` só com issue; sem aumento de retries ou timeout sem justificativa.
- [ ] 11. Page object com métodos de intenção e sem asserção escondida.
- [ ] 12. Snapshot visual atualizado com o diff revisado (esperado, real, diff), não com `--update-snapshots` às cegas.
- [ ] 13. O nome descreve a regra e o nível está certo: isso caberia em teste de componente, de API ou unitário?

## Se o teste foi gerado por codegen ou por agente

Código cru de codegen é roteiro linear, sem fixture nem dado via API, com asserções rasas e às vezes `nth()`. Agentes que "consertam" teste podem adaptá-lo a uma regressão real: revise como PR de pessoa e confirme que a falha original era do teste, não do app.

## Achados

| ID | Severidade | Arquivo:linha | Problema | Correção |
| --- | --- | --- | --- | --- |
| E2E-01 | [Alto / Médio / Baixo] | [caminho:linha] | [descrição] | [ação] |

## Veredito

[aprovar / aprovar com ressalvas / pedir mudanças]. Revisor é o mesmo modelo que escreveu os testes? [sim/não; se sim, não é validação independente].
