# Domínios: riscos característicos e casos que não podem faltar

Leia quando o sistema sob teste pertence a um domínio com regras próprias —
pagamentos, e-commerce, saúde, SaaS multi-tenant, dados, eventos, setor
público — ou quando a entrada envolve documentos e formatos brasileiros. Cada
seção lista o que quebra nesse domínio e os casos mínimos, com dados. Para
priorizar e montar o plano, combine com `references/estrategia.md`.

Regras e números regulatórios mudam. Os daqui foram conferidos em 2026; antes
de usar um limite como resultado esperado, confirme na norma vigente (Banco
Central, Receita, Febraban, ANVISA) e cite a fonte no caso de teste.

## Sumário

- [Pagamentos e fintech](#pagamentos-e-fintech)
- [PIX](#pix)
- [Boleto](#boleto)
- [Cartão](#cartão)
- [E-commerce](#e-commerce)
- [Saúde](#saúde)
- [SaaS multi-tenant B2B](#saas-multi-tenant-b2b)
- [Dados, ETL e BI](#dados-etl-e-bi)
- [Microsserviços e eventos](#microsserviços-e-eventos)
- [Setor público](#setor-público)
- [IoT, embarcados e jogos](#iot-embarcados-e-jogos)
- [Documentos e formatos brasileiros](#documentos-e-formatos-brasileiros)

## Pagamentos e fintech

O defeito caro aqui é silencioso: cobrança duplicada, centavo perdido, saldo
que não fecha. Ele não aparece na tela; aparece na conciliação semanas depois.
Por isso o oráculo é sempre um cálculo independente ou o extrato da outra
ponta, nunca o valor que o próprio sistema mostra.

| Risco | Caso que não pode faltar | Esperado |
| --- | --- | --- |
| Cobrança dupla | duplo clique em "Pagar"; reenviar a mesma requisição com a mesma `Idempotency-Key`; timeout do gateway seguido de retry | uma cobrança só; a segunda chamada devolve o resultado da primeira, não cria outra |
| Chave de idempotência mal escopada | mesma chave com corpo diferente (R$ 100,00 e depois R$ 150,00) | recusa explícita (conflito), nunca reaproveita silenciosamente |
| Arredondamento | R$ 100,00 em 3 parcelas; R$ 10,00 de desconto rateado entre 3 itens | parcelas 33,34 + 33,33 + 33,33 (ou a regra escrita); soma exatamente igual ao total |
| Ponto flutuante | `0.1 + 0.2` em cálculo de valor | valores em centavos inteiros ou decimal exato; nunca `float` |
| Regra de arredondamento | juros de 1% a.m. sobre R$ 333,33 por 17 dias | resultado conferido por planilha independente com a regra escrita (meio para cima × meio para o par) |
| Conciliação | pedido pago no sistema × liquidação no extrato do adquirente/PSP | cada transação casa por ID; divergência gera alerta, não ajuste manual silencioso |
| Estorno | estorno total, parcial, dois parciais somando mais que o original | parcial reduz o saldo estornável; soma acima do original é recusada |
| Chargeback | contestação depois do repasse ao lojista | débito registrado, pedido marcado, disputa com prazo visível |
| Limites | limite diário R$ 5.000,00: transferir 4.999,99 + 0,01; depois mais 0,01 | aceita até 5.000,00 exatos; recusa 5.000,01 com mensagem que diz o limite |
| Virada do limite | transação às 23:59:59 e às 00:00:00 no fuso do cliente | o contador zera no fuso definido pela regra (em geral America/Sao_Paulo), não em UTC |
| Antifraude | 10 tentativas em 1 minuto com cartões diferentes no mesmo dispositivo | bloqueio ou desafio; cliente legítimo tem caminho de recuperação |
| Concorrência de saldo | dois débitos simultâneos de R$ 80,00 em conta com R$ 100,00 | um aprova, outro recusa; saldo nunca fica negativo |

Armadilhas: testar o retry sem verificar o efeito no banco (conte as linhas,
não a resposta); usar `float` no próprio teste e "acertar" o erro do sistema;
esquecer que o webhook do gateway também chega duplicado e fora de ordem
(`pagamento.aprovado` antes de `pagamento.criado`).

### PIX

| Tema | O que testar | Dados e esperado |
| --- | --- | --- |
| Tipos de chave | CPF, CNPJ, e-mail, telefone, aleatória | CPF 11 dígitos e CNPJ 14 posições sem máscara; e-mail até 77 caracteres; telefone no formato `+5511987654321`; aleatória é UUID de 36 caracteres. Teste chave com máscara colada, e-mail com maiúsculas, telefone sem `+55` |
| Quantidade de chaves | cadastrar além do limite | até 5 chaves por conta de pessoa física e 20 por conta de pessoa jurídica; a próxima é recusada |
| CNPJ alfanumérico | chave Pix de empresa aberta depois de julho de 2026 | aceita `12ABC34501DE35` como chave; parser que só aceita dígitos é defeito |
| QR estático | mesmo QR pago duas vezes; QR sem valor | estático aceita vários pagamentos; sem valor, o pagador digita; `txid` de até 25 caracteres (ou `***`) |
| QR dinâmico | pagar depois da expiração; pagar duas vezes | payload buscado por URL; expirado é recusado; `txid` entre 26 e 35 caracteres alfanuméricos |
| Cobrança com vencimento | pagar antes, no dia, depois do vencimento; vencimento em feriado municipal | o PSP do pagador envia data prevista de pagamento (DPP) e código do município; juros, multa e desconto calculados para aquela data |
| Devolução | devolução total, parcial, várias parciais, após 90 dias | iniciada pelo recebedor em até 90 dias; soma das devoluções ≤ valor original |
| MED | pagador contesta por golpe | contestação em até 80 dias; bloqueio cautelar e análise; devolução só se houver saldo. O MED 2.0 rastreia contas intermediárias — confirme prazos no regulamento vigente |
| Limite noturno | Pix de R$ 1.000,01 às 20h01 | padrão de R$ 1.000,00 entre 20h e 6h, somando a janela; cliente pode mudar o início para 22h; aumento de limite só vale após 24 a 48 h, redução é imediata |
| Dispositivo novo | primeiro Pix em celular não cadastrado | limite de R$ 200,00 por transação e R$ 1.000,00 por dia até cadastrar o aparelho |
| Pix Automático | autorização, agendamento, cancelamento, saldo insuficiente | exige autorização prévia no app do pagador; agendamento enviado com antecedência mínima e máxima do regulamento (2 a 10 dias antes, na versão consultada); retentativa em falha; pagador vê e cancela a autorização |
| Timeout e status | resposta não chega em 30 s | consultar o status pelo EndToEndId antes de qualquer reenvio; reenviar às cegas gera Pix em dobro |

O **EndToEndId** tem 32 caracteres: `E` + 8 dígitos do ISPB de quem gerou +
`AAAAMMDDHHmm` em UTC + 11 alfanuméricos. Teste o parse dele (hora em UTC,
não em Brasília) e use-o como chave de conciliação. O `txid` é do recebedor e
serve à conciliação do lado de quem cobra; não confunda os dois.

Casos hostis: QR adulterado (CRC inválido no BR Code), QR de cobrança de
outro recebedor colado em tela de checkout, valor alterado entre a leitura e a
confirmação, app fechado no meio do pagamento e reaberto.

### Boleto

| Tema | O que testar | Esperado |
| --- | --- | --- |
| Formatos | código de barras (44 posições) × linha digitável (47 dígitos em cobrança; 48 em arrecadação/convênio, que começa com 8) | aceita os dois; converte um no outro sem perder dígito |
| Dígitos verificadores | alterar um dígito de cada campo | linha digitável usa módulo 10 por campo; o DV geral do código de barras, módulo 11; erro aponta o campo |
| Fator de vencimento | boletos vencendo em 21/02/2025 e 22/02/2025 | o fator conta dias desde 07/10/1997; chegou a 9999 em 21/02/2025 e reiniciou em 1000 em 22/02/2025 |
| Ambiguidade do fator | fator 1000 | pode ser 03/07/2000 ou 22/02/2025; o sistema deve resolver para o ciclo mais próximo da data atual, nunca para 2000 |
| Valor | R$ 0,01; R$ 99.999.999,99; boleto sem valor | campo de valor tem 10 posições; sem valor (zeros) pede digitação |
| Vencimento em dia não útil | vence no sábado ou em feriado da praça | pago no próximo dia útil sem multa |

Armadilha: guardar a linha digitável como número (perde zeros à esquerda) ou
calcular a data do fator com a base antiga sem o reinício — o boleto aparece
como vencido há 25 anos.

### Cartão

- **Luhn**: o número precisa passar no dígito verificador antes de ir ao
  gateway. Teste um dígito trocado (`4242 4242 4242 4241`) — deve ser
  recusado no cliente, sem chamada ao gateway.
- **Cartões de teste do gateway**: cada gateway publica os seus e eles não
  valem nos outros. Na Stripe: `4242 4242 4242 4242` aprova,
  `4000 0000 0000 0002` recusa genérico, `4000 0000 0000 9995` saldo
  insuficiente, `4000 0027 6000 3184` sempre exige 3DS. Teste cada motivo de
  recusa com sua mensagem — "erro desconhecido" para saldo insuficiente é
  defeito de UX.
- **3DS**: fluxo sem fricção, desafio aprovado, desafio recusado, desafio
  abandonado (fechar a janela), timeout do desafio. O pedido não pode ficar
  "pago" sem autenticação concluída, nem preso para sempre em "aguardando".
- **Parcelamento**: valor mínimo de parcela, parcelado pela loja (sem juros)
  × pelo emissor (com juros), soma das parcelas = total, troca do número de
  parcelas depois de aplicar cupom, estorno de compra parcelada.
- **Tokenização e cartão salvo**: cartão expirado, removido, de outro usuário
  (IDOR com o token).

**PCI DSS** (versão 4.0.1 é a vigente; os requisitos "datados para o futuro"
viraram obrigatórios em 31/03/2025). O que vira caso de teste: número
completo do cartão nunca em log, URL, analytics ou print de erro; exibição
mascarada (no máximo BIN e quatro últimos); CVV nunca armazenado depois da
autorização; ambiente de teste sem cartão real; inventário e controle de
alteração dos scripts carregados na página de pagamento (requisitos 6.4.3 e
11.6.1). Busque o número de cartão nos logs com uma expressão regular de PAN
mais Luhn — é o teste mais barato e o que mais acha problema.

## E-commerce

| Área | Casos | Esperado |
| --- | --- | --- |
| Carrinho | anônimo com 2 itens faz login em conta que já tinha 1 item | mescla (3 itens) ou regra escrita; nunca perde os itens anônimos |
| Carrinho | item fica sem estoque ou muda de preço enquanto está no carrinho | aviso claro antes do pagamento; preço cobrado é o confirmado na revisão |
| Estoque | último item: dois clientes finalizam ao mesmo tempo | um compra, outro recebe "esgotado"; estoque nunca negativo |
| Estoque | Pix gerado e não pago até expirar | reserva liberada no fim do prazo |
| Cupons | R$ 200,00 com 10% e R$ 20,00 cumulativos | 10% antes: 200 → 180 → 160; fixo antes: 180 → 162. A regra precisa dizer a ordem; teste as duas |
| Cupons | cupom expirado, de primeira compra reutilizado, aplicado em item excluído da promoção | recusa com motivo |
| Frete grátis | limite R$ 199,00: subtotal 198,99 e 199,00; cupom que derruba o subtotal para baixo do limite | regra diz se o limite é antes ou depois do desconto |
| Frete por CEP | CEP inexistente, CEP de área rural, CEP com zero à esquerda (01310-100) | mensagem clara; CEP salvo como texto de 8 dígitos |
| Checkout | abandonar no pagamento e voltar; pagamento recusado | carrinho preservado; nova tentativa não duplica pedido |
| Estados do pedido | criado → aguardando pagamento → pago → em separação → enviado → entregue; cancelado; devolvido | cada transição válida e tentativas inválidas (cancelar pedido já entregue pela API) |
| Arrependimento | pedido entregue há 7 e há 8 dias | CDC art. 49: 7 dias a partir do recebimento em compra fora da loja física; reembolso integral, frete incluso, e estorno no cartão |
| Nota fiscal | pagamento confirmado, cancelamento, devolução | NF-e/NFC-e emitida no evento certo; cancelamento dentro do prazo da SEFAZ ou nota de devolução depois |
| Busca | "cafe" × "café", "tenis" × "tênis", "celuar", "geladeira" × "refrigerador", SKU, zero resultados | acento e caixa ignorados; tolerância a erro de digitação; página de zero resultados com sugestão |
| Pico | Black Friday, lançamento | ver `references/performance.md`; teste a fila de checkout e o comportamento com o gateway lento |

Armadilha: testar promoção só com um item. Defeitos de rateio aparecem com 3
itens de preços diferentes e um deles fora da promoção.

## Saúde

| Risco | Casos | Esperado |
| --- | --- | --- |
| Dado sensível (LGPD art. 11) | perfil sem vínculo assistencial abre prontuário; exportação; log de aplicação | acesso negado e registrado; nenhum diagnóstico em log, URL ou analytics |
| Trilha de auditoria | leitura, alteração e impressão de prontuário | registra quem, o quê, quando, de onde — inclusive **leitura**; trilha não editável |
| Acesso de emergência | "quebrar o vidro" para paciente fora da equipe | permitido com justificativa obrigatória, alerta e revisão posterior |
| Prontuário | corrigir uma evolução já assinada | correção por adendo; o original permanece visível. Guarda mínima de 20 anos após o último registro (Lei 13.787/2018) |
| Cálculo de dose | regra de exemplo: 10 mg/kg, máximo 500 mg por dose | 20 kg → 200 mg; 50 kg → 500 mg; 60 kg → 500 mg (não 600); 0 kg e 350 kg recusados; peso digitado em gramas (20000) detectado |
| Unidades | mg × mcg (fator 1000), mL × gotas, vírgula decimal | conversão explícita; `0,5 mg` nunca vira `5 mg`; sem zero à direita ("5,0" lido como "50") |
| Alertas | interação medicamentosa, alergia registrada | alerta bloqueante para o grave, sem inundar de alertas triviais (fadiga de alerta faz o médico ignorar o importante) |
| Interoperabilidade | HL7 v2 (`ADT^A01` admissão, `ORU^R01` resultado) e FHIR (`Patient`, `Observation`, `MedicationRequest`) | mensagem malformada vai para fila de erro com motivo; nada é descartado em silêncio; códigos de terminologia validados |
| Disponibilidade | sistema fora do ar no plantão | procedimento de contingência testado; dados lançados offline sincronizam sem duplicar |

**Software como dispositivo médico (SaMD)**: se o software tem finalidade
clínica (diagnóstico, apoio à decisão terapêutica, cálculo de dose), pode ser
regulado pela ANVISA (RDC 657/2022), com classe de risco que define as
exigências. Para o QA, isso significa rastreabilidade requisito → risco →
teste → evidência, validação documentada a cada versão e controle de mudança.
Normas de referência usuais: IEC 62304 (ciclo de vida do software) e ISO 14971
(gestão de risco). O enquadramento é decisão regulatória: sinalize, não decida.

## SaaS multi-tenant B2B

O defeito que encerra contrato é vazamento entre clientes. Todo teste de
isolamento precisa de **dois tenants** com dados de nomes parecidos.

| Risco | Caso | Esperado |
| --- | --- | --- |
| Isolamento por ID | usuário do tenant A chama `GET /api/faturas/{id}` com ID do tenant B | 404 (não 403, que confirma a existência) |
| Isolamento indireto | busca, autocomplete, exportação CSV, relatório, anexos por URL, notificações, websockets, cache | nada do tenant B aparece; URL de arquivo é assinada e expira |
| Jobs em lote | job noturno processa os dois tenants | cada saída usa só os dados do próprio tenant (contexto do tenant perdido em worker é clássico) |
| Papéis | matriz papel × ação (admin, gestor, membro, leitor, cobrança) | cada célula testada pela API, não só pela tela escondendo o botão |
| Escalada | membro altera o próprio papel no corpo da requisição | ignorado ou recusado |
| Plano e limites | plano com 5 assentos: convidar o 5º e o 6º | 5º aceito; 6º bloqueado com oferta de upgrade |
| Downgrade | sair do plano com 10 usuários para o de 5 | regra explícita (bloqueia ou desativa); nunca apaga dados |
| Cobrança | upgrade no meio do ciclo, falha de cartão, fim do trial, webhook duplicado do provedor | proporcionalidade correta; tentativas e aviso; acesso conforme a regra; webhook idempotente |
| Convites | convite expirado, reutilizado, e-mail com caixa diferente, convidado já é de outro tenant | expirado e reutilizado recusados; mesma pessoa em dois tenants com troca de contexto clara |
| SSO | SAML/OIDC: domínio não verificado, provisionamento no primeiro login, usuário removido no IdP | não entra; recebe o papel padrão; perde acesso |
| SCIM | desativar usuário via SCIM | sessões e tokens revogados na hora, não no próximo login |
| Exportação | exportar todos os dados do tenant | completa, legível por máquina, só do tenant (portabilidade, LGPD art. 18, V) |
| Migrações | migração de schema em 1.000 tenants, um falha no meio | falha isolada, reexecutável; nenhum tenant em estado misto |
| Auditoria | ações de admin | log por tenant, imutável, visível ao admin do cliente |

## Dados, ETL e BI

Dimensões de qualidade de dados, cada uma com uma verificação automatizável:

| Dimensão | Pergunta | Verificação exemplo |
| --- | --- | --- |
| Completude | falta dado? | `cpf` nulo em ≤ 0% dos clientes ativos |
| Unicidade | há duplicata? | uma linha por `pedido_id` |
| Validade | está no formato e domínio? | `status` ∈ {criado, pago, cancelado}; CPF com DV válido |
| Consistência | bate entre tabelas e sistemas? | todo `item.pedido_id` existe em `pedido` |
| Exatidão | corresponde à realidade? | amostra conferida com a fonte (extrato, nota fiscal) |
| Atualidade | chegou a tempo? | maior `atualizado_em` com menos de 2 h às 8h |

**Reconciliação origem × destino** é o teste central de ETL. Compare por
partição (dia, filial), não só o total — totais iguais escondem erros que se
compensam:

```sql
-- rode na origem e no destino; o resultado precisa ser idêntico
SELECT data_venda,
       COUNT(*)                    AS linhas,
       SUM(valor_centavos)         AS soma,
       COUNT(DISTINCT pedido_id)   AS pedidos,
       MIN(pedido_id), MAX(pedido_id)
FROM vendas
WHERE data_venda BETWEEN DATE '2026-09-01' AND DATE '2026-09-30'
GROUP BY data_venda
ORDER BY data_venda;
```

Para colunas transformadas, compare um hash por linha (ex.: `md5` da
concatenação das colunas normalizadas) e liste as chaves divergentes.

Testes genéricos do dbt — `unique`, `not_null`, `relationships`,
`accepted_values` — cobrem unicidade, completude, consistência e validade:

```yaml
models:
  - name: fato_pedido
    columns:
      - name: pedido_id
        tests: [unique, not_null]
      - name: cliente_id
        tests:
          - relationships: {to: ref('dim_cliente'), field: cliente_id}
      - name: status
        tests:
          - accepted_values: {values: ['criado', 'pago', 'cancelado']}
```

Great Expectations e Soda fazem o mesmo fora do dbt (expectativas/checks
declarativos com relatório). Escolha um e rode no pipeline, bloqueando a
carga quando a verificação crítica falha.

Casos que não podem faltar:

- **SCD tipo 2**: cliente muda de cidade duas vezes no mesmo dia; esperado:
  um só registro vigente por chave, intervalos de vigência sem sobreposição
  nem buraco, fatos antigos apontando para a versão da época.
- **Reprocessamento idempotente**: rodar a mesma partição duas vezes; esperado:
  mesmas contagens e somas (sem duplicar). Carga por `INSERT` sem `MERGE` ou
  sem apagar a partição antes é a causa clássica.
- **Dado atrasado**: evento de 30/09 chega em 02/10; esperado: entra na
  partição de 30/09 se estiver dentro da janela de reprocessamento definida;
  fora dela, vai para tratamento explícito.
- **Fuso**: venda às 22h de 31/12 em Brasília é 01h de 01/01 em UTC. Guarde
  em UTC e corte o dia no fuso do negócio; teste a virada de mês e de ano.
- **Dashboards**: cada KPI conferido com uma consulta SQL independente; soma
  do detalhamento igual ao total; filtro vazio; período sem dados (mostra 0 ou
  "sem dados", não erro); divisão por zero em percentuais; permissão por linha
  (gerente vê só a própria região).

## Microsserviços e eventos

| Tema | Caso | Esperado |
| --- | --- | --- |
| Contrato | produtor renomeia campo ou muda tipo | teste de contrato quebra no pipeline do produtor (ver `references/automacao-api.md`) |
| Consistência eventual | criar pedido e consultar o saldo projetado | asserção com polling até um prazo (ex.: até 10 s, a cada 200 ms), nunca `sleep` fixo |
| Entrega pelo menos uma vez | publicar a mesma mensagem duas vezes | efeito aplicado uma vez (chave de idempotência, tabela de mensagens processadas) |
| Ordenação | `PedidoCancelado` chega antes de `PedidoCriado` | ordem garantida só por partição/chave; consumidor trata fora de ordem (versão, estado) |
| Mensagem venenosa | payload inválido | vai para a DLQ após N tentativas com o motivo; a fila não trava; existe reprocessamento da DLQ |
| Retry | dependência responde 503 três vezes | backoff exponencial com jitter; só operações idempotentes repetem; sem tempestade de retries |
| Saga | passo 3 (frete) falha depois de reservar estoque e cobrar | compensações executadas na ordem inversa; compensação que falha fica visível e é reexecutável |
| Circuit breaker | dependência fora por 1 minuto | circuito abre, resposta degradada rápida, meia-abertura testa a volta |
| Timeouts em cascata | serviço C lento | timeout de quem chama maior que o de quem é chamado somado aos retries; senão A desiste enquanto C ainda executa e o retry duplica |
| Outbox | banco grava, broker cai antes de publicar | evento publicado depois (outbox); nunca grava sem publicar nem publica sem gravar |

**Chaos engineering com cautela**: comece em ambiente de teste, com hipótese
escrita ("se o Redis cair, o checkout continua sem recomendação"), raio de
impacto pequeno e condição de aborto. Toxiproxy injeta latência, corte e
reset de conexão entre o serviço e a dependência — ótimo em testes de
integração. Chaos Mesh faz o mesmo em Kubernetes (matar pod, partição de
rede). Em produção, só com autorização explícita e plano de reversão.

## Setor público

- **Acessibilidade é obrigação legal**: Lei Brasileira de Inclusão (Lei
  13.146/2015, art. 63) e, no governo federal, o eMAG (versão 3.1, obrigatório
  para sites federais). Na prática, teste contra WCAG 2.2 AA — o eMAG é
  baseado nas WCAG — e veja `references/acessibilidade.md`. Falha de
  acessibilidade aqui é defeito de conformidade, não melhoria.
- **Login gov.br**: contas têm níveis bronze, prata e ouro. Teste cada
  serviço com conta abaixo do nível exigido (esperado: orientação para elevar
  o nível, sem erro genérico), sessão expirada no meio do formulário, retorno
  do login para a página certa e logout que encerra também a sessão local.
- **LAI (Lei 12.527/2011)**: pedido de informação com prazo de resposta de 20
  dias prorrogáveis por mais 10; teste contagem de prazo, protocolo, recurso
  e publicação de dados em formato aberto (CSV, não só PDF).
- **LGPD vale para o poder público**; dados de cidadão em teste só anonimizados.
- **Volume e picos sazonais**: prazos de declaração, inscrições e resultados
  concentram acesso no último dia — teste de carga com esse perfil.

## IoT, embarcados e jogos

**IoT/embarcados**: atualização OTA interrompida no meio (energia, rede) com
retorno à versão anterior; perda de conectividade com buffer local e reenvio
sem duplicar nem desordenar; relógio sem sincronismo (dispositivo em 1970);
leitura de sensor fora da faixa física; bateria fraca; credencial padrão de
fábrica; teste em bancada com hardware real (HIL) para o que simulador não
reproduz.

**Jogos**: taxa de quadros no hardware mínimo declarado; salvar e carregar
(inclusive arquivo de save corrompido e de versão anterior); multiplayer com
latência, perda de pacote e dessincronização; compras dentro do jogo (aplique
a seção de pagamentos: duplicidade, estorno, restauração de compra);
progressão que trava; localização de texto que estoura a interface.

## Documentos e formatos brasileiros

Gere e valide massa com `scripts/documentos_br.py`
(`gerar cpf -n 5 --mascara`, `gerar cnpj-alfa`, `validar <valor>`). Documento
gerado com DV correto pode pertencer a alguém real: use só em ambiente de
teste e nunca para consultar bases externas.

| Documento | Regra | Casos que pegam defeito |
| --- | --- | --- |
| CPF | 11 dígitos; 2 DVs por módulo 11 | com e sem máscara; `529.982.247-25` válido; DV trocado; `111.111.111-11` (passa no cálculo, é inválido); zero à esquerda `012.345.678-90` guardado como número vira 10 dígitos |
| CNPJ numérico | 14 dígitos: raiz (8) + ordem (4, matriz `0001`) + 2 DVs | `11.222.333/0001-81` válido; filial com mesma raiz; zeros à esquerda (`00.000.000/0001-91`) |
| CNPJ alfanumérico | desde julho de 2026, inscrições novas podem ter as 12 primeiras posições com letras (A–Z) e números; DVs continuam numéricos; CNPJs existentes não mudam | `12.ABC.345/01DE-35` válido (exemplo oficial); `00.000.000/E08G-12` (primeiro emitido, filial com raiz numérica); minúsculas (normaliza ou recusa — a regra decide); coluna `BIGINT`, máscara `99.999.999/9999-99` e teclado numérico no celular quebram |
| CEP | 8 dígitos, `00000-000` | zero à esquerda; CEP inexistente; CEP único de cidade pequena; CEP sem logradouro (usuário digita a rua) |
| Telefone | DDD (2 dígitos) + 9 dígitos no celular (começa com 9) ou 8 no fixo | `(11) 98765-4321`, `+55 11 98765-4321`, fixo `(11) 3456-7890`; DDD inexistente; número sem o nono dígito |
| RG | número e DV variam por UF; muitos não têm DV | não valide DV genericamente; aceite letras e `X`; a Carteira de Identidade Nacional usa o CPF como número |
| Placa | antiga `ABC-1234`; Mercosul `ABC1D23` | conversão troca só o 2º número por letra (0=A … 9=J): `ABC-1234` → `ABC1C34`; busca encontra o veículo pelas duas formas |
| Chave de acesso NF-e | 44 posições: UF, AAMM, CNPJ/CPF do emitente, modelo, série, número, tipo de emissão, código numérico, DV (módulo 11) | DV trocado; com emitente de CNPJ alfanumérico a chave passa a ter letras e o DV usa o mesmo valor ASCII − 48 |
| Inscrição estadual | formato e DV diferentes por UF; valor `ISENTO` | validar pela regra da UF informada; IE de SP em cadastro de MG recusada |

Cálculo do DV do CNPJ (numérico e alfanumérico): valor de cada caractere =
código ASCII − 48 (`0`–`9` → 0–9, `A` → 17, `Z` → 42); pesos
5,4,3,2,9,8,7,6,5,4,3,2 para o 1º DV e 6,5,4,3,2,9,8,7,6,5,4,3,2 para o 2º;
resto da divisão por 11 menor que 2 dá DV 0, senão 11 − resto. Para CNPJ só
com dígitos o resultado é o mesmo do cálculo antigo — por isso validadores
antigos parecem funcionar até o primeiro CNPJ com letra.

### Datas, moeda e números

- Data `DD/MM/AAAA` na tela, ISO `AAAA-MM-DD` na API. Use dia ≤ 12 nos testes
  (`01/02/2026`) para pegar troca dia/mês. `scripts/valores_limite.py data`
  gera limites, 29/02 e datas inexistentes.
- Moeda `R$ 1.234,56`: vírgula decimal, ponto de milhar. `Intl.NumberFormat`
  em `pt-BR` põe espaço não separável (U+00A0) entre `R$` e o número —
  asserção com espaço comum falha. Entrada `1.000` em campo pt-BR é mil, não
  um.

### Feriados

Nacionais: 1/1, Sexta-feira da Paixão (móvel), 21/4, 1/5, 7/9, 12/10, 2/11,
15/11, 20/11 (Dia Nacional de Zumbi e da Consciência Negra, nacional pela Lei
14.759/2023, a partir de 2024) e 25/12. Carnaval e Corpus Christi são ponto
facultativo federal e feriado só onde lei estadual ou municipal declara.
Municipais e estaduais variam (São Paulo, 25/1; Rio de Janeiro, 20/1). Teste
prazos em dias úteis com feriado no meio, vencimento em feriado local e
calendário de feriados como dado configurável, não como lista fixa no código.

### Fusos horários

Quatro fusos, sem horário de verão desde 2019 (decisão reavaliada a cada ano,
mantida até 2026): UTC−2 (Fernando de Noronha, `America/Noronha`), UTC−3
(Brasília, `America/Sao_Paulo`), UTC−4 (AM, MT, MS, RO, RR — ex.:
`America/Manaus`) e UTC−5 (Acre e sudoeste do AM, `America/Rio_Branco`).

- Use o identificador IANA, nunca deslocamento fixo: datas antigas ainda
  têm horário de verão no histórico. Em `America/Sao_Paulo`, 04/11/2018 às
  00:30 não existiu (o relógio pulou de 00:00 para 01:00) — seletor de data
  que grava meia-noite local exibe o dia anterior.
- Teste usuário em Manaus (UTC−4) com servidor em São Paulo: "hoje" e prazos
  que vencem à meia-noite mudam entre 23h e 0h.
- Mantenha a base de fusos (tzdata) atualizada no servidor, no banco e no
  container; se o horário de verão voltar, quem fixou `-03:00` erra.

### Reforma tributária do consumo (CBS/IBS)

A Emenda Constitucional 132/2023 e a Lei Complementar 214/2025 substituem
PIS/Cofins pela CBS (federal) e ICMS/ISS pelo IBS (estados e municípios), com
transição:

| Período | O que acontece |
| --- | --- |
| 2026 | ano de teste: CBS de 0,9% e IBS de 0,1% destacados no documento fiscal; recolhimento dispensado para quem cumpre as obrigações acessórias, valor compensável com PIS/Cofins |
| 2027 | CBS em alíquota cheia; PIS e Cofins extintos; começa o Imposto Seletivo |
| 2029 a 2032 | ICMS e ISS reduzidos gradualmente enquanto o IBS cresce |
| 2033 | fim da transição; ICMS e ISS extintos |

O que muda nos testes de sistemas fiscais (ERP, emissor de nota, PDV,
marketplace):

- **Alíquota e regra por data do fato gerador**, como configuração com
  vigência — não constante no código. Caso: operação em 31/12/2026 × em
  01/01/2027 com o mesmo produto.
- **Convivência de tributos**: na transição, a mesma nota carrega tributos
  antigos e novos; teste que um não é calculado sobre a base errada do outro.
- **Novos campos nos documentos fiscais** (grupos de IBS/CBS definidos em
  notas técnicas da NF-e): validação de schema, rejeições da SEFAZ e
  impressão do DANFE.
- **Arredondamento por item × pelo total**: a soma dos tributos dos itens
  precisa bater com o total da nota pela regra oficial.
- Não invente alíquota definitiva nem data de etapas futuras (como o split
  payment): use como oráculo a norma publicada e a nota técnica vigente, e
  deixe o teste parametrizado para quando os números mudarem.
