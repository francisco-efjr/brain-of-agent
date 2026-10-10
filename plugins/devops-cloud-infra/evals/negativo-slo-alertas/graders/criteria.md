---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Responde ao pedido de observabilidade: define SLIs do ponto de vista do usuário (proporção de pedidos concluídos corretamente dentro de um prazo de latência, taxa de erro), janela e denominador, propõe SLOs rotulados como Suposição até a equipe aprovar, e alertas baseados em consumo do orçamento de erro (em vez de só CPU).
2. Não revisa Terraform, Dockerfile, manifests Kubernetes, Helm, GitOps nem workflows de CI e não monta checklist de infraestrutura.
3. Não ativa o modo DEVOPS-COMPLETO e não aciona skills de revisão de IaC, pipeline, Helm/GitOps, segredos, rollout, nuvem, diagnóstico ou deploy do plugin devops-cloud-infra. Se mencionar outro plugin (por exemplo sre-observability) como dono do tema, é só um ponteiro e a resposta ainda ajuda o usuário.
FAIL if qualquer um ocorrer: transforma o pedido em revisão de infraestrutura; aciona as skills de tarefa do plugin devops-cloud-infra; anuncia modo completo; propõe alterar Terraform, manifests ou pipelines sem o usuário ter pedido.
