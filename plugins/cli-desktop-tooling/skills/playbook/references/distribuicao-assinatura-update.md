# Distribuição, assinatura de código e auto-update

Sumário: 1. Regras e gate · 2. Windows: certificado · 3. SignTool e SmartScreen · 4. Instaladores · 5. winget · 6. macOS · 7. Updaters · 8. Linux e Store · 9. Máquina limpa · 10. Licenças · 11. Roteiro do relatório · 12. Exemplos

Fontes: V-44 (Microsoft, A 9), V-40, V-41, V-42, V-43, V-36, V-45, V-46, V-17, V-18, V-20, V-21, V-49, V-38. Preço, região, versão mínima e prazo são fatos voláteis: leia da página na hora e cite com URL e data (ver `fontes.md`, seção 2). Esta referência alimenta uma auditoria por leitura: o plugin não assina, não notariza, não instala, não publica e não abre PR. Cada passo com efeito externo vira uma ficha (`assets/templates/ficha-de-acao-externa.md`) que o usuário confirma e executa.

## 1. Regras e gate

1. Segredo de assinatura (`.pfx`, chave privada, senha, chave de API) fica fora do repositório e fora de argumento de linha de comando; vai por store do sistema, KSP ou nuvem, ou segredo do cofre do CI.
2. Mesma identidade de assinatura em toda release; não modificar o arquivo depois de assinado.
3. Atualização é testada da versão anterior assinada para a nova, em máquina limpa; desinstalação também.
4. Assinar com certificado, notarizar, publicar release, abrir PR no `winget-pkgs`, aceitar EULA ou termos de conta, criar certificado e gerar chaves do Sparkle são ações do usuário. Reversibilidade: nenhuma delas é desfeita editando um arquivo local.
5. A fábrica nunca aceita EULA ou termos em nome do usuário (WiX v7, contas Apple e Microsoft).

## 2. Windows: escolha do certificado (V-44, Microsoft 2026)

Árvore de decisão, em ordem de preferência:

1. **MSIX na Store:** a Microsoft reassina, sem custo e sem aviso do SmartScreen. MSI ou EXE na Store: o publicador assina com certificado de uma CA do Programa de Raiz Confiável.
2. **Azure Artifact Signing** (antigo Trusted Signing), quando região e tipo de conta permitirem: sem token físico, integra com CI, cerca de US$ 9,99 por mês na página consultada; organizações nos EUA, Canadá, UE e Reino Unido; indivíduos só nos EUA e Canadá; **não dá confiança instantânea no SmartScreen**. Confirme na página antes de citar.
3. **OV com chave em HSM ou assinatura em nuvem:** a faixa citada é US$ 150 a 300 por ano; desde junho de 2023 o CA/Browser Forum exige chave privada em HSM ou token.
4. **SignPath Foundation:** assinatura gratuita para projetos de código aberto qualificados.
5. Auto-assinado: só desenvolvimento, ou empresa que distribui a confiança por política.

**EV não é necessário só por causa do SmartScreen.** O bypass do SmartScreen pelo EV foi removido em 2024 e EV e OV constroem reputação do mesmo jeito; pagar a mais por EV para evitar aviso "não se justifica mais" (V-44). A página do Electron (V-17) e relatos antigos dizem o contrário: prevalece a Microsoft (C-1 em `fontes.md`). O guia de assinatura do Tauri só vale para OV obtido antes de 1/6/2023 (V-46).

## 3. SignTool e SmartScreen (V-44)

- `signtool sign` exige `/fd` (SHA256 recomendado) e, com `/tr`, também `/td SHA256`. `signtool timestamp` sem `/td` só avisa. `signtool verify /pa` usa a política de autenticação padrão; `/tw` avisa quando falta timestamp. Códigos de saída: 0, 1 e 2 (avisos).
- Os exemplos oficiais usam `/p` com senha literal: não copie. Selecione o certificado do store (por exemplo `/sha1 <thumbprint>`, conhecimento estável, Inferido; confira `signtool sign /?`) ou use KSP/assinatura em nuvem. Em CI, importe o `.pfx` de um segredo do cofre.
- Sequência de referência (não executada; confirme as flags na versão instalada):

```powershell
signtool sign /fd SHA256 /tr <URL-DO-CARIMBO-DE-TEMPO> /td SHA256 /sha1 <THUMBPRINT> app.exe
signtool verify /pa /v app.exe
```

- Reputação do SmartScreen tem dois sinais: certificado do editor e hash do arquivo. Arquivo sem assinatura recomeça do zero a cada versão. Não existe envio manual de reputação para o consumidor. A primeira release assinada pode ainda mostrar aviso: avise o usuário. Smart App Control (Windows 11) pode bloquear arquivo sem assinatura e sem reputação positiva. Não assine programa potencialmente indesejado.

## 4. Instaladores Windows

| Opção | Pontos de auditoria | Fonte |
| --- | --- | --- |
| **MSIX / App Installer** | Identidade de pacote (publisher, nome, versão) exigida por notificações push, tarefas em segundo plano, distribuição na Store e Intune; atualização diferencial por blocos de 64 KB; desinstalação sem resíduos; pacote precisa estar assinado antes da instalação; `.appinstaller` servido por HTTPS; testar a atualização da versão anterior. A taxa "99,96% de sucesso" é alegação do vendedor, não use | V-40 |
| **Inno Setup** | Diretiva `SignTool` com marcador `$f` obrigatório; `SignedUninstaller`; várias entradas `SignTool` rodam em ordem (assinatura dupla); comando vindo de variável de ambiente ou store, sem senha literal; modo por usuário ou administrador; chaves silenciosas `/SILENT` e `/VERYSILENT`. Licença própria permissiva (manter avisos de copyright); a ajuda pede licença comercial a usuários comerciais (pedido, não condição). Sintaxe das seções não foi lida | V-41 |
| **WiX** | MSI: assinar o `.msi` ou os cabs externos e gravar as assinaturas (`wix msi inscribe`); bundles: assinar o motor Burn (`wix burn detach`, assinar, `wix burn reattach`) e depois o `.exe`; MSBuild `SignOutput=true`. **OSMF:** organizações com receita acima de US$ 10 mil patrocinam a organização do WiX (desde a v6). **WiX v7:** usar exige aceitar o EULA (`AcceptEula`, `-acceptEula` ou `wix eula accept wix7`): decisão do usuário, nunca da fábrica. `insignia`, timestamp, v3 e v4 não verificados | V-42 |
| **NSIS e MSI do Tauri** | Tauri só gera MSI (via WiX v3, segundo a página) e NSIS (`-setup.exe`); a página de instaladores não menciona MSIX. Para a Store: EXE ou MSI offline, assinado, silencioso (`/S` no NSIS, `/quiet` no MSI), com WebView2 em modo offline | V-46 |
| **Windows App SDK** | Framework-dependent contra self-contained; RID por arquitetura ou bundle MSIX; inicialização: empacotado framework-dependent usa a Deployment API, não empacotado usa a bootstrapper API, self-contained empacotado não precisa | V-36 |

Árvore curta para escolher (Inferido a partir de V-36, V-40 a V-43, V-46): (1) Store ou site? Store: MSIX ou EXE/MSI assinado. (2) Precisa de identidade de pacote? MSIX. (3) Runtime compartilhado ou embutido? (4) Quais arquiteturas? (5) Um build por RID ou um bundle? Se o usuário já tem Inno ou WiX funcionando, mantenha; migrar não é pedido.

## 5. winget (V-43)

- Manifesto: `ManifestVersion` 1.12.0 na página consultada; singleton (um instalador, uma localidade) ou múltiplo (mínimo 3 arquivos: version, defaultLocale, installer). Campos mínimos: `PackageIdentifier` (Publisher.Package), `PackageVersion`, `PackageLocale`, `Publisher`, `PackageName`, `License`, `ShortDescription`, `Installers` (`Architecture`, `InstallerType`, `InstallerUrl`, `InstallerSha256`), `ManifestType`, `ManifestVersion`.
- Checklist: URL direta do publicador, sem redirecionador e em HTTPS; SHA256 recalculado a cada release; instalação silenciosa testada (MSI `/q`, Inno `/SILENT` ou `/VERYSILENT`, Nullsoft `/S`); instalar e desinstalar como administrador e não administrador; `winget validate`; teste no Windows Sandbox com `Tools\SandboxTest.ps1`.
- Ferramentas: `wingetcreate` e `YAMLCreate.ps1` (as duas oferecem enviar o PR sozinhas: **não deixar**). O PR ao `microsoft/winget-pkgs` é público e irreversível na prática: ficha de ação externa e autorização explícita. Pasta `manifests/<letra>/<publisher>/<app>/<versão>`; um manifesto por submissão; a Microsoft pode recusar qualquer submissão; `Needs-Author-Feedback` fecha o PR após 10 dias sem resposta. Rótulos de erro: `Error-Hash-Mismatch`, `Validation-Indirect-URL`, `Validation-HTTP-Error`, `Validation-Domain`, `Validation-Unattended-Failed`, `Validation-Uninstall-Error`, `URL-Validation-Error`, `Binary-Validation-Error`.

## 6. macOS (V-45, V-38, V-49; classe B)

- Notarização é verificação automatizada (não é App Review) que gera um ticket para grampear (staple). Requisitos: assinatura válida em todos os executáveis; certificado **Developer ID** (não Mac Distribution, ad hoc, Apple Developer nem local); Hardened Runtime em apps e alvos de linha de comando; timestamp seguro; sem a entitlement `com.apple.security.get-task-allow` verdadeira; entitlements em XML ASCII; plugins herdam as entitlements do host. A Apple recomenda revisar o log do serviço.
- **Sintaxe de `notarytool` e `stapler` não foi verificada** (a página da Apple só nomeia as ferramentas, incluídas no Xcode): confira `xcrun notarytool --help` e `xcrun stapler --help` na versão instalada e não escreva o comando de memória. Submeter é ação do usuário.
- Tauri: certificado "Developer ID Application" (só o Account Holder o cria); duas vias por variáveis de ambiente: chave de API do App Store Connect (`APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH`) ou Apple ID (`APPLE_ID`, `APPLE_PASSWORD`, `APPLE_TEAM_ID`); em CI, `.p12` em base64 (`APPLE_CERTIFICATE`, `APPLE_CERTIFICATE_PASSWORD`). A assinatura ad hoc (`-`) não evita a aprovação do usuário em Privacidade e Segurança. A página do Tauri não trata de Hardened Runtime nem de entitlements.
- Qt: `macdeployqt` com identidade real (seção 6 de `desktop-stacks-e-seguranca.md`).
- Electron: sem assinatura ou com assinatura ad hoc, `safeStorage` volta a pedir permissão no Keychain após cada atualização; Squirrel.Mac exige app assinado (V-17).
- Universal binary e assinar duas vezes foram bloqueio relatado em V-65 (N=1).

## 7. Auto-update

| Stack | Fatos verificados | Teste obrigatório | Fonte |
| --- | --- | --- | --- |
| **Electron** | `autoUpdater` com Squirrel é o caminho oficialmente suportado; Squirrel.Windows serve `RELEASES` em `/RELEASES` mesmo sem atualização; Squirrel.Mac responde JSON com `url` ou 204 sem atualização; usar `app.isPackaged`; tratar o evento `error`. `update.electronjs.org` exige repositório GitHub **público** com builds em GitHub Releases (e builds assinados no macOS) | Caso "sem atualização" (RELEASES, 204); atualização da versão anterior assinada; rollback | V-18 |
| **Tauri v2** | Assinatura obrigatória e impossível de desligar; `pubkey` em `plugins.updater` recebe o **conteúdo** da chave; chave privada em `TAURI_SIGNING_PRIVATE_KEY` (caminho ou conteúdo) e `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` (opcional); arquivos `.env` não funcionam para isso; manifesto estático exige `version` e, por plataforma, `url` e `signature` (conteúdo do `.sig`); servidor dinâmico responde 204 sem atualização ou 200 com `url`, `version`, `signature`; TLS obrigatório em produção; no Windows `installMode` é `passive` (padrão), `basicUi` ou `quiet` (desencorajado) | Chave fora do repositório; manifesto validado antes de publicar; atualização da versão anterior para a nova | V-20 |
| **Sparkle (macOS)** | Appcast em XML na URL de `SUFeedURL`; chaves EdDSA por `generate_keys` (privada no chaveiro do login; pública em `SUPublicEDKey`); `generate_appcast` gera appcast e `.delta`; `SURequireSignedFeed` e `SUVerifyUpdateBeforeExtraction` (feed assinado validado a partir do Sparkle 2.9); HTTPS e notarização são recomendações; delta é ignorado se o checksum não bater | Atualização da versão anterior; feed assinado | V-49 |
| **MSIX** | `.appinstaller` descreve pacote e configuração de atualização; opções de `update-settings` não foram lidas | Instalar, atualizar e desinstalar | V-40 |

**Ordem Authenticode contra assinatura do updater do Tauri:** relato único (Fluxzy, V-21) diz que o Authenticode reescreve o binário e invalida a assinatura minisign do updater, então seria preciso assinar com Authenticode primeiro e gerar os `.sig` depois. As páginas oficiais (V-20, V-46) não tratam do tema. Trate como hipótese a testar com um build descartável; pergunte ao usuário; nunca apresente como regra.

Perder a chave privada do updater impede publicar atualizações para instalações existentes (Inferido pela lógica de assinatura, não reconferido): faça backup fora do repositório, com autorização do usuário.

## 8. Linux e Store

- Linux: sem fonte oficial lida. AppImage gerado em distribuição nova falha em outras por glibc e WebKitGTK é a principal dor de Tauri no Linux, segundo comentários do HN (V-65). Registre Não verificável e recomende testar nas distribuições-alvo.
- Microsoft Store: ver itens MSIX e Tauri acima; política e certificação da loja não foram lidas.

## 9. Teste em máquina limpa (VM, Windows Sandbox ou WSL2 quando fizer sentido)

Por passo, registre comando, versão do SO, saída ou captura e o aviso esperado do SmartScreen: (1) instalar sem privilégios extras; (2) primeira execução; (3) atualização da versão N-1 para N com build assinado; (4) caso "sem atualização"; (5) desinstalar sem resíduos; (6) reinstalar. Executar instalador de terceiros ou do projeto é ação do usuário em ambiente descartável; a fábrica prepara o roteiro (`assets/templates/checklist-release-desktop.md`).

## 10. Licenças

Qt: 14 módulos só-GPL (V-39). WiX: OSMF e EULA (V-42). Inno: licença própria permissiva (V-41). ShellCheck e outras ferramentas de build: GPL-3.0 não se embute (V-61). Nada aqui é aconselhamento jurídico.

## 11. Roteiro do relatório

Stack, instalador, canal (Store, site, winget, corporativo), arquiteturas, CI e arquivos de config de assinatura lidos; data da verificação; árvore de certificado com a decisão e as restrições; item a item: evidência `arquivo:linha` ou "não encontrado"; lista de ações do usuário; fichas de confirmação; Não verificável (macOS físico, Linux, Narrator, runtime do updater).

## 12. Exemplos

Pedido: "Comprei EV porque a Microsoft exige desde 2023; assino no CI com `signtool sign /f cert.pfx /p MinhaSenha123 /tr http://... app.exe`; app Tauri, distribuo pelo site."

| ID | Sev. (Inferido) | Evidência | Correção |
| --- | --- | --- | --- |
| REL-W01 | Alta | Premissa "EV obrigatório" | Refutada por V-44; EV não evita o aviso; reputação vem de identidade estável |
| REL-W03 | Crítica | Senha em `/p` no workflow | Segredo do CI ou store/KSP; sem senha em argumento |
| REL-W03 | Alta | Falta `/fd SHA256` e `/td SHA256` | Acrescentar; `signtool verify /pa` ao final |
| REL-U08 | Média | Tauri sem prova da ordem Authenticode e `.sig` | Teste em build descartável (hipótese de V-21) |
