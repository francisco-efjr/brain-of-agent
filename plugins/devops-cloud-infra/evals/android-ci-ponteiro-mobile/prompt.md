---
name: android-ci-ponteiro-mobile
description: Mede a cobertura de plataforma, verificando que a revisão de um workflow que assina e publica um app Android encontra os riscos de pipeline (upload em PR, permissions, pins, keystore) e aponta o plugin de mobile para assinatura e publicação em loja, sem afirmar detalhes de loja que não verificou.
tags: [devops-cloud-infra, gha-hardening-review, mobile, plataforma, positivo]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta que o step de upload para a Play Store roda também em pull_request e publica na faixa production sem aprovação (restringir ao push na principal, usar environment com revisores), a ausência de permissions, actions por tag, o keystore decodificado em disco e segredos de assinatura no job inteiro; reconhece o contexto mobile e aponta /mobile-apps:playbook para assinatura, faixas e publicação em loja; marca configuração de environment e branch protection como não verificável; não aprova nem inventa SHAs."
model: sonnet
---
Esse workflow do nosso app Android está ok? Ele builda o AAB, assina e já publica na Play Store quando mergeamos. Queremos que o time de produto publique sem depender de mim.

```yaml
name: android-release
on:
  push:
    branches: [main]
  pull_request:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v3
        with:
          distribution: temurin
          java-version: 17
      - name: Decode keystore
        run: echo "${{ secrets.KEYSTORE_B64 }}" | base64 -d > app/release.jks
      - name: Build AAB
        run: ./gradlew bundleRelease
        env:
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
      - uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_SERVICE_ACCOUNT_JSON }}
          packageName: com.example.loja
          releaseFiles: app/build/outputs/bundle/release/app-release.aab
          track: production
```
