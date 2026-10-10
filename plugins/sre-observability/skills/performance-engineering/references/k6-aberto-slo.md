# Molde k6: modelo aberto com thresholds do SLO

Rascunho **não executado** (nesta sessão não havia k6 instalado). Os valores (`rate<0.005`, `p(95)<300`, `delayAbortEval: '30s'`) são ilustrativos: derive do SLO. Redução e adaptação do script do brain-of-agent (`brains/qa/references/performance.md`, MIT, conteúdo próprio do usuário) com o padrão de limiares de V-21 (documentação do k6, destilada). Confira a sintaxe na versão instalada (`k6 version`).

## Script (`carga-checkout.js`)

```javascript
// Uso previsto, SÓ após autorização do alvo e da janela:
//   smoke:  k6 run -e BASE_URL=https://staging.exemplo.test -e CARGA_AUTORIZADA=sim -e MODO=smoke carga-checkout.js
//   carga:  k6 run -e BASE_URL=https://staging.exemplo.test -e CARGA_AUTORIZADA=sim -e PICO=60 carga-checkout.js
//   gate estrito (deve FALHAR): acrescente -e P95_MS=1
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const BASE_URL = __ENV.BASE_URL;
if (!BASE_URL) throw new Error('Defina BASE_URL com -e BASE_URL=...');
if (__ENV.CARGA_AUTORIZADA !== 'sim') {
  throw new Error('Defina CARGA_AUTORIZADA=sim somente depois de confirmar alvo, janela e autorização');
}
const SMOKE = __ENV.MODO === 'smoke';
const PICO = Number(__ENV.PICO || 5);          // iterações por segundo no patamar
const P95_MS = Number(__ENV.P95_MS || 300);    // vem do SLO

const produtos = new SharedArray('produtos', () => JSON.parse(open('./dados/produtos.json')));

export const options = {
  scenarios: {
    navegacao: {
      executor: 'ramping-arrival-rate',
      startRate: 1, timeUnit: '1s',
      preAllocatedVUs: SMOKE ? 2 : 20,
      maxVUs: SMOKE ? 2 : 200,
      stages: SMOKE
        ? [{ target: 1, duration: '1m' }]
        : [
            { target: PICO, duration: '2m' },    // rampa
            { target: PICO, duration: '15m' },   // patamar: é aqui que se mede
            { target: 0, duration: '1m' },
          ],
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.005'],
    checks: ['rate>0.99'],
    'http_req_duration{name:produto_detalhe}': [
      { threshold: `p(95)<${P95_MS}`, abortOnFail: true, delayAbortEval: '30s' },
      'p(99)<1000',
    ],
    dropped_iterations: ['count<10'],          // o gerador entregou a taxa pedida?
  },
  summaryTrendStats: ['avg', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

function campo(res, caminho) {
  try { return res.json(caminho); } catch (e) { return undefined; } // corpo não-JSON, ex.: 502 HTML
}

export default function () {
  const p = produtos[Math.floor(Math.random() * produtos.length)];
  const res = http.get(`${BASE_URL}/api/produtos/${p.id}`, { tags: { name: 'produto_detalhe' } });
  check(res, {
    'status 200': (r) => r.status === 200,
    'é o produto pedido': (r) => campo(r, 'id') === p.id,   // checa conteúdo, não só status
  });
  sleep(2 + Math.random() * 3);                              // think time sorteado
}
```

## Por que cada parte existe

| Parte | Motivo |
| --- | --- |
| `CARGA_AUTORIZADA` | Poka-yoke: o script não roda sem confirmação humana do alvo; não substitui a autorização real |
| `ramping-arrival-rate` | Modelo aberto: a chegada continua mesmo quando o sistema fica lento, como na vida real |
| `preAllocatedVUs` / `maxVUs` | Dimensione por Little (it/s x duração); `vus_max` igual a `maxVUs` na saída indica falta de VU |
| `tags: { name }` | Agrupa URLs com ID; sem a tag, cada ID vira uma série |
| `check` com conteúdo | Evita "erro verde" (200 com corpo de erro); `checks: ['rate>0.99']` o torna reprovador |
| `abortOnFail` + `delayAbortEval` | Interrompe quando o SLO já foi violado sem abortar no ruído do aquecimento |
| `dropped_iterations` | Se > 0, a taxa pedida não foi entregue: não se mediu a carga que se acha |
| `P95_MS` por variável | Permite a execução estrita que **deve falhar** e prova que o gate está ligado |

## Como validar o gate (Inferido até executar)

1. Smoke com limiar normal: deve terminar com thresholds aprovados e código de saída 0.
2. Mesmo smoke com `-e P95_MS=1`: deve reprovar e sair com código não-zero (o brain registra 99; Inferido). Se passar, o limiar não está ligado à métrica certa.
3. Cole as duas saídas reais no relatório; sem execução, escreva "não executado".

## Locust (equivalente mínimo, modelo fechado por padrão)

```python
# locustfile.py
from locust import HttpUser, task, between

class Visitante(HttpUser):
    wait_time = between(2, 5)            # think time

    @task(6)
    def produto(self):
        self.client.get("/api/produtos/1", name="produto_detalhe")
```

Execução prevista (somente após autorização): `locust -f locustfile.py --headless -u 500 -r 20 -t 30m --host https://staging.exemplo.test --csv resultado`. Um processo usa um núcleo; para mais carga distribua com `--master` e `--worker`. Como o padrão é fechado, a latência de cauda sob lentidão sai otimista (coordinated omission); para site público prefira modelo aberto.

## Smoke versus carga: o que pedir ao usuário antes

- Alvo e ambiente exatos (URL, região) e confirmação de que não é produção nem terceiro.
- Autorização e janela com os donos de aplicação, banco, rede, CDN/WAF e nuvem; contato; como interromper (Ctrl+C no gerador e quem desliga o tráfego).
- Volume máximo (it/s e duração) e dados sintéticos prontos (`dados/produtos.json`).
