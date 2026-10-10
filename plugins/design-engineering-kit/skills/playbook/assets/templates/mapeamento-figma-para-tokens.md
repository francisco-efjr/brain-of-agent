# Mapeamento Figma para tokens e componentes: [tela ou frame]

Template do design-engineering-kit. Uso: passo 4 do fluxo (a) do playbook. Compare por **função e valor**, não pelo nome da variável do Figma. Valor cru nunca entra no código. O que não tem equivalente é divergência para o humano, não improviso.

## 1. Origem

- **Frame/nó:** [link do Figma] · **Ferramentas lidas:** [get_design_context | get_variable_defs | get_screenshot | get_metadata] · **Data:** [AAAA-MM-DD]
- **Design system ativo:** [caminho] · **Stack:** [ ] · **Componentes reutilizáveis encontrados:** [lista]

## 2. Variáveis e estilos

| Variável/estilo no Figma | Valor | Token do sistema | Equivalência | Ação |
| --- | --- | --- | --- | --- |
| [Primary/500] | [#C2456E] | [`--accent`] | [exata | aproximada | nenhuma] | [usar | token proposto | divergência] |

Equivalência aproximada nunca é arredondada sem aprovação: registre a diferença.

## 3. Componentes

| Elemento no Figma | Componente do projeto | Props/variante | Code Connect (se existir) | Ação |
| --- | --- | --- | --- | --- |
| [Botão primário] | [`Button`] | [`variant="primary"`] | [mapa encontrado | não consultado] | [reutilizar | criar com justificativa] |

## 4. Estados que o Figma não mostra

| Estado | Fonte da definição | Decisão |
| --- | --- | --- |
| [vazio, carregando, erro, foco, texto longo] | [sistema | pendente] | [implementar | perguntar] |

## 5. Divergências e tokens propostos

| Item | Figma | Sistema | Proposta | Quem confirma |
| --- | --- | --- | --- | --- |
| [raio do card] | [14 px] | [`--radius-card` 12 px] | [manter sistema] | [humano] |

## 6. Verificação

- Comparação com `get_screenshot` do nó em [375 | 768 | 1280] pelo fluxo (b): [resultado ou "Não verificado"].
- **Não coberto:** [hover, animação, conteúdo oculto, variantes não selecionadas].
