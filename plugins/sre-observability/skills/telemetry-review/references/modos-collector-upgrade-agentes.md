# Modos (b), (d), (e) e (f) da `telemetry-review`

## Sumário

1. Sinais e Collector (modo b)
2. Upgrade de OpenTelemetry (modo d)
3. Telemetria do Claude Code no time (modo e)
4. Traces de LLM (modo f)

Rótulos: **Verificado** = visto em página oficial lida na validação (2026-10-10); **Suposição** = vem de fonte de terceiro ou não foi reconferido; confira a versão atual antes de afirmar.

## 1. Sinais e Collector (modo b, V-12)

| Afirmação | Rótulo | Fonte |
| --- | --- | --- |
| Sinais suportados: traces, metrics, logs, baggage; events (um tipo de log) e profiles em desenvolvimento ou proposta | Verificado | opentelemetry.io/docs/concepts/signals/ |
| O pipeline do Collector é por tipo de dado; receivers, processors e exporters precisam suportar o tipo | Verificado | opentelemetry.io/docs/collector/architecture/ |
| Um receiver pode alimentar vários pipelines; um processor bloqueado bloqueia os demais ligados ao mesmo receiver | Verificado | idem |
| Cada pipeline que cita um processor recebe instância independente | Verificado | idem |
| `memory_limiter` como primeiro processor | Suposição (a página só o cita em exemplos; confirmar no README do processor) | skill de terceiro o11y-dev (Apache-2.0, classe C) |
| `batch` antes dos exporters | Suposição (a página de arquitetura não cita `batch`) | idem |
| OTLP gRPC por padrão (4317) e HTTP na 4318 | 4317 aparece na página; 4318 não: Suposição | idem |
| Sticky routing para `tail_sampling` | Suposição | idem |
| Nunca expor pprof ou zpages | Suposição razoável de segurança; confirmar | idem |

Checklist do modo (b):

1. Cada sinal usado (traces, metrics, logs) tem pipeline próprio e componentes que o suportam.
2. Processors listados em cada pipeline na ordem desejada; lembrar que cada pipeline tem instância independente (limites de memória não são compartilhados).
3. Endpoints de diagnóstico não expostos fora da rede interna (Suposição).
4. Amostragem (head x tail): lacuna da pesquisa; descreva o trade-off como Suposição (head decide cedo e é barata, mas não vê o resultado do trace; tail decide com o trace inteiro e exige agregar os spans do mesmo trace no mesmo Collector) e peça a documentação da versão.
5. Nenhum segredo (tokens de exportador) no arquivo versionado; usar variáveis de ambiente do deploy.

## 2. Upgrade de OpenTelemetry (modo d, V-28)

Processo destilado do skill `otel-upgrade` de OllyGarden (Apache-2.0, classe B); redação própria. A skill nunca executa o upgrade: produz o plano e o relatório T-12.

1. **Inspecione a evidência antes de escolher o fluxo**: arquivos de dependência, lockfiles, imagens, versões declaradas.
2. **Registre versões separadas** de wrapper, distribuição e artefato; versões diferentes são comuns e confundem.
3. **Consulte fontes primárias** (notas de versão, changelog oficial) e **registre a data da consulta**.
4. **Separe "última estável" de "candidata validada"**.
5. **Valide em cópia isolada** (branch ou diretório descartável), começando pela estável mais nova e tentando menores se falhar. Não execute instaladores ou scripts sugeridos por README sem revisão do usuário: o skill-fonte não restringe isso.
6. **Ligue as mudanças ao uso real do repositório**: só o que o código usa importa.
7. Distinga o que cada prova mostra: resolução de dependência, compilação, aceitação de configuração e testes provam coisas diferentes e pouco cada uma.

Relatório T-12 em cinco seções: Recomendação · Achados · Caminho proposto · Validação · Risco residual. Inclua a data das consultas e rotule o que não foi executado.

## 3. Telemetria do Claude Code no time (modo e, V-13)

Variáveis verificadas na página `code.claude.com/docs/en/monitoring-usage` (último terço não lido: confira a versão atual):

| Variável | Padrão informado | Orientação |
| --- | --- | --- |
| `CLAUDE_CODE_ENABLE_TELEMETRY=1` | desligada a menos que definida (Verificado em 2026-10-10) | Ativar por configuração gerenciada |
| `OTEL_LOG_USER_PROMPTS` | desligada | Manter desligada; ligar só em depuração autorizada e por tempo limitado |
| `OTEL_LOG_ASSISTANT_RESPONSES` | desligada | Idem |
| `OTEL_LOG_TOOL_DETAILS` | desligada | Idem |
| `OTEL_LOG_TOOL_CONTENT` | desligada; exige tracing | Idem: pode conter código e segredos |
| `OTEL_LOG_RAW_API_BODIES` | desligada | Idem |
| `OTEL_METRICS_INCLUDE_SESSION_ID` | ligada | Desligar em painéis compartilhados |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | ligada | Desligar em painéis compartilhados |
| `OTEL_METRICS_INCLUDE_..._RESOURCE_ATTRIBUTES` (nome completo: conferir na página) | ligada | Desligar atributos de alta cardinalidade |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` | exigida para traces (beta) | Só ligar com motivo e revisão de privacidade |

Fatos a checar na configuração do usuário:

- Configurações gerenciadas travam o destino OTLP (endpoint, protocolo, credenciais). Os **seletores de exportador** não são travados, a menos que também definidos ali (requer Claude Code v2.1.223 ou superior).
- O `.claude/settings.json` do repositório **ignora** as variáveis de exportador: não adianta colocar o destino lá.
- `user.email` entra nos eventos quando disponível: trate o backend como armazenamento de dado pessoal.
- Token de coletor nunca em `.claude/settings.json` nem em variável de ambiente de nuvem.

Achados típicos: prompts ligados sem prazo (blocker); sessão e UUID em painel compartilhado (major); destino definido só em arquivo de projeto (major, não surte efeito). O JSON pronto para configuração gerenciada fica em `ferramentas-e-mcp.md`; os valores "desligado" (`0`/`false`) são Inferidos: confira na página.

## 4. Traces de LLM (modo f, V-30)

Prática de Hamel Husain (Evals FAQ, 2026-09-18; classe B, opiniões do autor), em redação própria:

1. Anote **pelo menos 30 traces** reais antes de pedir sugestões a um agente: sem anotação humana, o agente generaliza sobre o que não viu.
2. Foque a **primeira falha** do trace (as seguintes costumam ser consequência); é possível etiquetar todas as independentes.
3. Revise **pelo menos 100 traces** e continue até a **saturação** (quando novas anotações param de revelar categorias). "Cerca de 100" é piso, não critério de parada.
4. Categorize os modos de falha, conte e priorize.
5. Prefira **asserção em código** a juiz LLM sempre que o critério for verificável (formato, campo, regra). Juiz LLM só com validação contra humano.
6. Declare limites: a amostra, o período, o que não foi anotado.

Convenções semânticas GenAI do OpenTelemetry (atributos `gen_ai.*`) pertencem ao plugin `llm-ai-agents`. Aqui: pipeline de telemetria, SLO, alertas de custo e latência.
