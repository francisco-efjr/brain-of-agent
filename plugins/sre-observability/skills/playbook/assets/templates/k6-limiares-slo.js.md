# k6: limiares derivados do SLO e script aberto reduzido

Template T-10. **Valores ilustrativos: derive os seus do SLO.** Parte 1: snippet de limiares (V-21, docs do k6, redação própria). Parte 2: versão reduzida do script do brain-of-agent (`brains/qa/references/performance.md`, conteúdo próprio do autor do plugin, MIT; adaptado; **não reverificado** contra a versão atual do k6, rótulo Inferido). Rascunho **não executado**. O plugin não roda carga: execute só com alvo confirmado, autorização e janela (smoke de 1–2 VUs primeiro). Confira a sintaxe na versão instalada (`k6 version`); a documentação foi conferida em `next`, não em `latest`.

## Parte 1: limiares como SLO

```js
// Falha de limiar => k6 encerra com código de saída não-zero => o CI reprova.
// Checks sozinhos não afetam o código de saída: use também checks: ['rate>0.99'].
export const options = {
  thresholds: {
    http_req_failed: ['rate<0.005'],                        // erro < 0,5%
    http_req_duration: [
      { threshold: 'p(95)<300', abortOnFail: true, delayAbortEval: '30s' }, // p95 < 300 ms; aborta se violar, após 30 s de amostras
    ],
  },
};
```

Valide o limiar: uma execução que **deve passar** e outra com valor estrito (por exemplo `p(95)<1`) que **deve falhar**. Limiar que nunca falha não protege nada.

## Parte 2: script em modelo aberto (reduzido)

Dois fluxos com `ramping-arrival-rate`, massa compartilhada, `check` de conteúdo, limiar por endpoint e `dropped_iterations`. Aquecimento fora da conta: o patamar é o que se mede.

```js
// carga.js — k6 run -e BASE_URL=https://staging.exemplo.com carga.js   (ambiente NÃO produtivo, com autorização)
import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

const BASE_URL = __ENV.BASE_URL;
if (!BASE_URL) throw new Error('Defina BASE_URL com -e BASE_URL=...');

const produtos = new SharedArray('produtos', () => JSON.parse(open('./dados/produtos.json'))); // massa sintética

const estagios = (pico) => [
  { target: Math.ceil(pico / 6), duration: '2m' }, // aquecimento
  { target: pico, duration: '5m' },                // rampa
  { target: pico, duration: '20m' },               // patamar: é aqui que se mede
  { target: 0, duration: '2m' },
];

export const options = {
  scenarios: {
    navegacao: { executor: 'ramping-arrival-rate', exec: 'navegar', startRate: 5, timeUnit: '1s',
                 preAllocatedVUs: 100, maxVUs: 400, stages: estagios(60) },
    busca:     { executor: 'ramping-arrival-rate', exec: 'buscar', startRate: 1, timeUnit: '1s',
                 preAllocatedVUs: 30, maxVUs: 150, stages: estagios(20) },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
    'http_req_duration{name:produto_detalhe}': ['p(95)<400', 'p(99)<1000'],
    'http_req_duration{name:busca}': [{ threshold: 'p(95)<800', abortOnFail: true, delayAbortEval: '2m' }],
    dropped_iterations: ['count<10'], // o gerador entregou a taxa pedida?
  },
  summaryTrendStats: ['avg', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

const campo = (res, caminho) => { try { return res.json(caminho); } catch (e) { return undefined; } }; // corpo não-JSON (ex.: 502 HTML)
const pausa = (min, max) => sleep(min + Math.random() * (max - min));                                  // think time sorteado
const produtoAleatorio = () => produtos[Math.floor(Math.random() * produtos.length)];

export function navegar() {
  const p = produtoAleatorio();
  const res = http.get(`${BASE_URL}/api/produtos/${p.id}`, { tags: { name: 'produto_detalhe' } }); // tag agrupa URLs com ID
  check(res, {
    'produto: status 200': (r) => r.status === 200,
    'produto: é o produto pedido': (r) => campo(r, 'id') === p.id, // evita "erro verde": 200 com corpo errado
  });
  pausa(2, 5);
}

export function buscar() {
  const res = http.get(`${BASE_URL}/api/busca?q=${encodeURIComponent(produtoAleatorio().nome)}`, { tags: { name: 'busca' } });
  check(res, {
    'busca: status 200': (r) => r.status === 200,
    'busca: devolveu lista': (r) => Array.isArray(campo(r, 'resultados')),
  });
  pausa(3, 7);
}
```

## Como interpretar (resumo; detalhes em `references/performance-e-carga.md`)

- Leia primeiro os thresholds ✓/✗; depois `http_req_duration` por `name`.
- `dropped_iterations` > 0: a taxa pedida não foi entregue (não mediu a carga que se acha).
- `vus_max` = `maxVUs`: faltou VU; aumente ou investigue a latência.
- Dimensionamento (Lei de Little): navegação ≈ 60 it/s × ~4 s ≈ 240 VUs; `maxVUs: 400` dá folga.
- `http_req_failed` conta todo status ≥ 400; se um passo espera 409, declare os status esperados.
- Variáveis e flags de relatório (`K6_WEB_DASHBOARD`, `--out`) mudam entre versões: confira na documentação.
