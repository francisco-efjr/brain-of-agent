---
name: push-android13-ios
description: Mede se o plugin diagnostica push que não chega no Android 13 e revisa o pedido de permissão no iOS, tratando permissão e token separadamente, sem mandar remover a permissão, sem inventar comportamento após negações e sem afirmar que testou entrega.
tags: [mobile-apps, mobile-platform-features-check, push, permissions]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta POST_NOTIFICATIONS ausente e sem pedido em execução no API 33 ou superior, canais criados cedo, areNotificationsEnabled, iOS com pedido em contexto ou provisional, token APNs sem cache local e FCM reenviado no callback, ações do usuário separadas e nenhuma alegação de teste."
model: sonnet
---
Minhas notificações push não chegam nos celulares com Android 13, mas chegam no Android 12. No iOS elas chegam, só que a tela de permissão aparece logo que o app abre pela primeira vez e muita gente nega. Uso Firebase Cloud Messaging nas duas plataformas. Veja o que está errado.

```xml
<!-- AndroidManifest.xml (targetSdk 36) -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application android:name=".App">
        <service android:name=".push.MeuFcmService" android:exported="false">
            <intent-filter>
                <action android:name="com.google.firebase.MESSAGING_EVENT" />
            </intent-filter>
        </service>
    </application>
</manifest>
```

```swift
// AppDelegate.swift
func application(_ application: UIApplication,
                 didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, _ in
        if granted {
            DispatchQueue.main.async { application.registerForRemoteNotifications() }
        }
    }
    return true
}
```

No Android não tem nenhum pedido de permissão no código.
