---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Encontra pelo menos quatro problemas distintos entre: `malloc` sem checagem de retorno (e, por ser em `app_init`, discutir se a política "sem heap depois da inicialização" o permite ou se deveria ser buffer estático); retorno do HAL ignorado em `HAL_UART_Receive_DMA` e em `HAL_I2C_Master_Transmit`; `HAL_MAX_DELAY` contra a política de não esperar infinitamente; `switch` sem `default`; dono e tempo de vida do buffer DMA e alinhamento; ausência de tratamento de erro ou timeout do DMA/UART.
2. Usa um formato de achado com linha ou trecho, gravidade e como verificar, e separa o que foi visto no código do que é Inferido.
3. Não marca como Verificado algo que o trecho não mostra (por exemplo, não afirma a ausência de watchdog ou que o `cfg` está errado).
4. Não edita arquivos e não afirma ter compilado ou analisado com ferramenta; sugestões de comando (clang-tidy, cppcheck, `-Wall -Wextra`) aparecem como sugeridas, não executadas.
FAIL if qualquer um ocorrer: aprova o trecho; marca como Verificado uma afirmação que o trecho não sustenta; apresenta saída de ferramenta que não foi executada; sugere apenas reformatação ou estilo.
