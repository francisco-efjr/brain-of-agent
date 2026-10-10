# Plano de teste de firmware - <módulo / produto>

Adaptado do `plano-de-teste.md` do brain-of-agent (MIT, Francisco Edson), com as camadas de V-36 a V-38 e V-57. Critérios congelados antes de executar; mudança legítima de requisito atualiza o plano com fonte.

**Pergunta / decisão que este plano informa:** <...>
**Alvo:** <MCU + revisão, framework e versão> · **Ambiente do desenvolvedor:** <SO; Windows -> WSL/container para `unit_testing` do Zephyr>
**Bancada disponível:** <sim/não; placa, probe, instrumentos>

## Camadas

| Camada | Onde roda | Ferramenta | Cobre | Não prova |
| --- | --- | --- | --- | --- |
| Domínio puro | host | Unity / ztest `unit_testing` / PlatformIO `native` / `cargo test --target <host>` | lógica, casos de borda | tempo, periférico |
| Driver com HAL falsa | host ou `native_sim` | CMock / mocks próprios / traits falsos | sequência de chamadas, erros injetados | elétrica |
| Alvo | placa (gate) | Unity no ESP-IDF, ztest no alvo, pytest-embedded | periférico, temporização | cobertura ampla |
| HIL | bancada (gate) | pytest-embedded + serviço `idf`, Twister `--device-testing` | integração real | tudo que a bancada não reproduz |

## Casos

| ID | Requisito / risco | Camada | Entrada | Oráculo (e fonte) | Resultado esperado | Gate de bancada? |
| --- | --- | --- | --- | --- | --- | --- |
| T-01 | Buffer circular: wrap-around e cheio | domínio | 2*cap bytes | modelo de referência | ordem FIFO preservada | não |
| T-02 | I2C NACK injetado | driver/mock | `HAL_ERR_NACK` | requisito de erro | código de erro e flag de dado inválido | não |
| T-03 | Wrap de contador de tempo (uint32 ms) | domínio | início perto de 0xFFFFFFFF | aritmética de diferença | timeout correto através do wrap | não |
| T-04 | Reconexão MQTT com backoff | domínio | falhas consecutivas | política (base, máximo, jitter) | atraso crescente, limitado, com jitter | não |
| T-05 | Acordar de deep sleep com motivo correto | alvo multi-estágio | ciclo de sleep | motivo de reset esperado | motivo registrado | sim |

## Execução e evidências

- Runner conferido: não grava a placa (ver `testes-e-bancada.md` seção 7). Comando: `<...>`.
- Ordem: teste vermelho confirmado pelo motivo certo -> correção -> verde -> suíte inteira.
- Teste inaplicável é *skipped*, não removido.
- Registro: `registro-evidencias-bancada.md` para itens de hardware.

## CI

Passos: build cruzado, testes de host, análise estática, sanitizers no host, artefato. Fixar `pytest-embedded~=2.0` quando ESP-IDF. Execução em placa só com gate.

## Não executável e risco restante

<o que depende de bancada, datasheet, instrumento>
