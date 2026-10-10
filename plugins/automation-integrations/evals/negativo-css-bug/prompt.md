---
name: negativo-css-bug
description: "Caso negativo: pedido de CSS sem relação com automação, integrações ou MCP; nenhuma skill do plugin deve disparar."
tags: [automation-integrations, negativo, css, fora-de-escopo]
runs: 3
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 240
expected_outcome: "Resolve o problema de CSS no Safari sem acionar nenhuma skill do plugin automation-integrations e sem desviar para automação."
---
O botão "Enviar" do meu formulário de contato em React fica desalinhado só no Safari (iPhone e Mac): ele ultrapassa a largura do campo de texto e o texto dentro dele fica mais para cima. No Chrome está perfeito. Aqui está o código:

```jsx
export function Contato() {
  return (
    <form className="contato">
      <label>
        Mensagem
        <textarea rows="4" />
      </label>
      <button type="submit" className="btn-enviar">Enviar</button>
    </form>
  );
}
```

```css
.contato { display: flex; flex-direction: column; gap: 12px; width: 320px; }
.contato textarea { width: 100%; padding: 8px; border: 1px solid #ccc; }
.btn-enviar { width: 100%; padding: 12px; border: 0; background: #0a66c2; color: #fff; line-height: 1; }
```

O que está causando isso e como corrijo?
