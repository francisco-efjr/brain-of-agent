# Checklist operacional QA-COMPLETO: análise, implementação e revalidação

Como usar: somente no modo `QA-COMPLETO` (pedido explícito do usuário; não amplia permissões). As caixas de leitura só se marcam **após** ler; elas não indicam execução de produto. Adaptado do checklist do brain-of-agent (MIT) ao conjunto de arquivos deste plugin.

Objeto: <projeto ou fluxo> · Versão: <commit ou build> · Ambiente: <ambiente> · Data: <AAAA-MM-DD>
Pedido: <texto e escopo> · Modo: <QA-COMPLETO> · Permissões: <análise apenas / edições locais em [escopo] / outras>

## A. Leitura e fontes

| Arquivo ou fonte | Revisão ou data | Estado (completo/parcial/ausente) | Decisão relevante | Retomada |
| --- | --- | --- | --- | --- |

- [ ] Lote 1: `SKILL.md` do playbook, `checklist-completo`, `padroes-e-antipadroes`, `decisoes-e-tradeoffs`
- [ ] Lote 2: `estrategia-e-risco`, `design-de-testes`, `unitarios-e-integracao`
- [ ] Lote 3: `automacao-web-e2e`, `bugs-e-evidencia`, `evals-e-ia-llm`
- [ ] Lote 4: `claude-md-snippets`, `ferramentas-e-mcp`, `fontes`, e os templates
- [ ] Lote 5: `SKILL.md` e `references/` das skills de tarefa (arquivo inexistente na instalação = "ausente", cobertura parcial)
- [ ] Requisitos, código e materiais do objeto inventariados; fonte de verdade dos requisitos identificada

## B. Cobertura por área

A = aplicável · NA = não aplicável (com motivo) · NV = não verificável.

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

## C. Registro por item (uma linha por critério observável; não agrupe falhas diferentes)

Análise: pendente / conforme / não conforme / NV / NA · Implementação: não necessária / proposta / não autorizada / feita / impedida · Revalidação: pendente / passou / falhou / NV / NA.

| ID | Área e risco | Critério e fonte | Análise e evidência | Implementação | Revalidação e evidência | Pendência |
| --- | --- | --- | --- | --- | --- | --- |

## D. Analisar

Integridade das funções existentes · positivos, negativos, limites e transições · permissões, outro usuário ou tenant, expiração · duplicação, concorrência, timeout, recuperação · estados vazio/carregando/erro/desabilitado · contratos, precisão, fuso, persistência · acessibilidade · segurança e privacidade (sem exploração) · performance e observabilidade · IA: fontes, injeção, ferramentas, variabilidade · asserções, isolamento e falsos verdes. Cada item sem execução recebe NA ou NV com motivo na tabela C.

## E. Implementar (só se autorizado)

[ ] correção priorizada e ligada ao achado · [ ] contratos preservados ou mudança acordada · [ ] teste de regressão que falhou antes · [ ] dados, migrações, compatibilidade · [ ] diff sem alterações alheias (`git diff --stat`) · [ ] nenhum teste afrouxado, pulado ou removido sem decisão humana

## F. Revalidar

[ ] reprodução original contra a correção · [ ] esperado comparado a oráculo independente · [ ] efeito persistido e ausência de duplicação · [ ] regressões por impacto · [ ] ambiente, versão e revisão da evidência correspondem à entrega · [ ] primeira falha e retries preservados · [ ] falhas restantes e NV registrados

## G. Encerramento

Leitura: <integral / parcial> · Execução: <completa no escopo / parcial / não executada> · **Gate:** <Concluído / Parcial / Impedido>
Achados abertos por severidade: <contagens e IDs> · Riscos residuais: <...> · Recomendação: <resultado e condições> · Próximo passo: <...>

Nunca escreva "QA completo aprovado" com leitura ou execução parcial. Revisão por quem implementou é autoavaliação.
