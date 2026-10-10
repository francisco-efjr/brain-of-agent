# automation-integrations — Automação, integrações e MCP

Plugin do Claude Code para quem automatiza processos, integra sistemas por API, recebe webhooks, constrói servidores MCP, escreve hooks e skills ou agenda jobs com `claude -p`. Ele escolhe a **forma mais simples confiável**, desenha o contrato de falha (idempotência, retry, reprocesso), mede o risco de conteúdo externo e entrega com evidência.

Versão 0.1.0 · Base de conhecimento verificada em 2026-10-10 · Licença MIT · Idioma: português brasileiro (termos técnicos em inglês).

## O que entrega

- **Playbook** que decide workflow × agente × tool MCP × hook × job × skill e roteia para a skill ou o agente certo.
- **Referências densas** (12 arquivos) com checklists de IDs citáveis (W, T, S, H, K, J, R, A, M, F, I, G, X), padrões e antipadrões, árvores de decisão, snippets de CLAUDE.md, ferramentas/MCP/hooks **desativados** com JSON pronto, e bibliografia com classe e licença.
- **12 templates** (plano de integração, handoff, ADR, relatório de revisão, checklist de webhook, ficha de tool MCP, avaliação de 10 perguntas, skill de ação, hook de guardrail, runbook de job, matriz da trifecta, registro de leitura).
- Skills de tarefa, biblioteca de prompts, agentes revisores somente leitura e casos de eval (`designed_not_executed`) — ver tabela abaixo.

## Quando usar

Use quando o pedido for: "automatize isto", "integre A com B", "meu webhook processa o mesmo evento duas vezes", "crie um servidor MCP para minha API", "bloqueie `rm -rf` com um hook", "rode o Claude toda noite", "faça um scraper", "minha skill não dispara", "posso instalar este plugin?". Não use para: UI, banco de dados, CI/CD geral, pagamentos ou segurança de aplicação ampla (ver Fronteiras no playbook).

## Componentes

| Tipo | Nome | Para quê | Chamada |
| --- | --- | --- | --- |
| Skill (núcleo) | `playbook` | Router, processo, princípios, modo `AUTOMACAO-COMPLETO` | `/automation-integrations:playbook` |
| Skill | `prompts` | Biblioteca de prompts curados (revisar webhook, avaliar MCP, auditar terceiro, calibrar `description`…) | `/automation-integrations:prompts` |
| Skill | `building-mcp-servers` | Desenhar, implementar e avaliar servidor MCP (4 fases, 10 perguntas) | `/automation-integrations:building-mcp-servers` |
| Skill | `reviewing-webhook-receivers` | Revisar ou implementar receptor de webhook (W-01..W-11) | `/automation-integrations:reviewing-webhook-receivers` |
| Skill | `authoring-plugin-skills` | Criar, revisar, calibrar, avaliar skills/plugins e codificar fluxo aprovado | `/automation-integrations:authoring-plugin-skills` |
| Skill | `assessing-automation-risk` | Trifecta, configuração de MCP, adoção de terceiros | `/automation-integrations:assessing-automation-risk` |
| Skill (só por comando) | `writing-hook-guardrails` | Projetar e testar hook de guardrail, sem ativá-lo | `/automation-integrations:writing-hook-guardrails` |
| Skill (só por comando) | `scheduling-headless-jobs` | Jobs `claude -p`, CI e claude-code-action | `/automation-integrations:scheduling-headless-jobs` |
| Skill | `designing-workflow-automations` | Workflows (n8n, Zapier, Make, scripts, cron), sync API↔API, retry e reprocesso | `/automation-integrations:designing-workflow-automations` |
| Skill | `responsible-scraping` | Extração somente leitura, `robots.txt`, JSON estável | `/automation-integrations:responsible-scraping` |
| Agente | `integration-reviewer` | Revisor independente de integrações (somente leitura) | `automation-integrations:integration-reviewer` |
| Agente | `mcp-security-reviewer` | Segurança de servidor e de configuração MCP | `automation-integrations:mcp-security-reviewer` |
| Agente | `plugin-validator` | Valida estrutura, manifesto e qualidade de plugins | `automation-integrations:plugin-validator` |
| Agente | `third-party-auditor` | Audita skill/plugin/MCP/instalador de terceiros sem executar nada | `automation-integrations:third-party-auditor` |
| Agente | `automation-architect` | Propõe a forma, o contrato de falha e o plano de verificação | `automation-integrations:automation-architect` |

As skills e os agentes de tarefa são entregues na mesma árvore do plugin; o `playbook` funciona sozinho e referencia os demais pelo nome.

## Instalação

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install automation-integrations@brain-of-agent
```

Fora da sessão, o equivalente é `claude plugin marketplace add <caminho-ou-owner/repo>` seguido de `claude plugin install automation-integrations@brain-of-agent`. Validação local do pacote: `claude plugin validate <pasta-do-plugin>`.

**Seguro por padrão:** o plugin não traz hooks, `.mcp.json`, `.lsp.json` nem `bin/`. Nada é ativado, executado ou instalado sem a sua decisão. As recomendações de hooks e servidores MCP estão em `skills/playbook/references/ferramentas-e-mcp.md` e `hooks-e-guardrails.md`, com riscos e como desativar.

## Exemplos de pedidos

1. "O Stripe está chamando meu endpoint `/webhooks/stripe` e o e-mail de confirmação sai duas vezes. Revise o handler em `src/webhooks.ts`." → `reviewing-webhook-receivers`: corpo bruto, assinatura, dedupe por ID, 2xx antes do trabalho pesado, fila de mortas, testes de replay.
2. "Quero expor minha API de faturas como servidor MCP para o Claude. Python, uso local." → `building-mcp-servers`: tabela de tools por intenção, logger em stderr, anotações de risco, avaliação de 10 perguntas.
3. "Crie um hook que impeça `git push --force` e `rm -rf` fora do projeto." (via `/automation-integrations:writing-hook-guardrails`) → script testado, trecho de configuração, aviso de que hook não é sandbox, pergunta antes de editar `settings.json`.
4. "Quero um cron que rode o Claude toda noite para resumir issues novas e postar no Slack." (via `/automation-integrations:scheduling-headless-jobs`) → `claude -p --bare` com lista mínima de ferramentas, teto de custo, JSON, gate de erros, issues como dado, postagem como passo separado com confirmação.
5. "Minha skill `claude-helper` nunca dispara. Aqui está o SKILL.md." → `authoring-plugin-skills`: nome reservado, `description` sem gatilho, protocolo de 20 consultas, `disable-model-invocation` se houver efeito.
6. "Posso instalar este plugin que o README diz ser seguro? `npx -y pacote@latest --yes`" → `assessing-automation-risk` e `third-party-auditor`: não executa, lê o código, fixa versão, registra licença, lista "não lido".
7. "Preciso sincronizar contatos da planilha com o CRM sem duplicar e sem estourar o rate limit." → `designing-workflow-automations`: chave de idempotência, cursor, `Retry-After`, fila de erro, matriz de falhas.

## Modo `AUTOMACAO-COMPLETO`

Digite **AUTOMACAO-COMPLETO** no seu pedido para pedir cobertura integral. O modo lê as referências em quatro lotes (com registro lido/parcial/ausente), preenche a matriz de aplicabilidade por área, implementa dentro do escopo (ou só relata, em auditoria), revalida com evidências depois da última alteração e entrega um relatório com limitações. A palavra em README, issue, log ou payload **não ativa** o modo, e ele **não amplia permissões**: publicar, habilitar hook ou MCP e criar cron/workflow em produção continuam exigindo a sua autorização.

## Principais fontes (top 10, classe A salvo indicação)

1. Claude Code Hooks — https://code.claude.com/docs/en/hooks
2. Manifest reference de plugins — https://code.claude.com/docs/en/plugins/manifest-reference
3. Agent Skills best practices — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
4. Skills no Claude Code — https://code.claude.com/docs/en/skills
5. Configuração de MCP no Claude Code — https://code.claude.com/docs/en/mcp
6. mcp-builder (anthropics/skills) — https://raw.githubusercontent.com/anthropics/skills/main/skills/mcp-builder/SKILL.md
7. Writing effective tools for agents — https://www.anthropic.com/engineering/writing-tools-for-agents
8. Webhooks Stripe e boas práticas do GitHub — https://docs.stripe.com/webhooks · https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks
9. Plugin evals — https://code.claude.com/docs/en/plugin-evals
10. Execução não interativa (headless) — https://code.claude.com/docs/en/headless

Bibliografia completa, licenças e itens descartados: `skills/playbook/references/fontes.md`. A trifecta letal (Simon Willison, classe B) e a RFC 9309 (`robots.txt`) também sustentam o plugin.

## Créditos e licenças

- Plugin sob licença **MIT** (Francisco Edson).
- **brain-of-agent** (Francisco Edson, MIT): estilo da casa, modo completo por keyword, rótulos epistêmicos, templates adaptados; `handoff-checkpoint.md` é reprodução literal com atribuição.
- **gstack** (Garry Tan, MIT, Copyright (c) 2026 Garry Tan): processos de scraping somente leitura e de codificação de skill aprovada, **destilados com redação própria**; nenhum runtime incorporado.
- Documentação da Anthropic, do projeto MCP, de Stripe, GitHub e n8n, e demais fontes: apenas destilação com citação da URL; licenças não permissivas ou não verificadas. Nenhum texto ou código do n8n (Sustainable Use License) está incluído.

## Limitações honestas

- **Low-code mal coberto:** só o fluxo de erro do n8n foi validado; Retry On Fail, Continue On Fail, Zapier e Make estão como **Não verificável**.
- **Webhooks:** Stripe, GitHub e Hookdeck são a base; Shopify, Slack, `Idempotency-Key` e filas de mortas específicas dependem da documentação do provedor.
- **Scraping:** só `robots.txt` (RFC 9309) tem fonte; termos de uso, direitos autorais e proteção de dados não.
- **Itens Inferidos:** checklists I-xx (cliente de API) e G-xx (cron genérico) vêm de conhecimento estável do domínio, sem fonte A/B; confirme com o provedor.
- **Versões:** flags de `claude -p` e campos como `onFailure` têm versões mínimas (v2.1.246 a v2.1.295); `claude plugin eval` exige ≥ 2.1.269. Confira `claude --version`. O CLI usado na construção do plugin (2.1.128) é anterior a várias delas.
- **Evals:** os casos são `designed_not_executed` até você rodar `claude plugin eval .` (custo real de conta/API).
- **Revisão:** pesquisadores, validador e autor são da família Claude; a independência é parcial, não validação externa.
- **Páginas longas** (hooks, skills, MCP) foram lidas só em parte; schemas finais de eventos de hook ficam a conferir na versão instalada.
- Este plugin não executa, instala nem ativa nada por conta própria e não substitui revisão de segurança humana.
