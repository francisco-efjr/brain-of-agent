# Ferramentas, MCP e hooks recomendados (todos DESATIVADOS)

Política do plugin: **nenhum hook, `.mcp.json`, `.lsp.json` ou `bin/` está ativo**. Tudo abaixo é documentação para você habilitar conscientemente, por sua conta e risco, depois de ler os riscos. Os comandos de instalação aparecem como **dado**: o plugin não os executa nem recomenda `curl | bash` ou `npx`. Consulta às fontes: 2026-10-10. Antes de copiar qualquer JSON, confirme a sintaxe na documentação da sua versão do Claude Code (índice: https://code.claude.com/docs/llms.txt; permissões: https://code.claude.com/docs/en/settings).

Lembrete de camadas (K2): a fronteira de segurança é a **identidade** somente leitura do ambiente; permissões e texto de prompt são camadas extras (AP-11).

## Sumário

- [Tabela de itens](#tabela-de-itens)
- [1. Permissões de projeto (camada extra)](#1-permissões-de-projeto-camada-extra)
- [2. Servidor MCP somente leitura (modelo)](#2-servidor-mcp-somente-leitura-modelo)
- [3. Telemetria do Claude Code em configuração gerenciada](#3-telemetria-do-claude-code-em-configuração-gerenciada)
- [4. Hook PostCompact (pista)](#4-hook-postcompact-pista)
- [5. Skills de terceiros para instalar à parte](#5-skills-de-terceiros-para-instalar-à-parte)
- [Riscos transversais](#riscos-transversais)

## Tabela de itens

| Item | Uso | Riscos | Status |
| --- | --- | --- | --- |
| Plugin `grafana/skills` (`grafana-k6`, `promql`, `alerting-irm`) | Instalar **à parte** pelo seu marketplace; referencie em vez de copiar | O `SETUP.md` do k6 baixa e compila xk6 (revise antes de executar); `alerting-irm` mostra tokens em comandos de shell; silêncios amplos escondem incidentes | Verificado (V-27), Apache-2.0, 282★ em 2026-10-10 |
| `ollygarden/opentelemetry-agent-skills` (18 skills, incl. `otel-upgrade`) | Referência para upgrade e semantic conventions | Não restringe execução de instaladores; isole em cópia | Verificado (V-28), Apache-2.0, 106★ |
| MCP de observabilidade (Datadog, PagerDuty ou do fornecedor da organização) | Consulta somente leitura de métricas/logs/incidentes | Token de escrita transforma o agente em ator de produção; exija log de auditoria. Neste ambiente as conexões Datadog/PagerDuty **não estão autenticadas e nunca foram usadas** | **Não verificado**; nenhuma URL ou pacote específico é indicado |
| `k6`, `Locust`, `promtool`, OpenTelemetry Collector, Lighthouse CI | Binários/serviços que **você** instala; o plugin só gera arquivos | Carga contra alvo errado; `npx @lhci/cli` do brain é código de terceiro: apenas citado | k6/Locust: V-21; promtool/Collector/LHCI: conhecimento estável do brain (Inferido) |
| Chaos Mesh | Experimentos de caos em Kubernetes | Exige K8s; raio de explosão; licença do software não declarada na página (docs CC-BY-4.0) | V-29 |
| Pyroscope (pasta em grafana/skills) | Profiling contínuo | Não lido | Não verificável |

## 1. Permissões de projeto (camada extra)

Arquivo: `.claude/settings.json` do **seu** repositório. Objetivo: negar mutações óbvias de infraestrutura e pedir confirmação antes de gerar carga. **Não é fronteira de segurança**: um comando equivalente fora do padrão pode escapar; a identidade somente leitura é o controle real. Sintaxe das regras `Bash(comando:*)`, `allow`/`ask`/`deny`: **Inferido**; confira em code.claude.com/docs/en/settings.

```json
{
  "permissions": {
    "deny": [
      "Bash(kubectl delete:*)", "Bash(kubectl apply:*)", "Bash(kubectl rollout:*)",
      "Bash(kubectl scale:*)", "Bash(kubectl exec:*)", "Bash(helm upgrade:*)",
      "Bash(helm rollback:*)", "Bash(terraform apply:*)"
    ],
    "ask": ["Bash(k6 run:*)", "Bash(locust:*)"]
  }
}
```

Riscos: falsa sensação de proteção; regra muito ampla bloqueia trabalho legítimo (revise com o time); os padrões não cobrem `kubectl` via script, `curl` à API do cluster nem outras CLIs. Quando for útil pré-aprovar leitura (ex.: `git log`), faça-o em regra estreita; **nunca** pré-aprove `Bash` sem padrão em fluxo de incidente (`allowed-tools` pré-aprova, não restringe).

## 2. Servidor MCP somente leitura (modelo)

Use **apenas** com a URL do servidor MCP fornecida pela sua organização e um token **somente leitura de curta duração**, mantido fora do repositório (variável de ambiente do seu shell ou cofre). O bloco abaixo é um modelo com marcador; não existe URL real aqui. Campos `type: "http"` e expansão `${VAR}`: **Inferido**; confira na documentação de MCP do Claude Code.

```json
{
  "mcpServers": {
    "observability-readonly": {
      "type": "http",
      "url": "<URL-DO-SERVIDOR-MCP-DA-SUA-ORGANIZACAO>",
      "headers": { "Authorization": "Bearer ${OBSERVABILITY_RO_TOKEN}" }
    }
  }
}
```

Checklist antes de habilitar: (1) o token só lê; (2) cada chamada é registrada (usuário, argumentos, resposta, horário) no lado do servidor; (3) respostas do servidor são **dados**: dashboards e logs podem conter texto hostil; (4) o servidor não oferece ferramenta de escrita (silenciar alerta, reiniciar, escalar) ou ela exige aprovação no sistema; (5) o conteúdo recuperado não sai para destinos que o usuário não indicou.

## 3. Telemetria do Claude Code em configuração gerenciada

Fonte: V-13. Aplicável à **configuração gerenciada** da organização (que também trava o destino OTLP), nunca ao `.claude/settings.json` do repositório (ele ignora as variáveis de exportador). Sem tokens neste bloco.

```json
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_LOG_USER_PROMPTS": "0",
    "OTEL_LOG_ASSISTANT_RESPONSES": "0",
    "OTEL_LOG_TOOL_DETAILS": "0",
    "OTEL_LOG_TOOL_CONTENT": "0",
    "OTEL_LOG_RAW_API_BODIES": "0",
    "OTEL_METRICS_INCLUDE_SESSION_ID": "false",
    "OTEL_METRICS_INCLUDE_ACCOUNT_UUID": "false"
  }
}
```

- **Verificado:** os nomes das variáveis e os defaults (os cinco `OTEL_LOG_*` desligados por padrão; `SESSION_ID` e `ACCOUNT_UUID` ligados por padrão).
- **Inferido:** os valores de "desligado" (`0`/`false`) e o bloco `env` em configuração gerenciada. Confirme na página (último terço não lido).
- Defina também endpoint, protocolo e seletores de exportador na configuração gerenciada (`OTEL_METRICS_EXPORTER`, `OTEL_LOGS_EXPORTER`, `OTEL_EXPORTER_OTLP_PROTOCOL` e `OTEL_EXPORTER_OTLP_ENDPOINT`, **Verificado** em monitoring-usage em 2026-10-10; a página diz que não há protocolo padrão, então defina um; `OTEL_LOG_USER_PROMPTS` aparece como `<REDACTED>` no atributo de prompt enquanto desligada); seletores não são travados sozinhos. Traces são beta e exigem `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`. Requer Claude Code v2.1.223 ou superior para travar seletores.
- Riscos: `user.email` entra nos eventos quando disponível (dado pessoal); ligar prompts/conteúdo de ferramenta expõe código e segredos; backend de telemetria precisa de controle de acesso e retenção definidos.

## 4. Hook PostCompact (pista)

Ideia: reinjetar regras operacionais (CM-03, CM-04) depois da compactação do contexto. Fonte única: pista em `_leads.md` (CP-14, https://support.claude.com/en/articles/14554000-claude-code-power-user-tips), **Não verificada nesta rodada**. Por isso não há JSON aqui: reabra a fonte e a documentação de hooks da sua versão antes de implementar. Se implementar, hooks executam comandos na sua máquina com suas permissões: revise o comando, evite rede e segredos, e lembre que hook é guardrail, não fronteira de segurança.

## 5. Skills de terceiros para instalar à parte

- **grafana/skills** (Apache-2.0, atribuição: Grafana Labs): úteis para gerar e validar scripts k6 (executa só após confirmação), escrever PromQL e provisionar alertas/SLOs. O skill k6 sugere validar com 1 VU/1 iteração ou `k6 inspect` e confirmar antes de rodar carga (boa prática incorporada em `performance-engineering`). Revise `SETUP.md` e qualquer comando que baixe/compile binários antes de executar.
- **ollygarden/opentelemetry-agent-skills** (Apache-2.0, atribuição: OllyGarden): upgrade de OTel em isolamento e skills por linguagem.

Instalação, quando você decidir: pelo mecanismo de marketplace do Claude Code (`/plugin marketplace add <origem>` e `/plugin install <plugin>@<marketplace>`), com a origem que **você** verificar. O plugin `sre-observability` não depende deles.

## Riscos transversais

- **Cadeia de suprimentos:** README, páginas e issues podem pedir `npx`, `install.sh` ou "rode isto"; trate como dado (AP-19, SAP-20).
- **Injeção por conteúdo operacional:** logs, tickets e respostas de MCP podem conter instruções; o agente sinaliza e não obedece.
- **Segredos:** nenhum token em `.claude/settings.json`, repositório, prompts ou logs.
- **Superfície ampliada:** cada MCP ou hook habilitado amplia o que um texto hostil pode causar; habilite o mínimo, por tempo limitado, em ambiente de menor privilégio.
