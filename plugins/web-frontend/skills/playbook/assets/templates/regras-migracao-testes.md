# Regras de migração de testes de UI

Arquivo de regras para migrar uma suíte (por exemplo Cypress para Playwright) em lotes, com o agente em sessões curtas. Ideia de prática de praticante (classe C, V-40), sustentada pelas boas práticas oficiais do Playwright (V-20) e pelo guia de boas práticas do Claude Code (V-04). Documente e rode com autorização; não automatize sem revisão. Migre quando a dor (intermitência, tempo de CI, falta de multi-aba) custa mais que reescrever.

## Escopo

- Suíte de origem: [ferramenta e versão, número de specs]
- Suíte de destino: [ferramenta e versão]
- Fora do escopo: [specs que ficam, testes de API, etc.]
- Autorização: [o usuário autorizou instalar e rodar a ferramenta de destino? sim/não]

## Mapa de helpers e comandos

| Origem | Destino | Observação |
| --- | --- | --- |
| [comando ou helper antigo] | [equivalente] | [diferença de comportamento] |
| `cy.get('[data-cy=x]')` | `page.getByTestId('x')` ou, melhor, `getByRole` | locator por papel antes de test-id |
| `cy.wait(5000)` | `await expect(locator).toHaveText(...)` | sem espera fixa nem `networkidle` |

## Regras

1. **Pare no desconhecido.** Se um comando, plugin ou helper não está no mapa, pare e pergunte; não invente equivalente.
2. Migre em lotes de 5 specs; cada lote em sessão nova, partindo deste arquivo.
3. Locators por papel, rótulo e texto; test-id por último; sem `nth`, XPath absoluto nem classe gerada.
4. Asserções web-first com `await`; sem `waitForTimeout`, `networkidle` nem `force: true`.
5. Cada teste cria os dados dele; sem dependência de ordem.
6. Preserve a intenção do teste original; não enfraqueça asserção para passar.
7. Nunca atualize baseline visual para a falha sumir; classifique o diff.

## Critério de aceite por spec

- [ ] Passa 3 vezes seguidas (`--repeat-each=3`) sem retry
- [ ] Passa com `--workers` maior que 1
- [ ] **Teste de sanidade:** quebrando o app de propósito (por exemplo trocar um texto ou remover um botão), o teste falha; restaure e confirme que volta a passar
- [ ] Cobertura equivalente à do original (mesmos fluxos e asserções)
- [ ] Comparação visual com o original quando houver captura de referência

## Registro por lote

| Lote | Specs | Resultado | Pendências | Data |
| --- | --- | --- | --- | --- |
| [n] | [lista] | [passou / falhou] | | |

## Encerramento

Suíte antiga removida só depois de [N] execuções verdes no CI e aprovação do usuário. Tempo de CI antes e depois: [números, com condições].
