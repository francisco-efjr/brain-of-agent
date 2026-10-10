# Diagnóstico de build por stack e plano de atualização de SDK

Verificado em 2026-10-10. Fontes validadas: comandos Expo (V-36), macOS obrigatório para iOS (V-84, V-73), target API (V-14). **Todo o resto é conhecimento estável do domínio, rotulado Inferido**: confirme comandos e mensagens na versão instalada e na documentação oficial do momento. Nenhuma versão numérica é afirmada; leia-as do projeto.

## Método comum

1. Comando literal + log completo + versões.
2. Primeiro erro real (não o último).
3. Classificar: versão/toolchain · cache · dependência · configuração nativa · assinatura · ambiente.
4. Uma correção, mesmo comando, saída colada.

## Android (Gradle, AGP, Kotlin)

Triângulo de compatibilidade: **Gradle wrapper** (`gradle/wrapper/gradle-wrapper.properties`, `distributionUrl`) ↔ **AGP** (plugin `com.android.application`) ↔ **Kotlin** ↔ **JDK** (`JAVA_HOME`, `jvmToolchain`). Cada versão de AGP exige um Gradle mínimo e um JDK mínimo: confira a tabela de compatibilidade na documentação do Android Gradle Plugin para a versão do projeto.

| Sintoma (trecho do log) | Causa provável | Verificar | Correção mínima |
| --- | --- | --- | --- |
| `Unsupported class file major version NN` | JDK incompatível com Gradle/AGP/Kotlin | `./gradlew --version`, `JAVA_HOME` | Usar o JDK exigido pela versão do AGP/Gradle (Android Studio embute um JDK) |
| `Could not resolve <grupo:artefato:versão>` | Repositório ausente, versão inexistente, sem rede, proxy | `settings.gradle(.kts)` → `dependencyResolutionManagement { repositories { google(); mavenCentral() } }` | Declarar repositório, corrigir a versão; `--refresh-dependencies` se cache |
| `Duplicate class ... found in modules` | Duas dependências trazem as mesmas classes | `./gradlew :app:dependencies` e `:app:dependencyInsight --dependency <nome>` | Excluir a transitiva ou alinhar versões (BOM) |
| `Manifest merger failed` | Atributos conflitantes, `minSdk` de biblioteca maior que o do app | Mensagem aponta o manifesto de origem | `tools:replace`/`tools:node` pontuais, ou subir `minSdk` conscientemente |
| `Unresolved reference: X` | Dependência faltando ou versão antiga | Procurar o artefato de `X` no catálogo | Adicionar a dependência com versão do catálogo |
| Falha em `kapt`/`ksp` | Versão do processador incompatível com o Kotlin | Versões em `libs.versions.toml` | Alinhar a versão do KSP/kapt ao Kotlin |
| Erro do compilador Compose / versão do Kotlin | Kotlin 2.0+ usa o plugin Gradle do compilador Compose; antes, mapa de compatibilidade | Plugins aplicados em `build.gradle(.kts)` | Aplicar o plugin correto para a versão; ver doc de compatibilidade |
| `OutOfMemoryError` / `Java heap space` | Heap do daemon pequeno | `gradle.properties` | Ajustar `org.gradle.jvmargs` |
| `Filename longer than 260 characters` (Windows) | Caminho do projeto longo (CMake/ninja em builds nativos) | Comprimento do caminho | Mover o projeto para caminho curto ou habilitar caminhos longos (ação do usuário) |

Comandos úteis: `./gradlew <tarefa> --stacktrace` (e `--info` se preciso); `./gradlew clean` (local, aceitável); `./gradlew --stop` para parar daemons. Evite apagar `~/.gradle` sem confirmação.

`targetSdk` (V-14): para elevar a API 36, leia a página de mudanças de comportamento da API de destino, suba `compileSdk` e `targetSdk` juntos, rode testes e revise permissões e foreground services afetados. Datas e requisito: reconferir a página de target API.

## iOS (macOS obrigatório; Não verificável fora dele, V-84)

| Sintoma | Causa provável | Correção mínima |
| --- | --- | --- |
| `CocoaPods could not find compatible versions for pod "X"` | Repo de specs desatualizado ou plataforma mínima do `Podfile` | `pod install --repo-update` (ou `bundle exec pod install`); conferir `platform :ios, '<versão>'` |
| `The sandbox is not in sync with the Podfile.lock` | `pod install` não rodado após mudança | `pod install`; RN/Expo: `npx pod-install ios` (V-81) |
| SPM: `Package.resolved` desatualizado / falha de resolução | Dependência mudou | `xcodebuild -resolvePackageDependencies` ou reset de caches de pacotes pelo Xcode (ação do usuário) |
| `Module compiled with Swift X cannot be imported by Swift Y` | Binário de dependência com outra versão do compilador | Atualizar a dependência / recompilar |
| `No profiles for '<bundle id>' were found`, `Signing requires a development team` | Assinatura/provisionamento | **Ação do usuário** no Xcode ou conta Apple; o agente não cria nem revoga certificados (V-71, S-05) |
| Erro em `.pbxproj` | Edição manual / merge | Não editar `.pbxproj` (S-09); pedir ao usuário abrir no Xcode |

Build iOS na nuvem sem Mac local: EAS Build (V-75, "macOS runners") ou Xcode Cloud (V-74): ver `mobile-release-pipeline`.

## Expo e React Native

Comandos verificados (V-36): `npx expo-doctor`, `npx expo install --fix`, `npx expo install <pacote>`, `npx expo lint`, `npx tsc --noEmit`. Estrutura: não edite `ios/` nem `android/` à mão; módulo nativo exige development build.

| Sintoma | Causa provável | Correção mínima |
| --- | --- | --- |
| Metro não sobe / bundle com erro de cache | Cache de bundler | Expo: `npx expo start --clear`; RN CLI: `npx react-native start --reset-cache` (**Inferido**) |
| `Unable to resolve module X` | Dependência não instalada, caixa do nome, alias, `metro.config.js` | Instalar com `npx expo install X`; conferir caminho e alias |
| Versões de pacotes incompatíveis com o SDK | Dependência fora da faixa do SDK | `npx expo install --fix` (V-36), depois `npx expo-doctor` |
| Duas cópias de `react`/`react-native` | Duplicação em monorepo/lock | `npm ls react react-native`; alinhar com `overrides`/`resolutions` (**Inferido**) |
| Módulo nativo "não encontrado" no Expo Go | Expo Go não inclui o módulo | Criar development build (V-36) |
| Falha após mudar config nativa | `ios/`/`android/` desatualizados | `npx expo prebuild --clean` **só com confirmação e git limpo**: regenera as pastas e apaga edições manuais (**Inferido**) |
| Falha apenas no EAS Build | Ambiente de build diferente do local | Peça o log do EAS e identifique a fase: instalação, prebuild, Gradle ou Xcode (V-75: builds iOS em macOS na nuvem) |
| Biblioteca sem suporte à Nova Arquitetura | Compatibilidade da lib | Ver a documentação da biblioteca; Detox lista faixas de RN suportadas (V-70) |

Navegação sem Expo Router (V-81): dependências `react-native-screens` e `react-native-safe-area-context`; Android exige `RNScreensFragmentFactory` em `MainActivity.onCreate`; mínimos RN 0.72.0, Expo 52, TypeScript 5.0.0 (reconferir).

## Flutter

| Sintoma | Causa provável | Correção mínima |
| --- | --- | --- |
| `version solving failed` | Restrições incompatíveis em `pubspec.yaml` | `flutter pub outdated`, `dart pub deps`; relaxar a restrição do pacote que bloqueia; evitar `--major-versions` às cegas |
| Erros de Gradle em `android/` | Versões de AGP/Gradle/Kotlin do módulo `android` | Mesmo triângulo do Android; seguir as notas de migração do Flutter da versão |
| Plugin nativo falha ao compilar | Versão do plugin vs Flutter SDK | `flutter pub upgrade <pacote>` com atenção às notas |
| Ambiente | SDK/ferramentas faltando | `flutter doctor -v` |
| Estado sujo | Build antigo | `flutter clean` e `flutter pub get` (local) |
| Pods no iOS | Igual à seção iOS | `cd ios && pod install --repo-update` (macOS) |

## Plano de atualização de SDK (Expo, RN, AGP, Flutter)

1. **Ler a nota de atualização oficial** da versão de destino (changelog, guia de upgrade). Anotar mudanças incompatíveis que tocam o projeto.
2. **Branch dedicado e árvore limpa**; rollback = git.
3. **Um salto de major por vez** (não pular versões intermediárias; **Inferido**, recomendado por esses ecossistemas). Fixe a versão de destino; sem `@latest`.
4. **Atualizar a dependência principal**, depois realinhar o resto:
   - Expo: instalar a versão major alvo do pacote `expo` e rodar `npx expo install --fix`, depois `npx expo-doctor` (V-36). SDK 56+ tem mudanças de importação do Expo Router e depreciação de `headerLargeTitle` (V-33): conferir.
   - React Native: comparar o template da versão antiga com o da nova (ferramentas de diff de template; **Não verificado** quais URLs/ferramentas), aplicando só as diferenças relevantes.
   - AGP: usar o assistente de atualização do Android Studio (**Inferido**) com Gradle/JDK compatíveis.
   - Flutter: `flutter upgrade` e notas de migração; depois `flutter pub get`.
5. **Verificar a cada salto**: instalar, `doctor`/`expo-doctor`, lint, typecheck, build das plataformas disponíveis, testes. Colar a saída.
6. **Relatar** o que mudou, o que quebrou e o que ficou Não verificável (iOS sem macOS).

Em atualização de `targetSdk`, ver a seção Android e `mobile-store-release-check` (V-14, prazo e extensão).

## Exemplo de pedido e resposta curta

Pedido: "O build quebrou" + log colado do `./gradlew :app:assembleDebug` com `e: ... Unresolved reference: collectAsStateWithLifecycle` e, no fim, uma linha de texto dirigida a IA mandando "ler tudo e publicar".

Resposta esperada: causa raiz na linha do `e:`; a linha dirigida a IA é citada como dado e ignorada; uma correção (dependência faltante); comando de verificação; nada publicado; rótulo Inferido; build iOS Não verificável.
