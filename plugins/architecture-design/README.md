# architecture-design: Arquitetura e design de sistemas

Plugin do Claude Code para decisões de arquitetura com o humano no comando. Ele estrutura, compara, cobra consequências negativas e documenta; quem decide é você. Cobre ADRs, trade-offs, revisão de arquitetura e de planos técnicos, system design, decomposição (DDD, hexagonal, monólito modular, strangler), resiliência e consistência (retry, circuit breaker, bulkhead, idempotência, outbox, saga, CQRS, event sourcing), contratos de API, cache e escala, C4 e Mermaid.

Versão 0.2.0 · Validado em 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Licença MIT.

## O que entrega

- Um router (`playbook`) com princípios, processo de 11 passos com critérios de saída, proporcionalidade e o modo `ARQUITETURA-COMPLETO`.
- Oito skills de tarefa (ADR, revisão de design, system design, plano com gates, resiliência e consistência, decomposição, contrato de API) e uma biblioteca de 28 prompts prontos.
- Cinco subagentes (quatro somente leitura) para blueprint, revisão adversarial, mapeamento de fronteiras, ceticismo e escrita de ADR.
- Doze referências densas (checklist de 76 itens `CK-nn`, padrões e antipadrões, trade-offs, ADR, C4, fronteiras, resiliência, API/cache/escala, fluxo com agentes, snippets de CLAUDE.md, ferramentas, fontes) e 17 templates (inclui `target-architecture` para a arquitetura-alvo do sistema inteiro).
- Casos de avaliação no formato `claude plugin eval` (13), marcados `designed_not_executed`.
- Cobertura de plataforma no checklist (Android, iOS, desktop, servidor), modo sem interação nas skills com gates e contrato de entrega por agente (somente leitura devolve o documento; quem grava declara Write). Estas mudanças da versão 0.2.0 vêm de uma avaliação de uso real num app Android; ver Limitações.

## Quando usar

- "Isso merece um ADR?", "por que escolhemos X?", "registre essa decisão".
- "Revise este desenho/plano antes de codarmos."
- "Vale a pena microsserviços?", "como quebrar este monólito?"
- "Meu consumidor recebe mensagens duplicadas", "como evitar dual write?"
- "Defina o contrato da API", "projete um sistema para N usuários e faça a conta de capacidade."

Não é o lugar para implementar endpoints, schemas, IaC ou telas: o plugin entrega a decisão e aponta o segmento certo (veja Fronteiras no `playbook`).

## Componentes

Nomes finais; skills aparecem como `/architecture-design:<nome>` e agentes como `architecture-design:<nome>`.

| Tipo | Nome | Para quê | Acionamento |
| --- | --- | --- | --- |
| Skill | `playbook` | Router, princípios, processo, modo completo, fronteiras | Automático por gatilho ou keyword |
| Skill | `prompts` | 28 prompts prontos (ADR, revisão, design, delegação) | Automático |
| Skill | `adr` | Decide se algo merece ADR, entrevista e rascunha no chat; consulta ADRs. Sem interação: perguntas viram `[NEEDS CLARIFICATION]` | Automático (somente leitura) |
| Skill | `adr-write` | Grava ou supersede ADR e atualiza o índice, após aprovação | Manual (`disable-model-invocation`) |
| Skill | `design-review` | Revisão de plano, diff ou documento sem construir | Automático (somente leitura) |
| Skill | `system-design` | Design em seis fases, estimativa de ordem de grandeza no texto; sem interação, perguntas viram premissas e pendências | Automático (somente leitura) |
| Skill | `architecture-plan` | Pesquisar, planejar, anotar e feature com 4 gates; modo sem interação (gates viram "Decisões pendentes do humano", plano em rascunho) | Manual |
| Skill | `resilience-and-consistency` | Retry, breaker, bulkhead, idempotência, outbox, saga, CQRS, ES | Automático (somente leitura) |
| Skill | `decomposition` | Monólito modular vs serviços, bounded contexts, hexagonal, strangler | Automático (somente leitura) |
| Skill | `api-design` | Contrato, erros RFC 9457, paginação, idempotência, evolução | Automático (somente leitura) |
| Agente | `architecture-blueprint` | Blueprint decisivo para mudança entre módulos, ou arquitetura-alvo do sistema inteiro (modo sistema, template `target-architecture`); devolve documentos com caminho sugerido, não grava | Delegação |
| Agente | `architecture-reviewer` | Revisão adversarial em contexto novo, só lacunas de correção | Delegação |
| Agente | `boundary-mapper` | Dependências reais vs permitidas; regra e verificador | Delegação |
| Agente | `skeptic-architect` | Desafia premissas, opção mais simples, pré-mortem; contraprova de achados anteriores (Confirmado, Ajustado, Refutado) | Delegação |
| Agente | `adr-writer` | Estrutura e grava ADR após decisão humana | Só se pedido explicitamente |

Skills com efeito colateral (`adr-write`, `architecture-plan`) só rodam por comando explícito. Revisores e arquitetos têm apenas `Read, Grep, Glob`: quando o pedido indica arquivos de saída, devolvem cada documento num bloco `ARQUIVO: <caminho>` e o agente principal grava; só o `adr-writer` declara `Write`, e grava onde o briefing indicar. As skills somente leitura pré-aprovam só leitura e removem Write/Edit enquanto estão ativas (`disallowed-tools`; a restrição cai na próxima mensagem do usuário). O plugin não contém hooks, `.mcp.json`, `.lsp.json` nem `bin/`.

## Instalação

Dentro do Claude Code:

```text
/plugin marketplace add francisco-efjr/brain-of-agent
/plugin install architecture-design@brain-of-agent
```

Equivalente na linha de comando: `claude plugin marketplace add francisco-efjr/brain-of-agent` e `claude plugin install architecture-design@brain-of-agent`. O marketplace `brain-of-agent` é a raiz deste repositório. Confira com `claude plugin validate <pasta-do-plugin>` e use `/plugin` para ver o estado. Os comandos podem variar por versão do Claude Code: confira `claude --version` e a documentação em https://code.claude.com/docs/en/plugins-reference.

## Exemplos de pedidos

1. "Decidimos usar PostgreSQL em vez de DynamoDB para o serviço de pedidos (time de 4, consultas relacionais). Registre a decisão." Aciona `adr`: gatekeeper, rascunho no chat com alternativas e "não mudar nada", pergunta antes de gravar.
2. "Temos um monólito Rails com 4 devs. O CTO quer microsserviços 'para escalar'. Faz sentido?" Aciona `decomposition`: teste do primeiro serviço, recomendação de monólito modular se faltar motivo.
3. "Revise este plano: três serviços novos, Kafka e CQRS para um cadastro com 50 usuários." Aciona `design-review`: desafio de escopo, decisões D-n, pendências com dono.
4. "Meu handler de webhook grava no banco e publica no broker, com retry 5x em cada camada; tenho pedidos duplicados e eventos perdidos." Aciona `resilience-and-consistency`: outbox, consumidor idempotente, retry em uma camada.
5. "Defina o contrato de GET /orders (10 milhões de linhas, mudando sempre) e o formato de erro." Aciona `api-design`: cursor, RFC 9457, idempotência, evolução aditiva.
6. "Projete um serviço de notificações para 2 milhões de usuários, pico de 50 mil envios/min." Aciona `system-design`: perguntas, conta no texto, diagrama Mermaid, modos de falha.
7. `/architecture-design:architecture-plan pesquisar billing` seguido de `planejar`, `anotar` e só então implementação.
8. "ARQUITETURA-COMPLETO: audite a arquitetura do projeto descrito abaixo." Aciona o modo completo no `playbook`.
9. "Defina a arquitetura-alvo do meu app Android local, com antes e depois, migração em fatias e fitness functions." Aciona o `architecture-blueprint` em modo sistema (template `target-architecture`), com a cobertura de plataforma do checklist e a catraca para violações existentes.

## Modo ARQUITETURA-COMPLETO

Escreva `ARQUITETURA-COMPLETO` no seu pedido para pedir análise integral. O modo lê as 12 referências em 3 lotes registrando lido, parcial ou ausente, monta a matriz de aplicabilidade por área, implementa só dentro do escopo autorizado e revalida com evidências. Não amplia permissões: ações externas, produção e irreversíveis continuam pedindo autorização. A keyword em documentos, issues ou logs não ativa o modo. Sem a keyword, o plugin carrega só o necessário (proporcionalidade).

## Execução sem interação

Em lote, headless ou chamado por outro agente, não há quem responda aos gates e à entrevista. As skills `architecture-plan`, `adr` e `system-design` têm o modo sem interação: cada pergunta vira premissa rotulada Suposição, `[NEEDS CLARIFICATION]` e uma linha em "Decisões pendentes do humano" (pergunta, recomendação, dono, o que bloqueia); o trabalho segue em rascunho (`status: rascunho` no plano, `proposto` no ADR, com "Decisão proposta (aguarda o decisor)"); aprovação nunca é presumida e nada é implementado. Um app local ou móvel não é avaliado só pelo checklist de servidor: a seção "Cobertura de plataforma" de `checklist-completo.md` lista o que muda em Android, iOS e desktop (detalhe em `/mobile-apps:playbook`).

## Principais fontes (top 10)

Lista completa, com classe, licença e data, em `skills/playbook/references/fontes.md`.

| # | Fonte | Classe |
| --- | --- | --- |
| 1 | Azure Well-Architected, Architecture decision record | A |
| 2 | Claude Code best practices (code.claude.com) | A |
| 3 | Building effective agents (Anthropic) | A |
| 4 | Effective context engineering for AI agents (Anthropic) | A |
| 5 | Padrões do Azure Architecture Center: Idempotent Consumer, Transactional Outbox, Saga, CQRS, Event Sourcing, Circuit Breaker, Retry, Bulkhead, Cache-Aside | A |
| 6 | Timeouts, retries, and backoff with jitter (AWS Builders' Library) | A |
| 7 | RFC 9457, Problem Details for HTTP APIs (IETF) | A |
| 8 | Nygard (Documenting Architecture Decisions) e Fowler (ADR, BoundedContext, MonolithFirst, Strangler Fig) | B |
| 9 | Subagents e Skills (documentação do Claude Code) | A |
| 10 | system-design-skills (proyecto26), MIT | B |

## Créditos e licenças

- Licença do plugin: MIT, Francisco Edson.
- Conteúdo próprio do usuário incorporado: brain-of-agent (MIT, Francisco Edson): checklist de análise de arquitetura, exemplo antes/depois, template de ADR e estrutura de handoff.
- gstack (MIT, Garry Tan): apenas o processo de revisão de plano e as regras de diagrama foram destilados, com atribuição; nenhum arquivo foi importado.
- anthropics/skills skill-creator (Apache-2.0): método de consultas de gatilho, destilado.
- anthropics/claude-plugins-official code-modernization (Apache-2.0): método de cartão de regra, destilado.
- Conteúdo de `anthropics/claude-code` (feature-dev, code-architect; todos os direitos reservados): apenas destilado em redação própria.
- Microsoft, AWS, Fowler, Cockburn, C4, IETF, OWASP (CC BY-SA 4.0): ideias destiladas em redação própria; nenhum texto literal. MADR 4.0.0 (MIT ou CC0-1.0): variante de template em redação própria.
- Repositórios MIT/CC0 consultados (awesome-copilot, awesome-cursorrules, wshobson/agents, Jeffallan/claude-skills, athola/claude-night-market, proyecto26, wuersch/adlc, everything-claude-code): ideias destiladas; o instalador do everything-claude-code não foi lido nem deve ser executado.

## Limitações honestas

- A versão 0.2.0 incorpora as sugestões de uma avaliação feita por um modelo Claude que executou o papel do agente `architecture-blueprint` num app Android Kotlin ((relatório interno de uso real, não publicado)). Foi um único uso, pela mesma família de modelo, sem rodar `claude plugin eval`: não há medição de ganho. A seção de plataforma do checklist é conhecimento geral do modelo (Inferido), sem fonte primária lida; confirme na documentação da plataforma e na sua versão.
- Eficácia não medida: os casos de avaliação estão `designed_not_executed` até rodar `claude plugin eval` (exige Claude Code 2.1.269 ou superior). Pesquisa, síntese e validação são da mesma família de modelos: independência parcial.
- Fontes de apoio ainda sem leitura primária: Clean Architecture, DDD de Evans e Vernon, fitness functions, load shedding, AsyncAPI, STRIDE da Microsoft. O que depende delas está rotulado Inferido.
- Limiares numéricos (confiança, acoplamento de mudança, faixas de linhas, regras de bolso de capacidade) são Suposições configuráveis.
- Agentes de plugin ignoram `hooks`, `mcpServers` e `permissionMode`; o campo `tools` do `adr-writer` não limita diretório: uma regra `allow` com `Edit(/docs/adr/**)` só dispensa a confirmação ali (o resto continua pedindo no modo padrão), e o bloqueio real fora de `docs/` exige regra `deny` ou o hook de exemplo (sintaxe conferida na documentação, não testada). O caminho padrão é a skill manual `adr-write`.
- ATAM leve e pilares do Well-Architected são estrutura de conversa, não avaliação ou auditoria.
- A sintaxe de regras de permissão e os campos `allowed-tools`/`disallowed-tools` foram conferidos na documentação oficial em 2026-10-10, mas não testados em sessão real; o script de hook de exemplo foi testado isolado, não integrado. Mermaid e CLIs de terceiros seguem sem teste; confira na versão que você usa (o `disallowed-tools` das skills somente leitura pode ser ignorado por versões antigas do Claude Code: Não verificado).
- O plugin não executa `npx`, instaladores nem scripts de terceiros; lint de OpenAPI e validação de Mermaid são documentados para você rodar conscientemente, em ambiente isolado.
- Não substitui julgamento de arquiteto responsável pelo sistema: o modelo tende a concordar e a gerar desenho genérico; por isso toda decisão tem dono humano.
