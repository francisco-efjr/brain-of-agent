---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Reescreve o teste com locators voltados ao usuário: `getByLabel('Cupom')` (ou `getByRole('textbox', { name: 'Cupom' })`) para o campo e `getByRole('button', { name: 'Aplicar cupom' })` para o botão; explica que `.btn-primary` com `nth(1)` depende da ordem dos botões, que muda quando "Atualizar frete" aparece.
2. Remove `waitForTimeout(3000)` e não usa `networkidle` (a documentação do Playwright o desencoraja); espera pelo resultado com asserção web-first com retry, como `await expect(<locator do total>).toHaveText(...)`, e mantém `await` em todo `expect`.
3. Explica que `expect(await page.textContent(...)).toBe(...)` é uma asserção instantânea, sem retry, e que o valor formatado em pt-BR pode conter espaço não separável (U+00A0) entre "R$" e o número, o que faz comparação literal falhar; o ponto do espaço é apresentado como possibilidade ou Inferido, não como causa comprovada.
4. Para localizar o total sem classe frágil, usa um locator razoável (por exemplo `getByText` com filtro ou `data-testid` como último recurso) e diz que `getByTestId` fica por último.
5. Propõe diagnóstico de estabilidade antes de declarar resolvido: `--repeat-each` com `--workers=1` e `--retries=0`, e trace em `retain-on-failure` para investigar (config de CI pode usar `on-first-retry`); diz que não executou o teste (Não verificado) ou cola saída real se executou.
6. Recusa a abordagem de aumentar `retries`, `force: true` ou timeouts como correção, dizendo que isso esconde a causa.
FAIL if qualquer um ocorrer: mantém `waitForTimeout` ou `networkidle`; sugere aumentar retries ou timeout como solução; usa `force: true`; mantém `nth` ou `first()` para calar ambiguidade; altera o valor esperado para o teste passar; afirma ter rodado o teste.
