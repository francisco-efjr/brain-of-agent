# Funcionalidades: <sistema> · rodada AAAA-MM-DD

Alvo: <http://127.0.0.1:porta ou staging indicado> · Commit: <sha> · Modo: <teste ou melhoria> · Teto: <cerca de 15 exploradas e 8 com spec, ou PLAYWRIGHT-COMPLETO>
Versões: Node <v> · Playwright <versão exata> · Browser <canal e versão> · SO <...> · Exploração: `npx playwright cli` (embutido) · Portas: exploração <p1>, teste <p2>
Conta de teste: <origem: seed local, variável exportada ou cadastro local; nunca o valor> · Estado de login gerado: <sim ou não, por porta>

## Legenda e regras

- Status: Passou · Falhou · Bloqueado · N/A · Não validado nesta rodada.
- Prova (só para Passou): `spec-estável` (gate 5/5 e shuffle, revisado por outro agente) · `exploração` (sem spec; não protege regressão).
- Só a skill `evidence-report` altera as seções 3 e 4, a partir do `results.json` da execução de evidência e das notas de exploração. O `matrix-auditor` confere uma contra a outra.
- Nunca se edita spec ou asserção para mudar o status. N/A, Bloqueado e Não validado exigem motivo.
- IDs `F-NN` são estáveis entre rodadas: não renumere. Bugs usam `BUG-NN`.
- Rótulos: Verificado · Inferido · Suposição · Não verificável · Não aplicável.

## 1. Inventário e aplicabilidade (todas as funcionalidades)

| ID | Funcionalidade (ação de valor) | Superfície | Papéis | Pré-condições e dados sintéticos | Risco A/M/B | Camadas | Tocada | Escopo da rodada (explorar, spec ou fora, com motivo) | Playwright | Executor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-01 | Verbo + efeito (ex.: "Excluir tarefa atualiza lista e contador") | rota, tela ou endpoint | admin, usuário | conta de teste; lista vazia | A | e2e, api | sim | explorar e spec | Sim [E] | Playwright |
| F-02 | ... | ... | ... | ... | ... | ... | ... | ... | N/A | Compose UI test (exemplo) |

Marcação de maturidade: [E] estável · [X] experimental (nunca único critério) · [L] legado · [N/A]. Tabela completa de aplicabilidade: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/escopo-e-stacks.md`.

## 2. Cenários (só as funcionalidades do escopo)

### F-01 <nome>

| Cenário | Passos | Esperado | Fonte do esperado (requisito, doc, teste, UI; senão Suposição) |
| --- | --- | --- | --- |
| Feliz | 1. ... 2. ... | valor, contador ou estado observável | <requisito, issue, README, teste existente ou coerência da UI> |
| Negativo ou borda | ... | ... | ... |
| Permissão (se o risco pede) | ... | ... | ... |
| Persistência (se o risco pede) | recarregar e consultar a API | ... | ... |

Esperado sem fonte é **Suposição**: a falha vira decisão pendente, não bug afirmado.

## 3. Matriz de resultado

| ID | Status | Prova | Spec | Nota de exploração | Execução (comando, E2E_RUN, data) | Evidência (caminho absoluto) | Bug | Motivo | Rótulo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-01 | Não validado nesta rodada | - | - | - | - | - | - | <motivo> | - |

## 4. Totais

Inventariadas N · Passou P (spec-estável S, exploração E) · Falhou F · Bloqueado B · N/A A · Não validado V

Linha para a mensagem final (antes → depois): `Funcionalidades: N inventariadas · Passou P (S spec estável, E só exploração) · Falhou F (bugs BUG-NN) · Bloqueado B · N/A A · Não validado V · regressões R`

## 5. Bugs achados

| BUG | F-NN | Resumo | Spec vermelho (arquivo e commit) | Trace (caminho absoluto) | Decisão pendente (corrigir ou `test.fail()` anotado) |
| --- | --- | --- | --- | --- | --- |

## 6. Não validado nesta rodada

| ID | Motivo (ex.: fora do teto e risco baixo; sem mudança desde a rodada X) | Próxima rodada |
| --- | --- | --- |
