# Checklists de padrões de resiliência e consistência

Sumário: 1. Retry · 2. Circuit breaker · 3. Bulkhead · 4. Consumidor idempotente · 5. Transactional outbox · 6. Saga · 7. CQRS · 8. Event sourcing · 9. Como as peças se combinam · 10. Gotchas

Validado em 2026-10-10 (modelos Claude 4.x/5.x). Fontes: Microsoft Azure Architecture Center (classe A; destilado com redação própria): Retry V-31 (ms.date 2024-07-18, atualizado 2025-12-09), Circuit Breaker V-30 (2025-02-05, atualizado 2026-09-26), Bulkhead V-32 (2026-03-19, atualizado 2026-09-19), Idempotent Consumer V-33 (2026-08-13, atualizado 2026-09-05), Transactional Outbox V-34 (2026-02-23, atualizado 2026-09-25), Saga V-35 (2025-02-25, atualizado 2026-06-03), CQRS V-36 (2025-02-20, atualizado 2026-09-25), Event Sourcing V-37 (2026-03-27, atualizado 2026-09-25). Jitter e retry multiplicativo: AWS Builders' Library, N-01 (reconferida na página em 2026-10-10: 243x e jitter consistente por host). Conferir as páginas atuais antes de decisões caras; as páginas são atualizadas com frequência.

Resposta de cada item: sim, não ou Não aplicável (com motivo).

## 1. Retry (V-31, N-01)

Quando usar: falha transitória (rede, 503, 429, timeout) em operação idempotente. Quando NÃO usar: falha permanente (validação, autorização), operação não idempotente, ou quando mais capacidade é a solução (retry não substitui escala).

- [ ] A falha é transitória? (4xx de validação nunca melhora com repetição.)
- [ ] A operação é idempotente ou carrega chave de idempotência?
- [ ] O SDK ou cliente já repete? (Evite repetir por cima.)
- [ ] Só uma camada repete (a mais baixa que falha rápido)? Camadas acima falham sem repetir.
- [ ] Limite de tentativas definido (ex.: 3 a 5; Suposição, ajuste ao custo da latência) e prazo total (deadline) respeitado.
- [ ] Atraso exponencial com variação aleatória (jitter): por exemplo, espera aleatória entre 0 e `min(teto, base x 2^tentativa)`. Para trabalhos agendados, um deslocamento consistente por host pode ser melhor que aleatório (N-01).
- [ ] Respeita `Retry-After` quando o servidor o envia.
- [ ] Tentativas iniciais registradas como informação e só a última falha como erro; métrica de tentativas por chamada.
- [ ] Erro recorrente abre discussão de capacidade ou de breaker, em vez de mais retries.

Amplificação: 5 camadas com 3 tentativas cada = 3^5 = 243 chamadas ao fundo por requisição original (exemplo de N-01).

## 2. Circuit breaker (V-30)

Quando usar: chamadas a dependência remota que pode ficar lenta ou fora, onde falhar rápido protege o chamador. Quando NÃO usar: estado local em memória; arquiteturas de mensagens com DLQ (isolamento e retry já embutidos); plataforma que recupera sozinha (service mesh, health checks); substituir tratamento de exceção de negócio.

- [ ] Estados definidos: fechado, aberto, meio-aberto.
- [ ] Limiar de falhas e janela de tempo definidos (contagem por janela).
- [ ] Tempo em estado aberto e política de crescimento (ex.: aumentar a cada reabertura).
- [ ] Número limitado de chamadas de teste no meio-aberto; uma falha reabre.
- [ ] Fallback definido (valor padrão, cache, erro explícito).
- [ ] Evento e alerta a cada transição de estado.
- [ ] Reset manual e abertura forçada disponíveis para operação.
- [ ] Um breaker por dependência ou por fatia (shard), não um global.
- [ ] 429 e 503 podem abrir imediatamente (a fonte cita esse caso).
- [ ] O timeout do chamador é curto? Timeout longo anula a proteção.
- [ ] Combinado com retry: o retry para quando o breaker indica falha não transitória.
- [ ] É realmente necessário aqui, ou broker/mesh já cobre?

## 3. Bulkhead (V-32)

Quando usar: uma dependência lenta pode esgotar threads, conexões ou memória compartilhadas e derrubar chamadas não relacionadas. Quando NÃO usar: uso menos eficiente de recursos é inaceitável ou a complexidade não se justifica.

- [ ] Quais dependências podem esgotar um recurso compartilhado?
- [ ] Pool, fila ou processo separado por dependência crítica (ou por consumidor, ou por tenant).
- [ ] Tamanho de cada pool vem de número medido (concorrência em voo = taxa x latência).
- [ ] A plataforma já oferece o limite (limites de API gateway, cotas do banco, limites do orquestrador)? Prefira-o a recriar em código.
- [ ] Partições alinhadas aos bounded contexts, quando houver DDD.
- [ ] Alerta e SLA por partição.
- [ ] Custo de menor utilização aceito e documentado.
- [ ] Cargas de inferência de IA pedem limites rígidos por cota (V-32).

## 4. Consumidor idempotente (V-33)

Contexto: exatamente-uma-vez ponta a ponta é impraticável; at-least-once mais consumidor que ignora duplicata é efetivamente uma vez. Quando NÃO usar o mecanismo pesado: a operação já é naturalmente idempotente (upsert por chave de negócio, definir valor em vez de incrementar).

- [ ] Chave estável: id da mensagem ou chave de negócio; nunca CorrelationId nem id de entrega do broker.
- [ ] Chave composta com identidade do consumidor quando vários consumidores compartilham a tabela.
- [ ] A operação é naturalmente idempotente? Se sim, prefira isso ao marcador.
- [ ] Marcador e efeito na mesma transação do banco (padrão inbox).
- [ ] Restrição de unicidade no banco como árbitro de concorrência (duas entregas simultâneas).
- [ ] Efeito externo (e-mail, cobrança): estados "em andamento" e "concluído", com tratamento do caso de crash no meio.
- [ ] Retenção do marcador maior que a janela de redelivery, incluindo reenvios da DLQ.
- [ ] Detecção de duplicata do broker não substitui o consumidor.
- [ ] Chave propagada aos serviços chamados.
- [ ] Ordem tratada por sessão, partição ou versão quando importa.
- [ ] Métrica de duplicatas e chave presente nos logs.

## 5. Transactional outbox (V-34)

Quando usar: é preciso atualizar estado e publicar evento sem dual write. Quando NÃO usar: não há consumidor externo do evento; o broker e o banco participam da mesma transação suportada e testada (raro); a perda ocasional é aceitável por decisão de negócio.

- [ ] Estado e evento gravados **na mesma transação** (mesmo contêiner e partição lógica, em stores como Cosmos DB; mesma transação relacional em SQL).
- [ ] Evento com id estável (para deduplicação a jusante).
- [ ] Publicador assíncrono que marca como publicado (coluna "processado" em SQL; change feed em Cosmos DB) e retoma após falha.
- [ ] Ordem preservada por agregado; atenção a múltiplos publicadores concorrentes (ordem quebra sem particionar por agregado).
- [ ] TTL ou limpeza com margem de dias (a fonte usa 10 dias no exemplo).
- [ ] Consumidor idempotente (item 4): publicar duas vezes é esperado.
- [ ] Biblioteca testada em vez de código caseiro (a fonte cita NServiceBus e MassTransit; o exemplo dela não é para produção).
- [ ] Nada promete "elimina duplicatas": a outbox evita **perda** por dual write.

## 6. Saga (V-35)

Quando usar: transação de negócio que atravessa serviços com bancos próprios, tolerando consistência eventual e compensação. Quando NÃO usar: transações fortemente acopladas, compensação exigida em participantes anteriores, ou dependências cíclicas.

- [ ] Cada passo tem transação local e uma compensação (ou é pivô ou pós-pivô).
- [ ] Passo pivô identificado (ponto sem retorno); passos após o pivô são idempotentes e repetíveis até concluir.
- [ ] Coreografia só com poucos serviços; orquestração para fluxos complexos (e protegê-la como ponto único de falha).
- [ ] Bloqueio semântico em registros em edição (ex.: estado `pendente`).
- [ ] Anomalias tratadas: atualização perdida, leitura suja, leitura não repetível (contramedidas: bloqueio semântico, atualizações comutativas, visão pessimista, reler antes de agir, versionar, concorrência por risco).
- [ ] Estado da saga monitorado (instâncias presas, tempo máximo).
- [ ] Plano para compensação que falha (repetir, alertar, intervenção humana).
- [ ] Mensagens da saga idempotentes (item 4).

## 7. CQRS (V-36)

Quando usar: leitura e escrita com escala ou modelos diferentes, regras que pedem modelo de escrita próprio, interface orientada a tarefas, colaboração intensa ou times separados. Quando NÃO usar: domínio simples, CRUD suficiente.

- [ ] Leitura e escrita têm escala diferente?
- [ ] As regras justificam um modelo de escrita próprio?
- [ ] A interface é orientada a tarefas (comandos de negócio, não atualização de campos)?
- [ ] O time aceita consistência eventual e dado obsoleto na tela?
- [ ] Há mecanismo de sincronização confiável (outbox + consumidor idempotente)?
- Se as duas primeiras forem "não", não aplique. Comece separando modelos no mesmo banco antes de separar bancos.

## 8. Event sourcing (V-37)

Quando usar: auditoria, reconstrução histórica ou fluxos temporais são requisitos centrais (ledger de pagamentos, por exemplo). Quando NÃO usar: perfil de usuário, cadastros simples. A fonte avisa: complexo, caro de adotar e de abandonar, raramente necessário.

- [ ] O benefício (auditoria, histórico) justifica o custo?
- [ ] Eventos capturam intenção, não só estado resultante.
- [ ] Estratégia de evolução de esquema definida antes do primeiro evento (versão no evento, deserialização tolerante, upcasting).
- [ ] Concorrência otimista por fluxo (stream) e ordem por entidade.
- [ ] Snapshots quando o fluxo cresce (otimização, não substituto do log).
- [ ] Dados pessoais fora do log, ou crypto-shredding, por causa do direito ao esquecimento.
- [ ] Handlers de projeção idempotentes (item 4); cuidado com laços circulares.
- [ ] Testes given-when-then.
- [ ] Aplicado só à parte do sistema que precisa; event store não é broker.

## 9. Como as peças se combinam

| Problema | Combinação | Propriedade que se obtém |
| --- | --- | --- |
| Dual write (banco + broker) | Outbox + consumidor idempotente | Sem perda de evento; duplicata neutralizada a jusante |
| Chamada a provedor instável | Timeout curto + retry em uma camada com jitter + breaker + bulkhead | Falha rápida, sem amplificação, isolamento |
| Fluxo de negócio entre serviços | Saga (orquestrada se complexa) + passos idempotentes + outbox em cada serviço | Consistência eventual com compensação |
| Leitura em escala | CQRS com projeção alimentada por eventos (outbox) + cache-aside se um número exigir | Escala de leitura com obsolescência declarada |

## 10. Gotchas

- "Exatamente uma vez" é promessa de marketing quando atravessa fronteiras; descreva o mecanismo (at-least-once + idempotência).
- Marcador de idempotência com TTL menor que o reprocessamento da DLQ aceita duplicata antiga como nova.
- Breaker aberto sem fallback só transforma lentidão em erro: defina o que o usuário vê.
- Os limiares e tempos citados como exemplo (tentativas, TTL, janelas) são Suposição: ajuste com medições.
