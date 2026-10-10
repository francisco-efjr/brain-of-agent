---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Aponta o segredo (NPM_TOKEN) em ARG usado para gravar .npmrc e explica que ARG e ENV persistem na camada da imagem (e o .npmrc gravado também fica na camada), portanto não servem para segredo; propõe RUN --mount=type=secret (com docker build --secret) e remoção do .npmrc, ou equivalente.
2. Aponta FROM node:latest sem pin e recomenda tag exata ou digest (com atualização automatizada).
3. Aponta que o contêiner roda como root (não há USER) e recomenda usuário não-root.
4. Aponta apt-get update e apt-get install em RUN separados e recomenda o mesmo RUN.
5. Aponta CMD em forma shell (npm start) e recomenda forma exec.
6. Recomenda multi-stage e .dockerignore (COPY . . traz tudo, inclusive possíveis segredos locais), e menciona HEALTHCHECK ou probes como sugestão, sem tratá-los como erro.
7. Entrega correções concretas (trechos do Dockerfile) e rótulos coerentes (Verificado para o que está no texto).
FAIL if qualquer um ocorrer: diz que ARG é um lugar seguro para segredo; omite o problema do token; afirma ter construído a imagem, rodado docker history, hadolint ou scan; instrui a colocar o token em ENV.
