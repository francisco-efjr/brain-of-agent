---
name: swiftui-review-legado
description: Mede se o plugin revisa SwiftUI legado respeitando o deployment target informado (iOS 16), sem impor @Observable nem arquitetura, corrigindo onTapGesture, dono do objeto e atualização de UI, e declarando que o build não foi verificado.
tags: [mobile-apps, swift-ios-review, swiftui, concurrency]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Achados com arquivo e linha para ObservedObject criado na view, onTapGesture, Task.detached e DispatchQueue.main.async; usa StateObject (não Observable) porque o alvo é iOS 16; declara o modo Swift como desconhecido e rotula como Suposição; build Não verificável."
model: sonnet
---
Revisa esse SwiftUI pra mim. É um app antigo, o deployment target é iOS 16 e eu não sei dizer qual é o modo da linguagem Swift nem as configurações de concorrência do projeto (só tenho o Xcode no notebook do trabalho, aqui estou sem ele).

```swift
// ListaTarefasView.swift
struct ListaTarefasView: View {
    @ObservedObject var vm = ListaTarefasVM()

    var body: some View {
        List(vm.tarefas) { tarefa in
            HStack {
                Image(systemName: tarefa.feita ? "checkmark.circle.fill" : "circle")
                    .onTapGesture { vm.alternar(tarefa) }
                Text(tarefa.titulo)
            }
        }
        .onAppear { vm.carregar() }
    }
}

final class ListaTarefasVM: ObservableObject {
    @Published var tarefas: [Tarefa] = []

    func carregar() {
        Task.detached {
            let itens = try await API.shared.buscarTarefas()
            DispatchQueue.main.async { self.tarefas = itens }
        }
    }

    func alternar(_ t: Tarefa) {
        if let i = tarefas.firstIndex(where: { $0.id == t.id }) { tarefas[i].feita.toggle() }
    }
}
```
