---
name: negativo-react-hook
description: "Caso negativo de quase-acerto lexical: pergunta sobre hook do React (useEffect) que compartilha a palavra hook com o guardrail do Claude Code; nenhuma skill do plugin deve disparar."
tags: [automation-integrations, negativo, quase-acerto, react]
runs: 3
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 240
expected_outcome: "Explica o laço de renderização causado pelo useEffect e propõe a correção em React, sem acionar skill do plugin automation-integrations e sem tratar a pergunta como hook do Claude Code."
---
Meu hook customizado `useContador` entra em loop infinito de renderização no React 18. O componente fica re-renderizando sem parar e a aba trava. Aqui está o código:

```jsx
import { useEffect, useState } from "react";

export function useContador(itens) {
  const [total, setTotal] = useState(0);
  useEffect(() => {
    setTotal(itens.length);
  }, [itens, setTotal, total]);
  return total;
}

export function Painel() {
  const total = useContador([1, 2, 3]);
  return <p>Total: {total}</p>;
}
```

Qual é a causa e como eu conserto?
