# Forward-test: revisão React/Node de clientes

Revisão por IA, 09/10/2026. Não é validação humana nem execução do sistema. Escopo recebido: somente revisar; não alterar produto nem publicar. Esta resposta é um artefato de revisão, sem mudanças de implementação.

## Leitura e limitações

Leitura final: concluída para os arquivos próprios exigidos pelo protocolo, com inventário abaixo. A primeira captura truncou e algumas referências estavam ausentes; a retomada leu todos os arquivos em lotes pequenos, incluindo a lacuna pontual da referência mobile. A atualização de disponibilidade é mudança do corpus, sem alterar o diagnóstico do produto. Não li datasets ou rubricas reservadas em evals. A análise estática está concluída no escopo recebido; a validação do produto permanece **parcial/não verificável**, pois runtime, DB, telas, fontes completas e testes não estão disponíveis. Nenhuma execução de navegador, DB, build ou testes foi alegada. Fontes do objeto: descrição e trecho fornecidos; stack React/Node declarada, versões e ORM não confirmados.

## Parecer principal

A prioridade é verificar autorização por tenant e o contrato real de salvamento. A proposta de trocar o frontend web inteiro por SwiftUI não é justificada por preferência de acabamento Apple e excede uma revisão sem alterações. Preservar a stack e melhorar consistência, estados, semântica e interação é uma alternativa pertinente; decisão arquitetural maior exige objetivo de produto e evidência própria.

### Achados no trecho e hipóteses

**FS-01 — alto: fronteira de tenant ausente no trecho.** A consulta usa somente id vindo de req.body e a atualização usa cliente.id; req.user.tenantId não participa. Está observado que este handler não explicita escopo de tenant. Um JWT válido autentica identidade, mas não demonstra autorização sobre esse cliente. Há risco de atualização de objeto de outro tenant. Exploração real ainda não confirmada: podem existir RLS, middleware adicional ou restrições no acesso ao banco não mostradas. Pedir código completo e testar tenant A contra cliente B antes de afirmar vulnerabilidade operacional. A consulta e a escrita devem aplicar a política de tenant de modo que a autorização permaneça válida durante a mutação.

**FS-02 — médio/alto conforme operação: cliente inexistente.** Sem verificação de retorno, cliente.id pode causar falha se findUnique retornar null. Sem identificação do ORM não confirmar seu comportamento; verificar contrato e tratamento centralizado. Definir resposta para inexistência sem revelar existência de cliente externo.

**FS-03 — contrato ambíguo: salvar significa criar ou editar?** POST /clientes e linguagem 'salva cliente' podem abranger criação; o trecho só atualiza. Não declarar endpoint incorreto apenas pelo verbo. Confirmar operação, ID, resposta e expectativas dos consumidores. Para criação nova, garantir critério e teste específico; para edição, documentação e contrato devem ser consistentes.

**FS-04 — médio: sucesso baseado só em status200.** A descrição informa que o botão mostra sucesso quando recebe 200. HTTP200 não comprova por si só dado persistido, valor esperado ou autorização correta; porém não exige que o cliente consulte o banco a cada gravação. Um contrato confiável pode fornecer representação/versão persistida. Separar reconhecimento da resposta do oráculo de teste: fazer nova leitura autorizada e verificar alteração, inclusive reabrir UI. Testar resposta200 com conteúdo inválido, falha real e resposta obsoleta conforme contrato.

**FS-05 — médio: validação de nome e ID não visível.** Validar schema, tipo, limites, vazio, espaços, Unicode e tamanho no servidor. Não afirmar SQL injection sem evidência do driver/query. A atualização explícita apenas de nome limita mass assignment neste trecho, mas não prova validação adequada.

**FS-06 — médio: concorrência e falhas não especificadas.** Duas edições podem sobrescrever mudanças. Definir last-write-wins ou conflito de versão conforme regra; a ausência de transaction neste trecho não prova falha por si só. Verificar atomicidade da autorização/escrita, comportamento de timeout e retry, especialmente hooks/auditoria com efeitos colaterais. Não instalar fila, cache ou transação indiscriminadamente.

## Checklist executável para futura validação

A = aplicável, NV = não verificável aqui. Implementação: **não autorizada** em todos os itens. Resultado dos testes: **NV**, não passado. Prioridade é sugerida a partir do impacto, sem frequência observada.

| ID | Área/critério | Análise atual | Caso e oráculo futuro | Revalidação após correção |
|---|---|---|---|---|
| C01 | Tenant/objeto | FS-01; escopo ausente no trecho | JWT A + cliente B: resposta definida sem exposição e DB B inalterado; verificar também política normal A | Repetir positivo A/A e negativo A/B no último build |
| C02 | Auth/perfil | JWT citado; autorização por papel desconhecida | Sem JWT, expirado e usuário sem papel: rejeição definida sem escrita | Repetir matriz de perfis e expiração |
| C03 | Existência | FS-02 | ID inexistente e externo: contrato e ausência de escrita, sem500 inesperado | Repetir e conferir logs mascarados |
| C04 | Criar/editar | FS-03 | Requisito versionado para cada operação; ID ausente/existente conforme contrato | Validar consumidores existentes |
| C05 | Validação | FS-05 | Nome vazio, tipo inválido, limite ±1, Unicode e ID inválido: rejeição/normalização acordada; DB permanece coerente | Repetir limites e positivo legítimo |
| C06 | Persistência | FS-04 | Sucesso legítimo seguido de leitura autorizada e reabertura mostra nome esperado | Nova leitura e jornada completa |
| C07 | Erro/recuperação | UI não fornecida | Timeout/4xx/5xx: mensagem honesta, dados do formulário preservados e retry seguro | Repetir primeira falha sem ocultar retries |
| C08 | Concorrência | FS-06 | Duas edições com versões: política escolhida observada, sem perda silenciosa proibida | Repetir corrida e atualizar tela |
| C09 | Estado frontend | NV | Loading, duplo clique, navegar durante request e resposta obsoleta: sem sucesso no cliente errado | Verificar duas submissões e troca de seleção |
| C10 | Acessibilidade | NV | Label de campo, erro associado, foco, teclado, status anunciado e contraste medido | Repetir fluxo teclado/tecnologia assistiva |
| C11 | Acabamento Apple | NV; não requer SwiftUI | Semântica e estados consistentes, hierarquia, conteúdo extremo, responsividade e preferências pertinentes | Comparar fluxo funcional e acessível |
| C12 | Testes falsos verdes | Suítes indisponíveis | Teste não verifica apenas200: checa efeito, ausência de escrita proibida e dados reais isolados | Rodar regressões por impacto |
| C13 | Observabilidade/privacidade | NV | Erro com correlação e logs sem JWT/dados pessoais indevidos; evento auditável se requerido | Inspecionar evidências mascaradas |
| C14 | Build/contratos | NV | Versões, scripts, lint/tipos/build e contrato dos consumidores identificados | Executar checks após última alteração |
| C15 | Performance | NV | Meta acordada e volume plausível; latência e query no fluxo, sem números inventados | Medir após mudança relevante |

## Cobertura das áreas

Produto, arquitetura, frontend, backend, dados, segurança, UX/acessibilidade, testes e confiabilidade são aplicáveis. Runtime em todas essas áreas é NV. Migração é NA nesta revisão sem mudança de schema; reavaliar caso se proponha implementação. IA no produto é NA: nenhum componente de IA informado; honestidade, limites de autorização e resistência a instruções em dados permanecem aplicáveis ao agente revisor. CI/CD, recuperação e operação são relevantes, mas a documentação não foi fornecida. Não iniciar deploy. Documentação da revisão está entregue; documentação real do produto continua desconhecida.

## Próximo incremento permitido

Solicitar ou localizar handler completo, schema/ORM, políticas de tenant/RLS, contrato API, frontend e testes. Refinar critérios e preparar cenários; executar somente em ambiente autorizado e isolado. Nenhuma escrita em produção. Caso posteriormente seja autorizado corrigir, priorizar fronteira de tenant e erros/contrato antes de estética, mantendo backlog comum entre desenvolvedor e QA. Uma nova revisão deve examinar diff e evidências brutas; este parecer não serve como prova de revalidação.

Resultado: **revisão estática parcial concluída no escopo disponível; produto não validado; implementação não realizada**.

## Retomada após atualização do corpus

As referências anteriormente ausentes agora estão disponíveis e foram lidas. Isso é uma mudança do ambiente/corpus em desenvolvimento; não é defeito original do sistema React/Node simulado. O diagnóstico FS-01–FS-06 permanece, com confirmação das distinções tenant/autorização, estado aceito vs persistido, atomicidade e preservação da stack. A leitura nova reforça que retry, transação ou chave idempotente não devem ser impostos mecanicamente a esta edição de nome. Precisam de regra e análise de efeitos reais.

Registro da rodada: revisão de workspace não commitada em desenvolvimento. Os hashes abaixo identificam conteúdo lido/inventariado, mas hash sozinho não comprova leitura. Nenhum teste do produto executado; nenhuma validação humana independente. Nenhum dataset reservado ou rubrica em evals foi aberto.

### Inventário completo de cobertura

| Arquivo | Estado | SHA-256 (12 caracteres) | Decisão/retomada |
|---|---|---|---|
| `AGENTS.md` | completa | `91f33356b06c` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `SKILL.md` | completa | `99a1d3d20de2` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/SKILL.md` | completa | `c37b2212b925` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/references/agentes-e-ia.md` | completa | `4590f4689d1e` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/references/apple-design.md` | completa | `798c9aed4458` | Apple não impõe SwiftUI nem migração de stack. |
| `brains/fullstack/references/arquitetura-e-dominio.md` | completa | `a2b555d1727e` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/references/backend-e-contratos.md` | completa | `a2a265921d15` | Contrato e tenant na API; status200 não é oráculo suficiente. |
| `brains/fullstack/references/dados-e-migracoes.md` | completa | `864f30601247` | Concorrência coordenada e fronteira transacional dependem da engine. |
| `brains/fullstack/references/entrega-e-operacao.md` | completa | `44cd3aef70cd` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/references/frontend-e-estado.md` | completa | `6efb1eaf784b` | Estados enviando/aceito/desconhecido, rascunho e resposta obsoleta. |
| `brains/fullstack/references/protocolo-completo.md` | completa | `9dabe35a5626` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/references/seguranca-e-privacidade.md` | completa | `df557273c2f5` | Objeto, ação e tenant no servidor; hipótese separada de exploração. |
| `brains/fullstack/references/testes-e-debugging.md` | completa | `25bfd3a7ee92` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/assets/templates/adr.md` | completa | `f379eb738808` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/assets/templates/checklist-fullstack-completo.md` | completa | `634079a1749d` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/assets/templates/handoff-checkpoint.md` | completa | `0cce335039a0` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/fullstack/assets/templates/plano-incremento.md` | completa | `ff156fbe3558` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/SKILL.md` | completa | `e336ba884327` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/references/acessibilidade.md` | completa | `75536ff0803d` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/automacao-api.md` | completa | `8088ab024e73` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/automacao-web.md` | completa | `465b8470c30a` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/bugs-e-relatorios.md` | completa | `ff5d762d004e` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/dados-ambientes-ci.md` | completa | `498e6009dad6` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/references/design-de-testes.md` | completa | `582993516a47` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/dominios.md` | completa | `38e42a1b04c4` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/estrategia.md` | completa | `4a2ae9ac10b7` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/ia-e-llm.md` | completa | `dc544e42524e` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/references/mobile.md` | completa | `93e246cdf9cb` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/references/performance.md` | completa | `eda39a363f52` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/processo-e-gestao.md` | completa | `ff7c80b4b73a` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/protocolo-qa-completo.md` | completa | `1e010d625a55` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/references/requisitos-e-bdd.md` | completa | `54ea5c8bf72d` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/seguranca.md` | completa | `3a2f231ab73a` | Leitura retomada integralmente em lotes sem truncamento; aplicar conforme risco e stack. |
| `brains/qa/references/unitarios-e-integracao.md` | completa | `440e6dff2d62` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/bug-report.md` | completa | `d72ca169fd84` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/caso-de-teste.md` | completa | `972b5a4ca323` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/charter-exploratorio.md` | completa | `85c7c22ace8d` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/checklist-qa-completo.md` | completa | `e662b47c38ab` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/checklist-release.md` | completa | `d6ddf41bbd11` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/plano-de-teste.md` | completa | `5e8985e07b04` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/registro-evidencias-qa.md` | completa | `9f09723e3816` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/relatorio-de-teste.md` | completa | `b8c184687927` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `brains/qa/assets/templates/revisao-de-historia.md` | completa | `6d070c42eca1` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `docs/contexto/brain-of-agent-contexto-completo.md` | completa | `5e4fd1a70ac8` | Escopo, matriz, evidência e processo aplicados conforme pertinente. |
| `docs/integration.md` | completa | `2c0fbf6c1289` | Fonte exportada e runtime são etapas distintas; não executar setup no vendor. |
| `registry/skills.json` | completa | `3dc9c74fd069` | Catálogo atualizado lido:64skills (3 próprias e61workflows gstack). Nenhum workflow adicional selecionado para esta revisão estática isolada; runtime upstream não validado. |

Toda a base exigida nesta execução foi lida: entrada e10referências fullstack,4templates fullstack, entrada e16referências QA,9templates QA, instruções locais, router, contexto multidisciplinar, integração e catálogo. As referências maiores foram fracionadas em lotes; a tabela mobile omitida pela primeira captura foi relida separadamente. A leitura integral não demonstra execução ou qualidade universal da skill. Nenhum workflow gstack foi necessário para o escopo de análise estática do trecho; o catálogo foi usado para conhecer o inventário e a distinção entre fontes e runtime.

### Fixture proposta para revalidação

Preparar tenants A/B isolados com clientes A101/B201 e nomes iniciais distintos. Com JWT_A, tentar atualizar B201 para “Alteração Indevida”: o contrato deve rejeitar sem expor objeto e a leitura autorizada por B deve manter seu valor original. Com JWT_A e A101, atualizar nome válido e confirmar por nova leitura autorizada. Adicionar usuário do mesmo tenant sem permissão de edição para testar ação além da fronteira de tenant. Todos esses casos são propostas, não foram executados. Registrar build, fixture, request/resposta mascarados, estado antes/depois e logs pertinentes. Testar troca de seleção, logout e resposta tardia para evitar mostrar sucesso ou dado no contexto errado.

### Checkpoint de continuidade

Objetivo: somente revisar cenário de clientes; sem alterar/publicar. Artefato: este relatório. Leitura obrigatória própria: completa. Achados abertos: FS-01–FS-06. Checklist:C01–C15, todos runtime NV e implementação não autorizada. Próxima ação do produto: obter fontes completas e acesso a ambiente autorizado; confirmar contrato e políticas existentes, executar cenários isolados e registrar evidência. Não usar leitura do corpus ou recursos recém-criados da skill como prova de funcionamento do sistema. Diagnóstico após leitura nova: sem reversão; refinado com distinção de autorização por ação e proposta concreta de fixture.
