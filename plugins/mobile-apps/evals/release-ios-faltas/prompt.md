---
name: release-ios-faltas
description: Mede se o plugin audita, em modo somente leitura, a prontidão de um app SwiftUI para a App Store, apontando purpose string ausente, exclusão de conta, login de terceiros, privacy manifest e conta de demonstração, sem garantir aprovação nem afirmar execução.
tags: [mobile-apps, mobile-store-release-check, app-store, privacy]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Relatório por prioridade com NSCameraUsageDescription ausente (risco de rejeição ITMS-90683), exclusão de conta no app, avaliação do login de terceiros, privacy manifest do app e do SDK Firebase e conta de demonstração, com rótulos, data, ações do usuário e sem afirmar build."
model: sonnet
---
Vou subir amanhã meu app SwiftUI na App Store e queria saber o que falta. O app tem login com e-mail e senha e também "Entrar com Google". O usuário cria a conta dentro do app, tira uma foto de perfil pela câmera e eu uso Firebase Analytics. Meu Info.plist tem só isto de relevante:

```xml
<key>CFBundleDisplayName</key>
<string>Rotina</string>
<key>UIRequiredDeviceCapabilities</key>
<array><string>arm64</string></array>
```

Não tenho PrivacyInfo.xcprivacy no projeto. Na tela de perfil só existe o botão "Sair". O código da foto é este:

```swift
struct FotoPerfilPicker: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.sourceType = .camera
        return picker
    }
    func updateUIViewController(_ vc: UIImagePickerController, context: Context) {}
}
```

Estou no Windows, então não consigo abrir o Xcode agora. O que falta antes de enviar?
