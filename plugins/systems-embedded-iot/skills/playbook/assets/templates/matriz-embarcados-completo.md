# Matriz do modo EMBARCADOS-COMPLETO

Modelo derivado do protocolo `FULLSTACK-COMPLETO` do brain-of-agent (MIT, Francisco Edson). Ativa só por pedido do usuário digitado no chat; não amplia permissões; o gate de hardware continua valendo.

## 1. Entrada

- Objeto: <repositório / módulo / diff> · Revisão: <commit> · Modo: [análise apenas / implementação autorizada em: <escopo>]
- Alvo: <MCU + revisão>, framework e versão, toolchain · Ambiente: <SO>
- Ferramentas e limites (leitura, escrita, shell, rede, placa, probe, instrumentos, git): <lista; ausência é limitação verificável, não defeito do firmware>
- Autorização de gravação: [nenhuma / escopada: placa, porta, comando, binário, recuperação]
- Fonte de verdade dos requisitos: <...>

## 2. Registro de leitura

| Arquivo | Revisão | Estado (lido / parcial / ausente) | Decisão extraída |
| --- | --- | --- | --- |
| references/checklist-completo.md | | | |
| references/c-cpp-rust-firmware.md | | | |
| references/rtos-interrupcoes-e-recursos.md | | | |
| references/padroes-e-antipadroes.md | | | |
| references/barramentos-e-protocolos.md | | | |
| references/testes-e-bancada.md | | | |
| references/ferramentas-e-mcp.md | | | |
| references/decisoes-e-tradeoffs.md | | | |
| references/ota-e-seguranca-iot.md | | | |
| references/datasheet-drivers-e-plataformas.md | | | |
| references/claude-md-snippets.md | | | |
| references/fontes.md | | | |
| templates e skills de tarefa aplicáveis | | | |

Leitura em lotes com checkpoint persistido (lote 1: A a E; lote 2: barramentos, testes, ferramentas, decisões; lote 3: OTA/segurança, datasheet, snippets, fontes).

## 3. Matriz de aplicabilidade

| Área (`checklist-completo.md`) | Estado (aplicável / NA / NV) | Motivo (NA ou NV) | Itens OK | Itens com falha | Pendentes | Evidências |
| --- | --- | --- | --- | --- | --- | --- |
| A Alvo e escopo | | | | | | |
| B C/C++/Rust | | | | | | |
| C Memória | | | | | | |
| D ISR e concorrência | | | | | | |
| E RTOS | | | | | | |
| F Barramentos | | | | | | |
| G Rede (MQTT/BLE/Wi-Fi) | | | | | | |
| H Energia | | | | | | |
| I Testes | | | | | | |
| J Bancada e gate | | | | | | |
| K OTA e segurança | | | | | | |
| L Build e CI | | | | | | |
| M Documentação | | | | | | |
| N Entrega | | | | | | |

## 4. Gates

| Gate | Resultado | Evidência |
| --- | --- | --- |
| Entendimento | | |
| Plano | | |
| Implementação | | |
| Validação | | |
| Revalidação | | |
| Entrega | | |

## 5. Resultado

[Concluído no escopo / Parcial / Impedido] · Falhas críticas abertas: <...> · Lacunas: <leitura, acesso, execução, bancada> · Risco residual: <...> · Ações humanas: <...> · Revisão independente: <declarar se for do mesmo modelo> · Próximo passo: <...>
