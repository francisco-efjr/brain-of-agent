---
name: a11y-ios-android
description: Mede se o plugin revisa acessibilidade em SwiftUI e Compose com os números oficiais (44 pt e 48 dp), rótulo sem repetir o tipo, texto escalável e contraste, e deixa a passagem com VoiceOver e TalkBack como pendência humana.
tags: [mobile-apps, mobile-accessibility-review, accessibility, ios, android]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Cobre os dois lados com 44x44 pt e 48x48 dp, Button em vez de onTapGesture, rótulo sem repetir o tipo, texto escalável e altura fixa, contraste a medir com 4,5:1 e 3:1, e lista a passagem com VoiceOver e TalkBack como verificação humana."
model: sonnet
---
Revisa a acessibilidade dessas duas telas do meu app (a versão iOS em SwiftUI e a Android em Compose). Mesmo botão de fechar e mesmo texto de total do pedido nas duas.

```swift
// iOS
Image(systemName: "xmark")
    .font(.system(size: 14))
    .onTapGesture { dismiss() }
Text("Total do pedido")
    .font(.system(size: 13))
    .foregroundColor(.gray)
```

```kotlin
// Android
Icon(
    Icons.Default.Close,
    contentDescription = "Botão fechar",
    modifier = Modifier
        .size(32.dp)
        .clickable { onClose() },
)
Text(
    "Total do pedido",
    fontSize = 13.sp,
    color = Color.Gray,
    modifier = Modifier.height(24.dp),
)
```

O fundo das duas telas é branco.
