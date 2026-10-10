# Relatório de auditoria de app desktop

Auditoria por leitura de configuração e código. O app, o instalador e as ferramentas de terceiros não foram executados; nada foi instalado. Severidades são da fábrica (Inferido). Comportamento em runtime é Não verificável por leitura.

## Cabeçalho

- Projeto: [NOME] · Stack: [Electron | Tauri v2 | WPF | WinUI 3 | MAUI | Qt] · Versão: [VERSÃO] (fonte: [package.json | Cargo.lock | csproj])
- Conteúdo remoto carregado: [sim/não; origens]
- Escopo lido: [ARQUIVOS] · Data: [AAAA-MM-DD] · Revisor: [modelo ou pessoa]

## Mapa da fronteira de confiança

| Janela | Origem do conteúdo | Preload | Canais IPC ou comandos expostos | Permissões ou capabilities |
| --- | --- | --- | --- | --- |
| [main] | [local/remoto] | [arquivo] | [lista] | [lista] |

## Achados por severidade

| ID | Severidade | Evidência (arquivo:linha) | Risco | Recomendação mínima | Fonte V | Rótulo |
| --- | --- | --- | --- | --- | --- | --- |
| DSK-E02 | Crítica | `main.js:12` `nodeIntegration: true` com `loadURL` remoto | Conteúdo remoto com acesso ao Node | Desligar; preload específico; CSP | V-16 | Verificado (arquivo lido) |

A linha de exemplo ilustra o formato; apague-a. Item do checklist sem relação com a superfície do app (por exemplo `<webview>` sem uso) não é achado.

## Electron: fuses (V-48)

| Fuse | Valor encontrado | Recomendado | Rótulo |
| --- | --- | --- | --- |
| OnlyLoadAppFromAsar | [ ] | ligado | Inferido |
| RunAsNode | [ ] | desligado | Inferido |
| EnableNodeOptionsEnvironmentVariable | [ ] | desligado | Inferido |
| EnableNodeCliInspectArguments | [ ] | desligado | Inferido |
| GrantFileProtocolExtraPrivileges | [ ] | desligado | Inferido |
| EnableCookieEncryption | [ ] | ligado | Inferido |
| EnableEmbeddedAsarIntegrityValidation | [ ] | ligado | Inferido |

## Tauri: capabilities, comandos, isolation, CSP (V-19, V-47)

[Uma linha por capability: identifier, windows, permissions, remote. `AppManifest::commands` em `build.rs`? CSP? Isolation? Validação de entrada nos comandos Rust?]

## .NET (V-33 a V-37)

[Comandos e binding, ViewModel sem controles, 7 itens de acessibilidade do WinUI. Narrator é verificação humana.]

## Não verificável

- [Runtime (CSP efetiva, navegação), versão exata em uso, Linux, segurança e acessibilidade de Qt e .NET desktop (sem fonte), acessibilidade de Electron e Tauri (sem fonte).]

## Recomendações mínimas (ordem de aplicação)

1. [ ]

## Limitações

[O que não foi lido; severidades Inferido; nomes de permissão do Tauri variam por plugin.]

## Veredito e próximo passo

[Resultado] · [Próximo passo e quem executa]
