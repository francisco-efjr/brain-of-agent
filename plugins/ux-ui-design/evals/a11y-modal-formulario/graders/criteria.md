---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Cita critérios WCAG 2.2 pertinentes ao que o código mostra, sem exigir lista exata: ao menos quatro entre 2.1.1 (teclado, `div` com `onclick`), 4.1.2 (nome, papel e valor do "botão" e do "fechar"), 3.3.2 ou 1.3.1 (placeholder como único rótulo), 1.4.1 (erro só em vermelho), 2.4.3 e 2.4.7 (ordem e visibilidade do foco, `outline: none`), 3.3.1 ou 3.3.3 (identificação e sugestão de erro).
2. Recomenda HTML nativo antes de ARIA: `<button>` no lugar de `div` clicável, `<dialog>` aberto com `showModal()` (ou padrão de diálogo modal do ARIA APG com nome, `aria-modal` e foco), `<label>` associado aos campos, erro ligado ao campo (`aria-describedby`, `aria-invalid`) e texto do erro que não dependa só de cor; devolve o foco ao elemento que abriu o modal ao fechar, trata Escape e foco inicial.
3. Explica a causa do relato (foco some ao fechar porque o foco não é devolvido ao gatilho e o elemento oculto perdeu o foco) em termos coerentes com o código.
4. Não declara conformidade legal: diz que corrigir os itens não garante conformidade com a lei europeia de acessibilidade (EAA) nem com outra norma, que isso depende de revisão por jurisdição e de teste completo, e que o alvo técnico é WCAG 2.2 AA.
5. Lembra que ferramenta automática (axe, Lighthouse) cobre só parte e que teclado e leitor de tela precisam de teste manual; inclui uma lista do que não foi testado, rotulando o que veio da leitura do código como Inferido.
6. Se informa contraste, o cálculo é coerente (branco sobre #2d6a4f passa AA); não afirma que o formulário "está acessível".
FAIL if qualquer um ocorrer: cita 4.1.1 (Parsing) como critério vigente da WCAG 2.2; recomenda ARIA (`role="button"`, `tabindex`) antes de elementos nativos como solução principal; afirma conformidade com a lei, com a EAA ou com "WCAG AA completo"; ignora o teclado; inventa que testou com leitor de tela.
