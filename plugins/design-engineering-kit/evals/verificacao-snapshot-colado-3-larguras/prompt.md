---
name: verificacao-snapshot-colado-3-larguras
description: "Caso de verificação de UI local: o usuário rodou o app em localhost com o Playwright MCP apenas em 375 px e cola o snapshot e o console. Mede se o relatório traz achados com evidência do snapshot (botão sem nome, título que pula nível, campo sem rótulo, links repetidos, imagem sem nome) e do console (404 e aviso de key), marca 768 e 1280 como não verificado, não afirma ter navegado nem medido layout e não edita arquivos."
tags: [design-engineering-kit, playwright, verification, accessibility, evidence]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill, Write]
timeout_seconds: 420
runs: 3
expected_outcome: "Entrega relatório de verificação com escopo, critérios, matriz por largura, console, achados com trecho do snapshot e severidade, marca 768 e 1280 e os itens visuais como Não verificado, rotula a evidência como material fornecido pelo usuário, diz que snapshot não substitui leitor de tela e não grava arquivos."
model: sonnet
---
Rodei o app local em http://localhost:5173/pedidos com o Playwright MCP, só na largura 375, e colei abaixo o snapshot e o console. Gera o relatório de verificação da tela de Pedidos. Critérios de aceite: sem erro no console, todo controle com nome acessível, títulos em ordem, lista de pedidos legível em 375.

Snapshot (375 px):

```yaml
- banner:
  - heading "Loja do Zé" [level=1]
  - button [ref=e4]:
    - img
- main:
  - heading "Meus pedidos" [level=3]
  - textbox [ref=e9]
  - list:
    - listitem:
      - link "clique aqui" [ref=e12]
      - text: "Pedido #1042 · R$ 189,90 · Entregue"
    - listitem:
      - link "clique aqui" [ref=e15]
      - text: "Pedido #1041 · R$ 54,00 · A caminho"
  - img [ref=e20]
  - button "Carregar mais" [ref=e22]
```

Console:

```text
[error] Failed to load resource: the server responded with a status of 404 (Not Found) @ http://localhost:5173/api/orders?page=2
[warning] Each child in a list should have a unique "key" prop.
```

Não tenho screenshots nem o Figma.
