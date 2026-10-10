# Ficha de ação de release

Gate de confirmação nomeada (modelo de V-34, estendido por V-35, V-71, V-72 e V-73). Preencha **antes** de executar qualquer efeito externo: `eas update` em produção, `eas build` de produção, `eas submit`, `--auto-submit`, atalho de TestFlight, `fastlane pilot` com distribuição, promoção de trilha no Play, criação ou revogação de certificados, `match nuke`. "Submit for Review" no App Store Connect é sempre ação do usuário e não consta nesta ficha.

O agente executa **somente** o que estiver marcado "Confirmado" pelo usuário no chat, um comando por vez, colando a saída. Produção nunca é inferida pelo branch do git. Segredos nunca entram na ficha, no chat nem no log.

| Campo | Valor |
| --- | --- |
| Data da ficha | [AAAA-MM-DD] |
| Conta (organização/usuário) | [ex.: conta Expo "acme"; Apple Team ID; projeto Google Play] |
| Plataforma(s) | [iOS / Android] |
| App | [nome e identificador] |
| Build ID ou versão | [id] |
| Canal e branch (OTA) | [ex.: canal production -> branch main] |
| Ambiente | [development / preview / production] |
| `runtimeVersion` | [valor] (OTA só carrega JS, estilo e assets) |
| Perfil de build | [ex.: production] |
| Mensagem (OTA/changelog) | [texto] |
| Natureza da mudança | [só JS/estilo/assets (OTA) / nativa (nova build)] |
| Efeitos esperados | [o que muda para os usuários] |
| Rollback conhecido | [procedimento da documentação, ou "a fonte não descreve rollback; ver documentação do EAS"] |
| Ação do usuário (fora do agente) | [Submit for Review, formulários, chaves, DNS] |
| Ambiente do agente | [SO; sem macOS: archive/validação/upload local indisponíveis] |

## Comandos exatos (versões fixas; nenhum `@latest`; nenhum instalador)

1. `[comando 1]` — efeito: [ ] — Confirmado pelo usuário: [sim/não]
2. `[comando 2]` — efeito: [ ] — Confirmado pelo usuário: [sim/não]

## Confirmação

O usuário confirma por texto, repetindo conta, plataforma, build e canal: "[texto da confirmação]"

## Registro de execução

| Comando | Saída (colada) | Estado real verificado (`eas build:list`, `eas submit:list`, console da loja) | Rótulo |
| --- | --- | --- | --- |

Se algo não foi executado, diga. Se o estado final não pôde ser verificado, marque Não verificável.
