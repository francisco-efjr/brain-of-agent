<!--
Consultas de gatilho para medir sub e sobre-disparo das skills do plugin (método do skill-creator da Anthropic,
Apache-2.0, V-07: 20 consultas por skill, 8 a 10 que devem disparar e 8 a 10 limítrofes que não devem; divisão 60/40
treino/teste e 3 execuções por consulta na otimização). Execute com e sem o plugin e compare. As consultas abaixo
são exemplos escritos para este plugin; status: designed_not_executed.
Revise a description da skill ANTES de revisar o corpo.
-->
# Consultas de gatilho

Sumário: adr · design-review · system-design · resilience-and-consistency · decomposition · api-design · playbook · prompts · skills manuais · resumo da medição.

Como usar: para cada skill, rode as 20 consultas em sessão limpa, registre se a skill disparou (ferramenta `Skill` com o nome esperado) e calcule: acertos nas positivas, falsos disparos nas negativas. Meça pelo menos 3 execuções por consulta; uma execução não prova nada.

Registro: skill · consulta · esperado · disparou? · execução 1/2/3.

## adr (disparo automático; sem gravar)
Positivas (devem disparar):
1. "Decidimos trocar o broker de RabbitMQ para SQS. Isso merece um ADR?"
2. "Escreva um ADR para a escolha de PostgreSQL no serviço de pedidos."
3. "Por que escolhemos Kafka aqui? Tem registro?"
4. "Registre essa decisão: vamos usar um monólito modular."
5. "Write an architecture decision record for adopting gRPC between services."
6. "Should this be an ADR? We're moving auth to a separate service."
7. "Quais ADRs existem sobre cache neste repositório?"
8. "Preciso de um ADR retroativo para o uso de Redis."
Negativas limítrofes (não devem disparar):
1. "Renomeie a variável tmp para orderDraft." (decisão pequena e reversível)
2. "Escreva a documentação da API de pedidos para os clientes." (technical-writing-docs)
3. "Escreva a spec de requisitos do checkout." (product-discovery-specs)
4. "Qual a diferença entre Postgres e MySQL?" (pergunta pontual, sem decisão do projeto)
5. "Crie um runbook para failover do banco." (sre-observability)
6. "Resuma a decisão do ADR-0004 em uma frase para o changelog." (documentação, não decisão)
7. "Como eu registro uma decisão de design de tela?" (ux-ui-design)
8. "Qual o formato de commit que devo usar?" (git-workflow-release)

## design-review
Positivas:
1. "Revise este plano de arquitetura antes de começarmos a codar."
2. "Review this design doc: 3 services, Kafka and CQRS for a 50-user CRUD."
3. "O desenho do módulo de faturamento está bom? Aponte lacunas."
4. "Architecture review of the diff in branch feature/outbox."
5. "Antes de implementar, desafie o escopo deste plano."
6. "Há algo errado na arquitetura descrita neste README?"
7. "Faça uma revisão de design do serviço de notificações, sem alterar nada."
8. "Lock in the plan: what decisions are still open?"
Negativas limítrofes:
1. "Revise este PR de CSS." (code-quality-refactoring / web-frontend)
2. "Revise minha função de ordenação por bugs." (code-quality-refactoring)
3. "Faça a revisão de segurança do endpoint de login." (security-appsec)
4. "O texto do README está claro?" (technical-writing-docs)
5. "Revise o plano de testes do checkout." (qa-testing)
6. "Revise a copy da tela de onboarding." (ux-ui-design)
7. "Esta query está lenta; que índice criar?" (database-data-modeling)
8. "Revise o Dockerfile." (devops-cloud-infra)

## system-design
Positivas:
1. "Projete um sistema de notificações para 2 milhões de usuários."
2. "Design a URL shortener that handles 10k writes per second."
3. "Como arquitetar um feed de atividades com leitura pesada?"
4. "Faça a conta de capacidade: 50 mil envios por minuto, quantos workers?"
5. "How should we architect real-time presence for 100k concurrent users?"
6. "Preciso de um design de sistema para ingestão de eventos de dispositivos, com ordem de grandeza."
7. "Vale a pena colocar cache na frente do catálogo? Leitura é 95% do tráfego."
8. "Back-of-envelope for a chat service with 5M DAU."
Negativas limítrofes:
1. "Escreva o endpoint POST /orders em FastAPI." (backend-api)
2. "Configure o Redis no docker-compose." (devops-cloud-infra)
3. "Crie o schema SQL para pedidos." (database-data-modeling)
4. "Otimize esta consulta GROUP BY." (database-data-modeling)
5. "Monte um dashboard de latência." (sre-observability)
6. "Desenhe a tela de checkout." (ux-ui-design)
7. "Projete uma pipeline de dados diária de vendas." (data-engineering)
8. "Converta esta função JavaScript para TypeScript." (negativo distante)

## resilience-and-consistency
Positivas:
1. "Meu consumidor recebe mensagens duplicadas e cobra duas vezes. Como tratar?"
2. "Explique o padrão transactional outbox para o nosso serviço de pedidos."
3. "Qual estratégia de retry entre serviços usar sem derrubar a dependência?"
4. "Should we use saga orchestration or choreography for order fulfillment?"
5. "Preciso de um circuit breaker na integração com o provedor de pagamento."
6. "Dual write entre banco e Kafka: como resolver?"
7. "CQRS vale a pena para um módulo de relatórios?"
8. "Event sourcing para o ledger de pagamentos: riscos?"
Negativas limítrofes:
1. "Implemente retry com tenacity nesta função Python." (backend-api)
2. "Como configuro o retry do nó HTTP no n8n?" (automation-integrations)
3. "Crie um alerta para fila acumulada." (sre-observability)
4. "Qual o melhor tipo de dado para um timestamp no Postgres?" (database-data-modeling)
5. "Escreva testes de carga com k6." (qa-testing)
6. "Como funciona o CAP theorem? Só quero a definição." (pergunta conceitual pontual; resposta direta)
7. "Configure o dead-letter queue no SQS via Terraform." (devops-cloud-infra)
8. "Explique o que é uma promise em JavaScript." (distante)

## decomposition
Positivas:
1. "Devemos migrar nosso monólito Rails para microsserviços?"
2. "Mapeie os bounded contexts do nosso e-commerce."
3. "Is a modular monolith enough for a team of 6?"
4. "Como aplicar arquitetura hexagonal neste serviço Node?"
5. "Planeje um strangler fig para tirar o faturamento do legado."
6. "Defina agregados para pedido, item e pagamento."
7. "Quero uma regra de fronteira entre módulos verificada no CI."
8. "Quando extrair um módulo para serviço próprio?"
Negativas limítrofes:
1. "Refatore esta classe de 800 linhas." (code-quality-refactoring)
2. "Crie a estrutura de pastas de um app Next.js." (web-frontend)
3. "Migre o banco de MySQL para Postgres." (database-data-modeling)
4. "Divida este PR em commits menores." (git-workflow-release)
5. "Como separo ambientes dev e prod no Terraform?" (devops-cloud-infra)
6. "Explique o que é DDD em dois parágrafos." (pergunta conceitual pontual)
7. "Quebre esta tarefa em subtarefas para o sprint." (product-discovery-specs)
8. "Crie um módulo Python chamado utils." (trivial)

## api-design
Positivas:
1. "Defina o contrato de GET /orders com 10 milhões de linhas, paginação e erros."
2. "Qual estratégia de versionamento de API usar para clientes móveis?"
3. "Revise o design desta API REST (cole o OpenAPI)."
4. "How should our API return validation errors consistently?"
5. "Preciso de um modelo de erro padronizado para todos os serviços."
6. "Como desenhar idempotência para POST /payments no contrato?"
7. "Paginação por cursor no contrato da API: como especificar?"
8. "Design review of our public REST API before v2."
Negativas limítrofes:
1. "Implemente este endpoint em Express." (backend-api)
2. "Adicione rate limiting no gateway." (backend-api)
3. "Gere o OpenAPI a partir do código FastAPI." (backend-api)
4. "Configure OAuth2 com refresh token." (backend-api / security-appsec)
5. "Escreva a documentação de referência da API." (technical-writing-docs)
6. "Crie um cliente TypeScript para esta API." (backend-api / web-frontend)
7. "Faça um schema GraphQL para o catálogo." (backend-api)
8. "Teste esta API com Postman." (qa-testing)

## playbook (router do segmento)
Positivas:
1. "Qual arquitetura faz sentido para um SaaS B2B com 3 devs e 200 clientes?"
2. "Preciso de ajuda com uma decisão de arquitetura entre fila e chamada síncrona."
3. "ARQUITETURA-COMPLETO: audite a arquitetura deste repositório."
4. "Desenhe o diagrama C4 de contêineres do nosso sistema de pedidos."
5. "Vale a pena hexagonal num serviço CRUD pequeno?"
6. "Help me think through the architecture trade-offs of this design."
7. "Quais trade-offs de arquitetura eu devo considerar antes de adotar multi-região?"
8. "Monte um checklist de revisão de arquitetura para o nosso time."
Negativas limítrofes:
1. "Crie o pipeline de CI no GitHub Actions." (devops-cloud-infra)
2. "Qual índice criar para esta query lenta?" (database-data-modeling)
3. "Corrija este NullPointerException." (fora do segmento)
4. "Escreva a história de usuário do checkout." (product-discovery-specs)
5. "Configure alertas de latência no Grafana." (sre-observability)
6. "Refatore esta classe de 600 linhas." (code-quality-refactoring)
7. "Avalie o RAG do nosso chatbot." (llm-ai-agents)
8. "Faça o pentest desta API." (security-appsec)

## prompts (biblioteca)
Positivas:
1. "Me dê um prompt pronto para revisar um plano de arquitetura em outro chat."
2. "Preciso de um template de prompt para escrever ADR."
3. "Qual prompt de sistema uso no CLAUDE.md de um projeto de arquitetura?"
4. "Give me a system design prompt template I can reuse."
5. "Escreva um briefing para um subagente revisar fronteiras de módulo."
6. "Quero a mensagem inicial sugerida para uma sessão de arquitetura."
7. "Tem um prompt para pré-mortem de uma decisão de arquitetura?"
8. "Prompt para pedir a outra IA um diagrama C4 por nível."
Negativas limítrofes:
1. "Revise este plano de arquitetura (colado abaixo)." (executar: design-review)
2. "Escreva o ADR da escolha de PostgreSQL." (executar: adr)
3. "Melhore o prompt do nosso chatbot de suporte." (llm-ai-agents)
4. "Crie um prompt para gerar testes unitários." (qa-testing)
5. "Projete o serviço de notificações." (executar: system-design)
6. "Me explique o que é prompt engineering." (pergunta geral)
7. "Escreva um prompt de marketing para o lançamento." (fora do segmento)
8. "Traduza este prompt para inglês." (tarefa trivial)

## Skills manuais (adr-write, architecture-plan)
Não disparam automaticamente (`disable-model-invocation: true`). Meça apenas: (a) o modelo sugere o slash command correto quando o pedido casa; (b) nunca grava arquivo sem o usuário invocar a skill e aprovar.
Exemplos de pedido que devem levar à sugestão do comando: "grave o ADR rascunhado"; "pesquise o código e planeje a extração do faturamento, só implemente depois que eu aprovar".

## Resumo da medição
| Skill | Positivas disparadas (de 8) | Falsos disparos (de 8) | Ajuste na description |
| --- | --- | --- | --- |
