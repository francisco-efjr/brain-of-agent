# OWASP Top 10:2025 aplicado ao checkout

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Fonte: OWASP Top 10:2025 (https://top10.owasp.org/2025, lista A01-A10 Verificada em V-13) e checklist de implementação de V-13 (redação própria). Buscas abaixo são pontos de partida: adapte ao framework e leia o contexto de cada resultado antes de afirmar um achado.

## Tabela A01-A10 para checkout

| Cat. | Pergunta de checkout | Como detectar (busca) | Correção mínima |
|---|---|---|---|
| A01 Broken Access Control | Pedido, endereço, fatura e reembolso de outro cliente são acessíveis trocando o ID? Algum campo privilegiado (`role`, `status`, `desconto`, `total`) entra por mass assignment? | `findById(req.params`, `where: { id: req.params.id }` sem `userId`; `Object.assign(pedido, req.body)`; `Model.create(req.body)` | Filtrar por dono em toda consulta; `404` quando não for dele; allowlist de campos (`pick`/schema) na entrada |
| A02 Security Misconfiguration | Debug ligado, CORS aberto com credenciais, sem CSP/HSTS/`nosniff` | `DEBUG=true`, `cors({ origin: true, credentials: true })`, ausência de `helmet`/cabeçalhos no proxy | Cabeçalhos no proxy ou middleware; debug desligado em produção; CORS com lista explícita |
| A03 Software Supply Chain | Scripts de terceiros na página de pagamento (analytics, chat) e dependências sem lockfile | `<script src=` em templates de checkout; ausência de `package-lock.json`/`pnpm-lock.yaml`; `npm audit` fora do CI | Lockfile versionado, auditoria no CI, inventário e controle de mudança dos scripts da página de pagamento (PCI DSS 6.4.3 e 11.6.1: Inferido, brain; versão do padrão não reverificada) |
| A04 Cryptographic Failures | Dado de pagamento em trânsito e repouso; senha com hash fraco | `md5(`, `sha1(` para senha; campo `numero_cartao`, `cvv`, `pan` em modelo/log | Nunca armazenar número de cartão (token do provedor); TLS 1.2+; Argon2id ou bcrypt com custo >= 12 |
| A05 Injection | Cupom, busca e filtros entram em SQL/NoSQL/template como texto? | Template string em consulta: `` `...${cupom}...` ``, `.query("... " + `; `$where`, `$regex` vindo do cliente | Consulta parametrizada (`$1`, `?`), ORM com binding, validação de formato do código do cupom |
| A06 Insecure Design | Preço, frete e desconto vêm do cliente? O limite de uso do cupom é checado fora de transação? | `req.body.(total\|preco\|price\|frete\|desconto\|amount)`; fluxo "ler uso, comparar, gravar" em três comandos | Cálculo no servidor em centavos inteiros; checagem e incremento atômicos (`UPDATE ... WHERE usos < limite`) |
| A07 Authentication Failures | Login/checkout de convidado sem limite de tentativas, sessão não regenerada, token longo | Ausência de limitador na rota de login e de "validar cupom"; `req.session` sem `regenerate` no login | Hash lento, sessão regenerada no login, limite de tentativas, token de acesso <= 15 min |
| A08 Software or Data Integrity | Webhook aceito sem assinatura? Corpo reescrito antes de verificar? | Rota `/webhook` sem `constructEvent`/HMAC; `app.use(express.json())` global antes da rota | Assinatura sobre corpo bruto, dedupe por `event_id` (skill `webhook-pagamento`), integridade de pacotes |
| A09 Logging and Alerting Failures | Log com PII ou cartão? Eventos de segurança sem alerta (cupom em rajada, 403 em pedidos)? | `console.log(req.body)`, `logger.info(pedido)` com endereço/CPF | Log estruturado com IDs em campos (não na mensagem), sem PII; alerta de rajada |
| A10 Mishandling of Exceptional Conditions | Se a checagem do pagamento lança exceção ou o PSP dá timeout, o pedido é liberado? | `catch { /* ignora */ }` em torno de verificação de pagamento; `if (erro) pedido.status = 'pago'` | Falhar fechado: erro de verificação mantém o pedido pendente ou "retido para revisão"; tratar `retryable` por tipo |

Nota de fonte: o arquivo `security-and-owasp` do awesome-copilot (MIT) foi lido em V-13, mas seus snippets de SSRF, limitador de taxa e upload têm defeitos conhecidos (lista incompleta de IPs privados, `x-forwarded-for` falsificável, MIME confiado ao cliente). Nada foi copiado; use as correções desta tabela, não os snippets.

## Par vulnerável e corrigido (Express + PostgreSQL, redação própria)

Vulnerável: três falhas em ~10 linhas.

```js
app.post('/checkout', async (req, res) => {
  const { total, cupom, itens } = req.body;                       // A06: total vem do cliente
  const { rows } = await db.query(
    `SELECT * FROM cupons WHERE codigo = '${cupom}'`);            // A05: injeção
  const pedido = await Pedido.create({ ...req.body, total });     // A01: mass assignment
  await psp.cobrar({ valor: total, pedido: pedido.id });
  res.json(pedido);
});
app.get('/pedidos/:id', async (req, res) =>
  res.json(await Pedido.findById(req.params.id)));                // A01: IDOR
```

Corrigido (o nome das funções é ilustrativo; adapte ao projeto):

```js
app.post('/checkout', requireAuth, async (req, res) => {
  const entrada = checkoutSchema.parse(req.body);   // allowlist: itens[{sku,qtd}], cupom, enderecoId, chaveIdempotencia
  const cotacao = await carrinhos.precificar({      // servidor decide preço, frete e desconto, em centavos inteiros
    usuarioId: req.user.id, itens: entrada.itens, cupom: entrada.cupom, enderecoId: entrada.enderecoId,
  });
  const pedido = await pedidos.criarPendente({ usuarioId: req.user.id, cotacao, chave: entrada.chaveIdempotencia });
  const intencao = await psp.criarIntencao({ valor: cotacao.totalCentavos, moeda: 'BRL' },
                                          { idempotencyKey: entrada.chaveIdempotencia });
  res.status(202).json({ pedidoId: pedido.id, clientSecret: intencao.clientSecret }); // pedido "pago" só pelo webhook verificado
});

app.get('/pedidos/:id', requireAuth, async (req, res) => {
  const pedido = await Pedido.findOne({ where: { id: req.params.id, usuarioId: req.user.id } });
  if (!pedido) return res.sendStatus(404);          // 404 não confirma que o ID existe
  res.json(pedido);
});
```

Consulta de cupom parametrizada com uso atômico (PostgreSQL):

```sql
-- 1 linha afetada = uso reservado; 0 = cupom inexistente, expirado ou esgotado. Sem corrida entre dois checkouts.
UPDATE cupons SET usos = usos + 1
 WHERE codigo = $1 AND ativo AND (expira_em IS NULL OR expira_em > now()) AND usos < limite_usos
RETURNING id, tipo, valor;
```

Se o checkout falhar depois, devolva o uso numa compensação idempotente (`usos = usos - 1` ligado ao `pedido_id` único), ou registre o uso por pedido em tabela própria com `UNIQUE (cupom_id, pedido_id)`.

Testes que provam a correção (cada um falha no código vulnerável):

| Teste | Esperado |
|---|---|
| POST com `total: 1` e itens de R$ 100,00 | cobrança criada com o total do servidor, ou `422`; nunca R$ 0,01 |
| Usuário A lê `/pedidos/<id de B>` | `404` |
| `cupom = "X' OR '1'='1"` | `404`/`422` de cupom inválido, sem erro de SQL |
| 20 requisições simultâneas ao cupom com `limite_usos = 5` | exatamente 5 sucessos; contar linhas, não respostas |
| `role: "admin"` e `status: "pago"` no corpo | campos ignorados ou `422` |

## Abusos de e-commerce (achados "sugestão")

| Abuso | Sinal | Mitigação (Inferido: prática de engenharia, não item V-) |
|---|---|---|
| Força bruta de cupom | Muitas tentativas de códigos distintos na mesma conta/IP/sessão | Limite por conta, IP e sessão; atraso progressivo; códigos longos e aleatórios; alerta |
| Card testing | Rajada de pagamentos pequenos recusados, cartões diferentes, mesmo dispositivo ou IP | Limite de tentativas por carrinho e sessão; desafio (3DS/CAPTCHA do provedor); alerta de taxa de recusa; regras do PSP (o plugin não assume qual PSP) |
| Enumeração de pedido | IDs sequenciais, `404` e `403` distintos | IDs não adivinháveis (UUID) mais checagem de dono; resposta uniforme |
| Reenvio duplicado | Duplo clique, retry após timeout | Chave de idempotência por intenção de compra (V-10) |

A fonte oficial de security review (`claude-code-security-review`, MIT) exclui DoS e limite de taxa do filtro de falsos positivos; por isso estes itens nunca são "crítico" por padrão e entram como sugestão com correção mínima (V-44).

## Busca de número de cartão em logs de teste

Teste barato e eficaz (brain-of-agent, MIT, `brains/qa/references/dominios.md`, seção PCI): procurar 13 a 19 dígitos que passam no Luhn em logs, URLs, analytics e prints de erro. Rode só sobre logs de ambiente de teste e nunca imprima o número inteiro.

```python
#!/usr/bin/env python3
"""Procura candidatos a PAN em logs de TESTE: 13-19 dígitos que passam no Luhn."""
import re, sys
PAN = re.compile(r"(?<![\d.])(?:\d[ -]?){13,19}(?!\d)")

def luhn(digitos: str) -> bool:
    soma, dobrar = 0, False
    for ch in reversed(digitos):
        n = int(ch)
        if dobrar:
            n *= 2
            if n > 9: n -= 9
        soma += n; dobrar = not dobrar
    return soma % 10 == 0

total = 0
for caminho in sys.argv[1:]:
    with open(caminho, encoding="utf-8", errors="replace") as f:
        for n, linha in enumerate(f, 1):
            for m in PAN.finditer(linha):
                d = re.sub(r"\D", "", m.group())
                if 13 <= len(d) <= 19 and luhn(d):
                    print(f"{caminho}:{n}: possível PAN {d[:6]}{'*' * (len(d) - 10)}{d[-4:]}"); total += 1
sys.exit(1 if total else 0)
```

Verificado em 2026-10-10 com o cartão de teste público `4242 4242 4242 4242` (detectado) e um identificador de 16 dígitos que falha no Luhn (ignorado). Falsos positivos existem (IDs que passam no Luhn por acaso): revise manualmente. Regras que o brain lista como casos de teste: PAN nunca em log, URL, analytics ou print; exibição mascarada (no máximo BIN e quatro últimos); CVV nunca armazenado depois da autorização; ambiente de teste sem cartão real. Versão vigente do PCI DSS e SAQ aplicável: Não verificado nesta rodada (V-43); decisão humana com o adquirente.

## Rótulos usados aqui

Verificado: lista A01-A10 e checklist por categoria (V-13), defeitos dos snippets do awesome-copilot (V-13), exclusões do filtro da Action (V-44). Inferido: buscas por padrão de código, tabela de abusos, `UPDATE ... WHERE usos < limite` como padrão de atomicidade, PCI 6.4.3/11.6.1 (brain). Não verificável: versão e escopo PCI aplicável à sua operação.
