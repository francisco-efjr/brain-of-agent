# React Native, Expo, Flutter e Kotlin Multiplatform

Verificado em 2026-10-10. Fontes: V-26 a V-37, V-44, V-47, V-67, V-69, V-70, V-81, V-84. Antes de aconselhar, leia a versão da stack: `package.json` (react-native, expo, react-navigation), `app.json`/`app.config.*`, `eas.json`, `pubspec.yaml`. Em Windows, o lado Android e a lógica compartilhada funcionam localmente; iOS passa por build na nuvem (Inferido, V-75) ou macOS (V-84).

## Sumário

- [Comandos de verificação](#comandos-de-verificação)
- [React Native: performance](#react-native-performance)
- [Expo: projeto, rotas e AGENTS.md](#expo-projeto-rotas-e-agentsmd)
- [Expo: OTA e release](#expo-ota-e-release)
- [React Navigation sem Expo Router](#react-navigation-sem-expo-router)
- [Testes em React Native](#testes-em-react-native)
- [Flutter: arquitetura](#flutter-arquitetura)
- [Flutter: layout responsivo e performance](#flutter-layout-responsivo-e-performance)
- [Flutter: testes](#flutter-testes)
- [Kotlin Multiplatform](#kotlin-multiplatform)
- [Lacunas](#lacunas)

## Comandos de verificação

| Stack | Comandos | Status |
| --- | --- | --- |
| Expo | `npx expo lint`, `npx tsc --noEmit`, `npx expo-doctor`, `npx expo install --fix` | Verificado (V-36); conferir na versão do SDK |
| React Native sem Expo | Scripts do `package.json` (lint, test, tsc) | Leia os scripts do projeto |
| Flutter | `flutter analyze`, `flutter test` | Inferido (conhecimento estável); confirme na versão |

## React Native: performance

Oito pontos oficiais (V-30), em ordem de uso:

1. Dev mode é lento: meça em **release**.
2. `console.*` trava a thread JS: remova no release (plugin Babel `transform-remove-console`).
3. `getItemLayout` nas listas (útil quando a altura dos itens é conhecida, Inferido).
4. FlashList e Legend List, citadas pela página como alternativas para listas longas.
5. `useNativeDriver` nas animações.
6. `requestAnimationFrame` dentro de `onPress`.
7. Entenda a separação entre a thread JS e a thread de UI.
8. Use o Perf Monitor.

Camada de prioridades da skill de Vercel (V-31, classe B, licença nula na API e MIT no arquivo: destilado): listas virtualizadas (crítica); animar só transform e opacidade, navegadores nativos, UI (alta); estado e renderização (média); configuração (baixa). Preferências como `Pressable` no lugar de `TouchableOpacity` e `expo-image` são **preferência da skill**, nunca erro (C7). Contagem de categorias: 8 no SKILL.md (o AGENTS.md diz 13 e lista 14): use o SKILL.md (C10).

Ciclo da Callstack (V-32, MIT): medir; otimizar um ponto; remedir; validar e reverter se não houver ganho; sem memoização sem problema medido; para TTI medir só cold start; conferir a versão da biblioteca antes de aplicar uma correção específica; carregamento de chunks remotos, polyfill de `Intl` e compressão de bundle pedem revisão; `npx` com versão fixa. Prompt P-13.

## Expo: projeto, rotas e AGENTS.md

Template e guia oficiais (V-36): ler a versão major de `expo` e a documentação correspondente; `npx expo install` para dependências; validar com `npx expo lint`, `npx tsc --noEmit`, `npx expo-doctor`; Expo Router com telas em `src/app/`; **não editar `ios/` e `android/`** à mão; módulo nativo exige development build; EAS para build, submit e OTA. O contexto do agente é `AGENTS.md` (o Claude Code lê direto a partir da versão 2.1.277). Modelo em `assets/templates/agents-md-expo.md`.

Rotas (V-33, expo/skills, MIT, v1.0.1): rotas só em `app`; uma rota para `/` é obrigatória (pode estar num grupo); nomes em kebab-case; modais com `presentation: "modal"`; no SDK 56 ou superior, importar de `expo-router/react-navigation`; `headerLargeTitle` está depreciado (SDK 56+: `headerLargeTitleEnabled`). O template usa `src/app/`: leia a estrutura do projeto e siga-a (C8). Detalhes de deep links no Expo Router não foram lidos.

Plugin oficial `expo@claude-plugins-official` (V-36): instalação e riscos em [ferramentas-e-mcp.md](ferramentas-e-mcp.md); o plugin não o instala.

## Expo: OTA e release

Modelo de gate (V-34, expo/skills, MIT; nota 90, a melhor skill do conjunto):

- Só JavaScript, estilo e assets vão por OTA; qualquer mudança nativa exige build.
- `runtimeVersion` é a fronteira e não muda por conveniência; o canal fica na build e aponta para um branch.
- Produção só com pedido ou aprovação explícita, nunca inferida pelo branch do git.
- Antes de publicar, confirmar projeto, canal, ambiente, plataformas, runtime e mensagem.
- A fonte traz um checklist de seis itens para o caso "a build não atualiza". Os itens não foram enumerados na base: abra o `SKILL.md` de `eas-update` (URL em `fontes.md`) e use a lista dele, sem inventar.
- A fonte **não descreve rollback**: aponte a documentação do EAS.

`eas-app-stores` (V-35) mostra o fluxo `eas init`, `eas build:configure`, build de produção, `--auto-submit` ou `npx testflight`, monitoramento com `eas build:list`/`eas submit:list` e as trilhas Android (interna, fechada, aberta, produção). Ele não tem gate de confirmação: no plugin, `--auto-submit`, `eas submit` e atalhos de TestFlight só rodam com ficha de ação confirmada (`assets/templates/ficha-acao-release.md`). O `allowed-tools` original de V-34 permite `Bash(eas *)`; a skill do plugin não pré-aprova nada. EAS Build roda iOS em macOS runners da Expo; a página não diz "sem Mac" nem exige conta Apple (implícito) (V-75). Pipeline completo: [loja-release-ambiente.md](loja-release-ambiente.md).

## React Navigation sem Expo Router

V-81: pacote `@react-navigation/native`; dependências comuns dos navegadores `react-native-screens` e `react-native-safe-area-context`; em Expo, `npx expo install` casa versões com o SDK; em projeto nativo no Mac, `npx pod-install ios`; no Android, `react-native-screens` exige `supportFragmentManager.fragmentFactory = RNScreensFragmentFactory()` em `MainActivity.onCreate` (a página não diz se vale para Expo); o gesto de voltar preditivo ainda não é suportado, então desligue com `android:enableOnBackInvokedCallback="false"`; mínimos React Native 0.72.0, Expo 52 (com Expo Go) e TypeScript 5.0.0. Fixe a versão do `create-expo-app` em vez de `@latest`. `createNativeStackNavigator` e a camada de estado/dados sem Expo Router não têm fonte: Inferido.

## Testes em React Native

V-69: análise estática (ESLint, TypeScript); unitários com Jest (Arrange-Act-Assert, objetos reais antes de mocks, mocks para serviços externos e módulos nativos); integração; componentes com React Native Testing Library (visão do usuário: texto visível e helpers de acessibilidade, sem `testID` nem detalhes de implementação, snapshots pequenos; rodam em Node e não consideram código nativo); E2E com Detox, Appium ou Maestro **só para o vital** (autenticação, função central, pagamentos). `testID` só em E2E de app multilíngue (C2).

- **Detox** (V-70): aparelho real no iOS ainda não suportado; faixa de RN oficialmente suportada 0.77.x a 0.84.x no README na data da consulta, todas com a Nova Arquitetura; confira a versão do projeto. Instalação e pré-requisito de macOS não lidos.
- **Maestro no EAS Workflows** (V-37): job em alfa; perfil `e2e-test` com `withoutCredentials`, APK sem assinatura e build de simulador; fluxos YAML em `.maestro/` com `appId`; workflow em `.eas/workflows/e2e-tests.yml`; disparo manual, `pull_request` ou `pull_request_labeled`. Recurso em alfa pode mudar.
- Padrões de fluxos Maestro (V-44, classe C, só padrões): marcador `auth-loaded`, `runFlow` com `when:`, servidor mock, tags `ci`, `smoke`, `wip`. Não herde os comandos de instalação do skill.

## Flutter: arquitetura

Guia oficial (V-26): camadas **UI (View, ViewModel)** e **dados (Repository, Service)**; domínio opcional; repositório é a fonte de verdade; View sem lógica de negócio; repositórios não conhecem uns aos outros; services sem estado; relação View-ViewModel 1:1. Snippet S-20.

Skill de arquitetura em camadas (V-27, BSD-3-Clause, classe B): processo de 8 passos (modelos imutáveis; services; repository; use case opcional; ViewModel com `ChangeNotifier`; View com `ListenableBuilder`; registro em DI; testes). Use o processo, **reescreva os exemplos**: o cache ignora o ID e nunca invalida, há `try/finally` sem `catch`, tipos não definidos, e o passo 8 é um laço sem critério de parada (pode estimular enfraquecer testes).

Instruções do awesome-copilot (V-47, MIT, classe B, nota 5): camadas, fluxo unidirecional, modelos imutáveis (`freezed`/`built_value`, com aviso de build lento), testes de service, repositório e ViewModel, widget tests. Use como checklist de PR, não como norma. "go_router é a forma preferida para 90% dos apps" não tem fonte; `provider` é preferência pessoal. Prompt P-11.

## Flutter: layout responsivo e performance

Responsivo (V-28): `LayoutBuilder` mede o espaço do pai; `MediaQuery.sizeOf` mede a janela; breakpoint 600 é exemplo; não decida por orientação nem trave a orientação; limite a largura com `ConstrainedBox` e `Center`. O exemplo `AdaptiveLayout` da skill pode lançar erro de layout (`VerticalDivider` sem altura limitada) e a variante pequena perde a navegação: reescreva os exemplos.

Performance (V-29): trabalho fora de `build()`; `setState` na menor subárvore; `const`; `StatelessWidget` em vez de função; listas lazy; `Opacity` e `saveLayer` são caros; não sobrescreva `operator ==` em widgets; orçamento de 16 ms (8 de build e 8 de render); meça em profile mode com DevTools, no aparelho de menor capacidade. A regra "nunca em debug ou simulador" não consta na página de performance (vem da de build modes, a conferir).

## Flutter: testes

V-67: unitário (função, método, classe), widget (um widget) e integração (app inteiro ou grande parte); a confiança e o custo de manutenção sobem e a velocidade cai do unitário ao de integração; estratégia: muitos unitários e de widget, medidos por cobertura, mais integração suficiente para os casos importantes. O `integration_test` não interage com UI nativa (diálogos de permissão, notificações, platform views): a página sugere o pacote `patrol` (https://pub.dev/packages/patrol, citado, não aberto). Confira versão e compatibilidade.

## Kotlin Multiplatform

V-84: para construir apps iOS é preciso uma máquina macOS com Xcode; a IDE roda o Xcode por baixo para construir os frameworks; abra o Xcode ao menos uma vez e a cada atualização; KMP é totalmente suportado no IntelliJ IDEA e no Android Studio com o plugin Kotlin Multiplatform. Em Windows: alvos Android e lógica comum compilam; o alvo iOS exige macOS (a divisão exata do que compila em Windows é Inferido). Arquitetura e padrões KMP estão fora da cobertura (lacuna 14).

## Lacunas

- Acessibilidade específica de RN e Flutter (APIs de semântica) sem fonte lida: Inferido.
- Push e permissões em RN e Flutter passam por módulos nativos (Inferido); as regras das plataformas valem por baixo: [dados-push-permissoes-seguranca.md](dados-push-permissoes-seguranca.md).
- Concorrência em Flutter (isolates) sem fonte.
- Estado e dados em RN sem Expo Router sem fonte.
