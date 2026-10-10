---
name: flutter-camadas-negativo-proximo
description: Caso negativo próximo que mede se o plugin, diante de uma pergunta de arquitetura Flutter, aciona a revisão de arquitetura mobile, responde com camadas Flutter (View, ViewModel, Repository, Service) respeitando o Provider já usado e não aciona a skill de Swift.
tags: [mobile-apps, mobile-architecture-review, flutter, negative-near]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Propõe camadas Flutter com View e ViewModel 1:1, repositório como fonte de verdade e services sem estado, mantém o Provider existente, trata a escolha de pacotes como opinião, não menciona SwiftUI e não aciona swift-ios-review."
model: sonnet
---
Estou estruturando um app Flutter e uso Provider para estado. Hoje as telas chamam o pacote http direto dentro do initState e fazem setState. A estrutura atual é esta:

```text
lib/
  main.dart
  models/pedido.dart
  providers/pedidos_provider.dart
  screens/pedidos_screen.dart      // http.get dentro do initState
  screens/detalhe_screen.dart      // outro http.get, parseando o JSON na tela
```

Como organizo as camadas?
