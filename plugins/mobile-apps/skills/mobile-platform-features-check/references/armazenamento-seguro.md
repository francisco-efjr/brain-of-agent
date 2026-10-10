# Armazenamento seguro e MASVS

Verificado em 2026-10-10. Fontes oficiais: Android Keystore (V-82, https://developer.android.com/privacy-and-security/keystore), Keychain (V-83, https://developer.apple.com/documentation/security/restricting-keychain-item-accessibility.md), OWASP MASVS (V-25, https://mas.owasp.org/MASVS/). Redação própria. Mapeamentos para MASVS são do plugin. **Não cite níveis (L1/L2/R) nem IDs de controle**: a página lida não os traz e o MASTG não foi aberto (lacuna 2).

Regra do plugin (S-06): **segredo ou chave de serviço nunca no cliente.** Binários são inspecionáveis. Token de usuário em Keychain/Keystore, nunca em `UserDefaults`, `SharedPreferences` ou arquivo (V-82 trata de chaves e não menciona SharedPreferences; essa parte é **Inferido** e consistente com MASVS-STORAGE).

## Procurar no código

- Segredos embutidos: Grep `(api[_-]?key|secret|token|password|passwd|private[_-]?key|BEGIN (RSA|EC|PRIVATE))` (ignorando testes e exemplos); `google-services.json` e `GoogleService-Info.plist` contêm identificadores de projeto (não são segredos de servidor), mas chaves de servidor FCM, `.p8` do APNs, credenciais de contas de serviço e chaves de API privilegiadas **não** podem estar no app.
- Armazenamento: `UserDefaults|NSUserDefaults|SharedPreferences|AsyncStorage|SecureStore|Keychain|KeychainAccess|EncryptedSharedPreferences|flutter_secure_storage|AndroidKeyStore`.
- Logs: `print(|NSLog(|Log\.[dviwe]\(|console\.log\(|debugPrint\(` com token, e-mail, documento ou payload completo.
- Rede: ATS desativado (`NSAllowsArbitraryLoads`), `cleartextTrafficPermitted="true"` na config de segurança de rede (**Inferido**).

**Nunca reproduza o valor de um segredo encontrado** na resposta: cite `arquivo:linha`, o tipo e recomende rotação.

## Android Keystore (V-82), checklist

1. Chave criada no Keystore; o material nunca entra no processo do app e é **não exportável** (operações no processo do sistema). Não guarde "segredo bruto" no cliente: guarde uma chave no Keystore que cifra o dado.
2. Pode ficar em hardware seguro (TEE ou Secure Element) se o aparelho suportar algoritmo, modos de bloco, preenchimento e digests. **StrongBox** no Android 9+ (API 28).
3. Verificar o nível: `KeyInfo.getSecurityLevel()` (API 29+) ou `isInsideSecurityHardware()` (API 28 e inferior).
4. Exigir autenticação para ações sensíveis: `BiometricPrompt` com `setUserAuthenticationParameters()`; `canAuthenticate()` para checar disponibilidade.
5. Chave só biométrica é **invalidada** ao cadastrar nova biometria (padrão); `setInvalidatedByBiometricEnrollment(false)` muda isso. Trate a invalidação (reautenticar e recriar a chave).
6. `KeyChain` serve para credenciais de sistema aprovadas pelo usuário.
7. Limite honesto: com o SO comprometido, o atacante pode **usar** as chaves, mas não extraí-las.

```kotlin
val spec = KeyGenParameterSpec.Builder("token_key", KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT)
    .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
    .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
    .setUserAuthenticationRequired(true)       // ações sensíveis; ver setUserAuthenticationParameters
    .build()
KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore").run { init(spec); generateKey() }
```

(Esboço: parâmetros de autenticação variam com a API; confirme com a documentação da versão. **Inferido**.)

## Keychain iOS (V-83), checklist

1. Defina `kSecAttrAccessible` na criação. Ordem de restrição decrescente: **When Passcode Set** (o item some se o código for removido), **When Unlocked** (padrão), **After First Unlock** (para acesso em segundo plano), **Always** ("não recomendada", não "depreciada").
2. "Use sempre a opção mais restritiva que faça sentido": `WhenUnlocked` por padrão; `AfterFirstUnlock` só com necessidade real em segundo plano.
3. Sufixo **`ThisDeviceOnly`**: restaura no mesmo aparelho a partir do backup e não migra para outro. Para dados muito sensíveis que não devem ir ao iCloud: `kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly`.
4. Presença do usuário em ações financeiras: `SecAccessControl` com flag `userPresence` (ou biometria específica); `applicationPassword` pede senha própria.
5. Item sincronizável só aceita variantes sem `ThisDeviceOnly`: lógica consistente mas **Inferido** (V-83).
6. Metadados protegidos por Secure Enclave: fonte não aberta (Apple Platform Security).

```swift
let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrAccount as String: "refresh_token",
    kSecValueData as String: Data(token.utf8),
    kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
]
let status = SecItemAdd(query as CFDictionary, nil)
// tratar errSecDuplicateItem com SecItemUpdate; nunca registrar o token em log
```

## MASVS por grupo (V-25): uma linha de "o que verificar"

| Grupo | O que verificar |
| --- | --- |
| STORAGE | Dados sensíveis só em Keychain/Keystore ou cifrados; nada em log, backup desnecessário, cache ou captura de tela |
| CRYPTO | Algoritmos e modos do SO/framework; sem criptografia caseira; chaves no Keystore/Keychain |
| AUTH | Sessão e biometria tratadas no cliente sem substituir a validação no servidor; expiração e logout limpam estado |
| NETWORK | TLS; sem desativar validação; sem tráfego em texto claro; fixação de certificado só com política de rotação |
| PLATFORM | Permissões mínimas; componentes exportados; deep links validados (`deep-links.md`); WebView restrita |
| CODE | Dependências atualizadas; sem segredos no binário; `console.*`/debug fora de release |
| RESILIENCE | Medidas anti-adulteração conforme o risco do app (não assumir que ofuscação é segurança) |
| PRIVACY | Dados mínimos; consentimento; manifesto de privacidade e Data safety coerentes (`mobile-store-release-check`) |

As linhas são orientações do plugin sobre os oito grupos nomeados na página (Verificado: nomes); o detalhe de cada controle não foi lido.

## Saída de achado de segurança

Severidade, confiança (1 a 10), `arquivo:linha`, cenário concreto, correção e rótulo. Limiar: em dúvida, não reporte como falha; registre como pergunta ou **Suposição**. Achado crítico de backend ou supply chain é encaminhado ao segmento `security-appsec`.
