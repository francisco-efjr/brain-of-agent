# Relatório de revisão de firmware - <módulo / diff / commit>

**Escopo revisado:** <arquivos, revisão, perfil (bare metal / ESP-IDF / Zephyr / FreeRTOS / Rust)>
**Política de memória:** <...> · **Alvo:** <MCU + revisão> · **Data:** <...>
**Revisor:** <skill/agente>; revisão do mesmo modelo que escreveu o código é parcial, não validação externa.

## Resumo (3 a 5 linhas)

<o que foi encontrado, principal risco, recomendação>

## Achados

| ID | Severidade | Confiança (1-10) | arquivo:linha | Regra / fonte (V-nn) | Evidência (trecho) | Correção | Como verificar | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-01 | crítica / alta / média / baixa | | | | | | | Verificado / Inferido / Suposição |

Regras: achado com confiança abaixo de 6 vai para "Não verificado". Relate lacunas de correção e de requisito; estilo, se citado, vem marcado como opcional.

## Resumo por grupo

| Grupo | Achados | Observação |
| --- | --- | --- |
| Erro e retorno | | |
| Recursos e memória | | |
| Tipos e atomicidade | | |
| ISR e concorrência | | |
| Barramentos e rede | | |
| Robustez de campo (watchdog, fault handler, timeouts) | | |
| Orçamentos (pilha, flash/RAM, energia) | | |

## Verificado, simulado e testado em hardware

| Nível | Comando e saída essencial | Resultado |
| --- | --- | --- |
| Compilado | | |
| Analisado (clang-tidy, cppcheck, sanitizers no host) | | |
| Testado no host | | |
| Em hardware | (não executado, a menos que haja registro de bancada) | |

## Não verificado

- <itens que dependem de datasheet, placa, medição ou ferramenta indisponível>

## Ações humanas necessárias

- <gravações, chaves, eFuse, decisões de produto>

## Próximo passo

- <...>
