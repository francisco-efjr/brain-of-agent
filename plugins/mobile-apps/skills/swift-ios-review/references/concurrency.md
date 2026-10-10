# Swift Concurrency: triagem, correção e migração

Verificado em 2026-10-10. Base: triagem de Antoine van der Lee (V-20, MIT, repositório `AvdLee/Swift-Concurrency-Agent-Skill`), loop de Dimillian (V-21, classe B), estratégia do guia de migração do swift.org (V-80, Apache-2.0; só `MigrationStrategy.md` foi lido). Redação própria. A tabela de diagnósticos é conhecimento estável (**Inferido**) e precisa ser conferida compilando no Xcode/toolchain do projeto.

## 0. Antes de tudo

1. Ler a configuração: modo da linguagem (Swift 5 ou 6), `SWIFT_STRICT_CONCURRENCY` (`minimal`, `targeted`, `complete`), recursos upcoming habilitados, isolamento padrão do módulo, deployment target. Em SwiftPM: `swiftSettings` do `Package.swift`. **Não edite `.pbxproj`.**
2. Capturar o diagnóstico exato (texto completo do compilador).
3. Se faltar qualquer um, pergunte; não "adivinhe pelo nome do erro".

## 1. Árvore de decisão (5 passos, V-20)

1. **Configuração lida?** Não → pergunte.
2. **Diagnóstico exato em mãos?** Não → peça.
3. **Fronteira de isolamento**: o valor sai de `@MainActor` para `nonisolated`? de um actor para fora? de uma `Task` para uma closure `@Sendable`?
4. **`Task` herda o isolamento** do contexto onde foi criada. Use `Task { }` (herda) antes de `Task.detached { }` (não herda). Faça o isolamento inicial casar com o prefixo síncrono.
5. **Menor correção segura**, uma categoria por vez. Escape hatches só com invariante escrita e plano de remoção.

## 2. Diagnóstico → correção (primeira escolha → último recurso)

| Sintoma do compilador | Primeira escolha | Último recurso (com invariante e plano de remoção) |
| --- | --- | --- |
| Captura de tipo não-`Sendable` em closure `@Sendable` | Tornar o tipo `Sendable` de verdade: `struct` com membros `Sendable`; `final class` imutável; ou mover o estado para um `actor` | `@unchecked Sendable` com comentário da invariante (por exemplo, "acesso só sob `lock`") |
| Propriedade/método isolado a `@MainActor` usado de contexto `nonisolated` | Tornar o chamador `@MainActor`, ou `await` na fronteira | `MainActor.assumeIsolated { }` somente se provado que já está no main |
| Variável global/estática mutável "não é segura para concorrência" | Isolá-la a `@MainActor` ou a um `actor`; ou torná-la `let` imutável `Sendable` | `nonisolated(unsafe)` com invariante (por exemplo, "escrita só na inicialização") |
| Protocolo de framework antigo sem anotações | Conformar com isolamento explícito | `@preconcurrency import Framework` com plano de remoção |
| `Task.detached` capturando `self` | Trocar por `Task { }` no isolamento certo, ou método `async` chamado a partir de `.task` | — |
| Callback com handler (completion) | Embrulhar em `withCheckedContinuation`/`withCheckedThrowingContinuation`, retomando **exatamente uma vez** | — |

`@concurrent`, `nonisolated(nonsending)`, "approachable concurrency" e isolamento padrão do módulo são padrões que dependem da versão da toolchain (Xcode 26 / Swift 6.2): **confirme compilando**, não por nome (V-20).

## 3. Exemplo antes/depois (caso da view lenta de atualização de UI)

```swift
// Antes: captura self não-Sendable em Task.detached e volta ao main com GCD
final class ListVM: ObservableObject {
    @Published var items: [Item] = []
    func load() {
        Task.detached {
            let data = try await api.fetch()
            DispatchQueue.main.async { self.items = data }
        }
    }
}
```

```swift
// Depois (iOS 17+; api é um tipo Sendable, por exemplo struct ou actor)
@MainActor @Observable
final class ListVM {
    var items: [Item] = []
    var errorMessage: String?

    func load() async {
        do { items = try await api.fetch() }   // a atualização acontece no main actor
        catch { errorMessage = error.localizedDescription }
    }
}
// Na view: .task { await vm.load() }  (cancelada quando a view sai)
```

Notas: o `await` suspende sem bloquear o main; onde a chamada `api.fetch()` executa depende do isolamento de `fetch` e da toolchain (**Inferido**); trate erro explicitamente (o antes engolia o `try`). Em iOS 16, mantenha `ObservableObject` com `@MainActor` na classe e `@StateObject` na view.

## 4. Migração gradual (V-80, 5 passos)

1. Comece por um módulo externo (raiz, de que ninguém depende) ou por dependências próprias com estado global ou tipos implicitamente `Sendable`.
2. Permaneça no modo Swift 5 e habilite recursos upcoming **um a um** (`DisableOutwardActorInference`, `GlobalConcurrency`, `InferSendableFromCaptures`, em qualquer ordem), com problemas como avisos. Em SwiftPM: `.enableUpcomingFeature("GlobalConcurrency")` em `swiftSettings` (**Inferido**).
3. Ligue a verificação completa de concorrência no módulo.
4. Resolva os avisos com mudanças mínimas, descrevendo o que o código já faz; trate opt-outs inseguros como lista de melhorias futuras.
5. Itere para fora, sem exigir zero avisos antes de seguir.

Confira as flags contra a versão do Swift instalada (macOS/Xcode ou toolchain).

## 5. Verificação (loop de V-21)

Recompilar sem avisos **novos** e rodar testes. Sem macOS: "Não verificável". Testes novos de concorrência em Swift Testing (`@Test`, `#expect`); UI/performance em XCTest (V-66). Não misture APIs no mesmo teste.

## 6. O que não fazer

- Não adicionar `@unchecked Sendable` para calar o compilador.
- Não espalhar `@MainActor` em tudo por reflexo: ele resolve isolamento de UI, não de trabalho pesado.
- Não "corrigir" vários erros de categorias diferentes numa única mudança.
- Não afirmar que compila sem tê-lo feito.
