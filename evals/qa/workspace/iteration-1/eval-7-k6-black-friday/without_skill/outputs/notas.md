# Notas e incertezas

## Verificação
- k6 não está instalado nesta máquina e eu não podia instalar pacotes nem fazer requisições de rede. O script NÃO foi executado com k6 real.
- Validei a lógica (funil, contas de taxa/VUs, guarda de host, caminhos de erro 409 e JSON inválido, entrada por campanha) com um harness em Node com stubs de `k6`, `k6/http`, `k6/metrics` e `k6/data`. O harness ficou no scratchpad e não faz parte da entrega. Ele não valida a semântica real do k6.
- Resultado do harness: 20.000 sessões com o funil padrão geraram cerca de 7,2% de pedidos; o patamar de 3x dá 875 sessões/min, preAllocatedVUs 438 e maxVUs 876.

## Comportamentos do k6 que assumi sem poder testar
- `dropped_iterations: ['count<1']` passa quando a métrica não tem amostras.
- `responseCallback: http.expectedStatuses(...)` por requisição para aceitar 409 sem contar como falha HTTP.
- `open()` relativo ao arquivo do script (por isso a instrução de rodar da pasta do script).
- k6 lê variáveis de ambiente do sistema em `k6 run` (usei isso para `PAYMENT_TOKEN`).
- `--summary-export`, `--out` e `--tag` existem como descritos. Não afirmei nomes de outputs específicos de propósito.
- Alvo `0` em `ramping-arrival-rate` e `rate` inteiro com `timeUnit: '1m'`.

## Suposições de domínio (principal fonte de erro)
- Endpoints, payloads e formato das respostas são fictícios (`/api/search` retornando `items[].id`, `POST /api/carts` retornando `id`, `shipping-quote` retornando `options[].id`, `POST /api/checkout` retornando 201 + `orderId`, header `Idempotency-Key`). Marquei com `ADAPTAR`.
- O funil padrão (70% / 20% / 50%) e a distribuição de visualizações de produto (1 a 3) são chutes. Com conversão real diferente, a carga de busca e produto muda muito (ex.: 2% de conversão no lugar de 7% gera cerca de 3,5x mais sessões). Deixei `SESSIONS_PER_HOUR_1X` para sobrescrever.
- SLOs (p95/p99 por etapa, erro < 1%, sucesso de pedido > 98%) são placeholders.
- `AVG_SESSION_SEC=20` e o dimensionamento de VUs (1,5x de folga para pré-alocar, 2x para o máximo) são estimativas. Sob degradação forte (sobretudo no stress) as sessões ficam mais longas e podem faltar VUs, o que gera `dropped_iterations`. Nesse caso é preciso aumentar `AVG_SESSION_SEC`.
- Interpretei "3x" como 3x os pedidos/h do pico (3.600/h). Não sei se 1.200/h é média da hora mais cheia ou pico por minuto, nem se o comercial fala de pedidos, de receita ou de tráfego. Tratei isso como pergunta aberta na resposta.
- Multiplicadores de spike (1,5x o GROWTH = 4,5x) e dos degraus do stress (+1x por degrau até 6x) são escolhas minhas.
- O `abortOnFail` em `http_req_failed` também vale no stress: ele para no primeiro degrau em que o erro passa de 1%. Isso encontra o ponto de quebra, mas impede observar o que acontece depois. Se quiser ver o colapso inteiro, tire o `abortOnFail` no perfil stress.
- CEPs em `data/zipcodes.json` e termos em `data/search-terms.json` são exemplos não verificados. `TEST_DOCUMENT` padrão `00000000000` provavelmente é rejeitado pelo staging.
- Data da Black Friday (27/11/2026) deduzida do calendário (4ª sexta de novembro) e da data do sistema (05/10/2026). O cronograma sugerido é só uma sugestão.
- A guarda de host usa uma heurística de nome (staging, stg, hml, homolog, qa, test). Um staging com outro nome exige `CONFIRM_NOT_PRODUCTION=yes`, e isso é uma proteção fraca, não garantia.

## Decisões de escopo
- Entreguei de uma vez, com suposições explícitas, em vez de pedir esclarecimentos antes. As perguntas mais importantes estão na seção final da resposta.
- Fora do escopo: login, autocomplete, filtros e paginação, PIX e boleto assíncronos, páginas de campanha, front/CDN, injeção de falhas.
- Não incluí `handleSummary` (evita import remoto de jslib, que quebraria em runner sem internet). A conferência de pedidos/h atingidos é manual (`orders_created`).
- Não criei README separado. O cabeçalho do script e a resposta documentam o uso.
