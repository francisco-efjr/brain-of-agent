# Android e Jetpack Compose

Verificado em 2026-10-10. Fontes: V-06 a V-13, V-60, V-62, V-63, V-65, V-68, V-79. Antes de aconselhar, leia `build.gradle(.kts)`, `gradle/libs.versions.toml`, `gradle-wrapper.properties` e o `AndroidManifest.xml` para saber AGP, Kotlin, Compose BOM, `minSdk` e `targetSdk`. Skills oficiais Android `navigation`, `testing`, `performance` e `security` não foram lidas: tudo que disser sobre elas é Inferido.

## Sumário

- [Comandos de verificação](#comandos-de-verificação)
- [Arquitetura](#arquitetura)
- [Estado e efeitos no Compose](#estado-e-efeitos-no-compose)
- [Performance no Compose](#performance-no-compose)
- [Layouts adaptativos](#layouts-adaptativos)
- [Catálogo de skills oficiais](#catálogo-de-skills-oficiais)
- [Testes](#testes)
- [Segundo plano, Doze e vitals](#segundo-plano-doze-e-vitals)
- [Acessibilidade no Compose](#acessibilidade-no-compose)
- [Play Console](#play-console)
- [Armadilhas](#armadilhas)

## Comandos de verificação

Conhecimento estável do domínio (Inferido): confirme os nomes de tarefa no projeto com `./gradlew tasks` (no Windows, `gradlew.bat`).

| Objetivo | Comando típico | Observação |
| --- | --- | --- |
| Testes locais (JVM) | `./gradlew testDebugUnitTest` | ViewModel com fake roda aqui (V-08) |
| Testes instrumentados | `./gradlew connectedDebugAndroidTest` | Exige emulador ou aparelho conectado |
| Lint | `./gradlew lintDebug` | Variante pode mudar |
| Build | `./gradlew assembleDebug` | Para release, `assembleRelease` com assinatura (ação do usuário) |

Cole a saída. Se o ambiente não tem Android SDK ou emulador, diga "Não verificável".

## Arquitetura

Checklist de PR (V-07): separação de responsabilidades; **fonte única de verdade** com dono único; **fluxo unidirecional**; ao menos duas camadas (UI e dados), domínio opcional; `Context` apenas em componentes de app, fora da regra de negócio; operações main-safe; offline-first com banco como fonte de verdade "tipicamente"; Hilt recomendado pela página. É orientação, não norma: o repositório decide.

Repositório por tipo de dado; ViewModel expõe estado imutável; UI observa e emite eventos. Offline-first e sincronização: [dados-push-permissoes-seguranca.md](dados-push-permissoes-seguranca.md).

## Estado e efeitos no Compose

Fonte: V-10 (chrisbanes/skills, Apache-2.0, classe B). Quatro regras:

1. **Um dono por estado**, o mais baixo possível; só suba o dono com evidência.
2. **Efeito com chave semântica** e ciclo de vida do dono (`LaunchedEffect(userId)`, não `LaunchedEffect(Unit)` por hábito).
3. **Tela em três partes:** ligação de dados (observa o ViewModel), state holder e conteúdo imutável com callbacks.
4. **Revisão sem achado** é um resultado válido quando não há evidência.

Os anti-padrões dessa skill são inferidos pelo validador: rotule Inferido ao citá-los. Snippet S-19 resume a regra.

## Performance no Compose

Protocolo (V-11, classe B): (1) reproduzir uma transição; (2) classificar o eixo: **estabilidade**, **fase de leitura de State** ou **escrita de snapshot**; (3) descartar falsos positivos; (4) mudar um eixo; (5) remedir a mesma captura; (6) manter ou reverter.

Pontos de `references/stability.md` da mesma fonte (não do SKILL.md): strong skipping é o padrão a partir do Kotlin 2.0.20; `@Immutable` e `@Stable` são promessas e não devem calar o relatório do compilador; use `ImmutableList` na fronteira quando precisar. Folclore de estabilidade sem medição é antipadrão (C14). A fonte não exige benchmark nem baseline profile (lacuna): se o projeto os usa, é um bônus, não um requisito desta base. Para listas, `items(..., key = { it.id })` é conhecimento estável (Inferido) e consta no eval do plugin.

Template: `assets/templates/relatorio-performance.md`. Prompt: P-08 na skill `prompts`.

## Layouts adaptativos

Skill oficial `jetpack-compose/adaptive` (V-12, Apache-2.0, atualizada em 2026-09-22): pré-requisitos Compose e Navigation 3 (senão sugerir os skills de migração); `NavigationSuiteScaffold`; multipainel via `SceneStrategy`, **sem** `ListDetailPaneScaffold` nem `SupportingPaneScaffold`; `Grid` experimental só com confirmação do usuário; testes de screenshot sem atualizar as imagens de referência sem revisão humana. Depende de APIs recentes (Compose 1.11 beta para `Grid`): confira a versão do BOM.

## Catálogo de skills oficiais

Verificado (V-06): repositório `android/skills` (Apache-2.0) com 21 diretórios no topo, 17 de domínio: `build-system, camera, device-ai, devtools, identity, jetpack-compose, media, navigation, performance, play, profilers, security, system, testing, tv, wear, xr`. A página oficial dá `android skills list` e `android skills add <nome>`; o caminho de instalação de skills próprios (`.skills/`, `.agent/skills/`, `.agents`) diverge entre fontes: confira na versão do CLI. Não instale nada pelo plugin; leia antes (V-02). Alegações de "70% menos tokens" e "3x mais rápido" são Não verificáveis.

O domínio `build-system` existe e não foi lido (lacuna 3); para falhas de build use a skill `mobile-build-troubleshoot`.

## Testes

| Camada | Regra | Fonte |
| --- | --- | --- |
| Pequenos (locais) | ViewModel com repositório fake; Given/When/Then | V-08 |
| Médios e grandes | Instrumentados para o fluxo principal; poucos testes grandes | V-08 |
| Compose | `androidTestImplementation("androidx.compose.ui:ui-test-junit4:...")` e `debugImplementation("androidx.compose.ui:ui-test-manifest:...")` (este necessário para `createComposeRule()`, não para `createAndroidComposeRule<Activity>()`); `setContent`, `onNodeWithText`, `performClick`, `assertIsDisplayed`; sincroniza com a UI ociosa | V-65 |
| Views (Espresso) | Espera a fila de mensagens, `AsyncTask` e recursos ociosos a cada `onView()`; sem `sleep` nem polling; idling resources para trabalho assíncrono próprio | V-68 |

`testTag` e `useUnmergedTree` não aparecem na página de Compose lida: Inferido. Proporções de pirâmide (60/20/5) não são oficiais. Apps mistos podem usar Espresso e Compose test juntos (Inferido). Setup Gradle do Espresso não foi lido.

## Segundo plano, Doze e vitals

- **WorkManager** (V-60, classe B): `Worker.doWork()` em thread de segundo plano; `WorkRequest` define como e quando; `OneTimeWorkRequest`; `Result.success()`, `failure()`, `retry()`. Para trabalho adiável que precisa sobreviver ao fechamento do app. A página não menciona alarmes: horário exato é outro mecanismo (conferir na documentação de alarmes). Por worker: idempotente, nome único contra duplicação, restrição de rede declarada, `retry` com política.
- **Doze e App Standby** (V-63): com o aparelho parado, desconectado e de tela desligada, a rede é suspensa, wake locks são ignorados, alarmes comuns são adiados, sem JobScheduler (a página diz que o WorkManager também não roda); `setAlarmClock()` ainda dispara. Mensagens por FCM, de alta prioridade só se gerarem notificação; payload com dados suficientes; `setAndAllowWhileIdle`/`setExactAndAllowWhileIdle` no máximo um alarme a cada nove minutos por app. Testes em **emulador**: `adb shell dumpsys deviceidle force-idle` e `unforce`; `am set-inactive` para App Standby. Esses comandos alteram o estado do aparelho de teste.
- **Android vitals** (V-62, verificado em 2026-10-10): sessão excessiva = mais de 2 h acumuladas de wake locks parciais não isentos em 24 h; limiar quando 5% das sessões dos últimos 28 dias são excessivas; investigar tags com duração P90 ou P99 acima de 60 min; a partir de 2026-03-01 o título "pode" ser excluído de superfícies de descoberta e "em alguns casos" receber aviso na ficha (consequências são possibilidades; a aplicação atual não foi confirmada). Reconfira o post.
- Restrições e backoff do WorkManager e o encaixe dele na janela de manutenção do Doze não foram lidos (lacuna 8).

## Acessibilidade no Compose

V-09 e V-79: `contentDescription` única e sem repetir o tipo, `null` em ícones decorativos; `Modifier.semantics { }`, `mergeDescendants`, `heading()`, `paneTitle` (API 28+), `hideFromAccessibility`/`clearAndSetSemantics`; ações de gesto via `customActions`; tamanho mínimo de 48 dp (`Button` e `IconButton` já aplicam; elementos personalizados precisam de `sizeIn(minWidth = 48.dp, minHeight = 48.dp)`); contraste 4,5:1 abaixo de 18 sp (ou negrito abaixo de 14 sp) e 3:1 no restante; não depender só de cor. `onClickLabel` aparece só indiretamente na página (o exemplo usa `onLongClickLabel`). "Material 3" oficial não foi lido (m3.material.io sem conteúdo recuperável): não o cite.

## Play Console

Itens de loja do Android (target API, exclusão de conta, Data safety, localização em segundo plano) estão em [loja-release-ambiente.md](loja-release-ambiente.md).

## Armadilhas

- A página de WorkManager e a de Doze parecem se contradizer: não se contradizem. Em Doze o trabalho espera a janela de manutenção; horário exato e mensagem crítica têm mecanismos próprios (C5).
- Evite `play-policy-insights` executando scripts Python do repositório: o plugin só destila o checklist (V-13).
- Pirâmide de testes 60/20/5 e "mais estável que Detox/Appium" não são fatos desta base.
- Relatos de praticantes sobre Android Studio (V-51, classe C) servem como checklist de revisão de código gerado: convenções existentes, APIs obsoletas, ciclo de vida e recomposição no diff, stack trace completo, diff revisado como PR.
