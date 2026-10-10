# Tauri v2: checklist de segurança (capabilities, isolation, CSP)

Verificado em 2026-10-10 contra V-19 (segurança e capabilities; página com "Last updated: Jul 22, 2026") e V-47 (isolation e CSP). Trechos de configuração e de Rust são ilustrativos, **não foram compilados** e os nomes de permissão variam por plugin e por versão: confirme em https://v2.tauri.app/security/ na versão usada. Severidade e padrões de busca são da fábrica (Inferido).

Sumário: [Modelo de confiança](#modelo-de-confiança) · [Itens](#itens) · [Trechos](#trechos-de-referência) · [Padrões de busca](#padrões-de-busca)

## Modelo de confiança

- Núcleo Rust: acesso irrestrito ao sistema. Frontend (WebView): vê só o que o IPC expõe. A fronteira cruza com dados que devem ser inspecionados e definidos com rigor (V-19; a página não usa a palavra "validar").
- Capabilities restringem comandos por janela. A fronteira segue o **rótulo** da janela, não o título (V-19).
- Por padrão todos os comandos registrados em `invoke_handler` são chamáveis por todas as janelas, a menos que `AppManifest::commands` em `build.rs` restrinja (V-19).
- Em Linux e Android o Tauri não distingue iframe da janela (V-19).
- O WebView do sistema recebe atualizações de segurança do sistema (V-19), o que também significa que o comportamento varia por plataforma.

## Itens

DSK-T01 a T07 e as severidades padrão são os do `checklist-completo.md` do playbook; DSK-T08 a T13 são extensões desta skill (Inferido quanto à numeração e à severidade).

| ID | Verificar | Detectar | Sev. padrão | Fonte |
| --- | --- | --- | --- | --- |
| DSK-T01 | Uma capability por janela, com `windows` explícito | capability única para várias janelas; arquivo em `src-tauri/capabilities` sem `windows` | Alta | V-19 |
| DSK-T02 | Nenhum `remote.urls` amplo (`https://*`) nem sem justificativa escrita | `remote` em capabilities | Alta | V-19 |
| DSK-T03 | CSP configurada: `default-src` restrito, `connect-src` mínimo, sem CDN | `app.security.csp` ausente ou `null`; `unsafe-eval`; domínios de CDN | Média (média a alta se há conteúdo remoto) | V-47 |
| DSK-T04 | `AppManifest::commands` restringe o padrão "todos chamam todos" | `build.rs` sem `AppManifest` | Alta | V-19 |
| DSK-T05 | Entrada validada e tipada em cada comando Rust (tipos, tamanhos, caminhos dentro de pastas esperadas) | corpo dos `#[tauri::command]` com `String`/`PathBuf` usados direto em `fs` ou `Command` | Alta | V-19, V-47 |
| DSK-T06 | Isolation pattern ligado quando o frontend tem dependências de terceiros | `app.security.pattern` ausente | Média | V-47 |
| DSK-T07 | Quem cria janelas é controlado (o rótulo é a fronteira) | `WebviewWindowBuilder::new` com rótulo vindo de entrada do frontend | Média (alta se o rótulo vem do frontend) | V-19 |
| DSK-T08 | Lista mínima de comandos expostos (inventário) | `invoke_handler`, `generate_handler!`, `#[tauri::command]` | Info | V-19 |
| DSK-T09 | Permissões mínimas por capability | `permissions` com conjuntos amplos de plugins (nomes variam; leia cada plugin) | Média a Alta | V-19 |
| DSK-T10 | Se `tauri.conf.json` lista capabilities, só elas entram no build; a lista é a pretendida | campo de capabilities em `app.security` | Média | V-19 |
| DSK-T11 | Updater sem transporte inseguro | `dangerousInsecureTransportProtocol` | Alta | V-20 |
| DSK-T12 | Política de reporte de vulnerabilidade no README | `SECURITY.md`/README | Baixa | V-19 |
| DSK-T13 | Não depender de iframe como isolamento em Linux/Android | frames com conteúdo remoto | Média | V-19 |

Isolation e CSP **não** substituem capabilities (V-47). Para T11, o resto do updater (chaves, manifesto, assinatura) é tema de `desktop-release-checklist`.

## Trechos de referência

Capability de uma janela (modelo de V-19; `core:default` é o conjunto padrão do núcleo, estável, e as permissões adicionais dependem dos plugins):

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "janela-principal",
  "description": "Permissões mínimas da janela principal",
  "windows": ["main"],
  "permissions": ["core:default"]
}
```

Restringir os comandos do app em `build.rs` (V-19 cita `AppManifest::commands`; a forma exata do builder pode variar entre versões do `tauri-build`: confirme):

```rust
fn main() {
    tauri_build::try_build(
        tauri_build::Attributes::new().app_manifest(
            tauri_build::AppManifest::new().commands(&["abrir_projeto", "salvar_projeto"]),
        ),
    )
    .expect("falha ao configurar o build do Tauri");
}
```

CSP e isolation em `tauri.conf.json` (valores de exemplo de V-47; ajuste ao app):

```json
{
  "app": {
    "security": {
      "csp": "default-src 'self' customprotocol: asset:; connect-src ipc: http://ipc.localhost",
      "pattern": { "use": "isolation", "options": { "dir": "../isolation" } }
    }
  }
}
```

Notas de V-47: hashes para scripts locais e nonces para estilos e scripts externos são acrescentados no build; `'wasm-unsafe-eval'` em `script-src` para WebAssembly; evite conteúdo remoto como CDN. A isolation app roda em `<iframe>` em sandbox, intercepta a mensagem IPC antes do núcleo e a cifra com AES-GCM com chave gerada em tempo de execução; mantenha-a mínima. No hook de isolation, valide caminhos de arquivo (dentro de pastas esperadas) e a origem das requisições. No Windows, arquivos externos não carregam no iframe e módulos ES não funcionam.

Comando Rust com entrada validada (ilustrativo):

```rust
use std::path::PathBuf;

#[tauri::command]
fn salvar_projeto(nome: String, conteudo: String) -> Result<(), String> {
    if nome.is_empty() || nome.len() > 64 || !nome.chars().all(|c| c.is_alphanumeric() || c == '-' || c == '_') {
        return Err("nome inválido".into());
    }
    let destino: PathBuf = pasta_de_projetos().join(format!("{nome}.json"));
    std::fs::write(destino, conteudo).map_err(|e| e.to_string())
}
```

O ponto do trecho é a validação na fronteira: um `nome` com `..` ou separador de caminho nunca chega ao sistema de arquivos. `pasta_de_projetos()` é uma função do app, fora deste exemplo.

## Padrões de busca

| Objetivo | Expressão (Grep) | Onde |
| --- | --- | --- |
| Comandos expostos | `invoke_handler`, `generate_handler`, `tauri::command` | `src-tauri/src/**/*.rs` |
| Restrição de comandos | `AppManifest` | `src-tauri/build.rs` |
| Capabilities | `"windows"`, `"permissions"`, `"remote"` | `src-tauri/capabilities/*.json`, `*.toml` |
| Capabilities no config | `capabilities` | `src-tauri/tauri.conf.json` |
| CSP e isolation | `csp`, `pattern`, `isolation` | `src-tauri/tauri.conf.json` |
| Criação de janelas | `WebviewWindowBuilder`, `WebviewWindow::new` | `src-tauri/src/**/*.rs` |
| Updater inseguro | `dangerousInsecureTransportProtocol` | `src-tauri/tauri.conf.json` |
| Uso direto de entrada | `std::fs`, `std::process::Command`, `PathBuf::from` | corpo dos comandos |
