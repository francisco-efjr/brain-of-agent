---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta explicitamente "rápido", "vários formatos", "etc." e "seguro" (e idealmente "relatórios" sem dizer quais) como vagos e os converte em perguntas concretas (quais relatórios, quais formatos, tempo com que volume, quem pode exportar).
2. Propõe critérios mensuráveis (tempo, volume, formato exato, regra de permissão), mas marca todo limite que não veio do usuário como Suposição ou pergunta aberta com dono; não apresenta p95, tamanho máximo ou lista de formatos como decididos.
3. Inclui ao menos um caminho negativo observável (gerente sem permissão, falha na geração, volume acima do limite, filtro sem resultados).
4. Escreve os critérios na ordem caminho feliz, depois falhas e bordas, depois não funcionais; cada cenário descreve um comportamento com dado concreto, e nenhum usa verbos de interface (clicar, botão, tela, campo).
5. Pergunta ou declara em que canal o export roda (web, app, API) e o que muda, em uma frase.
FAIL if qualquer um ocorrer: aceita as palavras vagas sem questioná-las; apresenta números inventados como fatos; cenários do tipo "clico em Exportar"; nenhum caminho negativo; escreve step definitions ou código de automação.
