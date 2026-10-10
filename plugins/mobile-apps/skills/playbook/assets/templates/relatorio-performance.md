# Relatório de performance mobile

Base: protocolo de medir, mudar um eixo e remedir (V-11, V-22, V-30, V-32, V-29). Uma mudança por ciclo; mesma captura antes e depois; reverter se não houver ganho. Sem medição, escreva "Não verificável (sem medição)": não prometa ganho numérico.

**Aviso de redação:** antes de anexar traces, screenshots ou logs, remova tokens, dados pessoais e dados de produção; evite capturas de contas reais. Correção sobre o protocolo de V-22, que não orienta isso.

Plataforma e versões lidas: [ex.: Android, Compose BOM, Kotlin 2.x] · Build medido: [release / profile; nunca debug] · Aparelho: [modelo; de menor capacidade, se houver] · Data: [AAAA-MM-DD]
Sintoma e como reproduzir (uma transição): [ex.: rolar a lista de pedidos por 5 s]
Classe do sintoma: [renderização/rolagem / partida / memória / bateria e segundo plano]

## Ciclos

| Ciclo | Eixo investigado | Sintoma | Causa suspeita | Evidência (captura, relatório do compilador, DevTools) | Correção (uma mudança) | Validação (mesma captura depois) | Resultado |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [ex.: fase de leitura de State] | [quadros perdidos] | [leitura de scroll em composição] | [captura antes: ...] | [mover leitura para a fase de layout] | [captura depois: ...] | [mantido / revertido] |

## Medições

| Métrica | Antes | Depois | Como medir | Rótulo |
| --- | --- | --- | --- | --- |
| [ex.: quadros acima de 16 ms] | | | | Verificado / Não verificável |

## Verificação por plataforma

- Compose: estabilidade, fase de leitura, escrita de snapshot; `@Immutable`/`@Stable` são promessas (V-11).
- SwiftUI: perfil guiado só se necessário; Instruments exige macOS (V-22).
- Flutter: profile mode e DevTools; orçamento de 16 ms (V-29).
- React Native: release; `console.*` removido; medir só cold start para TTI (V-30, V-32).

## Falsos positivos descartados e limites

[o que parecia problema e não era; o que a medição não prova; lacunas]

## Próximo passo

[uma ação]
