# Plano de incremento de firmware

Adaptado do `plano-incremento.md` do brain-of-agent (MIT, Francisco Edson) e das práticas V-25 (contrato antes do código). Pule o plano se o diff cabe em uma frase.

## Objetivo e baseline

- Problema / necessidade e usuário: <...>
- Critério de sucesso e fonte: <...>
- Estado observado e reprodução (ou motivo de reset e registradores de falha): <...>
- Escopo, exclusões e autorização (inclui: pode gravar placa? sim/não): <...>
- Alvo: <MCU + revisão>, framework e versão, toolchain, placa: <...>

## Contrato (escopo, riscos, testes, reversão)

- Escopo: <...>
- Riscos: <ISR / memória / OTA / segurança / energia>
- Testes (host, simulado, bancada): <...>
- Reversão: <como voltar ao estado anterior, inclusive na placa>

## Fatia vertical

Evento ou entrada (sensor, rede, botão) -> ISR/driver -> fila ou estado -> regra -> saída (atuador, mensagem, log) -> resultado observável. Descreva cada fronteira e sua falha/recuperação.

| Requisito | Alteração | Invariante | Verificação / oráculo |
| --- | --- | --- | --- |
| | | | |

## Dependências de datasheet e fontes de verdade

| Elemento | Fonte (arquivo, seção) | Estado (Verificado / Não verificável) |
| --- | --- | --- |
| | | |

## Orçamentos

Flash/RAM, pilhas, latência, corrente: método de medição e meta (ver `orcamentos.md`).

## Fases

| Fase | Artefato utilizável | Risco | Mitigação | Critério de saída |
| --- | --- | --- | --- | --- |
| | | | | |

## Bancada necessária

Comandos de gravação (com cartão de gravação), caminho de recuperação, o que será observado. Nada é gravado sem confirmação explícita no chat.

## Entrega

Como compilar, testar e observar; evidências por nível; pendências; próximo passo.
