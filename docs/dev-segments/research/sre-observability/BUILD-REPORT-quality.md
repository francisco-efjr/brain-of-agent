# BUILD-REPORT de qualidade de prompt e conteúdo técnico: plugin `sre-observability`

Data: 2026-10-10 · Papel: validador independente de qualidade (rubrica D1 a D12, 0 a 100) · Escopo: `plugins/sre-observability` inteiro.

Declaração de independência: o validador é um modelo da mesma família dos construtores. Isto reduz o viés de autoria (leitura adversarial, fatos reconferidos em fontes oficiais), mas **não é validação externa**. As notas são julgamento de leitura, não medição; os evals continuam `designed_not_executed`.

## 1. Método

1. Leitura integral: `playbook`, 9 skills de tarefa, `prompts`, 4 agentes, README, 12 evals (prompt e graders). Biblioteca de prompts: leitura de PR-01 a PR-24 e PR-27 a PR-36 (34 de 36; PR-25 e PR-26 só por trechos). Referências do playbook: amostra (`slo-error-budget`, `alertas-e-sinais`, `fontes`, `telemetria-otel`, `ferramentas-e-mcp`, `decisoes-e-tradeoffs` por trechos); templates por amostra de links e placeholders.
2. Varreduras mecânicas: CAPS e ameaças (nenhuma fora de invariantes de segurança), marcadores de pendência, 67 URLs (todas 200, exceto placeholders de exemplo e o repositório `brain-of-agent`, 404 sem autenticação), slugs de skills de outros plugins (`debug-causa-raiz`, `infra-troubleshoot`, `perf-audit` existem).
3. Fidelidade técnica contra fontes oficiais (seção 4).
4. Correção direta; reverificação com `verify_plugin.py` e `claude plugin validate`.

Nenhum critério de reprovação automática foi encontrado (sem instrução de inventar resultado, sem ação destrutiva sem confirmação, sem obediência a conteúdo externo, sem cópia sem licença, frontmatter válido, sem segredo). Os revisores (`reliability-reviewer`, `perf-analyst`, `postmortem-scribe`, `incident-support`) têm só `Read, Grep, Glob`.

## 2. Tabela arquivo | antes | depois | correções

| Arquivo | Antes | Depois | Correções |
| --- | --- | --- | --- |
| `skills/playbook/SKILL.md` | 92 | 94 | Gotcha de Lighthouse e limiar "ruim" corrigido (fato); `allowed-tools` confirmado na doc e acrescentado "nem `Write`"; fronteiras: plugin vizinho ausente é dito, não fingido |
| `skills/alert-review/SKILL.md` | 90 | 94 | Tirado `Write` de `allowed-tools`; frase do 35× reescrita (estava truncada e enganosa, ver 4.4); referência a "lacuna 7.3.3 da síntese" removida |
| `skills/incident-triage/SKILL.md` | 92 | 93 | Sem mudança de conteúdo; verificada coerência com agente |
| `skills/postmortem/SKILL.md` | 91 | 93 | Tirado `Write` de `allowed-tools` (já pedia confirmação do caminho) |
| `skills/root-cause-investigation/SKILL.md` | 88 | 92 | Gotchas de procedência de terceiros reduzidos a 2 itens de valor operacional (economia de contexto) |
| `skills/slo-design/SKILL.md` | 91 | 93 | Tirado `Write` de `allowed-tools`; aviso de permissão normal |
| `skills/telemetry-review/SKILL.md` | 86 | 93 | Contradição com o eval corrigida: e-mail não vai para log como alternativa; identificador interno pode ir a log ou trace |
| `skills/telemetry-review/references/*` | n/a | n/a | Mesma correção no exemplo TL-01; `CLAUDE_CODE_ENABLE_TELEMETRY` passa a Verificado; ID interno `EV-06` trocado por nome do eval |
| `skills/performance-engineering/SKILL.md` | 85 | 92 | Limiares "ruim" passam a Verificados (4.1); Lighthouse por modo (4.2); código 99 do k6 Verificado (4.3); `Write` fora do pré-aprovado; CRLF misto normalizado |
| `skills/runbook/SKILL.md` | 91 | 93 | Tirado `Write` de `allowed-tools`; CRLF misto normalizado |
| `skills/release-health/SKILL.md` | 87 | 92 | Texto dizia `Write` "pré-aprovado só para o relatório", mas a pré-aprovação não filtra caminho: removido e reescrito |
| `skills/prompts/SKILL.md` | 90 | 91 | Sem mudança; pendência do validador estrutural resolvida por decisão (seção 5) |
| `skills/prompts/references/prompt-library.md` (PR-01 a PR-24) | 88 | 92 | Fonte de PR-17 rebaixada de "A" para B; CAPS não essenciais removidos; nota sobre códigos P-nn/C-nn (catálogo fora do plugin); código 99 do k6 Verificado |
| `skills/prompts/references/prompts-resiliencia-e-operacao.md` (PR-25 a PR-36) | 88 | 92 | Limiar "ruim" e Lighthouse corrigidos em PR-25; CAPS não essenciais removidos |
| `agents/incident-support.md` | 91 | 92 | Sem mudança; verificado contra doc de subagentes (campos aceitos, hooks/mcpServers/permissionMode ignorados em plugin) |
| `agents/reliability-reviewer.md` | 92 | 92 | Sem mudança; aritmética de RV-02/03 e burn rate refeita |
| `agents/postmortem-scribe.md` | 92 | 92 | Sem mudança; cinco perguntas conferidas no capítulo |
| `agents/perf-analyst.md` | 88 | 92 | Limiares "ruim" Verificados; Lighthouse por modo; código 99 do k6 |
| `README.md` | 86 | 90 | "SLO (8 passos)" corrigido para 9; semântica de `allowed-tools` explicitada (sem `Write` pré-aprovado) |
| `evals/slo-primeiro-checkout` | 90 | 90 | Sem mudança |
| `evals/alerta-cpu-vs-burn-rate` | 91 | 92 | Sem mudança no caso; skill alinhada ao critério de burn |
| `evals/incidente-log-com-instrucao-hostil` | 92 | 92 | Sem mudança |
| `evals/postmortem-notas-com-culpa` | 91 | 91 | Sem mudança |
| `evals/latencia-pos-deploy-quer-timeout` | 90 | 90 | Sem mudança |
| `evals/metricas-cardinalidade` | 84 | 91 | A skill e o exemplo mandavam mover o e-mail para log, enquanto o grader reprova isso: alinhados |
| `evals/carga-em-producao-sem-autorizacao` | 91 | 91 | Sem mudança |
| `evals/canario-antes-depois` | 89 | 89 | Sem mudança |
| `evals/negativo-fronteira-crashloop-build` | 90 | 90 | Sem mudança |
| `evals/lighthouse-inp-e-campo` | 80 | 90 | Premissa factual corrigida: critério dizia que o Lighthouse nunca mede INP e que o limiar "ruim" não é do web.dev; ambos imprecisos (4.1, 4.2) |
| `evals/runbook-keyword-em-wiki-e-comando-destrutivo` | 92 | 92 | Sem mudança |
| `evals/prompt-pronto-revisao-de-alertas` | 88 | 88 | Sem mudança |
| `evals/pergunta-pontual-burn-rate` (novo) | n/a | 90 | Caso novo: proporcionalidade; PASS/FAIL observáveis |
| `evals/negativo-refatorar-funcao-python` (novo) | n/a | 90 | Segundo caso negativo (sobredisparo) com `min: 0, max: 0, arm: both` |
| `skills/playbook/references/*`, `assets/templates/*` | amostra ≥ 85 | amostra ≥ 87 | Correções de fato em `decisoes-e-tradeoffs` (K9, K13), `checklist-completo` (SRE-111, SRE-112), `claude-md-snippets`, `performance-e-carga`, `padroes-e-antipadroes`, `alertas-e-sinais` (35×), `fontes` (URLs do web.dev; `brain-of-agent` não verificável), `ferramentas-e-mcp` (variáveis OTel), `slo-error-budget` (ID interno) |

Média antes (30 itens avaliados individualmente): 89,2. Média depois: 91,6. Mínimo depois: 88. Nenhum item abaixo de 80.

Dimensões que mais seguraram a nota (honestamente, nenhum item chega a 95): D9 (economia: o playbook e a biblioteca são densos; os blocos "Plataformas" repetidos em quatro agentes duplicam conteúdo) e D5 (poucos exemplos negativos nos prompts da biblioteca).

## 3. Segurança e direitos autorais

- Nenhuma skill pré-aprova `Bash` sem padrão. `root-cause-investigation` pré-aprova só `Bash(git log *)`, `Bash(git diff *)`, `Bash(git show *)`. Agora nenhuma skill pré-aprova `Write`: gravar arquivo passa pelo pedido normal de permissão (a doc confirma que `allowed-tools` pré-aprova e não restringe).
- Injeção: todas as 9 skills de tarefa e os 4 agentes declaram conteúdo lido como dado; 3 evals testam isso com texto hostil (log, wiki com comentário HTML dirigido a agentes, keyword `SRE-COMPLETO` em material colado). O `SRE-COMPLETO` só ativa por pedido do usuário.
- Sem segredos. Telemetria do Claude Code: padrões desligados, `user.email` tratado como dado pessoal.
- Direitos autorais: livros SRE do Google, Prometheus, OTel, k6, web.dev e Gregg apenas destilados; terceiros MIT/Apache-2.0 (gstack, superpowers, wshobson, awesome-copilot, grafana/skills, ollygarden) creditados e sem trecho literal; a tabela de burn rate é aritmética refeita (Workbook Table 5-8 conferida). Nada a corrigir.

## 4. Correções factuais (fonte e data de consulta: 2026-10-10)

1. **Limiares "ruim" de Core Web Vitals.** O plugin dizia que 4 s, 500 ms e 0,25 "não estão no web.dev" (Inferido). Estão nos artigos individuais: `web.dev/articles/lcp` (LCP acima de 4,0 s), `web.dev/articles/inp` (INP acima de 500 ms) e `web.dev/articles/cls` (CLS acima de 0,25). A página `web.dev/articles/vitals` só traz os de "bom". Rótulo passou a Verificado, com a ressalva de qual página traz o quê. Aplicado em playbook, performance-engineering, perf-analyst, decisões K13, checklist SRE-112, prompt PR-25, fontes e no grader do eval.
2. **"Lighthouse não mede INP".** Vale para o modo de navegação padrão (usa TBT como proxy; `web.dev/articles/inp` diz que ferramentas de laboratório que só observam o carregamento não reportam INP). O modo timespan (fluxos de usuário, desde o Lighthouse 9.6, post do Chrome de 2022) mede INP das interações roteirizadas. A afirmação absoluta foi qualificada em 9 arquivos e no eval. A página `developer.chrome.com/docs/lighthouse/performance/lighthouse-user-flows` deu 404; a confirmação do timespan veio do post do blog do Chrome via busca, então esse ponto específico é **Inferido** com fonte B.
3. **Código de saída 99 do k6 em threshold falho.** O plugin o marcava Inferido (vindo do brain). Material da Grafana (learning paths sobre exit code e thresholds) confirma 99; a página oficial de thresholds diz apenas "diferente de zero". Marcado Verificado com a ressalva e o comando `echo $?`. "Resumo compacto desde o k6 1.0" segue Inferido (a doc atual diz que compacto é o padrão e cita remoção de recursos legados na v2.0.0, sem confirmar a versão de origem).
4. **Exemplo 35× do Workbook.** O texto do plugin ("um limiar único de 35× ... nunca alertaria nessa abordagem") estava truncado. A fonte (Método 4, tabela de prós e contras) diz que uma queima de 35× abaixo do limiar escolhido nunca alerta e ainda consome o orçamento de 30 dias em 20,5 h (baixo recall). Reescrito em `alert-review`, `alertas-e-sinais` e `padroes-e-antipadroes`.
5. **Confirmados sem alteração:** Table 5-8 do Workbook (14,4/6/1, 1 h/5 min, 6 h/30 min, 3 d/6 h; 2%, 5%, 10%; janela curta = 1/12 da longa); Workbook desaconselha `for:` em alerta de SLO (com nota de rodapé sobre ruído efêmero); convenções de nome do Prometheus (prefixo, unidade plural, `_total` depois da unidade, `_ratio`, evitar IDs e e-mails em rótulos); cinco perguntas de revisão do capítulo de postmortem e ausência de seção de linha do tempo; sinais do OTel (traces, metrics, logs, baggage; events e profiles em desenvolvimento ou proposta); `allowed-tools` pré-aprova e aceita lista separada por espaço ou vírgula; `disable-model-invocation` bloqueia a chamada automática; plugins ignoram `hooks`, `mcpServers` e `permissionMode` em agentes e aceitam `maxTurns`; variáveis de telemetria do Claude Code (`CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_METRICS_EXPORTER`, `OTEL_LOGS_EXPORTER`, `OTEL_EXPORTER_OTLP_PROTOCOL` sem padrão, `OTEL_LOG_USER_PROMPTS` e correlatas desligadas por padrão, `.claude/settings.json` do repositório ignora variáveis de exportador, `user.email` incluído quando disponível); aritmética de budget, Little (4.167 sessões, 167 req/s, 667 req/s a 4×) e cardinalidade (histograma = buckets + 2).
6. **Inconsistência interna:** README dizia que `slo-design` tem 8 passos; a skill tem 9 (a referência do playbook tem 8 do livro). README corrigido.

## 5. Decisão sobre as pendências do relatório estrutural

1. **Referências temáticas de `prompts`** (5 arquivos previstos): decisão de **reduzir o plano**, não criar. Os 36 prompts já estão em dois arquivos com sumário e índice "situação para prompt" no `SKILL.md`; dividir em cinco só acrescentaria carga de contexto e links. O blueprint prevê "+ arquivos por subtema se grande", e a skill instrui a abrir só a seção necessária. Registrado como desvio aceito do SYNTHESIS 4.6.
2. **Marketplace** (`.claude-plugin/marketplace.json` ausente na raiz de `dev-segments`): problema do repositório, não do plugin. O README segue a convenção `francisco-efjr/brain-of-agent`, igual a `backend-api`. A URL do GitHub respondeu 404 sem autenticação; pode ser repositório privado, então a instalação por esse caminho é Não verificável para terceiros.
3. **Semântica de `allowed-tools`**: agora Verificada na documentação de skills (pré-aprova, não restringe).
4. **Evals**: 14 casos (12 originais mais 2 novos), todos `designed_not_executed`; `claude plugin eval` exige Claude Code 2.1.269 ou superior e o CLI local da construção é anterior (Não verificável localmente).

## 6. Pendências (decisão ou ação do usuário)

1. Executar `claude plugin eval .` com Claude Code atualizado (3 execuções por caso, ablação) e ler os transcripts; só então citar taxa de acerto. Os graders `llm` usam números de fontes de 2026-10-10.
2. Publicar o marketplace e confirmar a visibilidade do repositório `brain-of-agent` antes de divulgar o comando de instalação do README.
3. Confirmar o modo timespan do Lighthouse na documentação atual (a página de user flows retornou 404 nesta consulta) e, se desejado, trocar a fonte B por uma página oficial estável.
4. Itens ainda sem fonte classe A (já declarados como lacunas pelo plugin): profilers por linguagem, consulta lenta de banco, head versus tail sampling, estrutura oficial de runbook, template de postmortem do PagerDuty, crash reporting e RUM de mobile. Não foram inventados; seguem rotulados Não verificável.
5. Opcional: reduzir a repetição do bloco "Plataformas" nos quatro agentes (ganho de D9) e criar um eval por agente isolado e um para o modo `SRE-COMPLETO` legítimo (lacunas já listadas em `evals/README.md`).
6. Os códigos P-nn, C-nn e PAD-nn na coluna "Por que funciona" da biblioteca remetem a `docs/foundation/prompt-principles.md`, que não viaja com o plugin; foi acrescentada uma nota, mas o ideal é manter só o motivo escrito.

## 7. Rótulos

Verificado: fatos da seção 4 itens 1, 3 (parcial), 4, 5; resultado do verificador e do validador oficial; contagens; estado dos links (curl). Inferido: modo timespan do Lighthouse (fonte B); notas D1 a D12. Não verificável: execução dos evals, visibilidade do repositório `brain-of-agent`, marketplace. Não aplicável: direitos autorais (sem material a corrigir).
