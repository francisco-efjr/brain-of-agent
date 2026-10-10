---
name: perf-lcp-hero
description: Mede se o plugin diagnostica um LCP ruim a partir da evidência fornecida, decompondo em subpartes, apontando lazy-load e render client-side no elemento LCP, sem prometer ganhos numéricos, sem tratar laboratório como campo e propondo remedir nas mesmas condições.
tags: [web-frontend, perf-audit, core-web-vitals, lcp]
max_turns: 12
allowed_tools: [Read, Glob, Grep, Skill]
timeout_seconds: 600
runs: 3
expected_outcome: "Identifica loading=lazy no elemento LCP, a imagem só existir depois da hidratação, os atrasos de carregamento (cerca de 27%) e de renderização (cerca de 40%) acima do orçamento, propõe imagem no HTML inicial sem lazy com fetchpriority moderado, diz que INP exige dado de campo e manda remedir nas mesmas condições sem prometer segundos."
model: sonnet
---
A home da nossa loja está lenta no celular e o time de produto quer saber por quê. Rodei o Lighthouse e colei o resumo abaixo, junto com o componente do hero. Me diz onde está o problema e o que mudar, em ordem de prioridade.

```text
Lighthouse 2026-10-09, build de produção local, móvel emulado (Slow 4G, CPU 4x)
LCP: 4,8 s    CLS: 0,03    TBT: 120 ms    INP: não medido (só laboratório)
Elemento LCP: img.hero  (imagem principal da home)
Subpartes do LCP: TTFB 0,9 s | atraso de carregamento 1,3 s | duração do carregamento 0,7 s | atraso de renderização 1,9 s
```

```tsx
// components/Hero.tsx
'use client';
import { useEffect, useState } from 'react';

export function Hero() {
  const [pronto, setPronto] = useState(false);
  useEffect(() => {
    setPronto(true);
  }, []);

  if (!pronto) return <div className="hero-skeleton" />;
  return (
    <img src="/img/hero.jpg" alt="Equipe da loja" className="hero" loading="lazy" width={1600} height={900} />
  );
}
```
