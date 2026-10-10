# Experimento A/B: [nome]

Base: Evan Miller, "How Not To Run an A/B Test" (2010), destilado. Preencha **antes** de olhar qualquer resultado.

## Hipótese

Se [mudança] para [população], então [métrica] vai [direção] em pelo menos [δ], porque [motivo].

## Métricas

- **Primária:** [nome, fórmula, fonte, janela].
- **De guarda (não podem piorar):** [lista e limite].

## Dimensionamento

| Parâmetro | Valor | Origem |
| --- | --- | --- |
| Taxa base p | [ex.: 0,04] | [dado, fonte e data] |
| σ² = p(1 - p) | [ex.: 0,0384] | calculado |
| Efeito mínimo de interesse δ | [ex.: 0,005] | decisão de negócio de [dono] |
| Amostra por braço n ≈ 16 x σ² / δ² | [ex.: 24.576] | regra de bolso do autor (5% de significância, 80% de poder; conferir na fonte) |
| Tráfego diário por braço | [valor] | [dado] |
| Duração prevista | [dias] | n / tráfego |

## Desenho

- Unidade de aleatorização: [usuário, sessão, conta] · Braços: [controle, variante(s)] · Divisão: [50/50]
- Interferência entre braços considerada: [sim/não e como]
- Dias da semana completos cobertos: [sim/não]

## Parada e decisão (fixadas antes)

- **Critério de parada:** o teste termina quando cada braço atingir [n] ou em [data], o que ocorrer primeiro; **não** encerrar ao ver significância.
- **Espiadas permitidas:** nenhuma com parada por p-valor. Se for preciso monitorar: análise sequencial com checkpoints combinados antes ([lista]) ou abordagem bayesiana.
- **Decisão pré-registrada:** se a variante ganhar em [δ]: [ação]. Se perder: [ação]. Se empatar: [ação].

## Registro de resultados (preencha só depois da parada)

| Braço | n | Conversão | Intervalo | Observações |
| --- | --- | --- | --- | --- |

Análises avançadas (CUPED, SRM, OEC) pertencem a `/data-science-ml:playbook`. Limites: o modelo não executa o teste nem inventa dados.
