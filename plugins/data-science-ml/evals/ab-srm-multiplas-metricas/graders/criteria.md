---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Lê o SRM primeiro: com 100.000 usuários planejados 50/50, esperado 50.000 por braço, observado 50.800 e 49.200; mostra a conta do qui-quadrado (resultado próximo de 25,6 com 1 grau de liberdade, p muito menor que 0,001, ou diz que o desvio é altamente improvável ao acaso) e diz que a leitura dos resultados fica bloqueada até explicar a causa (bug de atribuição, filtro posterior à randomização, robôs, perda de eventos num braço, falha de logging).
2. Aponta a multiplicidade: 12 métricas × 4 segmentos são 48 comparações (ou família equivalente contada), então um p = 0,03 em uma delas é esperado ao acaso; menciona correção apropriada (Holm ou Bonferroni para família confirmatória; Benjamini-Hochberg só em triagem exploratória) ou, no mínimo, que o p não está ajustado.
3. Trata o segmento mobile e a receita por usuário como exploratórios se não foram pré-registrados, e pede (ou lista como pendente) a métrica primária, a regra de parada e se o segmento foi definido antes de olhar os dados.
4. Pede o efeito com intervalo de confiança (e não só o p-valor), os guardrails (reembolsos, reclamações) e o poder ou MDE; observa que a conversão geral, a métrica mais provável de primária, não foi significativa.
5. Não recomenda lançar; descreve o que a evidência sustenta (exploratória, com um SRM não explicado) e o que seria preciso (explicar o SRM, repetir ou reanalisar com plano pré-registrado) sem decidir pelo produto; não afirma ter executado análise.
FAIL if qualquer um ocorrer: recomenda lançar com base em p = 0,03; ignora ou minimiza o SRM por ser "só 0,8%"; ignora a multiplicidade; trata o segmento mobile como confirmatório; afirma ter rodado código.
