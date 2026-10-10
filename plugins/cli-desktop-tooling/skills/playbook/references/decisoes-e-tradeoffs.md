# Decisões e trade-offs

Sumário: 1. Como decidir · 2. Stack desktop · 3. Certificado Windows · 4. Instalador e canal · 5. Updater por stack · 6. TUI · 7. PowerShell ou bash · 8. CLI ou MCP · 9. Onde colocar uma regra do agente · 10. Exemplo de ADR curto

Regras: (1) restrição dura antes de preferência; (2) fato volátil com URL e data (`fontes.md`); (3) nenhum número de benchmark; (4) decisão cara de reverter vira ADR; (5) o que só um protótipo responde é dito. Os rótulos seguem o resto do plugin. O plugin recomenda; o usuário decide e executa qualquer compra, conta ou publicação.

## 1. Como decidir

1. Reúna requisitos e separe restrições duras (Store, MSIX, mobile, licença fechada, Linux, Node completo) de preferências (linguagem da equipe, tamanho).
2. Aplique os filtros duros em ordem; descarte alternativas com fonte (V-xx).
3. Compare as sobreviventes em matriz qualitativa (segurança padrão, distribuição, update, acessibilidade, curva da equipe, manutenção).
4. Liste o que exige protótipo e rotule o resto Inferido ou Suposição.
5. Registre ADR com decisão, consequências e condição de reconsiderar.

## 2. Stack desktop (V-65, V-33 a V-39, V-46)

| Se... | Então | Fonte | Rótulo |
| --- | --- | --- | --- |
| Precisa de MSIX ou identidade de pacote (Store com MSIX, push, tarefas em segundo plano) | Tauri gera só MSI e NSIS e a Store aceita EXE ou MSI; relato de bloqueio por falta de MSIX: prefira Electron ou stacks .NET | V-46, V-65, V-40 | Verificado (Tauri); Inferido (conclusão) |
| Alvo mobile ou macOS além do Windows | MAUI (exige Mac para iOS e macOS) | V-37 | Verificado |
| Só Windows nativo moderno | WinUI 3 (recomendado para novos apps; Windows 10 1809 ou posterior) | V-35 | Verificado |
| Base WPF existente, só Windows | Manter WPF; migrar de .NET Framework para .NET quando possível | V-33 | Verificado |
| Precisa de Node completo no processo principal | Electron | V-65 | Inferido |
| Pegada pequena aceitando WebView do sistema | Tauri; testar WebKitGTK cedo se Linux importa | V-65 | Não verificado contra fonte oficial (Linux) |
| Código fechado e Qt | Listar módulos e cruzar com os 14 só-GPL; LGPLv3 exige cumprir obrigações (assessoria jurídica) | V-39 | Verificado (lista); lacuna (obrigações) |
| Equipe só sabe web (React) | Electron ou Tauri com export estático; Next.js exige adaptação (sidecar no Tauri) | V-65 | Inferido (N=1) |

Protótipo obrigatório: assinar, instalar, atualizar e desinstalar em máquina limpa; WebView em Linux; ordem de assinatura do updater do Tauri; consumo e inicialização medidos pela equipe (nenhum número do relato V-65 entra).

## 3. Certificado Windows (V-44)

| Situação | Opção | Observação |
| --- | --- | --- |
| Distribui MSIX pela Store | Reassinatura pela Microsoft | Sem custo e sem aviso do SmartScreen |
| Site ou instalador próprio, região e conta elegíveis | Azure Artifact Signing | Sem token físico; não dá confiança instantânea no SmartScreen; confira preço e regiões na página |
| Site, região não elegível | OV com HSM ou assinatura em nuvem | Faixa de US$ 150 a 300 por ano na página consultada; HSM exigido desde junho de 2023 |
| Projeto de código aberto qualificado | SignPath Foundation | Gratuito |
| Desenvolvimento | Auto-assinado | Nunca em produção |
| Quer EV "para evitar o SmartScreen" | Não se justifica mais | Bypass removido em 2024 (C-1) |

## 4. Instalador e canal (V-36, V-40 a V-43, V-46)

| Necessidade | Escolha | Custo/risco |
| --- | --- | --- |
| Store e identidade de pacote | MSIX | Pacote assinado; Tauri não gera |
| Instalador clássico com script, sem MSI | Inno Setup | Licença própria permissiva; pedir licença comercial é pedido, não condição |
| MSI/bundle empresarial | WiX | OSMF (acima de US$ 10 mil de receita) e EULA a partir da v7: decisão do usuário |
| Tauri | NSIS ou MSI | Sem MSIX |
| Descoberta por linha de comando | winget | PR público no `winget-pkgs`: ação do usuário |
| Qt | `windeployqt` mais um dos instaladores acima | Redistributable do VC++ no instalador |

Regra: se o usuário já tem um instalador funcionando, não proponha trocar.

## 5. Updater por stack (V-18, V-20, V-49, V-40)

| Stack | Mecanismo | Pegadinha |
| --- | --- | --- |
| Electron | `autoUpdater` (Squirrel) com servidor próprio ou Hazel, Nuts, electron-release-server, Nucleus; `update.electronjs.org` | Serviço gratuito só para repositório público com GitHub Releases |
| Tauri v2 | Plugin updater, assinatura obrigatória, manifesto estático ou dinâmico | Chave perdida impede atualizar instalações existentes (Inferido); ordem com Authenticode é hipótese |
| macOS nativo (e Electron no macOS) | Sparkle com EdDSA e appcast | Gera segredo no chaveiro; confira a versão (2.9 para feed assinado) |
| MSIX | App Installer (`.appinstaller`) | Sem fonte sobre `update-settings` |
| Qt | Sem fonte | Declarar lacuna |

## 6. TUI (V-30 a V-32)

| Contexto | Escolha | Motivo | Rótulo |
| --- | --- | --- | --- |
| Python, teste headless desejado | Textual | `run_test`, `Pilot`, `snap_compare` | Verificado |
| Rust, binário único | Ratatui | Teste de eventos precisa de PTY | Verificado |
| Go, modelo Elm | Bubble Tea | `teatest` experimental | Verificado |
| Precisa de acessibilidade comprovada | Oferecer também CLI não interativa | Sem fonte de acessibilidade nas três | Suposição |

## 7. PowerShell ou bash

| Contexto | Escolha | Motivo |
| --- | --- | --- |
| Automação de build e instalação no Windows, máquina do usuário em 5.1 | PowerShell 5.1 | Já instalado; `ShouldProcess`, objetos |
| Precisa de `??`, `-Parallel` ou multiplataforma | PowerShell 7 com `#requires -Version 7` | V-60 |
| Script de CI Linux ou Git Bash | bash | Declarar no shebang; ShellCheck |
| Portabilidade máxima | POSIX sh | Sem `[[`, arrays, `local` (V-63) |
| Lógica complexa (mais de 100 linhas) | Linguagem estruturada (Python, Go) | Guia do Google (V-62) |

## 8. CLI ou MCP (C-6; V-11, V-12)

Para o ciclo local de desenvolvimento com agente, uma CLI simples com `--json`, exit codes e log em arquivo costuma bastar (V-12, B; sugestões de timeout e caminho de log são da fábrica). MCP serve onde a alternativa é pouco confiável ou o host exige OAuth e elicitation (V-55). MCP roda fora do sandbox e plugins podem trazer servidores (V-51, V-02). Este plugin não ativa MCP; para construir um servidor, veja `/automation-integrations:playbook` e `llm-ai-agents`.

## 9. Onde colocar uma regra do agente (V-06, V-08, V-51)

| Precisa valer sempre? | Escopo | Onde |
| --- | --- | --- |
| Sim, bloquear | Qualquer comando | Hook `PreToolUse` com `exit 2`, mais permissão `deny`; fronteira real é sandbox |
| Sim, fato universal curto | Projeto | `CLAUDE.md` (abaixo de 200 linhas) |
| Só em certos arquivos | Caminhos | `.claude/rules/*.md` com `paths` |
| Procedimento de várias etapas | Tarefa | Skill |
| Revisão independente | Contexto limpo | Subagente com `Read, Grep, Glob` |
| Outro agente (Cursor, Codex) também lê | Portabilidade | `AGENTS.md`; `CLAUDE.md` o importa |

## 10. Exemplo de ADR curto

```markdown
# ADR 001: Stack do app de monitoramento

Estado: proposta · Data: 2026-10-10

Contexto: Windows e macOS; equipe de React; Store com MSIX e auto-update obrigatórios.
Restrições duras: MSIX (V-40); Tauri gera só MSI e NSIS (V-46).
Opções: Electron | Tauri | WinUI 3 + MAUI (descartadas: equipe sem C#, V-37).
Decisão: Electron, a confirmar em protótipo (assinar, instalar, atualizar e desinstalar em máquina limpa).
Consequências: pegada maior (sem número); seguir o checklist de 20 itens e os fuses (V-16, V-48).
Não verificável: Linux; comportamento do WebView; custo de certificado na região (V-44).
Reconsiderar se: a Store passar a aceitar o pacote do Tauri de forma verificada.
```
