# Deep links: App Links (Android) e Universal Links (iOS)

Verificado em 2026-10-10. Fontes oficiais abertas: https://developer.android.com/training/app-links/verify-android-applinks e https://developer.apple.com/documentation/xcode/supporting-associated-domains (V-40, classe B). Redação própria. Os formatos JSON abaixo são conhecimento estável (**Inferido**); confirme na documentação atual. Não confirmados em página oficial (V-40): o limite de 128 KB e a regra "sem redirecionamento" no Android; a impressão digital do Play App Signing no `assetlinks.json` é prática correta, mas a página aberta não a traz.

Princípio de segurança (brain `qa/mobile.md`): **abrir uma rota não concede autorização sobre o objeto.** Valide host, caminho e parâmetros de todo link recebido; confirme antes de ação sensível; trate recurso inexistente e recurso de outra conta.

## Android: checklist (V-40)

1. Intent-filter com `android:autoVerify="true"`, ações VIEW, categorias BROWSABLE e DEFAULT, esquema http(s) e host.
2. `assetlinks.json` em `https://<host>/.well-known/assetlinks.json`, **para cada host** declarado.
3. A verificação é **assíncrona** (esperar pelo menos 20 s após a instalação antes de concluir que falhou).
4. Android 15+ **reverifica periodicamente** (até sete dias).
5. A impressão digital (SHA-256) do certificado de assinatura no arquivo deve corresponder ao certificado do APK/AAB distribuído; com Play App Signing, é a do certificado de assinatura do Play (**Inferido**; conferir na documentação do Play).

```xml
<activity android:name=".LinkActivity" android:exported="true">
  <intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https" android:host="exemplo.com" android:pathPrefix="/produto" />
  </intent-filter>
</activity>
```

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": { "namespace": "android_app", "package_name": "com.exemplo.app",
              "sha256_cert_fingerprints": ["<SHA256_DO_CERTIFICADO_DE_ASSINATURA>"] }
}]
```

Depuração (somente emulador; altera estado do aparelho de teste):

```bash
adb shell pm get-app-links com.exemplo.app
adb shell pm verify-app-links --re-verify com.exemplo.app
```

## iOS: checklist (V-40)

1. Capability **Associated Domains** com entrada `applinks:exemplo.com`: **sem caminho e sem barra final**.
2. Arquivo `apple-app-site-association` em `https://<host>/.well-known/apple-app-site-association`, **sem extensão**, HTTPS válido, **sem redirecionamentos**.
3. **Cada subdomínio** precisa de entrada e de arquivo próprios.
4. O app trata o link recebido (`onOpenURL` no SwiftUI, `scene(_:continue:)`/`application(_:continue:...)` no UIKit).
5. Validação do arquivo no domínio e teste no aparelho são ação do usuário (requer conta Apple e aparelho).

```json
{ "applinks": { "details": [ { "appIDs": ["<TEAMID>.com.exemplo.app"],
                               "components": [ { "/": "/produto/*" } ] } ] } }
```

```swift
.onOpenURL { url in
    guard url.host == "exemplo.com", let route = Route(url: url) else { return }   // valida host e caminho
    router.open(route)    // autorização do objeto continua no servidor/na tela de destino
}
```

## RN, Expo e Flutter

- Expo: esquemas e domínios na configuração (`scheme`, `ios.associatedDomains`, `android.intentFilters`: **Inferido**, conferir); Expo Router roteia por arquivo (V-33).
- React Navigation: configuração `linking` com prefixos e mapa de rotas (V-81 só cobre a instalação; `linking` é **Inferido**).
- Flutter: o roteamento de links depende do pacote de rotas e da camada nativa (sem fonte lida): **Inferido**; os arquivos de domínio (`assetlinks.json`, AASA) valem igual.

## Testes de link (brain `qa/mobile.md`)

App fechado, em segundo plano e aberto; sessão ausente (levar ao login e voltar ao destino); parâmetro inválido; recurso inexistente; recurso de outra conta (negar sem vazar existência); link repetido (idempotência da ação).

## Achados típicos

| Achado | Evidência | Correção |
| --- | --- | --- |
| `autoVerify` ausente | intent-filter sem o atributo | Adicionar e publicar `assetlinks.json` |
| `assetlinks.json` só no domínio raiz e links usam `www` | hosts declarados vs arquivo | Publicar por host |
| Entitlement `applinks:exemplo.com/produto` | caminho no domínio | Usar apenas o domínio |
| AASA atrás de redirecionamento 301 | resposta do domínio (peça ao usuário a saída de `curl -I`) | Servir direto em HTTPS |
| Ação sensível disparada direto pelo link | handler de `onOpenURL` | Confirmar e revalidar no servidor |
