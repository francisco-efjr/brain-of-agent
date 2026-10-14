# Ferramentas de teste por plataforma

Verificado em 2026-10-10. Fontes oficiais: Android (V-08 fundamentos, V-65 Compose, V-68 Espresso), Apple (V-66), Flutter (V-67), React Native (V-69), Detox (V-70, classe B), Maestro no EAS Workflows (V-37). Redação própria. Exemplos de código são esboços originais, **Inferido** quanto a nomes de API: confirme na versão do projeto. Nada aqui manda instalar ferramenta: instalar é decisão do usuário.

## Android

Fundamentos (V-08): testes **pequenos, médios e "grandes"**; **local** (JVM) vs **instrumentado** (aparelho/emulador), sem mapeamento 1:1 com o tamanho; ViewModel testado com **repositório fake**; comentários Given/When/Then. Sem proporção oficial de pirâmide.

| Camada | Ferramenta | Observação |
| --- | --- | --- |
| Unitário / ViewModel | JUnit, coroutines test, fake do repositório | Local; rápido |
| UI Compose | `ComposeTestRule` (V-65) | Dependências: `androidTestImplementation("androidx.compose.ui:ui-test-junit4:...")` e `debugImplementation("androidx.compose.ui:ui-test-manifest:...")` (a segunda é necessária para `createComposeRule()`, não para `createAndroidComposeRule<Activity>()`) |
| UI com Views | Espresso (V-68) | Sincroniza com fila de mensagens e idling resources; **sem `sleep` nem polling** |
| Apps mistos | os dois podem coexistir (Inferido) | |

```kotlin
class LoginScreenTest {
    @get:Rule val rule = createComposeRule()

    @Test fun mostraErroDeSenha() {
        // Given
        rule.setContent { LoginScreen(state = LoginState(error = "Senha inválida"), onSubmit = {}) }
        // Then
        rule.onNodeWithText("Senha inválida").assertIsDisplayed()
    }

    @Test fun enviaAoTocar() {
        var enviado = false
        rule.setContent { LoginScreen(state = LoginState(), onSubmit = { enviado = true }) }
        rule.onNodeWithText("Entrar").performClick()    // When
        assertTrue(enviado)                              // Then
    }
}
```

Os testes esperam a UI ficar ociosa antes de agir (V-65). Localize por semântica (texto, `contentDescription`); `testTag` é Inferido. Para trabalho assíncrono próprio, registre um idling resource em vez de dormir.

## iOS

Regra (V-66, Xcode 16+): a página diz "considere usar" **Swift Testing** para novos testes unitários; **XCTest** para UI e performance; um target pode conter os dois, mas **não misture APIs no mesmo teste**. UI usa XCTest com XCUIAutomation e roda no simulador (macOS).

```swift
import Testing
@Test func totalSomaItens() {
    let carrinho = Carrinho(itens: [.init(preco: 10), .init(preco: 20)])
    #expect(carrinho.total == 30)
}
```

```swift
// UI: XCTest + XCUIAutomation (macOS)
final class LoginUITests: XCTestCase {
    func testMostraErro() {
        let app = XCUIApplication(); app.launch()
        app.buttons["Entrar"].tap()
        XCTAssertTrue(app.staticTexts["Senha inválida"].waitForExistence(timeout: 5))
    }
}
```

`XCUIApplication` e seletores não foram lidos em profundidade (lacuna 10): o exemplo é **Inferido**. Sem macOS, o plano lista esses testes como **Não verificável**.

## Flutter

Tipos (V-67): **unitário** (função/método/classe), **widget** (um widget), **integração** (app inteiro ou grande parte). Confiança e custo de manutenção sobem, a velocidade cai do unitário à integração. Estratégia: muitos unitários e de widget, medidos por cobertura, mais integração suficiente para os casos de uso importantes. `integration_test` **não interage com UI nativa** (diálogos de permissão, notificações, platform views): a página sugere `patrol` (confira versão e compatibilidade).

```dart
testWidgets('mostra erro de senha', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: LoginPage()));
  await tester.tap(find.text('Entrar'));
  await tester.pump();
  expect(find.text('Senha inválida'), findsOneWidget);
});
```

## React Native e Expo

Camadas (V-69, oficial): análise estática (ESLint, TypeScript); unitários com Jest (Arrange-Act-Assert, preferir objetos reais a mocks, mocks para serviços externos e módulos nativos); integração; componentes com **React Native Testing Library** (do ponto de vista do usuário: texto visível e helpers de acessibilidade, evitar detalhes de implementação e `testID`, snapshots pequenos; rodam em Node e não consideram código nativo); **E2E só para o vital** (autenticação, funções centrais, pagamentos) com Detox, Appium ou Maestro, porque são mais lentos e instáveis.

```tsx
test('mostra erro de senha', async () => {
  render(<Login />);
  fireEvent.press(screen.getByText('Entrar'));
  expect(await screen.findByText('Senha inválida')).toBeTruthy();
});
```

E2E:

- **Maestro** (fluxos YAML em `.maestro/` com `appId`): no EAS Workflows é job em **alfa**, com perfil `e2e-test` (`withoutCredentials`, APK sem assinatura, build de simulador) e disparo manual, `pull_request` ou `pull_request_labeled` (V-37). Exemplos oficiais usam texto visível, não `testID`.

```yaml
appId: com.exemplo.app
---
- launchApp
- tapOn: "Entrar"
- assertVisible: "Senha inválida"     # assertVisible já espera até o timeout
```

- **Detox** (V-70): E2E em JavaScript para Android e iOS; **aparelho real no iOS não suportado**; versões de RN suportadas (README lido: 0.77.x a 0.84.x, todas com a Nova Arquitetura); pré-requisito de macOS **não verificado**. Confira a versão de RN do projeto contra a faixa antes de recomendar.
- `testID`: somente em E2E de app multilíngue, onde o texto muda por idioma (C2).

## Escolha rápida

| Situação | Escolha |
| --- | --- |
| Regra de negócio / estado | Unitário com fake (todas as plataformas) |
| Tela em Compose | `ComposeTestRule` |
| Tela SwiftUI | XCUIAutomation para fluxo; unidade na lógica com Swift Testing |
| Flutter com diálogo de permissão | `patrol` sobre `integration_test` |
| RN componente | RNTL por texto/papel |
| RN fluxo vital | Maestro ou Detox (E2E único) |
| Playwright | N/A em UI nativa; WebView e Chrome Android experimentais; backend com `request`: `qa-playwright:non-web-systems` |
| App que exige aparelho físico iOS | Detox não suporta aparelho real no iOS (V-70); XCUITest roda pelo Xcode (macOS); suporte das demais ferramentas em aparelho real: Não verificado. Appium delega a drivers instalados à parte (brain) |
