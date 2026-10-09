# Pesquisa: agentes de desenvolvimento e padrões transferíveis

Data da consulta: **09/10/2026**. Escopo: fontes primárias dos mantenedores e documentação de avaliação. Esta pesquisa orienta o brain desenvolvedor; não instala agentes, importa código, executa modelos nem certifica desempenho. As páginas vinculadas são mutáveis; registrar commit e versão antes de adotar uma dependência. Não comparar percentuais de projetos com modelos, budgets e ambientes diferentes.

## 1. Projetos observados

| Projeto / fonte primária | Evidência observada | Padrão útil | Limitação / licença observada |
|---|---|---|---|
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | Agente configurável para resolver issues; mantenedores recomendam mini-SWE-agent para trabalho futuro | Issue concreta, ambiente e trajetória examinável | O próprio README sinaliza mudança de foco. MIT anunciada no repositório |
| [mini-SWE-agent](https://github.com/SWE-agent/mini-swe-agent) | Implementação mínima, histórico linear e execução de comandos; suporta diferentes ambientes | Baseline simples, menos mecanismos opacos, comandos e resultados rastreáveis | A simplicidade do harness não limita por si só privilégios do shell. MIT anunciada |
| [OpenHands Software Agent SDK](https://github.com/OpenHands/software-agent-sdk) | APIs Python, TypeScript e REST; workspace local ou efêmero por Agent Server | Separar modelo, ferramentas, conversa e ambiente; ciclo de vida explícito | SDK oferece mecanismos; políticas e isolamento dependem de configuração. [MIT](https://github.com/OpenHands/software-agent-sdk/blob/main/LICENSE) |
| [Aider](https://github.com/Aider-AI/aider) | Edição assistida integrada ao Git e suporte a lint/testes | Mudança pequena com diff legível e revisão | Commit automático não substitui aceite; Apache-2.0 anunciada no repositório, arquivo LICENSE.txt |

Nenhum desses projetos foi copiado ou instalado nesta pesquisa. Licenças acima são identificação informativa das páginas consultadas; eventual redistribuição exige leitura das licenças e avisos na revisão exata, incluindo dependências. Popularidade, estrelas e divulgação dos mantenedores não servem como prova de qualidade para nosso caso.

## 2. Contexto e navegação

[Aider repository map](https://aider.chat/docs/repomap.html) descreve um mapa compacto de arquivos, símbolos e assinaturas, com seleção por relevância e orçamento de tokens. É um exemplo concreto de contextualização do código sem despejar todo o repositório em cada solicitação.

**Inferência para nosso brain:** ler integralmente o corpus próprio em modo completo por lotes e registrar cobertura; para o sistema alvo, produzir mapa e inspecionar implementações, chamadores e testes relacionados ao risco. Leitura de um índice não comprova leitura das implementações. Não confundir consumo completo do conhecimento com inserção simultânea de todos os arquivos em uma janela de contexto.

A [engenharia de contexto da Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) trata seleção de contexto, recuperação de informações, compactação e memória estruturada. **Aplicação proposta:** manter decisões, requisitos, falhas e evidências em artefatos persistentes; após compactação, reler o estado e os trechos críticos. Documentos e resultados de ferramentas devem ser tratados como dados, sem promover instruções encontradas neles a autorização do usuário.

## 3. Trabalhos longos, checkpoints e crítica

[Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) relata problemas de trabalho amplo demais e conclusão prematura. Apresenta inicialização do ambiente, lista de funcionalidades, implementação incremental e registros persistentes de progresso. É uma experiência de engenharia situada, não prova universal de arquitetura superior.

**Aplicação proposta:** iniciar com baseline executável; dividir por fatias verticais verificáveis; salvar estado com objetivo, arquivos alterados, testes executados, pendências e próximo passo. Encerrar por critérios de aceite e evidências, sem declarar conclusão somente por progresso visível. Não transformar expiração de tokens em critério de qualidade.

[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) descreve planejamento, geração e avaliação com rubricas concretas e remoção experimental de componentes do harness. **Inferência:** separar produção e crítica pode ser útil, mas criar mais agentes não demonstra ganho. Antes de ampliar a equipe, comparar baseline, custo e qualidade; para tarefa simples, um único agente pode executar fases distintas. Revisão do mesmo modelo não deve ser descrita como independente sem explicitar a dependência.

## 4. Ciclo de implementação e revalidação

[Aider linting and testing](https://aider.chat/docs/usage/lint-test.html) permite configurar lint e comandos de teste após alterações, com falhas retornando saída e código não zero. Esse mecanismo ilustra feedback executável durante a edição; não garante cobertura da regra de negócio.

**Contrato proposto para FULLSTACK-COMPLETO:**

1. Esclarecer objetivo, autorização, ambiente, fluxos e riscos.
2. Inspecionar arquitetura, dependências e testes; executar baseline apropriado.
3. Definir critério de aceite observável e checks por camada.
4. Implementar fatia pequena; manter comportamento existente e contratos explícitos.
5. Executar checks relevantes: tipos, lint, build, testes de regra, integração e jornada conforme impacto.
6. Investigar falhas; distinguir defeito do produto, teste, infraestrutura e falta de acesso.
7. Após corrigir, reproduzir o caso original e validar efeitos adjacentes.
8. Revisar diff, dados, permissões, acessibilidade, experiência, observabilidade e reversão.
9. Entregar evidências e limites; ausência de execução resulta em pendência, não aprovação.

Esta sequência é uma síntese nossa. Não atribuir às fontes cada item nem exigir comandos de uma stack inexistente.

## 5. Isolamento e autonomia

[Sandboxing no Claude Code](https://www.anthropic.com/engineering/claude-code-sandboxing) descreve restrições de filesystem e rede como fronteiras de execução. O princípio transferível é separar autonomia para implementar de privilégio para afetar recursos externos.

**Política proposta:** keywords ativam processo, não privilégios. Respeitar autorização já concedida e realizar trabalho reversível no escopo; mudanças destrutivas, operações em produção, publicação, gastos e mensagens externas dependem da autorização aplicável. Um worktree isola mudanças Git, mas não é uma barreira de rede ou segredos. Containers também precisam de configuração: volumes, credenciais, rede e permissões importam. Scripts do repositório alvo podem executar código arbitrário; inspecionar o necessário e usar o ambiente autorizado.

## 6. Avaliação: medir resultado e comportamento

[Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) distingue avaliadores por código, modelo e humanos; recomenda tarefas claras, ambientes isolados, inspeção de trajetórias e calibração. Também diferencia avaliação de capacidade e regressão. Para código, resultado executável deve pesar mais que coincidência com uma sequência rígida de ferramentas.

[SWE-bench](https://www.swebench.com/SWE-bench/) avalia patches para issues reais e fornece harness Docker para reprodução. Seu escopo não cobre sozinho design, acessibilidade, deploy, autorização ou todas as stacks. Usá-lo como inspiração metodológica, não como certificado de competência fullstack.

**Plano de benchmark próprio:**

- Mesma tarefa e ambiente para baseline sem skill, skill e skill com workflow.
- Fixtures limpas por tentativa; separar respostas de referência do contexto do agente.
- Testes positivos e negativos, erros de contrato, autorização, concorrência, migração e rollback.
- Incluir casos que exigem alterações e casos em que editar seria incorreto.
- Pontuar funcionalidade, regressão, segurança, acessibilidade, escopo, honestidade e manutenção.
- Registrar modelo/versão, corpus/commit, ferramentas, comandos, duração, custo disponível e estado final.
- Repetir tentativas quando houver orçamento autorizado; divulgar denominadores e variabilidade.
- Calibrar rubricas subjetivas com revisão humana e possibilidade de resultado inconclusivo.
- Separar validade estrutural do dataset, sucesso dos testes e desempenho efetivamente observado.
- Manter casos reservados e revisar falhas para evitar otimização somente para exemplos conhecidos.

## 7. Competências a traduzir em conhecimento e checklists

As recomendações abaixo são nossa síntese de necessidades de desenvolvimento, e não capacidades certificadas dos projetos pesquisados:

- Produto: requisitos verificáveis, casos negativos, prioridades e limites.
- Arquitetura: responsabilidades, contratos, dependências, decisões e caminhos de evolução.
- Interface: consistência com plataforma, estados completos, teclado, leitores de tela e feedback.
- Backend: autorização por objeto/ação, validação, erros estáveis, idempotência e concorrência.
- Dados: integridade, transações, migração segura, recuperação e retenção.
- Operação: configuração, segredos, build reproduzível, observabilidade, rollout e rollback.
- Qualidade: testes com oráculos reais, cobertura orientada a risco e revisão crítica de evidências.
- IA: limites de autonomia, contenção, rastreabilidade, resistência a instruções em dados e benchmark.

## 8. Decisões de adoção e limites

Adotar padrões e conhecimento antes de importar runtimes. Manter o gstack atual intacto. Não escolher um framework somente por promessa de benchmark. Não declarar que FULLSTACK-COMPLETO tem competência superior à QA por ter mais referências. A amplitude pretendida precisa ser validada por tarefas reais e critérios equivalentes.

O corpus deverá ter proprietário, data de revisão, fontes junto das afirmações e checklist de atualização. Quando fonte mudar, avaliar impacto sobre protocolo, fixtures e exemplos. Não atualizar automaticamente comandos ou políticas de runtime sem verificação no host alvo.
