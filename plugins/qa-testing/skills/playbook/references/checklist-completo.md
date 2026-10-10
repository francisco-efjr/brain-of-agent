# Checklist completo: matriz de 14 áreas, gates e critérios de saída

Use com o modo `QA-COMPLETO` (ver `SKILL.md`) ou, em uso seletivo, para escolher quais áreas pesam no pedido. Base: protocolo `QA-COMPLETO` e checklist operacional do brain-of-agent (conteúdo próprio, MIT), adaptado ao plugin. Validado em 2026-10-10.

## Sumário

- [Estados e gates](#estados-e-gates)
- [Matriz das 14 áreas](#matriz-das-14-áreas)
- [Registro de leitura](#registro-de-leitura)
- [Itens por fase: analisar, implementar, revalidar](#itens-por-fase)
- [Checklist final de uma mudança](#checklist-final-de-uma-mudança)
- [Exemplo de registro honesto](#exemplo-de-registro-honesto)

## Estados e gates

| Fase | Estados permitidos | Regra |
| --- | --- | --- |
| Análise | pendente · conforme · não conforme · NV · NA | NV (não verificável) quando falta acesso, ferramenta ou requisito; NA exige motivo |
| Implementação | não necessária · proposta · não autorizada · feita · impedida | Auditoria registra "não autorizada" e propõe; nada de alteração alheia ao pedido |
| Revalidação | pendente · passou · falhou · NV · NA | "Passou" só com evidência executada que corresponda ao artefato entregue |

Gates finais (não use "aprovado" fora deles):

- **Concluído:** escopo autorizado realizado; critérios de saída pertinentes verificados; exclusões justificadas; risco residual explícito.
- **Parcial:** falta leitura, acesso, execução ou revalidação material. Descreva o que falta.
- **Impedido:** uma ação necessária não pode avançar. Descreva a condição e o próximo passo.

Uma média de notas não compensa falha crítica. Recomendação favorável é informação para decisão, não garantia de ausência de defeitos.

## Matriz das 14 áreas

Para cada área: marque A (aplicável), NA (com motivo) ou NV. Classifique risco por impacto e probabilidade e documente a incerteza; evite pontuação artificial quando não há dados.

| # | Área | Perguntas que exigem decisão | Evidência que fecha o critério | Onde aprofundar |
| --- | --- | --- | --- | --- |
| 1 | Produto/requisitos | Qual regra, usuário e resultado? O que deve ser preservado? Há fonte de verdade versionada? | Regra com exemplo concreto e fonte; ambiguidade virou pergunta | `design-de-testes.md` (oráculos), skill `test-design` |
| 2 | UX/conteúdo | A jornada, as mensagens, a recuperação de erro e os extremos (vazio, 1.000 itens) fazem sentido? | Exploratório com charter; mensagem de erro dispara por caso | `design-de-testes.md` (exploratório, FEW HICCUPPS) |
| 3 | UI/design | Componentes, estados (vazio, carregando, erro, desabilitado), tokens e comportamento são coerentes? | Teste de componente ou visual com diff revisado | `automacao-web-e2e.md` |
| 4 | Arquitetura | Invariantes, dependências, estado e modos de falha estão modelados? Há seams testáveis? | Camada escolhida por risco; seam existente ou lacuna reportada | `decisoes-e-tradeoffs.md` (K1, árvore de camada) |
| 5 | Frontend/app | Navegação, concorrência assíncrona, persistência e ciclo de vida (recarregar, voltar, duas abas)? | E2E curto da jornada de valor + componente para estados | `automacao-web-e2e.md` |
| 6 | Backend/API | Contratos, autorização por objeto, idempotência, erro, paginação e integração? | Checklist por endpoint executado contra local/staging; contrato verificado | `nao-funcional-e-contrato.md` (skill `test-strategy`), `unitarios-e-integracao.md` |
| 7 | Dados | Precisão (centavos inteiros), fuso, migração, retenção, reconciliação? | Oráculo antes/depois (contagens, totais, amostra de casos especiais) | `unitarios-e-integracao.md` (dados de teste, integração) |
| 8 | QA/automação | Risco, oráculo, limites, isolamento e força das asserções? A suíte falharia diante da regressão conhecida? | Mutation check manual ou ferramenta; revisão por `test-reviewer` | `padroes-e-antipadroes.md`, `unitarios-e-integracao.md` |
| 9 | Acessibilidade | Semântica, teclado, foco, tecnologia assistiva, contraste, preferências (movimento reduzido, zoom 200%)? | Ferramenta automática + roteiro manual de teclado/leitor de tela (3 camadas, V-18) | `nao-funcional-e-contrato.md` |
| 10 | Segurança/privacidade | Fronteiras, acesso por objeto e tenant, segredos, abuso, dado pessoal em evidência? | Casos negativos de autorização (IDOR); evidência mascarada | `bugs-e-evidencia.md` (evidências e LGPD); plugin `security-appsec` |
| 11 | Performance/confiabilidade | Baseline, volume, recursos, timeout, recuperação? | Tipo de teste k6 adequado (smoke antes de carga), só em ambiente autorizado | `nao-funcional-e-contrato.md` (V-23) |
| 12 | IA/RAG/agente | Grounding, ferramentas, injeção, variabilidade, avaliadores? | Suíte de evals com graders de código antes de juiz LLM; várias execuções | `evals-e-ia-llm.md` |
| 13 | CI/operação | Checks, observabilidade, rollout, recuperação, smoke? Zero testes coletados vira verde silencioso? | Gate testado com falha controlada; manifesto do ambiente | `estrategia-e-risco.md` (regressão em camadas, prontidão) |
| 14 | Processo/documentação | Decisões, handoff, responsabilidade e continuidade registradas? | Handoff com Verificado / Não testado / próximo passo | templates `parecer-de-prontidao`, `relatorio-de-teste` |

## Registro de leitura

No modo completo, registre cada arquivo realmente acessado (não basta ver o nome ou um resultado de busca):

| Arquivo/fonte | Revisão ou data | Estado (completo/parcial/ausente) | Decisão extraída | Retomada |
| --- | --- | --- | --- | --- |

Leitura truncada é "parcial"; continue do ponto seguinte. Arquivo citado e inexistente na instalação é "ausente" (a cobertura nunca é declarada integral nesse caso). O template operacional é `assets/templates/checklist-qa-completo.md`; as execuções vão para `assets/templates/registro-evidencias-qa.md`.

## Itens por fase

**Analisar (marque cada item como conforme, não conforme, NV ou NA, com motivo):**

- [ ] Integridade das funções e regras existentes (o que deve ser preservado).
- [ ] Positivos, negativos, limites e transições relevantes ao risco.
- [ ] Permissões, dados de outro usuário ou tenant, expiração de sessão e token.
- [ ] Duplicação (clique duplo, retry, mensagem repetida), concorrência, timeout e recuperação.
- [ ] Estados vazio, carregando, erro, desabilitado e conteúdo extremo.
- [ ] Contratos, precisão, fuso, persistência e efeitos colaterais.
- [ ] Acessibilidade e comportamento da plataforma pertinente.
- [ ] Segurança, privacidade, dependências e segredos (sem executar exploração).
- [ ] Performance, observabilidade e operação conforme o risco.
- [ ] IA: fontes, injeção, ferramentas, variabilidade e evidência honesta.
- [ ] Asserções, isolamento e falsos verdes na suíte existente.

**Implementar (apenas com autorização no escopo nomeado):**

- [ ] Correção priorizada e ligada ao achado (ID do achado no commit ou no nome do teste).
- [ ] Contratos preservados, ou mudança explicitamente acordada.
- [ ] Teste de regressão que falhou antes da correção (falha colada, depois o verde).
- [ ] Dados, migrações e compatibilidade considerados.
- [ ] Diff revisado, sem alterações alheias ao escopo; `git diff --stat` confere os caminhos.
- [ ] Nenhum teste existente removido, pulado ou afrouxado sem decisão humana registrada.

**Revalidar:**

- [ ] Reprodução original executada contra a correção.
- [ ] Resultado comparado ao oráculo independente (não ao que a tela mostra).
- [ ] Efeito persistido e ausência de duplicação conferidos quando aplicável.
- [ ] Regressões por impacto executadas (inclui dependência por dado, configuração e evento).
- [ ] Ambiente, versão e revisão da evidência correspondem à entrega; alteração posterior invalida a evidência pertinente.
- [ ] Primeira falha e retries preservados; falhas restantes e NV registrados.

## Checklist final de uma mudança

Para qualquer tarefa, mesmo sem o modo completo (base: `testes-e-debugging` do brain, MIT):

- [ ] Riscos e invariantes ligados a casos e camadas.
- [ ] O teste falharia diante da regressão conhecida ou de uma mutação pertinente.
- [ ] Dados, relógio, dependências e isolamento controlados.
- [ ] Caminhos negativos, concorrência e falha parcial incluídos quando aplicáveis.
- [ ] Mocks identificados e limitações da integração declaradas.
- [ ] Falha intermitente não escondida por retries.
- [ ] Comandos, códigos de saída, versão e resultados registrados.
- [ ] Evidência distingue executado, revisado, inferido e bloqueado.
- [ ] Pendências têm impacto e próximo passo; nenhuma "aprovação QA" inventada.

Não amplie a suíte indefinidamente depois que as verificações adequadas passaram sem nova mudança ou preocupação concreta.

## Exemplo de registro honesto

> Base do plugin lida em 4 lotes; `nao-funcional-e-contrato.md` ausente nesta instalação (cobertura parcial de API e acessibilidade). Contrato da API de totais revisado. Três falhas corrigidas e revalidadas no ambiente local (comandos e saídas no registro de evidências). Fluxo com pagamento real e leitor de tela não executados (Não verificável). Resultado: **Parcial**; riscos detalhados no checklist.

Fonte do exemplo e do protocolo: brain-of-agent (`protocolo-qa-completo.md`, MIT), adaptado.
