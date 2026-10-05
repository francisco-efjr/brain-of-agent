# Performance

Como planejar, modelar, executar e interpretar testes de performance de
backend (carga, estresse, pico, resistência) e de frontend (Core Web Vitals).
Leia quando a pergunta for "aguenta?", "quantos usuários suporta?", "por que
ficou lento?" ou quando precisar de um script em k6, JMeter, Gatling ou Locust.

## Sumário

- [Tipos de teste e a pergunta de cada um](#tipos-de-teste-e-a-pergunta-de-cada-um)
- [Antes de começar](#antes-de-começar)
- [Modelagem de carga a partir de dados reais](#modelagem-de-carga-a-partir-de-dados-reais)
- [Métricas que importam](#métricas-que-importam)
- [k6: script completo](#k6-script-completo)
- [JMeter, Gatling e Locust](#jmeter-gatling-e-locust)
- [Execução](#execução)
- [Análise: onde está o gargalo](#análise-onde-está-o-gargalo)
- [Performance no CI](#performance-no-ci)
- [Frontend: Core Web Vitals e Lighthouse CI](#frontend-core-web-vitals-e-lighthouse-ci)
- [Anti-padrões](#anti-padrões)
- [Template de relatório](#template-de-relatório)

## Tipos de teste e a pergunta de cada um

Escolha pela pergunta de negócio; o mesmo script serve a vários tipos.

| Tipo | Pergunta que responde | Perfil típico |
| --- | --- | --- |
| Smoke de performance | O script funciona e o sistema responde sem erro? | 1–2 usuários, 1–2 min — sempre antes dos outros |
| Carga | No pico normal esperado, cumprimos o SLO? | rampa até o pico previsto, patamar de 15–30 min |
| Estresse | Acima do esperado, como degrada? Volta ao normal depois? | degraus acima do pico até violar o SLO; observar a recuperação |
| Pico (spike) | Uma subida abrupta (push, abertura de vendas, TV) derruba? O autoscaling chega a tempo? | de normal a 5–10× em segundos, depois volta |
| Resistência (soak) | Rodando horas, algo vaza (memória, conexões, disco, fila)? | carga normal por 4–12 h ou mais, cobrindo jobs noturnos e rotação de log |
| Capacidade (breakpoint) | Qual a vazão máxima **dentro do SLO**? | taxa crescente até o p95 cruzar o SLO — o limite é o SLO, não a queda do servidor |
| Escalabilidade | Dobrar instâncias dobra a vazão? Onde para de escalar? | mesma rampa com 1, 2 e 4 instâncias |
| Volume | Com base 10× maior, as consultas continuam no SLO? | carga moderada sobre massa grande |

## Antes de começar

1. **Pergunta de negócio por escrito.** "O checkout aguenta 4× o pico de 2025
   com p95 abaixo de 800 ms?" é testável; "ver se está rápido" não tem
   critério de sucesso nem de parada.
2. **SLI e SLO.** SLI é a medida (p95 do `POST /pedidos`, taxa de erro,
   vazão); SLO é o alvo ("p95 < 800 ms, p99 < 2 s, erro < 0,5%, a 120 req/s
   por 30 min"). Sem SLO o relatório vira opinião. Se o time não tem, proponha
   um a partir da latência atual de produção (APM) e registre como suposição.
3. **Ambiente representativo:** mesma topologia, instâncias iguais ou
   proporcionais, base com volume parecido (com 1.000 linhas, consulta sem
   índice é rápida). Extrapolar de ambiente menor é palpite — diga isso.
4. **Autorização e janela combinadas** com quem opera aplicação, banco, rede,
   CDN/WAF e nuvem (cada provedor tem política própria): carga sem aviso parece
   ataque. Registre volume máximo, horário, contato e como interromper.
5. **Terceiros** (pagamento, antifraude, SMS): stub ou virtualização com
   latência realista. Carregar sandbox de terceiro mede o terceiro, esbarra
   em limite de taxa e pode violar os termos de uso.
6. **Dados** sintéticos e variados (repetir usuário e produto mede cache e
   contenção de linha) e plano de limpeza.
7. **Monitoramento ligado antes do primeiro request:** APM e traces, CPU e
   memória por camada, pool de conexões, banco (consultas lentas, locks),
   filas **e o próprio gerador**. Sem isso você vê que ficou lento, não por quê.

## Modelagem de carga a partir de dados reais

**Fontes:** analytics (sessões/hora, páginas por sessão, duração), logs de
acesso ou do gateway (requisições por endpoint por minuto) e APM. Use a **hora
de pico**, não a média do dia — e dentro dela o minuto de pico.

**Mix de transações.** Reproduza a proporção real; ela muda o gargalo (busca
pesa no índice; checkout, em escrita e em terceiros).

| Fluxo | % das sessões | Requisições por sessão |
| --- | --- | --- |
| Navegar catálogo | 60% | 8 |
| Buscar | 25% | 6 |
| Adicionar ao carrinho e sair | 10% | 10 |
| Finalizar compra | 5% | 18 |

**Think time e pacing.** Think time é a pausa entre ações da sessão (a pessoa
lendo); pacing, o intervalo entre inícios de iterações. Sem think time, 100
VUs disparam como milhares de pessoas. Sorteie a pausa numa faixa (2–5 s)
para os usuários não sincronizarem em ondas.

**Modelo aberto × fechado** — a decisão mais subestimada do teste:

| | Aberto (taxa de chegada) | Fechado (usuários virtuais) |
| --- | --- | --- |
| Quem dita a carga | chegadas por segundo, independentes da resposta | N usuários; cada um só envia o próximo após a resposta |
| Quando o sistema fica lento | as chegadas continuam e a fila cresce, como na vida real | a carga cai sozinha: o teste alivia o sistema quando ele sofre |
| Representa | site público, API, app | população fixa: 200 atendentes de call center, pool de workers |
| Ferramenta | k6 `*-arrival-rate`; Gatling `injectOpen`; JMeter Open Model Thread Group ou Precise Throughput Timer | k6 `ramping-vus`; Gatling `injectClosed`; Locust; Thread Group do JMeter |

Para web e API públicas, use modelo aberto: o fechado subestima a latência
exatamente no ponto que interessa (ver coordinated omission).

**Lei de Little: L = λ × W** (concorrência = taxa de chegada × tempo de
permanência). Analytics: 50.000 sessões na hora de pico, 5 min cada.

- λ = 50.000 / 3.600 ≈ 13,9 sessões/s; W = 300 s → L ≈ **4.167 sessões
  simultâneas**. Com 12 requisições por sessão: ≈ **167 req/s**.
- Black Friday com fator 4× (pico do evento anterior ÷ pico de dia comum):
  ≈ 16.700 sessões simultâneas e ≈ 667 req/s. Some a margem que o negócio
  pedir (ex.: +30%) e diga no relatório de onde veio o fator.

A mesma lei dimensiona o gerador: VUs necessários ≈ iterações/s × duração da
iteração (com think time). 10 iterações/s de 8 s pedem ~80 VUs — reserve
folga para quando a latência subir.

## Métricas que importam

**A média engana.** 99 requisições de 100 ms e uma de 10 s dão média de
199 ms, mas uma em cada 100 esperou 10 s. Numa sessão de 20 requisições, a
chance de a pessoa pegar ao menos uma acima do p99 é 1 − 0,99²⁰ ≈ 18%.

- **Percentis:** p50 (típico), p95 e p99 (cauda), máximo (investigar, não
  usar como SLO). p99 estável exige milhares de amostras por endpoint; 2 min
  a 5 req/s não sustentam conclusão sobre p99.
- **Nunca tire média de percentis** (de instâncias ou de minutos): agregue
  histogramas ou amostras brutas.
- **Vazão** (req/s ou transações/s): se a carga sobe e a vazão não, saturou.
- **Taxa de erro**, com timeouts do cliente e "erros verdes" (200 com corpo de
  erro ou página de manutenção) — por isso o script checa conteúdo.
- **Saturação**, que explica a latência. **USE** por recurso (CPU, memória,
  disco, rede, pool, threads): Utilização, Saturação (fila), Erros. **RED**
  por serviço: Rate, Errors, Duration. RED mostra *onde* dói; USE, *por quê*.

**Coordinated omission.** No modelo fechado, quando o servidor trava 2 s,
cada VU fica esperando e deixa de enviar as requisições desse intervalo. As
amostras ruins nunca são medidas e o p99 sai otimista, às vezes por ordens
de grandeza. Mitigação: modelo aberto, ferramentas que corrigem pela taxa
pretendida e, no k6, vigiar `dropped_iterations` (iterações que não
começaram no horário por falta de VU).

## k6: script completo

Dois fluxos em modelo aberto, login com token reaproveitado por VU,
correlação de ID entre requisições, massa parametrizada e critérios de
aprovação. `usuarios.json` e `produtos.json` são gerados para o teste, com
contas sintéticas. Funciona no k6 1.x e 2.x.

```javascript
// checkout.js — k6 run -e BASE_URL=https://homolog.exemplo.com checkout.js
import http from 'k6/http';
import { check, sleep, fail } from 'k6';
import { SharedArray } from 'k6/data';
import exec from 'k6/execution';

const BASE_URL = __ENV.BASE_URL;
if (!BASE_URL) throw new Error('Defina BASE_URL com -e BASE_URL=...');

// Lidos uma vez e compartilhados entre VUs (somente leitura, sem cópia por VU).
const usuarios = new SharedArray('usuarios', () => JSON.parse(open('./dados/usuarios.json')));
const produtos = new SharedArray('produtos', () => JSON.parse(open('./dados/produtos.json')));

const estagios = (pico) => [
  { target: Math.ceil(pico / 6), duration: '2m' }, // aquecimento
  { target: pico, duration: '5m' },                // rampa
  { target: pico, duration: '20m' },               // patamar: é aqui que se mede
  { target: 0, duration: '2m' },
];

export const options = {
  scenarios: {
    navegacao: {
      executor: 'ramping-arrival-rate', exec: 'navegar', startRate: 5, timeUnit: '1s',
      preAllocatedVUs: 100, maxVUs: 400, stages: estagios(60), tags: { fluxo: 'navegacao' },
    },
    compra: {
      executor: 'ramping-arrival-rate', exec: 'comprar', startRate: 1, timeUnit: '1s',
      preAllocatedVUs: 30, maxVUs: 150, stages: estagios(6), tags: { fluxo: 'compra' },
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
    'http_req_duration{name:produto_detalhe}': ['p(95)<400', 'p(99)<1000'],
    'http_req_duration{name:pedido_criar}': [
      { threshold: 'p(95)<800', abortOnFail: true, delayAbortEval: '2m' },
      'p(99)<2000',
    ],
    dropped_iterations: ['count<10'], // o gerador entregou a taxa pedida?
  },
  summaryTrendStats: ['avg', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

function campo(res, caminho) {
  try { return res.json(caminho); } catch (e) { return undefined; } // corpo não-JSON (ex.: 502 HTML)
}
const pausa = (min, max) => sleep(min + Math.random() * (max - min)); // think time sorteado
const produtoAleatorio = () => produtos[Math.floor(Math.random() * produtos.length)];

let token = null, expiraEm = 0; // variáveis de módulo são por VU: um login por VU

function autenticar() {
  if (token && Date.now() < expiraEm - 30000) return token;
  const u = usuarios[(exec.vu.idInTest - 1) % usuarios.length]; // um usuário por VU
  const res = http.post(`${BASE_URL}/api/login`, JSON.stringify({ email: u.email, senha: u.senha }), {
    headers: { 'Content-Type': 'application/json' }, tags: { name: 'login' },
  });
  const ok = check(res, {
    'login: status 200': (r) => r.status === 200,
    'login: devolveu token': (r) => typeof campo(r, 'access_token') === 'string',
  });
  if (!ok) fail(`login falhou (VU ${exec.vu.idInTest}): status ${res.status}`);
  token = campo(res, 'access_token');
  expiraEm = Date.now() + (campo(res, 'expires_in') || 300) * 1000;
  return token;
}

export function navegar() {
  const p = produtoAleatorio();
  // a tag "name" agrupa URLs com ID; sem ela, cada ID vira uma série separada
  const res = http.get(`${BASE_URL}/api/produtos/${p.id}`, { tags: { name: 'produto_detalhe' } });
  check(res, {
    'produto: status 200': (r) => r.status === 200,
    'produto: é o produto pedido': (r) => campo(r, 'id') === p.id,
  });
  pausa(2, 5);
}

export function comprar() {
  const headers = { 'Content-Type': 'application/json', Authorization: `Bearer ${autenticar()}` };
  const item = http.post(`${BASE_URL}/api/carrinho/itens`,
    JSON.stringify({ produtoId: produtoAleatorio().id, quantidade: 1 }),
    { headers, tags: { name: 'carrinho_adicionar' } });
  const carrinhoId = campo(item, 'carrinhoId'); // correlação: o ID gerado alimenta o próximo passo
  if (!check(item, { 'carrinho: 201 com id': (r) => r.status === 201 && !!carrinhoId })) return;
  pausa(3, 7);
  const pedido = http.post(`${BASE_URL}/api/pedidos`,
    JSON.stringify({ carrinhoId, formaPagamento: 'cartao_teste' }),
    { headers, tags: { name: 'pedido_criar' } });
  check(pedido, {
    'pedido: status 201': (r) => r.status === 201,
    'pedido: tem número': (r) => !!campo(r, 'numero'),
  });
}
```

- **Checks validam conteúdo**; `checks: ['rate>0.99']` os torna reprovadores
  (check sem threshold é só estatística).
- **`http_req_failed`** conta todo status ≥ 400. Se um passo espera 409,
  declare: `http.setResponseCallback(http.expectedStatuses({ min: 200, max:
  399 }, 409))`.
- **`abortOnFail` + `delayAbortEval`** para quando o SLO já foi violado, sem
  abortar no ruído do aquecimento. Dimensionamento pela Lei de Little:
  navegação ≈ 60 it/s × ~4 s ≈ 240 VUs; `maxVUs: 400` dá folga.

**Como ler a saída.** O k6 sai com código 99 quando algum threshold falha — é
isso que quebra o pipeline. O resumo é compacto por padrão desde o k6 1.0
(`--summary-mode=full` detalha por cenário).

| Métrica | Leitura |
| --- | --- |
| thresholds ✓/✗ | veredito; leia primeiro |
| `http_req_duration` por `name` | latência por endpoint contra o SLO |
| `http_req_waiting` | tempo até o primeiro byte: é o servidor |
| `http_req_blocked`, `http_req_connecting`, `http_req_tls_handshaking` | altos indicam conexões esgotadas ou gerador sobrecarregado |
| `dropped_iterations` > 0 | a taxa pedida não foi entregue: você não mediu a carga que acha que mediu |
| `vus_max` igual a `maxVUs` | faltou VU; aumente ou investigue a latência |

O resumo mistura aquecimento, rampa e patamar; conclusões sobre o patamar
vêm da série temporal. As variáveis `K6_WEB_DASHBOARD=true` e
`K6_WEB_DASHBOARD_EXPORT=relatorio.html` geram painel ao vivo e HTML; `--out`
envia a Prometheus, InfluxDB ou JSON para cruzar com o APM.

**k6 browser.** O módulo `k6/browser` (API assíncrona parecida com a do
Playwright) roda Chromium real e mede Web Vitals (`browser_web_vital_lcp`,
`browser_web_vital_inp`, `browser_web_vital_cls`). Cada VU de navegador é um
Chromium inteiro: use o padrão híbrido — carga por HTTP e um cenário com 1–5
VUs de navegador (`options: { browser: { type: 'chromium' } }`) medindo a
experiência sob essa carga.

## JMeter, Gatling e Locust

| Ferramenta | Escolha quando | Cuidado |
| --- | --- | --- |
| k6 | time confortável com JS/TS, teste como código no repositório, CI | protocolos além de HTTP/gRPC/WebSocket dependem de extensões |
| JMeter | protocolos variados (JDBC, JMS, LDAP, FTP, SOAP), time já usa, montagem visual | `.jmx` é XML difícil de revisar em PR; gerador consome muita memória |
| Gatling | muita carga por máquina, DSL em Java/Kotlin/Scala, bom relatório HTML | `injectOpen` e `injectClosed` são explícitos — escolha conscientemente |
| Locust | time Python, lógica de usuário complexa | modelo fechado por padrão; um processo usa um núcleo — distribua com `--master`/`--worker` |

**JMeter:** GUI só para montar e depurar; execute em modo não-GUI —
`jmeter -n -t plano.jmx -l resultado.jtl -e -o relatorio/ -Jusuarios=200`,
lendo no plano `${__P(usuarios,10)}`. Desligue listeners (View Results Tree,
gráficos) durante a carga: consomem CPU e memória do gerador; o relatório
HTML sai do `.jtl` (`-e -o`). Massa via **CSV Data Set Config**, com
`Recycle on EOF = False` e `Stop thread on EOF = True` quando cada linha só
pode ser usada uma vez (cupom, conta). Correlação com JSON Extractor; ajuste
a heap do gerador pela variável `HEAP` (ex.: `-Xms1g -Xmx4g`).

**Locust:** `locust -f locustfile.py --headless -u 500 -r 20 -t 30m --host
https://homolog.exemplo.com --csv resultado`; `wait_time = between(2, 5)`
para think time e `@task(peso)` para o mix.

## Execução

- **Smoke primeiro** (1–2 VUs): muito "problema de performance" da primeira
  rodada é script errado. **Aquecimento** de 2–5 min (JIT, caches, pools,
  autoscaling) fora da conta; **rampa gradual** (abrupta só no teste de pico).
- **Duração:** patamar de 15–30 min para carga; horas para resistência.
  Vazamento, GC completo e job agendado não aparecem em 3 minutos.
- **O gerador não pode ser o gargalo.** Monitore CPU (abaixo de ~70–80%),
  memória, rede e arquivos abertos (`ulimit -n`); se satura, distribua.
  Gerador e alvo na mesma região medem o servidor; gerador distante mede
  servidor + rede — decida qual pergunta responde.
- **Cache e CDN:** a mesma URL repetida dá 100% de acerto de cache. Varie
  parâmetros e decida se o alvo é a borda ou a origem. Se o WAF bloquear o
  gerador, combine a liberação com quem opera; nunca contorne sozinho.
- **Comparabilidade:** mesma massa, base restaurada, mesma versão; anote o
  horário de cada patamar.

## Análise: onde está o gargalo

**Curva latência × vazão.** Subindo a taxa de chegada, a vazão acompanha e a
latência fica quase plana; no **joelho**, a vazão para de subir e a latência
dispara porque as requisições passam a esperar em fila. A capacidade útil é
a vazão no ponto em que o p95 cruza o SLO — antes do joelho —, não o ponto em
que o sistema cai. Opere com margem abaixo dele.

| Padrão | Interpretação provável |
| --- | --- |
| p50 e p95 sobem juntos | todas as requisições mais lentas: recurso compartilhado saturado (CPU, banco) |
| p50 estável, p95/p99 sobem | parte das requisições espera: fila de pool, pausas de GC, lock, cache miss em parte das chaves, um nó ruim, retries |
| erros antes de a latência subir | limite de conexões, rate limit, timeout curto, portas ou arquivos esgotados |
| latência cai enquanto o erro sobe | o sistema passou a falhar rápido (circuit breaker, 503) — não é melhora |
| piora contínua com carga constante | vazamento de memória, crescimento de tabela ou fila (resistência) |

| Gargalo | Sinal | Confirmação |
| --- | --- | --- |
| Pool de conexões do banco | latência alta com CPU do banco baixa | conexões pendentes no pool; span "aguardando conexão" |
| Threads/workers do servidor | fila na entrada, CPU da aplicação baixa | threads ocupadas no máximo |
| GC | picos periódicos de p99 | logs de GC; heap após coleta subindo |
| Locks | lentidão em escrita, deadlocks | eventos de espera no banco (ex.: `pg_stat_activity` no PostgreSQL) |
| N+1 | latência cresce com o tamanho da lista | trace com dezenas de spans SQL iguais por requisição |
| Cache miss | piora quando a massa varia | taxa de acerto do cache caindo |
| Terceiro | spans externos lentos, 429 do provedor | latência do span de saída; limite contratado |

Correlacione: filtre no APM o endpoint e a janela do patamar, abra os traces
mais lentos e compare com um rápido do mesmo endpoint — o span que cresce é o
suspeito. Um cabeçalho próprio (`X-Execucao-Carga: <id>`) isola o tráfego.

## Performance no CI

- **No PR, teste pequeno e estável:** carga baixa e fixa por 1–3 min,
  thresholds folgados que pegam regressão grosseira (p95 dobrou, erro > 0).
  A carga completa roda à noite ou antes do release, no ambiente representativo.
- **Compare com a baseline, não com número mágico:** meça o `main` no mesmo
  ambiente e falhe quando a piora passar da tolerância combinada (ex.: p95
  20% acima da mediana das últimas 5 execuções).
- **Ruído:** runner compartilhado varia muito. Repita 3–5 vezes, compare
  medianas e não reprove por uma execução isolada.
- **Prefira gates determinísticos:** número de consultas SQL por requisição
  (pega N+1 sem cronômetro), tamanho do bundle, número de requisições da
  página. Não oscilam e já apontam a causa.

## Frontend: Core Web Vitals e Lighthouse CI

| Métrica | Mede | Bom | Ruim |
| --- | --- | --- | --- |
| LCP (Largest Contentful Paint) | carregamento do maior elemento visível | ≤ 2,5 s | > 4 s |
| INP (Interaction to Next Paint) | resposta a interações (substituiu o FID em março de 2024) | ≤ 200 ms | > 500 ms |
| CLS (Cumulative Layout Shift) | estabilidade visual | ≤ 0,1 | > 0,25 |

Os limiares valem para o **p75** das visitas reais, separando celular e
desktop. Dado de campo (RUM com a biblioteca `web-vitals`, CrUX) é a verdade;
laboratório (Lighthouse) é diagnóstico reprodutível. Lighthouse não interage
com a página, logo não mede INP: use TBT (Total Blocking Time) como indicador.

**Lighthouse CI** (`npx @lhci/cli autorun` com `lighthouserc.json` na raiz):

```json
{
  "ci": {
    "collect": {
      "url": ["https://homolog.exemplo.com/", "https://homolog.exemplo.com/produto/42"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["warn", { "maxNumericValue": 200 }],
        "resource-summary:script:size": ["error", { "maxNumericValue": 300000 }],
        "categories:performance": ["warn", { "minScore": 0.9 }]
      }
    },
    "upload": { "target": "filesystem", "outputDir": "./lhci-relatorios" }
  }
}
```

- Três execuções porque uma isolada varia (o LHCI usa a mediana). Não use
  `temporary-public-storage` em sistema interno: publica o relatório.
- **Orçamentos** (peso de JS, imagens, requisições) são o gate mais estável;
  os 300 KB acima são exemplo — parta do estado atual e aperte aos poucos.
- O Lighthouse emula por padrão celular com rede lenta e CPU 4× mais lenta —
  cenário certo para o Brasil (muito Android intermediário em 4G instável).

**Throttling em teste E2E** (Playwright, só Chromium, via CDP):

```typescript
import { test, expect } from '@playwright/test';

test('busca responde em rede lenta e CPU limitada', async ({ page }) => {
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('Network.emulateNetworkConditions', {
    offline: false, latency: 150, // ms; vazões em bytes/s (~1,6 Mbps / 750 kbps)
    downloadThroughput: (1.6 * 1024 * 1024) / 8, uploadThroughput: (750 * 1024) / 8,
  });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  await page.goto(`${process.env.BASE_URL}/busca`);
  await page.getByRole('searchbox', { name: 'Buscar' }).fill('notebook');
  await expect(page.getByRole('list', { name: 'Resultados' })).toBeVisible({ timeout: 10_000 });
});
```

## Anti-padrões

- Média como critério de sucesso ou máximo como SLO; rodar sem SLO e decidir
  depois se "ficou bom"; relatório com números e sem interpretação.
- Modelo fechado sem think time simulando site público; mesmo usuário e
  produto em todas as requisições; checar só status 200.
- Gerador saturado ou na mesma máquina do sistema testado; capacidade de
  produção concluída de ambiente menor sem dizer; 3 minutos chamados de soak.
- Carga em produção ou em terceiro sem autorização e janela combinadas.

## Template de relatório

```markdown
# Teste de performance — <sistema> — <data>

**Pergunta:** <ex.: o checkout aguenta 4× o pico de 2025 dentro do SLO?>
**Veredito:** <atende | não atende | atende com ressalvas> — <uma frase>

## Condições
- Tipo, modelo e perfil: <carga…>, <aberto/fechado>, <rampa, patamar, taxa, mix>
- Origem dos números: <analytics/APM/logs, fator de pico>
- Ambiente: <topologia, tamanho vs produção, volume da base, versão>
- Stubs e fora do escopo: <terceiros simulados, fluxos não exercitados>

## Resultados no patamar
| Endpoint | Vazão | p50 | p95 | p99 | Erro | SLO | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Gargalos e evidências
- <sintoma> → <causa provável> → <evidência: trace, métrica, horário>

## Recomendações e risco residual
- <ação, dono, impacto esperado>; <o que não foi verificado e o risco que sobra>
- Medido: <...> | Extrapolado: <...> | Suposições: <...>
```
