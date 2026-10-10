# SLI, SLO e error budget

Para definir o primeiro SLO, revisar um existente ou redigir a política de error budget. Consulta às fontes: 2026-10-10. Texto em redação própria (os livros de SRE do Google são tratados como CC BY-NC-ND: nada é copiado). Rótulos: Verificado (lido na fonte), Inferido, Suposição, Não verificável.

## Sumário

- [Vocabulário mínimo](#vocabulário-mínimo)
- [Os 8 passos para o primeiro SLO](#os-8-passos-para-o-primeiro-slo)
- [SLIs por tipo de sistema](#slis-por-tipo-de-sistema)
- [Aritmética do error budget](#aritmética-do-error-budget)
- [Política de error budget](#política-de-error-budget)
- [Caso: 202 aceito, fila parada](#caso-202-aceito-fila-parada)
- [Plantão e toil](#plantão-e-toil)
- [Erros comuns ao propor SLOs](#erros-comuns-ao-propor-slos)

## Vocabulário mínimo

| Termo | Definição operacional | Exemplo |
| --- | --- | --- |
| SLI | Medida do que o usuário percebe, em proporção de eventos bons | requisições `POST /pedidos` com status < 500 e duração < 800 ms ÷ requisições válidas |
| SLO | Meta para o SLI numa janela | 99,9% em 30 dias corridos |
| SLA | SLO com consequência explícita (contrato, multa, crédito) | Crédito de 10% se disponibilidade mensal < 99,5% |
| Error budget | 100% − meta; quanto de falha o produto pode gastar | 0,1% (99,9%) |
| Burn rate | Velocidade de consumo do budget; 1 = consome exatamente o budget até o fim da janela | 14,4 = 2% do budget em 1 h numa janela de 30 d |

Teste de classificação: se não existe consequência explícita para o descumprimento, é SLO, não SLA. SLO interno costuma ser mais apertado que o divulgado (Verificado, V-01).

## Os 8 passos para o primeiro SLO

Fonte: V-01 (SRE Book "Service Level Objectives" e SRE Workbook "Implementing SLOs", Classe A). A sequência é do livro; as colunas "Critério de saída" e "Erro típico" são nossas (Inferido).

| # | Passo | Critério de saída | Erro típico |
| --- | --- | --- | --- |
| 1 | Escolher serviço e jornadas críticas do usuário | Lista de 1–3 jornadas em linguagem de usuário ("finalizar compra") | Começar pela infraestrutura ("CPU") |
| 2 | Mapear fluxo e dependências críticas | Diagrama ou lista: quem chama quem, o que é síncrono | Ignorar dependência de terceiro que domina a latência |
| 3 | Definir até 5 tipos de SLI, cada um com especificação em linguagem de usuário | Cada SLI tem uma frase "proporção de X que Y" | 12 SLIs que ninguém acompanha; média como SLI |
| 4 | Escolher a implementação mais barata disponível (logs de acesso, APM, métricas do balanceador) e registrar cobertura e limites | Campo "implementação" e "o que não cobre" preenchidos | Confundir especificação com implementação |
| 5 | Medir a linha de base em janela fixa; arredondar para baixo para propor a meta | Número medido colado + meta ≤ medido | Propor meta sem dado, ou acima do que o serviço já entrega |
| 6 | Latência com 2 limiares (maioria e cauda) | Ex.: p50 e p99, ou "90% < X e 99% < Y" | Um limiar só; usar máximo |
| 7 | Negociar a meta com produto, dev e operação; declarar a consequência (SLO ou SLA) | Ata com 3 aprovadores | Meta decidida só por engenharia |
| 8 | Publicar painel de conformidade; revisar contra incidentes e tickets a cada ciclo | Painel + data da próxima revisão | SLO sem revisão: vira papel |

Notas:
- A janela de 4 semanas do livro é ilustrativa (V-01). Janelas corridas de 28 ou 30 dias são comuns; calendário mensal esconde meses de tamanhos diferentes. Escolha uma e use a mesma no alerta.
- Meta nunca é 100%: o custo cresce de forma desproporcional e trava qualquer mudança (V-01).
- Percentis, nunca média. A média de 99 respostas de 100 ms e uma de 10 s é 199 ms; uma em cada 100 requisições esperou 10 s.
- Sem dados reais, a meta é **Suposição**; escreva "medir antes de comprometer".

## SLIs por tipo de sistema

O livro agrupa sistemas em serviço ao usuário, armazenamento e pipelines/big data (V-01). Os exemplos abaixo são nossos (Inferido).

| Tipo | SLIs típicos | Observação |
| --- | --- | --- |
| Serviço ao usuário (API, web) | Disponibilidade (respostas não-erro ÷ válidas), latência (proporção abaixo do limiar), qualidade (resposta íntegra, não degradada) | Contar erro implícito: 200 com conteúdo errado (V-04) |
| Armazenamento | Latência de leitura/escrita, disponibilidade, durabilidade (perda de dados) | Durabilidade se mede por verificação periódica, não por alerta de uso |
| Pipeline / lote | Frescor (idade do dado mais recente), cobertura (registros processados ÷ esperados), correção (reconciliação), tempo até conclusão | Lote: momento do último sucesso (V-11) |
| Fila / assíncrono | Idade da mensagem mais antiga, tempo ponta a ponta, taxa de mensagens em dead-letter | Latência HTTP de aceite não representa conclusão |

## Aritmética do error budget

Budget = 100% − meta. Tempo equivalente de indisponibilidade = (1 − meta) × janela.

| Meta | Janela | Budget | Equivalente de indisponibilidade |
| --- | --- | --- | --- |
| 99% | 30 d | 1% | 7,2 h (30×24×0,01) |
| 99,5% | 30 d | 0,5% | 3,6 h |
| 99,9% | 30 d | 0,1% | **43,2 min** (30×24×60×0,001) |
| 99,95% | 30 d | 0,05% | 21,6 min |
| 99,99% | 30 d | 0,01% | 4,32 min |

Em termos de requisições: com 10 milhões de requisições válidas em 30 dias e meta 99,9%, o budget é 10.000 requisições ruins. Se 3.500 já foram gastas em 8 dias, o consumo é 35% do budget em 27% da janela (8/30): ritmo acima do sustentável (burn ≈ 1,3). Refaça a conta com dados reais; os números são de exemplo.

Equivalente de tempo vale só se o tráfego for uniforme; use proporção de requisições como definição, tempo como intuição.

## Política de error budget

Fonte: V-02 (Workbook "Implementing SLOs"). Template em [politica-error-budget.md](../assets/templates/politica-error-budget.md). Elementos exigidos pela fonte (Verificado): consumo acompanhado diária ou semanalmente; ações definidas para o esgotamento e quem as executa; autores, revisores e aprovadores listados; caminho de escalonamento para divergências.

Exemplos de ações (Suposição de aplicabilidade; cada organização escolhe): em 50% consumido, revisar as causas principais; em 75%, priorizar bugs de confiabilidade no próximo ciclo; ao esgotar, pausar features e congelar mudanças não essenciais até o budget se recuperar. Quando a causa está numa dependência de outro time, a política deve registrar a decisão tomada (congelar ou não) e por quê.

Aprovação: produto, desenvolvimento e operação assinam. Sem acordo, revise SLIs e metas em vez de impor a política.

## Caso: 202 aceito, fila parada

Fonte: brain-of-agent `entrega-e-operacao.md` (conteúdo próprio, MIT). Um endpoint devolve 202 em 50 ms, mas o consumidor da fila parou. O SLI de latência HTTP continua verde e os usuários não recebem o resultado. Meça também:

- tempo até conclusão (do evento aceito ao efeito visível), com percentis;
- idade da mensagem mais antiga na fila;
- proporção de pedidos concluídos dentro do prazo prometido.

Cada alerta deve ter dono e ação de resposta. SLO orienta decisão e custo conforme a necessidade do produto; 99,99% não é meta universal.

## Plantão e toil

Fonte: V-24 (SRE Book "Being On-Call", Classe A). Valores do Google; calibre para o seu contexto (Suposição de aplicabilidade).

| Parâmetro | Valor de referência |
| --- | --- |
| Tempo em engenharia | ≥ 50% |
| Tempo de plantão | ≤ 25% |
| Equipe para 24x7 em um site | ≥ 8 engenheiros (dois sites: ≥ 6 em cada) |
| Esforço por incidente | ≈ 6 h (investigar, mitigar, escrever postmortem) |
| Incidentes por turno de 12 h | ≤ 2 |
| Páginas por dia (mediana) | próxima de 0 |
| Alertas por incidente | tender a 1 |

Uso prático: se o histórico mostra 40 páginas por semana e quase todas sem ação (cenário do eval `alerta-cpu-vs-burn-rate`), o problema é de alerta, não de pessoas. Siga [alertas-e-sinais.md](alertas-e-sinais.md).

## Erros comuns ao propor SLOs

- Aceitar "100% de disponibilidade" ou "tempo médio < 200 ms" do produto sem converter: explique o custo e proponha percentil com meta < 100%.
- SLI de HTTP 2xx tratado como sucesso de negócio: pedido aceito mas não processado conta como bom.
- SLO de dependência apresentado como SLO do usuário: o usuário percebe a composição.
- Meta copiada de exemplo (99,9%, 300 ms) sem linha de base (Suposição; SAP-18 em [padroes-e-antipadroes.md](padroes-e-antipadroes.md)).
- Janela do SLO diferente da janela do alerta sem refazer a conta de burn rate.
