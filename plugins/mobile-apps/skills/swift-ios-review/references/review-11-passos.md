# Revisão SwiftUI em 11 passos

Verificado em 2026-10-10. Os **nomes** dos 11 passos e as 12 regras de acessibilidade (lista completa em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/ios-swift.md`) vêm de SwiftUI Pro, de Paul Hudson (V-19, MIT, repositório `twostraws/SwiftUI-Agent-Skill`, versão 2.0.0). O **conteúdo de verificação** de cada passo abaixo é redação própria sobre conhecimento estável de SwiftUI (**Inferido**) e precisa ser conferido contra o SDK e o deployment target do projeto. Não reproduza regras que não se aplicam à versão lida. Só relate o que o código mostra.

Sumário: 1 API obsoleta · 2 views · 3 dados · 4 navegação · 5 design/HIG · 6 redimensionamento · 7 acessibilidade · 8 localização · 9 performance · 10 Swift · 11 higiene.

## 1. API obsoleta (condicionada ao deployment target)

| Padrão antigo | Alternativa | Desde | Observação |
| --- | --- | --- | --- |
| `NavigationView` | `NavigationStack` / `NavigationSplitView` | iOS 16 | Só se o target ≥ 16 |
| `.foregroundColor(_:)` | `.foregroundStyle(_:)` | iOS 15 em diante | Aceita estilos hierárquicos |
| `.cornerRadius(_:)` | `.clipShape(.rect(cornerRadius:))` | iOS 17 (forma `.rect`) | Em iOS 16, `RoundedRectangle` |
| `onChange(of:perform:)` | `onChange(of:) { old, new in }` ou sem parâmetros | iOS 17 | A forma antiga está depreciada |
| `ObservableObject` + `@Published` + `@StateObject` | `@Observable` + `@State` | iOS 17 | Veja passo 3 |
| `DispatchQueue.main.async` em código novo | `@MainActor` / `await` | Swift 5.5 | Passo 10 |
| `UIScreen.main.bounds` para layout | `GeometryReader`, `containerRelativeFrame`, `ViewThatFits` | varia | Passo 6 |

Se o target for menor que a "Desde", o achado vira nota ("quando subir o target"), não correção.

## 2. Views

- `body` barato: sem formatação pesada, ordenação, filtros caros nem I/O.
- Subviews como **tipos `View`** com entradas explícitas, não propriedades computadas gigantes; `AnyView` só com motivo (apaga identidade estrutural).
- `ForEach` com identidade estável (`Identifiable` ou `id:` estável), não índices de array mutável.
- Ações em métodos, não closures longas dentro do `body` (V-23).
- `.task { }` para trabalho assíncrono ligado ao ciclo de vida da view (cancelado quando a view sai), em vez de `Task { }` em `onAppear` sem cancelamento (**Inferido**).

## 3. Dados e estado

Antes/depois do caso mais comum (dono de objeto criado dentro da view):

```swift
// Antes: a view cria o objeto e não é dona dele; pode ser recriado em re-render do pai
struct ListView: View {
    @ObservedObject var vm = ListVM()
}

// Depois, iOS 16 ou inferior
struct ListView: View {
    @StateObject private var vm = ListVM()
}

// Depois, iOS 17+
@Observable final class ListVM { var items: [Item] = [] }
struct ListView: View {
    @State private var vm = ListVM()
}
```

Checklist: `@State` para valor que a view possui e é privado; `@Binding` para valor de outro dono; `@Bindable` para criar bindings de um `@Observable`; `@Environment` para dependência compartilhada; um dono por estado (V-10 vale também aqui por analogia, **Inferido**); `@ObservedObject` só para objeto cujo dono é outro.

## 4. Navegação

- `NavigationStack` com caminho como estado (`NavigationPath` ou array tipado) e `navigationDestination(for:)` por tipo de valor.
- `NavigationLink(value:)` em listas em vez de destinos construídos eagerly.
- Sheets e fullScreenCover com `item:` quando o conteúdo depende de um valor; evite booleano + variável separada que pode ficar fora de sincronia.

## 5. Design / HIG

- Prefira componentes do sistema (Form, List, Toolbar, `Label`, SF Symbols) a recriar controles.
- Estilos semânticos: cores do sistema e `foregroundStyle(.primary/.secondary)`, fontes por estilo (`.font(.body)`), não tamanhos fixos.
- Valores numéricos de alvo de toque e contraste vêm de V-18 (44x44 pt, mínimo 28 pt; 4,5:1 e 3:1), não de memória. **Não** copie "13 pt", "margens de 20 pt", "alvo 20x20" ou "texto tocável < 24 pt" de materiais de inspiração: Não verificáveis (C15).
- Liquid Glass é orientado a controles e navegação; aplicação extensa em conteúdo prejudica hierarquia (brain `apple-design.md`, Apple Materials). API nova de material: confirmar SDK e fallback antes de usar.

## 6. Redimensionamento

- `ViewThatFits`, `Layout`, `Grid`, `containerRelativeFrame` em vez de larguras fixas.
- `@ScaledMetric` para espaçamentos que devem acompanhar o Dynamic Type.
- Respeite safe areas; teste iPad/Split View se o app roda em iPad.
- Evite `GeometryReader` como muleta onde `frame`/alinhamento resolve.

## 7. Acessibilidade (V-19, 12 regras)

As linhas com fonte V-19 vêm da skill original (lista completa das 12, conferida em 2026-10-10, em `${CLAUDE_PLUGIN_ROOT}/skills/playbook/references/ios-swift.md`); as marcadas **Inferido** são conhecimento estável.

| Regra | Código correto | Fonte |
| --- | --- | --- |
| Respeitar Dynamic Type; limitar só com motivo | `.dynamicTypeSize(...DynamicTypeSize.accessibility3)` apenas em trechos que quebram | V-19 |
| Imagem decorativa | `Image(decorative: "banner")` | V-19 |
| Respeitar Reduce Motion | `@Environment(\.accessibilityReduceMotion) var reduceMotion` e desligar animações grandes | V-19 |
| Rótulos de entrada de voz | `.accessibilityInputLabels(["Enviar", "Mandar"])` | V-19 |
| Botão só com ícone sempre com texto | `Button { } label: { Label("Fechar", systemImage: "xmark") }.labelStyle(.iconOnly)` | V-19 |
| Não depender só de cor | `@Environment(\.accessibilityDifferentiateWithoutColor)` e acrescentar símbolo/texto | V-19 |
| `Button` em vez de `onTapGesture` | trocar `Image(...).onTapGesture {}` por `Button`; gesto inevitável recebe `.accessibilityAddTraits(.isButton)` | V-19, V-48 |
| Texto com estilo dinâmico; menu com título em texto | `.font(.body)` em vez de `.font(.system(size: 14))`; `Menu("Opções", systemImage: ...)` | V-19 |
| Rótulo curto, hint só quando necessária | `.accessibilityLabel("Enviar")`, `.accessibilityHint("Abre a tela de confirmação")` | V-78 |
| Agrupar elementos relacionados | `.accessibilityElement(children: .combine)` | V-78, Inferido |
| Títulos | `.accessibilityAddTraits(.isHeader)` | Inferido |
| Alvo mínimo | `.frame(minWidth: 44, minHeight: 44)` ou `.contentShape(Rectangle())` | V-18 (44x44 pt) |
| Estado dinâmico anunciado | `.accessibilityValue(isOn ? "Ativado" : "Desativado")` | V-78 |

Regra de rótulo no iOS: "não repetir o tipo do elemento" ("Enviar", não "Botão enviar") é **Inferido** até ler a página de traits (V-78, V-79 só confirma no Android). A passagem real com VoiceOver é verificação humana (V-78).

## 8. Localização

- Strings visíveis em `String(localized:)`/`LocalizedStringKey` (String Catalog `.xcstrings`); plurais pelo catálogo; datas e números com `format:`/`FormatStyle`.
- Sem concatenar fragmentos traduzidos; passe interpolação no catálogo.
- Purpose strings (`NS*UsageDescription`) localizadas em `InfoPlist.xcstrings` (V-58).

## 9. Performance

- Sem trabalho caro no `body`; `LazyVStack`/`LazyHStack`/`List` para coleções grandes.
- Evite invalidar a árvore inteira com um estado compartilhado largo; estado perto de quem usa.
- Mensurável: use `mobile-performance-diagnosis` (6 passos de V-22; Instruments exige macOS). `Self._printChanges()` ajuda em debug, não em release (**Inferido**).
- A referência `performance-plus` da skill original não está incluída neste plugin; para revisão profunda pedida, use `mobile-performance-diagnosis`.

## 10. Swift

- Concorrência moderna (`async/await`, `@MainActor`) em código novo; veja [concurrency.md](concurrency.md).
- Sem `try!`/`!` em dados externos; `guard`/`if let`.
- Tipos de valor por padrão; `final class` quando referência é necessária.
- `some View` como retorno de `body`.

## 11. Higiene

- Código morto, imports sem uso, `print` residual (use `Logger`), TODO sem dono.
- Segredos fora do código (S-06), tokens no Keychain (V-83).
- Previews que compilam e usam dados sintéticos.
- Nada de `// swiftlint:disable` em massa sem motivo.

## Relatório vazio é válido

Se nenhum passo gerar achado, devolva: "Sem achados. Verificado: passos 1 a 11 em <arquivos>; deployment target <X>; build não executado." Não invente problema para justificar a revisão.
