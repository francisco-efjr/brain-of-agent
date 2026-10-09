# Checklist operacional QA — análise, implementação e revalidação

Objeto: [projeto/fluxo] · Versão: [commit/build] · Ambiente: [ambiente]
Pedido: [texto/escopo] · Modo: [QA-COMPLETO/seletivo]
Permissões: [análise/edições locais/outras] · Data: [data]

## A. Leitura e fontes

| Arquivo/fonte | Revisão | Leitura completa/parcial/ausente | Decisão relevante | Retomada |
| --- | --- | --- | --- | --- |

- [ ] Router e skill QA lidos.
- [ ] 15 referências de conhecimento lidas, sem truncamentos pendentes.
- [ ] Protocolo e todos os templates lidos.
- [ ] Contexto multidisciplinar lido ou ausência declarada.
- [ ] Workflows selecionados lidos e disponibilidade de ferramentas confirmada.
- [ ] Requisitos, código e materiais do objeto inventariados.

Essas caixas só são marcadas após leitura. Elas não indicam execução de produto.

## B. Cobertura por área

Use A = aplicável, NA = não aplicável com motivo, NV = não verificável.

| Área | A/NA/NV | Motivo e fonte | IDs de itens | Risco remanescente |
| --- | --- | --- | --- | --- |
| Produto/requisitos | | | | |
| UX/conteúdo | | | | |
| UI/design | | | | |
| Arquitetura | | | | |
| Frontend/app | | | | |
| Backend/API | | | | |
| Dados | | | | |
| QA/automação | | | | |
| Acessibilidade | | | | |
| Segurança/privacidade | | | | |
| Performance/confiabilidade | | | | |
| IA/RAG/agente | | | | |
| CI/operação | | | | |
| Processo/documentação | | | | |

## C. Registro por item

Uma linha por critério observável. Não agrupe falhas diferentes.
Estados de análise: pendente/conforme/não conforme/NV/NA.
Estados de implementação: não necessária/proposta/não autorizada/feita/impedida.
Estados de revalidação: pendente/passou/falhou/NV/NA.

| ID | Área/risco | Critério e fonte | Análise e evidência | Implementação/alteração | Revalidação e evidência | Pendência |
| --- | --- | --- | --- | --- | --- | --- |

## D. Itens a analisar

- [ ] Integridade das funções e regras existentes.
- [ ] Positivos, negativos, limites e transições relevantes.
- [ ] Permissões, dados de outro usuário/tenant e expiração.
- [ ] Duplicação, concorrência, timeout e recuperação.
- [ ] Estados vazio/carregando/erro/desabilitado e conteúdo extremo.
- [ ] Contratos, precisão, fuso, persistência e efeitos colaterais.
- [ ] Acessibilidade e comportamento da plataforma pertinente.
- [ ] Segurança, privacidade, dependências e segredos.
- [ ] Performance, observabilidade e operação conforme risco.
- [ ] IA: fontes, injeção, ferramentas, variabilidade e evidência honesta.
- [ ] Asserções, isolamento e falsos verdes na suíte existente.

Para cada item sem execução, associe NA ou NV com motivo na tabela C.

## E. Itens a implementar quando autorizados

- [ ] Correção priorizada e ligada ao achado.
- [ ] Contratos preservados ou mudança explicitamente acordada.
- [ ] Teste de regressão necessário criado/ajustado.
- [ ] Estados, mensagens e recuperação corrigidos.
- [ ] Dados/migrações/compatibilidade considerados.
- [ ] Documentação e configuração pertinentes atualizadas.
- [ ] Diff revisado, sem alterações alheias ao escopo.

## F. Itens a revalidar

- [ ] Reprodução original executada após correção.
- [ ] Resultado observado comparado ao oráculo independente.
- [ ] Efeito persistido e ausência de duplicação verificados quando necessários.
- [ ] Regressões por impacto executadas.
- [ ] Ambiente e revisão da evidência correspondem à entrega.
- [ ] Primeira falha e retries preservados.
- [ ] Falhas restantes e NV registrados.

## G. Encerramento

Leitura: [integral/parcial] · Execução: [completa no escopo/parcial/não executada]
Achados abertos por severidade: [contagens e IDs]
Riscos residuais: [riscos] · Recomendação: [resultado e condições]
Próximo passo: [ação necessária]
