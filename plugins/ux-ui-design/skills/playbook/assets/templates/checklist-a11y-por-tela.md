# Checklist de acessibilidade por tela (WCAG 2.2 AA)

Template T-08. Uso: `a11y-checklist` e `a11y-reviewer`. Status por item: **Verificado** (testei e colei evidência), **Inferido** (li markup ou código, não testei), **Não testado**, **Não aplicável**. Axe zerado não é acessível: automação é piso. Este checklist não declara conformidade legal (LBI, NBR 17060, EAA, Section 508).

- **Tela ou fluxo:** [___] · **Alvo:** [web | iOS | Android] · **Data:** [AAAA-MM-DD]
- **Ambiente de teste:** [navegador e versão; leitor de tela e versão; viewport]

| # | Item | Critério | Como testar (manual / automático) | Status | Evidência |
| --- | --- | --- | --- | --- | --- |
| 1 | Idioma da página e título único | 3.1.1, 2.4.2 | Inspecionar `<html lang>` e `<title>` / axe `html-has-lang` | | |
| 2 | Estrutura: um h1, títulos sem saltos, landmarks, link de pular conteúdo | 1.3.1, 2.4.1, 2.4.6 | Árvore de acessibilidade, Tab inicial / axe | | |
| 3 | Todo controle tem nome, papel e estado | 4.1.2 | Árvore de acessibilidade ou leitor de tela / axe `button-name`, `link-name` | | |
| 4 | Rótulo visível contido no nome acessível | 2.5.3 | Comparar texto visível e nome computado | | |
| 5 | Contraste de texto 4,5:1 (3:1 texto grande) em todos os estados e temas | 1.4.3 | Calcular pela fórmula com valores reais / axe `color-contrast` (ler `incomplete`) | | |
| 6 | Contraste de componentes e foco 3:1 | 1.4.11 | Calcular borda de campo, ícone, anel de foco | | |
| 7 | Nada só por cor | 1.4.1 | DevTools: Emulate vision deficiencies | | |
| 8 | Reflow em 320 px e zoom de 200% | 1.4.10, 1.4.4 | Viewport 320 px; zoom do navegador | | |
| 9 | Espaçamento de texto ajustável sem perda | 1.4.12 | Aplicar linha 1,5×, parágrafo 2×, letras 0,12×, palavras 0,16× | | |
| 10 | Conteúdo de hover e foco dispensável, passável, persistente | 1.4.13 | Teclado e mouse | | |
| 11 | Todo uso de mouse tem equivalente por teclado; sem armadilha | 2.1.1, 2.1.2 | Tab, setas, Enter, Espaço, Esc | | |
| 12 | Ordem de foco = ordem visual; sem tabindex positivo | 2.4.3 | Tab / axe `tabindex` | | |
| 13 | Foco visível e não obscurecido | 2.4.7, 2.4.11 | Tab com cabeçalho fixo, cookies, chat | | |
| 14 | Alvos ≥ 24×24 px CSS (meta 44 em toque) | 2.5.8 | Medir alvo computado / axe `target-size` | | |
| 15 | Alternativa a gestos de arrastar | 2.5.7 | Operar sem arrastar | | |
| 16 | Rótulos e instruções em todo campo; `autocomplete` correto | 3.3.2, 1.3.5 | Inspeção; teste com autofill | | |
| 17 | Erro identificado, descrito e ligado ao campo; foco no primeiro erro | 3.3.1, 3.3.3 | Enviar com erro; leitor de tela | | |
| 18 | Não pedir de novo o que já foi informado | 3.3.7 | Percorrer o fluxo | | |
| 19 | Autenticação sem teste cognitivo obrigatório; colar senha permitido | 3.3.8 | Colar senha e código; gerenciador de senhas | | |
| 20 | Ajuda no mesmo lugar relativo nas telas | 3.2.6 | Comparar telas | | |
| 21 | Diálogo modal: nome, foco inicial, Tab circular, Esc, foco volta ao gatilho (9 itens do APG) | 2.1.2, 2.4.3, 4.1.2 | Teclado e leitor de tela | | |
| 22 | Mudança dinâmica anunciada (toast, total, erro) com região existente antes da mensagem | 4.1.3 | Leitor de tela | | |
| 23 | Movimento: `prefers-reduced-motion`; pausar o que se move por mais de 5 s; no máximo 3 flashes por segundo | 2.2.2, 2.3.1 | Ligar a preferência no sistema | | |
| 24 | Imagens: alternativa em informativas, `alt=""` em decorativas | 1.1.1 | Inspeção / axe `image-alt` | | |
| 25 | Mídia: legenda sincronizada e revisada; audiodescrição ou alternativa; som automático com controle | 1.2.2, 1.2.3, 1.2.5, 1.4.2 | Reproduzir | | |
| 26 | Orientação não travada; texto redimensionável | 1.3.4, 1.4.4 | Girar o aparelho | | |

## Automação (piso)

- Axe por rota **e por estado** (carregada, diálogo aberto, erro, menu móvel, tema escuro, 375 px): [rodou | não rodou]. Tags: `wcag2a`, `wcag2aa`, `wcag21a`, `wcag21aa`, `wcag22aa`. Fila `incomplete` revisada: [sim/não]. Regras desligadas ou exclusões, com motivo: [___].

## Não testado

[Liste: leitor de tela X, zoom Y, tema escuro, etc., e como confirmar]

## Observações

Critérios fora do AA que o contrato pode exigir (AAA, por exemplo 2.4.12, 2.4.13, 2.5.5): [___]. 4.1.1 foi removido na WCAG 2.2: não reportar "HTML inválido"; reportar o efeito.
