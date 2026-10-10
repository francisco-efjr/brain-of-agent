# Modelo de tasks.md, exemplo e verificação de dependências

Formato destilado do `tasks-template.md` do GitHub spec-kit (MIT, Copyright GitHub, Inc.; V-10): ID sequencial, marcador `[P]` de paralelismo, marcador de história, fases, checkpoint por história. Texto e exemplo são originais deste plugin; o placeholder do gerador do spec-kit não é usado.

## Sumário

- [Regras](#regras)
- [Modelo](#modelo)
- [Exemplo preenchido (ilustrativo)](#exemplo-preenchido-ilustrativo)
- [Verificar ciclos nas dependências](#verificar-ciclos-nas-dependências)
- [Plano de implementação: o que pedir ao plan-writer](#plano-de-implementação-o-que-pedir-ao-plan-writer)

## Regras

1. ID `T001`, `T002`... sequencial e estável (não renumere depois de aprovado; novas tarefas ganham o próximo número).
2. `[P]` somente se a tarefa toca arquivo diferente e não depende de tarefa incompleta. Na dúvida, não use `[P]`.
3. `[US1]`, `[US2]`... liga a tarefa à história da spec (P1, P2, P3). Tarefas de Setup, Fundação e Polish não levam marcador de história.
4. Caminho de arquivo exato em cada tarefa (existente, encontrado no mapa; ou novo, com o diretório justificado pelo padrão do repositório).
5. Cada tarefa tem uma linha `Verifica:` com comando, teste ou conferência descrita. A tarefa só termina quando a verificação passa. Testes automatizados novos só se a spec pede; a estratégia de testes é do segmento `qa-testing`.
6. Fundação bloqueia as histórias: o que é pré-requisito comum (esquema de dados, autenticação base) entra aqui, e só isso.
7. Cada fase de história termina com um **checkpoint**: a história funciona e é testável sozinha, sem as seguintes.
8. Dependência explícita: `(depende: T003, T004)` no fim da linha.
9. Nenhuma tarefa exige decisão humana nem deixa placeholder. Decisão pendente é pergunta aberta antes do plano.
10. Cada `FR-` da spec aparece em pelo menos uma tarefa.

## Modelo

```markdown
# Tarefas: <feature>

Spec: <caminho> (aprovada em AAAA-MM-DD por <nome>)
Comando de verificação do projeto: <comando real, lido do CLAUDE.md/README; ou "a definir com o usuário">

## Fase 1: Setup
- [ ] T001 <descrição> em `<caminho>`
  - Verifica: <comando ou conferência>

## Fase 2: Fundação (bloqueia as histórias)
- [ ] T002 <descrição> em `<caminho>` (depende: T001)
  - Verifica: <...>

## Fase 3: História 1 (P1) - <título>
Objetivo da fase: <o que a pessoa consegue fazer ao fim>
- [ ] T003 [P] [US1] <descrição> em `<caminho>` (depende: T002)
  - Verifica: <...>   Cobre: FR-001
**Checkpoint US1**: <como provar a história sozinha>

## Fase N: Polish
- [ ] T0NN <descrição> em `<caminho>`
  - Verifica: <...>

## Dependências e ordem
<resumo: Fundação antes das histórias; histórias podem seguir em paralelo se não compartilham arquivos>
```

## Exemplo preenchido (ilustrativo)

Spec hipotética de exportação de relatório em CSV. Caminhos, comandos e nomes são fictícios, só mostram o formato. Em um projeto real, caminhos vêm do mapa do código e os comandos do `CLAUDE.md`.

```markdown
# Tarefas: Exportação de relatório de vendas

Spec: specs/exportacao/spec.md (aprovada em 2026-10-10 por Ana)
Comando de verificação do projeto: npm test (lido do README; ilustrativo)

## Fase 1: Setup
- [ ] T001 Registrar a permissão `relatorios.exportar` em `src/auth/permissions.ts`
  - Verifica: `npm test -- permissions` passa; permissão aparece na lista exportada

## Fase 2: Fundação (bloqueia as histórias)
- [ ] T002 Criar a consulta de vendas por período em `src/reports/salesQuery.ts` (depende: T001)
  - Verifica: teste com 120 vendas em setembro e 30 em agosto retorna 120

## Fase 3: História 1 (P1) - Gerente exporta vendas do período em CSV
Objetivo da fase: a gerente baixa o arquivo com exatamente as vendas do filtro.
- [ ] T003 [P] [US1] Gerar o CSV a partir da consulta em `src/reports/csvExporter.ts` (depende: T002)
  - Verifica: arquivo gerado tem 120 linhas de venda + cabeçalho   Cobre: FR-001
- [ ] T004 [P] [US1] Expor a ação de exportar na tela de relatórios em `src/ui/ReportsPage.tsx` (depende: T002)
  - Verifica: gerente vê a ação; verificação manual descrita no checkpoint   Cobre: FR-002
- [ ] T005 [US1] Recusar usuário sem permissão em `src/reports/exportHandler.ts` (depende: T001, T003)
  - Verifica: tentativa de atendente retorna a mensagem de permissão e nenhum arquivo   Cobre: FR-003
**Checkpoint US1**: com a conta de gerente exportar setembro e conferir 120 linhas; com a de atendente, ver a recusa.

## Fase 4: História 2 (P2) - Falha na geração não deixa arquivo parcial
- [ ] T006 [US2] Garantir limpeza do arquivo parcial em `src/reports/csvExporter.ts` (depende: T003)
  - Verifica: teste que força erro no meio da geração; nenhum arquivo disponível   Cobre: FR-004
**Checkpoint US2**: forçar falha e confirmar mensagem de erro e ausência de arquivo.

## Fase 5: Polish
- [ ] T007 Registrar auditoria da exportação em `src/audit/exportAudit.ts` (depende: T005)
  - Verifica: registro com quem, quando, relatório e filtro, sem o conteúdo   Cobre: FR-005
```

Observações sobre o exemplo: T003 e T004 são `[P]` porque tocam arquivos distintos e dependem apenas de T002; T005 não é `[P]` porque depende de T003 no mesmo fluxo; T006 edita `csvExporter.ts` de novo, por isso depende de T003 e não pode ser `[P]` com ele.

## Verificar ciclos nas dependências

Script de leitura (Python 3.9+, só stdlib). Ele lê `tasks.md`, monta o grafo a partir de `(depende: ...)` e informa ciclos e referências a IDs inexistentes. Rode no seu terminal; o plugin não executa nada. Revise o código antes de rodar.

```python
import re, sys
from graphlib import TopologicalSorter, CycleError

deps = {}
for line in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"\s*- \[[ xX]\] (T\d+)\b", line)
    if m:
        d = re.search(r"\(depende: ([^)]*)\)", line)
        deps[m.group(1)] = re.findall(r"T\d+", d.group(1)) if d else []
unknown = sorted({x for v in deps.values() for x in v} - set(deps))
try:
    list(TopologicalSorter(deps).static_order())
except CycleError as e:
    print("ciclo:", e.args[1]); sys.exit(1)
print("ok:", len(deps), "tarefas; IDs desconhecidos:", unknown or "nenhum")
```

Uso: `python check_deps.py tasks.md`. Se o resultado não puder ser rodado, registre "grafo de dependências: Não verificado".

## Plano de implementação: o que pedir ao plan-writer

Oito seções (V-13): Requisitos e restrições; Passos; Alternativas; Dependências; Arquivos; Testes; Riscos e premissas; Especificações relacionadas. IDs: `REQ-`, `TASK-`, `TEST-`, `RISK-`, `ASSUMPTION-`, `ALT-`, `FILE-`, `DEP-`. Cada fase leva:

```markdown
### Fase 3: História 1 (P1)
Tarefas: TASK-003..TASK-005    Requisitos: REQ-001..REQ-003
Critério de conclusão (mensurável, verificável por comando):
- `npm test -- reports` passa, incluindo TEST-001 (120 linhas) e TEST-002 (recusa de atendente)
- Verificação manual descrita no checkpoint US1 executada e registrada
```

O campo "Critério de conclusão" é construção deste plugin (a fonte não o tem, V-13). Cada `REQ` liga a pelo menos uma `TASK` e um `TEST`. O agente escreve apenas em `plans/` e não executa comandos.
