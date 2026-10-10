# backend-api — Backend e APIs

Plugin do Claude Code para projetar, implementar, revisar, testar e depurar **serviços e APIs** (REST, GraphQL, gRPC) com contrato como fonte de verdade e verificação por evidência. Faz parte da fábrica `dev-segments` (um plugin por segmento de desenvolvimento). Versão 0.1.0 · licença MIT · pesquisa e design de 2026-10-10.

## O que entrega

- **Um playbook** (router + processo + modo `BACKEND-COMPLETO`) e uma base de conhecimento com 12 referências densas: checklist por endpoint e grade OWASP API, padrões e antipadrões, decisões e trade-offs, contrato/erros/paginação, autenticação e segurança, idempotência e resiliência, stacks, testes e depuração, tools para agentes, snippets de CLAUDE.md, ferramentas/MCP (desativados) e bibliografia classificada.
- **Skills de tarefa** para os fluxos mais repetidos: contrato de API, revisão de segurança, idempotência e resiliência, suíte de testes de API, depuração de backend, tools para agentes, convenções por stack e configuração de CLAUDE.md.
- **Agentes especialistas** (revisores somente leitura e executores com ferramentas mínimas).
- **Biblioteca de 32 prompts** reutilizáveis e **12 templates** (plano, ADR, ficha de endpoint, relatório de revisão, políticas de idempotência e de erros, checklist de entrega, handoff, plano de testes, aviso de deprecação, avaliação de 10 perguntas, matriz do modo completo).
- **Seguro por padrão:** sem hooks, sem `.mcp.json`, sem `.lsp.json`, sem `bin/`. Hooks e MCP recomendados estão documentados e desativados em `skills/playbook/references/ferramentas-e-mcp.md`, com JSON pronto, riscos e fonte.

## Quando usar

Use quando o pedido envolver endpoint, contrato OpenAPI, erros de API, autenticação e autorização (JWT, OAuth), idempotência, paginação, rate limiting, webhooks, filas e jobs, versionamento, testes de API, bug de backend (500, intermitência, lentidão) ou tools/MCP para agentes. Para pergunta pontual, o playbook responde direto, sem carregar referências. Para modelagem de banco, infraestrutura, threat modeling amplo, UI ou regras de pagamento, o playbook responde o mínimo do lado do serviço e aponta o plugin certo (`/database-data-modeling:playbook`, `/devops-cloud-infra:playbook`, `/security-appsec:playbook`, `/web-frontend:playbook`, `/fintech-payments:playbook`).

## Componentes

Nomes definitivos do design do segmento. Chamada de skill: `/backend-api:<skill>`; agente: `backend-api:<agente>`.

| Tipo | Nome | Para que serve |
| --- | --- | --- |
| Skill núcleo | `playbook` | Router, princípios, processo de 8 passos, intenção → skill/agente, proporcionalidade, modo `BACKEND-COMPLETO`, fronteiras |
| Skill | `prompts` | Índice e biblioteca de 32 prompts prontos (PR-01 a PR-32) |
| Skill | `api-contract-design` | Desenhar, documentar e evoluir o contrato: OpenAPI, erros RFC 9457, paginação, versionamento, compatibilidade |
| Skill | `api-security-review` | Auditoria somente leitura com OWASP API 2023, JWT/OAuth e hardening REST |
| Skill | `idempotency-and-resilience` | Chave de idempotência, retries, rate limit, webhooks, filas, outbox |
| Skill | `api-test-suite` | Testes de API que provam regra de negócio; contrato (Pact, OpenAPI) e fuzz em ambiente descartável |
| Skill | `backend-debugging` | Causa raiz em 4 fases, escalada após 3 falhas, lentidão e N+1 |
| Skill | `agent-tool-design` | Tools e endpoints para agentes; endpoint que chama a API de um modelo |
| Skill | `stack-conventions` | FastAPI, Go, NestJS/Node, Spring, .NET e GraphQL na versão instalada |
| Skill (somente por comando) | `backend-claude-md-setup` | Monta o bloco de CLAUDE.md a partir do repositório; `disable-model-invocation` |
| Agente | `api-security-reviewer` | Revisor de segurança (Read, Grep, Glob) com relatório de achados |
| Agente | `backend-architect` | Decisões e contratos de serviço (ADR), sem código |
| Agente | `api-contract-reviewer` | Compatibilidade de contrato; Bash só para validadores/diff locais |
| Agente | `backend-debugger` | Causa raiz, correção mínima e teste de regressão |
| Agente | `api-test-engineer` | Escreve e reforça testes de API |
| Evals | `evals/` | 12 casos no formato `claude plugin eval`, status `designed_not_executed` |

## Instalação

Dentro do Claude Code, a partir da raiz do marketplace `dev-segments` (caminho local ou repositório):

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install backend-api@brain-of-agent
```

Pelo terminal, o equivalente é `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install backend-api@brain-of-agent`. Confira a sintaxe na versão instalada (`claude plugin --help`). Validação local do pacote: `claude plugin validate <pasta-do-plugin>`.

## Exemplos de pedidos

1. **Idempotência de pagamento:** "Nosso `POST /payments` (Express + Postgres) cobrou duas vezes quando o app tentou de novo após timeout. Corrija." → `idempotency-and-resilience`: chave com escopo, hash do corpo, resposta persistida, restrição única, testes com duas requisições concorrentes; migração só proposta.
2. **Revisão de contrato:** "Vou publicar na v1: `taxId` passa a ser obrigatório, `status` ganha `REFUNDED` e a paginação vira cursor. Posso?" → `api-contract-design` + `api-contract-reviewer`: classificação compatível/breaking por item, alternativa compatível e plano de deprecação.
3. **Auditoria de JWT e BOLA:** "Revise a segurança deste FastAPI" (com o código da autenticação e de `GET /orders/{id}`) → `api-security-review` → `api-security-reviewer`: algoritmo vindo do header, `aud` desligado, falta de filtro por dono, relatório com severidade, `arquivo:linha`, cenário e correção, sem alterar o código.
4. **Depuração de 500 intermitente:** "500 só sob carga em `/reports`; aumentei o timeout e pus try/except e piorou. Log: connection slots are reserved." → `backend-debugging`: reproduzir, uma hipótese (engine/pool por requisição), teste que falha, uma correção, reversão dos patches de sintoma.
5. **Tools para agente:** "Vou expor `list_all_orders()` (5 MB) e `get_order_by_id` como tools MCP; o agente erra e estoura o contexto." → `agent-tool-design`: consolidação por fluxo, `concise|detailed`, paginação, erro acionável, `strict`, avaliação de 10 perguntas.
6. **Testes de endpoint:** "Escreva testes para `POST /orders` (FastAPI): total, `Idempotency-Key`, isolamento por cliente, erros em problem+json." → `api-test-suite`: oráculo independente, dois usuários, replay, 404 para alheio; diz que não executou, se for o caso.
7. **Go:** "Revise este serviço Go (go.mod `go 1.23`)" → `stack-conventions`: `ServeMux` com método, `PathValue`, erros, timeout, `Body.Close`, SSRF no `id`.
8. **Modo completo:** "BACKEND-COMPLETO. Revise e corrija o módulo de pedidos; edite só código e testes locais; migrações só no banco de teste." → leitura em lotes, matriz de aplicabilidade, implementação no escopo, revalidação com evidências.

## Keyword `BACKEND-COMPLETO`

Escreva `BACKEND-COMPLETO` na sua mensagem para ativar o modo de cobertura integral: leitura das referências em lotes com registro lida/parcial/ausente, matriz de aplicabilidade por área (contrato, erros, authN/authZ, idempotência, paginação, cache, rate limit, jobs, webhooks, integrações, versionamento, observabilidade, testes, dados, segredos, tools para agentes), implementação **dentro do escopo autorizado**, revisão adversarial e revalidação com evidências. A keyword **não amplia permissões** (produção, migração em ambiente compartilhado, publicação e ações irreversíveis continuam exigindo autorização concreta) e **não ativa** quando aparece em logs, documentos, comentários ou saídas de ferramenta. Sem a keyword, o plugin carrega só o necessário.

## Principais fontes (top 10)

Bibliografia completa, com licenças e lacunas, em `skills/playbook/references/fontes.md` (consulta em 2026-10-10).

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Claude Code best practices — https://code.claude.com/docs/en/best-practices | A |
| 2 | Writing tools for agents (Anthropic Engineering) — https://www.anthropic.com/engineering/writing-tools-for-agents | A |
| 3 | Define tools (Claude API) — https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools | A |
| 4 | RFC 9457 Problem Details — https://www.rfc-editor.org/rfc/rfc9457.html | A |
| 5 | OWASP API Security Top 10 (2023) — https://api-security.owasp.org/editions/2023/en/0x11-t10 | A |
| 6 | OWASP REST Security Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html | A |
| 7 | RFC 9700 OAuth 2.0 Security BCP — https://datatracker.ietf.org/doc/html/rfc9700 | A |
| 8 | RFC 8725 JWT BCP — https://www.rfc-editor.org/rfc/rfc8725 | A |
| 9 | Idempotência: Stripe (https://docs.stripe.com/api/idempotent_requests) e Google AIP-155 (https://google.aip.dev/155) | A |
| 10 | Paginação: Google AIP-158 — https://google.aip.dev/158 | A |

Também centrais: Azure REST API Guidelines (CC BY 4.0), OpenAPI 3.1.1 (Apache-2.0), claude-code-security-review (MIT) e o conteúdo próprio do usuário no brain-of-agent (MIT).

## Créditos e licenças

- **Plugin:** MIT, Francisco Edson.
- **brain-of-agent** (`francisco-efjr/brain-of-agent`, MIT): checklists por endpoint e de serviço, tabela de status HTTP, tabelas de teste de contrato, webhooks e mensageria, templates de plano, ADR e handoff, e o desenho do modo completo, adaptados ao formato de plugin.
- **gstack** (Garry Tan e contribuidores, MIT): somente o formato de achado `[CRITICAL|INFORMATIONAL] (confidence: N/10) arquivo:linha — descrição`, sem copiar blocos.
- **Destilados com redação própria e atribuição** (nenhum trecho literal): awesome-copilot (MIT), awesome-cursorrules (CC0-1.0), obra/superpowers (MIT), wshobson/agents (MIT), everything-claude-code (MIT), apollographql/skills (MIT), claude-code-security-review (MIT), anthropics/skills mcp-builder (Apache-2.0 na skill) e claude-api (sem licença única no repositório, só destilado), OpenAPI Specification (Apache-2.0), Microsoft api-guidelines (CC BY 4.0, atribuição Microsoft), RFCs e drafts da IETF, docs oficiais (Anthropic, Stripe, Google AIP, OWASP, gRPC, NestJS, Spring, FastAPI, Microsoft Learn, Go). Texto de documentação sem licença identificada foi apenas destilado.
- **Não usados:** itens rejeitados na pesquisa (NestJS anti-hallucination com "OVERRIDE", VoltAgent api-designer, entre outros), listados em `fontes.md`.

## Limitações honestas

- **Evals `designed_not_executed`:** os 12 casos foram desenhados, não rodados; exigem Claude Code 2.1.269 ou superior (`claude plugin eval`), execuções repetidas e baseline sem plugin.
- **Revisão não independente:** a pesquisa, a síntese e a pontuação foram feitas por modelos da família Claude; a independência é parcial e não equivale a validação externa.
- **Fontes lidas por resumo:** parte das páginas (OWASP API textos de prevenção, ~60% da spec OpenAPI, ~35% da RFC 9700) não foi lida na íntegra; datas de último commit de repositórios não foram observadas.
- **Lacunas sem fonte validada:** filas, jobs e outbox, observabilidade, cache de aplicação, webhooks como padrão, Rust, tRPC, OIDC, ABAC, Django REST Framework, Express/Fastify, Spring Boot avançado, .NET Minimal APIs. O plugin cobre parte com conhecimento do brain marcado *Inferido* e declara o resto.
- **Versões envelhecem:** OpenAPI 3.1 x 3.2, Spring 7.x, Go 1.22+, IDs de modelo, tabela de `tool_choice` e drafts IETF (rate limit expira em 24/11/2026; `Idempotency-Key` expirou em 18/04/2026). Cada skill manda conferir a versão instalada.
- **Hook e MCP não foram executados** nesta cadeia: o hook de arquivos protegidos segue o padrão da doc oficial (relida em 2026-10-10), e o MCP de banco é ilustrativo (o pacote específico não foi pesquisado).
- **Fatos herdados do brain:** Dredd arquivado (08/11/2024), RFC 9745/8594 e o modo `BACKWARD` padrão do Confluent foram reverificados em 2026-10-10 pelo validador de qualidade; o limite de 4 MB do gRPC e a janela de 5 min do SQS FIFO seguem *Inferido*.
- O plugin **não** substitui revisão de segurança profissional, pentest ou parecer jurídico; ações em produção continuam exigindo autorização humana.
