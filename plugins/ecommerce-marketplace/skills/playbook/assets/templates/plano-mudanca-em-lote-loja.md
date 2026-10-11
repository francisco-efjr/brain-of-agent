# Plano de mudança em lote na loja (gate de 7 passos)

Uso: preço em massa, importação CSV, redirecionamentos, SEO em massa, exclusão, mesclagem de clientes, cancelamento/reembolso em lote, publicação de tema. Gate de **redação própria** do plugin (V-18, V-19, V-25). Nada é escrito antes da aprovação do passo 4. Produção bloqueada por padrão; em dúvida, negue e pergunte.

## 0. Pedido e ambiente
- Mudança: [DESCRIÇÃO] · Plataforma e versão da API: [X] · Ambiente: [teste | dev | live] · Janela: [DATA/HORA]
- Critério de aceite: [COMO SABER QUE DEU CERTO] · Responsável pela aprovação: [NOME]

## 1. Credencial e escopo
- Variável de ambiente (apenas o nome): [NOME_DA_VARIÁVEL] · Escopo: [somente leitura | leitura e escrita em X] · Segredo fora do chat e do repositório: [CONFIRMADO]

## 2. Contagem e amostra (somente leitura)
| Item | Esperado | Encontrado | Divergência |
| --- | --- | --- | --- |
| Registros a alterar | [N] | [N] | [parar se divergir] |
| Amostra (5 a 10) | | [IDs] | |
Critério de seleção: [FILTRO EXATO]

## 3. Prévia (`dry_run`) com diff
| ID/SKU | Campo | Antes | Depois | Observação |
| --- | --- | --- | --- | --- |
| [ID] | [CAMPO] | [VALOR] | [VALOR] | |
Regras aplicadas: [ARREDONDAMENTO, EXCLUSÕES, ORDEM COM PROMOÇÕES]

## 4. Confirmação humana
- Itens: [N] · Soma/valores afetados: [X] · Ação irreversível? [SIM/NÃO]
- Se sim: backup/exportação prévia em [CAMINHO] (data/hora [X]) e **confirmação própria** da pessoa: [TEXTO/DATA]
- Aprovado por: [NOME] em [DATA/HORA]

## 5. Execução
- Tamanho do lote: [N] · Chave de idempotência por lote: [PADRÃO] · Registro: [LOG SEM PII]
| Lote | Itens | Status | Falhas |
| --- | --- | --- | --- |
| 1 | | | |

## 6. Releitura pela API-fonte da verdade
- Comparação com a prévia: [OK/DIVERGÊNCIA] · O storefront/CDN não é a verdade (cache) · Divergências: [LISTA]

## 7. Relatório e reversão
- O que mudou (antes/depois, contagens): [X] · Como desfazer: [PASSOS] · Reversão testada? [SIM/NÃO TESTADA]
- Pendências e riscos: [LISTA] · Próximo passo: [AÇÃO]
