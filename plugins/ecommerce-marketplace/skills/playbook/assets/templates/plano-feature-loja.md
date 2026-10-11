# SPEC: [NOME DA FUNCIONALIDADE DA LOJA]

Uso: funcionalidade de preço, promoção, frete, pagamento, estoque ou pedido. Entrevista curta (uma pergunta por vez, só o que muda a solução), depois este documento, depois **aprovação humana antes de implementar**. Base: V-22 (entrevista, EARS), V-38 (promoção). Marque cada afirmação sobre norma, API ou prazo com Verificado / Inferido / Suposição / Não verificável.

## 1. Contexto
- Objetivo de negócio: [UMA FRASE]
- Comprador ou operador afetado: [QUEM]
- Plataforma e versão: [Shopify aaaa-mm | Medusa v2.x | Woo REST | VTEX | Nuvemshop | própria] · PSP e modo: [nome | teste/live] · Moeda: [BRL]
- Alternativa mais simples considerada: [O QUE FOI DESCARTADO E POR QUÊ]
- Modo de escopo: [expandir | manter | reduzir] — justificativa: [UMA FRASE]

## 2. Regras de negócio com exemplos numéricos
| # | Regra | Exemplo (entrada → saída esperada) | Status |
| --- | --- | --- | --- |
| R1 | [REGRA] | [Ex.: R$ 200,00, cupom 10% e R$ 20,00 → 160,00 (percentual primeiro)] | decidido / a decidir |

Decisões obrigatórias quando houver desconto: ordem percentual × fixo; limite do frete grátis antes ou depois do desconto; regra de arredondamento e de resto; acumulação de cupons.

## 3. Requisitos (EARS)
- RQ-01 QUANDO [EVENTO], O SISTEMA DEVE [RESPOSTA].
- RQ-02 ENQUANTO [ESTADO], O SISTEMA DEVE [RESPOSTA].
- RQ-03 SE [CONDIÇÃO INDESEJADA], ENTÃO O SISTEMA DEVE [RESPOSTA].

## 4. Casos de borda (marque os que se aplicam)
- [ ] Estoque zero ou última unidade com dois compradores
- [ ] Cupom duplicado, expirado, de primeira compra reutilizado, item excluído da promoção
- [ ] Pagamento recusado, em análise, expirado (Pix/boleto) ou tardio
- [ ] Reenvio da mesma requisição (duplo clique, retry após timeout)
- [ ] Carrinho com 3 itens de preços diferentes e um fora da promoção
- [ ] CEP inexistente, rural, com zero à esquerda
- [ ] Moeda e arredondamento em parcelas; soma = total
- [ ] Pedido de outro cliente (autorização por objeto)

## 5. Fora de escopo
- [ITEM 1] · [ITEM 2]

## 6. Restrições fiscais, legais e de dados (Requer revisão especializada)
| Tema | Situação | Rótulo | Fonte e data de leitura |
| --- | --- | --- | --- |
| [Ex.: preço final com frete discriminado] | [ATENDE/NÃO/A VERIFICAR] | [Verificado/Não verificável] | [Decreto 7.962 art. 2º, 2026-10-10] |

## 7. Gates e riscos
- Efeitos externos (cobrança, reembolso, etiqueta, nota, publicação): proibidos em teste; aprovação humana para qualquer efeito real.
- Riscos: [LISTA]

## 8. Plano de implementação (fatias verticais)
1. [FATIA 1: teste primeiro] 2. [FATIA 2] 3. [FATIA 3]

## 9. Verificação executável (passo final)
- Comando: `[COMANDO DE TESTE/BUILD/LINT]` · Saída esperada: [CRITÉRIO]
- Oráculo independente dos valores: [PLANILHA/CÁLCULO SEPARADO]
- Evidência a colar: saída dos comandos, contagem de linhas no banco, diff.

## 10. Aprovação
- Aprovado por: [NOME] em [DATA] · Pendências antes de implementar: [LISTA]
