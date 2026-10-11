# Plano de testes de pagamentos

Base: V-33, V-61, V-65 e `dominios.md` do brain-of-agent (MIT). **O oráculo é um cálculo independente ou o extrato da outra ponta, nunca o valor que o próprio sistema mostra.** Use só o modo de teste do provedor e dados sintéticos; nenhuma chamada a API real; assinaturas de webhook geradas localmente. Para estratégia geral de QA, E2E e carga: `/qa-testing:playbook`.

## 1. Fluxo e riscos

- Fluxo/módulo/provedor sob teste: [ ] · Modo: teste · Stack de testes: [ ]
- Riscos priorizados (cobrança dupla, centavo perdido, saldo que não fecha, divergência de conciliação): [lista ordenada com motivo]
- Regras de negócio escritas (limites, fuso, arredondamento): [ ] · Fonte de cada número regulatório: [fonte vigente ou "seed a confirmar"]

## 2. Matriz de casos

| ID | Risco | Caso (dado de entrada) | Esperado | Oráculo independente | Fonte do número | Nível |
| --- | --- | --- | --- | --- | --- | --- |
| TC-01 | cobrança dupla | duplo clique; mesma chave; timeout + retry | uma cobrança; a 2ª chamada devolve a 1ª | contagem de linhas no banco | V-01 | integração |
| TC-02 | chave mal escopada | mesma chave com R$ 100,00 e depois R$ 150,00 | conflito registrado | linha de conflito | V-01 | integração |
| TC-03 | rateio | R$ 100,00 em 3 partes | 33,34 + 33,33 + 33,33; soma = total | cálculo independente / propriedade | V-10 | unidade |
| TC-04 | arredondamento | vetores da tabela da seção 3 | valores esperados da política escolhida | tabela da seção 3 | V-61 | unidade |
| TC-05 | concorrência de saldo | dois débitos de R$ 80,00 em R$ 100,00 | um aprova, um recusa; saldo ≥ 0 | saldo derivado do histórico | V-33 | integração (barreira real) |
| TC-06 | estorno | total; parcial; dois parciais > original | parcial reduz o estornável; soma acima recusada | ledger | V-33 | integração |
| TC-07 | webhook | válido, forjado, duplicado, fora de ordem, ID desconhecido, crash após efeito | ver roteiro hostil | estado no banco | V-05, V-06 | integração |
| TC-08 | conciliação | fonte truncada; totais iguais, itens diferentes | `INCOMPLETE_SOURCE`; divergência por chave | extrato | V-08 | dados |
| TC-09 | Pix timeout | resposta não chega | consulta por `EndToEndId` antes de reenviar | status no PSP (stub) | V-33 (seed 30 s) | integração |
| TC-10 | Pix txid/valor | `txid` com 25, 26, 35, 36 caracteres; reuso; valor `0.00`, `10.0`, `10.001` | só 26 a 35 aceitos; valor com 2 casas; zero é erro | schema do BCB | V-43 | unidade |
| TC-11 | Pix devolução | acima do saldo; fora da janela; id repetido | recusa | spec vigente (janela: conferir) | V-43 | unidade |
| TC-12 | BR Code | CRC válido (vetor positivo do Manual); payload alterado; dinâmico com valor/`txid`; dinâmico reutilizado | positivo aceito; alterado recusado; valor/`txid` ignorados; reuso aceito | CRC16 0x1021/0xFFFF sobre o payload até "6304" | V-65 | unidade |
| TC-13 | boleto | formatos 44/47/48; DV por campo; fator 21/02 e 22/02/2025; sem valor | conversão sem perder dígito; DV aponta o campo | norma (**Não verificada**) | brain | unidade |
| TC-14 | cartão | Luhn; recusa por motivo; saldo insuficiente | recusado no cliente sem chamar o gateway; mensagem por motivo | cartões de teste **do provedor** | brain | unidade/integração |
| TC-15 | 3DS | sem fricção; desafio aprovado; recusado; abandonado; timeout | pedido não fica pago sem autenticação nem preso para sempre | estado do PaymentIntent (stub) | V-39 | integração |
| TC-16 | parcelamento | parcela mínima; soma = total; troca com cupom; estorno parcelado | soma exata | cálculo independente | brain | unidade |
| TC-17 | token de outro usuário | cartão salvo de outra conta | 404/403 (IDOR) | resposta + log | V-26 (I) | integração |
| TC-18 | antifraude | 10 tentativas em 1 min, cartões diferentes, mesmo dispositivo | bloqueio ou desafio; caminho de recuperação | log do motor | brain | integração |
| TC-19 | limites e virada | R$ 5.000,00: 4.999,99 + 0,01 + 0,01; 23:59:59 e 00:00:00 no fuso do cliente | aceita até o limite exato; recusa o excedente; zera no fuso da regra | relógio fixo | brain | unidade |
| TC-20 | PAN em log | `4242424242424242` em payload de teste | nenhum PAN nos logs | regex + Luhn | V-23 | integração |

Números regulatórios (limite noturno, dispositivo novo, MED, Pix Automático) entram **apenas** como "seed a confirmar", configuráveis, nunca como oráculo.

## 3. Vetores de arredondamento (V-61; válidos só para a política escolhida; Python verificado, Java não executado)

| Entrada | Casas | Modo | Esperado |
| --- | --- | --- | --- |
| `0.125` | 2 | HALF_EVEN | `0.12` |
| `0.125` | 2 | HALF_UP | `0.13` |
| `2.345` | 2 | HALF_UP | `2.35` |
| `2.345` | 2 | HALF_EVEN | `2.34` |
| `2.355` | 2 | HALF_EVEN / HALF_UP | `2.36` |
| `7.325` | 2 | ROUND_DOWN | `7.32` |
| `7.325` | 0 | ROUND_UP | `8` |

## 4. Massa sintética

`documentos_br.py` (skill `payment-test-plan`): `gerar cpf`, `gerar cnpj-alfa`, `validar`, **só em teste**, nunca para consultar bases externas; um CPF/CNPJ gerado com DV correto pode pertencer a alguém real. Cartões de teste: os do próprio provedor (cada gateway publica os seus; os da Stripe herdados do brain devem ser conferidos).

## 5. Execução

| Teste | Comando | Saída essencial | Resultado | Provou o defeito? (mutação manual: remover a proteção e ver o teste falhar) |
| --- | --- | --- | --- | --- |
| [TC-01] | [ ] | [ ] | [passou / falhou / **Não executado**] | [sim / não / n/a] |

Regra: o que não rodou fica **Não executado**, com o motivo; não afirme resultado de teste que você não executou.
