# Checklist de acessibilidade mobile: 9 itens por plataforma

Verificado em 2026-10-10. Números e regras oficiais: HIG de acessibilidade (V-18, JSON da Apple), Android (V-09, V-79), VoiceOver (V-78), SwiftUI Pro (V-19, MIT), síntese V-48 (rótulos, nativos, alvos, texto, agrupamento, foco, contraste, movimento, passagem manual). Trechos de código são esboços originais; APIs marcadas **Inferido** são conhecimento estável e precisam ser conferidas na versão do projeto. RN e Flutter não têm fonte validada neste plugin (lacuna): todos os itens dessas stacks são **Inferido**.

## Números oficiais (copie daqui, não de memória)

| Medida | iOS (V-18) | Android (V-79, V-09) |
| --- | --- | --- |
| Alvo de toque | **44x44 pt** padrão; **28x28 pt** mínimo absoluto | **48x48 dp** (`Button`/`IconButton` já aplicam; personalizados precisam de `sizeIn`) |
| Texto escalável | Dynamic Type até **200%** (140% no watchOS); texto padrão 17 pt, mínimo 11 pt | Texto em `sp`; testar o maior tamanho |
| Contraste | **4,5:1** até 17 pt; **3:1** a partir de 18 pt ou negrito | **4,5:1** abaixo de 18 sp (ou negrito abaixo de 14 sp); **3:1** para o restante |
| Espaçamento entre alvos | ~12 pt (com borda), ~24 pt (sem borda) | — |

Não usar: "13 pt", "margens de 20 pt", "alvo 20x20", "texto tocável < 24 pt" (inspirações não verificadas, C15). Contraste de componentes não textuais: sem número em V-79.

## Item 1: rótulos

Regra: todo controle interativo tem rótulo; imagens decorativas ocultas; rótulo curto, sem repetir o tipo e único (Android, V-79); uma `UILabel` e um `accessibilityLabel` são coisas diferentes (V-78).

```swift
// SwiftUI
Button { dismiss() } label: { Label("Fechar", systemImage: "xmark") }
    .labelStyle(.iconOnly)                      // texto lido: "Fechar"
Image(decorative: "banner")                     // oculto para VoiceOver
```

```kotlin
// Compose
IconButton(onClick = onClose) { Icon(Icons.Default.Close, contentDescription = "Fechar") }
Icon(Icons.Default.Star, contentDescription = null)   // decorativo (null)
```

```tsx
// React Native (Inferido)
<Pressable accessibilityRole="button" accessibilityLabel="Fechar" onPress={onClose}>
  <CloseIcon />
</Pressable>
```

```dart
// Flutter (Inferido)
IconButton(icon: const Icon(Icons.close), tooltip: 'Fechar', onPressed: onClose)
ExcludeSemantics(child: DecorativeBanner())
```

## Item 2: controles nativos em vez de gestos

```swift
// Antes: não é botão para VoiceOver
Image(systemName: "heart").onTapGesture { toggle() }
// Depois
Button { toggle() } label: { Label("Curtir", systemImage: "heart") }.labelStyle(.iconOnly)
```

Android: `Modifier.clickable(onClickLabel = "Curtir", role = Role.Button) { }` ou `IconButton` (`onClickLabel` é indireto em V-09: confira a API). RN: `Pressable` com `accessibilityRole`. Flutter: `InkWell`/`IconButton` com `Semantics(button: true, label: ...)` quando necessário.

## Item 3: alvos de toque

```swift
Button("Mais") { }.frame(minWidth: 44, minHeight: 44)          // iOS
```

```kotlin
IconButton(onClick = onClick, modifier = Modifier.sizeIn(minWidth = 48.dp, minHeight = 48.dp)) { /* ícone 24.dp */ }
```

Alvo visual pequeno com área maior de toque: iOS `.contentShape(Rectangle())`; RN `hitSlop`; Flutter `MaterialTapTargetSize.padded` ou `SizedBox` mínimo (todos **Inferido**).

## Item 4: texto escalável

- iOS: estilos semânticos (`.font(.body)`, `.title`), `@ScaledMetric` para espaçamento; limitar com `dynamicTypeSize(...DynamicTypeSize.accessibility3)` só quando há motivo. Teste no maior tamanho de acessibilidade.
- Android: `sp`; sem altura fixa de container em `dp` que corte o texto; teste com escala de fonte máxima.
- RN: `allowFontScaling` (padrão ativo) e `maxFontSizeMultiplier` quando precisar limitar (Inferido). Flutter: `MediaQuery.textScalerOf(context)`; não desative a escala (Inferido).

## Item 5: agrupar e marcar títulos

```swift
VStack { Text("Total"); Text("R$ 90,00") }.accessibilityElement(children: .combine)
Text("Pagamentos").accessibilityAddTraits(.isHeader)            // Inferido
```

```kotlin
Row(Modifier.semantics(mergeDescendants = true) { }) { Text("Total"); Text("R$ 90,00") }
Text("Pagamentos", Modifier.semantics { heading() })
```

Android também: `paneTitle` (API 28+), `hideFromAccessibility`/`clearAndSetSemantics` para ocultar ou substituir (V-09).

## Item 6: ordem de foco

A ordem de leitura deve seguir a ordem visual. Procure no código: reordenação visual por `Modifier.offset`/`zIndex`/`order` sem semântica correspondente (Android `traversalIndex` — Inferido), `accessibilitySortPriority` (iOS, Inferido). A confirmação real é pendência humana.

## Item 7: contraste e cor

Calcule a razão com os valores reais de texto e fundo (fórmula de contraste WCAG); registre o par de cores e o tamanho. Nunca estime pela imagem (brain `apple-design.md`). Informação por cor sozinha (erro em vermelho, estado verde) precisa de texto/ícone: iOS `accessibilityDifferentiateWithoutColor` (V-19); Android V-09, V-48.

## Item 8: movimento e gestos

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion
withAnimation(reduceMotion ? nil : .spring()) { expanded.toggle() }
```

Alternativa visível a gestos: Android `semantics { customActions = listOf(CustomAccessibilityAction("Excluir") { onDelete(); true }) }` (V-09); iOS `.accessibilityAction(named: "Excluir") { }` (Inferido). RN: `accessibilityActions` + `onAccessibilityAction` (Inferido).

## Item 9: estado dinâmico e hint

```swift
Toggle("Notificações", isOn: $on)                               // estado vem de graça
Button("Salvar") { }.accessibilityHint("Abre a confirmação")    // só se o rótulo não bastar (V-78)
```

Estado que muda só por cor ou posição precisa de valor falado (`accessibilityValue`, `stateDescription`, `selected` em RN). Conteúdo longo demais no rótulo pode ir para a dica (V-78).

## Passagem humana (checklist para o usuário)

VoiceOver (V-78): ligar em Ajustes > Acessibilidade > VoiceOver; deslizar para navegar; toque duplo para ativar; dois dedos tocam para parar/retomar a fala; deslizar com dois dedos para cima para ler tudo; **Screen Curtain** com toque triplo de três dedos; verificar acesso a todo elemento e a ordem de leitura. TalkBack: ligar nas configurações de acessibilidade do aparelho Android; navegar por deslize e ativar com toque duplo (gestos do TalkBack: **Inferido**, conferir a ajuda do sistema). Repetir com a fonte no maior tamanho e com Reduce Motion ligado.
