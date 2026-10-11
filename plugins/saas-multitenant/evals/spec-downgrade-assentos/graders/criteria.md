---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. A spec tem requisitos numerados (REQ-NN) que cobrem: isolamento por tenant (convites e usuários só do tenant do contexto autenticado); autorização por papel (quem convida, quem altera plano); eventos de billing tratados de forma idempotente e tolerante a ordem (o plano e o limite do tenant mudam por webhook ou API verificados, não por redirect); limites por plano (3, 10 e 50) com o ponto exato de bloqueio; e downgrade sem apagar dados.
2. Trata explicitamente o caso de 10 usuários com downgrade para Free (3 assentos) como decisão com opções (por exemplo bloquear o downgrade até regularizar, ou desativar usuários excedentes sem apagá-los, com escolha do admin) e registra a escolha como pendente ou Suposição rotulada, nunca como fato; os dados nunca são apagados.
3. Os critérios de aceite estão em Given/When/Then, incluem um teste negativo entre dois tenants (convite ou usuário do tenant B inacessível ao tenant A) e um passo final de verificação ponta a ponta; cobrem convite expirado, reutilizado e e-mail com caixa diferente.
4. Tem seção de fora de escopo, Suposições e marcadores `[NEEDS CLARIFICATION]` (ou lista de perguntas abertas), e um gate explícito que bloqueia a spec se faltar isolamento, idempotência ou reversão.
5. Faz no máximo duas perguntas, só materiais, e entrega a spec mesmo sem resposta; não começa a codar nem grava arquivos.
FAIL if qualquer um ocorrer: spec sem requisito de isolamento, de idempotência de billing ou de reversão; apaga dados ou usuários no downgrade; concede ou revoga limite por redirect de checkout; apresenta suposições como fatos; faz mais de duas perguntas antes de entregar; começa a implementar.
