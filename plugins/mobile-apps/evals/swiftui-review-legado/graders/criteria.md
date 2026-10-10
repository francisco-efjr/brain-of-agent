---
type: llm
---
PASS if todos os itens abaixo são observáveis na resposta final:
1. Declara que o modo Swift e a configuração de concorrência são desconhecidos e que a recomendação depende deles (assume o caso conservador e rotula como Suposição, ou diz o que ler em Package.swift e .xcconfig), sem propor editar o arquivo `.pbxproj`.
2. Aponta `@ObservedObject var vm = ListaTarefasVM()` criado dentro da view como problema de dono do objeto e recomenda `@StateObject` (ou equivalente correto) porque o alvo é iOS 16; se mencionar `@Observable` com `@State`, deixa claro que é iOS 17 ou superior e não se aplica ao alvo atual.
3. Aponta `onTapGesture` em uma imagem como problema de acessibilidade e recomenda `Button` com rótulo acessível.
4. Aponta `Task.detached` combinado com `DispatchQueue.main.async` e captura de `self` como ponto de concorrência, e recomenda atualizar o estado no main actor (por exemplo `@MainActor` no tipo ou no método) pela menor mudança segura, sem recomendar `@unchecked Sendable` como solução.
5. Cada achado traz arquivo e linha (ou trecho exato), o antes e depois mínimo, e um rótulo (Verificado, Inferido, Suposição); não inventa problemas que não estão no código.
6. Diz que revisou por leitura e que compilar e rodar testes é Não verificável neste ambiente (sem macOS e Xcode).
FAIL if qualquer um ocorrer: recomenda `@Observable` ou `@Bindable` sem ressalva de versão para um alvo iOS 16; afirma que o código compila ou foi testado; impõe MVVM, TCA ou outra arquitetura; recomenda `@unchecked Sendable` ou `nonisolated(unsafe)` sem invariante; cita API que não existe.
