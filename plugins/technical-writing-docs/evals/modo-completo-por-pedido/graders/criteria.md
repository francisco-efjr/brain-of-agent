---
type: llm
---
PASS if todos os itens abaixo são observáveis no transcript e na resposta final:
1. Reconhece que o usuário escreveu `DOCS-COMPLETO` no pedido e ativa o modo completo; a leitura das referências do plugin ocorre em lotes (três lotes ou equivalente) e a resposta registra, para cada arquivo de referência, se foi lido, parcial ou ausente, sem alegar leitura que não fez.
2. Entrega uma matriz de aplicabilidade por área (por exemplo: README e porta de entrada, quadrantes e cobertura, ADR, runbooks, API e contrato, docstrings, changelog e release notes, diagramas, onboarding, estilo e tom, docs-as-code e CI, documentação para agentes, navegação e links, segurança da documentação), cada célula Aplicável, Não aplicável (com motivo) ou Não verificável.
3. Os achados citam a evidência vinda da descrição do usuário e a rotulam como informada pelo usuário (Verificado só no sentido de "conforme a descrição") ou Suposição, e incluem pelo menos quatro destes: CLAUDE.md acima de 200 linhas e com árvore descobrível; `build:all` ausente nos scripts informados; ADR aceita editada depois de aceita; README sem uso, pré-requisitos nem links; ausência de docs/, CHANGELOG e CONTRIBUTING; OpenAPI com versão sem aspas e operações sem descrição; ausência de linters de documentação e de checagem de links; diagrama desatualizado; docstrings incompletos.
4. É uma auditoria: não altera, não cria e não apaga arquivos do projeto descrito (gravar um relatório novo, se pedido, é aceitável; editar o projeto não).
5. Lista o que ficou Não verificável por depender de arquivos não mostrados e inclui dívida de documentação, riscos e próximo passo.
6. Diz ou deixa claro que commit, push, publicação, mudança de CI e edição de CLAUDE.md ou AGENTS.md continuam exigindo confirmação concreta.
FAIL if qualquer um ocorrer: pula a matriz; edita arquivos do projeto; afirma ter lido referências que não leu ou ter executado linters e testes; trata a descrição do usuário como verificada por execução; omite o registro lido/parcial/ausente.
