# Fiscal, tributário e frete no Brasil

Base da skill `fiscal-frete-br`. **Requer revisão fiscal/tributária/jurídica** em tudo que for norma. O plugin entrega checklists, mapeamento de dados e fichas versionadas; **não emite documento fiscal real, não calcula DIFAL nem IBS/CBS, não escolhe CFOP/NCM e não recolhe tributo**. Emissão apenas em homologação.

Modelo-alvo: Claude 4.x/5.x · pesquisa validada em 2026-10-10 (Planalto e Portal Nacional da NF-e lidos nessa data) · compilado em 2026-10-11. Notas técnicas, atos conjuntos e prazos mudam por informe: toda afirmação fiscal aqui tem **data de leitura** e deve ser relida antes de uso.

## Sumário

- [1. Regras de trabalho](#1-regras-de-trabalho)
- [2. NF-e e NFC-e: portal e notas técnicas](#2-nf-e-e-nfc-e-portal-e-notas-técnicas)
- [3. Reforma tributária do consumo (IBS/CBS)](#3-reforma-tributária-do-consumo-ibscbs)
- [4. DIFAL, split payment, contingência, CFOP/NCM](#4-difal-split-payment-contingência-cfopncm)
- [5. Frete: cotação, etiqueta, rastreio](#5-frete-cotação-etiqueta-rastreio)
- [6. Documentos e formatos brasileiros](#6-documentos-e-formatos-brasileiros)
- [7. Datas, moeda, feriados, fusos](#7-datas-moeda-feriados-fusos)
- [8. Não verificável (declarar)](#8-não-verificável-declarar) · [9. Testes](#9-testes)

## 1. Regras de trabalho

1. Toda afirmação fiscal recebe **fonte e data de leitura**; sem isso, rotule **Não verificável**.
2. Alíquotas, notas técnicas, prazos e tabelas ficam em **tabela versionada** (data, UF, fonte) no projeto, nunca fixos no código nem de memória (regra transversal da pesquisa).
3. Só **homologação**. O agente não envia XML assinado a produção, não cancela nem inutiliza nota.
4. A decisão fiscal é de quem tem responsabilidade fiscal (contador). O agente indica a **tabela e a pergunta**, não o código.
5. Lacunas permanecem lacunas: ver seção 8.

## 2. NF-e e NFC-e: portal e notas técnicas

Fonte: Portal Nacional da NF-e, `https://www.nfe.fazenda.gov.br/portal/principal.aspx` e as listas de Notas Técnicas e Informes (V-34, lidas em 2026-10-10 com `curl`, user-agent comum e jar de cookie; o portal tem menus Legislação e Documentos: Manuais, Esquemas XML, Notas Técnicas, Informes).

**Notas técnicas vigentes na leitura (amostra, Verificado em 2026-10-10):**

| NT | Versão | Assunto | Publicação | Observação |
| --- | --- | --- | --- | --- |
| 2025.002 | v1.52 | Adequação dos leiautes da NF-e e NFC-e à Reforma Tributária do Consumo (campos e regras de validação) | 01/10/2026 | Implantação **postergada** (informe de 05/10/2026): **26/10/2026 em homologação e 16/11/2026 em produção** |
| 2026.007 | v1.10 | Regras com a Lista Centralizada de Contribuintes e o CCC | 01/10/2026 | Postergada nas mesmas datas |
| 2026.008 | v1.00 | Assunto não detalhado na leitura | 01/10/2026 | Postergada nas mesmas datas |
| 2026.010 | v1.00 | Modelo do DANFE para a Reforma Tributária do Consumo | 01/10/2026 | |
| 2026.006 | v1.00 | Vinculação entre NF-e e transação financeira sujeita a **split payment** | 25/08/2026 | |
| 2026.004 | v1.01 | **CNPJ alfanumérico** | 08/06/2026 | |
| 2021.003 | v1.50 | GTIN | 25/09/2026 | |

Informes técnicos de 03/09/2026 (NCM, vigente a partir de 01/10/2026) e 04/09/2026 (CFOP) existem: o plugin só registra que existem; **não** transcreve códigos (seção 4).

**Como proceder (ficha):** antes de gerar qualquer campo, consulte a lista de NTs e registre em [ficha-nt-fiscal-versionada.md](../assets/templates/ficha-nt-fiscal-versionada.md): número, versão, publicação, **datas de homologação e de produção** (mudam por informe), UF, prazo de contingência (lido no MOC/NT), fonte e data de leitura. Em marketplace, trate o intermediador e o vínculo com transação financeira (NT 2026.006) como requisitos a conferir no manual.

**Ressalvas (V-34):** o Manual de Orientação do Contribuinte (versão), o PDF das NTs, o Ato Conjunto RFB/CGIBS nº 8/2026 e a documentação de emissores (Focus NFe, Tecnospeed) **não foram lidos**; os **campos IBS/CBS concretos (tags)** seguem **Não verificados**. O README do `nfephp-org/sped-nfe` (último commit 2026-10-02; `LICENSE.md` LGPL v3, README oferece "LGPLv3 ou MIT") cita a NT 2025.002-RTC v1.20, **desatualizada** frente ao portal: só destilação, schema `PL_010v1.20b` pode não ser o vigente.

## 3. Reforma tributária do consumo (IBS/CBS)

Fonte: Lei Complementar 214/2025, texto compilado no Planalto (`https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm`, lido por trechos em 2026-10-10; com redações da LC 227/2026; o cabeçalho cita "Vide Decreto nº 12.955, de 2026"). Foram lidos **apenas** os arts. 11, 22, 31–37 (V-57), 343, 344, 346, 347 e 348 de um texto de ~960 mil caracteres.

| Período | O que diz | Verificado por LC 214? |
| --- | --- | --- |
| 2026 | IBS 0,1% (estadual, art. 343) e CBS 0,9% (art. 346); valores recolhidos compensados com tributos vigentes (art. 348) | **Sim** (arts. 343, 346, 348) |
| 2027–2028 | IBS 0,05% estadual + 0,05% municipal (art. 344); CBS = alíquota fixada pelo art. 14 **reduzida em 0,1 ponto percentual** (art. 347) | **Sim** (arts. 344, 347) |
| 2027 (brain) | "CBS em alíquota cheia; PIS e Cofins extintos; começa o Imposto Seletivo" | **Não**: divergente do art. 347 lido (a CBS de 2027–2028 é a do art. 14 menos 0,1 pp); Imposto Seletivo e extinção de PIS/Cofins ficam **Inferido (brain)** |
| 2029–2032 (brain) | ICMS e ISS reduzidos gradualmente enquanto o IBS cresce | **Não** lido: **Inferido (brain)** |
| 2033 (brain) | Fim da transição; ICMS e ISS extintos | **Não** lido: **Inferido (brain)** |
| Alíquotas finais, regimes específicos, crédito presumido | — | **Não verificável** |

Regras do plugin: (1) todo cálculo recebe a **data do fato gerador**; (2) em 2026 IBS/CBS é de teste e compensável (valores acima); (3) de 2027 em diante exige tabela de alíquotas versionada com vigência; (4) arredondamento por item × pelo total: a soma dos tributos dos itens precisa bater com o total da nota pela regra oficial (**Inferido**, brain); (5) na transição a mesma nota carrega tributos antigos e novos: teste que um não é calculado sobre a base errada do outro; (6) novos grupos de campos nas NTs: validação de schema, rejeições da SEFAZ e impressão do DANFE; (7) não inventar alíquota definitiva nem data de etapas futuras.

**Local da operação com bem material:** o da entrega (art. 11, I).

**Papel fiscal da plataforma (art. 22, V-33):** plataformas digitais, ainda que no exterior, respondem pelo pagamento de IBS e CBS das operações feitas por seu intermédio, solidariamente com o adquirente e em substituição ao fornecedor residente no exterior; para fornecedor no País, solidariamente em hipóteses que incluem a plataforma não fornecer as informações exigidas ou o fornecedor **não emitir documento fiscal eletrônico** no valor da operação (redação da LC 227/2026); a plataforma pode **optar**, com anuência do fornecedor, por ser substituta tributária (emite documentos fiscais eletrônicos, apura e paga). Saída: ADR com o papel escolhido e a lista de dados exigidos do vendedor ([adr-papel-fiscal-plataforma.md](../assets/templates/adr-papel-fiscal-plataforma.md)). **Requer revisão tributária.**

## 4. DIFAL, split payment, contingência, CFOP/NCM

**DIFAL em venda interestadual a consumidor final não contribuinte (V-56; LC 190/2022 e EC 87/2015, Planalto, lidas em 2026-10-10; Requer revisão tributária).** Verificado: a LC 190 altera a LC 87/1996: na operação interestadual a consumidor final, o contribuinte da diferença entre a alíquota interna do destino e a interestadual é o **remetente** quando o destinatário **não é contribuinte** (o destinatário, quando contribuinte); a diferença cabe ao Estado de destino (base pela alíquota interna do destino); o fato gerador inclui a saída a consumidor final não contribuinte de outro Estado; os Estados devem manter portal com legislação, alíquotas interna e interestadual, benefícios, obrigações acessórias e ferramenta de apuração centralizada. A LC 190 entra em vigor na publicação, com efeitos sujeitos à anterioridade (art. 150, III, "c"). EC 87/2015 (art. 99 do ADCT): partilha 20% (2015), 40% (2016), 60% (2017), 80% (2018) ao destino, **100% ao destino a partir de 2019**. **Não verificado (fora da regra):** alíquotas de exemplo de 7% e 12%, Simples Nacional, grupo de partilha da NF-e, NFC-e, ADIs 7066/7070/7078 do STF, convênios do Confaz (fundos de pobreza), substituição tributária estadual.

Checklist que **bloqueia emissão sem conferência:** (1) o destinatário é contribuinte? (2) alíquotas interna e interestadual de tabela versionada, com data e UF; (3) portal do Estado de destino consultado; (4) campos da NF-e conferidos na NT vigente; (5) Simples Nacional e ST pelo contador; (6) valores só em `references/` do projeto com data e fonte.

**Split payment IBS/CBS (V-57; LC 214 arts. 31–35 com LC 227/2026; Requer revisão tributária).** Verificado: PSPs e operadoras de sistemas de pagamento segregam e recolhem IBS e CBS na liquidação financeira (arranjos abertos e fechados, públicos e privados). **Procedimento padrão** (art. 32): o fornecedor inclui no documento fiscal eletrônico dados que vinculam a operação ao pagamento e identificam os débitos; o originador da transação transmite as informações. **Procedimento simplificado** (art. 33, opcional na redação da LC 227/2026): percentual preestabelecido pelo Comitê Gestor do IBS e pela RFB, para operações em que o adquirente não é contribuinte do regime regular; originar pagamento sem identificar IBS/CBS implica a opção pelo simplificado; excedente devolvido ao fornecedor em até 3 dias úteis após a apuração; ato conjunto pode determinar o simplificado enquanto o padrão não funcionar em nível adequado. Art. 34: segregação na liquidação, proporcional em parcelas; antecipação de recebíveis não altera; PSPs segregam e recolhem mas **não são responsáveis tributários**. Art. 35: entrada em funcionamento simultânea nas operações com adquirentes **não contribuintes** do regime regular, para os principais instrumentos de pagamento do varejo; ato conjunto define a implementação gradual.

Postura do plugin: split no plano de revisão trimestral com o rótulo "norma lida: arts. 31 a 35 da LC 214/2025 com LC 227/2026; calendário e campos: **Não verificável**"; **não implementar campos por transação** sem ato conjunto e manual oficiais; marketplace B2C: **acompanhar** (a norma mira o consumidor final), decisão do contador e do PSP. A hipótese "fase inicial B2B / nenhuma ação em B2C" foi **rejeitada**; Decreto 12.955/2026, Ato Técnico Conjunto nº 4/2026 e datas de teste (15/10/2026) aparecem só em buscas: **Não verificáveis**.

**Contingência da NF-e (V-58; Requer revisão fiscal; checklist sem números).** Fontes: SEFAZ-GO (`goias.gov.br/economia/ocorrencia-de-problemas-tecnicos-2/`) e painel do portal (SVC-AN). Modalidades descritas: **FS-DA** (DANFE em formulário de segurança; envio à SEFAZ de origem após o problema), **EPEC** (registro prévio permite DANFE em papel comum; validade depende da transmissão posterior), **SVC** (depende de ativação pela SEFAZ de origem; Goiás usa SVC-RS; DANFE em papel comum, sem nova transmissão à origem). FS-DA e EPEC devem ser transmitidas logo após o fim do problema, **observado o prazo limite da legislação, que a página não numera**. Checklist do emissor: (1) modalidade e UF de origem; (2) prazo limite do MOC/NT vigentes (não escrito aqui); (3) `tpEmis` conferido no MOC; (4) sem emissão em produção sem homologação; (5) resultado "Não verificável" até a leitura. **Rejeitados como fato:** prazo de 168 h, códigos `tpEmis` e evento 110140.

**CFOP e NCM (V-59; regra de projeto, Suposição fundamentada).** Nenhum texto primário de CFOP foi lido (a página do Confaz para o Ajuste SINIEF 3/2024 retornou 404 na URL tentada). Regras: (1) CFOP e NCM **não saem de memória nem do texto da skill**; (2) ficam em tabela versionada com data, UF e link da SEFAZ; (3) quem tem responsabilidade fiscal escolhe o código; (4) o agente indica a tabela e a pergunta. Informes técnicos de 03/09/2026 (NCM) e 04/09/2026 (CFOP) existem no portal.

## 5. Frete: cotação, etiqueta, rastreio

**Melhor Envio (V-35; `docs.melhorenvio.com.br/docs/fluxo-completo-de-integracao.md`, `cotacao-de-fretes.md` de 2025-11-10, `webhooks.md` de 2026-06-02):**

- Fluxo: autenticação → cotação → compra de fretes → pagamento da etiqueta → geração e impressão de etiquetas → status por busca ativa ou webhook.
- Cotação exige **CEP de origem, CEP de destino e produtos ou volumes** (cm, kg, reais). Use os campos `custom_*` (`custom_price`, `custom_delivery_time`), que refletem a personalização do lojista. **Salve a cotação no checkout** para o envio respeitar o preço mostrado. Cada requisição cota **um** frete (um vendedor e um par de CEPs): marketplace cota por vendedor.
- Webhook: `X-ME-Signature` = HMAC-SHA256 do corpo com o secret do aplicativo; responder em < 6 s; reentrega após 15 min, até 5 tentativas, depois descartada; só dispara para etiquetas geradas **pelo mesmo aplicativo**. Eventos: `order.created`, `order.pending`, `order.released`, `order.generated`, `order.received`, `order.posted`, `order.delivered`, `order.cancelled`, `order.undelivered`, `order.paused`, `order.suspended`. Rastreio pode demorar até 1 dia útil após a postagem; no sandbox o status muda sozinho a cada 15 minutos.

**Fluxo do plugin:** (1) cotar por vendedor e gravar a cotação com o pedido; (2) comprar a etiqueta só depois do pagamento confirmado; (3) receber status por webhook **e** reconciliar por busca ativa; (4) verificar `X-ME-Signature` sobre o corpo bruto; (5) responder rápido, processar depois; (6) idempotência por `data.id` + `event`; (7) em marketplace, rastreio sob o contrato do vendedor; (8) segredos em variáveis de ambiente; (9) valores de frete de teste sempre sintéticos. Saída: diagrama de estados da etiqueta e tabela de eventos tratados.

**Correios (V-35; `https://www.correios.com.br/atendimento/developers`):** o portal Correios Web Services (CWS) concentra as APIs, públicas (login Meu Correios) e privadas (exigem contrato); a **API Rastro** restringe a consulta aos objetos do contrato do remetente; **desde 15/09/2025** a pré-postagem valida a `chaveNFe` e exige a Declaração de Conteúdo (descrição de ao menos cinco caracteres), com adicional 095 para itens restritos ao transporte aéreo; chaves de subdelegação do CWS valem até **180 dias**, sem renovação (alerta de validade); regras de segurança desde 27/04/2026 (redefinição de senha e 2FA nos canais PJ). **A documentação técnica de preço, prazo e rastreio fica atrás do login do CWS e não foi lida: Não verificável.** Frenet: não lido.

## 6. Documentos e formatos brasileiros

Tabela do brain-of-agent (`brains/qa/references/dominios.md`, MIT, do próprio autor; **Inferido**, conferido em 2026). O CNPJ alfanumérico é consistente com a NT 2026.004 (V-34, Verificado). Massa de teste: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/scripts/documentos_br.py` (rode `--self-test` antes; só se o usuário pedir; ver T-09 de [ferramentas-e-mcp.md](ferramentas-e-mcp.md)). **Documento gerado com DV correto pode pertencer a pessoa real:** só em teste, nunca para consultar bases externas.

| Documento | Regra | Casos que pegam defeito |
| --- | --- | --- |
| CPF | 11 dígitos; 2 DVs por módulo 11 | Com e sem máscara; `529.982.247-25` válido; DV trocado; `111.111.111-11` passa no cálculo e é inválido; zero à esquerda `012.345.678-90` guardado como número vira 10 dígitos |
| CNPJ numérico | 14 dígitos: raiz (8) + ordem (4, matriz `0001`) + 2 DVs | `11.222.333/0001-81` válido; filial com mesma raiz; `00.000.000/0001-91` |
| CNPJ alfanumérico | Desde julho de 2026 inscrições novas podem ter as 12 primeiras posições com letras A–Z e números; DVs numéricos; CNPJs existentes não mudam | `12.ABC.345/01DE-35` válido (exemplo oficial); `00.000.000/E08G-12`; minúsculas (a regra decide: normaliza ou recusa); coluna `BIGINT`, máscara `99.999.999/9999-99` e teclado numérico quebram |
| CEP | 8 dígitos, `00000-000` | Zero à esquerda; inexistente; único de cidade pequena; sem logradouro |
| Telefone | DDD + 9 dígitos no celular (começa com 9) ou 8 no fixo | `(11) 98765-4321`, `+55 11 98765-4321`, fixo `(11) 3456-7890`; DDD inexistente; sem o nono dígito |
| RG | Número e DV variam por UF | Não valide DV genericamente; aceite letras e `X` |
| Placa | Antiga `ABC-1234`; Mercosul `ABC1D23` | Conversão troca só o 2º número por letra (0=A … 9=J): `ABC-1234` → `ABC1C34` |
| Chave de acesso NF-e | 44 posições: UF, AAMM, CNPJ/CPF do emitente, modelo, série, número, tipo de emissão, código numérico, DV (módulo 11) | DV trocado; com emitente de CNPJ alfanumérico a chave passa a ter letras e o DV usa o mesmo valor ASCII − 48 |
| Inscrição estadual | Formato e DV por UF; valor `ISENTO` | Validar pela regra da UF informada |

**Cálculo do DV do CNPJ (numérico e alfanumérico):** valor de cada caractere = código ASCII − 48 (`0`–`9` → 0–9, `A` → 17, `Z` → 42); pesos 5,4,3,2,9,8,7,6,5,4,3,2 (1º DV) e 6,5,4,3,2,9,8,7,6,5,4,3,2 (2º DV); resto da divisão por 11 menor que 2 dá DV 0, senão 11 − resto. Para CNPJ só com dígitos o resultado é igual ao cálculo antigo: validadores antigos parecem funcionar até o primeiro CNPJ com letra.

## 7. Datas, moeda, feriados, fusos

Brain-of-agent (MIT; **Inferido**):

- Data `DD/MM/AAAA` na tela, ISO `AAAA-MM-DD` na API; use dia ≤ 12 nos testes (`01/02/2026`) para pegar troca dia/mês.
- Moeda `R$ 1.234,56`: `Intl.NumberFormat` em `pt-BR` põe espaço não separável (U+00A0) entre `R$` e o número — asserção com espaço comum falha. Entrada `1.000` em campo pt-BR é mil, não um.
- Feriados nacionais: 1/1, Sexta-feira da Paixão (móvel), 21/4, 1/5, 7/9, 12/10, 2/11, 15/11, 20/11 (nacional pela Lei 14.759/2023, a partir de 2024) e 25/12. Carnaval e Corpus Christi são ponto facultativo federal e feriado só onde lei estadual ou municipal declara. Calendário de feriados como **dado configurável**, não lista fixa no código; teste prazo em dias úteis com feriado no meio e vencimento em feriado local.
- Fusos: UTC−2 (`America/Noronha`), UTC−3 (`America/Sao_Paulo`), UTC−4 (`America/Manaus`) e UTC−5 (`America/Rio_Branco`); sem horário de verão desde 2019 (decisão reavaliada a cada ano). Use o identificador IANA, nunca deslocamento fixo; mantenha tzdata atualizada no servidor, no banco e no container. Em `America/Sao_Paulo`, 04/11/2018 às 00:30 não existiu.

## 8. Não verificável (declarar)

Campos/tags IBS/CBS na NF-e; Manual de Orientação do Contribuinte (versão, prazo de contingência, `tpEmis`); PDF das NTs; Ato Conjunto RFB/CGIBS nº 8/2026; calendário real do split payment; NFC-e por UF; Focus NFe e Tecnospeed; tabela CFOP; regras estaduais de DIFAL, Simples e fundo de pobreza; ADIs do STF; API de preço/prazo dos Correios; Frenet; endpoints de cálculo e compra do Melhor Envio; fluxo de saldo e cobrança do Melhor Envio. O art. 49 do CDC deixou de ser "Não verificável" (lido, V-55), mas a aplicação ao e-commerce e os prazos seguem **Requer revisão jurídica**.

## 9. Testes

- Data do fato gerador: operação em **31/12/2026 × 01/01/2027** com o mesmo produto, alíquotas vindas da tabela versionada.
- Nenhuma alíquota ou código fiscal literal no código (busca textual).
- Soma dos tributos por item = total da nota pela regra oficial.
- CNPJ alfanumérico em cadastro, coluna, máscara e chave NF-e; CPF com zero à esquerda.
- Frete: CEP com zero à esquerda; cotação gravada com o pedido; etiqueta só após evento de pagamento verificado; webhook com assinatura inválida; evento repetido.
- Prazo em dias úteis com feriado no meio e fuso (Manaus × São Paulo).
