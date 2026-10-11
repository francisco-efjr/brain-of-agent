# PSP brasileiro: webhook do Asaas, testes de sandbox, subcontas e Pix Automático

Condicional: vale só se o produto cobra por PSP brasileiro (Inferido). Redação própria. Base: V-50, V-51, V-52, V-53, V-62, V-66. Conferido em 2026-10-10. Nada foi executado. Não é orientação jurídica nem fiscal. Ledger, Pix, boleto e conciliação bancária ficam no segmento `fintech-payments`.

## 1. O que a documentação do Asaas diz sobre entrega de webhook (V-50, Verificado)

Fonte: https://docs.asaas.com/docs/webhooks-faq.

| Ponto | Regra |
| --- | --- |
| Sucesso | somente HTTP 200; outros 2xx contam como falha |
| Tempo | espera de até 10 segundos |
| Redirects | 301, 302, 307 e 308 não são seguidos |
| Fila interrompida | após 15 falhas consecutivas; eventos novos são guardados sem envio até a reativação |
| Retenção de pendentes | até 14 dias; depois são removidos de forma permanente |
| Autenticação | `authToken` enviado no header `asaas-access-token`, sem Bearer nem Basic; a API key não deve servir de token |
| Assinatura do corpo | a FAQ não menciona HMAC |
| IPs | é possível restringir a IPs oficiais; o sandbox pode ter IPs extras: validar os dois ambientes |
| Repetição | um evento pode chegar mais de uma vez, com o mesmo `id` (usar como chave de idempotência) |
| Ordem | modo sequencial preserva a ordem; o não sequencial não garante |

Consequência (Inferido): sem assinatura do corpo, o token estático não impede replay de uma requisição capturada. Mitigação: `id` com UNIQUE, allowlist de IP, HTTPS direto, segredo guardado no cofre e rotacionável.

## 2. Handler (esqueleto)

```ts
import crypto from 'node:crypto';

function safeEqual(a: string, b: string): boolean {              // comparação em tempo constante (Inferido como boa prática)
  const ba = Buffer.from(a), bb = Buffer.from(b);
  return ba.length === bb.length && crypto.timingSafeEqual(ba, bb);
}

app.post('/webhooks/asaas', express.json(), async (req, res) => {
  const token = req.header('asaas-access-token') ?? '';
  if (!safeEqual(token, process.env.ASAAS_WEBHOOK_TOKEN!)) return res.sendStatus(401);   // segredo do cofre; nunca a API key

  const ev = req.body;                                            // campos exatos: confira a documentação vigente e a versão da API
  try {
    await db.query(
      `INSERT INTO psp_events (provider, event_id, type, received_at) VALUES ('asaas', $1, $2, now())
       ON CONFLICT (provider, event_id) DO NOTHING`,
      [ev.id, ev.event],
    );
  } catch { return res.sendStatus(500); }                         // falha transitória: o provedor reenvia

  return res.sendStatus(200);                                     // exatamente 200; processar fora da requisição
});
```

O worker é o mesmo padrão do Stripe (outbox, retry, DLQ lógica), mapeando eventos para o estado de acesso do tenant. Alerta obrigatório: fila interrompida (o painel do provedor ou erros 5xx seguidos nos seus logs) antes dos 14 dias; o limite do alerta é Suposição.

## 3. Mapeamento evento para estado de acesso e teste de sandbox obrigatório (V-51)

Fonte: https://docs.asaas.com/docs/eventos-para-assinaturas. Verificado: sete eventos de assinatura (`SUBSCRIPTION_CREATED`, `_UPDATED`, `_INACTIVATED`, `_DELETED`, `_SPLIT_DISABLED`, `_SPLIT_DIVERGENCE_BLOCK`, `_SPLIT_DIVERGENCE_BLOCK_FINISHED`); `INACTIVATED` vale para assinatura "inativada" e `DELETED` para "removida"; as cobranças geradas chegam como `PAYMENT_*`, e `PAYMENT_CREATED` traz o campo `subscription`; a página não usa o termo cancelamento nem cita `PAYMENT_DELETED`. A FAQ de webhooks não cobre eventos de assinatura. Logo, qual evento chega num cancelamento é Não verificável sem sandbox.

Regra (V-51): o estado de acesso do tenant deriva de `SUBSCRIPTION_INACTIVATED`, `SUBSCRIPTION_DELETED` e dos `PAYMENT_*` associados pelo campo `subscription`. Preencha esta tabela no sandbox antes de adotar:

| Cenário | Ação no sandbox | Eventos observados (ordem e campos) | Estado de acesso decidido |
| --- | --- | --- | --- |
| Criar assinatura | criar via API | | |
| Primeira cobrança paga | pagar pelo meio de teste | | |
| Cobrança atrasada | deixar vencer | | |
| Alterar valor ou plano | atualizar a assinatura | | |
| Inativar assinatura | inativar | | |
| Remover assinatura | remover | | |
| Evento repetido | reenviar o mesmo evento | mesmo `id` deve ser ignorado | sem efeito |
| Fila interrompida | forçar 15 falhas (endpoint devolvendo 500) | | alerta disparado |

O resultado observado é Verificado só quando você coloca a saída real do sandbox; antes disso, a tabela é "Não verificado".

## 4. Subcontas (V-53, Inferido nas regras)

Fonte: https://docs.asaas.com/docs/subcontas. Verificado: criação de subconta por API permitida para conta-pai pessoa jurídica; BaaS exige modelo acordado e habilitado antes; no modelo não-BaaS o titular usa o Asaas com onboarding próprio; subcontas não-BaaS encerradas em até 48 horas e que nunca fizeram login não geram a taxa de criação (quando aplicável); novos clientes que criam subcontas por API ficam sujeitos ao período de avaliação regulatório (limites em outra FAQ, não lida). Endpoint, campos e herança de webhooks: Não verificáveis.

Regra de modelagem: separe dois fluxos de dinheiro. (a) O SaaS cobra o tenant (assinatura do SaaS, Customer ou equivalente). (b) O tenant cobra o cliente final (marketplace ou repasse), onde a subconta é candidata. Não misture no mesmo Customer nem na mesma tabela de estado de acesso. Se o produto precisa do fluxo (b), trate como projeto à parte com `fintech-payments`.

## 5. Pix Automático (V-62, Inferido nas regras)

Fonte: cópia comercial da Resolução BCB nº 402/2024 em lex.com.br (classe B; não é o site do BCB). Verificado na cópia: o art. 11-Q define o Pix Automático (o prestador do pagador inicia o Pix na conta do pagador a partir de instruções periódicas do prestador do recebedor, com autorização prévia específica dada uma vez); o pagador pode cancelar a autorização a qualquer momento ou alterá-la quando permitido; o prestador do pagador também cancela se o recebedor pedir; a Resolução 402 revoga a 360/2023; início em 16/06/2025. Os horários de imprensa não constam no texto da 402: não use. As jornadas de cancelamento e alteração estão nos manuais do BCB citados pela resolução, que não foram lidos.

Modelo de dados mínimo (Inferido):

| Campo | Uso |
| --- | --- |
| `authorization_id` | identificador da autorização no PSP |
| `state` | ativa, cancelada pelo pagador, cancelada pelo recebedor |
| `max_amount` | valor máximo autorizado |
| `starts_at`, `ends_at`, `periodicity` | vigência e periodicidade |
| `last_charge_status` | resultado da última cobrança |

Reconcilie com o banco (retorno do PSP) antes de marcar a cobrança como paga; cancelamento pelo pagador muda o estado de acesso conforme a política do spec. Datas e regras do regulador são parâmetros com fonte e data de verificação, nunca constantes no código (V-60).

## 6. Iugu: perguntas de pré-integração (V-52, sem regra)

Fonte: https://dev.iugu.com/ (índice lido; páginas internas não). Antes de integrar, responda lendo as páginas: (1) os gatilhos são assinados e como verificar (o changelog de 28/07/2026 cita assinatura RSA com múltiplos tokens; se vale para gatilhos é Não verificável); (2) a fatura aceita chave de idempotência (há página dedicada); (3) quem reenvia gatilho perdido e em que intervalo; (4) assinatura suspensa dispara evento.

## 7. Auditoria do handler (prompt PR-33)

Use o prompt PR-33 da skill `prompts` (derivado de V-66): lê o handler em modo somente leitura, confere token comparado com segredo do cofre, `id` UNIQUE, somente 200 dentro do prazo, processamento fora da requisição, ordem não assumida, mapeamento de eventos para acesso e alerta de fila interrompida; para cada item devolve arquivo e linha, Verificado ou Não verificado, e os testes de duplicado e fora de ordem.
