# Telemetria: métricas, logs, traces e OpenTelemetry

Para revisar instrumentação, nomes e cardinalidade de métricas, logging seguro, pipelines do Collector, upgrades de OpenTelemetry, telemetria do próprio Claude Code e análise de traces de apps com LLM. Consulta às fontes: 2026-10-10. Versões e nomes de variáveis mudam: confirme na documentação da versão instalada.

## Sumário

- [Sinais OpenTelemetry](#sinais-opentelemetry)
- [Pipeline do Collector: oficial × Suposição](#pipeline-do-collector-oficial--suposição)
- [Métricas: nomes, tipos e cardinalidade](#métricas-nomes-tipos-e-cardinalidade)
- [Instrumentação por tipo de sistema](#instrumentação-por-tipo-de-sistema)
- [Logging seguro](#logging-seguro)
- [Health checks](#health-checks)
- [Upgrade de OpenTelemetry](#upgrade-de-opentelemetry)
- [Telemetria do Claude Code no time](#telemetria-do-claude-code-no-time)
- [Saída de ferramentas para o agente](#saída-de-ferramentas-para-o-agente)
- [Traces de apps com LLM](#traces-de-apps-com-llm)
- [Lacunas](#lacunas)

## Sinais OpenTelemetry

Fonte: V-12 (opentelemetry.io, "Signals", Classe A, Verificado). Sinais suportados: **traces, metrics, logs e baggage**. Events (um tipo de log) e profiles estão em desenvolvimento/proposta: não prometa suporte estável. Coleta sozinha não dá diagnóstico: correlacione os sinais por operação (ID de requisição e contexto de trace) sem dado sensível (brain `entrega-e-operacao`).

Separe três usos que costumam ser misturados: **auditoria** (quem fez o quê, retenção longa, acesso restrito), **log de diagnóstico** (detalhe para depurar, retenção curta, redigido) e **métrica agregada** (barata, de baixa cardinalidade, base de SLO e alerta).

## Pipeline do Collector: oficial × Suposição

Fonte: opentelemetry.io/docs/collector/architecture (V-12).

**Oficial (Verificado):**
- Um pipeline por tipo de dado (traces, metrics, logs); cada componente precisa suportar o tipo do pipeline.
- Um receiver pode alimentar vários pipelines; um processor bloqueado pode bloquear os demais que dependem do mesmo receiver.
- Cada pipeline que cita um processor recebe **instância independente** dele.

**Suposição (vem de skill de terceiros, o11y-dev/opentelemetry-skill, Apache-2.0, Classe C; não consta na página do Collector):**
- `memory_limiter` como primeiro processor.
- OTLP gRPC como padrão e porta 4318 para HTTP (a página cita 4317; a 4318 não aparece).
- Sticky routing por trace ID para `tail_sampling`.
- Nunca expor `pprof`/`zpages` fora de rede de administração.
- `batch` como processor recomendado: a página do Collector **não** o menciona.

Como usar: ao revisar um `collector.yaml`, aponte cada item da lista acima como "recomendação não confirmada na página de arquitetura; confira na documentação específica do componente" antes de transformar em achado. Amostragem head × tail: lacuna (ver abaixo); descreva o trade-off como Suposição: head decide cedo e é barato mas não vê o resultado do trace; tail decide com o trace completo mas exige estado e roteamento por trace.

## Métricas: nomes, tipos e cardinalidade

Fonte: V-11 (prometheus.io/docs/practices/naming e /instrumentation, Classe A, Verificado).

| Regra | Bom | Ruim |
| --- | --- | --- |
| Prefixo de aplicação com uma palavra | `checkout_pedidos_total` | `pedidos` |
| Unidade base no plural, no nome | `http_request_duration_seconds` | `latency_ms` |
| Contador termina em `_total` **depois** da unidade | `process_cpu_seconds_total` | `process_cpu_total_seconds` |
| Razão de 0 a 1 | `cache_hit_ratio` (0–1) | percentual 0–100 |
| Nome do rótulo não entra no nome da métrica | `http_requests_total{method="GET"}` | `http_get_requests_total` |
| Contador para o que só sobe; medidor para o que sobe e desce | `queue_length` (medidor) | `rate()` sobre medidor |
| Exporte o timestamp do evento, não o tempo decorrido | `last_success_timestamp_seconds` | `seconds_since_last_success` |
| Contador de falhas **mais** contador de tentativas | `jobs_failed_total` + `jobs_total` | só a taxa pronta |
| Pré-inicialize séries com 0 | contador existe desde o start | série surge só no 1º erro (alerta nunca vê o "antes") |

**Cardinalidade.** Cada combinação de valores de rótulos é uma série. Guia da página: cardinalidade por métrica abaixo de 10 é um bom alvo; reavalie acima de 100 (o "10" é guia, não limite técnico). Nunca rotule por ID de usuário, e-mail, URL com ID ou trace ID; e-mail e user_id também são dado pessoal.

Estimativa (mostre a conta): séries = produto dos números de valores de cada rótulo × (buckets + `_sum` + `_count` se for histograma). Exemplo ilustrativo: `method` (5) × `route` (40) × `status` (8) = 1.600 séries de contador; como histograma com 12 buckets mais `+Inf`, `_sum` e `_count` (15 séries por combinação) ≈ 24.000 séries por instância. Acrescentar `user_id` com 100.000 valores multiplica por 100.000 (≈ 160 milhões de séries no contador). Use a **rota** (`/pedidos/{id}`), não o caminho cru.

Tenant em SaaS: `tenant_id` como rótulo só com limite de tenants conhecido e orçamento de séries; do contrário, agregue por plano ou faixa.

## Instrumentação por tipo de sistema

Fonte: V-11.

| Tipo | Meça | Exemplo |
| --- | --- | --- |
| Serviço online | Contagem de requisições, erros e latência (histograma) | `http_requests_total`, `http_request_duration_seconds` |
| Processamento offline (fila, stream) | Itens recebidos, em processamento, concluídos; idade do mais antigo | `items_in_total`, `items_inflight`, `items_out_total` |
| Lote (batch) | Momento do último sucesso e duração | `job_last_success_timestamp_seconds` |

Para o desenho de SLIs a partir destas métricas, veja [slo-error-budget.md](slo-error-budget.md).

## Logging seguro

Fonte: V-26 (claudecode-lab, Classe C, com correções; Verificado como leitura do artigo) e brain `entrega-e-operacao`.

- Logs estruturados (JSON) com **request ID** e contexto de trace (trace_id/span_id) para correlacionar com traces.
- Lista de **campos proibidos** versionada no repositório: senhas, tokens, cookies e cabeçalhos de autorização, chaves de API, e-mail, telefone, endereço, documento, texto bruto de prompt de LLM, corpo completo de requisição/resposta.
- **Teste que prove a redação**: fixture com valores sintéticos em cada campo proibido; o teste falha se algum aparecer na saída. Motivo: no artigo-fonte a lista do prompt (ampla) e a do código de exemplo (só 6 campos) não coincidiam; só um teste detecta essa divergência.
- Sem log de payload completo; registre tamanho, tipo, IDs opacos.
- Logging desde a primeira geração de código, não "depois".
- Nunca copie fixtures com formato de chave real (mesmo que inofensivas, acionam scanners de segredo).
- Alertas derivados do SLO (burn rate), não dos limiares de exemplo do artigo (5xx > 2% em 5 min com `for: 10m`; p95 > 1,5 s por 15 min são exemplos).

## Health checks

- Um health check **por dependência**, com timeout curto (exemplo do artigo: 800 ms por dependência; calibre).
- Readiness ≠ liveness (falha frequente listada no brain): liveness diz "reinicie-me"; readiness diz "não envie tráfego". Um liveness que consulta o banco reinicia toda a frota quando o banco cai.
- Health check não substitui SLI: "200 em /health" não prova que o fluxo do usuário funciona.

## Upgrade de OpenTelemetry

Fonte: V-28 (ollygarden/opentelemetry-agent-skills `otel-upgrade`, Apache-2.0, Classe B; destilação com atribuição a OllyGarden). Template: [relatorio-upgrade-otel.md](../assets/templates/relatorio-upgrade-otel.md).

1. Inspecione a evidência do repositório antes de escolher o fluxo (lockfiles, versões do SDK/agente, config).
2. Registre as versões **separadamente** para wrapper, distribuição e artefato.
3. Consulte as fontes primárias (changelog, release notes) e registre a **data da consulta**.
4. Separe "última estável" de "candidata validada".
5. Valide em **cópia isolada**, começando pela estável mais nova; se falhar, teste versões menores.
6. Ligue as mudanças de comportamento ao uso real do repositório (só o que o código usa importa).
7. Relate: Recomendação, Achados, Caminho proposto, Validação, Risco residual. Distinga resolução de dependência, compilação, aceitação de configuração e testes: cada um prova pouco por si.

Risco: o skill de origem não restringe execução de instaladores; a isolação é a salvaguarda. Este plugin não executa nem recomenda instalar nada.

## Telemetria do Claude Code no time

Fonte: V-13 (code.claude.com/docs/en/monitoring-usage, Classe A). Último terço da página não lido: confira nomes e versões na página atual.

Verificado:
- `CLAUDE_CODE_ENABLE_TELEMETRY=1` liga a telemetria.
- Desligados por padrão: `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_ASSISTANT_RESPONSES`, `OTEL_LOG_TOOL_DETAILS`, `OTEL_LOG_TOOL_CONTENT` (exige tracing), `OTEL_LOG_RAW_API_BODIES`.
- Ligados por padrão: `OTEL_METRICS_INCLUDE_SESSION_ID`, `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` e o seletor de atributos de recurso (a fonte o abrevia como `..._RESOURCE_ATTRIBUTES`; o prefixo `OTEL_METRICS_INCLUDE_` é Inferido do padrão dos outros dois: confira o nome completo na página).
- Traces são beta e exigem `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`.
- Configurações **gerenciadas** travam o destino OTLP (endpoint, protocolo, credenciais); os seletores de exportador não são travados sozinhos, a menos que também definidos ali (requer Claude Code v2.1.223 ou superior).
- O `.claude/settings.json` do repositório **ignora** as variáveis de exportador.
- `user.email` é sempre incluído quando disponível: trate o backend como dado pessoal.

Regras prontas: CM-01 em [claude-md-snippets.md](claude-md-snippets.md). JSON (desativado): [ferramentas-e-mcp.md](ferramentas-e-mcp.md). Checklist: prompts, respostas, detalhes e conteúdo de ferramenta desligados (ligar só em depuração autorizada, por tempo limitado, porque podem conter segredos e código); `session.id` e UUID da conta desligados em painéis compartilhados; nenhum token de coletor em `.claude/settings.json` nem em variável de ambiente de nuvem.

## Saída de ferramentas para o agente

Fonte: V-14 (Carlini, "Building a C compiler", Anthropic Engineering, 2026-02-05, Classe A; Ronacher, 2025-06-12, Classe C). Quando um agente (ou pessoa) lê a saída de teste, benchmark ou diagnóstico: poucas linhas no console e detalhe em arquivo de log de caminho fixo; `ERROR` e o motivo na **mesma linha** (para `grep`); agregados pré-calculados (contagens, taxas, p95); registre o comando e a saída reais, nunca a esperada; comando de start que recusa segunda instância (pidfile); arquivo de progresso com abordagens descartadas; teto de iterações em laços de benchmark. Ressalva: o caso do compilador tem oráculo forte (GCC); em SRE vale como princípio.

## Traces de apps com LLM

Fonte: V-30 (Hamel Husain, Evals FAQ, 2026-09-18, Classe B, "opiniões fortes" do autor). Para um app com LLM em produção:

1. Anote manualmente pelo menos **30 traces** antes de pedir sugestões a um agente.
2. Foque na **primeira falha** do trace (é possível etiquetar todas as independentes).
3. Continue até **saturar**: ~100 traces é um mínimo, não critério de parada.
4. Prefira asserção em código a juiz LLM quando a falha é verificável.

Convenções de atributos GenAI (spans e métricas `gen_ai.*`) pertencem ao plugin `llm-ai-agents`; aqui entram pipeline, SLO, alerta e custo/latência.

## Lacunas

- SDKs por linguagem, propagação de contexto e semantic conventions: não lidos.
- Amostragem head × tail: sem fonte A; trade-off descrito como Suposição.
- Política de retenção da telemetria do Claude Code: não verificada.
