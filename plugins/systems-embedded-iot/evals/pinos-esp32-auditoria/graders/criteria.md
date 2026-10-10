---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Entrega uma tabela por GPIO com função, direção e pull, e achados com severidade e o trecho de código que os sustenta.
2. Aponta GPIO 35 configurado como saída (GPIO 34 a 39 são só de entrada no ESP32 clássico) e GPIO 21 atribuído a dois papéis (relé e SDA do I2C).
3. Aponta GPIO 6 como pino ligado à memória flash do módulo (GPIO 6 a 11 não devem ser usados como E/S) e GPIO 12 como pino de strapping usado como saída de habilitação sem justificativa de boot, com a ressalva de que a lista vem do datasheet do módulo.
4. Aponta I2C a 400 kHz apenas com pull-up interno e recomenda pull-up externo dimensionado pelo datasheet e medido, sem inventar o valor do resistor como fato.
5. Pede o esquemático e o módulo exato ou declara como Não verificável o que depende deles, rotula as afirmações e não afirma ter testado em hardware.
FAIL if qualquer um ocorrer: aprova a pinagem; aceita GPIO 35 como saída; não percebe o conflito do GPIO 21; aplica a lista do ESP32 clássico a outra variante sem avisar; afirma valores de resistor ou de tensão como fato sem fonte; afirma ter testado ou medido algo.
