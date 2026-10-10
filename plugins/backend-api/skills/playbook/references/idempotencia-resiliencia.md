# Idempotência, resiliência, rate limit, webhooks, filas e cache

Referência para `idempotency-and-resilience` (recorte "de API/serviço": padrões de pagamentos e integrações SaaS completas ficam em `/fintech-payments:playbook` e `/automation-integrations:playbook`). Fontes: `V-nn` em `fontes.md`; brain = brain-of-agent (`backend-e-contratos.md`, `automacao-api.md`, MIT). Migrações aqui são **propostas**: o agente as escreve e roda só em banco de teste local; staging e produção são do humano.

## Sumário

- [1. Idempotência: o problema e o menu de políticas](#1-idempotência-o-problema-e-o-menu-de-políticas)
- [2. Desenho do armazenamento e algoritmo](#2-desenho-do-armazenamento-e-algoritmo)
- [3. Timeouts, retries e circuit breaker](#3-timeouts-retries-e-circuit-breaker)
- [4. Rate limiting](#4-rate-limiting)
- [5. Webhooks recebidos](#5-webhooks-recebidos)
- [6. Filas, jobs, DLQ e outbox](#6-filas-jobs-dlq-e-outbox)
- [7. Concorrência otimista](#7-concorrência-otimista)
- [8. Cache de aplicação](#8-cache-de-aplicação)
- [9. Testes que provam](#9-testes-que-provam)

## 1. Idempotência: o problema e o menu de políticas

Cenário (brain): o cliente recebe timeout depois de um pagamento aceito e tenta de novo. Sem proteção, cada `POST` cobra novamente. Idempotência de **método** HTTP (`PUT`, `DELETE`) não substitui uma chave de **operação de negócio** para `POST` com efeito (cobrança, envio, criação).

Políticas publicadas (V-15, V-16, V-35; comparação em `decisoes-e-tradeoffs.md`, seção 7). O header e os códigos de conflito são **escolhas de contrato**, não padrão universal:

| Decisão | Opções |
| --- | --- |
| Onde viaja a chave | header `Idempotency-Key` (draft expirado, mas amplamente usado), `request_id` no corpo (AIP-155, UUID de até 36 caracteres), `Repeatability-*` (Azure) |
| Quem gera | O cliente (UUID v4 ou string aleatória; Stripe aceita até 255 caracteres, sem dado pessoal) |
| Corpo diferente com a mesma chave | Erro (Stripe; 422 no draft) |
| Em processamento | 409 (draft) ou espera/erro conforme política |
| Falha de validação | Não consome a chave (o cliente corrige e repete) |
| Retenção | Mínimo de 24 h na Stripe; "janela razoável" no AIP-155; mínimo de 5 min na Azure. Documente a sua (boa prática, *Inferido*) |
| Escopo | Usuário/tenant/operação; chave global e previsível permite colisão ou descoberta entre tenants |

Stripe v1 salva status e corpo da **primeira** resposta depois que a execução começou (inclusive 500); a v2 completa trabalho parcial (semântica diferente). Não misture.

## 2. Desenho do armazenamento e algoritmo

O banco garante a atomicidade; checar na aplicação e inserir depois deixa corrida e permite duas cobranças.

```sql
-- Proposta (PostgreSQL; adaptar à engine). Executar só em banco de teste; produção é do humano.
CREATE TABLE idempotency_keys (
  scope_id        text        NOT NULL,   -- usuário ou tenant
  operation       text        NOT NULL,   -- ex.: 'POST /payments'
  key             text        NOT NULL,
  request_hash    text        NOT NULL,   -- hash dos parâmetros relevantes (fingerprint)
  state           text        NOT NULL CHECK (state IN ('in_progress', 'completed')),
  response_status integer,
  response_body   jsonb,
  created_at      timestamptz NOT NULL DEFAULT now(),
  expires_at      timestamptz NOT NULL,
  PRIMARY KEY (scope_id, operation, key)
);
CREATE INDEX idempotency_keys_expires_at ON idempotency_keys (expires_at);  -- limpeza
```

Algoritmo (Inferido a partir de V-15, V-16, V-31 e do brain):

1. Valide a requisição **antes** de tocar na chave: entrada inválida devolve 400/422 sem consumi-la.
2. `INSERT ... ON CONFLICT DO NOTHING` com `state = 'in_progress'`. Inseriu: execute o efeito, preferindo a **mesma transação** do dado de negócio; ao fim, grave `state = 'completed'`, status e corpo.
3. Não inseriu: leia a linha. `request_hash` diferente: devolva o código da política (default 422). `in_progress`: 409 (ou espere com prazo). `completed`: **reproduza** status e corpo originais, com o mesmo `Location`.
4. Falha **antes** do efeito: remova ou libere a chave. Falha **depois** de gravar o efeito com resposta não registrada: a política decide (Stripe salva inclusive o 500).
5. Linha `in_progress` órfã (processo morreu): trate por `expires_at`/timeout de lock definido na política; documente.
6. Limpeza periódica por `expires_at`.

Efeitos externos (gateway de pagamento) precisam da própria idempotência: envie ao provedor uma chave derivada e estável da operação, nunca uma nova a cada tentativa.

## 3. Timeouts, retries e circuit breaker

Do brain (MIT), com V-17 e V-18:

- **Orçamento por salto:** distribua o prazo do usuário entre as chamadas; nenhuma chamada consome o prazo inteiro.
- **Tentativas limitadas** e classificação de erro: retry em erro transitório (timeout, 503, `UNAVAILABLE`); nunca em permanente (400, 404, `INVALID_ARGUMENT`, `FAILED_PRECONDITION`); respeite `Retry-After` e a orientação do fornecedor.
- **Idempotência antes do retry:** retry automático só é seguro depois de entender a semântica da operação e a aceitação desconhecida (o cliente não sabe se completou).
- **Backoff exponencial com jitter** quando justificável (por exemplo `espera = random(0, min(teto, base * 2^tentativa))`): fórmula *Inferida* de conhecimento estável; fonte primária (AWS Builders' Library) é lacuna declarada.
- **Circuit breaker** limita tentativas durante a falha; **não** corrige inconsistência nem substitui idempotência.
- Go: `http.Client` sempre com timeout e `defer resp.Body.Close()` (V-18). gRPC: deadline em toda chamada, propagado ao próximo salto.
- Aceitar enfileirar não é concluir: responda conforme o compromisso (202 + estado), nunca 200 de "feito".

## 4. Rate limiting

Contrato (V-33, V-09 API4, V-10; o draft IETF está na revisão 11, de 23/05/2026, expira em 24/11/2026 e **não é RFC**):

1. **429** com corpo `application/problem+json` e `Retry-After`.
2. A **chave** do limite vem de credencial **validada** (identidade + plano + endpoint), nunca de header livre como `x-api-key` não verificado (o demo do blog de origem era burlável por isso). IP sozinho é fraco (NAT, proxies): combine.
3. Janela deslizante ou token bucket em armazenamento **compartilhado** entre instâncias (limite em memória local multiplica pelo número de pods, *Inferido*).
4. Política de falha do armazenamento **por rota**: aberta em formulário de contato, fechada em login e pagamento (heurística de blog classe C).
5. Cabeçalhos `RateLimit-Policy` (quota `q`, unidades `qu`, janela `w`, chave de partição `pk`) e `RateLimit` (restante `r`, tempo `t`, `pk`) só se o projeto aceitar um draft em andamento; sinalize no OpenAPI como experimental.
6. Limite por cliente, não global; limites mais rígidos em login, reset e envio.
7. Teste de recuperação depois de `Retry-After`; só em ambiente isolado.

## 5. Webhooks recebidos

Do brain (`automacao-api.md`) e V-24 (AP4: webhook sem assinatura é CRITICAL):

- **Assinatura HMAC sobre o corpo cru** (os bytes recebidos), com **timestamp dentro do conteúdo assinado**, tolerância (por exemplo 5 min) e **comparação em tempo constante**. Reserializar o JSON antes de verificar muda os bytes.
- **Dedupe persistente** por ID de evento (restrição única): o emissor reenvia em timeout ou 5xx, e duplicata é o caso normal.
- **Responda 2xx rápido** e processe de forma assíncrona; aceitar não é concluir.
- **Ordem invertida:** `pedido.cancelado` pode chegar antes de `pedido.pago`; use versão ou timestamp do evento, ou consulte o estado atual no emissor; estados terminais não regridem.
- **Rotação de segredo:** o antigo vale só na janela combinada.
- Cabeçalhos e conteúdo assinado variam por provedor: reproduza o do provedor real e leia a doc dele.

```python
import hashlib, hmac, time

def assinatura_valida(segredo: bytes, corpo_cru: bytes, ts: str, recebida: str, tolerancia_s: int = 300) -> bool:
    if abs(time.time() - int(ts)) > tolerancia_s:
        return False                       # replay ou relógio fora
    esperada = hmac.new(segredo, f"{ts}.".encode() + corpo_cru, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperada, recebida)   # tempo constante
```

Adaptação do exemplo do brain (MIT). O formato `timestamp.corpo` é ilustrativo: use o do provedor.

## 6. Filas, jobs, DLQ e outbox

Fonte: brain (`automacao-api.md`), *Inferido* (fontes primárias são lacuna). Kafka, RabbitMQ e SQS entregam **pelo menos uma vez**:

- **Consumidor idempotente:** mesma mensagem duas vezes produz um efeito (dedupe por ID de mensagem/evento com restrição única).
- **Mensagem envenenada** vai para a **DLQ** após N tentativas, com o motivo registrado, e as seguintes **continuam** sendo processadas.
- **Produtor com outbox:** grave o evento na mesma transação do dado; um processo separado publica e marca como enviado. Sem isso, falha entre gravar e publicar perde ou duplica evento.
- **Ordem:** Kafka garante ordem só dentro da partição (mesma chave); SQS Standard não garante; SQS FIFO ordena por `MessageGroupId` e deduplica em janela de 5 minutos; RabbitMQ perde ordem com vários consumidores ou reenfileiramento.
- **Schema registry:** verifique compatibilidade no CI antes do deploy (Confluent: modo padrão `BACKWARD`, Verificado em 2026-10-10).
- **Consistência eventual:** testes esperam por condição com prazo (`esperar_ate`), nunca `sleep` fixo; provar que algo **não** aconteceu exige um marco posterior processado pelo mesmo consumidor.

```sql
-- Proposta (PostgreSQL): outbox na mesma transação do dado
CREATE TABLE outbox (
  id           bigserial PRIMARY KEY,
  aggregate_id text        NOT NULL,
  event_type   text        NOT NULL,
  payload      jsonb       NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now(),
  published_at timestamptz
);
```

## 7. Concorrência otimista

`ETag`/`If-Match` para atualização de recurso (412 desatualizado, 428 ausente, 409 conflito de regra). No banco: atualização condicional com número de versão ou `UPDATE ... WHERE saldo >= :valor` e verificação de linhas afetadas, dentro da transação; lock apropriado quando a contenção é alta. Teste com **duas** requisições coordenadas, nunca duas chamadas sequenciais (brain, `dados-e-migracoes`). Nível de isolamento não se deduz pelo nome "transação": depende da engine.

## 8. Cache de aplicação

*Inferido*: sem fonte V; HTTP caching tem fonte (V-36, `contrato-erros-paginacao.md`). Regras estáveis:

- **Cache-aside** com TTL explícito; invalide na escrita ou aceite staleness documentada.
- **Chave com escopo** de usuário/tenant e versão do contrato (cache sem tenant vaza dado: é BOLA por cache).
- Proteja contra **stampede** (lock por chave, TTL com jitter, request coalescing).
- Nunca cache de resposta com dado sensível em camada compartilhada sem chave de escopo; `Cache-Control: no-store` para respostas sensíveis.
- Teste: a mesma consulta por dois tenants nunca devolve o dado do outro; escrita invalida a leitura seguinte.

## 9. Testes que provam

Primeira chamada; replay (mesma resposta, sem novo efeito); **duas requisições concorrentes** (um efeito); corpo divergente; perda de resposta após aceitação; validação inválida sem consumir a chave; assinatura adulterada; evento repetido; evento fora de ordem; recuperação após `Retry-After`; fornecedor lento. Não gere carga contra ambiente compartilhado ou externo sem escopo autorizado. Exemplos executáveis: skill `api-test-suite`.

Validado em 2026-10-10. O draft de rate limit expira em 24/11/2026; reconfira o estado antes de recomendar os cabeçalhos.
