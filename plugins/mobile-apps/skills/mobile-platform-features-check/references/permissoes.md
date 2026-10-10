# Permissões em tempo de execução e purpose strings

Verificado em 2026-10-10. Fontes oficiais: Android (V-56, https://developer.android.com/training/permissions/requesting), localização em segundo plano no Play (V-57, https://support.google.com/googleplay/android-developer/answer/9799150), purpose strings e privacidade no iOS (V-58, https://developer.apple.com/documentation/uikit/requesting-access-to-protected-resources.md e páginas irmãs). Redação própria. Brain `qa/references/mobile.md` (próprio, MIT) fornece os casos de teste.

Princípio: pedir **no momento em que o dado é necessário**, com justificativa específica, e **degradar com elegância** na negação, sem pressionar. O diálogo do sistema não pode ser personalizado (V-56) e não reaparece à vontade.

## Inventário (passo 1)

Grep por plataforma:

- iOS: `AVCaptureDevice|AVAudioSession|CLLocationManager|PHPhotoLibrary|PHPickerViewController|CBCentralManager|CNContactStore|ATTrackingManager|LAContext|UNUserNotificationCenter|HKHealthStore`.
- Android: `<uses-permission` em manifestos (incluindo mesclados de dependências), `checkSelfPermission|requestPermissions|RequestPermission`, `ACCESS_FINE_LOCATION|ACCESS_COARSE_LOCATION|ACCESS_BACKGROUND_LOCATION|CAMERA|RECORD_AUDIO|READ_MEDIA_|POST_NOTIFICATIONS|BLUETOOTH_`.
- Expo/RN: `expo-camera`, `expo-location`, `expo-notifications`, `react-native-permissions` e a configuração em `app.json` (`ios.infoPlist`, `android.permissions`, plugins).
- Flutter: `permission_handler`, `camera`, `geolocator` e os manifestos de `ios/` e `android/`.

SDKs de terceiros contam: a Apple rejeita por purpose string ausente mesmo quando a API vem de SDK, e o desenvolvedor responde por ele (V-58).

## iOS: checklist (V-58)

1. **Uma chave `NS*UsageDescription` por recurso usado** (tabela em `${CLAUDE_PLUGIN_ROOT}/skills/mobile-store-release-check/references/checklist-ios.md`). Verificado: câmera, localização em uso (`NSLocationWhenInUseUsageDescription`) e em segundo plano (`NSLocationAlwaysAndWhenInUseUsageDescription`). Outras chaves: **Inferido**, confirmar o nome na documentação.
2. A string **não é vazia**, tem menos de **4.000 bytes**, descreve de forma exata, significativa e **específica** o motivo (tipicamente uma frase completa).
3. Sem a string, o acesso falha e o app pode ser derrubado; o App Review rejeita com **ITMS-90683**.
4. **Localizar** com `InfoPlist.xcstrings`.
5. **Checar o status antes de cada uso**: o usuário pode mudar nos Ajustes; tratar falha de acesso quando não houver API dedicada.
6. **Pedir no momento da necessidade**, com fallback; não pedir tudo no primeiro launch.
7. Reset de permissões no aparelho de teste: "Reset Location & Privacy" (afeta todos os serviços; use em aparelho de teste).

Boas e más strings: "Precisamos da câmera." (genérica, risco de rejeição) vs "Usamos a câmera para você fotografar o recibo e anexá-lo à despesa." (específica e completa).

Padrão de status seguro (esboço Swift, câmera; confirmar API no SDK):

```swift
switch AVCaptureDevice.authorizationStatus(for: .video) {
case .authorized: startCapture()
case .notDetermined: if await AVCaptureDevice.requestAccess(for: .video) { startCapture() } else { showFallback() }
case .denied, .restricted: showFallback()   // sem insistir; oferecer caminho alternativo
@unknown default: showFallback()
}
```

Levar o usuário às Ajustes depois de negar: prática comum, **Inferido** (V-53). Oferecer como alternativa discreta, não como loop de insistência.

## Android: checklist (V-56)

Fluxo oficial: `checkSelfPermission` a cada uso → `shouldShowRequestPermissionRationale()` para UI educativa → pedir pelo contrato `RequestPermission` (recomendado) → tratar o resultado.

1. O diálogo do sistema **não pode ser personalizado**; explique antes, no contexto.
2. Na negação: **minimizar a perda de função**, ser específico, **não bloquear** a interface, **não pressionar**. O exemplo oficial comenta que não se deve apontar para as configurações para convencer o usuário.
3. Negação "mais de uma vez" encerra o diálogo (na seção de depuração: "duas vezes" marca `USER_FIXED`). A página não diz o que `shouldShowRequestPermissionRationale()` devolve após negação permanente.
4. Depuração (somente emulador): `adb shell dumpsys package <pacote>` e `pm clear-permission-flags` documentados; alteram o estado do aparelho de teste.
5. Permissões de execução desde o Android 6; `POST_NOTIFICATIONS` desde o API 33 (ver `push.md`).

```kotlin
val launcher = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
    if (granted) openCamera() else showAlternative()   // sem bloquear a UI
}
Button(onClick = { launcher.launch(Manifest.permission.CAMERA) }) { Text("Tirar foto") }
```

## Android: localização em segundo plano (Play, V-57)

6 itens: central à funcionalidade; tentar primeiro em primeiro plano; formulário de declaração (apps que targetam Android 10+ com `ACCESS_BACKGROUND_LOCATION`); vídeo de 30 s ou menos (recomendação); divulgação em destaque no app com "location", uso em segundo plano e lista das funcionalidades; nova declaração ao mudar a funcionalidade. Sem botão de aceitar obrigatório. Reconferir a página (sem data de atualização).

## Teste das permissões (brain `qa/mobile.md`)

Para cada permissão realmente usada: primeira solicitação, recusa, aceite, mudança nas configurações e retorno ao app (e concessão temporária/parcial se existir na combinação SO/API). O resultado esperado distingue a função bloqueada das que continuam:

- Câmera/documentos: recusa não fecha o app; cancelamento volta ao fluxo; captura inválida (arquivo vazio) não passa como anexo.
- Biometria: sucesso, cancelamento, indisponibilidade e fallback. Simular sucesso testa a reação do app, não a segurança do sensor.
- Sessão e permissões: troca de conta A→B não herda estados.

Plano completo: skill `mobile-test-strategy`.
