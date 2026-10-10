# Exemplo completo de relatório (caso sintético)

Entrada do usuário: "Vou subir amanhã meu app SwiftUI (login e-mail/senha + Google, foto de perfil pela câmera, Firebase Analytics). O `Info.plist` tem só `CFBundleDisplayName` e `UIRequiredDeviceCapabilities`, não tenho `PrivacyInfo.xcprivacy`, o app cria conta mas só tem botão de logout. O que falta?"

O exemplo mostra o nível de detalhe esperado. Os arquivos e linhas são fictícios; num caso real, cada linha vem de Grep/Read da sessão.

---

# Prontidão de loja: FotoDespesas (iOS) — 2026-10-10

Escopo lido: `Info.plist`, `FotoDespesas/Auth/AuthView.swift`, `Camera/CameraService.swift`, `Package.resolved`, lista de arquivos `*.swift` (38). Não lido: notas de revisão, metadados do App Store Connect. Build: **não executado** (leitura de código; sem macOS nesta sessão).

## Resumo

Três lacunas bloqueiam a submissão com risco provável de rejeição e uma pergunta ao usuário muda o resultado do item 4.8. Nada aqui garante aprovação.

## Achados

| Prioridade | Regra | Evidência | Impacto | Correção mínima | Rótulo |
| --- | --- | --- | --- | --- | --- |
| Risco provável de rejeição | 5.1.1(v) exclusão de conta | `AuthView.swift:41` cria conta; Grep `delete.?account\|excluir.?conta` sem resultado nos 38 `.swift`; só existe `logout()` em `SettingsView.swift:77` | O app cria conta e não oferece exclusão no app | Tela "Excluir conta" em Ajustes com confirmação, chamando o endpoint de exclusão do backend | Verificado (V-16) |
| Risco provável de rejeição | Purpose string de câmera | `CameraService.swift:12` usa `AVCaptureDevice`; `NSCameraUsageDescription` ausente em `Info.plist` (só 2 chaves) | Acesso à câmera falha e o upload pode ser rejeitado com ITMS-90683 | Adicionar `NSCameraUsageDescription` com frase específica ("Usamos a câmera para você fotografar o recibo e anexá-lo à despesa") e traduzir em `InfoPlist.xcstrings` | Verificado (V-58) |
| Alto | Privacy manifest | Glob `**/PrivacyInfo.xcprivacy`: 0 resultados; `Package.resolved` lista Firebase | O manifesto do app e os dos SDKs são exigidos conforme coleta de dados e required reason APIs; Firebase Analytics coleta dados | Criar `PrivacyInfo.xcprivacy` com tipos coletados e `NSPrivacyAccessedAPITypes` (Grep de `UserDefaults` retornou 6 usos, `Storage.swift:9`) e motivo por API; atualizar o SDK para a versão que traz manifesto | Verificado (V-17); versão do SDK: Não verificável |
| Alto | 4.8 login equivalente | `AuthView.swift:58` usa Google Sign-In | A regra se aplica a login de terceiro; há também login por e-mail e senha | **Conferir no texto atual da 4.8** se o login próprio já atende; não afirmo violação | Verificado (V-16) quanto à existência da regra; critério fino: Inferido |
| Médio | 2.1 conta de demonstração | Sem evidência no código | O revisor precisa entrar no app | Credenciais de demonstração nas notas de revisão, backend no ar | Verificado (V-16) |
| Baixo | Notas de versão | Nenhum arquivo de notas | Texto público da versão | Rascunho em arquivo, sem detalhes internos (P-26) | Inferido |

## Pontos fortes

- Fluxo de login separado em módulo próprio (`Auth/`), o que facilita adicionar a exclusão de conta.
- Chaves de API do Firebase não aparecem em `Info.plist` nem em `.swift` (Grep `AIza` sem resultado).

## Ações do usuário

1. Configurar metadados, classificação etária e política de privacidade no App Store Connect (itens que não mudam após o envio, V-73).
2. Fornecer conta de demonstração às notas de revisão.
3. Fazer archive, "Validate App" e upload no Xcode (macOS), e enviar para revisão. O plugin nunca aciona "Submit for Review".

## Não verificável

- Archive, validação e presença da build no TestFlight (sem macOS).
- Fim da seção 5 das App Review Guidelines (não lido, V-16).
- Comportamento real do revisor.

Fatos de loja: App Review Guidelines (https://developer.apple.com/app-store/review/guidelines/), privacy manifest (https://developer.apple.com/documentation/bundleresources/privacy-manifest-files), purpose strings (https://developer.apple.com/documentation/uikit/requesting-access-to-protected-resources.md). Verificados em 2026-10-10; reconferir antes de submeter.
