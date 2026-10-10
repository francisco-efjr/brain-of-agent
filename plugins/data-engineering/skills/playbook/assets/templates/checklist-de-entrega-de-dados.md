# Checklist de entrega de dados: [PEDIDO]

Uso: fim de qualquer tarefa de dados (modelo, DAG, job, SQL, contrato). Base: V-01. Cada item tem evidência colada ou "não verificado".

| # | Item | Resultado | Evidência |
| --- | --- | --- | --- |
| 1 | Comando de verificação declarado antes de editar e executado ao fim | [Verificado ou Não verificado: motivo] | `[COMANDO]` → [SAÍDA RESUMIDA EM ATÉ 10 LINHAS] |
| 2 | Contagens ou métricas antes e depois (quando há dados) | [Verificado, Não aplicável ou Não verificado] | Antes: [N] · Depois: [N] · Consulta: `[SQL]` |
| 3 | Arquivos alterados | [LISTA] | `git diff --stat` ou lista |
| 4 | Riscos e itens não verificados, cada um rotulado | [LISTA] | Seção abaixo |
| 5 | Nada fora do escopo foi tocado | [Sim ou Não: o quê] | Diff compatível com o pedido |

## Resultado
[RESUMO EM 2 A 4 LINHAS: o que mudou e o efeito]

## Verificado
- [ITEM] — [COMANDO E TRECHO DA SAÍDA]

## Inferido, Suposição
- [ITEM] — [RÓTULO] — [POR QUE NÃO FOI VERIFICADO]

## Não verificável ou não executado
- [ITEM] — [MOTIVO: sem acesso, sem permissão, sem versão informada]

## Riscos
- [RISCO] — [IMPACTO E MITIGAÇÃO]

## Pendências (incluindo `warn` com número)
- [PENDÊNCIA] — [CONTAGEM] — [DONO]

## Próximo passo
[AÇÃO] — [QUEM] — [CONDIÇÃO]. Ações externas (rodar em produção, backfill, `VACUUM`, publicar) só por confirmação explícita do usuário e fora deste plugin.

Observação: revisão feita pelo mesmo modelo que implementou é autoavaliação, não validação independente.
