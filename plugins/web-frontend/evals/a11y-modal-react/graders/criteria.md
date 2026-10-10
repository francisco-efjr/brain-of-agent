---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Apresenta achados com localização (arquivo e linha ou trecho do código), severidade e critério WCAG 2.2 por número, e cobre pelo menos estes pontos: (a) `div` com `onClick` usado como botão de fechar e de confirmar, sem papel, sem foco por teclado e sem tratamento de Enter ou Espaço (2.1.1, 4.1.2); (b) o diálogo não tem papel nem nome (`role="dialog"` ou `<dialog>`, `aria-modal`, `aria-labelledby`); (c) a gestão de foco: foco não entra no diálogo, não fica contido, Esc não fecha, foco não volta ao gatilho; (d) `outline: none` remove o foco visível sem substituto (2.4.7); (e) o campo de confirmação só tem placeholder, sem rótulo (3.3.2 ou 1.3.1).
2. Recomenda HTML nativo antes de ARIA: `<dialog>` aberto com `showModal()` (ou gestão de foco equivalente explicada) e `<button type="button">` reais; o botão de fechar recebe nome acessível (por exemplo `aria-label`) porque "×" não descreve a ação.
3. Pode mencionar, sem ser exigido, contraste do texto `#777` sobre `#c0392b` abaixo de 4,5:1 e alvo de 16 px abaixo do mínimo de 24 px (2.5.8); se mencionar, os números ou critérios estão corretos.
4. Separa o que foi lido no código do que não foi testado: inclui uma lista "não testado" ou Não verificável (leitor de tela, navegador) e trata o que um leitor de tela anunciaria como Inferido.
5. Mantém o modo de diagnóstico pedido: correção mínima por achado, sem reescrever o componente inteiro e sem afirmar que editou arquivos.
FAIL if qualquer um ocorrer: sugere apenas `role="button"` no `div` sem tabindex e teclado; afirma ter testado com NVDA, VoiceOver, axe ou navegador; inventa um critério WCAG que não existe; recomenda `tabindex` positivo; ignora toda a gestão de foco do diálogo; aplica a correção em arquivos apesar de o usuário pedir só diagnóstico.
