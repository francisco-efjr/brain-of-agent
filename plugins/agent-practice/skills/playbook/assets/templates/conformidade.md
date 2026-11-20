# CONFORMIDADE: <projeto ou entrega>

- **Data e hora:** <AAAA-MM-DD HH:MM>
- **Projeto / entrega:** <nome e caminho>
- **Contextos:** C0 + <C1, C2, ...> (dinâmicos surgidos: <C6, C7, ...>)
- **Modo:** <proporcional | PRATICA-COMPLETO (pedido explícito em <data>)>
- **Executor:** <agente/modelo/ferramenta> · **Verificador independente:** <agente/modelo> · **Responsável humano:** <nome>
- **Uso de IA declarado:** <onde e como foi usada> (MET-08)

## Portões

| Portão | Resultado | Evidência / observação |
| --- | --- | --- |
| G0 Ativação | <atendido | lacuna> | <linha "Guia: ..." no plano> |
| G1 Pedido e plano | <atendido | N/A: motivo> | <pedido.md> |
| G2 Oráculo | <atendido | N/A: motivo> | <comando de testes e saída> |
| G3 Ambiente | <atendido | lacuna declarada> | <auditoria do kit> |
| G4 Destrutivo (bloqueante) | <atendido | N/A: nada destrutivo> | <plano, aprovação citada> |
| G5 Produção | <atendido | N/A> | <travas OPS-04> |
| G6 Entrega | <atendido | pendente> | <esta tabela> |

## Regras aplicáveis

Status: **Atendida** (com evidência executada nesta sessão), **Exceção** (justificada, abaixo), **N/A** (motivo objetivo), **Pendente humana** (depende de decisão ou aprovação registrada no chat).

> Proporcional: portões, exceções, pendências humanas e falhas linha a linha; N/A agregado por motivo; Atendidas em amostra com evidência. Tabela integral só em `PRATICA-COMPLETO` ou risco alto (MET-06).
>
> A amostra sempre inclui as regras de maior risco tocadas (G4, G5, VER-02, SEG-09 e as `[A+H]`) e ao menos uma por contexto casado.
>
> Atendidas fora da amostra: <IDs, todos listados; nenhum ID aplicável fica fora das listas>

| ID | Regra (curta) | Contexto | Status | Evidência (arquivo:linha, comando, saída) | Observação |
| --- | --- | --- | --- | --- | --- |
| VER-02 | Quem escreveu a verificação não escreveu o código | C0 | Atendida | `tests/test_x.py:1`; autor: agente B; `pytest -q` → 12 passed | |
| SEG-19 | Lista de proteção não vazia | C6 | N/A | nada destrutivo no escopo | |
| REV-02 | Revisão de pessoa experiente | C5 | Pendente humana | pedido enviado no chat em <data> | aguardando <nome> |

## Requisito a requisito (VER-09)

| Requisito do pedido | Passou / Parcial / Falhou | Evidência |
| --- | --- | --- |
| <requisito 1> | <status> | <evidência> |

## Exceções

| ID da regra | Motivo | Risco aceito | Quem decidiu (citação do chat) | Condição de revisão |
| --- | --- | --- | --- | --- |
| <ID> | <motivo> | <risco> | <nome, data> | <quando reavaliar> |

Exceção em regra `[H]`, em G4 ou em G5 só com decisão humana escrita no chat.

## Pendências humanas

- [ ] <decisão ou aprovação necessária> · regra <ID> · dono <nome> · pedido pronto em <local>

## Contraprova

- Auditor: `conformance-auditor` · modelo: <qual> · independente do executor: <sim | não: limitação>
- Linhas refutadas ou rebaixadas: <lista | nenhuma>

## Não verificado

- <o que não foi possível provar e por quê (Não verificável)>

## Resumo para o chat

`Guia: contextos C0+C2+C4 · aplicáveis N · atendidas A · exceções E · N/A X · pendências humanas H · conformidade: <caminho ou "no chat">`
