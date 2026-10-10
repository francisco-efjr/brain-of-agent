# React, Next.js e TypeScript em componentes

Regras de revisão e implementação para React 19, Next.js App Router (16.x) e TSX. Leia ao revisar componentes, decidir fronteira client/server, mexer em cache, escrever formulários com Actions ou tipar props. Versões lidas em 2026-10-10: React 19.3, Next.js 16.4.0, TanStack Query (docs `latest`). **Comece sempre lendo `package.json` e `next.config.*`.** Fontes: V-13, V-14, V-44, V-46, V-48, V-51, V-11.

## Sumário

- [Effects: três perguntas](#effects-três-perguntas)
- [Server e Client Components](#server-e-client-components)
- [Cache e renderização no Next.js 16.4: dois modelos](#cache-e-renderização-no-nextjs-164-dois-modelos)
- [Formulários com Actions](#formulários-com-actions)
- [Estado de servidor com TanStack Query](#estado-de-servidor-com-tanstack-query)
- [API de componentes e composição](#api-de-componentes-e-composição)
- [TypeScript em TSX: 8 regras](#typescript-em-tsx-8-regras)
- [React Compiler](#react-compiler)
- [Diagnóstico de hidratação](#diagnóstico-de-hidratação)

## Effects: três perguntas

Fonte: react.dev "You Might Not Need an Effect" (V-13, Verificado). Antes de aceitar um `useEffect`:

1. Existe sistema externo para sincronizar (DOM imperativo, socket, timer, biblioteca de terceiros)? Se não, provavelmente não precisa de Effect.
2. É consequência de uma ação do usuário? Então a lógica vai no event handler.
3. Pode ser calculado no render? Então calcule no render (valor derivado), não em estado sincronizado por Effect.

Sinal de revisão: Effect cujo corpo só chama `setState` a partir de props ou state. Reset de estado quando uma prop muda: use `key` no componente. Cálculo caro: `useMemo` só com medição (a página sugere medir com `console.time`) e lembrando do React Compiler. Stores externos: `useSyncExternalStore`. Busca de dados em Effect manual: cleanup com flag `ignore` para descartar resposta obsoleta; o preferível é biblioteca ou framework.

## Server e Client Components

Fonte: Next.js docs, Server and Client Components (16.4.0, atualizada em 2026-10-05; V-14, Verificado).

- Layouts e páginas são Server Components por padrão. `'use client'` declara a fronteira e leva ao bundle do cliente os imports e componentes renderizados diretamente.
- Reduza o bundle marcando só os componentes interativos (exemplo da doc: só o `Search` é cliente), não o layout.
- Props de servidor para cliente precisam ser serializáveis. Um Server Component pode ser passado como `children` a um Client Component.
- Providers de contexto o mais fundo possível, com `children`.
- Variáveis de ambiente sem prefixo `NEXT_PUBLIC_` não vão ao bundle do cliente (viram string vazia); com o prefixo, são públicas. **Segredo nunca leva `NEXT_PUBLIC_`.** O pacote `server-only` faz o build falhar se um módulo de servidor for importado no cliente.
- Componente de terceiros sem a diretiva: envolva em um Client Component próprio.

Checklist de fronteira: o componente usa estado, handler, efeito ou API de navegador? Então é Client, e folha. Tem segredo ou acesso a banco? `server-only`. Precisa de contexto? Provider fino com `children`. Biblioteca sem `'use client'`? Wrapper. Regra de revisão: nenhum layout inteiro marcado como client sem motivo.

## Cache e renderização no Next.js 16.4: dois modelos

Fontes: guias Caching, ISR e ISR com Cache Components (V-51, Verificado; atualizadas em outubro de 2026). **Nunca misture regras dos dois modelos.** Decida lendo `next.config.*`:

**Com `cacheComponents: true`** (a doc manda definir também `partialPrefetching: true`; deixar sem definir gera aviso; apps novos do `create-next-app` já vêm com ambos ligados e os dois serão padrão no próximo major):

- `'use cache'` em função (nível de dados) ou componente (nível de UI), pareado com `cacheLife`; `cacheTag` para invalidação pontual.
- Dado por requisição vai em `<Suspense>`, para o fallback fazer parte do shell estático.
- `Math.random()`, `Date.now()` e `crypto.randomUUID()` exigem `connection()` com `<Suspense>` ou `'use cache'`; `performance.now()` é exceção (telemetria).
- ISR segue o guia próprio: `generateStaticParams` define o que entra no build; URLs fora da lista recebem o App Shell na hora e o resultado completo é guardado em cache; com Partial Prefetching, `await params` vai dentro de `<Suspense>`.

**Sem Cache Components** (modelo anterior, "Caching (Previous Model)"):

- `export const revalidate = N` com stale-while-revalidate, `generateStaticParams`, `dynamicParams`, `revalidatePath` e `revalidateTag` (a regeneração ocorre na próxima requisição); falha na revalidação mantém o último dado bom; header `x-nextjs-cache` (`HIT`, `STALE`, `MISS`, `REVALIDATED`); intervalo alto recomendado (1 hora em vez de 1 segundo).

**Limites de ISR:** só Node.js (não funciona com static export); `revalidate = 0` ou `no-store` tornam a rota dinâmica; com várias instâncias, o cache em arquivo é por instância e a revalidação sob demanda só atinge a instância chamada, então use cache handler compartilhado (pedido de integração para `/devops-cloud-infra:playbook`); o Proxy não roda em revalidação sob demanda.

**Decisão por conteúdo (Inferido a partir das recomendações):** muda pouco, tempo de revalidação alto; evento de escrita, `revalidateTag` ou `revalidatePath`; tempo real, renderização dinâmica. O modelo muda rápido: anote a versão lida (16.4.0) e reconfira.

## Formulários com Actions

Fontes: react.dev `useActionState` (React 19.3) e Next.js, guia de formulários (16.4.0, atualizada em 2026-10-06; V-46, Verificado).

`const [state, formAction, isPending] = useActionState(action, initialState, permalink?)`. Detalhes verificados: `dispatchAction` precisa rodar dentro de uma Action ou `startTransition` (senão log de erro em dev); chamadas ficam em fila e rodam em sequência; erro lançado cancela as ações em fila e vai ao Error Boundary, erro esperado volta como estado; estado e payload precisam ser serializáveis; não há reset embutido. Com `useActionState` a ação recebe `prevState` primeiro e depois o `FormData`. `useFormStatus` precisa estar em componente filho do form.

Padrão "form com estado de erro":

1. Server Action com `'use server'`; **a primeira linha confere sessão e permissão**: a doc manda verificar autenticação e autorização dentro de cada Server Action, mesmo em página autenticada.
2. Valide com schema no servidor (Zod, Valibot ou equivalente) usando `safeParse`; em falha, **devolva** `{ errors }` em vez de lançar; lance só para erro inesperado.
3. O componente do form é Client Component com `useActionState`.
4. Botão com `disabled={isPending}`; mensagens em região `aria-live="polite"` e ligadas aos campos (ver `acessibilidade-wcag22.md`).
5. Argumentos fixos via `bind`; um campo `hidden` leva o valor no HTML, então não confie nele para dado sensível.
6. Feedback otimista com `useOptimistic` só quando houver reversão clara.

```tsx
'use server'
import { z } from 'zod' // exemplo; aceite o validador do projeto
const schema = z.object({ email: z.string().email() })

export async function cadastrar(prev: { errors?: Record<string, string[]> }, formData: FormData) {
  const sessao = await getSession() // verificar autenticação e autorização aqui, em toda action
  if (!sessao?.podeCadastrar) return { errors: { _form: ['Sem permissão.'] } }
  const r = schema.safeParse({ email: formData.get('email') })
  if (!r.success) return { errors: r.error.flatten().fieldErrors }
  await criarUsuario(r.data) // função do projeto
  return { errors: undefined }
}
```

(Exemplo ilustrativo escrito para este plugin; `getSession` e `criarUsuario` são funções do projeto, não de biblioteca.) Critério de saída: o envio funciona e mostra erro. Se o formulário precisa funcionar antes da hidratação, verifique o comportamento na versão instalada (Suposição: a página lida não afirma isso).

## Estado de servidor com TanStack Query

Fonte: "Important Defaults" (V-48, Verificado): queries nascem stale (`staleTime` 0); `gcTime` padrão de 5 minutos para queries inativas; falhas são repetidas 3 vezes com espera exponencial antes de exibir erro; refetch em foco da janela, reconexão e montagem; `staleTime` pode ser um tempo (por exemplo 2 minutos), `Infinity` (só invalida manualmente) ou `'static'` (nunca refaz, nem com invalidação manual).

Regras de revisão: dado de API vai para `useQuery` com `queryKey` que inclui todos os parâmetros e `staleTime` escolhido de propósito; trate `isPending`, `error` e `data`; antes de somar `retry`, lembre que já há 3 tentativas silenciosas. Estado de interface (modal aberto, aba ativa) não entra na query (Inferido: a página não traz esta regra). Mutations, invalidação e SSR com hidratação não foram lidos: Não verificado.

## API de componentes e composição

Base: `vercel-labs/agent-skills` `composition-patterns` (V-11, classe B; 8 regras; MIT declarado e não confirmado, só destilação). Checklist de revisão:

- Sem prop booleana que muda o comportamento do componente; prefira variantes explícitas ou componentes distintos.
- Componente composto com contexto compartilhado (`Tabs`, `Tabs.List`, `Tabs.Panel`); só o provider sabe como o estado é gerido.
- `children` em vez de props `renderX`.
- React 19 (apenas se o projeto for 19 ou superior): sem `forwardRef`, `use()` no lugar de `useContext()`. No React 19, `forwardRef` deixa de ser necessário e `ref` é passado como prop; `forwardRef` será descontinuado em versão futura (Verificado em https://react.dev/reference/react/forwardRef, 2026-10-10).

## TypeScript em TSX: 8 regras

Fontes: react.dev/learn/typescript (React 19.3) e TypeScript Handbook, JSX (V-44, Verificado). Os exemplos "ruim" são ilustrativos, escritos para este plugin.

1. **Props em `interface NomeProps` com JSDoc por campo.** Ruim: `function Button(p: { title: string; disabled: boolean })` repetido. Bom: `interface ButtonProps { /** texto do botão */ title: string; /** bloqueia clique */ disabled: boolean }`.
2. **Evento com o tipo do React.** Ruim: `(e: any) => ...`. Bom: `(e: React.ChangeEvent<HTMLInputElement>) => ...`; sem tipo específico, `React.SyntheticEvent`.
3. **`children`:** `React.ReactNode` para "qualquer coisa renderizável", `React.ReactElement` só para elementos JSX; não prometa "somente `<li>`", o tipo não garante.
4. **Estado finito com união, nunca `string`.** Ruim: `useState("idle")` (infere `string`). Bom: `useState<Status>("idle")` com `type Status = "idle" | "loading" | "success" | "error"`; para dados atrelados ao estado, união discriminada `{ status: "success"; data: T } | { status: "error"; error: Error }`.
5. **Contexto sem `any`.** Ruim: `createContext<Obj>(null as any)`. Bom: `createContext<Obj | null>(null)` mais um hook que lança erro se `null`, para o consumidor receber `Obj`.
6. **Callback memoizado com tipo de handler.** Ruim: `useCallback((e) => ..., [])` em strict. Bom: `useCallback<React.ChangeEventHandler<HTMLInputElement>>((e) => ..., [])`. Se o projeto usa React Compiler, não adicione `useCallback` por hábito.
7. **`style` com `React.CSSProperties`** em props de estilo.
8. **Reducer:** tipo de ação como união e `default` que lança. Ruim: `action: any` e ramo `default` que devolve `state`. Bom: `type Action = { type: "reset" } | { type: "setCount"; value: number }` e `default: throw new Error("Unknown action")`. A verificação de exaustividade com `never` é recurso do TypeScript (Inferido; não está na página do React).

Diagnóstico de JSX (Handbook): em `.tsx` a asserção `<T>x` não vale, use `x as T`; tag não declarada aparece em `JSX.IntrinsicElements`; erro de `children` incompatível vem de `JSX.ElementChildrenAttribute`; `JSX.ElementType` existe desde o TS 5.1; `JSX.Element` é caixa-preta. Prop obrigatória ausente, prop desconhecida e tipo de prop errado são erros de props do componente.

Critério de saída: `tsc --noEmit` sem erro novo (Inferido: comando padrão; confirme o script no `package.json`) e nenhum `any` introduzido sem comentário. **Lacuna:** genéricos em componentes, `satisfies`, `useRef` e `forwardRef` não foram lidos; Vue e Svelte com TypeScript também não. Trate como Não verificado e consulte a documentação.

## React Compiler

`useMemo` e `useCallback` por hábito entram em conflito com o React Compiler, que memoiza automaticamente (V-13, V-44). Antes de pedir ou remover memoização, descubra se o projeto usa o Compiler (config do bundler ou plugin do Babel no `package.json`) e só memoize com medição. Se não souber, pergunte; é uma dúvida material.

## Diagnóstico de hidratação

Nenhuma página primária de hidratação do React ou do Next foi lida neste plugin: as causas abaixo são **Inferidas** (conhecimento comum). Em "hydration mismatch", procure por: valores que mudam entre servidor e cliente (`Date.now()`, `Math.random()`, fuso e locale diferentes), leitura de `window`, `localStorage` ou `matchMedia` durante o render, HTML inválido aninhado (`<p>` dentro de `<p>`, `<div>` dentro de `<p>`), extensões do navegador que alteram o DOM. No Vue, V-52 confirma como fontes de mismatch valores aleatórios e fusos horários diferentes, e `data-allow-mismatch` a partir do Vue 3.5. Corrija na origem (renderize o valor dependente de cliente depois da montagem) antes de suprimir o aviso. Registre a hipótese como Inferida até reproduzir.
