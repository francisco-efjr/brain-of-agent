# Documento de SLO — [SERVIÇO]

Template T-01. Base: SRE Book/Workbook sobre SLO (V-01), redação própria. Preencha na ordem; campo sem dado real recebe o rótulo **Suposição** e entra em "Dados que faltam". Não use 100%, média nem metas copiadas de exemplo.

**Serviço e dono:** [serviço] · [time] · **Revisão:** [data] · próxima: [data] · **Rótulo geral:** [Verificado/Inferido/Suposição]

## 1. Jornadas críticas (passo 1)

| ID | Jornada em linguagem de usuário | Por que é crítica |
| --- | --- | --- |
| J1 | [ex.: finalizar compra] | [receita, volume, contrato] |

## 2. Fluxo e dependências (passo 2)

[Quem chama quem; o que é síncrono; dependências de terceiros. Ex.: web → API de pedidos → banco → gateway de pagamento (terceiro).]

## 3. SLIs (passos 3 e 4; no máximo 5 tipos)

| SLI | Especificação (linguagem de usuário) | Implementação (a mais barata disponível) | Cobertura e limites |
| --- | --- | --- | --- |
| Disponibilidade | Proporção de [`POST /pedidos` válidas] que retornam sem erro | [logs de acesso do nginx, campo `status`] | [não cobre falhas antes do balanceador] |
| Latência | Proporção de [requisições] com duração abaixo do limiar | [`request_time` no log] | [mede o servidor, não a rede do cliente] |
| [Conclusão assíncrona, se houver] | Proporção de pedidos concluídos em até [prazo] | [evento de conclusão − evento de aceite] | [não cobre pedido que nunca emite evento] |

Erro implícito (conta como ruim): [200 com corpo de erro; resposta acima do limiar de política].

## 4. Linha de base e metas (passos 5 e 6)

Janela fixa de medição: [ex.: 28 dias corridos]. Dados medidos: [valor medido colado com a consulta/período]. Meta = linha de base arredondada **para baixo**.

| SLI | Medido | Meta proposta | Janela do SLO | Latência: limiar 1 (maioria) | Limiar 2 (cauda) |
| --- | --- | --- | --- | --- | --- |
| Disponibilidade | [x%] | [≤ medido, < 100%] | [28 ou 30 d corridos] | n/a | n/a |
| Latência | [p50/p95/p99 medidos] | [proporção] | idem | [ex.: 90% < X ms] | [ex.: 99% < Y ms] |

Error budget: 100% − [meta] = [x%] ≈ [conta: (1 − meta) × janela, ex.: 0,001 × 30 × 24 × 60 = 43,2 min]. Cole a conta feita para a sua meta.

## 5. Consequência (passo 7)

[ ] SLO (sem consequência contratual) · [ ] SLA: [consequência explícita: crédito, multa, penalidade]. SLO interno mais apertado que o divulgado: [sim/não, valor]. Teste: sem consequência explícita = SLO.

Aprovado por: produto [nome/papel, data] · desenvolvimento [..] · operação [..]. Política de error budget: [link para o documento da política: T-02].

## 6. Painel e revisão (passo 8)

Painel de conformidade: [URL ou "a criar"]. Revisão contra incidentes e tickets a cada [ciclo]: [data da última, achados].

## 7. Dados que faltam e riscos

| Item | Impacto | Como obter | Dono |
| --- | --- | --- | --- |
| [ex.: p99 dos últimos 28 dias] | [meta de latência é Suposição] | [consulta no log/APM] | [papel] |

Limitações: [ex.: SLO de dependência não é SLO do usuário; HTTP 2xx não prova sucesso de negócio].
