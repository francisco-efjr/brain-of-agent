# NF-e, IBS/CBS, DIFAL, split payment, contingência e CFOP/NCM

Modelo-alvo e data de validação: Claude 4.x/5.x, 2026-10-10. **Requer revisão fiscal** em tudo. Nada aqui é parecer nem aconselhamento tributário; nenhum documento fiscal é emitido. Fontes lidas por validador em 2026-10-10: Portal Nacional da NF-e (V-34), LC 214/2025 no Planalto, com redações da LC 227/2026 (V-33, V-57), LC 190/2022 e EC 87/2015 (V-56), página da SEFAZ-GO sobre problemas técnicos (V-58). Tabela de transição CBS/IBS do brain-of-agent (MIT) é **Inferido** onde não coberta pela lei lida. O texto das leis foi parafraseado.

## 1. Ficha de Nota Técnica (modelo e exemplos lidos em 2026-10-10)

Campos de `ficha-nt-fiscal-versionada.md`: NT · versão · publicação · homologação · produção · UF · prazo de contingência (lido no MOC/NT) · fonte · data de leitura.

| NT | Versão | Assunto | Publicação | Homologação | Produção | Rótulo |
|---|---|---|---|---|---|---|
| 2025.002 | v1.52 | Adequação dos leiautes da NF-e e NFC-e à Reforma Tributária do Consumo (campos e regras de validação) | 01/10/2026 | 26/10/2026 (postergada, informe de 05/10/2026) | 16/11/2026 (postergada) | Verificado (portal) |
| 2026.007 | v1.10 | Regras com a Lista Centralizada de Contribuintes e o CCC | 01/10/2026 | 26/10/2026 (postergada) | 16/11/2026 (postergada) | Verificado |
| 2026.008 | v1.00 | (ver portal) | 01/10/2026 | 26/10/2026 (postergada) | 16/11/2026 (postergada) | Verificado (assunto não lido) |
| 2026.010 | v1.00 | Modelo do DANFE para a RTC | 01/10/2026 | não lido | não lido | Verificado a publicação |
| 2026.006 | v1.00 | Vinculação entre NF-e e transação financeira sujeita ao split payment | 25/08/2026 | não lido | não lido | Verificado a publicação |
| 2026.004 | v1.01 | CNPJ alfanumérico | 08/06/2026 | não lido | não lido | Verificado a publicação |
| 2021.003 | v1.50 | GTIN | 25/09/2026 | não lido | não lido | Verificado a publicação |

Informes técnicos de 03/09/2026 (NCM, vigente a partir de 01/10/2026) e 04/09/2026 (CFOP) existem no portal. Não foi lido: o Manual de Orientação do Contribuinte (versão), o PDF das NTs (tags IBS/CBS), o Ato Conjunto RFB/CGIBS nº 8/2026 e a documentação de emissores (Focus NFe, Tecnospeed). **Os campos IBS/CBS concretos (tags) seguem Não verificados.** O portal exige cookie de sessão anônima para leitura por `curl` (V-34). Revisão trimestral: registre a data da leitura e releia a lista antes de gerar qualquer campo.

Regras da skill (V-34): (1) antes de gerar qualquer campo, consultar a lista de NTs e registrar número, versão, publicação e as datas de homologação e produção, que mudam por informe; (2) emissão apenas em homologação; (3) tabelas NCM, CFOP e GTIN versionadas por informe e NT; (4) em marketplace, tratar o intermediador e o vínculo com a transação financeira (split payment, NT 2026.006) como requisitos a conferir no manual; (5) o plugin nunca emite documento fiscal real; (6) entrega checklist e mapeamento de dados, não XML assinado em produção.

### Mapeamento campo a campo (modelo)

| Campo/grupo da NF-e | Origem do dado no pedido | Regra | NT/fonte | Rótulo |
|---|---|---|---|---|
| Emitente (CNPJ numérico ou alfanumérico) | Cadastro da empresa/vendedor | DV conforme NT 2026.004 | NT 2026.004 | Verificado (existência da NT); campos finos: ler a NT |
| Destinatário (CPF/CNPJ, IE, endereço) | Checkout | Validar formato (seção Documentos) | MOC | Não verificado |
| Itens: NCM, CFOP, GTIN | Tabela versionada de produtos | Nunca de memória (seção 6) | Informes 03/09 e 04/09/2026 | Requer revisão fiscal |
| Tributos IBS/CBS | Tabela de vigência por fato gerador | Seção 2 | LC 214/2025 + NT 2025.002 | Alíquotas 2026 Verificadas; tags Não verificadas |
| Vínculo com transação financeira | Dados do pagamento | Exigência do split | NT 2026.006 | Conferir manual |
| Chave de acesso (44 posições) | Gerada pelo emissor | DV módulo 11 (ASCII - 48 com emitente alfanumérico) | MOC | Inferido (brain) |

## 2. IBS/CBS por data do fato gerador

| Período | Regra | Verificado por LC 214? | Fonte |
|---|---|---|---|
| 2026 | CBS 0,9% (art. 346); IBS 0,1% estadual (art. 343); valores recolhidos compensados com tributos vigentes (art. 348) | **Sim** | V-33 |
| 2027 a 2028 | IBS de 0,05% estadual + 0,05% municipal (art. 344); CBS = alíquota fixada pelo art. 14 reduzida em 0,1 ponto percentual (art. 347) | **Sim**; valor da alíquota do art. 14: **Não verificável** (não lida) | V-33 |
| 2029 a 2032 | ICMS e ISS reduzidos gradualmente enquanto o IBS cresce | **Não** (resumo do brain) | Inferido (brain) |
| 2033 | Fim da transição; ICMS e ISS extintos | **Não** | Inferido (brain) |
| Imposto Seletivo (2027) | Começa a vigorar | **Não** | Inferido (brain) |
| Alíquotas finais, regimes específicos, crédito presumido | — | **Não verificável** | — |

O brain resume 2027 como "CBS em alíquota cheia" e "PIS e Cofins extintos"; o art. 347 lido diz que em 2027 e 2028 a CBS é a alíquota do art. 14 reduzida em 0,1 p.p.: prevalece o texto lido da lei. O brain também diz que em 2026 "o recolhimento é dispensado para quem cumpre as obrigações acessórias": a lei lida confirma a compensação (art. 348); a dispensa **não** foi lida (Inferido).

Regra do plugin (V-33): todo cálculo de tributo recebe a **data do fato gerador**; de 2027 em diante exige tabela de alíquotas versionada, **nunca valores fixos no código**; local da operação com bem material é o da entrega (art. 11, I).

### Teste de vigência (executado em 2026-10-10, Python 3.14)

```python
from datetime import date
from decimal import Decimal

VIGENCIAS = [  # fonte: LC 214/2025 arts. 343, 346 e 348 (lidos em 2026-10-10); períodos sem linha = erro explícito
    {"de": date(2026, 1, 1), "ate": date(2026, 12, 31), "cbs": Decimal("0.009"), "ibs": Decimal("0.001"),
     "fonte": "LC 214/2025 art. 343 e 346", "lido_em": date(2026, 10, 10)},
    # 2027+: adicionar SOMENTE com a alíquota lida em norma/ato vigente, com fonte e data.
]

class AliquotaNaoVerificada(Exception):
    pass

def aliquotas(fato_gerador: date) -> dict:
    for v in VIGENCIAS:
        if v["de"] <= fato_gerador <= v["ate"]:
            return v
    raise AliquotaNaoVerificada(f"sem linha versionada para {fato_gerador.isoformat()}")   # falha fechada

assert aliquotas(date(2026, 12, 31))["cbs"] == Decimal("0.009")
try:
    aliquotas(date(2027, 1, 1))
    raise SystemExit("deveria falhar: não há linha para 2027")
except AliquotaNaoVerificada:
    pass
```

Os valores de 2026 aparecem aqui só como linha de tabela com fonte e data; no projeto, a tabela vive em arquivo de dados versionado (JSON/CSV/tabela no banco), não em constante de código.

## 3. DIFAL em venda interestadual a consumidor final não contribuinte (V-56)

Checklist que bloqueia a emissão sem conferência (todas as respostas por contador; **Requer revisão tributária**):

1. O destinatário é contribuinte? (Verificado na LC 190/2022 sobre a LC 87/1996: em operação interestadual a consumidor final, o contribuinte da diferença entre a alíquota interna do destino e a interestadual é o **remetente** quando o destinatário **não é contribuinte**; destinatário, quando contribuinte.)
2. Alíquotas interna e interestadual de **tabela versionada**, com UF e data.
3. Portal da UF de destino consultado (a lei manda os Estados manterem portal com legislação, alíquotas interna e interestadual, benefícios e obrigações acessórias, e ferramenta de apuração centralizada).
4. Campos da NF-e conferidos na NT vigente (seção 1).
5. Simples Nacional e substituição tributária: por contador.
6. Valores só em `references/` com data, UF e fonte, nunca no texto da skill.

Verificado: o imposto da diferença cabe ao Estado de destino (base pela alíquota interna do destino); o fato gerador inclui a saída de bem a consumidor final não contribuinte de outro Estado; a LC 190 entra em vigor na publicação, com efeitos sujeitos à anterioridade (Constituição, art. 150, III, "c"); a EC 87/2015 (art. 99 do ADCT) fixa a partilha: 20% (2015), 40% (2016), 60% (2017), 80% (2018) e **100% para o destino a partir de 2019**. **Não verificável**: alíquotas de exemplo (7% e 12%), regras do Simples Nacional, grupo de partilha na NF-e e NFC-e, datas e teor das ADIs 7066, 7070 e 7078, convênios do Confaz, regras estaduais de substituição tributária.

## 4. Split payment de IBS/CBS (V-57)

- Art. 31 da LC 214/2025: prestadores de serviço de pagamento eletrônico e instituições operadoras de sistemas de pagamento segregam e recolhem IBS e CBS na liquidação financeira, em arranjos abertos e fechados, públicos e privados.
- Procedimento **padrão** (art. 32): o fornecedor inclui no documento fiscal eletrônico dados que vinculam a operação ao pagamento e identificam os débitos; o originador da transação transmite as informações. Procedimento **simplificado** (art. 33, opcional na redação da LC 227/2026): percentual preestabelecido pelo Comitê Gestor do IBS e pela RFB, aplicável a operações em que o adquirente não é contribuinte do regime regular; excedente devolvido ao fornecedor em até 3 dias úteis após a apuração; ato conjunto pode determinar o simplificado enquanto o padrão não estiver funcionando em nível adequado.
- Art. 34: segregação na liquidação, proporcional em parcelas; antecipação de recebíveis não altera; os PSPs são responsáveis por segregar e recolher, mas **não são responsáveis tributários**.
- Art. 35 e produção de efeitos: o split deve entrar em funcionamento de forma simultânea nas operações com adquirentes não contribuintes do regime regular, para os principais instrumentos de pagamento do varejo; ato conjunto define a implementação gradual e pode prever hipóteses facultativas.
- **Correção da validação:** a sugestão "fase inicial B2B e nenhuma ação em B2C" foi **rejeitada**; o texto mira justamente o adquirente não contribuinte. Uma fase B2B opcional por regulamento pode existir, mas é **Não verificável**.
- Não verificado (não use): Decreto 12.955/2026, Ato Técnico Conjunto nº 4/2026, início de testes em 15/10/2026, manuais de habilitação de 8/9/2026; calendário 2027 × 2028; arranjos da primeira fase; campos por transação.
- Checklist de espera: (1) split no plano de revisão trimestral com o rótulo "norma lida: arts. 31 a 35 da LC 214/2025 com LC 227/2026; calendário e campos: Não verificável"; (2) não implementar campos por transação sem ato conjunto e manual oficiais; (3) marketplace B2C: acompanhar, com decisão do contador e do PSP; (4) o plugin não calcula nem recolhe IBS/CBS.

## 5. Contingência de NF-e (V-58; Classe B6 para o conceito)

Fonte lida: SEFAZ-GO; o painel de contingência SVC-AN do Portal Nacional estava sem Estado em contingência na leitura.

| Modalidade | O que é (conforme a página lida) |
|---|---|
| FS-DA | DANFE em formulário de segurança; envio à SEFAZ de origem após o problema |
| EPEC | Registro prévio permite DANFE em papel comum; a validade depende da transmissão posterior |
| SVC | Depende da ativação pela SEFAZ de origem (Goiás usa SVC-RS); DANFE em papel comum e sem nova transmissão à origem |

FS-DA e EPEC devem ser transmitidas logo após o fim do problema, observado o **prazo limite da legislação, que a página não numera** (remete ao Manual de Orientação do Contribuinte). Checklist do emissor: (1) modalidade e UF de origem; (2) prazo limite do MOC/NT vigentes (não escrito na skill); (3) `tpEmis` conferido no MOC; (4) nada em produção sem homologação; (5) resultado marcado Não verificável até a leitura. **Rejeitados como fato** até leitura do MOC: prazo de 168 h, códigos `tpEmis` (4, 6, 7, 9 aparecem só em busca) e evento 110140.

## 6. CFOP e NCM: regra de não fixar código (V-59)

Regra de projeto (Suposição fundamentada; nenhum texto primário de CFOP foi lido; a URL tentada do Ajuste SINIEF 3/2024 retornou 404, o que pode ser URL errada): (1) CFOP e NCM não saem de memória nem do texto da skill; ficam em tabela versionada com data, UF e link da SEFAZ; (2) quem tem responsabilidade fiscal escolhe o código; (3) o agente indica a tabela e a pergunta, não o código. Informes de 03/09/2026 (NCM, vigente desde 01/10/2026) e 04/09/2026 (CFOP) constam do portal e devem ser lidos pelo responsável.

## 7. Lista consolidada: Não verificável nesta rodada

Campos/tags IBS/CBS; MOC (versão, prazos, `tpEmis`); NFC-e por UF; Frenet; API de preço e prazo dos Correios (atrás de login); regras estaduais de DIFAL, Simples e fundo de pobreza; ADIs do STF; calendário real do split; tabela CFOP; Ato Conjunto RFB/CGIBS nº 8/2026; Focus NFe e Tecnospeed. O CDC art. 49 deixou de ser Não verificável (lido em V-55); sua aplicação ao e-commerce e os prazos continuam Requer revisão jurídica (ver skill `estoque-reserva-pedido`).
