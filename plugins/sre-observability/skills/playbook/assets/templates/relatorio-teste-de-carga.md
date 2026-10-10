# Teste de performance — [SISTEMA] — [data]

Template T-09. Adaptado de `brains/qa/references/performance.md` do brain-of-agent (conteúdo próprio, MIT), com limiares derivados do SLO (V-21). Preencha só com resultados de execuções reais, com saída colada; o que foi extrapolado vai em "Extrapolado". O plugin não executa carga: o usuário executa com autorização e janela combinadas.

**Pergunta:** [ex.: o checkout aguenta 4× o pico de 2025 dentro do SLO?]
**Veredito:** [atende | não atende | atende com ressalvas] — [uma frase]

## Condições

- Tipo, modelo e perfil: [smoke / carga / estresse / pico / soak / breakpoint]; [aberto/fechado]; [rampa, patamar, taxa, mix]
- Origem dos números: [analytics/APM/logs; hora de pico; fator de pico e de onde veio; Lei de Little: L = λ × W com a conta]
- Ambiente: [topologia, tamanho vs produção, volume da base, versão testada]
- Autorização e janela: [quem autorizou, janela, volume máximo, como interromper]
- Stubs e fora do escopo: [terceiros simulados, fluxos não exercitados]
- Gerador: [onde rodou, CPU/memória/rede monitoradas, `dropped_iterations`, `vus_max` × `maxVUs`]
- Versão da ferramenta e do script: [`k6 version`, commit do script]

## Resultados no patamar

| Endpoint | Vazão | p50 | p95 | p99 | Erro | SLO | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`POST /pedidos`] | [req/s] | [ms] | [ms] | [ms] | [%] | [p95 < 800 ms, erro < 0,5%] | [✓/✗] |

Thresholds do k6: [lista ✓/✗ com a saída colada]. Curva latência × vazão e joelho: [descrição; capacidade útil = vazão em que o p95 cruza o SLO].

## Gargalos e evidências

- [sintoma] → [causa provável] → [evidência: trace, métrica, horário] · rótulo [Verificado / Inferido]

## Recomendações e risco residual

- [ação, dono, impacto esperado]
- Risco que sobra: [o que não foi verificado]

## Medido × extrapolado × suposições

- **Medido:** [..]
- **Extrapolado:** [ex.: capacidade de produção a partir de ambiente com [x]% do tamanho]
- **Suposições:** [..]

## Verificação do relatório

- [ ] A pergunta, o SLO e o ambiente estão escritos
- [ ] Os limiares foram validados (uma execução que passa e uma estrita que falha)
- [ ] Nenhum percentil é média de percentis; p99 tem amostras suficientes
- [ ] `dropped_iterations` = 0 ou explicado
- [ ] Nada foi afirmado sobre produção sem dizer que é extrapolação
