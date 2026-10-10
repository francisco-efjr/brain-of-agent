# Checklist de release de app desktop

Leitura e planejamento. Nada é assinado, notarizado, instalado nem publicado por este checklist. Cada linha precisa de evidência (arquivo:linha ou saída colada) ou "não encontrado". Fatos voláteis levam URL e data da consulta. Itens com efeito externo viram uma ficha (`ficha-de-acao-externa.md`) e ficam na lista "Ações do usuário".

- Projeto: [NOME] · Stack e instalador: [ ] · Canal: [Store | site | winget | corporativo] · Arquiteturas: [ ]
- Região e tipo de conta (afetam Azure Artifact Signing): [ ] · Data da verificação: [AAAA-MM-DD]

## Windows

| Item | Status (conforme / lacuna / NV / NA) | Evidência | Fonte | Fato volátil (URL, data) |
| --- | --- | --- | --- | --- |
| Certificado escolhido pela árvore (MSIX Store, Azure Artifact Signing, OV com HSM ou nuvem, SignPath); sem "EV obrigatório" | [ ] | [ ] | V-44 | [ ] |
| Mesma identidade de assinatura em todas as releases | [ ] | [ ] | V-44 | |
| `signtool sign` com `/fd SHA256`, `/tr` e `/td SHA256`; `signtool verify /pa` ao final | [ ] | [ ] | V-44 | |
| Senha e chave fora do repositório e fora de argumentos | [ ] | [ ] | V-44 | |
| Arquivo não modificado após assinar | [ ] | [ ] | V-44 | |
| Instalador: MSIX (identidade, `.appinstaller` HTTPS) / Inno (`SignTool`, `$f`) / WiX (cabs, MSI, Burn, bundle) / NSIS ou MSI do Tauri | [ ] | [ ] | V-40, V-41, V-42, V-46 | |
| WiX v7: decisão do usuário sobre EULA e OSMF registrada | [ ] | [ ] | V-42 | |
| winget: manifesto, SHA256 recalculado, silencioso testado, `winget validate` | [ ] | [ ] | V-43 | |
| Aviso do SmartScreen na primeira release documentado | [ ] | [ ] | V-44 | |

## macOS

| Item | Status | Evidência | Fonte |
| --- | --- | --- | --- |
| Developer ID Application; Hardened Runtime; timestamp seguro | [ ] | [ ] | V-45 |
| Sem `get-task-allow` verdadeira; entitlements em XML ASCII | [ ] | [ ] | V-45 |
| Comando de notarização conferido com `xcrun notarytool --help` (sintaxe não verificada pela fábrica) | [ ] | [ ] | V-45 |
| Credenciais por variáveis do CI ou chaveiro; nunca no repositório ou em argumento | [ ] | [ ] | V-45 |
| Sparkle: EdDSA, `SUFeedURL` HTTPS, `SUPublicEDKey`, feed assinado | [ ] | [ ] | V-49 |
| Qt: `macdeployqt -sign-for-notarization` com identidade real | [ ] | [ ] | V-38 |

## Linux

Sem fonte oficial lida (AppImage, glibc, WebKitGTK por relato do HN). Registrar Não verificável e as distribuições-alvo a testar.

## Auto-update

| Item | Status | Evidência | Fonte |
| --- | --- | --- | --- |
| Chave privada fora do repositório (`TAURI_SIGNING_PRIVATE_KEY` do cofre do CI) | [ ] | [ ] | V-20 |
| Endpoint HTTPS; manifesto validado antes de publicar | [ ] | [ ] | V-20 |
| Caso "sem atualização" (RELEASES, 204) testado | [ ] | [ ] | V-18, V-20 |
| Atualização da versão anterior assinada para a nova testada | [ ] | [ ] | V-18, V-20, V-49 |
| Electron: `app.isPackaged`, evento `error`; servidor escolhido | [ ] | [ ] | V-18 |
| Tauri: ordem Authenticode e `.sig` testada (hipótese, V-21) | [ ] | [ ] | V-21 |
| Plano de rollback | [ ] | [ ] | Inferido |

## Máquina limpa (VM, Windows Sandbox)

| Passo | Resultado | Evidência |
| --- | --- | --- |
| Instalar | [ ] | [ ] |
| Primeira execução (aviso esperado do SmartScreen) | [ ] | [ ] |
| Atualizar de N-1 para N | [ ] | [ ] |
| Desinstalar sem resíduos | [ ] | [ ] |

## Licenças

Qt: módulos só-GPL cruzados (V-39). WiX (V-42). Inno (V-41). Ferramentas GPL não embutidas (V-61). Não é aconselhamento jurídico.

## Ações do usuário (a fábrica não executa)

1. [ ] [Ação] com ficha `ficha-de-acao-externa.md` nº [ ]

## Não verificável

[Linux, macOS físico, Narrator, comportamento do updater em produção, política da Store.]
