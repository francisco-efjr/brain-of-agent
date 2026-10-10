# Progresso do firmware - <projeto>

Arquivo de continuidade entre sessões (par de `features.json`; V-02). Cada sessão lê este arquivo e `git log` antes de agir e termina com git limpo e commitado. Sem segredos.

**Alvo e revisão:** <MCU, placa, framework e versão, commit atual>
**Última atualização:** <data> · **Sessão:** <n>

## Estado
| Funcionalidade (`features.json`) | Estado | Evidência (comando e saída, ou caminho do log) | Nível (compilado/host/simulado/hardware) |
| --- | --- | --- | --- |
| F-001 | <pendente / em andamento / passa> | | |

## O que foi feito nesta sessão
- <ação, arquivo, resultado>

## Comandos executados e primeira falha
- <comando> -> <resultado essencial>

## Estado da placa
- Firmware gravado: <versão/hash ou "nada gravado nesta sessão">. Gravações exigem confirmação (cartão de gravação no registro de bancada).

## Pendências, riscos e bloqueios
- <item> · <dependência de datasheet / bancada / decisão humana>

## Próxima ação concreta
- <uma funcionalidade, um critério de saída>

Ao retomar: confirme `git status`, revisão e toolchain antes de assumir que este estado continua válido.
