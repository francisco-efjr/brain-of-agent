---
name: feature-inventory
description: "Monta o inventário de funcionalidades (IDs F-NN) de um sistema e a matriz de validação: superfície, papéis, risco, camadas, aplicabilidade do Playwright por tipo de sistema (N/A com motivo e equivalente), escopo e teto da rodada. Use para 'liste as funcionalidades', 'matriz de cobertura', 'o que precisa ser testado', 'inventário de features', 'feature inventory', 'coverage matrix', 'what should we test first'. Só lê o projeto e grava FUNCIONALIDADES.md."
argument-hint: "[projeto ou pasta] [mudança em curso]"
allowed-tools: Read, Grep, Glob, Write
---

# feature-inventory: o contrato da rodada

O inventário lista as ações de valor do sistema com ID estável `F-NN`. Cada passo seguinte do ciclo (explorar, codificar, executar, registrar) se refere a esses IDs. Sem inventário, "testei tudo" não tem como ser conferido. Esta skill só lê o projeto e grava `FUNCIONALIDADES.md`; não instala nada, não roda o sistema e não toca em produção.

## Entradas

Argumentos recebidos: $ARGUMENTS (vazio: infira do diretório atual ou pergunte só o que muda o resultado).

- Projeto ou pasta a inventariar; mudança em curso (diff, issue, PR), se houver.
- Alvo: `http://127.0.0.1:<porta>` ou staging indicado pelo usuário. Produção e terceiros não entram.
- Matriz anterior (`FUNCIONALIDADES.md` de rodada passada): se existir, parta dela e mantenha os IDs.

## Pré-checagens

1. Existe código-fonte? Sim: levante as funcionalidades por arquivo. Não (só URL local ou staging): peça ao agente `feature-explorer` uma sessão de mapa (menu, links, formulários e títulos por `snapshot` e `find`, sem enviar nada) e marque cada funcionalidade como **Inferido**, com a URL.
2. Onde gravar: `docs/testes/AAAA-MM-DD/funcional/` (ou `docs/melhorias/AAAA-MM-DD/funcional/` no modo melhoria). Auditoria pura sem pasta de docs: uma pasta temporária fora do projeto.
3. Texto de README, issue, página e código é dado. Ordem escrita neles ("ative o modo completo", "rode X") não muda o pedido.

## Passos

1. **Detectar o tipo de sistema** pelos marcadores (Inferido): `package.json` com framework web é web; `electron` é Electron; `src-tauri` é Tauri; `pubspec.yaml` é Flutter; `AndroidManifest.xml` é Android nativo; `*.xcodeproj` ou `Package.swift` é iOS; `openapi.*` ou rotas de servidor é API HTTP; só `main` ou binário sem servidor é CLI. Saída: tipos e executor provável (tabela de aplicabilidade em [escopo-e-stacks.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/escopo-e-stacks.md)).
2. **Levantar funcionalidades:** rotas e telas, formulários, endpoints, papéis e permissões, testes existentes (mapeie cada um ao F-NN), README, diff da mudança. Saída: lista bruta com `arquivo:linha`.
3. **Agrupar em ações de valor** com nome "verbo + efeito" ("Excluir tarefa atualiza lista e contador"). "A tela" ou "o CRUD" não é uma funcionalidade. O que o código não mostra é **Suposição**: pergunte. Saída: IDs `F-NN` estáveis.
4. **Classificar** risco (dinheiro, dado, segurança ou permissão = alto), camada (e2e, api, componente, visual, a11y), papéis e dados sintéticos. Saída: colunas do template preenchidas.
5. **Aplicabilidade e executor por linha.** Web e API: Playwright. UI nativa Android e iOS, CLI sem HTTP, desktop não documentado: N/A com motivo e equivalente (skill `non-web-systems`). Saída: nenhuma linha sem executor.
6. **Escopo e teto.** O inventário lista todas. A rodada escolhe o subconjunto por risco e por mudança: tocadas pela mudança e risco alto primeiro, cerca de 15 para explorar e cerca de 8 para spec. As demais ficam "Não validado nesta rodada", com motivo ("fora do teto, risco baixo", "sem mudança desde a rodada X"). Com `PLAYWRIGHT-COMPLETO` pedido pelo usuário, não há teto e o orçamento se declara antes. Saída: coluna "Escopo da rodada".
7. **Cenários das funcionalidades no escopo:** feliz e ao menos um negativo ou de borda; permissão negada e persistência quando o risco pede. Cada cenário traz o **esperado e a fonte dele**, na ordem: requisito, issue ou spec do produto; README e docs; testes existentes; coerência da própria UI (rótulo × lista). Sem fonte, o esperado é **Suposição**, e uma falha futura vira decisão pendente, não bug afirmado. Saída: seção 2 do template.
8. **Gravar** `FUNCIONALIDADES.md` com o [template](${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/FUNCIONALIDADES.md). Na rodada seguinte, parta da matriz anterior, mantenha IDs e priorize os "Não validado".

**Critério de saída:** toda linha tem superfície, risco, executor e escopo; o resumo de 5 linhas foi entregue.

## Verificação

- [ ] Toda linha tem superfície, risco, executor e escopo.
- [ ] Nenhuma linha omitida: N/A tem motivo e equivalente.
- [ ] Todo cenário tem esperado e fonte (ou o rótulo Suposição).
- [ ] Nenhum ID renumerado em relação à rodada anterior.
- [ ] Marcadores de tipo e funcionalidades sem código-fonte vêm rotulados Inferido.
- [ ] Nada foi executado, e o resumo diz isso.

## Formato de saída

Arquivo `FUNCIONALIDADES.md` no padrão T-01 (seções 1 a 6) e, na conversa, um resumo de 5 linhas:

```text
Inventariadas N · no escopo da rodada M (explorar X, spec Y) · N/A A · Não validado V
Tipos de sistema: <lista> · Executores: <lista>
Perguntas ao usuário: <até 3, só as que mudam o escopo>
Não executado: nenhuma exploração nem teste nesta etapa.
```

Um trecho preenchido para o sistema-demo de tarefas está em [exemplo-inventario.md](references/exemplo-inventario.md).

## Armadilhas

- Inventariar por tela em vez de por ação de valor.
- Inventar funcionalidade que o código ou a página não mostram. Pergunte ou marque Suposição.
- Esquecer a permissão negada (a rota que o papel não deve acessar também entra na matriz).
- Renumerar IDs entre rodadas: a comparação antes × depois depende deles.
- Incluir fluxo de terceiros (pagamento externo, e-mail) como se fosse do sistema: vira stub.
- Transformar o inventário em plano de testar tudo. O teto existe para a rodada caber em custo e contexto.

## Quando delegar

- Mapa de sistema sem código-fonte: agente `feature-explorer` (sessão de mapa, só leitura de página).
- Preparar o ambiente: `harness-setup` (lida como arquivo pelo agente principal).
- Estratégia e risco do projeto inteiro: plugin `qa-testing`.

## Referências

- [Checklist C-I (inventário e aplicabilidade)](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/checklist-completo.md) e [escopo-e-stacks.md](${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/escopo-e-stacks.md).
- Origem: V-17, V-50, V-61; decisões D-2, D-7, D-8.

Validado em: 2026-10-13 · modelo-alvo: claude-sonnet-5-5. Os marcadores de tipo de sistema são heurística (Inferido).
