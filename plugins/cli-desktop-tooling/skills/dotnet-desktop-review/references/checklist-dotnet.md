# Checklist de apps desktop .NET (WPF, WinUI 3, MAUI)

Verificado em 2026-10-10 contra V-33, V-34, V-35, V-36, V-37. Os IDs DSK-N01 a N07 e as severidades padrão são os do `checklist-completo.md` do playbook; DSK-N08 em diante são extensões desta skill (Inferido quanto à numeração e à severidade). Padrões de busca, nomes de propriedades de projeto e trechos de código são da fábrica (**Inferido**, conhecimento estável do ecossistema): confirme na versão do SDK e dos pacotes do projeto. Os trechos não foram compilados.

Sumário: [IDs canônicos](#ids-canônicos-dsk-n01-a-n07) · [WPF e MVVM](#wpf-e-mvvm-toolkit) · [Acessibilidade WinUI 3](#acessibilidade-winui-3-v-35) · [MAUI](#maui) · [Empacotamento](#empacotamento-v-36) · [Padrões de busca](#padrões-de-busca)

## IDs canônicos (DSK-N01 a N07)

| ID | Sev. | Verificar | Fonte | Correção |
| --- | --- | --- | --- | --- |
| DSK-N01 | Média | Handlers de clique para ações reutilizáveis em WPF (`Click="` repetido; regra de negócio no code-behind) | V-33 | Comando (`ICommand`); code-behind só para comportamento específico da tela |
| DSK-N02 | Média | ViewModel com referência a controles (`using System.Windows.Controls`, `using Microsoft.UI.Xaml.Controls`, `Window`, `Button`) | V-34 | Desacoplar; serviço de interface para diálogos |
| DSK-N03 | Alta | Controle interativo sem nome acessível (botão só com ícone, `Image` informativa, `TextBox` sem rótulo) | V-35 | `AutomationProperties.Name` (ou `x:Uid` com recurso localizado); `AutomationProperties.LabeledBy` para campos |
| DSK-N04 | Média | Três subitens: **N04a** cor fixa que bloqueia alto contraste; **N04b** ordem de Tab não revisada; **N04c** controle customizado sem `AutomationPeer` | V-35 | N04a: `{ThemeResource ...}` e dicionário de alto contraste. N04b: Tab segue o layout. N04c: sobrescrever `OnCreateAutomationPeer` (N04c é Alta) |
| DSK-N05 | Média | MAUI sem alvo mobile ou macOS (`<TargetFrameworks>` só com `windows10.0...`) | V-37 | WinUI 3 ou WPF |
| DSK-N06 | Média | `PublishSingleFile` fora de app não empacotado e self-contained | V-36 | Ajustar o modo de publicação |
| DSK-N07 | Baixa | Acessibilidade do WPF e segurança de .NET desktop não avaliadas | V-33 (lacuna) | Declarar Não verificável |

## WPF e MVVM Toolkit

Pacote `CommunityToolkit.Mvvm` (MIT, V-34). A página lida cita: `ObservableObject`, `ObservableRecipient`, `ObservableValidator`, `RelayCommand`, `AsyncRelayCommand`, `IMessenger` (`WeakReferenceMessenger`, `StrongReferenceMessenger`) e `Ioc`. Não afirma nada sobre geradores de código.

| ID | Sev. | Como detectar | Fonte | Correção |
| --- | --- | --- | --- | --- |
| DSK-N08 | Média | `DataContext` atribuído em vários lugares; `{Binding}` sem caminho claro; erros de binding no log de saída do depurador | V-33 | Um `DataContext` por tela, definido de forma previsível |
| DSK-N09 | Baixa | Aparência alterada por código em vez de `ControlTemplate`/estilo | V-33 | `ControlTemplate` troca aparência sem mudar comportamento |
| DSK-N10 | Info | `.csproj` com `TargetFrameworkVersion` v4.x ou `net4xx` | V-33 | A página oficial recomenda migrar de .NET Framework para .NET (acessibilidade e confiabilidade melhores): plano, não defeito |
| DSK-N11 | Média | Comandos implementados à mão; `async void` em handlers | V-34 | `RelayCommand`/`AsyncRelayCommand` |
| DSK-N12 | Baixa | ViewModels se referenciando diretamente para trocar dados | V-34 | `IMessenger`; `WeakReferenceMessenger` evita vazamento por referência forte (estável, Inferido) |
| DSK-N13 | Baixa | Validação espalhada em setters e code-behind | V-34 | `ObservableValidator` |
| DSK-N14 | Info | Projeto MAUI usando o Toolkit | V-34 | Não afirmar compatibilidade nem incompatibilidade; testar |

Forma básica sem geradores (ilustrativa; `SetProperty` é do `ObservableObject`, estável, Inferido quanto à assinatura na sua versão):

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

public class PedidoViewModel : ObservableObject
{
    private string _status = "";
    public string Status
    {
        get => _status;
        set => SetProperty(ref _status, value);
    }

    public AsyncRelayCommand SalvarCommand { get; }

    public PedidoViewModel(IPedidoService servico)
        => SalvarCommand = new AsyncRelayCommand(async () => Status = await servico.SalvarAsync());
}
```

## Acessibilidade WinUI 3 (V-35)

Base: acessibilidade vem de UI Automation (peers e patterns); o dado mais importante é o nome acessível; teclado é embutido; alto contraste funciona sem cores fixas; controle customizado precisa de `AutomationPeer`; DirectX em `SwapChainPanel`/`SurfaceImageSource` não é acessível por padrão; a verificação combina checagem automática a cada build e teste manual com Narrator. A página de WPF equivalente **não** foi lida: para WPF os mesmos itens são Inferido.

Os sete itens da fonte, ligados aos IDs: (1) nome acessível = DSK-N03; (2) ordem de Tab = DSK-N04b; (3) alto contraste = DSK-N04a; (4) escala de texto = DSK-N15; (5) `AutomationPeer` = DSK-N04c; (6) Narrator = DSK-N16; (7) checagem automática no CI = DSK-N17.

| ID | Sev. | Como detectar | Correção |
| --- | --- | --- | --- |
| DSK-N15 | Média | `FontSize` e `Height`/`Width` fixos em contêineres de texto; texto cortado ao aumentar a escala | Layout flexível; testar com escala do sistema alta |
| DSK-N16 | Alta | Fluxo crítico nunca testado com leitor de tela | Narrator nos fluxos críticos (verificação humana; **Não verificável** por leitura) |
| DSK-N17 | Média | Nenhuma checagem automática de acessibilidade no CI | Checagem a cada build (a ferramenta é escolha do time; um exemplo conhecido, não validado aqui, é o Accessibility Insights for Windows — Inferido) |
| DSK-N18 | Alta | `SwapChainPanel` ou `SurfaceImageSource` em tela crítica | Alternativa acessível fora do conteúdo DirectX |
| DSK-N19 | Baixa | Estado só por cor | Sinal combinado: ícone com cor, alerta visual com som (V-35) |

Exemplo antes/depois (ilustrativo):

```xml
<!-- Antes: leitor de tela lê "botão" sem contexto (DSK-N03) -->
<AppBarButton Icon="Delete" Click="OnDelete" />

<!-- Depois -->
<AppBarButton Icon="Delete" Command="{x:Bind ViewModel.ExcluirCommand}"
              AutomationProperties.Name="Excluir pedido" />
```

```xml
<!-- Antes: cor fixa quebra o alto contraste (DSK-N04a) -->
<TextBlock Foreground="#FF1E1E1E" Text="Total" />

<!-- Depois -->
<TextBlock Foreground="{ThemeResource TextFillColorPrimaryBrush}" Text="Total" />
```

O nome do recurso de tema (`TextFillColorPrimaryBrush`) existe nos temas padrão do WinUI (estável, Inferido); confirme no projeto.

## MAUI

Justifique MAUI pelo alvo mobile ou macOS (DSK-N05); iOS e macOS exigem um Mac para compilar (V-37). No Windows ele usa WinUI 3, então os itens de acessibilidade acima valem para a parte Windows. A página lida não trata de MVVM do MAUI nem de empacotamento e acessibilidade de desktop.

## Empacotamento (V-36)

Árvore: (1) Store ou assinatura própria (V-44) · (2) identidade de pacote (V-40) · (3) framework-dependent ou self-contained · (4) RID e bundle · (5) `PublishSingleFile` só para não empacotado e self-contained (Windows App SDK 1.5 ou posterior; DSK-N06).

| Modo | Vantagem | Custo | Inicialização do runtime (V-36) |
| --- | --- | --- | --- |
| Empacotado, framework-dependent | Pequeno; atualizável pelo sistema | Depende do runtime; risco de componente compartilhado removido ou regressão | Deployment API |
| Não empacotado, framework-dependent | Sem identidade de pacote | Idem; instalação do runtime | Bootstrapper API |
| Self-contained | Controle da versão, isolamento, xcopy | Maior; no não empacotado, mais lento e sem servicing | Empacotado: não precisa de inicialização |

Arquiteturas: publicar por RID (`win-x64`, `win-arm64`); bundle MSIX com x64 e ARM64; Arm64EC para bases C/C++ grandes; a emulação Prism roda x64 só no Windows 11 ARM64 (x86 em Windows 10 e 11 ARM64). Propriedades de projeto relacionadas (`WindowsPackageType`, `WindowsAppSDKSelfContained`, `RuntimeIdentifier`, `PublishSingleFile`) são nomes do ecossistema (Inferido): leia o `.csproj` para ver o que está definido, não o que deveria estar.

## Padrões de busca

| Objetivo | Expressão (Grep) | Arquivos |
| --- | --- | --- |
| Botões só com ícone | `<AppBarButton` / `<Button` sem `AutomationProperties.Name` na mesma tag | `*.xaml` |
| Cores fixas | `Foreground="#`, `Background="#`, `Fill="#`, `Color="#` | `*.xaml` |
| Handlers de clique | `Click="` | `*.xaml` |
| Controle customizado | `: Control` / `: ContentControl` e `OnCreateAutomationPeer` | `*.cs` |
| ViewModel com controle | `using System.Windows.Controls`, `using Microsoft.UI.Xaml.Controls` | `ViewModels/**/*.cs` |
| DirectX | `SwapChainPanel`, `SurfaceImageSource` | `*.xaml`, `*.cs` |
| Empacotamento | `WindowsPackageType`, `SelfContained`, `PublishSingleFile`, `RuntimeIdentifier` | `*.csproj`, `Directory.Build.props` |
