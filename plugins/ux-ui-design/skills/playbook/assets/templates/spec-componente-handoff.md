# Especificação de componente ou tela para handoff

Template T-06. Uso: `design-brief` (modo handoff) e `ui-designer`. A spec descreve comportamento e contrato; a implementação em código fica com o plugin de frontend (`/web-frontend:playbook`). Reutilize antes de criar: liste o que já existe.

## 1. Identificação

- **Nome:** [`Nome`] · **Tipo:** [componente | tela | padrão]
- **Propósito (uma frase):** [___]
- **Plataforma e versão mínima:** [web | iOS | Android; ___]
- **Reutiliza:** [componentes e tokens existentes encontrados com Grep] · **É novo:** [o que ainda não existe e por quê]

## 2. API (props tipadas)

| Prop | Tipo | Padrão | Obrigatória | Observação |
| --- | --- | --- | --- | --- |
| [variant] | [`'primary'` ou `'secondary'`] | `'primary'` | não | |

## 3. Estados

| Estado | Aparência (tokens) | Comportamento | Anúncio / acessibilidade |
| --- | --- | --- | --- |
| Normal | [token] | | |
| Hover | [token] | | n/a |
| Foco | anel visível ≥ 3:1, não obscurecido | | |
| Pressionado | | | |
| Desabilitado | | não recebe clique | `disabled` ou `aria-disabled`: decidir e justificar |
| Carregando | | mantém o foco, evita duplo envio | anuncia o texto ("Salvando…") |
| Erro | | preserva o que foi digitado | ligado ao campo por `aria-describedby` |
| Vazio (se lista) | | ação principal | |

## 4. Tokens consumidos

[Lista de tokens semânticos e de componente; nenhum valor cru nem primitivo.]

## 5. Teclado e foco

[Tab, Enter, Espaço, setas, Esc; ordem de foco; foco inicial e de retorno (diálogos).]

## 6. Nota de acessibilidade

[Elemento nativo usado (button, a, dialog, label); nome acessível; critérios WCAG 2.2 AA relevantes; alvo ≥ 24×24 px CSS (meta 44); o que ainda precisa de teste manual com leitor de tela.]

## 7. Conteúdo

[Textos finais ou chaves de i18n; limites de caracteres; comportamento em texto longo (nome de 47 caracteres) e na tradução (expande).]

## 8. Responsivo

[320, 768, 1440 px; o que muda, o que empilha, o que some e por quê.]

## 9. Casos de borda

[Zero itens, erro de rede, resposta obsoleta, dados extremos, permissão negada, offline (se aplicável).]

## 10. Critérios de aceite

- [ ] Todos os estados da seção 3 implementados e demonstrados (story ou captura).
- [ ] Operação completa por teclado; foco visível.
- [ ] Contraste dos pares verificado nos temas suportados.
- [ ] Reflow em 320 px sem rolagem horizontal.
- [ ] Persistência e autorização verificadas à parte do visual (protótipo navegável não prova salvamento).

## 11. Pendências e suposições

[O que o designer não pôde verificar e o que o desenvolvedor precisa confirmar.]
