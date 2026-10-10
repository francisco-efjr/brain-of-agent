---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Diz que o plano não está bom e aponta o problema de olhar o resultado repetidamente e parar ao ver significância (parada oportunista), que aumenta o falso positivo muito acima dos 5% nominais.
2. Calcula a amostra com a regra de bolso n = 16 x σ² / δ², com σ² = 0,04 x 0,96 = 0,0384 e δ = 0,005, chegando a cerca de 24,6 mil por braço (24.576), e rotula como regra de bolso do autor (não cálculo de poder completo).
3. Conclui que 10 mil por braço é insuficiente para detectar 0,5 ponto percentual com essa regra.
4. Propõe corrigir o desenho: fixar hipótese, efeito mínimo, amostra e critério de parada antes de começar e não encerrar ao ver significância; ou usar análise sequencial com checkpoints definidos antes, ou abordagem bayesiana, dizendo que isso muda a análise.
5. Não inventa dados sobre o checkout além dos informados; pode perguntar sobre o tráfego diário para estimar a duração.
FAIL if qualquer um ocorrer: aprova o plano; dá um número de amostra sem mostrar a fórmula ou com conta errada (fora de 24 a 25 mil por braço); omite o risco da parada oportunista; apresenta a regra de bolso como garantia estatística exata.
