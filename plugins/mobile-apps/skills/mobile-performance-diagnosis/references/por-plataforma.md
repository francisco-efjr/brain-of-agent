# Diagnóstico de performance por plataforma

Verificado em 2026-10-10. Fontes: Compose (V-11, chrisbanes, Apache-2.0, classe B), SwiftUI (V-22, Dimillian, MIT, B), Flutter (V-29, oficial), React Native (V-30 oficial, V-32 Callstack MIT). Redação própria. Comandos e trechos marcados **Inferido** são conhecimento estável do domínio: confirme na versão do projeto.

Método comum: reproduzir uma transição → classificar o eixo → mudar um ponto → remedir a mesma captura → reverter se não melhorou.

## Compose (Android)

### Como medir (Inferido)

- Build **release** (não debugável) em aparelho real de baixa capacidade. Debug distorce.
- Relatórios do compilador Compose: com o plugin Gradle do compilador (Kotlin 2.0+), propriedades `reportsDestination` e `metricsDestination` na extensão `composeCompiler { }` geram `*-composables.txt` e `*-classes.txt`. Conferir a documentação da versão.
- Layout Inspector → contagem de recomposição/skip; Perfetto/System Trace para frames; Macrobenchmark como opção (V-11 não o exige).

### Os 3 eixos (V-11)

| Eixo | Sintoma | Verificação | Correção típica |
| --- | --- | --- | --- |
| **Estabilidade** | Composable "restartable, not skippable" com parâmetros instáveis | Relatório do compilador | Dados imutáveis; `ImmutableList` na fronteira (V-11, `stability.md`); só use `@Immutable`/`@Stable` se a promessa é verdadeira |
| **Fase de leitura de State** | Leitura de scroll/animação na composição recompõe a cada frame | Procure leituras como `scrollState.value`, `animateFloat.value` no corpo do composable | Adiar a leitura: modificadores com lambda que leem na fase de layout/draw (`Modifier.offset { }`, `Modifier.graphicsLayer { }`) |
| **Escrita de snapshot** | Escrita de State durante composição, laços de recomposição | Procure `state = x` fora de callback/efeito | Mover a escrita para evento/efeito; `derivedStateOf` para valor derivado que muda menos que a fonte |

Falsos positivos: composable pequeno "não pulável" que quase nunca recompõe não é problema; priorize o que recompõe com frequência durante o gesto reproduzido.

### Strong skipping e anotações (V-11, `stability.md`)

Strong skipping é padrão no Kotlin 2.0.20+. Lambdas são memoizadas e parâmetros instáveis comparados por igualdade de instância. Resultado: muitas anotações antigas deixam de ser necessárias. `@Immutable`/`@Stable` são promessas ao compilador; usá-las para silenciar o relatório esconde defeitos. Confirme a versão do Kotlin do projeto antes de aconselhar.

### Listas

```kotlin
LazyColumn {
    items(products, key = { it.id }) { product ->      // identidade estável
        ProductRow(product, onClick = { onOpen(product.id) })
    }
}
```

`key` estável preserva estado e evita recomposição desnecessária ao inserir/remover. Não coloque `remember` em tudo: `remember` guarda o resultado de cálculo caro ou objeto que precisa sobreviver à recomposição, não otimiza por reflexo.

## SwiftUI (iOS), 6 passos de V-22

1. Classifique o sintoma (rolagem, abertura de tela, digitação, animação).
2. Revise o código atrás de causas óbvias: trabalho no `body`, `ForEach` sem identidade estável, estado largo invalidando a árvore, imagens grandes decodificadas na main.
3. Perfil guiado **só se necessário**: Instruments (SwiftUI, Time Profiler, Hangs). **Exige macOS.**
4. Mapeie a evidência até a causa suspeita.
5. Corrija com a menor mudança.
6. **Repita a mesma captura** e compare.

Ajuda em debug: `let _ = Self._printChanges()` dentro do `body` mostra o que invalidou a view (não use em release; **Inferido**). Redija dados sensíveis de traces e screenshots (correção de V-22).

## Flutter (V-29, oficial)

- Trabalho fora de `build()`: `build` pode rodar a cada frame de animação.
- `setState` na **menor subárvore** possível; extraia widgets.
- `const` quando possível; `StatelessWidget` em vez de função que devolve widget.
- Listas **lazy** (`ListView.builder`), não `ListView(children: [...])` para listas longas.
- `Opacity` e `saveLayer` são caros; use alternativas (`AnimatedOpacity`, aplicar opacidade na cor).
- Não sobrescreva `operator ==` em widgets.
- Orçamento de 16 ms por frame (8 ms build + 8 ms render para 60 Hz).
- Meça em **profile mode** com DevTools, no aparelho de menor capacidade: `flutter run --profile` (Inferido; a página de build modes dá os detalhes). A regra "nunca em debug ou simulador" não consta em V-29.

## React Native / Expo (V-30 e V-32)

1. **Meça em release.** Dev mode é lento por design (V-30). Candidatos: `npx react-native run-android --mode release`, `npx react-native run-ios --mode Release`; Expo: `npx expo run:android --variant release`, `npx expo run:ios --configuration Release` (flags: **Inferido**, confira `--help`).
2. `console.*` trava a thread JS em produção: plugin Babel `transform-remove-console`.
3. Listas: virtualizadas; `getItemLayout` quando a altura é conhecida; FlashList ou Legend List (citadas em V-30).
4. Animações: `useNativeDriver: true` onde suportado; animar só `transform` e `opacity` (V-31); evitar trabalho na thread JS durante o gesto.
5. `requestAnimationFrame` em `onPress` para trabalho pesado após o feedback visual (V-30).
6. Separe **thread JS** de **thread UI**: o sintoma indica qual (queda de FPS da JS vs da UI no Perf Monitor).
7. **Ciclo de V-32**: medir → otimizar **um** ponto → remedir → validar; reverter se não houver ganho. **Não adicione memoização sem problema medido.** Conferir a versão da biblioteca antes de aplicar correção específica. Medir só cold start para TTI.
8. Comandos `npx` de qualquer skill externa: fixe a versão (V-32 avisa).

## Partida (cold start): o que medir em cada stack (Inferido)

- Android: tempo até a primeira tela desenhada (`Displayed` no logcat; Macrobenchmark). 
- iOS: Instruments App Launch (macOS).
- Flutter/RN: tempo até a primeira tela interativa com o build de release; RN: só cold start para TTI (V-32).

## Quando a causa não é de renderização

Estado duplicado ou ausência de fonte de verdade → `mobile-architecture-review`. Rede lenta/N+1 → fronteira `backend-api`. Banco local sem índice → `database-data-modeling` (lado do cliente). Registre e encaminhe.
