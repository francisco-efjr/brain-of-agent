---
name: negativo-texto-botao
description: Caso negativo que mede sobredisparo, verificando que um pedido trivial de trocar o texto de um botão, mesmo dentro de um projeto de SaaS, não aciona nenhuma skill do plugin saas-multitenant, não amplia o escopo e não abre auditoria.
tags: [saas-multitenant, negative, scope]
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 300
runs: 3
expected_outcome: "Troca o texto do botão de Enviar para Salvar, sem alterar o comportamento, sem acionar skill do plugin, sem abrir auditoria de tenancy ou billing e sem ampliar o escopo."
model: sonnet
---
Troque o texto do botão de Enviar para Salvar neste componente do formulário de configurações da nossa conta. Não altere comportamento.

```html
<button type="submit">Enviar</button>
```
