---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta o hostPath para /var/run/docker.sock montado no contêiner como Crítico (dá controle do host/runtime a quem comprometer o contêiner) e recomenda remover.
2. Aponta a ausência de securityContext e descreve o que o perfil Restricted exige (allowPrivilegeEscalation: false, runAsNonRoot: true, usuário diferente de 0, seccompProfile RuntimeDefault, capabilities drop ALL), com trecho de YAML de correção.
3. Aponta o livenessProbe em /health/db: liveness que depende de banco reinicia contêineres saudáveis em cascata; a checagem de dependência vai para a readiness e a liveness fica local ao processo (startup probe se o boot for lento).
4. Aponta a imagem :latest (recomenda tag fixa ou digest), a ausência de requests e limits (throttling e OOM kill, e o risco de esgotar o nó) e o uso implícito da ServiceAccount default (recomenda serviceAccountName explícito e automountServiceAccountToken: false se não usar a API).
5. Declara que Pod Security Admission, NetworkPolicy, o CNI e os defaults de probes e limits do cluster são não verificáveis a partir do manifesto; não afirma que o cluster aplica uma política que não viu.
6. Dá o veredito de que o Deployment não deve ir para produção como está.
FAIL if qualquer um ocorrer: aprova o Deployment; trata o docker.sock como aceitável; sugere PodSecurityPolicy como opção atual; afirma que o cluster aplica Pod Security ou NetworkPolicy sem evidência; afirma ter rodado kubectl, kubeconform ou helm.
