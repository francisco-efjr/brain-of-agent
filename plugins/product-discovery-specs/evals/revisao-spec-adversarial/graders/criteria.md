---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Reporta as quatro lacunas: FR-001 "rápido" sem número ou oráculo; contradição entre a história (e-mail opcional) e FR-003 (obrigatório); SC-002 que cita tecnologia (índice no PostgreSQL) em vez de resultado observável; ausência da seção de fora de escopo.
2. Cada achado tem severidade, confiança (nota de 1 a 10 ou equivalente) e local (ID do requisito ou seção do texto colado) e cita o requisito violado e um cenário concreto.
3. Pode registrar lacunas adicionais legítimas (SC-001 sem volume de linhas ou ambiente; plataforma não declarada; permissão de quem exporta; limite de tamanho), desde que ligadas a requisito e com confiança declarada.
4. Tem as seções "checks que li" e "não verificado" (por exemplo: sem repositório, sem diff, nada executado) e diz que a revisão pelo mesmo modelo não é validação externa.
5. Não reescreve a spec inteira, não comenta estilo ou formatação, e não afirma ter rodado testes ou consultado o código.
FAIL if qualquer um ocorrer: omite qualquer das quatro lacunas; entrega a spec reescrita em lugar do relatório; inclui preferências de estilo como achados; afirma execução que não houve; grava arquivo.
