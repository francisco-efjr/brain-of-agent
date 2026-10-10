# Casos de borda de firmware: catálogo e nomes de teste

Uso: consulta da skill `firmware-test-host`, passo 5. Cada linha é um defeito que só aparece em campo ou na bancada se o teste de host não o pegar antes. Fontes lidas em 2026-10-10: V-16 (testes de lógica no host, fault handler), V-30 a V-33 e V-35 (erros de barramento e rede), V-36 a V-38 (frameworks), V-12 (corrida com interrupção), V-39 (reset após deep sleep). Itens sem fonte lida são Inferido (conhecimento estável do domínio).

Sumário: [Como escolher](#como-escolher) · [Catálogo](#catálogo) · [Simular interrupção no host](#simular-interrupção-no-host) · [Aritmética de tempo](#aritmética-de-tempo) · [Queda de energia no meio de uma escrita](#queda-de-energia-no-meio-de-uma-escrita) · [Nomear e ordenar](#nomear-e-ordenar)

## Como escolher

1. Liste os estados e as entradas do módulo; cada fronteira (vazio, cheio, máximo, zero, um, estouro) vira ao menos um caso.
2. Para cada chamada que cruza a interface de hardware, liste as respostas possíveis (sucesso, NACK, timeout, resposta curta, dado inválido) e cubra todas.
3. Para tudo que depende de tempo, use um relógio injetado (função devolvendo o "agora" que o teste controla); nunca durma no teste.
4. Priorize pelo custo da falha em campo: perda de dado e travamento antes de estética.

## Catálogo

| Área | Caso | O que verifica | Rótulo |
| --- | --- | --- | --- |
| Buffer circular | vazio, cheio, cap 1, cap 0, wrap do índice, saída preservada em erro | contrato de erro e ordem FIFO | Inferido |
| Buffer circular | produtor e consumidor alternados em padrões diferentes (3 push, 2 pop, 3 push) | wrap em estados parciais | Inferido |
| Contador/tempo | deadline cruzando o wrap do contador de 32 bits | comparação correta com subtração com sinal | Inferido |
| Contador/tempo | timeout exatamente no limite (igual, um a menos, um a mais) | erro de um | Inferido |
| Barramento | NACK no endereço, NACK no dado, timeout, resposta curta, resposta de tamanho errado | caminho de erro e saída intacta (V-35 item 1) | Verificado (requisito), Inferido (casos) |
| Barramento | falha seguida de sucesso: o driver se recupera sem estado preso | recuperação | Inferido |
| Barramento | limite de tentativas e atraso entre tentativas | sem laço infinito (V-35 itens 2 e 4) | Verificado (requisito) |
| UART | byte perdido no meio do frame; frame truncado; frame com CRC inválido; comprimento maior que o buffer; comprimento zero | enquadramento e ressincronização | Inferido |
| UART | overflow de FIFO e erro de paridade/quadro sinalizados ao driver | contagem de erros e política | Verificado (eventos no ESP-IDF, V-32) |
| CAN | transição Error Active, Warning, Passive, Bus Off; recuperação com limite | máquina de estados do nó | Verificado (V-31) |
| CAN | filtro de máscara com IDs dentro e fora, ID de 29 bits | filtro configurado com nó desabilitado | Verificado (V-31) |
| MQTT | queda do link com mensagens em voo; reconexão com backoff; QoS 1 duplicado entregue duas vezes | idempotência do consumidor, política de backoff | Verificado (QoS 1 pode duplicar, V-33) |
| MQTT | will e mensagem de status online após reconectar | ordem de publicações | Inferido |
| Protocolo | campo de comprimento hostil (maior que o buffer), campo reservado diferente de zero, versão desconhecida | validação de entrada | Inferido |
| Conversão | fim de escala, valor negativo, arredondamento, saturação, ponto fixo | sem overflow nem perda silenciosa | Inferido |
| Endianness | decodificação de inteiros de 16 e 32 bits de buffer de bytes | independência de alinhamento (use cópia por byte ou `memcpy`) | Inferido |
| Máquina de estados | cada transição legal; cada evento ilegal em cada estado | estado inválido não corrompe | Inferido |
| Política de retry | contagem de tentativas, atraso crescente, teto, reinício após sucesso | backoff com teto | Inferido |
| Persistência | dado válido, dado com CRC inválido, formato de versão antiga, armazenamento cheio | migração e erro | Inferido |
| ISR (simulada) | interrupção chamada entre duas instruções do código principal | corrida de leitura-modificação-escrita (V-12) | Verificado (risco), Inferido (técnica) |
| Reset | estado após reset por watchdog, por brownout, por deep sleep | inicialização defensiva (V-39 para deep sleep) | Verificado (V-39) |
| Configuração | limites do Kconfig/`sdkconfig`/defines (mínimo, máximo, inválido) | build falha ou comportamento definido | Inferido |

## Simular interrupção no host

A ISR é uma função C comum; no host o teste a chama manualmente no ponto exato do entrelaçamento perigoso. Para isso, o código principal acessa o dado compartilhado por funções pequenas e o teste injeta um gancho que chama a ISR no meio:

```c
/* produção: o acesso passa por uma função que o teste pode interceptar */
extern void (*test_hook_between_read_and_write)(void);   /* NULL em produção */

void counter_increment_from_main(volatile uint32_t *c)
{
    uint32_t tmp = *c;                                   /* leitura */
    if (test_hook_between_read_and_write) { test_hook_between_read_and_write(); }
    *c = tmp + 1u;                                       /* escrita: perde a atualização da ISR */
}
```

O teste instala um gancho que executa `*c += 1` como se fosse a ISR e verifica que, com a proteção correta (seção crítica, atômico), nenhuma atualização se perde. Isso prova a lógica de proteção, não a atomicidade do hardware; o teste na placa mede o resto. Conserve o gancho fora do binário de produção (`#ifdef UNIT_TEST`). Técnica: Inferido; a necessidade vem de V-12.

## Aritmética de tempo

Contadores de 32 bits em milissegundos dão a volta em cerca de 49,7 dias (2^32 ms). A forma segura de comparar é pela diferença com sinal:

```c
static inline int time_reached(uint32_t now, uint32_t deadline)
{
    return (int32_t)(now - deadline) >= 0;     /* vale enquanto o prazo está a menos de 2^31 ms */
}
```

Casos de teste: `now = 0xFFFFFFF0`, `deadline = 0x00000010` (prazo depois do wrap) retorna 0; `now = 0x00000011` retorna 1; prazo igual retorna 1; prazo a mais de 2^31 ms de distância é fora do contrato e deve estar documentado. O relógio injetado é uma variável que o teste move. Aritmética: verdadeira por construção; o idioma é Inferido.

## Queda de energia no meio de uma escrita

Para armazenamento próprio (configuração em flash, contadores): faça o falso de armazenamento falhar depois do N-ésimo byte ou da N-ésima página, e varie N sobre toda a operação. Em cada N, o estado depois do reinício deve ser o antigo ou o novo, nunca meio a meio, e o CRC ou o número de sequência deve detectar o torn write. Se o projeto usa o sistema de arquivos ou NVS do SoC, a garantia vem dele e o teste de host cobre só o uso (Não verificável aqui: armazenamento NVS/flash é lacuna de fonte do segmento).

## Nomear e ordenar

- Nome do teste = comportamento: `test_pop_on_empty_fails_and_keeps_output`, não `test_pop_2`.
- Um arquivo de teste por módulo; casos felizes primeiro, depois bordas, depois falhas injetadas.
- Casos que dependem de ordem de chamadas do mock ficam em testes próprios, nomeados pelo contrato.
- Teste lento ou que precisa de bancada leva etiqueta (`[bench]` ou categoria própria) e fica fora da suíte padrão de host; o plano registra o gate.
- Um bug de campo ganha um teste com o identificador do relatório (`test_issue_142_reconnect_loop_has_backoff`), vermelho antes da correção (V-22).
