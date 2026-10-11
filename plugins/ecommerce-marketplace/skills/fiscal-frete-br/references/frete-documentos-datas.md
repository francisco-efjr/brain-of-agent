# Frete, documentos brasileiros, datas, feriados e fusos

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. Fontes lidas por validador em 2026-10-10: docs do Melhor Envio (webhooks `updatedAt` 2026-06-02; cotação 2025-11-10; fluxo completo) e portal Correios (V-35). Tabelas de documentos, datas, feriados e fusos: brain-of-agent (Francisco Edson, MIT), `brains/qa/references/dominios.md` e `brains/qa/scripts/documentos_br.py`, incorporadas com adaptação e marcadas **Inferido (brain, conferido em 2026, não reverificado nesta rodada)**, exceto onde dito. Frete de teste sempre sintético.

## 1. Fluxo de frete: cotação -> compra -> pagamento -> etiqueta -> rastreio (V-35)

| Etapa | Regra | Rótulo |
|---|---|---|
| Autenticação | Conforme a doc do Melhor Envio; segredos só em variáveis de ambiente | Verificado (existência do passo) |
| Cotação | Exige CEP de origem, CEP de destino e produtos ou volumes (cm, kg, reais). **Cada requisição cota um frete** (um vendedor e um par de CEPs): marketplace cota por vendedor | Verificado |
| Resposta | Usar os campos `custom_*` (por exemplo `custom_price`, `custom_delivery_time`), que refletem a personalização do lojista | Verificado |
| Gravar a cotação | Salvar a cotação escolhida **no checkout**, com o pedido, para o envio respeitar o preço mostrado | Verificado |
| Compra do frete e pagamento da etiqueta | Só depois do **pagamento do pedido confirmado** (webhook verificado, skill `webhook-pagamento`) | Regra do plugin; endpoints de cálculo/compra e fluxo de saldo: **Não verificados** |
| Geração e impressão | Etiqueta gerada pelo mesmo aplicativo que receberá o webhook | Verificado |
| Status | Webhook **e** busca ativa | Verificado |
| Rastreio | Pode demorar até 1 dia útil após a postagem; em marketplace, sob o contrato do vendedor | Verificado |

### Webhook do Melhor Envio

- Cabeçalho `X-ME-Signature`: HMAC-SHA256 do corpo com o secret do aplicativo (codificação do digest: **Não verificado**; leia a doc).
- Timeout de **6 s**; nova tentativa após **15 minutos**, até **5 tentativas**, depois a notificação é **descartada**. Só dispara para etiquetas geradas pelo mesmo aplicativo.
- Idempotência sugerida: `data.id` + `event`. Responder em menos de 6 s e processar depois.
- Sandbox: o status muda sozinho a cada 15 minutos (útil para teste, não confunda com comportamento de produção).

### Eventos tratados (tabela de eventos; preencha a ação do seu projeto)

| Evento | Significado provável | Ação sugerida | Idempotência |
|---|---|---|---|
| `order.created` | Etiqueta criada no carrinho do app | Registrar | `data.id` + evento |
| `order.pending` | Aguardando pagamento da etiqueta | Aguardar | idem |
| `order.released` | Etiqueta liberada | Registrar | idem |
| `order.generated` | Etiqueta gerada | Disponibilizar impressão | idem |
| `order.received` | Recebida pela transportadora (leitura **Inferido**) | Registrar | idem |
| `order.posted` | Postada | Atualizar pedido para "enviado"; rastreio pode demorar até 1 dia útil | idem |
| `order.delivered` | Entregue | Pedido "entregue"; abre prazo de arrependimento (contagem: decisão com o jurídico) | idem |
| `order.cancelled` | Cancelada | Reavaliar envio; estoque/reembolso por humano | idem |
| `order.undelivered` | Não entregue | Contato com cliente; decisão de reenvio | idem |
| `order.paused` / `order.suspended` | Pausada/suspensa | Alertar operação | idem |

A doc lista os eventos; a semântica e a ordem esperada acima são interpretação (**Inferido**). Como a ordem não é garantida e a notificação é descartada após 5 tentativas, o estado final vem da busca ativa.

Estados da etiqueta (diagrama de texto; Inferido):

```text
criada -> pendente -> liberada -> gerada -> (recebida) -> postada -> entregue
                          \-> cancelada          \-> não entregue
(qualquer) -> pausada | suspensa
```

### Correios (V-35, B6)

- Portal Correios Web Services (CWS): APIs públicas (login Meu Correios) e privadas (exigem contrato). A API Rastro restringe a consulta aos objetos do contrato do remetente.
- **Desde 15/09/2025** a pré-postagem valida a `chaveNFe` e exige a Declaração de Conteúdo (descrição de ao menos cinco caracteres), com adicional 095 para itens restritos ao transporte aéreo.
- Chaves de subdelegação do CWS valem até **180 dias**, sem renovação: alerte antes do vencimento. Regras de segurança desde 27/04/2026 (redefinição de senha e 2FA nos canais PJ).
- **Não verificado:** a documentação técnica de preço, prazo e rastreio está atrás do login do CWS; Frenet não lido; fluxo de saldo e cobrança do Melhor Envio não verificado.

### Testes de frete

| Caso | Esperado |
|---|---|
| Carrinho de dois vendedores | Duas cotações, cada uma gravada no subpedido |
| Preço mostrado no checkout × preço da etiqueta | Igual, pela cotação gravada |
| Etiqueta comprada antes do pagamento | Impossível (teste falha o código antigo) |
| Mesmo webhook duas vezes | Um efeito |
| Webhook perdido | Busca ativa corrige o estado |
| CEP inexistente, rural, com zero à esquerda | Mensagem clara; CEP salvo como texto de 8 dígitos |

## 2. Documentos e formatos brasileiros (brain-of-agent, MIT)

Gere e valide massa com o script do plugin, só se o usuário pedir. Rode antes `--self-test` (executado em 2026-10-10 a partir do snapshot: "self-test: OK").

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/scripts/documentos_br.py" --self-test
python "${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/scripts/documentos_br.py" gerar cpf -n 5 --mascara
python "${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/scripts/documentos_br.py" gerar cnpj-alfa -n 3
python "${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/scripts/documentos_br.py" validar 529.982.247-25 12.ABC.345/01DE-35
```

Um documento gerado com DV correto **pode pertencer a uma pessoa ou empresa real**: use só em ambiente de teste e nunca para consultar bases externas (Receita, bureaus) nem cadastrar em sistemas de terceiros. O script precisa do `scripts/documentos_br.py` do playbook (escrito por outra parte do plugin); se ausente, descreva o algoritmo e peça ao usuário o script.

| Documento | Regra | Casos que pegam defeito |
|---|---|---|
| CPF | 11 dígitos; 2 DVs por módulo 11 | com e sem máscara; `529.982.247-25` válido; DV trocado; `111.111.111-11` passa no cálculo e é inválido; zero à esquerda guardado como número vira 10 dígitos |
| CNPJ numérico | 14 dígitos: raiz (8) + ordem (4, matriz `0001`) + 2 DVs | `11.222.333/0001-81` válido; filial com mesma raiz; zeros à esquerda |
| CNPJ alfanumérico | Desde julho de 2026, inscrições novas podem ter as 12 primeiras posições com letras e números; DVs numéricos; CNPJs existentes não mudam | `12.ABC.345/01DE-35` válido (exemplo oficial); minúsculas (normaliza ou recusa, a regra decide); coluna `BIGINT`, máscara `99.999.999/9999-99` e teclado numérico quebram |
| CEP | 8 dígitos, `00000-000` | zero à esquerda; inexistente; CEP único de cidade pequena; sem logradouro |
| Telefone | DDD + 9 dígitos no celular (começa com 9) ou 8 no fixo | `(11) 98765-4321`, `+55 11 98765-4321`; DDD inexistente; sem o nono dígito |
| Chave de acesso NF-e | 44 posições: UF, AAMM, CNPJ/CPF do emitente, modelo, série, número, tipo de emissão, código numérico, DV (módulo 11) | DV trocado; emitente alfanumérico: a chave passa a ter letras e o DV usa ASCII - 48 |
| Inscrição estadual | Formato e DV por UF; valor `ISENTO` | validar pela regra da UF informada |

Cálculo do DV do CNPJ (numérico e alfanumérico): valor de cada caractere = código ASCII - 48 (`0`-`9` -> 0-9, `A` -> 17, `Z` -> 42); pesos 5,4,3,2,9,8,7,6,5,4,3,2 para o 1º DV e 6,5,4,3,2,9,8,7,6,5,4,3,2 para o 2º; resto da divisão por 11 menor que 2 dá DV 0, senão 11 - resto. Para CNPJ só com dígitos o resultado coincide com o cálculo antigo, por isso validadores antigos parecem funcionar até o primeiro CNPJ com letra. Consistente com a NT 2026.004 (CNPJ alfanumérico), cuja existência e data foram verificadas (V-34).

Fonte: brain-of-agent, `brains/qa/references/dominios.md`, seção "Documentos e formatos brasileiros" (MIT, Francisco Edson), adaptada. RG e placa ficam fora do escopo de e-commerce.

## 3. Datas, moeda e números

- Data `DD/MM/AAAA` na tela, ISO `AAAA-MM-DD` na API. Use dia <= 12 nos testes (`01/02/2026`) para pegar troca dia/mês.
- Moeda `R$ 1.234,56`: vírgula decimal, ponto de milhar. `Intl.NumberFormat('pt-BR', ...)` põe espaço não separável (U+00A0) entre `R$` e o número; asserção com espaço comum falha. Entrada `1.000` em campo pt-BR é mil, não um.

## 4. Feriados

Nacionais: 1/1, Sexta-feira da Paixão (móvel), 21/4, 1/5, 7/9, 12/10, 2/11, 15/11, 20/11 (Dia Nacional de Zumbi e da Consciência Negra, nacional pela Lei 14.759/2023, desde 2024) e 25/12. Carnaval e Corpus Christi são ponto facultativo federal e feriado só onde lei estadual ou municipal declara. Municipais e estaduais variam (São Paulo, 25/1; Rio de Janeiro, 20/1). Teste prazos em dias úteis com feriado no meio, vencimento em feriado local, e mantenha o calendário como **dado configurável**, não lista fixa no código. Aplique em prazo de entrega, prazo de arrependimento (contagem decidida com o jurídico) e vencimento de boleto (pago no próximo dia útil sem multa).

## 5. Fusos horários

Quatro fusos, sem horário de verão desde 2019 (decisão reavaliada a cada ano, mantida até 2026 segundo o brain): UTC-2 (`America/Noronha`), UTC-3 (`America/Sao_Paulo`), UTC-4 (`America/Manaus`) e UTC-5 (`America/Rio_Branco`).

- Use o identificador IANA, nunca deslocamento fixo: datas antigas têm horário de verão no histórico. Em `America/Sao_Paulo`, 04/11/2018 às 00:30 não existiu.
- Teste usuário em Manaus (UTC-4) com servidor em São Paulo: "hoje" e prazos que vencem à meia-noite mudam entre 23h e 0h.
- Mantenha a base de fusos (tzdata) atualizada no servidor, no banco e no container; quem fixou `-03:00` erra se o horário de verão voltar.
- Fato gerador fiscal e corte de promoção usam o fuso definido pela regra (em geral `America/Sao_Paulo`), não UTC.

Fonte das seções 3 a 5: brain-of-agent, `dominios.md` (MIT), seção "Documentos e formatos brasileiros" (Datas, Feriados, Fusos); Inferido, não reverificado.
