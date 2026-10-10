---
name: componente-react-next
description: Mede se o plugin revisa um layout Next.js marcado inteiro como client e um carrinho com Effects que só copiam estado derivado, aplicando as três perguntas de Effect, movendo a busca para o servidor, evitando memoização por reflexo e rotulando a versão e o modelo de cache como premissa.
tags: [web-frontend, component-review, react, nextjs, effects, client-server]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Aponta o layout inteiro como client sem motivo e a busca em useEffect, propõe busca no servidor e cliente apenas nas folhas interativas, identifica total e visiveis como estado derivado a calcular no render com as três perguntas, não adiciona useMemo por hábito e declara a versão do Next e o modelo de cache como premissa ou pergunta."
model: sonnet
---
Estamos num projeto Next.js com App Router. Revisa estes dois arquivos: o layout carrega tudo no cliente e o carrinho me parece ter efeito demais. Quero saber o que está errado e como ficaria o certo, sem reescrever o projeto.

```tsx
// app/layout.tsx
'use client';
import { useEffect, useState } from 'react';
import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<{ name: string } | null>(null);

  useEffect(() => {
    fetch('/api/me')
      .then((r) => r.json())
      .then(setUser);
  }, []);

  return (
    <html lang="pt-BR">
      <body>
        <header>{user ? `Olá, ${user.name}` : 'Entrar'}</header>
        {children}
      </body>
    </html>
  );
}
```

```tsx
// app/carrinho/Cart.tsx
'use client';
import { useEffect, useState } from 'react';

type Item = { id: string; nome: string; preco: number; qtd: number; ativo: boolean };

export function Cart({ items }: { items: Item[] }) {
  const [busca, setBusca] = useState('');
  const [visiveis, setVisiveis] = useState<Item[]>([]);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    setVisiveis(items.filter((i) => i.ativo && i.nome.includes(busca)));
  }, [items, busca]);

  useEffect(() => {
    setTotal(visiveis.reduce((soma, i) => soma + i.preco * i.qtd, 0));
  }, [visiveis]);

  return (
    <section>
      <input value={busca} onChange={(e) => setBusca(e.target.value)} aria-label="Buscar no carrinho" />
      <ul>
        {visiveis.map((i) => (
          <li key={i.id}>{i.nome} x {i.qtd}</li>
        ))}
      </ul>
      <p>Total: R$ {total.toFixed(2)}</p>
    </section>
  );
}
```
