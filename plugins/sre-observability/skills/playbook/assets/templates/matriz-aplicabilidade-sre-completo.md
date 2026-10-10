# Matriz de aplicabilidade — modo SRE-COMPLETO

Template T-14. Forma adaptada do protocolo de modo completo do brain-of-agent (`protocolo-completo.md`, MIT, conteúdo próprio). Preencha **antes** de analisar. "Aplicável" exige referência lida; "Não aplicável" exige motivo; "Não verificável" (NV) quando falta acesso ou dado. Isto é cobertura da matriz com limitações honestas, não uma lista de caixas artificialmente verdes. O modo não amplia permissões: nenhum acesso a produção, carga, caos ou mudança de configuração além do pedido.

**Pedido do usuário (citação curta):** [".. SRE-COMPLETO .."] · **Escopo:** [serviço/repositório/ambientes] · **Acesso:** [nenhum / somente leitura / escrita limitada] · **Tipo de entrega:** [auditoria só relata / implementação no escopo]

## Inventário de leitura (lotes)

| Lote | Arquivos | Estado (lido / parcial / ausente) | Observação |
| --- | --- | --- | --- |
| L1 | checklist-completo, slo-error-budget, alertas-e-sinais | [..] | [..] |
| L2 | telemetria-otel, incidentes-e-postmortem | [..] | [..] |
| L3 | performance-e-carga, resiliencia-canario-capacidade | [..] | [..] |
| L4 | padroes-e-antipadroes, decisoes-e-tradeoffs, claude-md-snippets, ferramentas-e-mcp, fontes | [..] | [..] |

## Matriz (20 áreas)

| # | Área | Estado (aplicável / NA / NV) | Motivo | Evidência | Referência lida | Skill ou agente |
| --- | --- | --- | --- | --- | --- | --- |
| A1 | SLI/SLO | [..] | [..] | [..] | slo-error-budget | slo-design |
| A2 | Error budget e política | [..] | [..] | [..] | slo-error-budget | slo-design |
| A3 | Alertas | [..] | [..] | [..] | alertas-e-sinais | alert-review |
| A4 | Dashboards e sinais | [..] | [..] | [..] | alertas-e-sinais | alert-review |
| A5 | Métricas e instrumentação | [..] | [..] | [..] | telemetria-otel | telemetry-review |
| A6 | Logs | [..] | [..] | [..] | telemetria-otel | telemetry-review |
| A7 | Traces, OTel e Collector | [..] | [..] | [..] | telemetria-otel | telemetry-review |
| A8 | Telemetria de LLM/agentes | [..] | [..] | [..] | telemetria-otel | telemetry-review |
| A9 | Incidente: papéis e severidade | [..] | [..] | [..] | incidentes-e-postmortem | incident-triage |
| A10 | Runbooks | [..] | [..] | [..] | incidentes-e-postmortem | runbook |
| A11 | Postmortem | [..] | [..] | [..] | incidentes-e-postmortem | postmortem |
| A12 | Plantão e toil | [..] | [..] | [..] | slo-error-budget | alert-review |
| A13 | Capacidade e autoscaling | [..] | [..] | [..] | resiliencia-canario-capacidade | performance-engineering |
| A14 | Resiliência de dependências | [..] | [..] | [..] | resiliencia-canario-capacidade | reliability-reviewer |
| A15 | Canário e release health | [..] | [..] | [..] | resiliencia-canario-capacidade | release-health |
| A16 | Teste de carga | [..] | [..] | [..] | performance-e-carga | performance-engineering |
| A17 | Performance de frontend | [..] | [..] | [..] | performance-e-carga | performance-engineering |
| A18 | Profiling de backend e banco | [..] | [..] | [..] | performance-e-carga | performance-engineering |
| A19 | Caos | [..] | [..] | [..] | resiliencia-canario-capacidade | playbook |
| A20 | Segurança do agente: identidade, aprovação, telemetria do Claude Code | [..] | [..] | [..] | incidentes-e-postmortem, telemetria-otel | telemetry-review |

## Resultado por área aplicável

| # | Achados (IDs SRE-nn) | Mudança feita no escopo | Revalidação (comando e saída) | Estado final |
| --- | --- | --- | --- | --- |
| [A3] | [SRE-21] | [regra reescrita em rascunho] | [promtool check rules: saída colada / não executado] | [concluído / parcial / impedido] |

## Revalidação e revisão independente

- Checks invalidados por mudanças posteriores: [..]
- Revisão independente com `reliability-reviewer` em contexto limpo: [feita / não feita]. **Autoavaliação do mesmo modelo não é validação externa.**
- Resultado: [concluído no escopo / parcial / impedido]. Falha crítica impede recomendação favorável; média de notas não a compensa. Leitura obrigatória ausente torna o modo parcial.

## Limitações e riscos residuais

[Lacunas conhecidas (profiling por linguagem, consulta lenta de banco, PromQL oficial de burn rate, amostragem OTel), acessos que faltaram, o que ficou Não verificável.]
