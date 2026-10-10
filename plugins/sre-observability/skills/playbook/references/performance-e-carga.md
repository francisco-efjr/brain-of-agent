# Performance e testes de carga

Para planejar e interpretar testes de carga, performance de frontend, profiling e regressão. Base: `brains/qa/references/performance.md` do brain-of-agent (conteúdo próprio do usuário, MIT, adaptado; **não reverificado contra fontes externas**, rótulo Inferido onde indicado) + V-19, V-20, V-21, V-25. Consulta às fontes: 2026-10-10. Este plugin **não executa carga**: planeja, gera rascunho de script e lê resultados que o usuário executou.

## Sumário

- [Tipos de teste e a pergunta de cada um](#tipos-de-teste-e-a-pergunta-de-cada-um)
- [Antes de começar (7 itens)](#antes-de-começar-7-itens)
- [Modelagem da carga](#modelagem-da-carga)
- [Métricas que importam](#métricas-que-importam)
- [k6: limiares do SLO e leitura da saída](#k6-limiares-do-slo-e-leitura-da-saída)
- [Outras ferramentas](#outras-ferramentas)
- [Execução](#execução)
- [Análise: onde está o gargalo](#análise-onde-está-o-gargalo)
- [Performance no CI e regressão](#performance-no-ci-e-regressão)
- [Frontend: Core Web Vitals](#frontend-core-web-vitals)
- [Profiling e flame graphs](#profiling-e-flame-graphs)
- [Antipadrões](#antipadrões)
- [Lacunas](#lacunas)

## Tipos de teste e a pergunta de cada um

Escolha pela pergunta de negócio; o mesmo script serve a vários tipos. Fonte dos tipos: k6 "Test types" (V-21; URL correta `https://grafana.com/docs/k6/latest/testing-guides/test-types/`; a antiga `.../load-test-types/` dá 404) + brain.

| Tipo | Pergunta que responde | Perfil típico |
| --- | --- | --- |
| Smoke | O script funciona e o sistema responde sem erro? | 1–2 usuários, 1–2 min; **sempre antes dos outros** |
| Carga (average-load) | No pico normal esperado cumprimos o SLO? | rampa até o pico previsto, patamar de 15–30 min |
| Estresse | Acima do esperado, como degrada? Volta ao normal depois? | degraus acima do pico até violar o SLO; observe a recuperação |
| Pico (spike) | Uma subida abrupta derruba? O autoscaling chega a tempo? | de normal a 5–10× em segundos, depois volta |
| Resistência (soak) | Rodando horas, algo vaza (memória, conexões, disco, fila)? | carga normal por 4–12 h, cobrindo jobs noturnos e rotação de log |
| Capacidade (breakpoint) | Qual a vazão máxima **dentro do SLO**? | taxa crescente até o p95 cruzar o SLO |
| Escalabilidade | Dobrar instâncias dobra a vazão? | mesma rampa com 1, 2 e 4 instâncias |
| Volume | Com base 10× maior as consultas seguem no SLO? | carga moderada sobre massa grande |

Perfil simples (rampa, platô, descida) vence "montanha-russa" (V-21).

## Antes de começar (7 itens)

1. **Pergunta de negócio por escrito.** "O checkout aguenta 4× o pico de 2025 com p95 < 800 ms?" é testável; "ver se está rápido" não tem critério de sucesso nem de parada.
2. **SLI e SLO.** SLI é a medida (p95 de `POST /pedidos`, taxa de erro, vazão); SLO é o alvo ("p95 < 800 ms, p99 < 2 s, erro < 0,5% a 120 req/s por 30 min"). Sem SLO o relatório vira opinião; se o time não tem, proponha um a partir da latência atual (APM) e marque **Suposição**.
3. **Ambiente representativo:** mesma topologia, instâncias iguais ou proporcionais, base com volume parecido (com 1.000 linhas, consulta sem índice é rápida). Extrapolar de ambiente menor é palpite: diga.
4. **Autorização e janela** combinadas com quem opera aplicação, banco, rede, CDN/WAF e nuvem (cada provedor tem política): carga sem aviso parece ataque. Registre volume máximo, horário, contato e **como interromper**.
5. **Terceiros** (pagamento, antifraude, SMS) em stub com latência realista. Carregar sandbox de terceiro mede o terceiro, esbarra em limite de taxa e pode violar termos de uso.
6. **Dados** sintéticos e variados (repetir usuário e produto mede cache e contenção de linha) e plano de limpeza.
7. **Monitoramento ligado antes do primeiro request:** APM/traces, CPU e memória por camada, pool de conexões, banco (consultas lentas, locks), filas **e o próprio gerador**.

## Modelagem da carga

**Fontes de números:** analytics (sessões/hora, páginas por sessão), logs de acesso/gateway (req por endpoint por minuto), APM. Use a **hora de pico**, e dentro dela o minuto de pico, não a média do dia. Reproduza o **mix** real de transações (ele muda o gargalo).

**Think time e pacing.** Think time é a pausa entre ações da sessão; pacing, o intervalo entre inícios de iterações. Sem think time, 100 VUs disparam como milhares de pessoas. Sorteie a pausa numa faixa (2–5 s) para evitar ondas sincronizadas.

**Modelo aberto × fechado** (K10):

| | Aberto (taxa de chegada) | Fechado (usuários virtuais) |
| --- | --- | --- |
| Quem dita a carga | chegadas por segundo, independentes da resposta | N usuários; cada um só envia após a resposta |
| Sistema lento | as chegadas continuam e a fila cresce, como na vida real | a carga cai sozinha: o teste alivia o sistema |
| Representa | site público, API, app | população fixa (200 atendentes, pool de workers) |
| Ferramenta | k6 `*-arrival-rate`; Gatling `injectOpen`; JMeter Open Model Thread Group | k6 `ramping-vus`; Gatling `injectClosed`; Locust (padrão); Thread Group do JMeter |

Para web e API públicas use modelo **aberto**; o fechado subestima a latência exatamente onde interessa (coordinated omission). Esta recomendação vem do brain (Inferido, não reverificada externamente).

**Lei de Little: L = λ × W.** Exemplo: 50.000 sessões na hora de pico, 5 min (300 s) cada. λ = 50.000 ÷ 3.600 ≈ 13,9 sessões/s; L ≈ 13,9 × 300 ≈ **4.167 sessões simultâneas**; com 12 requisições por sessão ≈ **167 req/s**. Black Friday com fator 4× (pico do evento anterior ÷ pico de dia comum): ≈ 16.700 sessões e ≈ 667 req/s; some a margem do negócio e **diga de onde veio o fator**. A mesma lei dimensiona o gerador: VUs ≈ iterações/s × duração da iteração (10 it/s de 8 s ≈ 80 VUs; reserve folga para quando a latência subir).

## Métricas que importam

- **Média engana.** 99 requisições de 100 ms e uma de 10 s dão média de 199 ms. Numa sessão de 20 requisições, a chance de pegar ao menos uma acima do p99 é 1 − 0,99²⁰ ≈ 18%.
- **Percentis:** p50 (típico), p95 e p99 (cauda); máximo serve para investigar, não como SLO. p99 estável exige milhares de amostras por endpoint (2 min a 5 req/s não sustentam conclusão sobre p99).
- **Nunca tire média de percentis** (de instâncias ou de minutos): agregue histogramas ou amostras brutas.
- **Vazão:** se a carga sobe e a vazão não, saturou.
- **Taxa de erro** incluindo timeouts do cliente e "erros verdes" (200 com corpo de erro ou página de manutenção): o script checa conteúdo.
- **Saturação** explica a latência: USE por recurso, RED por serviço (ver [alertas-e-sinais.md](alertas-e-sinais.md)).
- **Coordinated omission.** No modelo fechado, quando o servidor trava 2 s, cada VU espera e deixa de enviar as requisições desse intervalo; as amostras ruins nunca são medidas e o p99 sai otimista. Mitigação: modelo aberto, ferramentas que corrigem pela taxa pretendida e, no k6, vigiar `dropped_iterations`.

## k6: limiares do SLO e leitura da saída

Fonte: k6 docs "Thresholds" (V-21, Classe A) e "Test types"; Locust MIT. Sintaxe conferida na versão `next` da documentação, não em `latest`: **confira na versão instalada** (`k6 version`).

Verificado: limiar na forma `agregação operador valor` (`p(95)<300`); falha de limiar encerra o k6 com **código de saída não-zero** (99 segundo o brain, Inferido), o que reprova o pipeline; **checks sozinhos não afetam o código de saída** (use `checks: ['rate>0.99']` para torná-los reprovadores); `abortOnFail` interrompe o teste quando o limiar falha e `delayAbortEval` adia a avaliação para coletar amostras; na nuvem a avaliação é a cada 60 s.

Snippet mínimo (valores **ilustrativos**; derive do SLO). Script completo reduzido em [k6-limiares-slo.js.md](../assets/templates/k6-limiares-slo.js.md):

```js
export const options = {
  thresholds: {
    http_req_failed: ['rate<0.005'],
    http_req_duration: [{ threshold: 'p(95)<300', abortOnFail: true, delayAbortEval: '30s' }],
  },
};
```

**Valide o próprio limiar** (Inferido, trilha de aprendizado da Grafana citada em V-21): uma execução que **deve passar** e outra com valor estrito que **deve falhar**. Limiar que nunca falha não protege nada.

**Como ler o resultado** (ordem de leitura; brain, Inferido):

| Métrica | Leitura |
| --- | --- |
| thresholds ✓/✗ | veredito; leia primeiro |
| `http_req_duration` por tag `name` | latência por endpoint contra o SLO |
| `http_req_waiting` | tempo até o primeiro byte: é o servidor |
| `http_req_blocked`, `http_req_connecting`, `http_req_tls_handshaking` altos | conexões esgotadas ou gerador sobrecarregado |
| `dropped_iterations` > 0 | a taxa pedida não foi entregue: você **não mediu a carga que acha que mediu** |
| `vus_max` = `maxVUs` | faltou VU; aumente ou investigue a latência |

O resumo mistura aquecimento, rampa e patamar; conclusões sobre o patamar vêm da série temporal. A tag `name` agrupa URLs com ID (sem ela, cada ID vira uma série). O módulo `k6/browser` mede Web Vitals sob carga (padrão híbrido: carga por HTTP + 1–5 VUs de navegador); cada VU de navegador é um Chromium inteiro.

## Outras ferramentas

| Ferramenta | Escolha quando | Cuidado |
| --- | --- | --- |
| k6 | time com JS/TS, teste como código no repositório, CI | protocolos além de HTTP/gRPC/WebSocket dependem de extensões |
| Locust (MIT, V-21) | time Python, lógica de usuário complexa; modo headless para CI; execução distribuída | modelo fechado por padrão; um processo usa um núcleo: distribua com `--master`/`--worker` |
| JMeter | protocolos variados (JDBC, JMS, LDAP, FTP, SOAP) | `.jmx` é XML difícil de revisar; execute em modo não-GUI; desligue listeners durante a carga (Inferido, brain) |
| Gatling | muita carga por máquina, DSL JVM | escolha `injectOpen`/`injectClosed` conscientemente |

Exemplo Locust (brain, Inferido): `locust -f locustfile.py --headless -u 500 -r 20 -t 30m --host https://staging.exemplo.com --csv resultado`; `wait_time = between(2, 5)` para think time. Os comandos são **texto de exemplo**: o plugin não os executa.

## Execução

- **Smoke primeiro** (1–2 VUs): muito "problema de performance" da primeira rodada é script errado. Smoke de 1–2 VUs é o máximo sem confirmação explícita.
- **Aquecimento** de 2–5 min (JIT, caches, pools, autoscaling) fora da conta; **rampa gradual** (abrupta só no teste de pico).
- **Duração:** patamar de 15–30 min para carga; horas para resistência. Vazamento, GC completo e job agendado não aparecem em 3 minutos.
- **O gerador não pode ser o gargalo.** Monitore CPU (abaixo de ~70–80%, regra de bolso), memória, rede e arquivos abertos; se saturar, distribua. Gerador e alvo na mesma máquina é erro.
- **Cache e CDN:** a mesma URL repetida dá 100% de acerto. Varie parâmetros e decida se o alvo é a borda ou a origem. Se o WAF bloquear o gerador, combine a liberação com quem opera; nunca contorne sozinho.
- **Comparabilidade:** mesma massa, base restaurada, mesma versão; anote o horário de cada patamar. Cabeçalho próprio (`X-Execucao-Carga: <id>`) isola o tráfego de teste nos logs.
- **Produção:** nunca sem pedido explícito, autorização, janela e critério de aborto. Em terceiro, nunca.

## Análise: onde está o gargalo

**Curva latência × vazão.** Subindo a taxa de chegada, a vazão acompanha e a latência fica quase plana; no **joelho** a vazão para de subir e a latência dispara (fila). A capacidade útil é a vazão no ponto em que o p95 cruza o SLO, antes do joelho; opere com margem abaixo dele.

| Padrão | Interpretação provável |
| --- | --- |
| p50 e p95 sobem juntos | todas as requisições mais lentas: recurso compartilhado saturado (CPU, banco) |
| p50 estável, p95/p99 sobem | parte espera: fila de pool, pausas de GC, lock, cache miss em parte das chaves, nó ruim, retries |
| erros antes de a latência subir | limite de conexões, rate limit, timeout curto, portas ou arquivos esgotados |
| latência cai enquanto o erro sobe | o sistema passou a falhar rápido (circuit breaker, 503): não é melhora |
| piora contínua com carga constante | vazamento de memória, crescimento de tabela ou fila (resistência) |

| Gargalo | Sinal | Confirmação |
| --- | --- | --- |
| Pool de conexões do banco | latência alta com CPU do banco baixa | conexões pendentes no pool; span "aguardando conexão" |
| Threads/workers | fila na entrada, CPU da aplicação baixa | threads ocupadas no máximo |
| GC | picos periódicos de p99 | logs de GC; heap após coleta subindo |
| Locks | lentidão em escrita, deadlocks | eventos de espera no banco (ex.: `pg_stat_activity` no PostgreSQL) |
| N+1 | latência cresce com o tamanho da lista | trace com dezenas de spans SQL iguais por requisição |
| Cache miss | piora quando a massa varia | taxa de acerto do cache caindo |
| Terceiro | spans externos lentos, 429 do provedor | latência do span de saída; limite contratado |

Correlacione: filtre no APM o endpoint e a janela do patamar, abra os traces mais lentos e compare com um rápido do mesmo endpoint; o span que cresce é o suspeito. Aumentar timeout ou escala para "resolver" lentidão é mascarar e pode amplificar carga e retries (SAP-10; ver [resiliencia-canario-capacidade.md](resiliencia-canario-capacidade.md)).

## Performance no CI e regressão

Fontes: brain (Inferido) + V-20 (gstack `benchmark`, MIT, Garry Tan, Classe B; destilado com atribuição; limiares do autor são Suposição).

- **No PR:** teste pequeno e estável (carga baixa e fixa por 1–3 min) com limiares folgados que pegam regressão grosseira. Carga completa à noite ou antes do release, no ambiente representativo.
- **Compare com baseline próprio, não com número mágico:** meça o `main` no mesmo ambiente; falhe quando a piora passar da tolerância combinada (ex.: p95 20% acima da mediana das últimas 5 execuções; exemplo).
- **Baseline imutável** durante a comparação; **ausência registrada como ausência** (métrica não coletada ≠ 0); baseline zero ⇒ variação N/A; **falha de carga é falha**, não lentidão.
- **Ruído:** runner compartilhado varia muito; repita 3–5 vezes e compare medianas (no gstack a mediana de 3 é opcional; K11). Não reprove por uma execução isolada.
- **Gates determinísticos primeiro:** número de consultas SQL por requisição (pega N+1 sem cronômetro), tamanho do bundle, número de requisições. Não oscilam e já apontam a causa.
- Limiares do gstack (tempo > 50% ou > 500 ms regressão, > 20% aviso; bundle > 25% regressão, > 10% aviso; requisições > 30% aviso) são **exemplo, Suposição**; relativize ao seu baseline.

## Frontend: Core Web Vitals

Fonte: V-19 (web.dev/articles/vitals, atualizado 2024-10-31, Classe A) + awesome-copilot `performance-optimization.instructions.md` (MIT, Classe B; 50+ regras, algumas contestáveis: não copiadas).

| Métrica | Bom (Verificado no web.dev) | Ruim (**Inferido**: não consta no web.dev; coincide com valores públicos e com o brain) |
| --- | --- | --- |
| LCP | ≤ 2,5 s | > 4 s |
| INP | ≤ 200 ms | > 500 ms |
| CLS | ≤ 0,1 | > 0,25 |

- Limiares valem para o **p75** das visitas reais, separando mobile e desktop.
- **Campo antes de laboratório** (K9): RUM e CrUX decidem; Lighthouse é diagnóstico/regressão. **Lighthouse em modo de navegação não mede INP** (usa TBT como proxy; o modo timespan mede só interações roteirizadas).
- LCP: imagem prioritária e pré-carregada, sem lazy-load acima da dobra, CSS crítico, scripts com `defer`/`async`. INP: divida tarefas longas, code splitting, trabalho pesado em worker. CLS: dimensões nas imagens, `font-display`, espaço reservado.
- Confira compatibilidade de navegador atual antes de recomendar APIs recentes. Pontos contestáveis do arquivo de terceiros, **não copiar**: cache de página inteira sem checar dados por usuário, suporte de navegador datado, barrel imports, `Intl.DateTimeFormat` como substituto universal de bibliotecas de data.
- Orçamentos (peso de JS, imagens, requisições) são o gate mais estável; parta do estado atual e aperte aos poucos. Lighthouse CI e emulação CDP no Playwright são tema do plugin `qa-testing`/`web-frontend` (ponteiro): `npx @lhci/cli` do brain é código de terceiro, apenas citado como texto.
- Implementação da otimização no código de UI: plugin `web-frontend`. Aqui: meta p75, interpretação de campo, regressão.

## Profiling e flame graphs

Fonte: V-25 (Brendan Gregg, Flame Graphs, Classe A, Verificado).

- O **eixo x não é tempo**: é a população de pilhas, ordenada alfabeticamente. A **largura** indica presença nas amostras (proporção do total).
- Procure **platôs largos perto do topo**: funções que gastam em si mesmas.
- Tipos: CPU, off-CPU (espera), memória, diferencial (antes × depois). Escolha o tipo pela pergunta: "lento com CPU baixa" pede off-CPU.
- **Flame chart** (eixo x em tempo, comum em DevTools) é outra coisa.
- A qualidade das pilhas depende do profiler (inlining e frames omitidos distorcem).

## Antipadrões

Média como critério de sucesso ou máximo como SLO; rodar sem SLO e decidir depois se "ficou bom"; relatório com números e sem interpretação; modelo fechado sem think time simulando site público; mesmo usuário e produto em todas as requisições; checar só status 200; gerador saturado ou na mesma máquina do alvo; capacidade de produção concluída de ambiente menor sem dizer; 3 minutos chamados de soak; carga em produção ou em terceiro sem autorização e janela. Ver SAP-11, SAP-12, SAP-13 em [padroes-e-antipadroes.md](padroes-e-antipadroes.md). Template de relatório: [relatorio-teste-de-carga.md](../assets/templates/relatorio-teste-de-carga.md).

## Lacunas

- **Profilers de backend por linguagem** (Go pprof, async-profiler, py-spy, Node) e Pyroscope: sem fonte A lida. Rotule Não verificável e peça a documentação da linguagem.
- **Consulta lenta de banco** (EXPLAIN, índices): sem fonte A; coordene com `database-data-modeling`.
- Locust em detalhe, dados de teste e carga em CI: parcial.
- Capacidade com modelos de fila/previsão: sem fonte.
