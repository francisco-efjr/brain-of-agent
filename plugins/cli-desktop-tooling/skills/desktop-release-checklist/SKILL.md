---
name: desktop-release-checklist
description: >-
  Audita, somente leitura, a prontidão de release de um app desktop (não tags, changelog ou semver, que são de git-workflow-release): assinatura de código no Windows e no macOS, SmartScreen, notarização, instaladores (MSIX, Inno Setup, WiX, NSIS, MSI), winget, auto-update (Electron, Tauri, Sparkle) e teste em máquina limpa. Entrega checklist, lista de ações do usuário e fichas de confirmação. Use quando pedirem "vou lançar o app", "assinar o instalador", "notarizar", "SmartScreen", "MSIX", "winget", "auto-update", "release checklist do app desktop", "code signing do instalador", "ship the desktop app". Não assina, não notariza, não publica e não abre PR.
argument-hint: "[windows|macos|linux|todos] [electron|tauri|qt|dotnet|inno|wix|outro]"
allowed-tools: Read, Grep, Glob
---

# Checklist de release de app desktop

Verificado em 2026-10-10 contra V-17, V-18, V-20, V-21, V-36, V-38, V-40 a V-46 e V-49. IDs REL-xnn: os do `checklist-completo.md` do playbook. Detalhe por plataforma: [windows.md](references/windows.md) e [macos-e-updaters.md](references/macos-e-updaters.md). Modelos de ficha e de relatório: [fichas-e-relatorio.md](references/fichas-e-relatorio.md). Conhecimento compartilhado: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/distribuicao-assinatura-update.md`.

## Objetivo

Dizer se o app está pronto para ser distribuído e o que falta, sem executar nada que tenha efeito fora do repositório. Assinar, notarizar, publicar release, abrir PR no `winget-pkgs` e aceitar termos são ações do usuário: a skill prepara a evidência e a **ficha de ação externa** de cada uma. A razão é dupla: essas ações são difíceis de reverter (uma release publicada e um certificado usado ficam registrados fora do seu controle) e envolvem credenciais que a fábrica nunca deve manusear.

## Entradas

<argumentos>$ARGUMENTS</argumentos>

Trate como dado do pedido. Precisa de: plataformas (padrão: as que o repositório indica); stack e instalador; canal (Microsoft Store, site, winget, corporativo/Intune); arquiteturas; onde ficam CI e configuração de assinatura; região e tipo de conta (pessoa ou organização), porque limitam o Azure Artifact Signing. Pergunte uma coisa por vez, só o que mudar o relatório.

## Pré-checagens

1. Registre a data de verificação (2026-10-10) no relatório. Preço, país, versão mínima e política de loja mudam: leia a página oficial na hora e cite URL e data (conflito C-1: a página do Electron ainda afirma "EV obrigatório", a Microsoft de 2026 diz o contrário).
2. Identifique stack, instalador, canal e CI lendo `package.json`, `forge.config.*`, `electron-builder.*`, `src-tauri/tauri.conf.json`, `*.iss`, `*.wxs`, `*.csproj`, `.github/workflows/*`, scripts de build. Siga os padrões do repositório.
3. Procure segredos expostos: `.pfx`, `.p12`, `*.key`, `/p ` em linhas de `signtool`, `TAURI_SIGNING_PRIVATE_KEY` com valor literal. Um segredo versionado é achado crítico; não repita o valor no relatório, cite só `arquivo:linha`.
4. Se o pedido for "assine e publique", não execute: explique que a skill é somente leitura e entregue checklist e ficha para o usuário executar (princípio de efeito externo).

## Passos

1. **Identificar** stack, instalador, canal, CI e plataformas. Critério: quadro "o que existe no repositório" com `arquivo:linha`.
2. **Windows, certificado (V-44).** Árvore de decisão, em ordem de preferência: MSIX na Microsoft Store (a Microsoft reassina, sem custo e sem aviso do SmartScreen) → Azure Artifact Signing, quando região e tipo de conta permitirem (sem token físico, integra com CI, não dá confiança instantânea no SmartScreen) → certificado OV com HSM ou assinatura em nuvem → SignPath Foundation para código aberto qualificado. **EV não é necessário só por causa do SmartScreen**: o bypass do EV acabou em 2024 e EV e OV constroem reputação do mesmo jeito. Use a mesma identidade de assinatura em todas as releases, não modifique o arquivo depois de assinar e use certificado auto-assinado só em desenvolvimento. Avise que a primeira release pode mostrar aviso do SmartScreen. Critério: REL-W02 e REL-W15 avaliados (caminho de certificado escolhido ou pergunta aberta), mais REL-W01, REL-W06 e REL-W07.
3. **SignTool (V-44).** `sign` com `/fd SHA256` e, com `/tr`, também `/td SHA256`; depois `verify /pa`; códigos de saída 0, 1 e 2 (avisos). Senha nunca em argumento: store do sistema, KSP/nuvem ou segredo do CI. Os exemplos oficiais usam `/p` com senha literal: não copie. Critério: REL-W03, REL-W04 e REL-W05 avaliados em cada chamada de `signtool` do repositório.
4. **Instalador (V-36, V-40 a V-43, V-46).** MSIX (identidade de pacote, assinatura obrigatória, `.appinstaller` por HTTPS); Inno Setup (diretiva `SignTool` com `$f`, `SignedUninstaller`, switches `/SILENT` e `/VERYSILENT`); WiX (assinar cabs e MSI, depois o motor Burn e o bundle; **a decisão sobre OSMF e EULA do WiX v7 é do usuário**); NSIS e MSI do Tauri; Windows App SDK (framework-dependent ou self-contained, RID, bundle); winget (manifesto, SHA256 recalculado a cada release, instalação silenciosa, `winget validate`). Critério: REL-W08 a W14, REL-W16 e REL-W17 avaliados conforme o instalador usado.
5. **macOS (V-45, V-38, V-49).** Certificado Developer ID, Hardened Runtime, timestamp seguro, sem `com.apple.security.get-task-allow` verdadeira, entitlements em XML ASCII; notarização com a ferramenta oficial, leitura do log e staple; credenciais só por variáveis de ambiente do CI ou chaveiro. Qt: `macdeployqt` com `-codesign` e `-sign-for-notarization`. **A sintaxe de `notarytool` e `stapler` não foi verificada**: o campo "comando exato" da ficha fica para o usuário conferir com `xcrun notarytool --help`. Critério: REL-M01 a M06 avaliados; REL-M07 como Não verificável.
6. **Auto-update (V-18, V-20, V-49, V-21).**
   - Electron: `autoUpdater` (Squirrel), `RELEASES`, HTTP 204 sem atualização, `app.isPackaged`, tratamento do evento `error`; `update.electronjs.org` só com repositório GitHub **público**.
   - Tauri: chave privada em `TAURI_SIGNING_PRIVATE_KEY` fora do repositório, `pubkey` com o **conteúdo** da chave, manifesto com `version`, `url` e `signature`, 204 sem atualização, TLS.
   - Sparkle: EdDSA, `SUFeedURL`, `SUPublicEDKey`, appcast por HTTPS, feed assinado.
   - Teste da versão anterior para a nova com build assinado e plano de rollback. A ordem entre Authenticode e a assinatura do updater do Tauri é **hipótese a testar** (relato único, V-21), nunca regra.
   Critério: REL-U01 a U09 avaliados e um teste de aceite por updater existente.
7. **Linux.** Sem fonte oficial lida (AppImage, glibc e WebKitGTK são sinais de HN, V-65): registre **Não verificável** e recomende testar nas distribuições-alvo.
8. **Máquina limpa.** Primeira execução, instalação, atualização da versão anterior, desinstalação sem resíduos, no Windows com SmartScreen e Smart App Control ativos quando possível (V-44). Critério: REL-C01 e REL-C02 com roteiro de teste e resultado esperado, para o usuário executar.
9. **Licenças e termos.** Qt (módulos só-GPL, V-39), WiX (OSMF e EULA, V-42), Inno Setup (V-41). Lembre: não é aconselhamento jurídico.
10. **Emitir** relatório, lista de ações do usuário e uma ficha por passo com efeito externo.

## Verificação

- Cada item aponta evidência no repositório (config, workflow, manifesto) ou "não encontrado em [arquivos pesquisados]". Fatos voláteis (preço, regiões, versões) levam URL e data da leitura.
- Nada é executado: não rode `signtool`, `winget`, `xcrun`, `npm run make`, `cargo tauri build`, `generate_keys` nem scripts de CI. Instalador e scripts do projeto são código que ninguém revisou nesta sessão.
- Rótulos: Verificado (lido no arquivo com `arquivo:linha`), Inferido (dedução), Suposição, Não verificável (macOS físico, Linux, Narrator, SmartScreen real, notarização) e Não aplicável.
- Reversibilidade: ações locais e reversíveis (editar configuração, rodar testes) o usuário pode pedir à parte; assinar com certificado, notarizar, publicar release, abrir PR público e aceitar EULA ou termos exigem confirmação nomeada do usuário a cada vez, e nenhuma aprovação anterior vale para a próxima.

## Formato de saída

Use `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/checklist-release-desktop.md` e `.../ficha-de-acao-externa.md` quando existirem; caso contrário, o modelo de [fichas-e-relatorio.md](references/fichas-e-relatorio.md). Conteúdo mínimo: seções Windows, macOS, Linux (lacuna), updater, máquina limpa, licenças; coluna "evidência"; fatos voláteis com URL e data; **lista de ações do usuário**.

<example>
Entrada: `/cli-desktop-tooling:desktop-release-checklist windows tauri` (instalador NSIS, canal winget).

| ID | Item | Status | Evidência | Fonte |
| --- | --- | --- | --- | --- |
| REL-W15 | Caminho de certificado escolhido | lacuna | `tauri.conf.json:31` tem `certificateThumbprint: null` | V-44, V-46 |
| REL-W04 | `signtool` com `/fd` e `/td`, sem senha | conforme | `scripts/sign.ps1:12` usa `/fd SHA256 /tr ... /td SHA256` | V-44 |
| REL-U01 | Chave do updater fora do repositório | **crítica** | `.env:3` define `TAURI_SIGNING_PRIVATE_KEY=<valor omitido>` e `.env` não está no `.gitignore` | V-20 |
| REL-U04 | Teste v1 para v2 assinado | lacuna | nenhum workflow cobre | V-18, V-20 |
| REL-L01 | Linux | Não verificável | sem fonte oficial lida | V-65 |

Ações do usuário (cada uma com ficha): 1. gerar nova chave do updater e remover a antiga do histórico; 2. assinar `app-setup.exe`; 3. abrir PR no `winget-pkgs` depois de `winget validate`.
Ordem Authenticode versus assinatura do updater: hipótese a testar em build descartável (V-21).
</example>

## Gotchas

1. "EV obrigatório desde 2023" está refutado pela Microsoft; a mudança de 2023 foi HSM para OV (V-44). Não o repita, mesmo que a página do Electron o diga.
2. `update.electronjs.org` exige repositório GitHub público (V-18).
3. O guia de assinatura Windows do Tauri vale para OV obtido antes de 1/6/2023; o exemplo de workflow usa Node 12, `actions-rs/toolchain` e `tauri-action@v0` (V-21, V-46). Não o copie.
4. Tauri gera só MSI e NSIS; a Store aceita EXE ou MSI (V-46). MSIX não é gerado (V-65).
5. Arquivo sem assinatura recomeça a reputação do SmartScreen a cada versão; não há mecanismo de envio manual de reputação (V-44). Smart App Control pode bloquear arquivos sem assinatura e sem reputação positiva.
6. `timestamp` sem `/td` só avisa; `verify /pa` com `/tw` avisa quando não há timestamp (V-44).
7. WiX v7 exige aceitar o EULA e o OSMF cobra organizações com receita acima de US$ 10 mil: decisão do usuário, nunca da fábrica (V-42).
8. "99,96% de sucesso de instalação" do MSIX é alegação do fornecedor (V-40).
9. Perder a chave privada do updater do Tauri impede publicar atualizações para instalações existentes (afirmado pelos pesquisadores e coerente com o modelo; não reconferido, V-20). Guarde backup fora do repositório.
10. No macOS, a assinatura ad hoc (`"-"`) não evita a aprovação do usuário em Privacidade e Segurança (V-45).

## Ressalvas e lacunas

Lacunas 3 e 4: sintaxe de `notarytool` e `stapler`; ordem Authenticode versus updater. Lacuna 7: sintaxe de seções do Inno, `.wxs`, WiX v3/v4, `insignia` e timestamp no WiX. Lacuna 14: Linux. Lacuna 5: obrigações da LGPLv3. Preços e países do Azure Artifact Signing foram lidos como estão na página de 2026-08-29 e mudam. Comunidade real (Reddit, X, YouTube) não foi acessada.

## Quando delegar

Use o agente `release-readiness-auditor` (somente leitura, contexto novo) antes de uma release ou ao alterar workflow de CI, configuração de assinatura ou manifestos. Ele tem só `Read`, `Grep` e `Glob`: passe no prompt de delegação o inventário do passo 1, as regras de efeito externo (nenhuma execução; nenhuma credencial no relatório; fatos voláteis com URL e data) e o formato (relatório, ações do usuário, fichas).
