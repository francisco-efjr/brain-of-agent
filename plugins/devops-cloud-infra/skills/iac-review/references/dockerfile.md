# Dockerfile: checklist de revisão e autoria

Conferido em 2026-10-10 contra as páginas de boas práticas, build secrets e referência do Dockerfile (V-19, V-55) e o cheat sheet da OWASP (V-20). Destilação com redação própria. Conferir flags na versão instalada (`docker version`, `docker buildx version`).

## Checklist DK-nn

| ID | Verificar | Detectar | Sev. | Fonte |
| --- | --- | --- | --- | --- |
| DK-01 | base fixada por digest (`FROM imagem:tag@sha256:...`), com Dependabot ou Docker Scout para atualizar; nunca `latest` | `FROM` sem `@sha256` | Alto | V-19 |
| DK-02 | multi-stage: compiladores, caches e chaves ficam no estágio de build | um só `FROM` com toolchain | Médio | V-19 |
| DK-03 | `apt-get update` e `apt-get install` no mesmo `RUN` (cache velho de `update` instala pacote desatualizado) | `RUN apt-get update` isolado | Médio | V-19 |
| DK-04 | `.dockerignore` presente (exclui `.git`, `.env`, `node_modules`, state, chaves) | `ls .dockerignore` | Médio; Alto se há `COPY . .` e `.env` no contexto | V-19 |
| DK-05 | `USER` não-root no estágio final | ausência de `USER` | Alto em produção | V-19, V-20 |
| DK-06 | `CMD`/`ENTRYPOINT` em forma exec (`["node","server.js"]`): o processo recebe sinais e vira PID 1 | `CMD npm start` | Médio | V-19 |
| DK-07 | `WORKDIR` absoluto; sem `sudo` | `WORKDIR app` | Baixo | V-19 |
| DK-08 | nenhum segredo em `ARG` ou `ENV` (persistem nas camadas; `docker history` os mostra); usar `RUN --mount=type=secret` e `--ssh default` | `ARG .*(TOKEN\|SECRET\|PASSWORD\|KEY)`, `ENV` idem | Crítico | V-55 (a página de boas práticas não trata de segredos; é regra OWASP/geral) |
| DK-09 | `HEALTHCHECK` local ao processo (nunca checa banco ou serviço externo); só o último vale; `HEALTHCHECK NONE` desativa o herdado | leitura | Médio | V-55, V-58 |
| DK-10 | sem `curl \| sh` nem `ADD` de URL sem checksum; pacotes com versão ou lockfile | `curl .*\|`, `ADD http` | Alto | AP-19; Inferido |
| DK-11 | após o build, `docker history --no-trunc <imagem>` não mostra segredo | executar (só com imagem local e autorização) | Crítico se mostra | V-55 (Inferido) |

Padrões do HEALTHCHECK (V-55): `--interval` 30s, `--timeout` 30s, `--start-period` 0s, `--retries` 3, `--start-interval` 5s (Docker Engine 25.0 ou superior). Saída 0 = saudável, 1 = não saudável, 2 = reservado. O binário usado (wget, curl) precisa existir na imagem final; imagens "slim" costumam não ter.

## Exemplo anotado

Entrada:

```dockerfile
FROM node:latest
ARG NPM_TOKEN
ENV NPM_TOKEN=$NPM_TOKEN
COPY . .
RUN apt-get update
RUN apt-get install -y curl
RUN npm install
CMD npm start
```

Achados esperados:

| ID | Sev. | Linha | Evidência | Correção | Rótulo |
| --- | --- | --- | --- | --- | --- |
| IAC-01 | Crítico | 2-3 | token em `ARG` e `ENV` fica nas camadas e no `docker history` | `RUN --mount=type=secret,id=npmrc,target=/root/.npmrc`; tratar o token como exposto se a imagem foi publicada | Verificado |
| IAC-02 | Alto | 1 | `latest` muda sem aviso | tag fixa + digest | Verificado |
| IAC-03 | Alto | (ausente) | sem `USER`: roda como root | `USER node` (a imagem oficial do Node traz o usuário `node`) | Verificado no arquivo; usuário da imagem: Inferido |
| IAC-04 | Médio | 5-6 | `update` e `install` em `RUN` separados | juntar no mesmo `RUN` e limpar listas | Verificado |
| IAC-05 | Médio | 8 | `CMD` em forma shell | `CMD ["node","dist/server.js"]` | Verificado |
| IAC-06 | Médio | 4 | `COPY . .` sem `.dockerignore` visível | criar `.dockerignore` | Inferido (arquivo não recebido) |
| IAC-07 | Médio | (ausente) | sem `HEALTHCHECK` e sem multi-stage | ver versão corrigida | Verificado |

Versão corrigida (tag de exemplo; escolha a LTS que o projeto usa e obtenha o digest real com `docker buildx imagetools inspect node:<tag>`; não invente digest):

```dockerfile
# syntax=docker/dockerfile:1
FROM node:24-bookworm-slim@sha256:<digest-obtido-pelo-comando> AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
COPY . .
RUN npm run build

FROM node:24-bookworm-slim@sha256:<digest-obtido-pelo-comando>
WORKDIR /app
ENV NODE_ENV=production
COPY package.json package-lock.json ./
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci --omit=dev
COPY --from=build --chown=node:node /app/dist ./dist
USER node
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:8080/healthz').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
CMD ["node", "dist/server.js"]
```

Build com segredo (o arquivo `.npmrc` é do usuário e nunca entra na imagem): `docker build --secret id=npmrc,src="$HOME/.npmrc" -t app:teste .` (opções do `--secret`: `id`, `src` ou `env`; no `RUN --mount`: `id`, `target`, `env`; padrão `/run/secrets/<id>`; V-55). Você não roda o build sem o usuário pedir: ele baixa a imagem base e executa o `npm ci`.

## Autoria: perguntas que mudam o resultado

Pergunte só se a resposta muda o arquivo, uma por vez: runtime e versão (lidos de `package.json`, `pyproject.toml`, `go.mod` quando existirem), porta e rota de saúde da aplicação, necessidade de acesso a repositório privado durante o build (`--ssh default`), arquitetura alvo. Sem resposta, escolha o padrão mais conservador e liste a suposição.

## Verificação

- `hadolint Dockerfile` (se instalado) e a saída colada. Hadolint é um linter conhecido de Dockerfile (conhecimento estável; Inferido, não consta em V).
- Cada achado de segredo cita linha e tipo, sem valor.
- Nenhum `docker build` ou `docker run` sem pedido: o que não rodou vai para "não executado".
