# Checklist iOS de pré-submissão (12 itens)

Verificado em 2026-10-10. Fontes oficiais: App Review Guidelines (V-16, https://developer.apple.com/app-store/review/guidelines/), privacy manifest (V-17), purpose strings (V-58), distribuição pelo Xcode (V-73). Texto de documentação Apple: redação própria. A lista de 12 foi reconstruída só a partir de itens Verificados; os padrões de Grep são conhecimento estável do domínio (**Inferido**).

Para cada item, preencha: aplicável (sim, não, a conferir), evidência `arquivo:linha` ou "não encontrado em <lista>", status (conforme, lacuna, Não verificável).

| # | Item | Regra e fonte | Quando se aplica | Como detectar (Grep/Glob) | Correção mínima |
| --- | --- | --- | --- | --- | --- |
| 1 | Exclusão de conta dentro do app | 5.1.1(v), V-16 | O app permite criar conta | `-i "delete.?account\|excluir.?conta\|apagar.?conta\|deleteUser"` e chamadas `DELETE` a `/account` ou `/users` | Fluxo "Excluir conta" acessível no app que apague a conta e os dados associados (ou inicie essa exclusão), com confirmação |
| 2 | Login equivalente | 4.8, V-16 | O app usa login de terceiro (Google, Facebook) | `GIDSignIn\|GoogleSignIn\|FBSDKLoginKit\|LoginManager\|ASAuthorizationAppleIDProvider\|expo-apple-authentication\|google-signin` | Conferir no texto atual da 4.8 se o login próprio ou outro já atende; se não, oferecer opção equivalente. Não afirmar violação sem conferir (**Inferido** para os critérios finos) |
| 3 | Compra in-app e restauração | 3.1.1, V-16 | O app desbloqueia conteúdo ou função digital | `StoreKit\|Product\.products\|SKPaymentQueue\|AppStore\.sync\|restorePurchases\|react-native-iap\|purchases-` e links de pagamento externo | Usar IAP para o que a regra cobre e oferecer "Restaurar compras". Detalhes de monetização fora do escopo do plugin (fronteira `fintech-payments`) |
| 4 | Conta de demonstração e backend ativo | 2.1, V-16 | O app exige login | Procure notas de revisão em `README`, `docs/`, `fastlane/metadata`; geralmente **não há evidência no código** | Credenciais de demonstração nas notas de revisão e backend de produção no ar, ou modo demo aprovado antes. Ação do usuário |
| 5 | Mais que um site empacotado | 4.2, V-16 | O app é basicamente uma WebView | `WKWebView\|SFSafariViewController\|react-native-webview\|webview_flutter`; conte telas nativas vs telas só com WebView | Agregar funcionalidade nativa real ou reavaliar a publicação |
| 6 | Conteúdo de usuário | 1.2, V-16 | O app exibe conteúdo criado por usuários | `-i "report\|denunciar\|block\|bloquear\|moderat\|flag"` | Filtro, denúncia, bloqueio de usuário e contato publicado |
| 7 | Rastreamento (ATT) | 5.1.2, V-16 | O app rastreia entre apps/sites de terceiros (IDFA, SDK de atribuição) | `ATTrackingManager\|NSUserTrackingUsageDescription\|ASIdentifierManager\|AdSupport\|AppsFlyer\|Adjust\|FBSDKCoreKit` | Solicitar autorização ATT antes de rastrear, com `NSUserTrackingUsageDescription`; sem rastreamento, não incluir o pedido |
| 8 | Sem funções ocultas | 2.3.1, V-16 | Sempre | `remoteConfig\|RemoteConfig\|featureFlag\|LaunchDarkly\|unleash`; conteúdo ou funções ativadas por servidor depois da revisão | Documentar flags nas notas de revisão; não esconder funções que mudem a natureza do app |
| 9 | Privacy manifest do app e dos SDKs | V-17 | Coleta de dados e uso de required reason APIs; SDKs na lista da Apple | Glob `**/PrivacyInfo.xcprivacy`, `Pods/**/PrivacyInfo.xcprivacy`, `SourcePackages/**/PrivacyInfo.xcprivacy`; Grep nas categorias de required reason API: `UserDefaults\|NSUserDefaults`, `creationDate\|modificationDate\|NSFileCreationDate`, `systemUptime\|mach_absolute_time`, `volumeAvailableCapacity\|statfs`, `activeInputModes` (lista de categorias: **Inferido**, conferir a lista atual da Apple) | Criar `PrivacyInfo.xcprivacy` com `NSPrivacyAccessedAPITypes` e motivo por API (V-17); revisar tipos coletados e domínios de rastreamento; atualizar SDKs que ainda não trazem manifesto |
| 10 | Purpose string específica e localizada por recurso | V-58 | Qualquer API protegida usada pelo código ou por SDKs | Glob `**/Info.plist`, `**/InfoPlist.xcstrings`, `**/InfoPlist.strings`; compare com o inventário do passo 2 | Uma chave `NS*UsageDescription` por recurso, frase completa e específica, não vazia, menos de 4.000 bytes, localizada. Sem a chave: acesso falha e há rejeição ITMS-90683 |
| 11 | Metadados que não mudam após o envio | V-73 | Sempre | Sem evidência no código | Revisar nome, subtítulo, categoria, classificação etária e política de privacidade antes de enviar. Ação do usuário |
| 12 | Build validado e presente no TestFlight | V-73 | Sempre | Sem evidência no código | Archive, "Validate App", upload ao App Store Connect e build no TestFlight. **Requer macOS e Xcode**: fora dele, **Não verificável**. "Submit for Review" é sempre ação do usuário |

## Tabela API protegida para chave de purpose string

Verificado (V-58) para câmera e localização; as demais são conhecimento estável (**Inferido**, lacuna 6): confirme o nome da chave na documentação Apple antes de afirmar ao usuário.

| Recurso | Chave | Status |
| --- | --- | --- |
| Câmera | `NSCameraUsageDescription` | Verificado |
| Localização em uso | `NSLocationWhenInUseUsageDescription` | Verificado |
| Localização em segundo plano | `NSLocationAlwaysAndWhenInUseUsageDescription` | Verificado |
| Microfone | `NSMicrophoneUsageDescription` | Inferido |
| Fotos | `NSPhotoLibraryUsageDescription` (e `...AddUsageDescription` para só salvar) | Inferido |
| Bluetooth | `NSBluetoothAlwaysUsageDescription` | Inferido |
| Face ID | `NSFaceIDUsageDescription` | Inferido |
| Contatos | `NSContactsUsageDescription` | Inferido |
| Rastreamento (ATT) | `NSUserTrackingUsageDescription` | Inferido |

## Onde as chaves vivem em Expo e Flutter

- Expo: `app.json`/`app.config.*` em `expo.ios.infoPlist` e nas configurações dos plugins de cada módulo (por exemplo, texto de câmera no plugin do módulo). Manifesto de privacidade em `expo.ios.privacyManifests` (**Inferido**; conferir na documentação do SDK instalado). `ios/` pode não existir no repositório (prebuild gerenciado): "não encontrado em ios/" não prova ausência.
- Flutter: `ios/Runner/Info.plist` e `ios/Runner/PrivacyInfo.xcprivacy`.
- React Native nativo: `ios/<App>/Info.plist`.

## Exemplo de frase de purpose string (referência de qualidade, não para copiar)

Ruim: "Precisamos da câmera." (genérica). Melhor: "O app usa a câmera para você fotografar o recibo e anexá-lo à despesa." (específica, completa, explica o motivo). Mantenha a língua do app e traduza em `InfoPlist.xcstrings`.

## Sequência de release iOS (V-73), com marcação

1. Apple Developer Program ativo e registro do app no App Store Connect. Ação do usuário.
2. `Product > Archive` no Xcode. Requer macOS.
3. "Validate App". Requer macOS.
4. "Distribute App" para TestFlight & App Store. Requer macOS; envia ao App Store Connect, tratado em `mobile-release-pipeline`.
5. Testes internos/externos no TestFlight. Ação do usuário.
6. Revisar metadados que não podem ser alterados após o envio. Ação do usuário.
7. Enviar a build do TestFlight para o App Review. Sempre ação do usuário; o plugin nunca aciona.
