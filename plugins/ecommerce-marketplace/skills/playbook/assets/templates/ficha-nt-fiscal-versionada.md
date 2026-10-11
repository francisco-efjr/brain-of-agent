# Ficha de Nota Técnica fiscal versionada

Uso: registrar cada Nota Técnica (NT) da NF-e/NFC-e, informe e tabela fiscal que o projeto usa, **antes** de gerar qualquer campo. O plugin não emite documento fiscal real: emissão só em homologação. Valores e códigos (alíquotas, CFOP, NCM, prazos) moram **aqui, com data e fonte**, nunca fixos no código nem de memória (V-34, V-56, V-58, V-59). **Requer revisão fiscal.**

## Cabeçalho
- Projeto: [NOME] · Responsável fiscal: [NOME | pendente] · Data da última leitura da lista de NTs: [AAAA-MM-DD] · Fonte da lista: https://www.nfe.fazenda.gov.br/portal/principal.aspx (Notas Técnicas e Informes)

## Fichas
| NT / informe | Versão | Assunto | UF | Publicação | Homologação | Produção | Prazo de contingência (lido no MOC/NT) | Fonte (URL) | Data de leitura | Status no projeto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025.002 | v1.52 | Adequação dos leiautes da NF-e e NFC-e à Reforma Tributária do Consumo | todas | 2026-10-01 | 2026-10-26 (postergada, informe de 05/10/2026) | 2026-11-16 (postergada) | [não lido] | Portal NF-e, lista de NTs | 2026-10-10 | [a implementar em homologação] |
| 2026.006 | v1.00 | Vinculação NF-e × transação financeira sujeita ao split payment | todas | 2026-08-25 | [consultar] | [consultar] | n/a | Portal NF-e | 2026-10-10 | [acompanhar] |
| 2026.004 | v1.01 | CNPJ alfanumérico | todas | 2026-06-08 | [consultar] | [consultar] | n/a | Portal NF-e | 2026-10-10 | [validar cadastros] |
| [NT] | | | [UF] | | | | | | | |

Valores acima são exemplos **Verificados em 2026-10-10**; reconfira no portal (as datas mudam por informe). Campos IBS/CBS (tags), MOC e atos conjuntos: **Não verificados**.

## Tabelas fiscais versionadas
| Tabela | Versão/vigência | UF | Fonte (SEFAZ/Planalto) | Data de leitura | Quem validou |
| --- | --- | --- | --- | --- | --- |
| Alíquotas IBS/CBS | [vigência por data do fato gerador] | n/a | LC 214/2025 (arts. 343, 344, 346, 347) | [AAAA-MM-DD] | [NOME] |
| Alíquotas internas/interestaduais (DIFAL) | [vigência] | [UF] | Portal da SEFAZ da UF de destino | [AAAA-MM-DD] | [NOME] |
| CFOP | [versão] | [UF] | [link da SEFAZ] | [AAAA-MM-DD] | [NOME] |
| NCM | [versão, informe 03/09/2026] | n/a | [link] | [AAAA-MM-DD] | [NOME] |

## Regras
1. O agente indica a tabela e a pergunta; quem tem responsabilidade fiscal escolhe o código.
2. Teste de data: operação em 31/12/2026 × 01/01/2027 com o mesmo produto.
3. Sem tabela preenchida, a resposta é "Não verificável".
