---
name: revisao-motion-componente
description: "Caso de revisão de motion por leitura: trechos de CSS e TSX com transition all, ease-in, scale zero, origem no centro, hover sem portão, toast com keyframes, command palette animada por atalho e nenhuma regra de reduzir movimento, mais um token de painel de 500 ms do design system. Mede se a revisão usa tabela Before/After/Why, cobre os padrões principais, trata o token do sistema como divergência e não como bloqueio, dá veredito explícito e declara que a sensação de movimento não é verificável por leitura."
tags: [design-engineering-kit, motion, review, emil, design-system-precedence]
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 480
runs: 3
expected_outcome: "Revisa por leitura com tabela Before/After/Why e local de cada trecho, cobre ao menos seis problemas, aponta o token de 500 ms como decisão do design system, entrega veredito Block com justificativa, diz que sensação de movimento não é verificável por leitura e não edita arquivos."
model: sonnet
---
Revisa o motion destes componentes antes do merge. Só tenho esses trechos. O popover abre a partir do botão "Filtros".

```css
/* src/ui/popover.css */
.popover {
  position: absolute;
  transform: scale(0);
  transform-origin: center;
  transition: all 400ms ease-in;
}
.popover[data-open="true"] {
  transform: scale(1);
}
.btn:hover {
  transform: translateY(-2px);
}
.toast {
  animation: toast-in 600ms ease-in-out;
}
@keyframes toast-in {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
.sheet {
  transition: transform var(--motion-panel) var(--ease-out);
}
```

```tsx
// src/ui/CommandPalette.tsx
useHotkey("mod+k", () => setOpen(true));
return (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.45 }}
  />
);
```

```css
/* src/styles/tokens.css (design system do projeto) */
:root {
  --ease-out: cubic-bezier(.2, .8, .2, 1);
  --motion-panel: 500ms;
}
```

Não existe nenhuma regra com `prefers-reduced-motion` no projeto.
