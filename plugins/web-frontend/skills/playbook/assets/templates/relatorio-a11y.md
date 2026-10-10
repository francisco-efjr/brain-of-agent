# Relatório de acessibilidade: [fluxo ou tela]

Alvo: WCAG 2.2 nível AA, salvo requisito diferente: [alvo]. Isto não é parecer jurídico nem declaração de conformidade. Base: formato de achado do brain-of-agent (`acessibilidade.md`, MIT) e molde de severidade de V-17 e V-61. Data: [AAAA-MM-DD].

## Escopo e ambiente

- Fluxo crítico avaliado: [login, cadastro, checkout, busca]
- Modo: [estático (leitura do código) / runtime (teclado e leitor de tela)]
- Navegador e tecnologia assistiva: [ex.: Windows 11, Firefox com NVDA; macOS, Safari com VoiceOver]
- Viewports e temas: [320 px, desktop, claro, escuro]
- Automação executada: [axe versão e tags, saída] ou "não executada"

## Achados

Um bloco por achado:

> **[Título curto: onde e o que]**
> - ID: A11Y-[nn] · Severidade: [Crítico / Alto / Médio / Baixo] · Confiança: [1-10]
> - Critério WCAG: [número, nome, nível]
> - Afeta: [quem: teclado, leitor de tela, voz, baixa visão, cognição]
> - Onde: [`arquivo:linha` ou fluxo e passos]
> - Esperado versus anunciado/observado: [texto anunciado versus esperado]
> - Evidência: [regra do axe e seletor, captura, gravação]
> - Correção mínima: [mudança proposta, preferindo HTML nativo]
> - Reteste: [como confirmar]

Severidade pelo efeito na tarefa: Crítico = tarefa impossível; Alto = confunde, prende o foco ou esconde erro; Médio = atrito com contorno; Baixo = polimento. Comportamento de leitor de tela que você não observou é **Inferido**.

## Resumo por critério

| Critério | Resultado | Nota |
| --- | --- | --- |
| 1.1.1 Conteúdo não textual | [ok / falha / não testado] | |
| 1.4.3 Contraste (mínimo) | | |
| 1.4.10 Reflow (320 px) | | |
| 2.1.1 Teclado | | |
| 2.4.7 Foco visível | | |
| 2.4.11 Foco não obscurecido (mínimo) | | |
| 2.5.7 Movimentos de arrastar | | |
| 2.5.8 Tamanho do alvo (mínimo) | | |
| 3.3.1 / 3.3.3 Erro: identificação e sugestão | | |
| 3.3.7 Entrada redundante | | |
| 3.3.8 Autenticação acessível (mínimo) | | |
| 4.1.2 Nome, função, valor | | |

## Checklist de reteste

- [ ] Tab/Shift+Tab percorre tudo na ordem visual, sem armadilha
- [ ] Enter, Espaço, Esc e setas conforme o padrão do widget
- [ ] Diálogos: foco entra, fica contido, Esc fecha, foco volta ao gatilho
- [ ] Erros de formulário ligados ao campo e anunciados
- [ ] Axe sem violações nos estados testados e `incomplete` revisado
- [ ] Zoom 200% e 320 px sem perda; movimento reduzido respeitado

## Não testado

[lista do que ficou de fora: leitores de tela não usados, estados não alcançados, mobile nativo, jurisdição]

## Armadilhas desta auditoria

Varredura feita no esqueleto de carregamento dá falso verde; axe zerado não é acessível; `focus()` programático pode não ativar `:focus-visible`: use Tab.
