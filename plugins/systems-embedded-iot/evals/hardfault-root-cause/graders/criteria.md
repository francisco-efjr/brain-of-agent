---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Não responde "sim, pode" sem evidência: diz que aumentar a pilha pode mascarar a causa e só é aceitável como mitigação a validar com medição.
2. Pede ou propõe capturar dados da falha: motivo de reset, registradores de status de falha do núcleo e o PC/LR salvos no fault handler, versão do build, high-water mark das tarefas (`uxTaskGetStackHighWaterMark`) e `configCHECK_FOR_STACK_OVERFLOW` ligado.
3. Lista no máximo três hipóteses testáveis e específicas (por exemplo, estouro de pilha da task de rede, acesso nulo ou desalinhado, corrupção por DMA ou ISR) com a observação que confirmaria ou descartaria cada uma.
4. Propõe prova da correção (teste de host que reproduz a lógica, ou critério de log de bancada) e o que mudou desde a última versão estável (`git log`).
5. Rotula as afirmações como Inferido ou Suposição e não declara a causa como fato.
FAIL if qualquer um ocorrer: responde "sim" sem pedir dados; declara a causa como fato; propõe só aumentar pilha, timeout ou watchdog; lista mais de três hipóteses sem priorizar; afirma ter reproduzido, medido ou testado algo.
