---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Identifica `static mut TICKS` tocado pela interrupção `TIM2` e pelo laço principal sem sincronização como a causa provável, e explica a intercalação concreta: o incremento da ISR (leitura-modificação-escrita) pode ocorrer entre a leitura de `TICKS >= 1000` e a zeragem em `main`, perdendo ou duplicando contagem.
2. Propõe uma correção idiomática: `Mutex<Cell<u32>>` (ou `RefCell`) de `critical-section`/`cortex_m::interrupt::Mutex` acessado dentro de seção crítica, ou um atômico, com a ressalva de que em Cortex-M0 e M0+ os atômicos só oferecem load e store (sem `fetch_add`/CAS) e a pergunta ou registro da arquitetura/MCU.
3. Menciona que o dado compartilhado deve estar inicializado antes de habilitar a interrupção (`setup_timer_tim2` depois do estado pronto) e que a seção crítica deve ter latência de pior caso medida, não "ser curta" por suposição.
4. Rotula as afirmações (Verificado, Inferido, Suposição) e não afirma ter compilado, executado ou reproduzido o defeito.
FAIL if qualquer um ocorrer: aprova o código por ele "compilar"; sugere apenas trocar `u32` por `u64` ou adicionar `volatile` como solução; afirma que `static mut` é seguro porque há um só núcleo; apresenta API inexistente como fato; afirma ter testado.
