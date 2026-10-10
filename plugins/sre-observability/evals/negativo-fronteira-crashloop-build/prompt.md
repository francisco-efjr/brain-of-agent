---
name: negativo-fronteira-crashloop-build
description: "Caso negativo de fronteira, verificando que um CrashLoopBackOff em staging causado por Dockerfile multi-stage, sem usuário afetado, é resolvido como problema de build de container sem acionar nenhuma skill do plugin sre-observability, abrir incidente ou criar papéis de IC e OL."
tags: [sre-observability, negativo, fronteira, sobredisparo]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 600
runs: 3
expected_outcome: "Diagnostica o binário ausente ou incompatível (compilado com glibc copiado para alpine com musl, ou caminho do COPY errado) e propõe correção no Dockerfile (CGO_ENABLED=0 ou imagem final compatível); não aciona skill nem agente do plugin sre-observability; não trata como incidente de produção nem cria papéis de incidente."
model: sonnet
---
No cluster de staging, o pod do `worker` entra em CrashLoopBackOff desde que eu mudei o Dockerfile para multi-stage. O `kubectl logs` mostra só `exec /app/worker: no such file or directory`. Não tem usuário afetado, é só o staging. Como eu corrijo o Dockerfile?

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN go build -o /out/worker ./cmd/worker

FROM alpine:3.20
COPY --from=build /out/worker /app/worker
CMD ["/app/worker"]
```
