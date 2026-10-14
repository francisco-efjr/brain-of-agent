# Exemplo de inventário: sistema-demo de tarefas

Trecho ilustrativo do `FUNCIONALIDADES.md` de um sistema-demo (login, lista de tarefas e API), com dados sintéticos. Os IDs seguem o template do spec (F-07 = excluir tarefa). O que veio de execução está marcado com o fato de origem (X-07, X-14); o restante é formato de exemplo, não resultado.

## Cabeçalho

```markdown
# Funcionalidades: sistema-demo de tarefas · rodada 2026-10-13
Alvo: http://127.0.0.1:4173 (exploração) · Commit: <sha> · Modo: teste · Teto: ~15 exploradas / ~8 com spec
Versões: Node v24.15.0 · Playwright 1.64.0 · Browser Chrome <versão> · SO Windows 11 · Exploração: `npx playwright cli` (embutido)
```

## Seção 1: inventário e aplicabilidade (trecho)

| ID | Funcionalidade (ação de valor) | Superfície | Papéis | Pré-condições e dados | Risco | Camadas | Tocada | Escopo da rodada | Playwright | Executor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-01 | Entrar com credenciais inválidas mostra erro e não abre sessão | `/login` | visitante | conta de teste do seed local | A (segurança) | e2e | não | explorar e spec | Sim | Playwright |
| F-06 | Adicionar tarefa mostra o item e soma o contador | `/tarefas` | usuário | lista com dado único por teste | M | e2e, api | não | explorar e spec | Sim | Playwright |
| F-07 | Excluir tarefa atualiza lista e contador | `/tarefas` | usuário | tarefa criada pelo próprio teste | M | e2e, api | sim | explorar e spec | Sim | Playwright |
| F-08 | Listar tarefas pela API reflete o que a UI mostrou | `/api/tarefas` | usuário | idem | M | api | não | spec | Sim | Playwright `request` |
| F-12 | Tela de relatórios | `/relatorios` | admin | — | B | e2e | não | Não validado nesta rodada: fora do teto, risco baixo | Sim | Playwright |
| F-15 | App Android nativo do mesmo produto, fluxo de lista | app Android | usuário | AVD existente | M | nativo | não | N/A para Playwright | Não | Compose UI test ou Espresso; exploração por `adb` (Inferido) |

Notas do exemplo:

- F-01 vem do que foi explorado em X-07: senha errada mostra `alert: "E-mail ou senha inválidos."`.
- F-06 e F-07 vêm de X-14: adicionar "Comprar pão" mostra `1 pendente(s)`.
- F-12 e F-15 mostram o que a rodada deixa de fora e por quê. A linha F-15 não é omitida: N/A tem motivo e equivalente.

## Seção 2: cenários (só as do escopo)

### F-07 Excluir tarefa atualiza lista e contador

| Cenário | Passos | Esperado | Fonte do esperado |
| --- | --- | --- | --- |
| Feliz | adicionar a tarefa, excluir | o item some e o contador volta ao valor de antes (`0 pendente(s)` quando a lista estava vazia) | coerência da UI: o rótulo do contador deve bater com a lista |
| Persistência | recarregar a página depois de excluir | o item continua ausente; a API não o devolve | coerência da UI e do backend |
| Borda | adicionar com título vazio | nenhuma tarefa é criada e aparece um aviso (`alert`) | Suposição: o texto exato do aviso não tem fonte; confirmar com o dono do produto |

A linha "Borda" mostra o rótulo Suposição: se esse cenário falhar, a rodada registra uma decisão pendente, não um bug.

## Seção 3 (ainda vazia no inventário)

A matriz de resultado nasce com todas as linhas em "Não validado nesta rodada". Só a skill `evidence-report` altera o status, depois de uma execução com evidência.
