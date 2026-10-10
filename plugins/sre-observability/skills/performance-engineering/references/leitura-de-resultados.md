# Leitura de resultados de carga

## Sumário

1. Ordem de leitura
2. Métricas do k6 e o que dizem
3. Padrão observado para interpretação provável
4. Gargalo, sinal e confirmação
5. Curva latência x vazão e capacidade útil
6. Erros de leitura frequentes

Fonte: brain `performance.md` (MIT, conteúdo próprio, adaptado) e V-21, V-23; tabelas são heurísticas de diagnóstico: **Inferido** até confirmadas com traces e métricas do sistema testado.

## 1. Ordem de leitura

1. Veredito: thresholds aprovados ou reprovados, no **patamar** (a rampa e o aquecimento distorcem o resumo; conclua pela série temporal).
2. `dropped_iterations` e `vus_max` versus `maxVUs`: a carga pedida foi entregue?
3. Erros: taxa, tipo (timeout do cliente, 429, 5xx, "verde" com corpo de erro).
4. Latência por endpoint (p50, p95, p99) contra o SLO.
5. Saturação do alvo e do **gerador**.
6. Só então hipóteses de gargalo.

## 2. Métricas do k6

| Métrica | Leitura |
| --- | --- |
| thresholds (aprovado ou reprovado) | Veredito; leia primeiro |
| `http_req_duration` por tag `name` | Latência por endpoint contra o SLO |
| `http_req_waiting` | Tempo até o primeiro byte: é o servidor |
| `http_req_blocked`, `http_req_connecting`, `http_req_tls_handshaking` | Altos indicam conexões esgotadas ou gerador sobrecarregado |
| `dropped_iterations` > 0 | A taxa pedida não foi entregue; a carga medida é menor que a pretendida |
| `vus_max` igual a `maxVUs` | Faltou VU: aumente ou investigue por que a latência subiu |
| `checks` | Só reprova se houver threshold sobre ele |

## 3. Padrão observado para interpretação provável

| Padrão | Interpretação provável |
| --- | --- |
| p50 e p95 sobem juntos | Todas as requisições mais lentas: recurso compartilhado saturado (CPU, banco) |
| p50 estável, p95 e p99 sobem | Parte das requisições espera: fila de pool, pausas de GC, lock, cache miss em parte das chaves, um nó ruim, retries |
| Erros antes de a latência subir | Limite de conexões, rate limit, timeout curto, portas ou arquivos esgotados |
| Latência cai enquanto o erro sobe | O sistema passou a falhar rápido (circuit breaker, 503): não é melhora |
| Piora contínua com carga constante | Vazamento de memória, crescimento de tabela ou de fila (típico de soak) |

## 4. Gargalo, sinal e confirmação

| Gargalo | Sinal | Confirmação |
| --- | --- | --- |
| Pool de conexões do banco | Latência alta com CPU do banco baixa | Conexões pendentes no pool; span "aguardando conexão" |
| Threads ou workers do servidor | Fila na entrada, CPU da aplicação baixa | Threads ocupadas no máximo |
| GC | Picos periódicos de p99 | Logs de GC; heap após coleta subindo |
| Locks | Lentidão em escrita, deadlocks | Eventos de espera no banco (ex.: `pg_stat_activity` no PostgreSQL) |
| N+1 | Latência cresce com o tamanho da lista | Trace com dezenas de spans SQL iguais por requisição |
| Cache miss | Piora quando a massa varia | Taxa de acerto do cache caindo |
| Terceiro | Spans externos lentos, 429 do provedor | Latência do span de saída; limite contratado |

Correlação: filtre no APM o endpoint e a janela do patamar, abra os traces mais lentos e compare com um rápido do mesmo endpoint; o span que cresce é o suspeito. Um cabeçalho próprio (`X-Execucao-Carga: <id>`) isola o tráfego do teste.

## 5. Curva latência x vazão e capacidade útil

Subindo a taxa de chegada, a vazão acompanha e a latência fica quase plana; no **joelho** a vazão deixa de subir e a latência dispara porque as requisições passam a esperar em fila. A capacidade útil é a vazão em que o p95 cruza o SLO, **antes** do joelho, não o ponto em que o sistema cai. Opere com margem abaixo dele e diga qual margem foi assumida (Suposição).

Percentis: p99 estável exige milhares de amostras por endpoint; 2 min a 5 req/s (cerca de 600 amostras) não sustentam conclusão sobre p99. **Nunca tire média de percentis**: agregue histogramas ou amostras brutas. A chance de uma sessão de 20 requisições pegar ao menos uma acima do p99 é 1 - 0,99^20, cerca de 18%.

## 6. Erros de leitura frequentes

- Concluir pelo resumo do teste inteiro (mistura aquecimento, rampa e patamar).
- Ignorar `dropped_iterations`: o "passou" vale para uma carga menor que a pedida.
- Gerador saturado (CPU acima de ~70% a 80%, `ulimit -n` baixo): o gargalo é o teste.
- Modelo fechado sem think time e coordinated omission: p99 otimista, às vezes por ordens de grandeza.
- Cache e CDN: mesma URL repetida dá 100% de acerto; varie parâmetros e decida se o alvo é a borda ou a origem.
- Declarar capacidade de produção a partir de ambiente menor sem rótulo **Extrapolado**.
- Comparar execuções com massa, base ou versão diferentes sem dizer.
