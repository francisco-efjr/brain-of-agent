---
name: mobile-test-strategy
description: "Define a estratégia e o plano de testes de apps mobile por camada e por plataforma: unitário, ViewModel com fake, UI (Compose test, XCTest e XCUIAutomation, widget test, React Native Testing Library), integração e E2E (Maestro, Detox, Patrol), mais matriz de risco de dispositivos, ciclo de vida, rede e operações ambíguas. Use para 'como testar', 'plano de testes', 'E2E', 'Maestro', 'Detox', 'XCUITest', 'Compose test', 'integration_test', 'test strategy for my app', 'matriz de dispositivos'. Planeja; escrever e rodar testes é do agente mobile-test-engineer."
argument-hint: "[plataforma] [feature ou fluxo]"
allowed-tools: Read, Grep, Glob
disallowed-tools: Write, Edit, NotebookEdit
---

# mobile-test-strategy

Plano de testes que diz **o que cada teste prova e o que não prova**, por camada e plataforma, com base nos riscos reais do app. Somente leitura. Verificado em 2026-10-10.

Por que começar pelo risco: uma lista genérica de aparelhos não é estratégia; emulação de viewport ou "só emulador Android" não prova permissões, ciclo de vida, armazenamento nem distribuição de loja (brain `qa/mobile.md`, conteúdo próprio MIT). O plano preserva o stack de testes que o projeto já usa se ele atende ao risco.

## Entradas

`$ARGUMENTS` = `[plataforma] [feature ou fluxo]`. Descubra lendo o repositório: framework de teste em uso, `build.gradle(.kts)` (`testImplementation`, `androidTestImplementation`), `Package.swift`/targets de teste, `pubspec.yaml` (`dev_dependencies`), `package.json` (jest, RNTL, detox, maestro), pastas `.maestro/`, `e2e/`, `integration_test/`. Pergunte só o que muda o plano: o app tem dados persistidos, offline, permissões, pagamentos, atualização de versão anterior? Quais aparelhos/SOs têm usuários?

## Pré-checagens

1. **Ambiente.** XCUITest e testes iOS rodam no simulador do Xcode (macOS); fora dele, **Não verificável** (V-66). Detox: aparelho real no iOS não suportado, conferir a faixa de versões de RN (V-70).
2. **Não instale ferramentas.** `curl | bash` de Maestro, `sdkmanager`, `npx tsx` em segundo plano e `npx` sem versão fixa são decisão do usuário; este plano não os executa nem os sugere como passo automático (V-44, S-16).
3. Dados de teste sintéticos; segredos de logs redigidos (S-18).

## Passos

1. **Mapear riscos** (fluxo crítico, dados persistidos, permissões, rede, atualização, troca de conta, pagamentos) e a **base real de dispositivos**. Use a matriz de [references/risco-ciclo-vida-rede.md](references/risco-ciclo-vida-rede.md).
   *Saída:* lista de riscos priorizada (impacto × probabilidade) com dono.
2. **Escolher a ferramenta por camada e plataforma** (tabela em [references/ferramentas-por-plataforma.md](references/ferramentas-por-plataforma.md)):
   - **Android** (V-08): testes pequenos/médios/grandes; locais vs instrumentados; ViewModel com repositório fake; Given/When/Then. UI Compose: `createComposeRule` (V-65). Views: Espresso, sem `sleep` (V-68).
   - **iOS** (V-66): Swift Testing para unitários novos; XCTest/XCUIAutomation para UI e performance; não misturar APIs no mesmo teste.
   - **Flutter** (V-67): unitário, widget, integração; `integration_test` não toca UI nativa (diálogos de permissão, notificações): `patrol`, conferir versão.
   - **React Native** (V-69): ESLint/TypeScript, Jest, RNTL por texto/papel, E2E só para o vital (Detox, Appium ou Maestro). Expo EAS Workflows + Maestro em alfa (V-37).
   *Saída:* tabela camada → ferramenta → o que prova → o que não prova.
3. **Regra de `testID`** (C2): componentes por texto/papel; `testID` só em E2E de app multilíngue (V-69 oficial prevalece sobre V-44).
4. **Cobrir a matriz de ciclo de vida e rede** do passo 1 (interrupção, resposta perdida depois do servidor processar, troca A→B, atualização preservando dados): casos em [references/risco-ciclo-vida-rede.md](references/risco-ciclo-vida-rede.md).
5. **Automação confiável**: contas e registros sintéticos por API/fixture; localizar por semântica ou identificador estável; esperar condição com limite (no Maestro `assertVisible` já espera até o timeout); **nunca repetir ação de negócio para contornar lentidão**; na falha, capturar build, dispositivo/SO, estado inicial, passos, logs redigidos e ID da operação.
6. **Definir metas e baseline antes de comparar** (performance, tempo, taxa de flake) no mesmo perfil. Execução em debug não representa release.
7. **Entregar o plano** no formato abaixo, indicando o que é execução do `mobile-test-engineer` e o que é do usuário.

Critério de saída: cada risco tem pelo menos um teste mapeado ou uma lacuna declarada; cada teste diz o que prova e o que não prova; comandos de verificação listados; nada instalado.

## Verificação

- Comandos candidatos (a confirmar na versão do projeto): Android `./gradlew testDebugUnitTest` (locais) e `./gradlew connectedDebugAndroidTest` (instrumentados); iOS `xcodebuild test` ou Xcode (macOS); Flutter `flutter test` e `flutter test integration_test`; RN `npx jest` e E2E conforme a ferramenta; Expo `npx expo lint`, `npx tsc --noEmit` (V-36). Comandos de Gradle/Flutter/Jest: **Inferido** (conhecimento estável).
- O plano diz o que foi executado. Se só houve emulador Android, **escreva exatamente isso** e não estenda a iOS, aparelho físico ou distribuição de loja (brain `qa/mobile.md`).
- Rótulos: Verificado (V-xx lido), Inferido, Suposição, Não verificável.

## Formato de saída

Use `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/plano-testes-mobile.md` e `matriz-dispositivos-risco.md` se existirem. Exemplo resumido (caso sintético: app de despesas, Android Compose + Room, com sincronização):

```markdown
## Plano de testes — Despesas (Android) — 2026-10-10
Execução até aqui: nenhuma. Dispositivos: a definir com o usuário (base real desconhecida).

| Risco | Camada | Ferramenta | Prova | Não prova |
| --- | --- | --- | --- | --- |
| Cálculo de total e validação | Unitário local | JUnit + fake do repositório (`./gradlew testDebugUnitTest`) | Regra de negócio e estados do ViewModel | Renderização, SO, banco real |
| Tela de lançamento mostra erro | UI Compose | `createComposeRule`, `onNodeWithText` | Estado fake → UI (V-65) | Integração com rede e permissões |
| Resposta perdida após o servidor processar | Integração | Fake de API que "efetiva e não responde" + `opId` | Uma só despesa criada ao reenviar | Latência real da rede |
| Fluxo crítico "lançar despesa" | E2E (poucos) | Maestro (instalação do usuário) | Caminho feliz no aparelho | Todos os modelos e fabricantes |
| Atualização desde a versão anterior | Manual guiado | Perfil sintético na versão N-1, depois instalar a candidata | Migração preserva dados | Rollback de loja |

## Lacunas declaradas
- Sem aparelho físico: consumo de bateria e câmera não cobertos (Não verificável).
- iOS: fora do escopo do plano (sem macOS nesta sessão).

## Execução (do mobile-test-engineer, com comandos aprovados pelo usuário)
1) ...
```

## Gotchas

1. Pirâmide 60/20/5 **não é oficial** (V-08 não traz proporção). Não cite como norma.
2. "Mais estável que Detox/Appium" (V-44) é afirmação do autor, sem benchmark. Não entra no plano como fato.
3. O pré-requisito de macOS do Detox e seus comandos de instalação não foram lidos (V-70, lacuna 10).
4. `testTag` e `useUnmergedTree` no Compose não aparecem na página oficial (V-65): **Inferido**.
5. Dois momentos diferentes: "fechar e abrir" (Home, recriar tela, remover dos recentes, forçar parada, reinstalar). Identifique a transição exata (brain). "Don't keep activities" não prova todos os cenários de morte de processo.
6. CI verde ≠ fluxo funcionando se as asserções forem fracas; captura de tela ≠ prova de persistência.
7. Material de instalação do skill Maestro de terceiros (V-44) tem comandos inseguros; use apenas os padrões de teste (marcador de carregamento, `runFlow` com `when:`, tags `ci`/`smoke`/`wip`, servidor mock).

## Ressalvas e lacunas

XCUIApplication e seletores, setup Gradle do Espresso, instalação do Detox e Patrol não lidos (lacuna 10). Estratégia de testes para Flutter com `patrol`: só a menção na página de V-67. Metas numéricas de cobertura não são oficiais em nenhuma fonte lida.

## Quando delegar

- Escrever ou ajustar testes e rodar comandos já aprovados: agente `mobile-test-engineer` (único com escrita; só em pastas de teste; para após 3 tentativas falhas).
- Revisão de testes escritos: `mobile-pr-reviewer`.
- Teste de push, permissões e links: itens de `mobile-platform-features-check`.
- QA geral e automação web/API: segmento `qa-testing`.

## Referências

- [references/ferramentas-por-plataforma.md](references/ferramentas-por-plataforma.md), [references/risco-ciclo-vida-rede.md](references/risco-ciclo-vida-rede.md)
- Compartilhado: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/qualidade-performance-a11y-testes.md`
