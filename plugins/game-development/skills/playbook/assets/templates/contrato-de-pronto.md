# Contrato de pronto — [funcionalidade]

Preencha **antes** de codar. Cada critério tem um comando, sonda ou captura que o prova, e um limiar fixado antes de medir. Não reduza critério para esconder falha.

- **Engine e versão:** [Godot 4.x | Unity 6000.x | Unreal 5.x] · **Commit/build:** [hash]
- **Comando de check:** [comando] · **Cena de teste:** [caminho]
- **Origem do pedido:** [GDD §x | história | pedido do usuário]

| # | Critério (comportamento observável) | Como provar (comando, sonda, captura) | Limiar mínimo | Tipo |
| --- | --- | --- | --- | --- |
| 1 | Funciona: [comportamento] sem erro no log | [`comando`] -> linha [esperada] | exit 0, 0 linhas `ERROR` | Logic / Integration |
| 2 | Regressão: [comportamento antigo] segue igual | [comando ou teste] | igual ao baseline [commit] | Integration |
| 3 | Orçamento de frame (se o projeto definiu) | [profiler no hardware-alvo] | <= [N] ms | Performance |
| 4 | Legibilidade: feedback visual/sonoro presente | [captura] + humano | presente | Visual/Feel |

## Pendência humana (NÃO AVALIADO por agente)

- [ ] Sensação de jogo: [o que o humano deve sentir/avaliar]
- [ ] Áudio: [...]
- [ ] Legibilidade visual: [...]

## Fora do escopo

[o que este contrato não cobre]

## Calibração do avaliador (opcional)

[2 a 3 exemplos de notas comentadas do projeto; ver agente `game-evaluator`]
