# Checklist de revisão de arquitetura (por eixo)

Sumário: 1. Como usar · 2. Eixos E1 a E11 · 3. Perguntas de desafio de escopo · 4. Princípios do gstack como perguntas · 5. Armadilhas de avaliação · 6. Gotchas

Validado em 2026-10-10. Fontes: `arquitetura-e-dominio.md` do brain-of-agent (MIT, Francisco Edson), oito eixos de revisão (padrões, escalabilidade, tecnologia, integração, segurança, desempenho, dívida, evolução; ideia do item VoltAgent rebaixado a classe C em VALIDATED, reescrita em V-03/V-19), V-19 (gstack plan-eng-review, MIT, só o processo), V-42, V-45, V-30 a V-38. O checklist integral do plugin está em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/checklist-completo.md`; este arquivo é o recorte que a skill usa. Os IDs `E` são códigos de eixo; os IDs `ARQ-nn` pertencem ao relatório de cada revisão.

## 1. Como usar

Para cada eixo: responda a pergunta, procure a evidência com a "detecção" e classifique: lacuna (gera `ARQ-nn`), sem lacunas, ou Não aplicável (motivo). A coluna "detecção" são buscas de leitura (Grep/Glob); nenhuma exige executar código. Padrões de busca são exemplos: ajuste à linguagem e ao framework do projeto (Suposição).

Os eixos abaixo foram escritos para sistemas de servidor. Se o alvo é app local ou móvel (Android, iOS) ou desktop, percorra também a seção "Cobertura de plataforma" de `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/checklist-completo.md` antes de marcar eixos inteiros como Não aplicável; "Não aplicável" em bloco esconde riscos do dispositivo (ciclo de vida, retenção local, intents, manifesto).

## 2. Eixos

| ID | Eixo | Pergunta | Detecção (leitura) | Severidade típica se faltar | Correção mínima |
| --- | --- | --- | --- | --- | --- |
| E1.1 | Fronteiras | Há regra de dependência escrita (quem pode importar quem)? | `CLAUDE.md`, `docs/adr/`, config de lint; `Grep` por `import` cruzando camadas | Médio | Tabela camada -> pode importar / não pode (skill `decomposition`) |
| E1.2 | Fronteiras | Alguma fronteira é imposta por máquina (teste de arquitetura, lint, CI)? | `Glob` por `.dependency-cruiser*`, `ArchUnit`, scripts de CI | Médio | Verificador no CI; sem ele a fronteira é só prosa |
| E1.3 | Fronteiras | Um módulo acessa tabela de outro módulo? | `Grep` por nomes de tabela de outro módulo em SQL/ORM | Alto | Propriedade de esquema: acesso só pela fachada do dono |
| E2.1 | Fluxo de dados | O fluxo crítico está descrito ator -> comando -> autorização -> regra -> transação -> efeito externo -> resposta? | Documento de design; seguir o handler no código | Médio | Escrever a sequência e marcar onde o processo pode morrer |
| E2.2 | Fluxo de dados | Quem é dono de cada dado e quem decide cada regra? | Ler modelos e serviços; ADRs | Alto | Nomear dono; evitar dois escritores do mesmo dado |
| E3.1 | Estados e falhas parciais | O que acontece se o processo cair entre gravar no banco e chamar o efeito externo ou publicar o evento? | `Grep` por commit seguido de `publish`/`send`/`http` no mesmo handler | Crítico | Outbox (skill `resilience-and-consistency`) |
| E3.2 | Estados e falhas parciais | Estados e transições estão explícitos (máquina de estados), sem combinações de booleanos contraditórias? | Colunas `is_*`, `*_flag` com combinações impossíveis | Alto | Enum de estado com transições permitidas e dono |
| E3.3 | Estados e falhas parciais | Timeout é tratado como "aceitação desconhecida" e não como falha definitiva? | `Grep` por `timeout` e o tratamento do erro | Alto | Consultar o estado remoto ou repetir com chave idempotente |
| E4.1 | Concorrência | Duas requisições simultâneas na mesma entidade produzem uma só operação de negócio? | Restrições de unicidade, versão otimista, locks | Alto | Unique constraint, versão (`If-Match`), lock pelo escopo mínimo |
| E4.2 | Concorrência | A consistência entre agregados é tratada como eventual e cada transação cobre um agregado? | Transações que tocam várias entidades de contextos diferentes | Médio | Reduzir transação a um agregado; usar eventos |
| E5.1 | Idempotência | Operações repetidas (retry, redelivery, duplo clique) são seguras? | Handlers de mensagem e POST com efeito sem chave de idempotência | Alto | Chave estável, marcador e efeito na mesma transação |
| E5.2 | Idempotência | Há mais de uma camada repetindo a mesma chamada? | `Grep` por `retry`/`backoff` em cliente, SDK, gateway e job | Alto | Retry em uma só camada, com limite e jitter |
| E6.1 | Migração e rollback | Existe plano de migração em fases reversíveis, cada uma com verificação? | Seção de migração do plano; scripts de migração | Alto | Expand/contract (expandir, migrar, contrair); fases pequenas |
| E6.2 | Migração e rollback | O plano promete rollback de dados só porque há migração `down`? | `Grep` por `down`/`rollback` e a promessa no documento | Alto | Declarar o que não volta (dados escritos após a migração) |
| E7.1 | Autorização | A autorização é verificada por objeto (esta pessoa pode ver este recurso), não só por rota? | Handlers que carregam recurso por id sem checar dono/tenant | Crítico | Checagem de posse/tenant no ponto de acesso a dados |
| E7.2 | Autorização | Há fronteira de confiança sem validação de entrada ou sem autenticação entre serviços? | Endpoints internos expostos; confiança em cabeçalhos | Alto | Autenticar entre serviços; validar na fronteira |
| E8.1 | Observabilidade | Cada fluxo crítico tem identificador de correlação, log estruturado e métrica de sucesso/erro? | `Grep` por trace id, logger, métricas no fluxo | Médio | Propagar trace context; definir 1 a 3 sinais por fluxo |
| E8.2 | Observabilidade | Falhas silenciosas (catch vazio, DLQ sem alerta) são visíveis? | `Grep` por `catch` que engole erro; filas de erro sem consumidor | Alto | Alerta em DLQ e em erro recorrente |
| E9.1 | Testes | Cada requisito do plano mapeia a um teste, e há teste por camada onde o risco mora? | Plano vs `Glob` de testes | Médio | Tabela requisito -> teste; teste de fronteira no CI |
| E9.2 | Testes | Os testes provam o comportamento ou apenas o mock do fornecedor? | Testes que só afirmam chamadas de mock | Médio | Teste de contrato/integração real com dublê do fornecedor documentado |
| E10.1 | Desempenho | Há um número (carga, latência, tamanho de dado) que justifica cada otimização (cache, fila, réplica)? | Documento de design; ausência de estimativa | Médio | Estimativa de ordem de grandeza no texto; medir antes de otimizar |
| E10.2 | Desempenho | Consultas em loop (N+1) ou listas sem paginação em caminho crítico? | `Grep` por consulta dentro de `for`/`map`; endpoints de lista sem `limit` | Médio | Carregamento em lote; paginação por cursor |
| E11.1 | Dívida e evolução | O desenho tem um caminho para mudar de ideia (reversibilidade, ponto de extensão real)? | ADRs, gatilhos de reavaliação | Médio | Registrar gatilhos; evitar abstração sem uma segunda variação real |
| E11.2 | Dívida e evolução | A alternativa mais simples foi descartada com motivo? | Seção de alternativas do plano | Médio | Incluir "não mudar nada" e a opção mínima |
| E11.3 | Dívida e evolução | Há abstrações que só repassam argumentos (camadas sem decisão)? | Classes/funções que apenas delegam | Baixo -> Opcional | Remover a camada ou justificar com uma variação real |

Severidade típica é ponto de partida; ajuste ao contexto (um E3.1 em fluxo sem dinheiro nem dados importantes pode ser Médio). Rotule a severidade como julgamento (Inferido).

## 3. Perguntas de desafio de escopo (passo 2)

1. Qual é a solução menor que ainda atende o requisito declarado? (Escreva-a, mesmo que seja rejeitada.)
2. O que já existe no repositório (módulo, biblioteca, serviço) que cobre parte disto? `Grep` pelo conceito antes de afirmar que não existe.
3. O que dá para não construir agora e adicionar quando um gatilho medido aparecer?
4. Quantas partes móveis novas o plano cria (serviços, filas, tabelas, dependências, deploys) e qual requisito justifica cada uma?
5. Se a premissa mais cara estiver errada, quanto custa voltar atrás?

## 4. Princípios do gstack, reescritos como perguntas (Suposição de preferência)

Inspiração de processo do `plan-eng-review` do gstack (V-19, MIT, Garry Tan; não importado, apenas ideias reescritas). Tratar como heurísticas de preferência, não como regras.

| Princípio | Pergunta |
| --- | --- |
| Raio de explosão | Se isto falhar, o que mais para de funcionar? |
| Chato por padrão | Existe uma tecnologia já usada no projeto que resolve? O que justifica uma nova? |
| Reversibilidade | Dá para desfazer com um deploy, ou exige migração de dados? |
| Lei de Conway | A fronteira proposta coincide com os times que vão mantê-la? |
| Explícito sobre esperto | Um mantenedor novo entende o fluxo lendo o código, sem conhecer a história? |
| Diff pequeno | O plano pode ser entregue em fatias verticais independentes? |

## 5. Armadilhas de avaliação (brain-of-agent)

- Organização em pastas não é isolamento; isolamento exige regra verificável.
- Cobertura de linha não prova proteção do domínio.
- Compilar não é integrar; mock de fornecedor não é evidência do fornecedor.
- Onde faltar acesso, registre a fronteira não observada e a validação que resta.

## 6. Gotchas

- "Sem lacunas" é uma resposta válida; não invente achados para parecer útil (V-03).
- Limiar de confiança 7 e as severidades acima são Suposição; deixe o usuário ajustar.
- Padrões de `Grep` dão pistas, não provas: um `import` pode estar morto, e uma dependência pode existir só em runtime (Inferido).
- ATAM leve não é avaliação ATAM (SEI/CMU leva dias com avaliadores treinados; N-08) e o Well-Architected não é auditoria.
