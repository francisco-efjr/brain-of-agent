# Exemplo de relatório de auditoria (resumido)

Caso sintético para calibrar profundidade. O trecho auditado foi inventado e é o mesmo tipo de material que um usuário cola no chat.

## Material recebido

```html
<section class="pricing">
  <h2>Escolha o plano ideal para você</h2>
  <div class="card"><span class="icon">🚀</span><h3>Básico</h3><p>Tudo que você precisa para começar.</p><a class="btn">Saiba mais</a></div>
  <div class="card"><span class="icon">⚡</span><h3>Pro</h3><p>Tudo que você precisa para crescer.</p><a class="btn">Saiba mais</a></div>
  <div class="card"><span class="icon">💎</span><h3>Equipe</h3><p>Tudo que você precisa para escalar.</p><a class="btn">Saiba mais</a></div>
  <input placeholder="Seu e-mail">
</section>
```

```css
.pricing { background: linear-gradient(135deg, #7c3aed, #4f46e5); text-align: center; }
.card { border-radius: 24px; border-left: 4px solid #a78bfa; transition: all .3s; }
.btn { outline: none; background: #a78bfa; color: #fff; }
```

## Relatório

**Escopo e limitações.** Markup e CSS colados, 14 linhas. Nada foi renderizado; todo efeito visual é Inferido. Tokens e briefing não informados; superfície presumida: Persuade (Suposição). Contraste calculado onde havia hex.

**Teste de tronco.** Não aplicável (trecho de seção, sem navegação).

| Categoria | Resultado | Itens-chave |
| --- | --- | --- |
| 1 Hierarquia | PARTIAL | três planos iguais, sem plano recomendado; chamadas iguais |
| 3 Cor e contraste | FAIL | texto branco sobre `#a78bfa`: 2,72:1 (calculado), abaixo de 4,5:1 |
| 5 Estados | FAIL | `outline: none` sem substituto; sem estado de foco |
| 7 Movimento | PARTIAL | `transition: all`; sem `prefers-reduced-motion` |
| 8 Microcopy | FAIL | "Saiba mais" três vezes; descrições idênticas |
| 9 Visual genérico | FAIL | gradiente roxo, três cartões iguais, emoji como ícone, borda lateral de acento, tudo centralizado |

**Achados**

| ID | Categoria | Impacto | Evidência | Correção |
| --- | --- | --- | --- | --- |
| UI-01 | estados | alto | Verificado no código: `.btn { outline: none }`, sem `:focus-visible` | restaurar contorno de 2 px com contraste de pelo menos 3:1 contra o fundo |
| UI-02 | cor | alto | `#fff` sobre `#a78bfa` = 2,72:1 (calculado) | escurecer o fundo do botão ou usar texto escuro; recalcular |
| UI-03 | acessibilidade | alto | `<input placeholder>` sem `<label>` | rótulo visível e associado; placeholder só como exemplo |
| UI-04 | microcopy | médio | três botões "Saiba mais" | "Ver recursos do plano Pro", "Começar com o Básico" etc. |
| UI-05 | visual genérico | médio | gradiente roxo, três cartões, emoji como ícone | só se o briefing não os pediu; sugerir diferenciar o plano recomendado em peso e posição |
| UI-06 | movimento | médio | `transition: all .3s` | listar `background-color, transform` e proteger com `prefers-reduced-motion` |

**Quick wins:** UI-01, UI-03, UI-04. **Top 3 de impacto alto:** UI-01, UI-02, UI-03.

**Não verificado:** renderização em 375, 768 e 1440 px; contraste do estado hover; leitor de tela; se o briefing pediu gradiente e três planos; desempenho.

Opinião de modelo; não substitui teste com usuários nem revisão de acessibilidade com tecnologia assistiva.

## Observações de método

- O contraste de `#ffffff` sobre `#a78bfa` foi calculado com a fórmula do WCAG (resultado 2,72:1, valor calculado para este exemplo em 2026-10-10 a partir da fórmula do arquivo `contraste-wcag.md`); confirme com o script antes de reaproveitar o número.
- O relatório não reescreve a página: oferece correção específica por achado e deixa a aplicação para outro pedido.
