Montei o teste k6 do fluxo busca → produto → carrinho (com frete) → checkout, com perfis de smoke, baseline, carga esperada, stress, spike e soak. Os endpoints, o funil de conversão e os SLOs são suposições minhas e precisam ser trocados pelos seus (detalhes abaixo). Não consegui rodar o k6 de verdade aqui, então o primeiro passo é o perfil `smoke`.

Arquivos:
- `blackfriday.js`: o script, com a configuração e os perfis no topo.
- `data/search-terms.json`: termos de busca, divididos em populares e cauda longa.
- `data/zipcodes.json`: CEPs para o cálculo de frete.

## O que significa "3x"

3x de 1.200 pedidos/h são 3.600 pedidos/h, ou seja, **1 pedido por segundo** em média. Para o checkout isso é pouco. Quem costuma quebrar é a concorrência em horários curtos, o estoque nos produtos mais vendidos, os serviços externos (pagamento, frete, antifraude) e a busca. Três pontos mudam o tamanho do teste:

1. **Pedidos por hora é uma média.** Na virada da meia-noite ou num push de campanha o pico por minuto pode ser 2 a 3 vezes a média horária. O perfil `spike` salta para 4,5x em 30 segundos e depois testa a recuperação.
2. **Pedidos não medem o tráfego de navegação.** Na Black Friday a conversão costuma cair, então busca e produto crescem mais que 3x. O script deriva o número de sessões a partir de um funil que eu chutei (busca→produto 70%, produto→carrinho 20%, carrinho→checkout 50%, cerca de 7% de sessões viram pedido). Se a conversão real for 2%, o tráfego de busca e produto é cerca de 3,5 vezes maior que o do teste. **O número mais valioso que você pode me passar é o de sessões/h e buscas/h do pico do ano passado.** Com ele, rode com `-e SESSIONS_PER_HOUR_1X=<valor>`.
3. **Margem.** O teste de carga (`load`) mira os 3x. Eu aprovaria a Black Friday só se o sistema também aguentasse cerca de 1,5x a previsão (4,5x, uns 5.400 pedidos/h) sem degradar. O `spike` usa esse valor e o `stress` sobe até 6x para achar o ponto de quebra.

Com os padrões, o patamar de 3x dá cerca de 875 sessões/min (14,6/s). Isso rende uns 3.600 pedidos/h e uns 45 requisições/s só neste funil. Um gerador k6 comum aguenta isso. Só use outra máquina em vez do notebook por causa da rede, e monitore a CPU do gerador.

## Como o teste foi desenhado

- **Modelo aberto** (`ramping-arrival-rate`): as sessões chegam na taxa definida mesmo que o sistema fique lento, como acontece na Black Friday. Com VUs fixos o teste "alivia" a própria carga quando o sistema degrada e esconde o problema.
- **Funil probabilístico**: cada sessão busca e abandona em cada etapa com a probabilidade configurada. O produto vem dos resultados da busca, favorecendo o topo. Há entrada direta por link de campanha (`FLASH_PRODUCT_ID`) para simular concorrência em um produto em promoção.
- **Métricas de funil**: `funnel_1..4`, `orders_created`, `order_success`, `rate_limited_429_503`, `cart_conflict_409` e `step_failures` por etapa.
- **Thresholds** (placeholders, ver abaixo):
  - erro HTTP < 1%, com abort após 2 min;
  - sucesso de pedido > 98%;
  - `dropped_iterations` = 0. Se for maior que 0, o teste não entregou a carga pedida e o resultado não vale;
  - p95/p99 por etapa.
- **Dados**: e-mails `lt+<run>-...@loadtest.invalid`, header `X-Load-Test`, `Idempotency-Key` por pedido. Isso facilita a limpeza e a identificação do tráfego de teste no backend.

| Perfil | Carga | Duração |
|---|---|---|
| `smoke` | 1 VU, funil completo, 3 pedidos | 1 min |
| `baseline` | 1x (1.200 pedidos/h) | 14 min |
| `load` | 3x, patamar de 30 min (`HOLD`) | 40 min |
| `stress` | 3x → 4x → 5x → 6x, degraus de 10 min | 55 min |
| `spike` | 1x → 4,5x em 30 s, 5 min, volta a 1x e observa a recuperação | 22 min |
| `soak` | 3x por 2 h (`SOAK_DURATION`) | cerca de 2 h 10 |

## Antes de rodar (o que pode dar errado no staging)

"Igual a produção" precisa valer em quatro pontos, senão o resultado engana:

1. **Pagamento, antifraude, frete, e-mail/SMS, ERP e nota fiscal em sandbox ou mock.** Se algum for real, o teste cobra cartões, dispara mensagens para clientes e queima cota ou conta de terceiros. O script exige `PAYMENT_TOKEN` e só aceita host com cara de staging (`staging`, `stg`, `hml`, `qa`, `test`). Mesmo assim, confirme você mesmo.
2. **Volume de dados e configuração.** Confirme tamanho do catálogo e do índice de busca, volume do banco, cache aquecido, autoscaling, limites de pool e réplicas. Infra igual com banco pequeno dá resultado bom demais.
3. **Estoque e limpeza.** Só o patamar do `load` gera cerca de 1.800 pedidos. Os SKUs de teste precisam de estoque enorme ou de um reset. Pedidos com 409 aparecem em `cart_conflict_409` e indicam problema no dado, não no sistema. Tenha também uma rotina para cancelar ou apagar pedidos pelo domínio `@loadtest.invalid` e pelo `X-Load-Test`.
4. **WAF, CDN e rate limit por IP.** O tráfego sai de poucos IPs. Libere o gerador, senão você mede o WAF. Avise as outras equipes que usam o staging e marque uma janela.

Sem APM, métricas de banco e de filas no staging, o k6 só diz que ficou lento, não o motivo. Mande as métricas do k6 para o seu Prometheus/Grafana/InfluxDB com `--out` e use `--tag testid=...` para cruzar com os painéis.

## Como rodar

Rode a partir da pasta do script, porque ele lê `data/`.

```bash
export PAYMENT_TOKEN=<token de sandbox>   # não passe segredo na linha de comando
k6 run -e BASE_URL=https://staging.loja-exemplo.com.br -e PROFILE=smoke blackfriday.js

# depois, nesta ordem:
k6 run -e BASE_URL=... -e PROFILE=baseline --summary-export=baseline.json blackfriday.js
k6 run -e BASE_URL=... -e PROFILE=load     --summary-export=load.json     blackfriday.js
k6 run -e BASE_URL=... -e PROFILE=stress   blackfriday.js
k6 run -e BASE_URL=... -e PROFILE=spike    blackfriday.js
k6 run -e BASE_URL=... -e PROFILE=soak     blackfriday.js
```

No fim de cada rodada, confira:

1. `dropped_iterations` deve ser 0. Se aparecer "Insufficient VUs", aumente `AVG_SESSION_SEC`.
2. `orders_created` deve estar perto da meta (cerca de 1 pedido/s no patamar de 3x).
3. Nenhum threshold deve estar vermelho.

Depois, olhe o lado do servidor. O pedido criado não é pedido processado, então veja se as filas (ERP, nota, estoque) drenaram e quanto tempo levaram.

Rode o `baseline` primeiro e compare com o que a produção fez no ano passado. Se o staging não reproduzir as latências conhecidas, ele não é "igual" e os números dos outros perfis não servem para decidir.

## O que preciso de você ou o que você precisa ajustar

- **Contrato da API.** Os endpoints (`/api/search`, `/api/products/:id`, `/api/carts`, `/api/carts/:id/items`, `/api/carts/:id/shipping-quote`, `/api/checkout`) e os campos das respostas são inventados. Os pontos a adaptar estão marcados com `ADAPTAR`. Se você mandar um HAR do fluxo ou o OpenAPI, eu ajusto.
- **Funil e tráfego real** (sessões/h, buscas/h, conversão por etapa), como explicado acima.
- **SLOs.** Os limites de p95/p99 do script são placeholders. Defina com produto e engenharia o que é "aprovado".
- **Dados reais**: termos de busca (top-N do ano passado), CEPs válidos para o seu frete, e CPF de teste via `TEST_DOCUMENT`. Nunca use CPF ou e-mail de pessoa real.
- **Origem do número 1.200.** É a média da hora mais cheia ou o pico por minuto extrapolado? Isso muda o perfil de spike.

## O que este teste não cobre

- Login. O fluxo é de visitante, e se a maioria compra logada a autenticação precisa entrar.
- Autocomplete da busca, filtros e paginação, home e páginas de campanha.
- Imagens, CDN e front-end (o k6 aqui testa só a API).
- Cupom, PIX e boleto com confirmação assíncrona.
- Falhas induzidas, como gateway lento ou queda de réplica.

A Black Friday cai em 27/11, daqui a cerca de 7 semanas. Sugiro rodar smoke e baseline já esta semana, load e stress na seguinte, e deixar de 2 a 3 semanas para corrigir o que aparecer. Depois, repita o `load`, rode o `spike` e o `soak`, e congele mudanças na semana anterior.
