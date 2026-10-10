---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aplica um critério de inclusão explícito (estrutural, difícil de reverter ou transversal) e conclui que a escolha PostgreSQL contra DynamoDB merece ADR, enquanto a renomeação de `tmp` para `orderDraft` não merece, informando o destino (nenhum registro, convenção de código ou linter).
2. Apresenta um rascunho de ADR no chat com status `proposto`, contexto, decisão em voz ativa, pelo menos 2 alternativas (DynamoDB e "não mudar nada" ou equivalente) cada uma com motivo, pelo menos 1 consequência negativa e nível de confiança ou gatilho de reavaliação.
3. Cita como decisores apenas Marina e Paulo; o que não foi informado (número do ADR, data exata, outros stakeholders) aparece como "a confirmar", "a definir" ou `[NEEDS CLARIFICATION]`.
4. Pede aprovação do usuário, ou oferece gravar, antes de criar qualquer arquivo.
5. Trata o "pico de 200 req/s" como dado informado pelo usuário ou Suposição e não acrescenta métricas inventadas.
FAIL if qualquer um ocorrer: grava arquivo sem aprovação; cria ADR para a renomeação da variável; rascunho sem nenhuma consequência negativa; inventa decisor, data ou número de ADR sem marcar; afirma ter lido ou criado arquivos do repositório que o usuário disse não ter aberto.
