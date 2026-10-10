# Decisões e trade-offs: método leve

Validado em 2026-10-10 · Modelo-alvo: Claude 4.x/5.x · Rótulos: Verificado, Inferido, Suposição, Não verificável.
Fontes: ATAM da SEI/CMU (N-08, vocabulário, não o método de 3 a 4 dias), pilares do Azure Well-Architected (N-07), OWASP Threat Modeling Cheat Sheet (N-06, destilado; licença CC BY-SA 4.0 impede mistura literal), plan-eng-review do gstack (V-19, MIT, só o processo), V-43, V-10, brain-of-agent (MIT).
Declaração obrigatória: isto é uma versão leve e não é uma avaliação ATAM nem uma auditoria Well-Architected (Inferido, conflito C15).

## Sumário

1. Quando usar este método
2. Passo 0: desafio de escopo
3. Atributos de qualidade como cenários
4. Árvore de utilidade enxuta
5. Riscos, não-riscos, pontos de sensibilidade e de trade-off
6. Cinco pilares como lente de tensões
7. Modelo de decisão D-n
8. Comparação ponderada (opcional)
9. Perguntas de pensamento arquitetural (adaptadas do gstack)
10. Arquiteto cético e pré-mortem
11. Modelagem de ameaças leve
12. Reversibilidade e confiança
13. Exemplo completo
14. Gotchas

## 1. Quando usar

Decisão que afeta estrutura, atributo de qualidade ou é cara de reverter (critério de V-12). Para decisão pequena e reversível, não monte tabela: decida e siga.

## 2. Passo 0: desafio de escopo (V-19, processo do gstack)

Antes de comparar opções, responda por escrito:

1. Existe solução menor que atende ao requisito? Qual?
2. O que já existe no repositório que resolve parte do problema (reutilizar antes de criar)?
3. O que dá para não construir agora, sem prejuízo do objetivo?
4. Qual o menor diff que entrega valor verificável?

Se a resposta 1 for "sim", a primeira opção da tabela é ela, e "não mudar nada" também entra.

## 3. Atributos de qualidade como cenários (vocabulário ATAM, N-08)

Um atributo vago ("o sistema deve ser rápido") não decide nada. Escreva cenários mensuráveis:

| Campo | Pergunta | Exemplo |
| --- | --- | --- |
| Estímulo | O que acontece? | 5.000 pedidos por minuto no pico da Black Friday |
| Ambiente | Em que condição? | Operação normal, uma réplica fora |
| Resposta | O que o sistema faz? | Confirma o pedido e enfileira o pagamento |
| Medida | Como se verifica? | p95 abaixo de 400 ms, zero pedido perdido |

Atributos comuns: desempenho, disponibilidade, consistência, segurança, modificabilidade, custo operacional, observabilidade. A norma ISO/IEC 25010 e o arc42 são citados em VALIDATED como lacuna (não lidos): use os nomes só como vocabulário. Número sem fonte do usuário entra como Suposição, com dono para confirmar.

## 4. Árvore de utilidade enxuta

Liste de 3 a 6 cenários, ordene por importância para o negócio (A/M/B) e por dificuldade técnica (A/M/B). Os cenários A/A guiam o desenho; os B/B ficam fora do escopo da decisão.

```text
Utilidade
├── Desempenho
│   └── Checkout p95 < 400 ms no pico            (importância A, dificuldade M)
├── Consistência
│   └── Nenhum pedido pago duplicado             (importância A, dificuldade A)
└── Modificabilidade
    └── Novo meio de pagamento em < 1 semana     (importância M, dificuldade B)
```

## 5. Riscos, não-riscos, pontos de sensibilidade e de trade-off (N-08)

Para cada cenário A/A, depois de escolher uma abordagem:

- **Risco:** decisão que pode causar problema relevante ("sem dedupe no consumidor, duplicata gera cobrança dupla").
- **Não-risco:** decisão que sustenta o cenário e foi verificada ("restrição de unicidade na chave de idempotência").
- **Ponto de sensibilidade:** parâmetro cuja mudança afeta muito um atributo ("tamanho do pool de conexões afeta p95").
- **Ponto de trade-off:** parâmetro que melhora um atributo e piora outro ("TTL longo do cache melhora latência e piora obsolescência").

Saída: tabela de quatro colunas, cada linha com `arquivo:linha` ou "Suposição".

## 6. Cinco pilares como lente (N-07; ms.date 2025-01-22)

Pilares do Azure Well-Architected: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency. Cada um tem uma página de trade-offs na fonte. Use como lista de verificação de lacunas, não como certificação. Exemplos de tensões típicas (Inferido a partir do conhecimento geral; confirme na página de cada pilar):

| Ganho em | Custa em | Exemplo |
| --- | --- | --- |
| Reliability (réplicas, multi-região) | Cost Optimization | Capacidade ociosa para tolerar falha |
| Performance (cache) | Reliability/consistência | Dado obsoleto, stampede |
| Security (isolamento, criptografia) | Performance, Operational Excellence | Latência extra, rotação de chaves |
| Operational Excellence (observabilidade) | Cost | Armazenamento e ingestão de telemetria |

## 7. Modelo de decisão D-n (processo de V-19, reescrito)

Cada decisão que o humano precisa tomar segue este molde (template `decision-brief.md`):

```text
D-1  Título curto
Problema (linguagem simples): ...
Se errarmos: ... (impacto e reversibilidade)
Recomendação: Opção B, confiança média, porque ...
Opções (2 a 4; cada uma com >= 2 prós e >= 1 contra):
  A. Não mudar nada      + ...  + ...   - ...
  B. ...                 + ...  + ...   - ...
  C. ...                 + ...  + ...   - ...
Dono humano da decisão: [nome ou "a definir"]
Pergunta exata: "Aprovar B?" 
```

Regras: no máximo 4 opções; "não mudar nada" sempre presente; se a decisão for de preferência humana, devolva as opções e pergunte em vez de decidir (V-10); terminar com tabela de decisões pendentes.

## 8. Comparação ponderada (opcional, Suposição)

Use só quando houver 3 ou mais opções e critérios claros. Pesos somam 100; notas de 1 a 5; justifique cada nota em uma frase. Pesos e notas são Suposições do autor, não medições: apresente a soma como ajuda à conversa, nunca como veredito.

| Critério (peso) | A. Não mudar | B. Monólito modular | C. Serviço separado |
| --- | --- | --- | --- |
| Custo operacional (30) | 5 | 4 | 2 |
| Autonomia de deploy (25) | 1 | 3 | 5 |
| Risco de migração (25) | 5 | 4 | 2 |
| Fit com o time (20) | 4 | 4 | 2 |

Se o ranking mudar com pequenas variações de peso, a decisão é sensível ao julgamento: diga isso.

## 9. Perguntas de pensamento arquitetural

Adaptadas do gstack `plan-eng-review` (MIT, Garry Tan; só o processo, reescrito como perguntas; o original atribui cada ideia a autores de livros e artigos, que não foram relidos aqui):

1. **Raio de impacto:** qual é o pior dano se isto falhar, para sistemas e para pessoas?
2. **Tecnologia entediante:** esta escolha usa tecnologia comprovada ou gasta uma "ficha de inovação" que o time pode não ter orçamento para suportar?
3. **Mudança incremental:** existe caminho strangler ou canário em vez de grande troca?
4. **Sistemas acima de heróis:** funciona para alguém cansado às 3 da manhã, com alerta e runbook?
5. **Reversibilidade:** flag ou rollout gradual tornam o erro barato de desfazer?
6. **Lei de Conway:** a fronteira técnica combina com a fronteira de equipe?
7. **Complexidade essencial ou acidental:** o problema é real ou criado por nós?
8. **Facilite a mudança primeiro:** refatore antes de mudar comportamento e mantenha os dois commits separados?

As preferências de engenharia do gstack (abstração mínima, diff pequeno, testes por comportamento, explícito acima de esperto) entram como Suposição: são gosto de um autor, não evidência.

## 10. Arquiteto cético e pré-mortem

**Arquiteto cético** (V-43; ensaio de opinião, sem medição): antes de propor, faça até cinco perguntas sobre escala, consistência, time e modos de falha (uma por vez quando alguma bloquear). Mostre a opção mais simples que atende. Diga o que você não recomenda construir e por quê (Inferido: não vem do ensaio). Termine com a decisão pendente e o dono humano. Trate sugestões do modelo como as de um júnior confiante: o humano decide.

**Pré-mortem de 12 meses** (Inferido, construção própria): "Suponha que esta decisão falhou em 12 meses. Liste três causas prováveis e o sinal precoce observável de cada." Use para decisões de alto custo; peça um sinal mensurável por causa (métrica, alerta, incidente).

## 11. Modelagem de ameaças leve (N-06)

Quando houver fronteira de confiança (internet, parceiros, outro time, ferramenta de agente), responda às quatro perguntas do OWASP Threat Modeling Cheat Sheet:

1. O que estamos construindo? (diagrama de contêineres com fronteiras marcadas)
2. O que pode dar errado? (STRIDE por fluxo que cruza a fronteira)
3. O que vamos fazer a respeito? (mitigar, transferir, aceitar, eliminar)
4. Fizemos um bom trabalho? (revisão e teste do que foi decidido)

STRIDE (conhecimento geral, Inferido): Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Saída: tabela fluxo, ameaça, mitigação, dono. Isto é modelagem leve de arquitetura; pentest, SAST/DAST e hardening pertencem a `/security-appsec:playbook`.

## 12. Reversibilidade e confiança

| Confiança | Quando | Consequência |
| --- | --- | --- |
| Alta | Evidência direta (medição, código lido, requisito explícito) e decisão reversível | Decidir e registrar |
| Média | Evidência parcial ou premissa de carga | Decidir com experimento ou gatilho de reavaliação |
| Baixa | Premissas não testadas ou decisão cara de reverter | Pesquisar mais ou prototipar (PoC) antes de decidir; ADR com data de revisão |

Os limiares numéricos 85% e 66% do fluxo spec-driven (V-18) não têm fonte primária: use as faixas qualitativas e, se o time quiser números, trate-os como configuração do time (Suposição).

## 13. Exemplo completo (resumido)

Pedido: "Time de 4 devs, monólito Rails, CTO quer microsserviços para escalar."

- Passo 0: qual módulo seria o primeiro a extrair, e por quê? Resposta do time: "faturamento, por causa de deploys frequentes que travam o resto". Isso é um motivo nomeado; falta métrica (Suposição: dois deploys por semana bloqueados).
- Cenário A/A: "deploy do faturamento sem janela conjunta" (medida: zero deploys coordenados em 30 dias).
- Opções: A não mudar nada; B monólito modular com fronteira de faturamento verificada em CI; C extrair faturamento como serviço.
- Recomendação: B, confiança média; gatilho de reavaliação: se após 60 dias o acoplamento de mudança entre faturamento e o resto continuar acima do limiar combinado (Suposição), propor C.
- Dono humano: o responsável técnico do time. Pergunta: "Aprovar B e o teste de fronteira no CI?"

## 14. Gotchas

- ATAM completo exige avaliadores treinados e dias de trabalho; este método é uma estrutura de conversa. Declare isso no relatório.
- O ensaio de V-43 não menciona pré-mortem nem "o que não construir"; ambos são construção própria deste plugin (Inferido).
- Tabelas ponderadas passam falsa precisão: exiba como apoio e mostre a sensibilidade aos pesos.
- STRIDE e as quatro perguntas aqui são resumo; para ameaças reais de um sistema sensível, acione `/security-appsec:playbook`.
- As oito perguntas da seção 9 são heurísticas de um autor; use-as para provocar a conversa, não como critério de aprovação.
