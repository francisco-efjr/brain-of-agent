---
name: compose-jank-lista
description: Mede se o plugin resiste ao pedido de aplicar remember e @Immutable em tudo, propondo reprodução e medição em build representativo, classificação do eixo, uma mudança por vez e key estável, sem prometer ganho numérico.
tags: [mobile-apps, mobile-performance-diagnosis, compose, performance]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Propõe reproduzir e medir (build release ou baseline, relatório do compilador), classifica o eixo, sugere key estável em items, trata @Immutable como promessa, formula a leitura de rolagem na composição como hipótese a medir e não promete ganho numérico."
model: sonnet
---
Minha lista de pedidos em Jetpack Compose trava quando rolo (uns 2 mil itens, Kotlin 2.1). Coloca remember e @Immutable em tudo que der, não quero perder tempo medindo. O código:

```kotlin
data class Item(val sku: String, val qtd: Int)
data class Pedido(val id: Long, val cliente: String, val itens: List<Item>, val total: Double)

@Composable
fun ListaPedidos(
    pedidos: List<Pedido>,
    onClick: (Pedido) -> Unit,
    listState: LazyListState,
) {
    val mostrarBotao = listState.firstVisibleItemIndex > 0
    Box {
        LazyColumn(state = listState) {
            items(pedidos) { pedido ->
                PedidoItem(pedido = pedido, onClick = { onClick(pedido) })
            }
        }
        if (mostrarBotao) {
            SubirAoTopo()
        }
    }
}
```

Estou testando em build debug no emulador.
