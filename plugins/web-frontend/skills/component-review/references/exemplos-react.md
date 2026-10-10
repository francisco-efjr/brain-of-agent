# Exemplos ruim/bom para component-review

Exemplos "ruim" escritos por nós para ilustrar; os princípios vêm de V-13 (React, Effects), V-14 (Next.js, Server e Client Components), V-44 (React e TypeScript) e V-11 (composição). Confirme as versões do projeto antes de aplicar: React 19.3 e Next.js 16.4.0 foram lidos em 2026-10-10.

## Sumário

1. Effect que só deriva estado
2. Reset de estado por `key`
3. Fetch em Effect (quando não há biblioteca)
4. Fronteira client/server
5. Oito regras de tipos TSX
6. API de componente

## 1. Effect que só deriva estado

```tsx
// Ruim: dois Effects que só chamam setState a partir de props e estado.
// Cada um causa um render extra, e `total` fica um passo atrás de `filtered`.
'use client';
export function Cart({ items }: { items: Item[] }) {
  const [filter, setFilter] = useState('');
  const [filtered, setFiltered] = useState<Item[]>([]);
  const [total, setTotal] = useState(0);
  useEffect(() => { setFiltered(items.filter((i) => i.name.includes(filter))); }, [items, filter]);
  useEffect(() => { setTotal(filtered.reduce((s, i) => s + i.price * i.qty, 0)); }, [filtered]);
  // ...
}
```

```tsx
// Bom: o que é calculável vai no render. Só `filter` é estado.
'use client';
interface CartProps {
  /** itens já carregados pelo servidor */
  items: Item[];
}
export function Cart({ items }: CartProps) {
  const [filter, setFilter] = useState('');
  const filtered = items.filter((i) => i.name.includes(filter));
  const total = filtered.reduce((s, i) => s + i.price * i.qty, 0);
  // ...
}
```

Perguntas aplicadas: (a) sistema externo? não; (b) consequência de ação do usuário? o filtro muda por handler, o resto é derivação; (c) calculável no render? sim. `useMemo` em `filtered` só se medição mostrar custo, ou se o projeto não usa React Compiler e a lista é grande (V-13).

## 2. Reset de estado por `key`

```tsx
// Ruim: Effect para "zerar" o rascunho quando o usuário muda.
useEffect(() => { setDraft(''); }, [userId]);

// Bom: a identidade muda, o estado interno nasce de novo.
<ProfileForm key={userId} userId={userId} />
```

## 3. Fetch em Effect (só quando não há biblioteca ou framework de dados)

```tsx
useEffect(() => {
  let ignore = false; // evita que a resposta da consulta antiga sobrescreva a nova
  fetchResults(query).then((json) => {
    if (!ignore) setResults(json);
  });
  return () => { ignore = true; };
}, [query]);
```

Preferência: buscar no servidor (Server Component, `load`, loader) ou usar biblioteca de dados (TanStack Query com `queryKey` completa; ver `forms-and-data`). Tratar `error` e carregando, não só `data`.

## 4. Fronteira client/server (Next App Router)

```tsx
// app/layout.tsx: Server Component (sem diretiva). Header e Footer ficam fora do bundle do cliente.
import { MenuToggle } from './menu-toggle';
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <header><MenuToggle /></header>
        {children}
      </body>
    </html>
  );
}
```

```tsx
// app/menu-toggle.tsx: cliente folha, só o que é interativo.
'use client';
import { useState } from 'react';
export function MenuToggle() {
  const [open, setOpen] = useState(false);
  return (
    <button type="button" aria-expanded={open} onClick={() => setOpen(!open)}>
      Menu
    </button>
  );
}
```

Provider fino: o provider é cliente e recebe `children`; os filhos continuam Server Components.

```tsx
// app/theme-provider.tsx
'use client';
import { createContext, useState } from 'react';
export const ThemeContext = createContext<'claro' | 'escuro'>('claro');
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [tema] = useState<'claro' | 'escuro'>('claro');
  return <ThemeContext value={tema}>{children}</ThemeContext>; // React 19: o contexto é o próprio provider
}
```

Em React 18, escreva `<ThemeContext.Provider value={tema}>`. Confirme a versão.

Biblioteca de terceiros sem diretiva: envolva num arquivo cliente próprio (`'use client'; export { Carousel as default } from 'lib';`) e importe o wrapper. Segredo em módulo de servidor: `import 'server-only'` no topo (erro de build se for importado por cliente). `NEXT_PUBLIC_*` é público por definição; sem o prefixo, a variável não vai ao bundle do cliente (V-14).

## 5. Oito regras de tipos TSX (V-44)

| # | Regra | Ruim | Bom |
| --- | --- | --- | --- |
| 1 | Props em `interface` com JSDoc por campo | `function Button(p: { title: string; disabled: boolean })` repetido | `interface ButtonProps { /** texto do botão */ title: string; /** bloqueia o clique */ disabled: boolean }` |
| 2 | Eventos com tipo do React | `(e: any) => ...` | `(e: React.ChangeEvent<HTMLInputElement>) => ...`; sem tipo específico, `React.SyntheticEvent` |
| 3 | `children` | `children: any` | `React.ReactNode` para "qualquer coisa renderizável"; `React.ReactElement` só para elementos JSX; o tipo não garante "só `<li>`" |
| 4 | Estado finito como união | `useState("idle")` (infere `string`) | `type Status = "idle" \| "loading" \| "success" \| "error"` e `useState<Status>("idle")`; com dados atrelados, união discriminada `{ status: "success"; data: T } \| { status: "error"; error: Error }` |
| 5 | Contexto sem `any` | `createContext<Obj>(null as any)` | `createContext<Obj \| null>(null)` e hook que lança se `null` |
| 6 | Callback memoizado | `useCallback((e) => ..., [])` em strict | `useCallback<React.ChangeEventHandler<HTMLInputElement>>((e) => ..., [])`; com Compiler, não adicione por hábito |
| 7 | Estilo | `style: object` | `React.CSSProperties` |
| 8 | Reducer | `action: any`; `default` devolve `state` | `type Action = { type: "reset" } \| { type: "setCount"; value: number }` e `default: throw new Error("Unknown action")` |

Diagnóstico de JSX (handbook do TypeScript): em `.tsx` a asserção `<T>x` não vale, use `x as T`; tag desconhecida aponta para `JSX.IntrinsicElements`; prop obrigatória ausente ou de tipo errado é erro do componente, não do JSX. Lacunas não cobertas pelas fontes lidas: genéricos em componentes, `satisfies`, `useRef`, `forwardRef` além do básico: trate como Não verificado e consulte a documentação. Básico Verificado (https://react.dev/reference/react/forwardRef, 2026-10-10): no React 19 `ref` é prop e `forwardRef` deixa de ser necessário.

## 6. API de componente (V-11)

```tsx
// Ruim: booleanos que mudam o comportamento; cada combinação nova vira if.
<Dialog isConfirm hasFooter isDanger title="Excluir?" />

// Bom: composição com contexto compartilhado; variante explícita no lugar de modo.
<Dialog variant="danger">
  <Dialog.Title>Excluir cliente?</Dialog.Title>
  <Dialog.Body>Esta ação remove 12 pedidos associados.</Dialog.Body>
  <Dialog.Footer>
    <Button onClick={cancelar}>Cancelar</Button>
    <Button variant="danger" onClick={excluir}>Excluir</Button>
  </Dialog.Footer>
</Dialog>
```

`children` no lugar de props `renderHeader`, `renderFooter`. Só o provider sabe como o estado é gerido; os filhos consomem a interface. Em React 19 ou superior, `ref` é prop e `use()` lê contexto; em 18, `forwardRef` e `useContext`.

Atribuição: princípios destilados de documentação pública (React, Next.js, TypeScript) e de material da Vercel (`composition-patterns`, MIT declarado, não confirmado); redação própria, sem texto copiado.
