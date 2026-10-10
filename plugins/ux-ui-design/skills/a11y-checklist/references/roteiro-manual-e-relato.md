# Roteiro manual de acessibilidade e formato de achado

Base: `acessibilidade.md` do brain-of-agent (MIT, do usuário), com a correção de data e contagem da WCAG 2.2 (V-08). Atalhos de leitores de tela mudam por versão e configuração; confirme na documentação do leitor usado antes de ensinar um atalho como regra.

## Sumário

- [Como conduzir](#como-conduzir)
- [Teclado](#teclado)
- [Leitor de tela](#leitor-de-tela)
- [Zoom, reflow, movimento, cor e mídia](#zoom-reflow-movimento-cor-e-mídia)
- [Mobile](#mobile)
- [Formato de achado](#formato-de-achado)

## Como conduzir

Faça por tarefa completa (cadastrar, comprar, recuperar senha), não por tela isolada. Só pessoas avaliam também linguagem (termo desconhecido, instrução ambígua). Quando possível, observe 3 a 5 pessoas do público real em silêncio. Este plugin não executa o roteiro: ele o especifica, e quem testa informa o que viu. Resultados relatados sem execução são Inferido.

## Teclado

Teclas: Tab e Shift+Tab, Enter (link, botão), Espaço (botão, caixa de seleção), setas (rádio, abas, menu, slider), Esc (fecha diálogo e menu). No macOS, ative a navegação por teclado do sistema e, no Safari, a opção que permite Tab entre todos os itens; sem isso, o Tab pula links e você reporta um falso defeito.

1. O primeiro Tab mostra "Pular para o conteúdo", que leva ao `main` (2.4.1).
2. A ordem de foco segue a ordem visual (2.4.3); `tabindex` positivo é defeito.
3. O foco é sempre visível (2.4.7) e não fica coberto por cabeçalho fixo, banner de cookies ou chat (2.4.11).
4. Tudo que funciona com mouse funciona com teclado (2.1.1): menu em hover, tooltip, carrossel, arrastar, seletor de data.
5. Sem armadilha (2.1.2): sair de player, editor rico, mapa, iframe de pagamento.
6. Diálogo: o foco entra, Tab circula dentro, Esc fecha, o foco volta ao gatilho.
7. Conteúdo de hover ou foco sai com Esc e não some ao passar o ponteiro sobre ele (1.4.13).

## Leitor de tela

Combinações de referência: NVDA com Firefox ou Chrome (Windows), VoiceOver com Safari (macOS e iOS), TalkBack com Chrome (Android); JAWS com Chrome onde o público usar. Priorize a combinação do seu público.

| Ação | NVDA (tecla NVDA = Insert) | VoiceOver macOS (VO = Ctrl+Option) |
| --- | --- | --- |
| Ligar | Ctrl+Alt+N (instalado) | Cmd+F5 |
| Próximo item / ativar | seta para baixo / Enter | VO+seta para a direita / VO+Espaço |
| Próximo título | H (1 a 6 por nível) | VO+Cmd+H |
| Próximo campo de formulário | F | VO+Cmd+J |
| Lista de elementos | NVDA+F7 | VO+U (rotor) |
| Calar a fala | Ctrl | Ctrl |

Anote em três colunas: passo, o que foi anunciado, o que deveria ser anunciado. Verifique:

- nome, papel e estado de cada controle ("Aceito os termos, caixa de seleção, não marcada");
- conteúdo encontrável por títulos e marcos (`main`, `nav`);
- erro de formulário anunciado com o modo de corrigir;
- mudança dinâmica anunciada (item adicionado, total, toast);
- foco num lugar sensato depois de cada ação (fechar diálogo, enviar formulário, trocar de rota).

## Zoom, reflow, movimento, cor e mídia

- Zoom do navegador a 200%: nada cortado ou sobreposto. Janela de 1280 px a 400%: só rolagem vertical (tabela, mapa e diagrama são exceção) e menu acessível.
- Fonte grande do sistema somada ao zoom; retrato e paisagem (1.3.4).
- Movimento reduzido ligado no sistema (ou emulado no DevTools): parallax e animações de transição param.
- Nada só por cor (1.4.1): simular daltonismo em Rendering, Emulate vision deficiencies; testar o tema escuro, que tem contraste próprio.
- Vídeo: legenda sincronizada e revisada (1.2.2), porque automática sem revisão erra nome próprio e número; audiodescrição ou alternativa (1.2.3, 1.2.5); ao vivo, legenda (1.2.4). Som automático por mais de 3 s precisa de controle (1.4.2).

## Mobile

- Alvo: o piso web é 24 px CSS; em iOS e iPadOS a HIG fala em 44×44 pt como padrão e 28×28 pt como mínimo (V-39; © Apple, destilado). O valor de 48 dp do Android e os tokens do Material 3 não foram verificados nesta rodada: Não verificável.
- Texto: Dynamic Type (iOS) e escala de fonte (Android); use `sp` e estilos de texto do sistema; na escala máxima o texto não trunca e a tela rola. A HIG pede permitir ampliação de pelo menos 200% (140% no watchOS).
- Nome acessível: Android `contentDescription`; iOS `accessibilityLabel`; React Native `accessibilityLabel` com `accessibilityRole`; Flutter `Semantics(label: …)`. Imagem decorativa sai da árvore. Não ponha o papel no rótulo ("botão Salvar" vira "botão Salvar, botão"). Implementação nativa pertence ao plugin `mobile-apps`.
- Gestos de vários dedos e sacudir o aparelho precisam de alternativa simples (2.5.1, 2.5.4).
- Contraste: o Accessibility Inspector da Apple usa AA (4,5:1 até 17 pt; 3:1 a partir de 18 pt ou negrito); ofereça esquema de maior contraste com Increase Contrast e verifique claro e escuro (V-39).

## Formato de achado

Severidade pelo efeito na tarefa (impede sem contorno é alta), não só pelo `impact` do axe. Template: [T-09](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/achado-a11y.md).

> **Carrinho: botão de remover item é anunciado só como "botão"**
>
> - **Critério:** 4.1.2 Nome, função, valor (A).
> - **Afeta:** quem usa leitor de tela e quem usa controle por voz.
> - **Ambiente:** homologação, build 2.14.0; Windows 11, Firefox com NVDA; reproduz em iOS, Safari com VoiceOver.
> - **Passos:** 1. Adicionar "Camiseta azul M" e "Boné preto". 2. Abrir `/carrinho`. 3. Com NVDA ligado, Tab até o primeiro item.
> - **Esperado:** "Remover Camiseta azul M do carrinho, botão".
> - **Obtido:** "botão"; não dá para saber o que faz nem de qual item.
> - **Evidência:** axe `button-name` (critical) em `.cart-item:nth-child(1) .icon-btn`; gravação com áudio do leitor.
> - **Severidade:** crítico (impede revisar o carrinho com autonomia, sem contorno). **Prioridade:** alta (fluxo de compra).
> - **Correção:** `<button type="button" aria-label="Remover Camiseta azul M do carrinho">` com o ícone em `<svg aria-hidden="true">`; depois de remover, foco no próximo item e aviso em `role="status"` ("Camiseta azul M removida. Total: R$ 89,90").

O exemplo é de caso fictício do material do brain-of-agent (MIT); os valores são ilustrativos. Em uma revisão sem execução, troque "Ambiente" e "Evidência" por "Não testado com leitor de tela" e rotule a correção como Inferido.
