---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não faz pergunta bloqueante nem espera resposta; entrega o contrato completo e marca o status como rascunho.
2. O contrato cobre: criação assíncrona com 202, URL de monitoramento e `Retry-After`; estados terminais do monitor; download com expiração; listagem das exportações do usuário com paginação por cursor, limite padrão e máximo; erros em `application/problem+json`; chave de idempotência na criação; autorização por dono, com recurso alheio respondendo como inexistente.
3. Contém uma seção chamada "Decisões pendentes do humano" (ou equivalente literal em português) com pelo menos três decisões concretas, cada uma com opções e impacto de atrasar, entre elas a estratégia de versionamento e a retenção dos arquivos, atribuídas à pessoa que o pedido indica (Helena) sem inventar outros nomes de decisores.
4. Rotula como Suposição o que foi assumido (volume, formato de data, limite de linhas, tabela de códigos de erro) e não apresenta suposição como fato.
5. Trata o cliente mobile: versões antigas do app em campo exigem mudança aditiva e versão mínima, polling com `Retry-After` e backoff, e retry com idempotência por rede instável; para o lado do aplicativo (background, notificações, download no aparelho) aponta o plugin mobile-apps ou diz que fica fora do escopo do serviço.
6. Menciona o que muda para o painel web (download e CORS) e para parceiros hipotéticos (versão fixada, deprecação), em poucas linhas.
7. Não inventa números de capacidade, latência ou custo; não grava arquivos.
FAIL if qualquer um ocorrer: termina com perguntas e sem contrato; inventa decisores ou aprovações; apresenta suposições como fatos; grava arquivos; ignora o cliente mobile; afirma ter executado algo.
