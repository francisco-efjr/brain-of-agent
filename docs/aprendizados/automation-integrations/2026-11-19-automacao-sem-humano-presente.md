---
data: 2026-11-19
tags: [automation-integrations, observabilidade-instrumentar, seguranca-hardening]
plugins: [automation-integrations, sre-observability, security-appsec]
agentes: [automation-integrations:third-party-auditor, sre-observability:reliability-reviewer]
contexto: "Automações agendadas de uma IA local num PC Windows (Agendador de Tarefas e agenda do OpenJarvis)"
tipo_de_sessao: pesquisa
modelo: claude-opus-5-5
---
# Automação sem humano presente: ficha aprovada, limites e parada de emergência

Origem: tema `local-ai-core/automacao/`, com 25 fontes diretas e 63 itens validados da casa. Detalhes em `local-ai-core/automacao/PESQUISA-AUTOMACAO.md`.

## Boas práticas confirmadas
- [Verificado na documentação] Definir antes o que a execução automática pode fazer, numa ficha aprovada; o que precisaria de aprovação vira pendência no log. Motivo: na hora não há a quem perguntar. Evidência: guia de agentes da OpenAI (humano em ação de alto risco), OWASP Agentic 2026 (cascata e agente fora do escopo).
- [Verificado na documentação] Limites no próprio Agendador: tempo máximo (o padrão é de três dias) e sem instâncias sobrepostas. Evidência: documentação do ScheduledTasks.
- [Verificado na documentação] Repetir só erro transitório, com espera exponencial e aleatória, teto de tentativas e disjuntor. Evidência: AWS Builders' Library, Fowler.
- [Verificado na documentação] Avisar só o que é urgente, importante, acionável e real; silêncio também é falha (dead man's switch). Evidência: SRE do Google, ensaio de Ewaschuk.
- [Verificado na documentação] Tarefa determinística não precisa de IA: script PowerShell no Agendador; IA só para julgamento, pela agenda do OpenJarvis.

## Armadilhas
- [Verificado na documentação] O FileSystemWatcher perde eventos quando o buffer estoura → combinar evento com conferência periódica.
- [Verificado na documentação] A documentação do OpenJarvis traz duas sintaxes para `jarvis scheduler create` → conferir com `--help`.
- [Inferido] Tarefa que roda sem usuário logado guarda senha no Agendador → tratar como R3.

## Pesquisa
| Fonte (URL) | Classe | Acesso | Achado |
| --- | --- | --- | --- |
| https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasksettingsset | A | 2026-11-19 | Limites da tarefa |
| https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter | A | 2026-11-19 | Tentativas e espera |
| https://sre.google/sre-book/eliminating-toil/ | A | 2026-11-19 | O que automatizar |
| https://open-jarvis.github.io/OpenJarvis/user-guide/scheduled-monitor/ | A | 2026-11-19 | Agenda do OpenJarvis |
| https://www.cisa.gov/back-business-data | A | 2026-11-19 | Backup 3-2-1 |

## Lacunas
- A casa não tinha itens sobre o Agendador de Tarefas do Windows nem sobre execução sem humano presente para agentes locais.

## Promoção sugerida
- `automation-integrations` / playbook: ficha de automação e regra "execução automática só faz o que a ficha aprovou".
