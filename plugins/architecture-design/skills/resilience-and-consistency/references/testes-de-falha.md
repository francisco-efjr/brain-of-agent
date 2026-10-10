# Testes de falha para resiliência e consistência

Sumário: 1. Princípio · 2. Matriz de testes · 3. Exemplo de teste de duplicata · 4. Testes de resiliência de chamada · 5. O que um teste de falha não prova · 6. Gotchas

Validado em 2026-10-10. Base: propriedades de V-33 (idempotência), V-34 (outbox), V-35 (saga), V-30 e V-31 (breaker, retry); testes given-when-then de V-37; princípio "dar ao agente um meio executável de verificação" (V-03). Os nomes de teste e o pseudo-código são ilustrativos. Comandos reais dependem do projeto: descubra-os no repositório (scripts do gerenciador de pacotes, Makefile, CI) ou pergunte; não invente comando.

## 1. Princípio

Cada propriedade prometida pelo design precisa de um teste que a quebre se o mecanismo for removido (vermelho confirmado). Sem esse teste, "o design é idempotente" é Suposição, não Verificado.

## 2. Matriz de testes

| Propriedade | Cenário | Como simular | Resultado esperado |
| --- | --- | --- | --- |
| Idempotência do consumidor | Mesma mensagem entregue 2 vezes | Chamar o handler duas vezes com o mesmo `message_id` | Um só efeito de negócio; segunda chamada confirma (ack) sem efeito |
| Idempotência sob concorrência | Duas entregas simultâneas | Duas threads/processos com a mesma chave | Um vencedor (unicidade do banco); o outro descarta |
| Atomicidade marcador + efeito | Falha após o efeito, antes do COMMIT | Injetar exceção entre efeito e commit | Nada persistido (nem marcador, nem efeito); a reentrega processa normalmente |
| Outbox: sem perda | Queda entre COMMIT e publicação | Matar o relay após o commit do estado | Evento permanece na outbox e é publicado depois |
| Outbox: duplicata a jusante | Publicou e caiu antes de marcar | Matar o relay entre publicar e marcar | Evento publicado 2 vezes; o consumidor aplica 1 vez |
| Aceitação desconhecida | Timeout após o provedor processar | Provedor falso que processa e não responde | Um só efeito externo (chave de idempotência ou consulta de estado) |
| Compensação | Passo 3 falha definitivamente | Falha injetada no passo 3 | Passos 1 e 2 compensados (ou pivô tratado) e estado final consistente |
| Compensação que falha | Estorno devolve erro | Falha injetada na compensação | Tentativas repetidas, alerta e item na fila de intervenção; saga não fica "verde" silenciosa |
| Passo pós-pivô repetido | Reentrega do passo após o pivô | Chamar duas vezes | Mesmo resultado, sem efeito duplo |
| DLQ e reprocessamento | Reprocessar mensagem antiga | Reenviar da DLQ após o TTL do marcador | Política explícita: marcador ainda vale, ou duplicata é aceita por decisão registrada |
| Mensagens fora de ordem | `Atualizado` chega antes de `Criado` | Inverter a ordem | Tratado por versão ou sessão; sem estado inválido |

## 3. Exemplo de teste de duplicata (pseudo-código)

```text
given um consumidor 'faturamento' e uma mensagem m1 (pedido o1, valor 100)
when  o handler processa m1
and   o handler processa m1 novamente (mesmo message_id)
then  existe exatamente 1 cobrança para o1
and   a tabela inbox contém 1 linha (faturamento, m1)
and   as duas chamadas devolveram sucesso ao broker (ack)
```

Variante de falha: injete exceção depois de gravar a cobrança e antes do COMMIT; ao reentregar m1, a cobrança deve existir exatamente uma vez. A lógica equivalente foi exercitada com sqlite3 em 2026-10-10 (Verificado para a lógica; o teste do projeto real precisa rodar no ambiente do usuário).

## 4. Testes de resiliência de chamada

- **Retry em uma camada:** contar quantas vezes o provedor falso é chamado para uma falha transitória: o esperado é no máximo `max_attempts`, não `max_attempts` por camada.
- **Jitter:** com gerador aleatório injetado, verificar que a espera fica entre 0 e `min(teto, base x 2^n)` e que o prazo total é respeitado.
- **Breaker:** após o limiar de falhas, as chamadas passam a falhar rápido sem tocar o provedor; após o tempo aberto, poucas chamadas de teste; uma falha reabre; sucesso fecha.
- **Bulkhead:** saturar o pool da dependência A e verificar que a dependência B continua respondendo dentro do SLA.
- **Timeout:** o timeout do chamador é menor que o do chamador acima na cadeia (orçamento de tempo decrescente).

## 5. O que um teste de falha não prova

- Com broker em memória ou dublê, o comportamento real de redelivery, particionamento e ordem não foi exercitado: declare isso (Não verificável).
- Sucesso em um ambiente de teste não prova comportamento sob carga de produção: use ambiente de carga do time.
- Teste verde com asserção fraca não prova nada (por exemplo, afirmar apenas "não lançou exceção"): exija a asserção da propriedade (contagem de efeitos).

## 6. Gotchas

- Teste que usa `sleep` fixo para esperar a outbox fica instável; use espera por condição com limite.
- Injetar falha em mock em vez do banco real esconde problemas de transação: prefira banco real de teste para os testes de atomicidade.
- Cobrir só o caminho feliz de redelivery (sem crash no meio) é o erro mais comum.
