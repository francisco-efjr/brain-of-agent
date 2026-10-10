---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Dá nota por categoria apenas para tipos (3 erros de `tsc`) e lint (7 avisos, 0 erros), com os números citados a partir da saída colada, e declara a régua usada para converter contagem em nota (na régua do plugin: menos de 10 erros de tipo vale 7; de 5 a 19 avisos de lint vale 4). Outra régua é aceita se for declarada e aplicada de forma coerente às duas categorias.
2. Declara testes e código morto como indisponíveis, com o motivo (sem script de teste nem runner instalado; sem ferramenta de código morto configurada), e não os trata como aprovados nem como "pulados sem explicação".
3. Se der nota composta, marca-a como cobertura parcial (por exemplo "cobertura parcial: 2 de 5 categorias", ou "2 de 4" se shell for declarado não aplicável, ou "baseada só em tipos e lint") e não a apresenta como saúde geral do projeto; nunca dá 10/10.
4. Ordena as recomendações por peso da categoria vezes o déficit de nota e inclui a ausência de testes como lacuna de cobertura a resolver, não como nota zero inventada.
5. Não corrige código, não executa comandos (o caso não permite) e não inventa saída de testes nem de outras ferramentas. Pode mostrar o final da saída bruta das falhas.
FAIL if qualquer um ocorrer: dá nota alta ou 10/10 ignorando as categorias ausentes; inventa resultados de teste ou de cobertura; "corrige" os erros de tipo ou aplica `--fix`; omite que a cobertura é parcial; calcula tendência ou compara com rodada anterior inexistente.
