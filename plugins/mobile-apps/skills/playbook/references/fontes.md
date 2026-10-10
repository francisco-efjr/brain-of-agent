# Fontes validadas do segmento Aplicativos mobile

Data de consulta de todas as linhas: 2026-10-10 (um validador, claude-sonnet-5-5, reabriu as páginas; a pesquisa foi feita por outro modelo da mesma família, então a independência é parcial). Itens `V-nn` são os da base de evidência do segmento; as referências do plugin citam esses códigos.

Classes: **A** = fonte primária ou oficial · **B** = autor reconhecido ou repositório com sinais · **C** = relato de praticante ou comunidade (serve de hipótese, não de regra). Nota entre parênteses = nota 0 a 10 do validador. "doc. (destilar)" = texto de documentação sem licença permissiva observada: o plugin usa redação própria e não copia. Estrelas e datas de push são sinais, não prova de qualidade, e vieram da API ou da página do repositório na data da consulta.

Códigos de rastreio que aparecem nas skills: `Cn` (por exemplo C6) é um conflito entre fontes já resolvido no desenho do segmento, e a resolução está escrita na própria frase que o cita; `lacuna n` é um tema sem fonte lida, e o que depende dele sai como Inferido, Suposição ou Não verificável. As listas completas ficam em `docs/research/mobile-apps/SYNTHESIS.md` (seções 3.2 e 7.3) no repositório `dev-segments`, fora do plugin; não é preciso abri-las para aplicar as regras.

## Sumário

- [Claude Code, skills e avaliação](#claude-code-skills-e-avaliação)
- [Android](#android)
- [iOS e Swift](#ios-e-swift)
- [React Native, Expo e Flutter](#react-native-expo-e-flutter)
- [Loja, release e ambiente](#loja-release-e-ambiente)
- [Dados, push, permissões e segurança](#dados-push-permissões-e-segurança)
- [Acessibilidade, bateria e testes](#acessibilidade-bateria-e-testes)
- [Conteúdo próprio e de terceiros do brain-of-agent](#conteúdo-próprio-e-de-terceiros-do-brain-of-agent)
- [Rejeitadas ou só como sinal](#rejeitadas-ou-só-como-sinal)
- [Lacunas de leitura](#lacunas-de-leitura)

## Claude Code, skills e avaliação

| V | Título | URL | Classe | Licença e sinais |
| --- | --- | --- | --- | --- |
| V-01 | Boas práticas de autoria de skills (Anthropic) | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | A (9) | doc. (destilar) |
| V-02 | Equipping agents with Agent Skills (Anthropic Engineering) | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | A (9) | doc. (destilar); publicado 2025-10-16, atualizado 2025-12-18 |
| V-03 | Best practices for Claude Code | https://code.claude.com/docs/en/best-practices | A (9) | doc. (destilar) |
| V-04 | Skills no Claude Code (frontmatter e carga) | https://code.claude.com/docs/en/skills | A (9) | doc. (destilar); últimos ~6,6 mil caracteres não lidos |
| V-05 | skill-creator (anthropics/skills) | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | A (8) | licença nula na API e no frontmatter: destilar; 180.198 estrelas, push 2026-10-09 |
| V-49 | Prompt do revisor adversarial mobile | original do validador, sem URL | B (derivada) | original do projeto; base: V-03 |

## Android

| V | Título | URL | Classe | Licença e sinais |
| --- | --- | --- | --- | --- |
| V-06 | Catálogo oficial android/skills | https://developer.android.com/tools/agents/android-skills · https://github.com/android/skills | A (9) | Apache-2.0; 7.743 estrelas, push 2026-09-25; 21 diretórios no topo, 17 de domínio |
| V-07 | Guia de arquitetura Android | https://developer.android.com/topic/architecture | A (9) | doc. (destilar) |
| V-08 | Fundamentos de teste Android | https://developer.android.com/training/testing/fundamentals | A (9) | doc. (destilar) |
| V-09 | Acessibilidade Android: princípios e API padrão do Compose | https://developer.android.com/guide/topics/ui/accessibility/principles · https://developer.android.com/develop/ui/compose/accessibility/api-defaults | A (9) | doc. (destilar) |
| V-10 | compose-state-and-effects (chrisbanes/skills) | https://raw.githubusercontent.com/chrisbanes/skills/main/skills/compose-state-and-effects/SKILL.md | B (6) | Apache-2.0; ~1,1 mil estrelas (página) |
| V-11 | compose-performance (chrisbanes/skills) | https://raw.githubusercontent.com/chrisbanes/skills/main/skills/compose-performance/SKILL.md | B (6) | Apache-2.0; referência `stability.md` |
| V-12 | Skill oficial de layouts adaptativos | https://raw.githubusercontent.com/android/skills/main/jetpack-compose/adaptive/SKILL.md | A (9) | Apache-2.0; atualizado 2026-09-22 |
| V-13 | play-policy-insights (android/skills) | https://raw.githubusercontent.com/android/skills/main/play/play-policy-insights/SKILL.md | A (8) | Apache-2.0; executa scripts Python: não executar |
| V-14 | Requisito de target API do Google Play | https://developer.android.com/google/play/requirements/target-sdk | A (9) | doc. (destilar); página "Last updated 2026-10-01" |
| V-15 | Exclusão de conta no Google Play | https://support.google.com/googleplay/android-developer/answer/13327111 | A (9) | doc. (destilar) |
| V-54 | POST_NOTIFICATIONS no Android 13+ | https://developer.android.com/develop/ui/views/notifications/notification-permission | A (9) | doc. (destilar) |
| V-55 | Firebase Cloud Messaging no Android | https://firebase.google.com/docs/cloud-messaging/android/get-started | A (8) | doc. (destilar) |
| V-56 | Permissões em tempo de execução (Android) | https://developer.android.com/training/permissions/requesting | A (9) | doc. (destilar) |
| V-57 | Localização em segundo plano (política do Google Play) | https://support.google.com/googleplay/android-developer/answer/9799150 | A (9) | doc. (destilar); sem data na página |
| V-59 | Offline-first no Android | https://developer.android.com/topic/architecture/data-layer/offline-first | A (9) | doc. (destilar) |
| V-60 | WorkManager: trabalho persistente | https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started | B (7) | doc. (destilar) |
| V-62 | Android vitals: wake locks parciais excessivos | https://developer.android.com/blog/posts/raising-the-bar-on-battery-performance-excessive-partial-wake-locks-metric-is-now-out-of-beta | A (9) | doc. (destilar); post de 2025-11-10 |
| V-63 | Doze e App Standby | https://developer.android.com/training/monitoring-device-state/doze-standby | A (9) | doc. (destilar) |
| V-65 | Testes de UI no Compose | https://developer.android.com/develop/ui/compose/testing | A (9) | doc. (destilar) |
| V-68 | Espresso | https://developer.android.com/training/testing/espresso | B (7) | doc. (destilar) |
| V-79 | Acessibilidade Android: alvo de 48 dp e contraste | https://developer.android.com/guide/topics/ui/accessibility/apps | A (9) | doc. (destilar); m3.material.io sem conteúdo recuperável |
| V-82 | Android Keystore | https://developer.android.com/privacy-and-security/keystore | A (9) | doc. (destilar) |
| V-76 | Gradle Play Publisher (Triple-T) | https://github.com/Triple-T/gradle-play-publisher | B (5) | MIT; ~4,3 mil estrelas (página); modo de manutenção; não é oficial do Google |

## iOS e Swift

| V | Título | URL | Classe | Licença e sinais |
| --- | --- | --- | --- | --- |
| V-16 | App Review Guidelines (Apple) | https://developer.apple.com/app-store/review/guidelines/ | A (9) | doc. (destilar); fim da seção 5 (após 5.3.4) não lido |
| V-17 | Privacy manifest files | https://developer.apple.com/documentation/bundleresources/privacy-manifest-files | A (9) | doc. (destilar); lido pelo endpoint JSON da documentação |
| V-18 | HIG: acessibilidade (JSON) | https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json | A (9) | doc. (destilar) |
| V-19 | SwiftUI Pro (Paul Hudson) | https://github.com/twostraws/SwiftUI-Agent-Skill · https://www.hackingwithswift.com/articles/282/swiftui-agent-skill-claude-codex-ai | A (9) | MIT; ~5,5 mil estrelas (página); versão 2.0.0; o artigo 284 do mesmo site é piada de 1º de abril: ignorar; `swiftui-pro/references/accessibility.md` (12 regras) aberto pelo validador de qualidade em 2026-10-10 e resumido com redação própria em `ios-swift.md` |
| V-20 | Swift Concurrency (Antoine van der Lee) | https://raw.githubusercontent.com/AvdLee/Swift-Concurrency-Agent-Skill/main/skills/swift-concurrency/SKILL.md | A (8) | MIT; 1.678 estrelas, push 2026-09-14; rodapé promocional com link de rastreamento: ignorar |
| V-21 | swift-concurrency-expert (Dimillian) | https://raw.githubusercontent.com/Dimillian/Skills/main/swift-concurrency-expert/SKILL.md | B (6) | MIT; 3.989 estrelas, push 2026-03-29 |
| V-22 | swiftui-performance-audit (Dimillian) | https://raw.githubusercontent.com/Dimillian/Skills/main/swiftui-performance-audit/SKILL.md | B (6) | MIT |
| V-23 | swiftui-view-refactor (Dimillian) | https://raw.githubusercontent.com/Dimillian/Skills/main/swiftui-view-refactor/SKILL.md | B (6) | MIT; "MV antes de MVVM" é opinião do autor |
| V-24 | app-store-changelog (Dimillian) | https://raw.githubusercontent.com/Dimillian/Skills/main/app-store-changelog/SKILL.md | B (6) | MIT; script não lido nem executado |
| V-52 | Registro no APNs e token de dispositivo | https://developer.apple.com/documentation/usernotifications/registering-your-app-with-apns.md | A (9) | doc. (destilar) |
| V-53 | Autorização de notificações (UNUserNotificationCenter) | https://developer.apple.com/tutorials/data/documentation/usernotifications/asking-permission-to-use-notifications.json | A (8) | doc. (destilar); a página não trata de negação |
| V-58 | Purpose strings e privacidade no iOS | https://developer.apple.com/documentation/uikit/requesting-access-to-protected-resources.md · https://developer.apple.com/documentation/uikit/protecting-the-user-s-privacy.md · https://developer.apple.com/documentation/bundleresources/information-property-list/nslocationwheninuseusagedescription.md · https://developer.apple.com/documentation/bundleresources/information-property-list/nscamerausagedescription.md | A (9) | doc. (destilar) |
| V-61 | SwiftData com sincronização iCloud | https://developer.apple.com/documentation/swiftdata/syncing-model-data-across-a-persons-devices.md | A (9) | doc. (destilar); sem resolução de conflito descrita |
| V-64 | Energia no iOS: índice atual e Low Power Mode (arquivado) | https://developer.apple.com/tutorials/data/documentation/xcode/reducing-your-app-s-battery-use.json · https://developer.apple.com/library/archive/documentation/Performance/Conceptual/EnergyGuide-iOS/LowPowerMode.html | B (6) | doc. (destilar); a página arquivada é de 2016-09-13 |
| V-66 | XCTest, Swift Testing e XCUIAutomation | https://developer.apple.com/tutorials/data/documentation/xctest.json | A (8) | doc. (destilar) |
| V-78 | VoiceOver: auditoria, rótulos, dicas e agrupamento | https://developer.apple.com/documentation/uikit/supporting-voiceover-in-your-app.md | A (9) | doc. (destilar) |
| V-80 | Swift Concurrency Migration Guide (`MigrationStrategy.md`) | https://github.com/swiftlang/swift-migration-guide · https://raw.githubusercontent.com/swiftlang/swift-migration-guide/main/Guide.docc/MigrationStrategy.md | B (7) | Apache-2.0; 357 estrelas; `Guide.docc/Guide.md` não existe (404) |
| V-83 | Keychain: acessibilidade e presença do usuário | https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility.md | A (9) | doc. (destilar) |
| V-38 | release-review (rshankras/claude-code-apple-skills) | https://raw.githubusercontent.com/rshankras/claude-code-apple-skills/main/skills/release-review/SKILL.md | B (6) | MIT; 787 estrelas; só formato de relatório e padrão somente leitura |

## React Native, Expo e Flutter

| V | Título | URL | Classe | Licença e sinais |
| --- | --- | --- | --- | --- |
| V-26 | Guia de arquitetura Flutter | https://docs.flutter.dev/app-architecture/guide | A (9) | doc. (destilar) |
| V-27 | Skill Flutter de arquitetura em camadas | https://raw.githubusercontent.com/flutter/agent-plugins/main/skills/flutter-apply-architecture-best-practices/SKILL.md | B (7) | BSD-3-Clause; 3.042 estrelas; exemplos com bugs: só o processo de 8 passos |
| V-28 | Skill Flutter de layout responsivo | https://raw.githubusercontent.com/flutter/agent-plugins/main/skills/flutter-build-responsive-layout/SKILL.md | B (7) | BSD-3-Clause; exemplos com erro de layout: só as regras |
| V-29 | Boas práticas de performance Flutter | https://docs.flutter.dev/perf/best-practices | A (9) | doc. (destilar) |
| V-30 | Performance do React Native | https://reactnative.dev/docs/performance | A (9) | doc. (destilar) |
| V-31 | Vercel react-native-skills | https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/react-native-skills/SKILL.md | B (7) | licença nula na API e MIT no arquivo: destilar; 32.136 estrelas; 8 categorias no SKILL.md |
| V-32 | Callstack react-native-best-practices | https://raw.githubusercontent.com/callstackincubator/agent-skills/main/skills/react-native-best-practices/SKILL.md | A (8) | MIT; 1.665 estrelas, push 2026-10-08 |
| V-33 | expo-router (expo/skills) | https://raw.githubusercontent.com/expo/skills/main/plugins/expo/skills/expo-router/SKILL.md | A (8) | MIT; 2.685 estrelas; v1.0.1 |
| V-36 | AGENTS.md do Expo e guia para Claude Code | https://docs.expo.dev/agents/claude.md · https://raw.githubusercontent.com/expo/expo/main/packages/create-expo/template/agent-files/AGENTS.md | A (9) | MIT (template); doc. (destilar) |
| V-37 | E2E com Maestro no EAS Workflows | https://docs.expo.dev/tutorial/cicd/e2e-tests.md | A (8) | doc. (destilar); recurso em alfa |
| V-47 | Instruções Dart/Flutter (awesome-copilot) | https://raw.githubusercontent.com/github/awesome-copilot/main/instructions/dart-n-flutter.instructions.md | B (5) | MIT; 39.874 estrelas; "go_router em 90% dos apps" sem fonte |
| V-67 | Testes no Flutter | https://docs.flutter.dev/testing/overview | A (9) | doc. (destilar) |
| V-69 | Estratégia de testes no React Native | https://reactnative.dev/docs/testing-overview | A (9) | doc. (destilar) |
| V-70 | Detox | https://github.com/wix/Detox | B (7) | MIT; ~12,0 mil estrelas (página) |
| V-81 | React Navigation: instalação | https://reactnavigation.org/docs/getting-started.md | A (8) | doc. (destilar) |
| V-84 | Kotlin Multiplatform: iOS exige macOS com Xcode | https://kotlinlang.org/docs/multiplatform/quickstart.html | A (8) | doc. (destilar) |

## Loja, release e ambiente

| V | Título | URL | Classe | Licença e sinais |
| --- | --- | --- | --- | --- |
| V-34 | eas-update (expo/skills) | https://raw.githubusercontent.com/expo/skills/main/plugins/expo/skills/eas-update/SKILL.md | A (8) | MIT; `allowed-tools` original amplo (`Bash(eas *)`) |
| V-35 | eas-app-stores (expo/skills) | https://raw.githubusercontent.com/expo/skills/main/plugins/expo/skills/eas-app-stores/SKILL.md | A (8) | MIT; sem gate de confirmação: usado só com a reescrita do plugin |
| V-71 | fastlane match | https://docs.fastlane.tools/actions/match/ | A (8) | doc. (destilar) |
| V-72 | fastlane pilot | https://docs.fastlane.tools/actions/pilot/ | A (8) | doc. (destilar) |
| V-73 | Distribuição pelo Xcode: archive, TestFlight, App Store | https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases.md | A (9) | doc. (destilar) |
| V-74 | Xcode Cloud | https://developer.apple.com/xcode-cloud/ | A (8) | doc. (destilar); preços datados |
| V-75 | EAS Build | https://docs.expo.dev/build/introduction/ | A (8) | doc. (destilar) |
| V-77 | Claude Code no celular e na nuvem | https://code.claude.com/docs/en/mobile.md | A (9) | doc. (destilar) |
| V-41 | claude-plugins-official (swift-lsp, kotlin-lsp, expo) | https://github.com/anthropics/claude-plugins-official | B (7) | Apache-2.0; 37.592 estrelas, push 2026-10-09; README de swift-lsp não lido |
| V-39 | XcodeBuildMCP (agora também MobileBuildMCP) | https://github.com/cameroncooke/XcodeBuildMCP | B (6) | MIT; ~6,5 mil estrelas (página) |

## Dados, push, permissões e segurança

| V | Título | URL | Classe | Licença e sinais |
| --- | --- | --- | --- | --- |
| V-25 | OWASP MASVS | https://mas.owasp.org/MASVS/ | A (9) | doc. (destilar); níveis e IDs de controle não lidos; MASTG não aberto |
| V-40 | Deep links: App Links e Universal Links | https://developer.android.com/training/app-links/verify-android-applinks · https://developer.apple.com/documentation/xcode/supporting-associated-domains | B (7) | doc. (destilar) |
| V-45 | Checklist offline-first (secondsky) | https://raw.githubusercontent.com/secondsky/claude-skills/main/plugins/mobile-offline-support/skills/mobile-offline-support/SKILL.md | C (4) | MIT; 227 estrelas; exemplo com bugs: só a lista reescrita |

(V-52 a V-61 e V-82 a V-83 estão nas tabelas de Android e iOS.)

## Acessibilidade, bateria e testes

| V | Título | URL | Classe | Licença e sinais |
| --- | --- | --- | --- | --- |
| V-48 | Checklist de acessibilidade mobile (dadederk/ios-accessibility-agent-skill + V-09 e V-18) | https://github.com/dadederk/ios-accessibility-agent-skill | B (7) | MIT; 174 estrelas; README avisa que é trabalho em andamento; números vêm de V-09 e V-18 |
| V-44 | Padrões de fluxos Maestro (tovimx) | https://cdn.jsdelivr.net/gh/tovimx/maestro-mobile-testing-skill@main/SKILL.md | C (4) | MIT; instala com `curl` com pipe para `bash`: só os padrões de teste |
| V-46 | Axiom: skills roteadoras | https://github.com/charleswiltgen/axiom · https://charleswiltgen.github.io/Axiom/ | B (5) | MIT; ~1,2 mil estrelas (página); 276 skills declaradas: padrão, não instalação |
| V-43 | claude-swift-engineering | https://github.com/johnrogers/claude-swift-engineering | C (5) | MIT; 231 estrelas, push 2026-01-18; conteúdo dos agentes não relido |
| V-42 | Relatos iOS: Tolans, Crosley, keskinonur | https://www.tolans.com/relay/how-we-claudified-our-ios-app-without-wrecking-our-codebase · https://blakecrosley.com/guides/ios-agent-development · https://github.com/keskinonur/claude-code-ios-dev-guide | C (4) | keskinonur sem licença (843 estrelas): só destilação; alegações de ganho não verificáveis |
| V-50 | App macOS/SwiftUI feito com Claude Code (via Simon Willison) | https://simonwillison.net/2025/Jul/6/macos-app-built-entirely-by-claude-code/ | C (3) | relato de uma pessoa, de mais de um ano |
| V-51 | Claude Code no Android Studio (Sagnik Bhattacharya) | https://sagnikbhattacharya.com/blog/claude-code-android-studio | C (3) | blog pessoal, sem métricas |

## Conteúdo próprio e de terceiros do brain-of-agent

| Arquivo | Natureza | Uso no plugin |
| --- | --- | --- |
| `brains/qa/references/mobile.md` | Próprio do usuário (MIT, Francisco Edson), repositório francisco-efjr/brain-of-agent, commit 0d025fb | Incorporado e adaptado: matriz por risco, ciclo de vida, rede e operação ambígua, permissões, atualização, automação confiável, roteiro de release |
| `brains/fullstack/references/apple-design.md` | Próprio (MIT) | Adaptado ao iOS/iPadOS: critérios locais de acabamento. As métricas do arquivo de inspiração (13 pt, margens de 20 pt, alvo de 20x20 pt) são Não verificadas e não entram |
| `brains/fullstack/assets/templates/*` e `brains/qa/assets/templates/*` | Próprios (MIT) | Base dos templates em `assets/templates/` |
| `vendor/gstack/ios-qa/SKILL.md` e `vendor/gstack/ios-design-review/SKILL.md` | gstack, MIT, Copyright (c) 2026 Garry Tan | Só ideias de processo, destiladas com atribuição: tiers de evidência, ponte de depuração apenas em Debug, rubrica de 10 dimensões. Nenhum comando, binário ou texto em bloco foi copiado |

URLs citadas pelo brain e **não reabertas** na construção do plugin (conferir antes de citar): https://developer.android.com/studio/debug/dev-options · https://appium.io/docs/en/latest/intro/drivers/ · https://developer.apple.com/documentation/xcuiautomation · https://docs.maestro.dev/reference/commands-available/assertvisible · https://developer.apple.com/design/human-interface-guidelines/ (HIG geral).

## Rejeitadas ou só como sinal

- Regras SwiftUI do awesome-cursorrules: desatualizadas (centradas em `@StateObject`/`@ObservedObject`, `[weak self]` por padrão, `Task.detached` para trabalho pesado).
- Guia de 6 estrelas com `curl | bash`, `sudo`, `npx -y` sem versão fixa e hook que reescreve todo comando Bash: não herdar nada.
- Blogs de fornecedores sobre taxa de rejeição: nunca abertos, números divergentes.
- Alegações não verificáveis (não entram como fato): "100 mil linhas em um dia", "70% menos tokens", "3x mais rápido", "mais estável que Detox/Appium".
- Hacker News: item de baixa tração (5 pontos); nenhum Reddit, X ou YouTube verificável. A comunidade é sinal fraco neste segmento.

## Lacunas de leitura

Não lidos pelo validador, logo qualquer conteúdo que dependa deles é Inferido: níveis e controles do MASVS e o MASTG; skills Android `navigation`, `testing`, `performance` e `security`; Material 3 oficial; payload de push, notificações silenciosas e FCM no iOS; chaves de privacidade iOS além de câmera e localização; conflito do CloudKit; restrições e backoff do WorkManager; artigos de energia do iOS e Power Profiler; XCUIApplication e seletores, setup do Espresso, instalação do Detox e Patrol; App Store Connect Help, TestFlight Beta App Review e `fastlane deliver`; `createNativeStackNavigator`; demais páginas do guia de migração Swift; arquitetura de Kotlin Multiplatform. Reabra a fonte antes de afirmar qualquer coisa nessas áreas.
