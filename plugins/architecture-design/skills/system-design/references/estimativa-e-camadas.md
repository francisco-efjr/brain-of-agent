# Estimativa de ordem de grandeza e camadas L0 a L7

Sumário: 1. Fórmulas · 2. Lei de Little · 3. Fatores de pico e margens · 4. Camadas L0 a L7 · 5. Perguntas de clarificação · 6. Armadilhas

Validado em 2026-10-10 (modelos Claude 4.x/5.x). Fontes: V-41 (laço de seis passos, camadas L0 a L7, conta no texto; MIT; números dele são regra de bolso, Suposição), V-42, V-38. As fórmulas de capacidade são matemática estável (Verificado por conta). Todos os valores numéricos de exemplo são Suposição do exemplo, nunca fato sobre um sistema real. Conferir limites de provedores e de serviços gerenciados na documentação do fornecedor (Não verificável aqui).

## 1. Fórmulas

| Grandeza | Fórmula | Observação |
| --- | --- | --- |
| QPS médio | eventos por dia / 86.400 | 1 milhão por dia ≈ 11,6 por segundo |
| QPS de pico | QPS médio x fator de pico | Fator de pico é Suposição; use o pico informado pelo usuário quando existir |
| Armazenamento | itens por dia x bytes por item x dias de retenção x fator de replicação | Inclua índices (Suposição: +30% a +100%, depende do esquema) |
| Banda de saída | QPS de pico x bytes por resposta | Converta bytes/s para bits/s multiplicando por 8 |
| Concorrência em voo | taxa de chegada x tempo de serviço (lei de Little) | Define pool de conexões, threads, workers |
| Nós necessários | pico / capacidade medida por nó, com margem | Sem benchmark, a capacidade por nó é Suposição |
| Backlog de fila em queda de dependência | taxa de chegada x duração da queda | Define tamanho de fila e retenção |

Regras de apresentação: escreva "premissa -> conta -> resultado" em linhas curtas; arredonde para 1 ou 2 algarismos significativos; marque cada premissa; diga qual premissa mais move o resultado ("o resultado dobra se o tamanho médio dobrar").

## 2. Lei de Little

L = λ x W. Número médio de itens no sistema (L) = taxa de chegada (λ) x tempo médio de permanência (W). Uso prático: com 833 requisições por segundo e 0,2 s por chamada ao provedor, há cerca de 167 chamadas simultâneas em voo (833 x 0,2). Divida pela concorrência de cada processo para estimar processos, e confirme os limites de conexões do provedor e do banco.

## 3. Fatores de pico e margens

- Pico/média típico varia muito por domínio (Suposição): tráfego B2B interno costuma ficar baixo; campanhas, notificações em massa e eventos de venda podem ficar em dezenas de vezes. Prefira o pico informado ou uma série real de métricas.
- Margem de capacidade: duplicar o pico calculado é um ponto de partida defensável (Suposição); ajuste ao custo da falha e à elasticidade da plataforma.
- Tráfego retentado soma carga: com falha transitória de p% e até k tentativas extras, a carga extra pode chegar a p x k (ex.: 5% x 2 = +10%). Com retry em várias camadas a amplificação é multiplicativa: 5 camadas com 3 tentativas cada resultam em 3^5 = 243 chamadas ao fundo por requisição original (exemplo do artigo da AWS Builders' Library, N-01; Inferido: não passou por segundo validador). Por isso retry em uma só camada.

## 4. Camadas L0 a L7 (checklist de design; V-41)

| Camada | Pergunta de design | Decisões típicas | Skill ou referência |
| --- | --- | --- | --- |
| L0 Enquadramento | Quais são os requisitos, o escopo e as metas de nível de serviço? | Requisitos com número, fora de escopo, SLO | este arquivo, seção 5 |
| L1 Borda | Como o tráfego entra e é controlado? | Balanceador, autenticação, limite de taxa, CDN | `backend-api`, `devops-cloud-infra` |
| L2 Serviços | Quais serviços e módulos existem e por quê? | Monólito modular vs serviços, fronteiras | skill `decomposition` |
| L3 Estado | Onde o dado mora e como é lido? | Banco, cache, armazenamento de objetos, particionamento | skill `adr` para a escolha; `database-data-modeling` para o modelo |
| L4 Assíncrono | O que pode sair do caminho síncrono? | Filas, retentativas, dead-letter queue | skill `resilience-and-consistency` |
| L5 Correção | Quais invariantes devem valer e sob falha? | Idempotência, outbox, concorrência, consistência | skill `resilience-and-consistency` |
| L6 Operação | Como saberemos que funciona e como mudamos com segurança? | Observabilidade, deploy, rollback, segurança, custo | `sre-observability`, `security-appsec` |
| L7 Crescimento | O que muda se o volume dobrar ou decuplicar? | Particionamento, extração de módulo, gatilhos de revisão | skill `decomposition`, ADR com gatilhos |

Percorra de L0 a L7 anotando "não aplicável (motivo)" onde for o caso; pular uma camada em silêncio é onde nascem as falhas de design.

## 5. Perguntas de clarificação (no máximo 5, uma por vez quando bloqueiam)

1. **Quem e quanto:** quantos usuários ou chamadores, qual pico, qual crescimento esperado em 12 meses?
2. **Correção:** o que não pode ser perdido, duplicado ou reordenado? Qual a consequência de um duplicado?
3. **Latência e disponibilidade:** qual o tempo de resposta aceitável e quanto tempo fora do ar é tolerável por mês?
4. **Restrições:** tamanho e experiência do time, orçamento, stack existente, prazo, requisitos regulatórios.
5. **Dependências e falhas:** quais serviços externos entram, que limites de taxa eles têm, o que é aceitável degradar?

## 6. Armadilhas

- Estimativa com falsa precisão ("843,17 QPS"): arredonde.
- Tamanho médio de item ignorando índices, replicação e retenção: subestima armazenamento em 2x ou mais.
- Dimensionar pela média e não pelo pico: filas e pools quebram no pico.
- Usar número de blog ou de fornecedor como fato: sem fonte observada, é Suposição (AP-20).
- Confundir capacidade teórica de um serviço gerenciado com o limite contratado: confira a documentação do fornecedor (Não verificável aqui).
