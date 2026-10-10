---
name: mobile-performance-diagnosis
description: "Diagnostica lentidão, jank, recomposição ou re-render excessivo, cold start e consumo de bateria em apps mobile (Compose, SwiftUI, Flutter, React Native), um eixo por vez e sempre com medição antes e depois. Use para 'app lento', 'travando ao rolar', 'recomposição', 're-render', 'cold start', 'bateria', 'wake lock', 'Doze', 'slow scrolling', 'battery drain', 'frame drops', 'coloca remember e @Immutable em tudo'. Não promete ganho numérico sem medir."
argument-hint: "[plataforma] [sintoma] [evidência opcional]"
allowed-tools: Read, Grep, Glob
---

# mobile-performance-diagnosis

Acha a causa com evidência e propõe **uma** mudança por vez, medida antes e depois. Memoização, `@Immutable`, `useMemo` ou `const` espalhados sem problema medido são antipadrão (V-11, V-22, V-32). Verificado em 2026-10-10.

Por que um eixo por vez: com várias mudanças juntas, não se sabe qual ajudou, qual atrapalhou e qual não fez nada. O ciclo é reproduzir, classificar, mudar um ponto, **remedir a mesma captura**, reverter se não houver ganho.

## Entradas

`$ARGUMENTS` = `[plataforma] [sintoma] [evidência]`. Peça (uma pergunta por vez, só o que falta): como reproduzir (qual tela, qual gesto), qual build foi medido (release/profile ou debug?), qual aparelho (o de menor capacidade importa), evidência existente (trace, relatório do compilador Compose, DevTools, Perf Monitor, Android vitals). **Antes de colar traces ou screenshots, redija tokens, dados pessoais e dados de produção** (V-22, S-18).

## Pré-checagens

1. **Build representativo.** Debug não representa: dev mode do RN é lento e deve ser medido em release (V-30); Flutter mede em profile mode com DevTools (V-29); Compose mede em build release/não debugável. Medição só em debug vira **Suposição**.
2. **Ambiente.** Instruments (iOS) exige macOS. Sem ele: revisão de código e sintomas; medição **Não verificável**.
3. **Sem otimização especulativa.** Se não há sintoma reproduzível, diga e peça como reproduzir. Não "otimize preventivamente".

## Passos

1. **Classificar o sintoma**: renderização/rolagem · partida (cold start) · memória · bateria/segundo plano.
   *Saída:* categoria e hipótese de eixo.
2. **Reproduzir uma transição** específica (uma rolagem, uma navegação) e capturar a linha de base: p50/p95 de frame time, tempo até a primeira tela, memória, ou a métrica do vitals. Sem número, sem comparação.
   *Saída:* linha de base com ferramenta e build; ou "Não verificável (sem medição)".
3. **Aplicar o diagnóstico da plataforma** em [references/por-plataforma.md](references/por-plataforma.md):
   - **Compose** (V-11): eixo = estabilidade dos parâmetros, fase de leitura de State, escrita de snapshot; descarte falsos positivos do relatório do compilador; `@Immutable`/`@Stable` são **promessas**, não devem calar o relatório; `ImmutableList` na fronteira.
   - **SwiftUI** (V-22): 6 passos; perfil guiado só se necessário.
   - **Flutter** (V-29): trabalho fora de `build()`, `setState` na menor subárvore, `const`, listas lazy, evitar `Opacity`/`saveLayer`, não sobrescrever `operator ==` em widgets; orçamento de 16 ms (8 de build + 8 de render).
   - **React Native** (V-30, V-32): release; `console.*` trava a thread JS; `getItemLayout`; FlashList/Legend List; `useNativeDriver`; separação thread JS/UI; Perf Monitor.
   - **Bateria** (V-62, V-63, V-64): [references/bateria.md](references/bateria.md).
   *Saída:* tabela "evidência → causa suspeita".
4. **Mudar um único eixo** e **remedir a mesma captura**. Aplique a mudança só se o usuário pediu a correção; senão, entregue o diff proposto e o roteiro de medição para ele rodar. Comandos passam pelo prompt de permissão normal. Se não houver ganho mensurável, reverter e passar à próxima hipótese. Duas hipóteses falhas seguidas: pare e reporte (C-16).
   *Saída:* antes/depois com o mesmo procedimento.
5. **Relatar** no formato abaixo, com rótulos.

Critério de saída: causa suspeita ligada a evidência; mudança proposta é uma; critério de validação numérico definido (ou "Não verificável"); nenhum ganho prometido sem medição.

## Verificação

- Números antes/depois **na mesma captura** (mesmo aparelho, mesma rota, mesmo build) ou "Não verificável (sem medição)".
- Comandos `adb` de Doze (`dumpsys deviceidle force-idle`, `am set-inactive`) só em **emulador** e só como referência; alteram o estado do aparelho de teste (V-63).
- Nenhum benchmark ou baseline profile é exigido por V-11 (lacuna): se o projeto não tem Macrobenchmark, sugira como opção (**Inferido**), não como pré-requisito.

## Formato de saída

Use `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/relatorio-performance.md` se existir. Exemplo (caso sintético: pedido "a lista trava, coloca remember e @Immutable em tudo"):

```markdown
## Diagnóstico de performance — Compose — lista de produtos — 2026-10-10
Dados sensíveis redigidos de traces/screenshots: sim. Build medido: release, aparelho de menor capacidade do usuário (informar modelo).

| Sintoma | Causa suspeita | Evidência | Correção (um eixo) | Validação | Rótulo |
| --- | --- | --- | --- | --- | --- |
| Frames perdidos ao rolar `ProductList` | `LazyColumn` sem `key`; itens recompõem ao inserir no topo | `ProductList.kt:37` `items(products)` sem `key`; relatório do compilador mostra `ProductRow` "restartable, not skippable" por `List<Product>` instável | Passar `key = { it.id }` em `items` (identidade estável). **Só isso.** | Repetir a mesma rolagem; comparar contagem de recomposições e frames > 16 ms antes/depois; reverter se não houver ganho | Inferido até medir |
| — | Leitura de scroll na composição | `ProductList.kt:52` `Modifier.offset(y = scrollState.value.dp)` lê State em composição | Fase de layout: `Modifier.offset { IntOffset(0, scrollState.value) }` (segundo eixo, depois de remedir o primeiro) | idem | Inferido |

Não aplicado, de propósito: `@Immutable`/`remember` em tudo. São promessas e podem esconder o problema no relatório (V-11). Com Kotlin 2.0.20+ o strong skipping é padrão (V-11, `stability.md`); confirme a versão do projeto.
Não verificável: números reais (sem medição nesta sessão).
```

## Gotchas

1. Debug não representa release em nenhuma das quatro stacks (V-29, V-30).
2. A afirmação "meça em aparelho físico, nunca simulador" não consta na página de V-29; a página cita profile mode e o aparelho de menor capacidade. Boa prática a conferir na página de build modes.
3. V-22 (Dimillian) pede traces e screenshots sem mandar remover dados sensíveis: este plugin acrescenta a redação.
4. Android vitals: consequências de wake locks são possibilidades ("pode"), não certezas; a aplicação a partir de 2026-03-01 não foi confirmada (V-62).
5. Em Doze, a página oficial diz que tarefas de WorkManager não rodam (V-63). Isso é compatível com usar WorkManager para trabalho adiável (C5).
6. Energia no iOS: só o índice atual e a página arquivada de Low Power Mode foram lidos; artigos de CPU, rede, localização e Power Profiler não (lacuna 9). A sintaxe Swift da página arquivada está obsoleta.
7. Medir só cold start para TTI em RN (V-32); não misture com warm start na mesma comparação.

## Ressalvas e lacunas

Sem fonte validada para: Macrobenchmark/baseline profiles (V-11 não exige), memória/leaks em qualquer plataforma, tamanho de binário, partida a frio no iOS além de V-22. Esses pontos ficam **Inferido** ou fora do relatório. Limiar de vitals e datas: reconferir na página (verificado em 2026-10-10).

## Quando delegar

- Revisão do diff depois da correção: agente `mobile-pr-reviewer`.
- Se a causa é arquitetura (estado duplicado, fonte de verdade ausente): `mobile-architecture-review`.
- Se o sintoma é bateria em segundo plano ligada a push/permissão: `mobile-platform-features-check`.
- Crash reporting e simbolização: fora do escopo (fronteira `sre-observability`).

## Referências

- [references/por-plataforma.md](references/por-plataforma.md), [references/bateria.md](references/bateria.md)
- Compartilhado: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/qualidade-performance-a11y-testes.md`
