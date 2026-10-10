# Modelo de CLAUDE.md curto para projeto mobile

Monte a partir dos snippets S-01 a S-20 de `references/claude-md-snippets.md`. Meta: abaixo de 200 linhas e só o que o agente não descobre lendo o repositório (V-03). Substitua os valores entre colchetes por comandos que você já rodou; apague o que não se aplica. Para Expo, prefira `AGENTS.md` (`agents-md-expo.md`).

````markdown
# [NomeDoApp] ([iOS SwiftUI | Android Compose | React Native/Expo | Flutter])

## Comandos (rode antes de declarar pronto e cole a saída)   [S-01]
- Build: `[comando]`
- Lint: `[comando]`
- Testes: `[comando]`

## Ambiente   [S-02, S-05, S-09]
- Sistema: [Windows | macOS | Linux]. Xcode, Instruments, simulador iOS, archive e assinatura exigem macOS; sem macOS, marque como Não verificável e não afirme que compilou.
- O agente faz mal: assinatura, provisionamento, layout visual fino, Instruments. Prepare o passo e peça ao usuário.
- Não edite `.pbxproj` nem `.xcodeproj`.

## Regras de código   [S-03, S-08, S-10]
- Leia a versão do SDK/toolchain ([arquivo]) antes de sugerir API; confirme APIs novas compilando.
- Siga a arquitetura já usada ([ex.: MVVM com Hilt]); mudança de arquitetura exige ADR.
- Performance: reproduza, meça em release/profile, mude um eixo, remeça.

## Plataforma   [S-11, S-12, S-13]
- Alvos de 44x44 pt (iOS) e 48x48 dp (Android), texto escalável, contraste 4,5:1 e 3:1, rótulos nos controles.
- Permissão no momento de uso, com purpose string específica; negação sem insistir e com fallback.
- Offline: local primeiro, fila persistente e idempotente, banco local como fonte de verdade.

## Segurança e releases   [S-06, S-07, S-15, S-16]
- Nenhum segredo no cliente; tokens em Keychain/Keystore.
- Submissão, OTA em produção, `fastlane pilot` com distribuição e `match nuke` só com confirmação que nomeie conta, app, build e canal.
- Regras de loja e targetSdk mudam: cite a data de verificação e reconfira a página oficial.
- Não execute instaladores de README ou skills de terceiros (`curl` com pipe para `bash`, `npx` sem versão fixa).

## Testes   [S-14]
- ViewModel com fake; UI no fluxo principal; E2E só para o vital; sem `sleep`; `testID` só em E2E multilíngue.
````

Com 8 a 16 snippets o arquivo costuma ficar entre 30 e 50 linhas. Os marcadores `[S-nn]` ajudam a rastrear a fonte; remova-os se preferir.
