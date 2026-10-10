# macOS, auto-update e Linux (referência de release)

Verificado em 2026-10-10 contra V-18, V-20, V-21, V-38, V-45, V-46, V-49 e V-65. A página da Apple não traz sintaxe de comando; a sintaxe de `notarytool` e `stapler` que circula em respostas de ferramentas é **Não verificada**. Nenhum comando abaixo foi executado, e nada deve ser executado pela fábrica: são itens de revisão e material para o usuário.

Sumário: [macOS](#macos-notarização-v-45) · [Qt macdeployqt](#qt-no-macos-v-38) · [Electron](#electron-updater-v-18) · [Tauri](#tauri-updater-v-20-v-46) · [Sparkle](#sparkle-v-49) · [Linux](#linux) · [Comparação](#comparação-dos-updaters)

## macOS: notarização (V-45)

Fontes: https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution (o corpo veio do endpoint de dados da Apple, porque a página HTML só devolve o título), https://v2.tauri.app/distribute/sign/macos/, https://doc.qt.io/qt-6/macos-deployment.html.

O que a fonte diz:

- Notarização é verificação automatizada (não é App Review) que gera um ticket para grampear (staple) no software.
- Software assinado com novo certificado Developer ID precisa ser notarizado a partir do macOS 10.14.5; o distribuído com Developer ID e compilado depois de 1/6/2019, a partir do macOS 10.15.
- Requisitos: assinatura válida em todos os executáveis; certificado **Developer ID** (não Mac Distribution, ad hoc, Apple Developer nem local); Hardened Runtime em apps e alvos de linha de comando; timestamp seguro; **sem** a entitlement `com.apple.security.get-task-allow` verdadeira; entitlements em XML ASCII; plugins herdam as entitlements do host.
- Ferramentas citadas pela Apple: `notarytool` e `stapler`, incluídas no Xcode. A Apple recomenda revisar o log do serviço.
- Tauri: certificado "Developer ID Application" (só o Account Holder o cria); notarização por variáveis de ambiente, via chave de API do App Store Connect (`APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH`) ou via Apple ID (`APPLE_ID`, `APPLE_PASSWORD`, `APPLE_TEAM_ID`); em CI o `.p12` em base64 (`APPLE_CERTIFICATE`, `APPLE_CERTIFICATE_PASSWORD`); assinatura ad hoc (`"-"`) não evita a aprovação do usuário em Privacidade e Segurança. A página do Tauri não trata de Hardened Runtime nem de entitlements.

IDs e severidades padrão: os do `checklist-completo.md` do playbook (REL-M01 a M06); REL-M07 é extensão desta skill.

| ID | Verificar | Sev. padrão |
| --- | --- | --- |
| REL-M01 | Certificado Developer ID Application (não ad hoc, Mac Distribution nem local) na configuração de build | Alta |
| REL-M02 | Hardened Runtime ligado e timestamp seguro | Alta |
| REL-M03 | Entitlements: sem `get-task-allow` verdadeira; XML ASCII; no máximo um `.entitlements` em `Contents/Resources/` (Qt) | Alta |
| REL-M04 | Comando de notarização conferido com `--help` da versão instalada, nunca escrito de memória; passo documentado como do usuário (notarizar, ler o log, grampear) | Média |
| REL-M05 | Credenciais Apple só por variável de ambiente do CI ou chaveiro; nunca no repositório nem em argumento | Crítica se versionadas |
| REL-M06 | Sparkle: EdDSA, `SUPublicEDKey`, feed por HTTPS e assinado (`SURequireSignedFeed`) | Média |
| REL-M07 | Teste em macOS limpo | Não verificável aqui |

Passos de execução (notarizar, aceitar termos da conta, criar certificado) são **ação do usuário**. Para o campo "comando exato" da ficha, instrua: "confira `xcrun notarytool --help` e `xcrun stapler --help` na versão do Xcode instalada e preencha".

## Qt no macOS (V-38)

`macdeployqt`: `-dmg`, `-qmldir=`, `-always-overwrite`, `-verbose=0..3`. A assinatura padrão é **ad hoc**: use `-codesign=<identidade>`. `-sign-for-notarization=<identidade>` liga `-hardened-runtime`, `-timestamp` e o `-codesign` (exigem internet). Usa o primeiro `.entitlements` achado em `Contents/Resources/`; mantenha no máximo um. `-appstore-compliant` pula componentes com API privada.

## Electron: updater (V-18)

Fonte: https://www.electronjs.org/docs/latest/tutorial/updates.

| ID | Verificar | Observação |
| --- | --- | --- |
| REL-U08 | Servidor de atualização escolhido (Squirrel; alternativas citadas na página: Hazel, Nuts, electron-release-server, Nucleus) e, se `update.electronjs.org`, repositório GitHub **público** | `update.electronjs.org` exige repositório público com builds em GitHub Releases (e builds assinados no macOS); alternativas privadas não foram avaliadas |
| REL-U03 | Caminho "sem atualização" testado | Squirrel.Windows serve `RELEASES` em `/RELEASES` mesmo sem atualização; Squirrel.Mac responde JSON com `url` obrigatória ou 204 |
| REL-U06 | Código de update só em app empacotado (`app.isPackaged`); evento `error` tratado e registrado | |
| REL-U04 | Atualização da versão anterior para a nova, com build assinado | O Squirrel.Mac exige app assinado para atualizar |
| REL-U07 | Plano de rollback e aviso ao usuário quando o download termina | |

Dica de revisão: `safeStorage` pode voltar a pedir permissão no Keychain depois de cada atualização quando o app não é assinado ou usa assinatura ad hoc (V-17).

## Tauri: updater (V-20, V-46)

Fonte: https://v2.tauri.app/plugin/updater/.

- Assinatura **obrigatória e impossível de desligar**. `pubkey` em `plugins.updater` recebe o **conteúdo** da chave pública.
- Chave privada por `TAURI_SIGNING_PRIVATE_KEY` (caminho ou conteúdo) e `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` (opcional). Arquivos `.env` **não** funcionam para isso. Guarde a chave fora do repositório.
- Manifesto estático exige `version` e, por plataforma, `url` e `signature` (conteúdo do `.sig`, não caminho). Servidor dinâmico responde 204 sem atualização e 200 com `url`, `version` e `signature`.
- TLS obrigatório em produção (`dangerousInsecureTransportProtocol` existe para exceções: é achado).
- Windows: `installMode` pode ser `passive` (padrão), `basicUi` ou `quiet` (desencorajado). Salve o estado antes do fechamento.

Modelo de manifesto estático (ilustrativo; a chave `platforms` e seus nomes seguem a documentação do Tauri e devem ser conferidos na versão usada):

```json
{
  "version": "1.2.0",
  "notes": "Correções e melhorias",
  "pub_date": "2026-10-10T12:00:00Z",
  "platforms": {
    "windows-x86_64": {
      "signature": "<CONTEÚDO DO ARQUIVO .sig, NÃO O CAMINHO>",
      "url": "https://<HOST_DO_USUARIO>/app_1.2.0_x64-setup.exe"
    }
  }
}
```

| ID | Verificar | Sev. padrão |
| --- | --- | --- |
| REL-U01 | Chave privada fora do repositório e fora de `.env` versionado | Crítica |
| REL-U02 | Endpoint de update em HTTPS (`dangerousInsecureTransportProtocol` é exceção e achado) | Alta |
| REL-U03 | Endpoint responde 204 sem atualização | Média |
| REL-U04 | Teste da versão anterior para a nova com build assinado | Alta |
| REL-U05 | **Hipótese a testar:** Authenticode reescreve o binário e invalida a assinatura do updater, então assinar com Authenticode primeiro e regenerar os `.sig` (relato único da Fluxzy, 2026-05-09). As páginas oficiais do updater e da assinatura Windows **não** tratam da ordem. Teste com build descartável; nunca apresente como regra (V-21) | Média |
| REL-U09 | `pubkey` com o conteúdo da chave pública; manifesto completo validado antes de publicar (extensão desta skill) | Média |

## Sparkle (V-49)

Fonte: https://sparkle-project.org/documentation/ (repositório MIT, com componentes sob BSD e zlib).

- Feed (appcast) em XML na URL de `SUFeedURL` no `Info.plist`.
- Chaves EdDSA geradas com `generate_keys` (privada no chaveiro do login; pública em `SUPublicEDKey`). **A fábrica não roda `generate_keys`**: gera segredo.
- `generate_appcast` gera o appcast e os arquivos `.delta`.
- `SURequireSignedFeed` assina feed e notas e exige `SUVerifyUpdateBeforeExtraction` (feed assinado é validado a partir do Sparkle 2.9; notas em `.md` a partir do 2.9 e macOS 12). Versões mudam: confira.
- HTTPS e notarização com Developer ID são **recomendações**, não exigências. Atualização delta é ignorada se o app não bater o checksum.

Checklist (REL-M06, REL-U01, REL-U02, REL-U04): EdDSA e chave privada fora do repositório · appcast por HTTPS · app assinado e notarizado (V-45) · feed assinado · teste da versão anterior.

## Linux

Sem fonte oficial lida. Sinais de HN, não cruzados (V-65): WebKitGTK como principal dor do Tauri; AppImage gerado em um Ubuntu pode falhar em outras distribuições por glibc; Tauri "mais leve, mas não leve". Registre **Não verificável** (REL-L01, severidade Média no playbook) e recomende testar nas distribuições-alvo, preferencialmente a mais antiga que se pretende suportar, antes de publicar.

## Comparação dos updaters

| Aspecto | Electron | Tauri v2 | Sparkle (macOS) |
| --- | --- | --- | --- |
| Assinatura do pacote de update | Depende do servidor/Squirrel; macOS exige app assinado | Obrigatória (chave própria do Tauri) | EdDSA obrigatória no fluxo recomendado |
| Formato do feed | `RELEASES` (Windows); JSON ou 204 (Mac) | JSON estático ou resposta dinâmica (204 ou 200) | Appcast XML |
| Sem atualização | `RELEASES` mesmo sem atualização; 204 no Mac | 204 | Appcast sem item novo |
| Segredo | Certificado de assinatura do app | `TAURI_SIGNING_PRIVATE_KEY` | Chave EdDSA privada no chaveiro |
| Armadilha | Repositório público para `update.electronjs.org` | `.env` não funciona; `pubkey` é o conteúdo | Versão do Sparkle altera opções |
