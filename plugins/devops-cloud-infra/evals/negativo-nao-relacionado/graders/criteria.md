---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Entrega uma função Python que valida CPF (cálculo dos dois dígitos verificadores, rejeição de sequências de dígitos repetidos, aceita entrada com e sem pontuação) e testes em pytest que cobrem CPF válido, inválido, repetido e formatado.
2. Não aciona nenhuma skill do plugin devops-cloud-infra e não carrega o playbook.
3. A resposta é proporcional ao pedido e não menciona Terraform, Kubernetes, Docker, CI/CD, deploy, rollback nem DEVOPS-COMPLETO.
FAIL if qualquer um ocorrer: aciona skill ou agente do plugin; menciona infraestrutura, pipeline ou deploy sem o usuário ter pedido; transforma o pedido em revisão de infraestrutura ou em checklist de DevOps; anuncia modo completo.
