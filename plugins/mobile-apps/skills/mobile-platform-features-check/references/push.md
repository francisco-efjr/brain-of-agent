# Push: checklist por plataforma

Verificado em 2026-10-10. Fontes oficiais: registro no APNs (V-52, https://developer.apple.com/documentation/usernotifications/registering-your-app-with-apns.md), autorização com `UNUserNotificationCenter` (V-53), `POST_NOTIFICATIONS` e canais (V-54, https://developer.android.com/develop/ui/views/notifications/notification-permission), FCM no Android (V-55, https://firebase.google.com/docs/cloud-messaging/android/get-started). Redação própria. Não lidos: payload de envio, notificações silenciosas, FCM no iOS (lacuna 5).

Permissão e token são coisas separadas: a **autorização** do usuário decide se a notificação é exibida; o **token** identifica o aparelho/app no provedor.

## iOS (APNs), 6 itens (V-52)

1. Capability **Push Notifications** adicionada (cria o entitlement `aps-environment`). Procure em `*.entitlements`.
2. Serviço de push habilitado no **App ID** na conta Apple (ação do usuário; o agente não faz).
3. **Registrar a cada launch** e receber o token (`registerForRemoteNotifications()`; o token é único por aparelho e por app).
4. Tratar sucesso **e falha** (rede, APNs inalcançável, entitlement ausente): marcar o estado e tentar de novo.
5. Enviar o token ao servidor por conexão cifrada, **sem cache local e sem log em texto**: o token muda após restauração de backup, aparelho novo ou reinstalação.
6. Um usuário pode ter **vários aparelhos**; o servidor guarda vários tokens por usuário.

Detecção: Grep `registerForRemoteNotifications|didRegisterForRemoteNotificationsWithDeviceToken|didFailToRegisterForRemoteNotificationsWithError|aps-environment`. Token impresso em log ou em `UserDefaults`: achado.

### Autorização (V-53)

Fluxo: gatilho de uso real → pedido com **opções mínimas realmente usadas** (`.alert`, `.sound`, `.badge`, opcional `.provisional`) → checar `notificationSettings()` antes de agendar → caminho alternativo se não autorizado, sem insistir.

```swift
let center = UNUserNotificationCenter.current()
let granted = try await center.requestAuthorization(options: [.alert, .sound])   // depois da 1ª ação que justifique
// antes de agendar notificação local:
let settings = await center.notificationSettings()
guard settings.authorizationStatus == .authorized || settings.authorizationStatus == .provisional else { return }
```

- O primeiro pedido mostra o diálogo; pedidos seguintes não (V-53).
- A página diz que pedir em contexto que explique o benefício (por exemplo, depois do primeiro item criado) funciona melhor que pedir no primeiro launch.
- `.provisional` entrega em silêncio, só na central de notificações, com botões Manter e Desativar; permite pedir no primeiro launch porque não exibe diálogo.
- A página **não** trata de negação, `.denied`, `.notDetermined` nem Ajustes. Levar o usuário às Ajustes com texto explicativo é prática comum, **Inferido**.
- A assinatura do código acima (`requestAuthorization` assíncrono e `authorizationStatus`) é conhecimento estável: confirme no SDK do projeto.

## Android (FCM), 6 itens (V-55) + permissão (V-54)

1. **Serviço** que estende `FirebaseMessagingService`, com filtro `com.google.firebase.MESSAGING_EVENT` e `android:exported="false"`. Necessário para notificações em primeiro plano e payloads de dados.
2. **`POST_NOTIFICATIONS`** declarada e **pedida em tempo de execução** no API 33+. O SDK 23.0.6+ do FCM declara a permissão, mas o pedido continua com o app.
3. **Canal padrão** via meta-data `com.google.firebase.messaging.default_notification_channel_id` (Android 8+), **criado cedo**. Para apps que targetam 12L ou inferior, criar o canal em segundo plano pode adiar o diálogo e notificações recebidas antes de aceitar "serão perdidas".
4. **Token/Firebase Installation ID**: a seção do token de registro está marcada como depreciada, com recomendação de Installation IDs; reenviar ao servidor **no callback** quando o provedor atualizar.
5. **Payload** com dados suficientes (não depender de rede ao receber em Doze, V-63).
6. **Nunca remover** a permissão com `tools:node="remove"` se o app usa notificações: bloqueia todas, não só as do FCM.

```xml
<service android:name=".MyFirebaseService" android:exported="false">
    <intent-filter><action android:name="com.google.firebase.MESSAGING_EVENT" /></intent-filter>
</service>
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
<meta-data android:name="com.google.firebase.messaging.default_notification_channel_id"
           android:value="@string/default_channel_id" />
```

### Permissão `POST_NOTIFICATIONS` (V-54)

- API 33+: notificações começam **desligadas** em instalação nova; o app espera a concessão.
- Declarar no manifesto; checar `Build.VERSION.SDK_INT >= 33`; pedir **em contexto** com o contrato `ActivityResultContracts.RequestPermission`.
- Tela intermediária de justificativa só quando `shouldShowRequestPermissionRationale()` for verdadeiro.
- Checar `NotificationManagerCompat.from(context).areNotificationsEnabled()` antes de enviar.
- Isenções: sessões de mídia; `Notification.CallStyle` quando o app declara `MANAGE_OWN_CALLS`, implementa `ConnectionService` e chama `registerPhoneAccount()`. Notificações negadas de serviço em primeiro plano ainda aparecem no Gerenciador de Tarefas.
- Comportamento após **negações repetidas**: a página não o descreve (só trata "não permitir" para apps que targetam 12L ou inferior). Não afirme.

```kotlin
val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
    if (!granted) { /* degradar: manter o app útil, sem pressionar nem bloquear a UI */ }
}
if (Build.VERSION.SDK_INT >= 33) launcher.launch(Manifest.permission.POST_NOTIFICATIONS)
```

(Esboço Compose; exemplo de código de `shouldShowRequestPermissionRationale` e `areNotificationsEnabled` não consta na página: **Inferido**.)

## Cross-platform (RN, Flutter)

Push chega por módulos nativos (Firebase Messaging, Expo Notifications, `flutter_local_notifications`): as regras de cima se aplicam ao projeto nativo gerado. **Inferido**: sem fonte lida. Em Expo gerenciado, entitlements e manifesto vêm da configuração (`app.json`, plugins) e podem não estar no repositório; leia a configuração e diga o que não pôde ver. Conferir a versão do SDK do módulo.

## O que o servidor precisa (fronteira `backend-api`)

Chave `.p8`/certificado APNs e credenciais FCM ficam no servidor; o cliente só guarda o token e o envia. Várias contas por aparelho e troca A→B: o servidor precisa dissociar o token do usuário anterior no logout (**Inferido**; veja o teste de troca de conta em `mobile-test-strategy`).

## Teste manual (pendência do usuário)

Receber ≠ tocar (brain `qa/mobile.md`): teste conteúdo na tela bloqueada, destino do toque, ação duplicada, item removido e usuário que saiu da conta. Entrega depende de SO e provedor; separe o teste do handler da entrega real.
