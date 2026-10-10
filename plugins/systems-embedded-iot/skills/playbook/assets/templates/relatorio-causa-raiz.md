# Relatório de causa raiz - <sintoma, onde, condição>

Metodologia destilada do `/investigate` do gstack (repositório garrytan/gstack, MIT; V-22), sem copiar o arquivo, e do `bug-report.md` do brain-of-agent (MIT). Status final: DONE, DONE_WITH_CONCERNS ou BLOCKED.

- **Ambiente / versão:** <MCU + revisão, placa, firmware (commit/build), toolchain>
- **Sintoma:** <o que o usuário vê>
- **Frequência e condições:** <ocorrências / tempo ligado / carga / temperatura>
- **Reprodução ou registro:** <passos; OU motivo de reset, registradores de falha, contador de reinícios, versão do build>
- **O que mudou recentemente:** <`git log`/diff relevante>
- **Dados que faltam:** <o que pedir ou instrumentar (fault handler que registra, contador, log)>

## Hipóteses (máximo 3)

| # | Hipótese testável | Como confirmar (log, assert temporário, captura de barramento, oráculo host x alvo) | Resultado | Estado |
| --- | --- | --- | --- | --- |
| 1 | | | | confirmada / descartada / não testada |

Após três hipóteses falhas: pare, relate e pergunte.

## Causa raiz

<causa, não sintoma; rótulo Verificado / Inferido>. Aumentar pilha ou timeout só entra com medição e justificativa.

## Correção

<menor diff; arquivos; se tocar mais de cinco arquivos, pergunte antes>

## Prova

- Teste de regressão que falha sem a correção (host) ou log de bancada com data e revisão: <comando e saída>
- Suíte inteira: <comando e saída>

## Riscos, limitações e o que não foi testado

<...>

## Status

DONE / DONE_WITH_CONCERNS / BLOCKED · Próximo passo: <...> · Hipótese de causa (se ainda não confirmada) é inferência, não fato.
