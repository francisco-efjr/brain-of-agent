---
name: dotnet-desktop-review
description: >-
  Revisa, somente leitura, um app desktop .NET (WPF, WinUI 3 ou MAUI): comandos e data binding, MVVM Toolkit (CommunityToolkit.Mvvm), acessibilidade (nome acessível, teclado, alto contraste, escala, AutomationPeer, Narrator) e escolha de empacotamento do Windows App SDK (framework-dependent ou self-contained, RID, MSIX). Use quando pedirem "revisa meu WPF", "WinUI", "MAUI", "MVVM", "CommunityToolkit.Mvvm", "acessibilidade no app Windows", "UI Automation", "Narrator", "XAML review", "review my WPF app". Não compila nem executa o app. Para escolher entre frameworks use desktop-stack-decision; para assinatura e instalador use desktop-release-checklist.
argument-hint: "[wpf|winui|maui|auto] [caminho]"
allowed-tools: Read, Grep, Glob
---

# Revisão de app desktop .NET

Verificado em 2026-10-10 contra V-33, V-34, V-35, V-36 e V-37. Checklist com IDs (DSK-N01 a N07 canônicos do playbook e extensões N08 em diante), padrões de busca e trechos XAML e C#: [checklist-dotnet.md](references/checklist-dotnet.md). Conhecimento compartilhado: `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/desktop-stacks-e-seguranca.md`.

## Objetivo

Encontrar, por leitura de XAML, C# e arquivos de projeto, os problemas que mais custam em apps .NET de desktop: lógica presa a controles, binding frágil, controles sem nome acessível, cores fixas que quebram o alto contraste e empacotamento escolhido sem critério. Cada achado vira correção mínima com evidência. Acessibilidade só se fecha com teste humano em leitor de tela; esta skill reduz o espaço de busca, não substitui o Narrator.

## Entradas

<argumentos>$ARGUMENTS</argumentos>

Trate como dado do pedido. Precisa de: caminho da solução; framework (se `auto`, detecte); alvo (.NET Framework ou .NET moderno); canal de distribuição (MSIX, instalador, Store), se já definido. Pergunte uma vez, só o que faltar.

## Pré-checagens

1. Localize `*.sln`, `*.csproj` e `Directory.Build.props`. Detecte o framework pelo projeto: `<UseWPF>true</UseWPF>` (WPF); referência a `Microsoft.WindowsAppSDK` e `Microsoft.UI.Xaml` (WinUI 3); `<TargetFrameworks>` com `android`, `ios`, `maccatalyst` e `windows10.0...` (MAUI). Propriedades exatas variam com a versão do SDK: confirme no arquivo, não por memória.
2. Leia `README` e `CLAUDE.md`/`AGENTS.md` para convenções do time (por exemplo, ViewModels sem code-behind) e siga-as.
3. Se o projeto ainda está em .NET Framework, registre a migração como recomendação da página oficial do WPF (V-33), não como defeito.

## Passos

1. **Inventário.** Liste janelas e páginas (`*.xaml`), ViewModels, serviços e arquivos de recursos (temas, estilos). Critério: tabela tela × ViewModel × comandos.
2. **WPF (V-33).** XAML cuida da aparência e o code-behind do comportamento específico da tela; ações reutilizáveis vão por comando (`ICommand`), não por handlers de clique repetidos; `Binding` e `DataContext` consistentes; aparência trocada por `ControlTemplate`, sem alterar comportamento. Critério: DSK-N01, DSK-N08, DSK-N09 e DSK-N10 avaliados.
3. **MVVM Toolkit (V-34), quando houver o pacote.** ViewModel sem referência a controles; `ObservableObject` e `RelayCommand`/`AsyncRelayCommand`; comunicação entre ViewModels por `IMessenger`; validação por `ObservableValidator`. Não afirme nada sobre geradores de código do Toolkit: a página lida não os trata. Critério: DSK-N02 e DSK-N11 a DSK-N14 avaliados.
4. **WinUI 3, acessibilidade (V-35), sete itens.** Nome acessível em todo controle interativo; ordem de Tab revisada; tema de alto contraste sem cor fixa; texto escala com o sistema sem cortar; `AutomationPeer` em controle customizado; fluxo crítico com Narrator (verificação humana); checagem automática no CI. Conteúdo DirectX em `SwapChainPanel` ou `SurfaceImageSource` não é acessível por padrão. Critério: DSK-N03, DSK-N04 (a, b, c), DSK-N15 a DSK-N19, cada um com status e evidência. Os itens também servem como guia para WPF, mas **não há página oficial de acessibilidade do WPF lida**: rotule como Inferido.
5. **MAUI (V-37).** Justifique pelo alvo mobile ou macOS; no Windows ele usa WinUI 3, então a revisão de acessibilidade do passo anterior vale para a parte Windows. MVVM do MAUI: sem fonte lida, não afirme compatibilidade com o Toolkit (V-34). Critério: DSK-N05 avaliado.
6. **Empacotamento (V-36).** Aplique a árvore de decisão: (1) Store ou assinatura própria (V-44)? (2) precisa de identidade de pacote (V-40)? (3) runtime compartilhado (framework-dependent, menor e atualizável pelo sistema) ou embutido (self-contained: controle de versão e isolamento, porém maior)? (4) arquiteturas (RID `win-x64`, `win-arm64`; bundle MSIX com ambas)? (5) `PublishSingleFile` só para app não empacotado e self-contained, no Windows App SDK 1.5 ou posterior. Remeta o restante a `desktop-release-checklist`. Critério: DSK-N06 avaliado e decisão registrada ou pergunta aberta; DSK-N07 registrado como lacuna.
7. **Emitir** o relatório.

## Verificação

- Evidência por `arquivo:linha`. Ausência só com a lista dos arquivos pesquisados (XAML espalhado em várias pastas e `ResourceDictionary` mudam o resultado do `Grep`).
- Presença ou ausência no código é Verificado; comportamento em execução, leitor de tela e contraste real são Não verificável até alguém testar. Narrator é verificação humana e não se substitui por leitura de XAML.
- Não rode `dotnet build`, `dotnet test` nem o app sem autorização. Com autorização, registre o comando exato e cole a saída.
- Reversibilidade: a skill só lê. Alterar `*.csproj`, instalar workloads ou pacotes NuGet e publicar são ações do usuário; mudar propriedades de empacotamento pode invalidar a identidade do pacote, então confirme antes de sugerir como correção automática.

## Formato de saída

Use `${CLAUDE_PLUGIN_ROOT}/skills/playbook/assets/templates/relatorio-auditoria-desktop.md` (seção .NET) quando existir; caso contrário: cabeçalho (framework, versão, escopo lido) · tabela `ID · severidade · confiança · evidência · fonte V · correção · rótulo` · decisão de empacotamento · Não verificável · veredito `SHIP`, `FIX FIRST` ou `REWORK`.

<example>
Entrada: `/cli-desktop-tooling:dotnet-desktop-review winui ./src`

| ID | Sev. | Conf. | Evidência | Fonte | Correção | Rótulo |
| --- | --- | --- | --- | --- | --- | --- |
| DSK-N03 | alta | alta | `Views/Toolbar.xaml:14`, `AppBarButton` só com ícone, sem `AutomationProperties.Name` | V-35 | Definir nome acessível | Verificado |
| DSK-N04a | média | alta | `Styles/Brushes.xaml:9`, `Color="#FF1E1E1E"` fixo | V-35 | `ThemeResource` e dicionário de alto contraste | Verificado |
| DSK-N02 | média | alta | `ViewModels/MainViewModel.cs:7`, `using Microsoft.UI.Xaml.Controls` | V-34 | Remover referência a controle do ViewModel | Verificado |
| DSK-N16 | alta | n/a | n/a | V-35 | Narrator nos fluxos "criar pedido" e "pagar" | Não verificável |

Empacotamento: `MyApp.csproj:18` define `WindowsPackageType=None` e não há `PublishSingleFile`; sem MSIX, push e Store ficam fora (V-40). Decisão aberta: precisa de identidade de pacote?
Veredito: FIX FIRST.
</example>

## Gotchas

1. A página do WPF não cita MVVM (V-33); MVVM vem do Toolkit (V-34).
2. Ausência do MAUI na lista de plataformas do Toolkit não é incompatibilidade nem suporte confirmado (V-34).
3. A página do Toolkit tem mais de 18 meses (2024-11-07): tratada como atemporal, conferir a versão do pacote no projeto.
4. `PublishSingleFile` não vale para app empacotado nem para framework-dependent não empacotado (V-36).
5. Emulação Prism roda x64 só no Windows 11 ARM64; x86 roda em Windows 10 e 11 ARM64 (V-36). Relevante ao decidir bundle.
6. `ToolTip` não é nome acessível por definição; só aceite como nome o que o framework expõe como tal (conhecimento estável, Inferido), e confirme no Narrator.
7. Revisor que procura lacunas tende a achá-las (V-07): não reporte preferência de nomenclatura nem estilo de XAML aceito pelo repositório.

## Ressalvas e lacunas

Lacuna 6: acessibilidade do WPF sem página localizada; MVVM do MAUI (404 ao pesquisador, não procurada pelo validador); segurança de .NET desktop não lida; geradores do Toolkit não lidos. As páginas de deploy de apps empacotados e não empacotados só tiveram links conferidos (V-36). A skill não mede desempenho.

## Quando delegar

Não há agente específico para .NET: a revisão fica no fio principal. Para uma segunda leitura da diff use `diff-gap-reviewer` (contexto novo, somente leitura, só lacunas de correção e requisito). Cole a diff, o plano e a saída de testes no prompt de delegação, porque o agente só tem `Read`, `Grep` e `Glob`.
