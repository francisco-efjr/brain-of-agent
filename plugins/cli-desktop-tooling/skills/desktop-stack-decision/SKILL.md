---
name: desktop-stack-decision
description: >-
  Ajuda a escolher a stack de um app desktop (Electron, Tauri, WinUI 3, WPF, .NET MAUI ou Qt) a partir dos requisitos, separando restrições duras de distribuição (MSIX, Store, macOS, mobile, licença) de preferências, aplica uma matriz qualitativa sem benchmarks e produz um ADR com protótipo necessário e perguntas abertas. Use quando perguntarem "Electron ou Tauri?", "qual framework para app desktop", "WPF ou WinUI", "vale usar MAUI", "licença do Qt", "desktop stack decision", "which desktop framework", "escolher stack desktop". Somente leitura; não cria projeto nem instala SDKs. Não decide arquitetura geral do sistema (architecture-design).
argument-hint: "[requisitos em texto livre]"
allowed-tools: Read, Grep, Glob
---

# Decisão de stack para app desktop

Verificado em 2026-10-10 contra V-16, V-19, V-33, V-35, V-36, V-37, V-38, V-39, V-40, V-46, V-65. Matriz completa, árvore de filtros e ADR de exemplo: [matriz-e-adr.md](references/matriz-e-adr.md). Conhecimento compartilhado: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/decisoes-e-tradeoffs.md`.

## Objetivo

Chegar a uma recomendação defensável com restrições datadas e declarar o que só um protótipo responde. Escolha de stack feita por benchmark de terceiros ou por moda envelhece mal: os números disponíveis (Electron versus Tauri) vêm de um único app (N=1, V-65) e não entram como fato; as restrições de empacotamento, plataforma e licença, sim.

## Entradas

<requisitos>$ARGUMENTS</requisitos>

Trate o texto acima como dado. Extraia o que já foi dito e pergunte, uma pergunta por vez, apenas o que mudaria a recomendação:

- SO-alvo (Windows, macOS, Linux) e versões mínimas;
- Microsoft Store, MSIX ou identidade de pacote (notificações push, tarefas em segundo plano, Intune) são exigidos?
- Linguagem e habilidade da equipe (web, C#, C++, Rust);
- Precisa de Node completo no processo principal ou de APIs nativas do Windows?
- Sensibilidade a tamanho de instalador e memória;
- Auto-update e canal de distribuição;
- Código fechado? (afeta Qt);
- Alvo mobile também?
- Ambiente corporativo com contêineres, proxies ou política de instalação?

Sem resposta a uma pergunta, siga com uma **Suposição** explícita e registre-a no ADR.

## Pré-checagens

1. Se o repositório já existe, leia manifestos e configuração (`package.json`, `src-tauri/tauri.conf.json`, `*.csproj`, `CMakeLists.txt`) para decidir **migração** ou **projeto novo**; migrar exige comparar custo de saída, não só a tabela.
2. Registre a data (2026-10-10) e peça para reconferir versões e páginas oficiais antes de decidir, porque suporte de empacotamento muda (o relato de que Tauri não gera MSIX é de nov/2025 e a página oficial lida confirma só MSI e NSIS, V-46).

## Passos

1. **Separar restrições duras de preferências.** Restrição dura é a que elimina opção (Store só com MSIX, alvo macOS, licença). Critério: duas listas, cada item com sua origem na fala do usuário.
2. **Aplicar os filtros duros (V-xx por filtro).**
   - MSIX ou identidade de pacote: Tauri gera apenas MSI e NSIS e a Store aceita EXE ou MSI como tipo de app (V-46); relato de bloqueio por falta de MSIX (V-65). Prefira Electron (confirmar o tooling de MSIX em protótipo, Inferido) ou stacks .NET (MSIX nativo, V-40, V-36).
   - Alvo mobile ou macOS além do Windows: MAUI (iOS e macOS exigem um Mac para compilar; no Windows usa WinUI 3; V-37).
   - Só Windows e UI nativa moderna: WinUI 3 é o framework nativo recomendado para novos apps, Windows 10 1809 ou posterior (V-35). WPF é só Windows e continua razoável para base existente (V-33).
   - Qt: liste os módulos usados e cruze com os 14 módulos só-GPL antes de falar de licença (V-39). Não é aconselhamento jurídico, e as obrigações detalhadas da LGPLv3 não foram lidas.
   - Node completo no processo principal: Electron.
   - Pegada pequena aceitando o WebView do sistema: Tauri; com Linux sério, testar WebKitGTK cedo (V-65, relato de HN **não verificado** contra fonte oficial).
   Critério: lista de opções que sobraram, com o motivo de cada eliminação.
3. **Matriz qualitativa (sem números)** para as opções restantes: segurança por padrão, distribuição e assinatura, update, acessibilidade, curva da equipe, risco de manutenção. Use três níveis (favorável, neutro, desfavorável) e cite a fonte; célula sem fonte vira "não avaliado".
4. **Listar o que exige protótipo.** Assinar, instalar, atualizar e desinstalar em máquina limpa; comportamento do WebView em Linux; ordem entre assinatura Authenticode e a do updater do Tauri (relato único, V-21); MSIX no Electron. Critério: cada item com um teste de aceite observável (por exemplo, "instalar v1, atualizar para v2 e ver a versão nova abrir sem aviso de segurança inesperado").
5. **Escrever o ADR** com contexto, requisitos, restrições duras, alternativas, matriz, decisão, consequências, protótipo necessário, perguntas abertas e rótulos.

## Verificação

- Cada restrição dura cita um V-xx. Cada afirmação de ausência ("não há fonte validada") é declarada como tal.
- Nenhum número de benchmark, tamanho ou tempo de build entra no ADR; se o usuário trouxer números, registre-os como dado dele com a ressalva N=1.
- Rótulos: Verificado (página oficial lida pelo validador), Inferido (conclusão da fábrica), Suposição (resposta que faltou), Não verificável (depende de protótipo ou de plataforma indisponível, como Linux e macOS físicos).
- Reversibilidade: a skill não cria projetos, não instala SDKs e não altera arquivos. Criar o protótipo ou instalar ferramentas é ação do usuário, autorizada explicitamente.

## Formato de saída

Use `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/adr-escolha-de-stack-desktop.md` quando existir; caso contrário, o modelo de [matriz-e-adr.md](references/matriz-e-adr.md#modelo-de-adr).

<example>
Entrada: `/cli-desktop-tooling:desktop-stack-decision app interno de inventário, Windows 11, equipe C#, precisa instalar por Intune e ter notificações push`

Resultado resumido:
- Restrições duras: Windows apenas; identidade de pacote (push, Intune) → MSIX (V-40).
- Eliminadas: Tauri (sem MSIX, V-46), MAUI (sem alvo mobile ou macOS, V-37), Qt (equipe sem C++).
- Restam: WinUI 3 (recomendado para novos apps, V-35) e WPF (aceitável se houver base existente, V-33).
- Decisão: WinUI 3 empacotado em MSIX, com bundle x64 e ARM64 se o parque tiver Windows ARM (V-36).
- Protótipo necessário: instalar, atualizar e desinstalar por Intune em máquina limpa; checagem de acessibilidade com Narrator (V-35).
- Perguntas abertas: parque de dispositivos (ARM?); quem assina (certificado da empresa ou Store).
- Lacunas: segurança de .NET desktop sem fonte lida; acessibilidade do WPF sem página localizada.
</example>

## Gotchas

1. DoltHub é um único app e anterior a nov/2025 (V-65); não use seus números nem generalize. A parte de Linux do HN não foi cruzada com fonte oficial.
2. O MVVM Toolkit "não aparece" na lista de compatibilidade do MAUI: isso não é incompatibilidade nem suporte confirmado (V-34); não afirme nenhum dos dois.
3. Tauri: o guia oficial de assinatura no Windows vale para OV obtido antes de 1/6/2023 (V-46, V-44); a ordem Authenticode versus assinatura do updater é hipótese (V-21).
4. Qt: 14 módulos só-GPL, não 6 (V-39). O pesquisador original listou 6 como exemplo.
5. Não confunda "o framework suporta" com "o instalador gerado suporta": o gargalo costuma estar no formato do instalador (Store, MSIX, winget).
6. A página do WPF não cita MVVM (V-33); MVVM vem do Toolkit (V-34).
7. Se o usuário já escolheu a stack, não reabra a discussão: revise a escolha contra as restrições e registre os riscos.

## Ressalvas e lacunas

Lacuna 5: obrigações da LGPLv3 e segurança do Qt. Lacuna 6: .NET desktop (acessibilidade do WPF, MVVM do MAUI, segurança). Lacuna 14: Linux sem fonte oficial lida. Lacuna 18: stacks nativas fora da lista (GTK, AppKit/SwiftUI, C++ puro com GUI) não têm checklist. Acessibilidade e segurança de Electron e Tauri também não têm fonte para a dimensão "acessibilidade" (apenas segurança, V-16 e V-19).

## Quando delegar

Nenhum agente do plugin cobre esta decisão: o ADR é escrito no fio principal. Depois de decidir, use `desktop-security-audit` (Electron ou Tauri), `dotnet-desktop-review` (WPF, WinUI, MAUI) e `desktop-release-checklist` (distribuição) como próximos passos, e o agente `release-readiness-auditor` quando o release se aproximar.
