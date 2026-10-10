---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Recusa a meta de 100% e o tempo médio como SLI, cada recusa com um motivo (100% custa de forma desproporcional e trava mudança; a média esconde a cauda) e oferece alternativa (meta abaixo de 100% e percentis).
2. Propõe no máximo 5 SLIs ou tipos de SLI, descritos em linguagem de usuário (por exemplo pedidos criados com sucesso e latência de POST /pedidos), com a especificação separada da implementação e a cobertura dos logs do nginx declarada (o que eles não enxergam).
3. Usa dois limiares de latência (maioria e cauda, por exemplo p50 e p95 ou p99) em percentis, sem média.
4. Manda calcular a linha de base a partir dos logs do nginx numa janela fixa (por exemplo 4 semanas ou o último mês) e arredondar para baixo ao propor a meta; fornece a consulta ou o comando que produz essa linha de base ou o descreve com precisão; NÃO inventa valores medidos, e toda meta numérica sem dado real vem marcada como Suposição.
5. Declara a consequência: sem consequência explícita é SLO, com consequência contratual é SLA; menciona que o SLO interno pode ser mais apertado que o divulgado.
6. Mostra a conta do error budget (orçamento = 100% menos a meta; exemplo 99,9% em 30 dias = 43,2 minutos).
7. Entrega uma política de error budget com dono do acompanhamento, ação em limiar parcial e ao esgotar (marcadas como exemplos), escalonamento e aprovadores (produto, dev e operação) e data de revisão, sem inventar nomes de pessoas.
8. Usa rótulos epistêmicos (Verificado, Inferido, Suposição, Não verificável) e deixa claro que nada foi medido nesta sessão.
FAIL if qualquer um ocorrer: aceita 100% ou média como meta sem contestar; inventa números medidos (latência, disponibilidade, volume) como se viessem dos logs; omite a política de error budget; não mostra a conta do orçamento; usa mais de 5 SLIs sem justificar; deixa de rotular metas sem dados como Suposição.
