---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um rascunho de contrato no padrão ODCS fixando a versão 3.2.0, com ao menos: identificação e versão do contrato, schema com tipos e chave (`customer_id`), regras de qualidade, SLA de frescor de 2 horas (atualização horária) e servidor ou local.
2. Não inventa o responsável: o dono aparece como time de CRM com a pessoa marcada como pendente ou como pergunta.
3. Entrega a matriz de regras com ação: `customer_id` nulo ou duplicado = `fail`; `country` fora da lista ISO = `drop` com contagem reportada e quarentena (ou `warn` com justificativa explícita); `email` ausente e `segment` atrasado = `warn` com número de pendências, e não `fail` (a ausência de email é esperada em 8%).
4. Toda regra relata a contagem de violações; `warn` é tratado como pendência com número e prazo, não como aprovação; menciona que `drop` exige um fluxo de quarentena (o dbt, por si, só distingue erro de aviso por `severity`).
5. Propõe a política para o agente com três níveis: `block` (DDL e DML destrutivo, `SELECT *` em produção), `warn` (falta de filtro de partição ou de limite) e `log` (estilo), e/ou role somente leitura; trata `email` como dado pessoal a mascarar nas amostras.
6. Afirma que o contrato NÃO foi validado e que a validação deve ser feita com o JSON Schema oficial do ODCS pelo usuário; não declara o YAML como válido.
FAIL if qualquer um ocorrer: inventa o nome do dono; declara o contrato válido ou validado; usa `fail` para `email` ausente; propõe `accepted_values` com valores inventados para `country`; deixa regras sem ação ou sem contagem de violações; executa ou diz ter executado algo.
