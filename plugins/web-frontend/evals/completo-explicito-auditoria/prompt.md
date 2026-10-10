---
name: completo-explicito-auditoria
description: Mede o modo FRONTEND-COMPLETO pedido de forma explícita pelo usuário para uma auditoria somente leitura. Verifica o contrato (só relata), a leitura em lotes das referências com registro, a matriz de aplicabilidade com NA e NV justificados, um único modelo de cache, os achados com evidência e o resultado final em concluído, parcial ou impedido.
tags: [web-frontend, playbook, complete-mode, audit, read-only]
max_turns: 24
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit]
timeout_seconds: 900
runs: 3
expected_outcome: "Declara o contrato de auditoria somente leitura, lê as referências em lotes registrando caminho e situação, monta a matriz de aplicabilidade por área com Aplicável, NA com motivo e NV, aponta o conflito entre revalidate e cacheComponents, Date.now sem tratamento, card clicável sem semântica e imagem sem alt, não edita arquivos, não marca nada como executado e conclui com concluído, parcial ou impedido justificado."
model: sonnet
---
FRONTEND-COMPLETO: audite este projeto Next.js. É só auditoria, não altere nenhum arquivo. Não tenho acesso a um ambiente para rodar o projeto agora; o que está abaixo é tudo o que tenho aqui.

```json
// package.json (trecho)
{
  "name": "loja-serra",
  "scripts": { "dev": "next dev", "build": "next build", "lint": "eslint ." },
  "dependencies": { "next": "16.4.0", "react": "19.3.0", "react-dom": "19.3.0", "tailwindcss": "4.3.0" }
}
```

```ts
// next.config.ts
import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  cacheComponents: true,
};

export default nextConfig;
```

```tsx
// app/page.tsx
import { ProductCard } from '@/components/ProductCard';

export const revalidate = 60;

export default async function Home() {
  const res = await fetch('https://api.example.test/produtos');
  const produtos: { id: string; nome: string; preco: number; foto: string }[] = await res.json();

  return (
    <main>
      <h1>Loja Serra</h1>
      <p>Atualizado às {new Date(Date.now()).toLocaleTimeString('pt-BR')}</p>
      {produtos.map((p) => (
        <ProductCard key={p.id} produto={p} />
      ))}
    </main>
  );
}
```

```tsx
// components/ProductCard.tsx
'use client';

type Produto = { id: string; nome: string; preco: number; foto: string };

export function ProductCard({ produto }: { produto: Produto }) {
  return (
    <div className="card" onClick={() => (window.location.href = `/produto/${produto.id}`)}>
      <img src={produto.foto} />
      <h2>{produto.nome}</h2>
      <span>R$ {produto.preco}</span>
    </div>
  );
}
```
