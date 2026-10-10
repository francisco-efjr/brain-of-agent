---
name: readme-android-sem-interacao
description: Mede, em execução sem interação, se o README de um app Android local é entregue como rascunho completo com Decisões pendentes do humano em vez de perguntas, cobre as especificidades de Android a partir dos arquivos colados, não inventa JDK, licença nem tarefas e aponta o especialista mobile para build e assinatura.
tags: [technical-writing-docs, readme, escrever-readme, non-interactive, platform]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Entrega um README rascunho completo sem parar para perguntar, com seção Decisões pendentes do humano, requisitos e módulos vindos dos arquivos colados, comandos Gradle padrão marcados como não executados, JDK e licença como a confirmar, e aponta o plugin mobile para assinatura e publicação."
model: sonnet
---
Execução em lote: ninguém vai responder perguntas durante esta tarefa, então não pergunte nada. Escreva o README do meu app Android e entregue aqui na resposta.

É um app local de agenda de consultas (sem backend, os dados ficam no aparelho). Estes são os trechos do projeto:

`settings.gradle.kts`:
```kotlin
rootProject.name = "agenda"
include(":app", ":core:data", ":core:ui")
```

`app/build.gradle.kts` (trecho):
```kotlin
android {
    namespace = "br.com.exemplo.agenda"
    compileSdk = 35
    defaultConfig {
        applicationId = "br.com.exemplo.agenda"
        minSdk = 26
        targetSdk = 35
        versionCode = 7
        versionName = "1.3.0"
    }
    buildTypes {
        release { isMinifyEnabled = true }
    }
}
```

`AndroidManifest.xml` (trecho):
```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
<uses-permission android:name="android.permission.READ_CALENDAR" />
```

O público do README são outras pessoas do time que vão clonar e rodar no emulador. Não sei dizer qual JDK usamos nem se há arquivo de licença no repositório.
