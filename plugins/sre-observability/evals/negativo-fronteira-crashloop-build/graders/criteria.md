---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final e no transcript:
1. Diagnostica que o erro exec ... no such file or directory num binário que existe indica incompatibilidade de ligação dinâmica (binário Go compilado com cgo e glibc na imagem golang, executado em alpine com musl), ou caminho incorreto, e explica o mecanismo.
2. Propõe correção no Dockerfile: compilar com CGO_ENABLED=0 (binário estático) ou usar uma imagem final compatível com a de build (por exemplo debian slim ou distroless adequada), e conferir o caminho do COPY.
3. Não aciona nenhuma skill nem agente do plugin sre-observability.
4. Não trata como incidente de produção: não abre documento de incidente, não define papéis IC, OL ou CL, não fala de severidade, SLO, burn rate nem postmortem.
5. A resposta é proporcional ao pedido (correção de build), sem checklist de SRE.
FAIL if qualquer um ocorrer: aciona qualquer skill do plugin sre-observability; trata o caso como incidente com papéis, severidade ou postmortem; transforma o pedido em revisão de confiabilidade; não resolve o erro do Dockerfile.
