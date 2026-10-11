Montei o teste em k6 do funil busca → produto → carrinho → checkout, com cinco perfis (smoke, carga, estresse, pico e resistência) no mesmo script. **Não rodei contra o staging nem no k6 real** (sem rede e sem k6 instalado aqui). Rodei só a sintaxe e a lógica do script contra um servidor simulado; detalhes no fim.

## O que muda o número: 1.200 pedidos/hora não é a carga

3x dá **3.600 pedidos/h = 1 pedido/s** no checkout. Só que o pedido é a ponta do funil: o que o servidor sente é a quantidade de sessões que chegam na busca, e isso depende da conversão, que você não me passou. Supondo (e é só suposição) que 60% das sessões que buscam abrem um produto, 20% destes adicionam ao carrinho e 25% destes concluem, a conversão é 3%:

| Cenário k6 | Sessões/s no patamar | O que faz |
| --- | --- | --- |
| `so_busca` | 13,3 | busca e sai |
| `ate_produto` | 16,0 | busca → produto |
| `ate_carrinho` | 3,0 | busca → produto → login → carrinho, abandona |
| `compra` | 1,0 | funil completo, com frete e pedido (os 3.600 pedidos/h) |

Total: ~33 sessões/s (~120 mil/h) e ~63 req/s. Se a conversão real for 1%, o checkout continua em 1 pedido/s, mas o topo vai para ~100 sessões/s e quase 3x as requisições. Por isso as taxas do funil são parâmetros (`P_PRODUTO`, `P_CARRINHO`, `P_PEDIDO`): troque pelos números do analytics de 2025 e o script recalcula tudo, inclusive o número de VUs.

## Como o teste foi desenhado

- **Modelo aberto** (`ramping-arrival-rate`, taxa de chegada): se o staging engasgar, a carga não alivia sozinha, como acontece com cliente real. Com VUs fixos o p99 sairia otimista (coordinated omission).
- **Jornada correlacionada**: o produto vem do resultado da busca; o carrinho recebe o produto aberto; o pedido usa o `carrinhoId` e a opção de frete devolvidos. Think time sorteado entre os passos.
- **Distribuição realista**: termos de busca e posição do resultado enviesados para os populares (`SKEW`). Repetir o mesmo item mede cache e disputa de linha de estoque; espalhar tudo igual esconde o item quente da Black Friday.
- **Login por sessão** no carrinho, com uma conta por sessão. O login (hash de senha) pode ser um gargalo escondido no pico; reaproveitar token por VU esconderia isso.
- **Asserções de conteúdo**, não só status: o produto devolvido é o pedido, o carrinho contém o item, o frete tem opção, o pedido tem número. Resposta 200 com página de manutenção falha o check.
- **Proteções contra falso verde**: `pedidos_criados` precisa chegar a 90% do esperado (sem isso, o threshold de latência do pedido passaria sem amostra) e `dropped_iterations` precisa ficar perto de zero (senão o gerador não entregou a carga declarada). O `setup()` faz um preflight e **para o teste** se o staging não responder.
- **Tráfego identificável**: header `X-Execucao-Carga` e `User-Agent` próprio (APM, WAF, limpeza e conciliação) e `Idempotency-Key` no pedido.
- **Trava contra produção**: com `HOST_PRODUCAO` definido, o script recusa rodar contra esse host.

## Suposições (corrija o que estiver diferente)

Supondo que:
1. O funil é o da tabela acima.
2. "3x" é 3x **pedidos** (não 3x tráfego) e o pico de 1.200/h é o de uma hora cheia. Se o pico por minuto dentro da hora for maior que a média, use `FATOR` maior ou o perfil estresse.
3. Busca e produto são anônimos; carrinho em diante exige login; o frete é uma chamada própria; o pagamento do staging é um stub (`cartao_teste`).
4. Rotas e formato das respostas são os do comentário "Contrato" no topo do script. **Inventei esses nomes**: confirme com o OpenAPI.
5. SLOs propostos (pedido p95 < 800 ms e p99 < 2 s; busca p95 < 600 ms; produto p95 < 400 ms; carrinho p95 < 500 ms; frete p95 < 800 ms; login p95 < 1 s; erro < 1%, e < 0,5% no pedido). Sem origem em dado seu: troque pelos do APM ou do contrato.
6. "Igual à produção" significa mesma topologia, instâncias do mesmo tamanho, banco com volume parecido, mesmo CDN/WAF e mesmas flags. Se algo difere, o resultado vale como comparação, não como capacidade absoluta.

## Arquivos

`carga-black-friday.js` (abaixo), `gerar_massa.py`, `dados/termos.json`. O `dados/usuarios.json` sai do gerador.

```javascript
// carga-black-friday.js
// Funil busca -> produto -> carrinho -> checkout, em modelo aberto (taxa de chegada).
//
//   export SENHA_USUARIOS=...   # do cofre/secret do CI; não vai na linha de comando nem no repositório
//   k6 run -e BASE_URL=https://staging.exemplo.com -e PERFIL=smoke \
//          -e EXECUCAO_ID=bf-2026-10-12-01 carga-black-friday.js
//
// PERFIL: smoke | carga (padrão) | estresse | pico | resistencia. Rode nessa ordem.
//
// PREMISSAS A CONFIRMAR (marcadas com [PREMISSA]): rotas e formato das respostas,
// taxas do funil, SLOs, login exigido a partir do carrinho. As rotas e campos do
// contrato aparecem de novo em jornada()/autenticar(): ajuste os dois lugares.
import http from 'k6/http';
import { check, sleep, fail } from 'k6';
import { SharedArray } from 'k6/data';
import { Counter } from 'k6/metrics';
import exec from 'k6/execution';

// ---------- Configuração: tudo vem do ambiente ----------
const num = (nome, padrao) => (__ENV[nome] ? Number(__ENV[nome]) : padrao);

const BASE_URL = __ENV.BASE_URL;
const SENHA = __ENV.SENHA_USUARIOS; // senha única das contas sintéticas de carga (criadas no staging)
const PERFIL = __ENV.PERFIL || 'carga';
const EXECUCAO_ID = __ENV.EXECUCAO_ID || 'carga-bf'; // identifica o tráfego no APM, WAF e banco
if (!BASE_URL) throw new Error('Defina BASE_URL do STAGING: -e BASE_URL=https://...');
if (!SENHA) throw new Error('Defina SENHA_USUARIOS (senha das contas sintéticas de carga).');
// Trava opcional: -e HOST_PRODUCAO=www.loja.com.br impede rodar contra produção por engano.
if (__ENV.HOST_PRODUCAO && BASE_URL.includes(__ENV.HOST_PRODUCAO)) {
  throw new Error('BASE_URL aponta para produção. Teste de carga em produção exige autorização e janela próprias.');
}

// ---------- Funil/SLO [PREMISSA: substitua pelos números do analytics e do APM] ----------
const PEDIDOS_HORA_BASE = num('PEDIDOS_HORA_BASE', 1200); // pico de 2025
const FATOR = num('FATOR', 3); // expectativa do comercial (confirmar: 3x de pedidos, não de sessões)
const P_PRODUTO = num('P_PRODUTO', 0.6); // das sessões que buscam, % que abre um produto
const P_CARRINHO = num('P_CARRINHO', 0.2); // dos que abrem produto, % que adiciona ao carrinho
const P_PEDIDO = num('P_PEDIDO', 0.25); // dos que têm carrinho, % que conclui o pedido
const SKEW = num('SKEW', 3); // 1 = uniforme; maior = mais concentrado nos termos/produtos populares

// SLOs propostos, sem origem em dado do time: troque pelos do APM/contrato.
const SLO = {
  busca: ['p(95)<600', 'p(99)<1500'],
  produto: ['p(95)<400', 'p(99)<1000'],
  login: ['p(95)<1000'],
  carrinho_adicionar: ['p(95)<500', 'p(99)<1200'],
  frete: ['p(95)<800', 'p(99)<2000'],
  pedido_criar: ['p(95)<800', 'p(99)<2000'],
};

// ---------- Contrato [PREMISSA: confirme contra o OpenAPI/APM] ----------
// GET  /api/busca?q=termo            200 { itens: [{ id, nome, preco }] }
// GET  /api/produtos/{id}            200 { id, preco }
// POST /api/login                    200 { access_token, expires_in }   (exigido do carrinho em diante)
// POST /api/carrinho/itens           201 { carrinhoId, itens: [{ produtoId, quantidade }] }
// GET  /api/frete?carrinhoId&cep     200 { opcoes: [{ codigo, valor, prazo }] }
// POST /api/pedidos                  201 { numero }   (pagamento no stub, forma 'cartao_teste')
const CEPS = ['01310100', '20040020', '30130010', '40020000', '80010000', '90010000', '70040010', '69005010', '66010000', '60025100'];

// ---------- Dados (gerados; ver gerar_massa.py) ----------
const usuarios = new SharedArray('usuarios', () => JSON.parse(open('./dados/usuarios.json')));
const termos = new SharedArray('termos', () => JSON.parse(open('./dados/termos.json'))); // ordenados por popularidade

// ---------- Modelo de carga ----------
const minutos = (d) => { // aceita o formato do k6: 30s, 20m, 1h30m
  if (!/^(\d+(\.\d+)?[hms])+$/.test(d)) throw new Error(`Duração inválida: ${d} (exemplos: 30s, 20m, 1h30m)`);
  const parte = /(\d+(?:\.\d+)?)([hms])/g;
  let total = 0, m;
  while ((m = parte.exec(d)) !== null) total += Number(m[1]) * { s: 1 / 60, m: 1, h: 60 }[m[2]];
  return total;
};

const PEDIDOS_MIN = (PEDIDOS_HORA_BASE * FATOR) / 60; // pedidos por minuto no patamar
const SESSOES_MIN = PEDIDOS_MIN / (P_PRODUTO * P_CARRINHO * P_PEDIDO); // sessões que começam buscando
// Sessões por minuto em cada ponto de saída do funil (soma = SESSOES_MIN).
const TAXA_MIN = {
  soBusca: SESSOES_MIN * (1 - P_PRODUTO),
  ateProduto: SESSOES_MIN * P_PRODUTO * (1 - P_CARRINHO),
  ateCarrinho: SESSOES_MIN * P_PRODUTO * P_CARRINHO * (1 - P_PEDIDO),
  ateCompra: PEDIDOS_MIN,
};
// Duração média estimada de cada jornada em segundos (latência + think time), para dimensionar VUs (Lei de Little).
const DURACAO_EST = { soBusca: 1.5, ateProduto: 6, ateCarrinho: 13, ateCompra: 30 };

// Perfis: lista de [múltiplo do alvo, duração]. 1 = FATOR x pico de 2025.
const PERFIS = {
  smoke: [[0.03, '30s'], [0.03, '2m30s']],
  carga: [[1 / 6, '2m'], [1, '5m'], [1, __ENV.PATAMAR || '20m'], [0, '2m']],
  estresse: [
    [0.5, '3m'],
    ...[].concat(...[1, 1.25, 1.5, 2].map((m) => [[m, '2m'], [m, '5m']])), // degraus de 1x a 2x do alvo
    [0.5, '3m'], [0.5, '5m'], // recuperação: o sistema volta ao normal?
  ],
  // pico: do pico de 2025 (1/FATOR do alvo) ao alvo em 30 s, simulando a virada da promoção
  pico: [[1 / FATOR, '3m'], [1 / FATOR, '3m'], [1, '30s'], [1, '10m'], [1 / FATOR, '30s'], [1 / FATOR, '5m']],
  resistencia: [[0.5, '5m'], [0.5, __ENV.DURACAO_RESISTENCIA || '4h'], [0, '2m']],
};
if (!PERFIS[PERFIL]) throw new Error(`PERFIL inválido: ${PERFIL}. Use ${Object.keys(PERFIS).join(' | ')}`);
const MULT_MAX = Math.max(...PERFIS[PERFIL].map(([m]) => m));

// Taxa em iterações/minuto: o k6 só aceita taxa inteira, e 1 pedido/s ou menos pede unidade menor que 1 s.
function estagios(taxaMin) {
  return PERFIS[PERFIL].map(([m, d]) => ({ target: m > 0 ? Math.max(1, Math.round(taxaMin * m)) : 0, duration: d }));
}
function iteracoesPrevistas(stages) { // área sob a rampa (startRate = 0)
  let anterior = 0, total = 0;
  for (const s of stages) { total += ((anterior + s.target) / 2) * minutos(s.duration); anterior = s.target; }
  return Math.floor(total);
}
function cenario(funcao, chave) {
  const stages = estagios(TAXA_MIN[chave]);
  const necessarios = (TAXA_MIN[chave] * MULT_MAX / 60) * DURACAO_EST[chave]; // VUs em regime
  return {
    executor: 'ramping-arrival-rate', exec: funcao, startRate: 0, timeUnit: '1m',
    preAllocatedVUs: Math.max(2, Math.ceil(necessarios * 1.5)),
    maxVUs: Math.max(5, Math.ceil(necessarios * 3)), // folga para quando a latência subir
    stages, tags: { fluxo: funcao },
  };
}

const cenarios = {
  so_busca: cenario('soBusca', 'soBusca'),
  ate_produto: cenario('ateProduto', 'ateProduto'),
  ate_carrinho: cenario('ateCarrinho', 'ateCarrinho'),
  compra: cenario('ateCompra', 'ateCompra'),
};
const PEDIDOS_ESPERADOS = iteracoesPrevistas(cenarios.compra.stages);
const LOGINS_ESPERADOS = iteracoesPrevistas(cenarios.ate_carrinho.stages) + PEDIDOS_ESPERADOS;

// No perfil carga, a execução para quando o SLO do checkout já foi violado (após o aquecimento).
const aborta = (t) => (PERFIL === 'carga' ? { threshold: t, abortOnFail: true, delayAbortEval: '4m' } : t);

const thresholds = {
  http_req_failed: ['rate<0.01'],
  'http_req_failed{name:pedido_criar}': ['rate<0.005'],
  checks: ['rate>0.99'],
  dropped_iterations: ['count<30'], // o gerador entregou a taxa pedida? Se não, a carga medida é menor que a declarada
  // Guarda contra falso verde: sem pedidos criados não há amostra de pedido_criar e o threshold de latência passaria vazio.
  pedidos_criados: [`count>=${Math.max(1, Math.floor(PEDIDOS_ESPERADOS * 0.9))}`],
};
for (const [nome, limites] of Object.entries(SLO)) {
  thresholds[`http_req_duration{name:${nome}}`] = nome === 'pedido_criar' ? limites.map(aborta) : limites;
}

export const options = {
  scenarios: cenarios,
  thresholds,
  userAgent: 'k6-carga-blackfriday', // para a equipe de rede/WAF reconhecer o gerador
  summaryTrendStats: ['avg', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

// ---------- Métricas de negócio ----------
const pedidosCriados = new Counter('pedidos_criados');
const buscasSemResultado = new Counter('buscas_sem_resultado');

// ---------- Utilitários ----------
const cabecalhos = (extra = {}) => ({ Accept: 'application/json', 'X-Execucao-Carga': EXECUCAO_ID, ...extra });
const corpo = (res) => { try { return res.json(); } catch (e) { return null; } }; // 502 em HTML não derruba a iteração
const pausa = (min, max) => sleep(min + Math.random() * (max - min)); // think time sorteado
const enviesado = (n) => Math.floor(Math.pow(Math.random(), SKEW) * n); // 0 é o mais provável
const escolher = (lista) => lista[enviesado(lista.length)];

export function setup() {
  // Preflight: URL errada ou staging fora do ar é bloqueio, não resultado de carga.
  const r = http.get(`${BASE_URL}/api/busca?q=${encodeURIComponent(termos[0])}`, { headers: cabecalhos(), tags: { name: 'preflight' } });
  if (r.status !== 200) fail(`Preflight falhou: GET /api/busca devolveu ${r.status}. Verifique BASE_URL e o ambiente.`);
  if (usuarios.length < LOGINS_ESPERADOS) {
    console.warn(`usuarios.json tem ${usuarios.length} contas e o perfil prevê ~${LOGINS_ESPERADOS} sessões autenticadas: haverá reuso de conta (carrinho antigo da mesma conta pode sobrar).`);
  }
  console.log(JSON.stringify({
    execucao: EXECUCAO_ID, perfil: PERFIL, pedidosHoraAlvo: PEDIDOS_HORA_BASE * FATOR,
    sessoesPorSegundoNoPatamar: Number((SESSOES_MIN / 60).toFixed(1)),
    funil: { P_PRODUTO, P_CARRINHO, P_PEDIDO }, pedidosEsperados: PEDIDOS_ESPERADOS,
  }));
}

function autenticar() {
  const u = usuarios[exec.scenario.iterationInTest % usuarios.length]; // uma conta por sessão, sem reuso enquanto houver contas
  const res = http.post(`${BASE_URL}/api/login`, JSON.stringify({ email: u.email, senha: SENHA }), {
    headers: cabecalhos({ 'Content-Type': 'application/json' }), tags: { name: 'login' },
  });
  const c = corpo(res);
  const ok = check(res, {
    'login: status 200': (r) => r.status === 200,
    'login: devolveu token': () => !!c && typeof c.access_token === 'string',
  });
  return ok ? c.access_token : null;
}

// Percorre o funil até o passo `ate`. Cada retorno antecipado é uma falha já registrada em check().
function jornada(ate) {
  // 1. Busca (anônima) com termo do analytics, enviesado para os mais populares
  const termo = escolher(termos);
  const rBusca = http.get(`${BASE_URL}/api/busca?q=${encodeURIComponent(termo)}`, { headers: cabecalhos(), tags: { name: 'busca' } });
  const cBusca = corpo(rBusca);
  const itens = cBusca && Array.isArray(cBusca.itens) ? cBusca.itens : null;
  if (!check(rBusca, { 'busca: status 200': (r) => r.status === 200, 'busca: corpo com lista de itens': () => itens !== null })) return;
  if (itens.length === 0) { buscasSemResultado.add(1); return; } // zero resultados é caminho válido, não erro
  if (ate === 'busca') return;

  // 2. Produto: a correlação vem do resultado da busca, não de uma lista fixa
  pausa(2, 5);
  const escolhido = escolher(itens); // posições do topo da lista são as mais clicadas
  const rProduto = http.get(`${BASE_URL}/api/produtos/${escolhido.id}`, { headers: cabecalhos(), tags: { name: 'produto' } });
  const cProduto = corpo(rProduto);
  if (!check(rProduto, {
    'produto: status 200': (r) => r.status === 200,
    'produto: é o produto pedido': () => !!cProduto && cProduto.id === escolhido.id,
    'produto: preço positivo': () => !!cProduto && Number(cProduto.preco) > 0,
  })) return;
  if (ate === 'produto') return;

  // 3. Carrinho (autenticado)
  pausa(3, 8);
  const token = autenticar();
  if (!token) return;
  const auth = cabecalhos({ 'Content-Type': 'application/json', Authorization: `Bearer ${token}` });
  const rCarrinho = http.post(`${BASE_URL}/api/carrinho/itens`, JSON.stringify({ produtoId: escolhido.id, quantidade: 1 }),
    { headers: auth, tags: { name: 'carrinho_adicionar' } });
  const cCarrinho = corpo(rCarrinho);
  const carrinhoId = cCarrinho && cCarrinho.carrinhoId;
  if (!check(rCarrinho, {
    'carrinho: status 201 com id': (r) => r.status === 201 && !!carrinhoId,
    'carrinho: contém o produto escolhido': () => !!cCarrinho && Array.isArray(cCarrinho.itens)
      && cCarrinho.itens.some((i) => i.produtoId === escolhido.id && i.quantidade >= 1),
  })) return;
  if (ate === 'carrinho') return;

  // 4. Checkout: frete e pedido. Pagamento, antifraude e frete externo devem estar em stub com latência realista.
  pausa(3, 10);
  const cep = CEPS[Math.floor(Math.random() * CEPS.length)];
  const rFrete = http.get(`${BASE_URL}/api/frete?carrinhoId=${carrinhoId}&cep=${cep}`, { headers: auth, tags: { name: 'frete' } });
  const cFrete = corpo(rFrete);
  if (!check(rFrete, {
    'frete: status 200': (r) => r.status === 200,
    'frete: tem opção de entrega': () => !!cFrete && Array.isArray(cFrete.opcoes) && cFrete.opcoes.length > 0,
  })) return;
  pausa(5, 15);
  const chave = `${EXECUCAO_ID}-${exec.vu.idInTest}-${exec.vu.iterationInInstance}-${Date.now()}`;
  const rPedido = http.post(`${BASE_URL}/api/pedidos`,
    JSON.stringify({ carrinhoId, cep, freteCodigo: cFrete.opcoes[0].codigo, formaPagamento: 'cartao_teste' }),
    { headers: { ...auth, 'Idempotency-Key': chave }, tags: { name: 'pedido_criar' } });
  const cPedido = corpo(rPedido);
  const criado = check(rPedido, {
    'pedido: status 201': (r) => r.status === 201,
    'pedido: tem número': () => !!cPedido && !!cPedido.numero,
  });
  if (criado) pedidosCriados.add(1);
}

export function soBusca() { jornada('busca'); }
export function ateProduto() { jornada('produto'); }
export function ateCarrinho() { jornada('carrinho'); }
export function ateCompra() { jornada('pedido'); }
```

`gerar_massa.py` cria `dados/usuarios.json` com contas `carga.000001@example.com` etc. (domínio reservado, nunca entrega e-mail):

```python
#!/usr/bin/env python3
"""Gera dados/usuarios.json com contas sintéticas para o teste de carga.

Uso: python3 gerar_massa.py --n 10000
Os e-mails usam example.com (domínio reservado, nunca entrega). As contas precisam
ser criadas no STAGING pela equipe (seed/API), com a mesma senha informada em
SENHA_USUARIOS, com notificações (e-mail/SMS) desligadas ou apontando para um sumidouro.
A senha não é gerada nem gravada aqui.
"""
import argparse
import json
import pathlib

p = argparse.ArgumentParser()
p.add_argument("--n", type=int, default=10000, help="quantidade de contas")
p.add_argument("--saida", default="dados/usuarios.json")
a = p.parse_args()

contas = [{"email": f"carga.{i:06d}@example.com"} for i in range(1, a.n + 1)]
destino = pathlib.Path(a.saida)
destino.parent.mkdir(parents=True, exist_ok=True)
destino.write_text(json.dumps(contas, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{len(contas)} contas em {destino}")
```

`dados/termos.json` é uma lista de strings **em ordem de popularidade**. A que mandei é um exemplo de 30 termos (com variação de acento, erro de digitação e um termo sem resultado). Substitua pelos termos reais do analytics de busca, incluindo cauda longa.

## Como rodar

```bash
python3 gerar_massa.py --n 10000                 # e criar essas contas no staging, com a senha de SENHA_USUARIOS
export SENHA_USUARIOS=...                        # do cofre/secret, não na linha de comando
K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=relatorio-carga.html \
  k6 run -e BASE_URL=https://staging.exemplo.com -e PERFIL=smoke -e EXECUCAO_ID=bf-smoke-01 carga-black-friday.js
```

Rode nesta ordem, só avançando se o anterior estiver limpo:

| Perfil | Duração | Pergunta |
| --- | --- | --- |
| `smoke` | 3 min, 3% do alvo | script, massa e ambiente funcionam? (a maior parte dos "problemas de performance" da primeira rodada é script errado) |
| `carga` | 29 min (2 aquecimento, 5 rampa, 20 patamar, 2 descida) | aguenta 3x dentro do SLO? |
| `estresse` | ~39 min, degraus de 1x a 2x do alvo e recuperação | onde fica o joelho, como degrada e se volta ao normal |
| `pico` | 22 min, do pico de 2025 ao alvo em 30 s | a virada de meia-noite derruba? o autoscaling chega a tempo? |
| `resistencia` | 4 h a 50% do alvo (`DURACAO_RESISTENCIA`) | vazamento de memória, conexões ou fila |

O k6 sai com código 99 se um threshold falhar. No perfil `carga`, a execução aborta sozinha se o p95/p99 do pedido estourar depois dos 4 min de aquecimento. No `estresse` não aborta, porque o objetivo é ver a degradação: threshold vermelho ali é informação, não defeito do teste.

**Leia assim:** o veredito vem do patamar na série temporal do dashboard (o resumo final mistura aquecimento e rampa). Antes de olhar latência, confira `dropped_iterations` ≈ 0, `vus_max` abaixo do `maxVUs` de cada cenário e `pedidos_criados` perto do esperado (o `setup()` imprime o esperado; ~1.450 na carga). Se alguma dessas falhar, você não mediu a carga que acha que mediu.

## Antes do primeiro run

- **Autorização e janela** com quem opera aplicação, banco, rede, CDN/WAF e nuvem; sem aviso, carga parece ataque. Combine volume máximo, horário, contato e como interromper. Se o WAF bloquear o gerador, a liberação é deles; não contorne.
- **Terceiros em stub com latência realista** (gateway de pagamento, antifraude, cálculo de frete, NF-e). Apontar para o sandbox real mede o terceiro e esbarra no limite de taxa dele. E-mail e SMS desligados ou para um sumidouro.
- **Massa**: contas suficientes (a carga usa ~6.000 sessões autenticadas; o `setup()` avisa se faltar) e **estoque alto nos itens populares**. Erro de estoque no teste é massa mal semeada (ou bug de reserva), não capacidade.
- **Monitoramento ligado antes** (APM, CPU/memória por camada, pool de conexões, consultas lentas e locks, filas) **e no próprio gerador**: CPU abaixo de ~70–80%. A carga usa até ~555 VUs (~1.100 no estresse); se o gerador saturar, distribua.
- **Manifesto do ambiente** registrado: commit, instâncias, tamanho da base, flags, versão dos stubs. É ele que sustenta o "igual à produção".
- **CDN/cache**: busca e produto são GET e podem ser servidos da borda. Decida se o alvo é a borda ou a origem; para medir a origem, reduza o `SKEW` e combine com quem opera o CDN.

## Depois do teste: conferir no banco

O que o k6 vê é a resposta; o dano caro é silencioso. Conte linhas, não respostas:

- Pedidos criados no banco com o marcador da execução (`X-Execucao-Carga`) **=** `pedidos_criados` do k6. Sobra é pedido duplicado; falta é pedido perdido.
- Nenhum item com estoque negativo.
- Filas (e-mail, NF-e, pagamento) drenaram, sem backlog parado.
- Limpar por `EXECUCAO_ID`, nunca por "apagar pedidos de hoje".

## O que fica de fora (e o risco que sobra)

- **Capacidade de terceiros reais**: com stubs, o teste não diz se gateway, antifraude e transportadora aguentam 1 pedido/s nem se há limite de taxa contratado. É um ponto frequente de limite no pico; peça os limites aos fornecedores.
- **Disputa pelo último item e cupom concorrente** (venda acima do estoque): não está aqui. Peça um teste de concorrência dirigido em um SKU com pouco estoque.
- **Front-end**: assets, CDN, JavaScript e Web Vitals (LCP/INP/CLS) e o app mobile não são medidos por um teste HTTP. Dá para somar 1–5 VUs de navegador (`k6/browser`) sobre esta carga.
- **Tráfego de robôs/scraping** e o pico de um minuto específico (dependem de log real).
- **Extrapolação**: se o staging não for realmente igual, isso é palpite, e o resultado só vale como regressão relativa.

## O que verifiquei e o que não

- **Executado aqui**: `node --check` na sintaxe; o script rodado com k6 e HTTP simulados nas quatro jornadas (percurso certo de rotas em cada uma), nos caminhos de erro (502 em HTML, produto errado, carrinho sem o item, busca sem resultado) e no cálculo de taxas, VUs e estágios dos cinco perfis. Achei e corrigi um bug nesse processo (duração composta como `2m30s`).
- **Não verificado**: execução no k6 real, o contrato de API real, o comportamento do staging e os SLOs. Taxas e VUs derivam das suposições acima.

## Perguntas cuja resposta muda o resultado

1. Pedidos e **sessões** por hora no pico de 2025, e o pico por minuto dentro daquela hora (dá a conversão real e corrige o topo do funil).
2. "3x" é de pedidos ou de tráfego? Inclui margem?
3. Latência atual de produção (p95 por endpoint) e SLOs formais, se existirem.
4. OpenAPI das rotas: o carrinho exige login? o checkout é uma chamada ou várias? há cupom?
5. Os terceiros do staging são stubs ou sandbox real? O "igual à produção" inclui CDN/WAF e volume da base?
6. Quem autoriza, em qual janela, e quem opera WAF/CDN?
7. Como semear 6–10 mil contas e o estoque no staging?
