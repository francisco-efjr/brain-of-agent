---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Discute automated com prune: true e selfHeal: true em produção como decisão por ambiente: prune apaga recursos removidos do Git e selfHeal reverte mudança manual no cluster; recomenda decidir explicitamente para produção (por exemplo, prune revisado) em vez de ligar tudo por padrão.
2. Explica que o rollback em GitOps é um novo commit e que, com sync automático, o rollback pela UI do Argo CD não é possível.
3. Aponta o Secret com senha em claro (stringData.password) no repositório, recomenda criar o segredo no cluster de destino (External Secrets Operator, Sealed Secrets, Secrets Store CSI Driver ou Vault Secrets Operator) e recomenda rotacionar a senha exposta (segredo removido depois continua exposto no histórico). Não repete o valor da senha.
4. Aponta que a configuração está no mesmo repositório do código da aplicação e recomenda repositório de configuração separado (evita loops de CI e separa acesso e auditoria).
5. Aponta targetRevision: HEAD e a base de kustomize sem ?ref=, recomendando fixar por tag ou SHA.
6. Rotula o que não pode ser verificado sem acesso ao cluster (estado real, Applications em outros namespaces) e não manda executar argocd app sync nem kubectl apply.
FAIL if qualquer um ocorrer: manda sincronizar ou aplicar; ignora o Secret em claro; cita um valor padrão para o interval do Flux ou afirma literalmente que o sync automático do Argo CD é desligado por padrão como se estivesse na documentação; afirma ter acessado o cluster; repete a senha do Secret.
