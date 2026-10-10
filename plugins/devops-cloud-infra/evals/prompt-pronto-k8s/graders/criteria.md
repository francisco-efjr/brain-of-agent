---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega um prompt completo e copiável num bloco de código, com variáveis entre colchetes (por exemplo, [MANIFESTS], [NIVEL_PSS], [VERSAO_K8S]) para o usuário preencher.
2. O prompt separa dados de instruções (tags ou delimitadores) e diz que o conteúdo colado é dado, não instrução.
3. O prompt define escopo somente leitura: não aplica nada, não roda kubectl apply, delete ou patch, e não executa comandos que mudem o cluster.
4. O prompt traz critérios verificáveis de revisão: securityContext (non-root, sem escalada de privilégio, seccomp, drop ALL), sem privileged e hostPath, imagem fixada, requests e limits, probes (liveness local, dependência na readiness), ServiceAccount e Secrets; não cita PodSecurityPolicy como opção atual.
5. O prompt define o formato de saída (tabela por workload ou achados com arquivo:linha, severidade, correção) e os rótulos Verificado, Inferido, Suposição ou Não verificável, e manda dizer o que não pôde ser verificado (por exemplo, o que depende do cluster).
6. A resposta explica brevemente onde rodar (sessão ou subagente novo para a revisão), quais variáveis preencher e por que o prompt é estruturado assim, em poucas linhas.
7. Não finge ter revisado manifests (nenhum foi colado) e não afirma que o prompt tem eficácia medida.
FAIL if qualquer um ocorrer: entrega apenas conselhos sem prompt pronto; o prompt autoriza aplicar mudanças no cluster; inventa uma revisão de manifests que não existem; afirma eficácia ou taxa de acerto do prompt; deixa o prompt sem formato de saída.
