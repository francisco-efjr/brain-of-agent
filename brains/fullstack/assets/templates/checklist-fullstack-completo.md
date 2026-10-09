# Checklist FULLSTACK-COMPLETO

Projeto/objeto: [nome] · Pedido/escopo: [objetivo]
Revisão/ambiente: [commit/build/ambiente] · Data: [data]
Autorização: [análise/implementação local/ações externas específicas]

## 1. Leitura e capacidades

| Arquivo | Revisão | Completa/parcial/ausente | Decisão extraída | Ponto de retomada |
| --- | --- | --- | --- | --- |

- [ ] Instruções e skill fullstack lidas; router lido quando presente no repositório.
- [ ] Nove referências técnicas, protocolo e quatro templates lidos.
- [ ] QA SKILL, quinze referências, protocolo e templates lidos.
- [ ] Contexto, integração e catálogo lidos ou ausência registrada.
- [ ] Workflows selecionados lidos e ferramentas disponíveis identificadas.
- [ ] Fontes de requisito, design e contrato inventariadas.

| Capacidade | Disponível/indisponível | Ambiente/limite | Evidência |
| --- | --- | --- | --- |
| Leitura/edição | | | |
| Shell/build/testes | | | |
| Navegador | | | |
| Banco/integrações | | | |
| Rede/Git | | | |

## 2. Aplicabilidade de áreas

A = aplicável; NA = não aplicável com justificativa; NV = não verificável.

| Área | A/NA/NV | Regra/fonte | Risco/justificativa | IDs |
| --- | --- | --- | --- | --- |
| Produto/requisitos | | | | |
| UX/UI/conteúdo e acabamento | | | | |
| Frontend/app e navegação | | | | |
| Backend/API/integração | | | | |
| Arquitetura/domínio | | | | |
| Dados/persistência/migração | | | | |
| Segurança/privacidade | | | | |
| Acessibilidade/plataforma | | | | |
| Testes/debugging | | | | |
| Performance/confiabilidade | | | | |
| IA/RAG/ferramentas | | | | |
| CI/CD/operação | | | | |
| Documentação/continuidade | | | | |

## 3. Backlog rastreável

Uma linha por critério/achado, com evidência e estado separados.

| ID | Requisito/risco | Critério/oráculo | Análise | Implementação/arquivos | Validação | Revalidação | Evidência | Pendência |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Estados: pendente; inferido; verificado; falhou; não autorizado; NA; NV.
Não confunda implementação concluída com critério operacional verificado.

## 4. Analisar antes de alterar

- [ ] Fluxo principal e alternativas identificados.
- [ ] Regras e conteúdo que precisam ser preservados mapeados.
- [ ] Conflitos e suposições materiais expostos.
- [ ] Stack/versões/comandos confirmados no projeto.
- [ ] Estado do Git e alterações do usuário preservados.
- [ ] Invariantes, contrato e consumidores identificados.
- [ ] Autorização por operação/objeto/tenant avaliada.
- [ ] Precisão, tempo/fuso e unidade de dados definidos.
- [ ] Estados UI, respostas obsoletas, cancelamento e recuperação considerados.
- [ ] Concorrência, reenvio e efeitos duplicados avaliados.
- [ ] Migração, compatibilidade e limites de rollback identificados.
- [ ] Risco de segredo no cliente/log/Git verificado.
- [ ] Design e comportamento avaliados na plataforma alvo.
- [ ] Testes existentes revisados para falso verde.

## 5. Implementar dentro do escopo

- [ ] Fatia vertical e critério de saída definidos.
- [ ] Decisões relevantes documentadas, sem complexidade gratuita.
- [ ] APIs conferidas para a versão instalada.
- [ ] Regras no servidor quando necessário, além da validação cliente.
- [ ] Estados vazio/carregando/erro/indisponível e recuperação implementados.
- [ ] Acessibilidade e foco não ficam para depois do acabamento.
- [ ] Contratos e migrações mantêm compatibilidade necessária.
- [ ] Timeout/retry/idempotência respeitam efeitos colaterais.
- [ ] Regressões significativas e dados isolados preparados.
- [ ] Configuração/segredos/documentação tratados.
- [ ] Diff não altera partes alheias nem fontes vendor.

## 6. Validar e revalidar

- [ ] Build/tipos/lint relevantes executados.
- [ ] Regra validada no nível adequado com oráculo independente.
- [ ] Contratos e integração real pertinentes verificados.
- [ ] Fluxo principal e negativos de alto risco executados.
- [ ] Persistência e efeito colateral observados quando necessários.
- [ ] Reprodução original repetida após correção.
- [ ] Regressões por impacto executadas após última mudança relevante.
- [ ] Teclado, estados e layout verificados nos ambientes pertinentes.
- [ ] Sem vazamento/ação não autorizada em integrações e ferramentas.
- [ ] Primeira falha, retries e evidências preservados.
- [ ] Limitações de runtime/host/modelo explícitas.

## 7. Entregar

- [ ] Artefatos localizáveis, execução e pré-requisitos descritos.
- [ ] Revisão/ambiente de cada evidência registrados.
- [ ] Migração e recuperação documentadas quando aplicáveis.
- [ ] Achados não resolvidos e riscos residuais explícitos.
- [ ] Nenhuma alegação de execução ou leitura ausente.
- [ ] Continuidade e próxima ação concretas.

Leitura: [integral/parcial] · Execução: [completa no escopo/parcial/não executada]
Resultado: [concluído no escopo/parcial/impedido]
Críticos abertos: [IDs] · Recomendação/condições: [texto]
