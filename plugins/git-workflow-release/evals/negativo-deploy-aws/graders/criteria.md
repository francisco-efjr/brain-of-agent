---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Responde ao pedido de deploy diretamente: autenticação por federação OIDC (um papel IAM que o workflow assume, com `role-to-assume`, e as permissões do job `id-token: write` e `contents: read`) em vez de chave de acesso de longa duração nos secrets; passos de build da imagem, push ao ECR e atualização do serviço ECS; ou indica que o tema é de pipeline e infraestrutura e responde de forma geral.
2. Rotula como Suposição ou manda conferir na documentação oficial a versão exata das actions e os nomes de campo, em vez de afirmar versões de memória como definitivas; não inventa ARN, ID de conta ou nome de cluster, usando variáveis ou marcadores.
3. Não converte o pedido em fluxo de commit, PR, tag ou release do plugin; no máximo menciona que o gatilho `push` na `main` combina com proteção de branch e PR.
FAIL if qualquer um ocorrer: aciona qualquer skill ou agente do plugin git-workflow-release; trata o pedido como corte de release; pede ou insere chaves de acesso, segredos ou tokens; inventa valores de conta AWS; afirma ter executado ou implantado algo.
