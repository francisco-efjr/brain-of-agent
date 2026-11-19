# Pesquisa: core de automação de rotinas

Data: 2026-11-19 · Pesquisador: Claude Opus 5.5 (Claude Code) · Consultas de busca novas: 16 · Fontes diretas: 25 (2 da casa, 23 externas) · Itens validados da casa reaproveitados: 63.

## 1. Achados principais

1. **Automatize toil, não tudo.** Toil é trabalho manual, repetitivo, automatizável e sem valor duradouro (S-01). Fluxo previsível é melhor como script do que como agente (H-02 V-08).
2. **Sem humano presente, a ação espera.** Ação de alto risco ou irreversível passa para um humano (G-03); a OWASP lista falhas em cascata e agentes fora do escopo entre os riscos de agentes, com disjuntores, orçamento de tentativas e observabilidade como mitigação (G-01). Daí: execução automática só faz o que a ficha aprovou; o resto vira pendência.
3. **Injeção sem testemunha.** Automação que lê conteúdo não confiável não pode ter ao mesmo tempo dados sensíveis e poder de mudar o sistema ou comunicar para fora (G-02, H-02 V-20).
4. **Repetir com cuidado.** Só erro transitório, espera exponencial com aleatoriedade, teto de tentativas e prazo (S-04, S-09); operações idempotentes tornam a repetição segura (S-05); disjuntor para de tentar depois de falhas seguidas (S-06).
5. **Limites no próprio Agendador.** Tempo máximo (o padrão é de três dias), sem instâncias sobrepostas (T-01, T-02); códigos de resultado distinguem "ainda rodando" de "já havia outra instância" (T-03).
6. **Avisar pouco e bem.** Aviso deve ser urgente, importante, acionável e real; avisar pelo sintoma e deixar a causa no log (S-02, S-03, H-01 V-04, V-05). Silêncio também é falha, por isso o dead man's switch (S-07).
7. **Eventos falham calados.** O FileSystemWatcher perde eventos quando o buffer estoura (T-06): evento mais conferência periódica.
8. **Backup é 3-2-1 e restaurável** (S-08).
9. **O OpenJarvis tem agenda própria** para tarefas com IA (`scheduled-monitor`, `jarvis scheduler`, resumo da manhã) (O-01, O-02, O-03).

## 2. Validação da esteira para automação

| Passo | Em automação | Evidência |
| --- | --- | --- |
| 0 Classificar | Pausar é R1; criar, alterar, reativar é R2; admin, sem usuário logado, apagar, enviar para fora é R3 | G-01, G-03 |
| 1 Estruturar | Vale automatizar? Que gatilho? Que critério de sucesso? | S-01 |
| 2 a 5 Visão a conceber | Ficha com ações fechadas, limites, avisos e como desligar | T-01, T-02, S-03 |
| 6 Produzir | Script idempotente com parada geral, log e disjuntor | S-05, S-06 |
| 7 Testar de novo | Uma execução em ensaio com log revisado | H-01 V-17 |
| 8 Validar o escopo | O usuário aprova a ficha (PLANO) | G-03 |
| 9 Implementar | Registrar a tarefa e conferir com Get-ScheduledTask | T-01 |
| 10 Verificar e registrar | Observar as primeiras execuções; revisar na data | S-07 |

O estudo acrescenta ao tema um passo próprio, que a esteira de ações sob demanda não tinha: **definir antes o que a execução sem humano pode fazer**, porque na hora não haverá a quem perguntar.

## 3. Decisões de desenho

- **Ficha antes da automação**, em `IA-Operador\automacoes\`, para que o usuário saiba o que roda no PC dele e como desligar.
- **Pasta `\IA-Operador\` no Agendador** e prefixo `IA-` para listar e desligar tudo de uma vez.
- **Arquivo `PARAR`** como parada geral simples, que funciona mesmo se o modelo estiver fora do ar.
- **Cartão no perfil padrão**: automação entra completa só quando o usuário montar o tema.

## 4. Limites

- Buscas conferidas por trechos; o comportamento exato de `StartWhenAvailable` e da autodesativação da tarefa deve ser conferido no primeiro uso.
- A documentação do OpenJarvis traz duas sintaxes para `jarvis scheduler create`.
- O modelo de script não foi executado num Windows nesta sessão.
- Casos de eval `designed_not_executed`.

## 5. Fontes

### 5.1 Pesquisa validada da casa (H)

| ID | Arquivo | Itens | Usado em |
| --- | --- | --- | --- |
| H-01 | `docs/dev-segments/research/sre-observability/VALIDATED.md` | 30 aprovados | Sinais de ouro, ruído de alertas, gate antes de mudar, cascata e retries, logs sem segredo |
| H-02 | `docs/dev-segments/research/automation-integrations/VALIDATED.md` | 33 aprovados | Fluxo ou agente, webhooks com duplicatas, trifecta por fluxo, jobs não interativos |

### 5.2 Windows e ferramentas (T)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| T-01 | [New-ScheduledTaskSettingsSet](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasksettingsset) | A | Busca | Tempo máximo, StartWhenAvailable, RestartCount |
| T-02 | [TaskSettings.MultipleInstances](https://learn.microsoft.com/en-us/windows/win32/taskschd/tasksettings-multipleinstances) | A | Busca | Sem execuções sobrepostas |
| T-03 | [Task Scheduler error and success constants](https://learn.microsoft.com/en-us/Windows/win32/taskschd/task-scheduler-error-and-success-constants) | A | Busca | Códigos de resultado |
| T-04 | [Register-ScheduledTask](https://learn.microsoft.com/powershell/module/scheduledtasks/register-scheduledtask) | A | Busca | Registro da tarefa |
| T-05 | [Microsoft: desktop wakes up unexpectedly](https://learn.microsoft.com/en-us/troubleshoot/windows-client/setup-upgrade-and-drivers/desktop-wakes-up-unexpectedly-from-sleep-hibernation) | A | Busca | Wake timers |
| T-06 | [FileSystemWatcher (.NET)](https://learn.microsoft.com/dotnet/fundamentals/runtime-libraries/system-io-filesystemwatcher) | A | Busca | Eventos perdidos |
| T-07 | [Microsoft Learn: Power Automate for desktop](https://learn.microsoft.com/en-us/training/modules/robotic-process-automation/2-pad) | A | Busca | Fluxos de interface |
| T-08 | [BurntToast](https://github.com/windos/burnttoast) | B | Busca | Notificações pelo PowerShell |

### 5.3 Confiabilidade (S)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| S-01 | [Google SRE: Eliminating Toil](https://sre.google/sre-book/eliminating-toil/) | A | Busca | O que automatizar |
| S-02 | [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) | A | Busca | Sintoma e causa |
| S-03 | [Ewaschuk: My Philosophy on Alerting](https://docs.google.com/document/d/199PqyG3UsyXlwieHaqbGiWVa8eMWi8zzAn0YfcApr8Q/mobilebasic) | A | Busca | Avisos acionáveis |
| S-04 | [AWS Builders' Library: Timeouts, retries and backoff with jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter) | A | Busca | Tentativas e espera |
| S-05 | [AWS Builders' Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-apis/) | A | Busca | Idempotência |
| S-06 | [Fowler: Circuit Breaker](https://www.martinfowler.com/bliki/CircuitBreaker.html) | A | Busca | Disjuntor |
| S-07 | [Healthchecks: monitoring cron jobs](https://healthchecks.sre.cfainstitute.org/docs/monitoring_cron_jobs/) | B | Busca | Dead man's switch |
| S-08 | [CISA: Back up business data](https://www.cisa.gov/back-business-data) | A | Busca | Regra 3-2-1 |
| S-09 | [AWS Architecture Blog: Exponential backoff and jitter](https://aws.amazon.com/jp/blogs/architecture/exponential-backoff-and-jitter/) | A | Busca | Variantes de jitter |

### 5.4 OpenJarvis (O)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| O-01 | [OpenJarvis: scheduled monitor](https://open-jarvis.github.io/OpenJarvis/user-guide/scheduled-monitor/) | A | Busca | Preset e `jarvis scheduler` |
| O-02 | [OpenJarvis: scheduled ops](https://open-jarvis.github.io/OpenJarvis/tutorials/scheduled-ops) | A | Busca | Sintaxe alternativa e `schedules.toml` |
| O-03 | [OpenJarvis: morning digest](https://open-jarvis.github.io/OpenJarvis/user-guide/morning-digest/) | A | Busca | Resumo da manhã |

### 5.5 Segurança de agentes (G)

| ID | Fonte | Classe | Status | Usado em |
| --- | --- | --- | --- | --- |
| G-01 | [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | A | Íntegra (PDF extraído, tema Windows) | ASI08 cascata, ASI10 agente fora do escopo |
| G-02 | [Meta: Agents Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/) | A | Busca | Conteúdo não confiável sem poder de mudar |
| G-03 | [OpenAI: A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | A | Busca | Humano em ação de alto risco e após falhas |

Contagem: 2 (H) + 8 (T) + 9 (S) + 3 (O) + 3 (G) = 25 fontes diretas, mais 63 itens validados da casa.
